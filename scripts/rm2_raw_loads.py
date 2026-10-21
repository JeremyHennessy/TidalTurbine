"""Reduce six checksum-pinned 2 kHz original NI rig records; NO blade stress.

Uses upstream RM2 code transformations, source t1/t2 and tare-drag
values. Descriptive raw support drag and shaft torque are not fatigue.
Requires optional numpy/h5py only for --analyze-dir (not normal CI).
"""
from pathlib import Path
import argparse
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"research/benchmarks/RM2_RAW_SIX_SOURCE_MANIFEST.json"
REPORT=ROOT/"reports/RM2-RAW-LOADS-001.json"
TARE_DRAG={0.4:8.092422052240382,1.0:46.64324118685838,1.2:66.90768309869615}
RHO=1000.0
D=1.075
H=0.807
COEFF_TARE_SLOPE=0.00104768276035
COEFF_TARE_INTERCEPT=-0.848866229797

def sha256(path):
    dig=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):dig.update(b)
    return dig.hexdigest()

def load_manifest():
    m=json.loads(MANIFEST.read_text(encoding="utf8"))
    if m["schema"]!="RM2-RAW-SIX-NI-SOURCE-MANIFEST-001" or len(m["trials"])!=6:
        raise ValueError("Unexpected raw source manifest")
    if m["source_data_committed_to_git"] or m["selected_trial_count"]!=6:
        raise ValueError("Raw source custody invalid")
    return m

def rounded(value):
    f=float(value)
    if not math.isfinite(f):
        raise ValueError("Nonfinite derived metric")
    return round(f,6)

def require_bytes(path,spec):
    if not path.exists() or path.stat().st_size!=spec["bytes"] or sha256(path)!=spec["sha256"]:
        raise ValueError("Raw source bytes/hash mismatch: "+str(path))

def read_trial(folder,source):
    import numpy as np
    import h5py
    name=source["trial_id"]; speed=float(source["nominal_speed_m_s"]);run=source["run"]
    path=folder/(name+"_nidata.h5")
    meta=folder/(name+"_metadata.json")
    require_bytes(path,source["ni"])
    require_bytes(meta,source["metadata"])
    settings=json.loads(meta.read_text("utf8"))
    if abs(float(settings["Tow speed (m/s)"])-speed)>0.001 or abs(
        float(settings["Tip speed ratio"])-(2.9 if run==10 else 3.1))>0.001:
        raise ValueError("Metadata operating point mismatch "+name)
    channel_info=settings["NI metadata"]["Channel info"]
    for key,unit in (("torque_trans","Nm"),("drag_left","N"),("drag_right","N")):
        if channel_info[key]["Scaled units"]!=unit:
            raise ValueError("Unverified source units "+key)
    if channel_info["turbine_angle"]["Units"]!="Degrees" or channel_info["carriage_pos"]["Units"]!="m":
        raise ValueError("Unverified NI encoder units")
    if float(settings["NI metadata"]["Sample rate (Hz)"])!=2000:
        raise ValueError("Unexpected NI sample rate")

    with h5py.File(path,"r") as h:
        data=h["data"]
        channels=("time","carriage_pos","torque_trans","drag_left","drag_right","turbine_angle")
        x={key:np.asarray(data[key][...],dtype=np.float64) for key in channels}
    t=x["time"];n=len(t);dt=float(t[1]-t[0])
    if n<10000 or any(len(x[k])!=n or not np.isfinite(x[k]).all() for k in channels):
        raise ValueError("Invalid sample arrays")
    if abs(dt-1/2000)>1e-8 or np.max(np.abs(np.diff(t)-dt))>1e-8:
        raise ValueError("Timebase not uniform 2kHz")

    # Published upstream processing source: first 2-second zero reference
    # and separately measured apparatus tare drag.
    raw_drag=x["drag_left"]+x["drag_right"]
    tare_at_rest=float(np.mean(raw_drag[t<2.]))
    drag=raw_drag-tare_at_rest-TARE_DRAG[speed]

    # Angle encoded in degrees; source uses second-order differentiation,
    # 8-sample smoothing and /6 to form RPM. Proxy here uses centered
    # finite difference and 8-point moving average; no exact upstream
    # signal filter equivalence or independent sensor calibration claimed.
    rpm=np.convolve(np.gradient(x["turbine_angle"],dt)/6.,
                    np.ones(8)/8,mode="same")
    omega=rpm*np.pi/30.
    torque=x["torque_trans"]+COEFF_TARE_SLOPE*rpm+COEFF_TARE_INTERCEPT
    # Carriage position differentiation, source's 100-sample smoothing;
    # steady interval velocity is independently checked against nominal U.
    u=np.convolve(np.gradient(x["carriage_pos"],dt),
                  np.ones(100)/100,mode="same")
    t1,t2=source["source_time_window_s"]
    mask=(t>=t1)&(t<t2)
    count=int(np.sum(mask))
    if count<1000 or count>=n or np.min(u[mask])<=0.2:
        raise ValueError("Invalid steady tow window or carriage speed")
    area=D*H
    cp=torque[mask]*omega[mask]/(.5*RHO*area*u[mask]**3)
    cd=drag[mask]/(.5*RHO*area*u[mask]**2)
    cp_mean=float(np.mean(cp));cd_mean=float(np.mean(cd))
    # Tolerance checks are gross preservation and reduction sanity only:
    # original processing uses different differential/smoothing and
    # blade-pass-aligned window rules; NOT independently validated model.
    if abs(cp_mean-source["source_mean_cp"])>0.006 or abs(cd_mean-source["source_mean_cd"])>0.006:
        raise ValueError(f"Unable to reproduce published processed means within predefined 0.006: {name} Cp {cp_mean} Cd {cd_mean}")

    torque_win=torque[mask];drag_win=drag[mask];ang=np.mod(x["turbine_angle"][mask],360)
    def describe(x):
        return {"mean":rounded(np.mean(x)), "std":rounded(np.std(x)),
                "min":rounded(np.min(x)),"max":rounded(np.max(x)),
                "p05":rounded(np.percentile(x,5)),"p95":rounded(np.percentile(x,95))}
    def phase_means(arr):
        ids=np.minimum((ang//10).astype(int),35)
        counts=np.bincount(ids,minlength=36)
        if (counts<100).any():raise ValueError("Too few samples per phase bin")
        means=np.bincount(ids,weights=arr,minlength=36)/counts
        return {"bin_midpoints_deg":[i*10+5 for i in range(36)],
                "means":[rounded(x) for x in means],
                "sample_count_range":[int(np.min(counts)),int(np.max(counts))],
                "peak_to_peak_of_phase_averages":rounded(np.ptp(means))}
    return {
      "trial_id":name,"nominal_speed_m_s":speed,"nominal_tsr":2.9 if run==10 else 3.1,
      "source_processed_reference":{"source_mean_cp":source["source_mean_cp"],
        "source_mean_cd":source["source_mean_cd"],"source_n_revolutions":source["source_n_revolutions"],
        "source_window_s":[t1,t2]},
      "raw_ni_sha256":source["ni"]["sha256"],"raw_ni_bytes":source["ni"]["bytes"],
      "metadata_sha256":source["metadata"]["sha256"],"source_units_metadata_verified":True,
      "sample_rate_hz":2000,"raw_record_samples":n,"steady_window_samples":count,
      "source_steady_window_s":[t1,t2],
      "mean_tow_speed_m_s":rounded(np.mean(u[mask])),
      "mean_rpm":rounded(np.mean(rpm[mask])),
      "mean_shaft_mechanical_power_w":rounded(np.mean(torque_win*omega[mask])),
      "mean_cp_proxy":rounded(cp_mean),"mean_cd_proxy":rounded(cd_mean),
      "cp_reproduction_abs_error":rounded(abs(cp_mean-source["source_mean_cp"])),
      "cd_reproduction_abs_error":rounded(abs(cd_mean-source["source_mean_cd"])),
      "rig_shaft_torque_nm":describe(torque_win),
      "rig_support_streamwise_drag_n":describe(drag_win),
      "rig_shaft_torque_phase_mean":phase_means(torque_win),
      "rig_support_drag_phase_mean":phase_means(drag_win),
      "research_boundaries":[
        "NI rig-support force and rotary shaft torque are NOT blade-root bending stress",
        "Phase-binned profiles average 9-14 revolutions over one historical tow, not independently sampled fatigue histories",
        "Source NI transducer calibration declared in metadata, not independently reverified",
        "No direct measured delivered electrical/PTO/actuator net energy",
        "No field turbulence, third-party instrument failure/sensor phase response or statistical significance",
        "Raw binary measurements remain in temporary external artifact, not Git"
      ]
    }

def make_report(folder):
    manifest=load_manifest()
    trials=[read_trial(folder,source) for source in manifest["trials"]]
    pairs=[]
    for speed in (0.4,1.0,1.2):
        a=next(x for x in trials if x["nominal_speed_m_s"]==speed and x["nominal_tsr"]==2.9)
        b=next(x for x in trials if x["nominal_speed_m_s"]==speed and x["nominal_tsr"]==3.1)
        def pct(sa,sb):
            return rounded(100*(sa/sb-1))
        pairs.append({
          "nominal_speed_m_s":speed,"candidate_trial_id":a["trial_id"],
          "reference_trial_id":b["trial_id"],
          "shaft_mean_torque_change_percent":pct(a["rig_shaft_torque_nm"]["mean"],b["rig_shaft_torque_nm"]["mean"]),
          "shaft_torque_std_change_percent":pct(a["rig_shaft_torque_nm"]["std"],b["rig_shaft_torque_nm"]["std"]),
          "support_mean_drag_change_percent":pct(a["rig_support_streamwise_drag_n"]["mean"],b["rig_support_streamwise_drag_n"]["mean"]),
          "support_drag_p95_change_percent":pct(a["rig_support_streamwise_drag_n"]["p95"],b["rig_support_streamwise_drag_n"]["p95"]),
          "support_drag_std_change_percent":pct(a["rig_support_streamwise_drag_n"]["std"],b["rig_support_streamwise_drag_n"]["std"]),
          "rig_phase_mean_torque_ptp_change_percent":pct(a["rig_shaft_torque_phase_mean"]["peak_to_peak_of_phase_averages"],b["rig_shaft_torque_phase_mean"]["peak_to_peak_of_phase_averages"]),
          "rig_phase_mean_drag_ptp_change_percent":pct(a["rig_support_drag_phase_mean"]["peak_to_peak_of_phase_averages"],b["rig_support_drag_phase_mean"]["peak_to_peak_of_phase_averages"]),
        })
    return {
      "id":"RM2-RAW-LOADS-001",
      "classification":"ORIGINAL_NI_RIG_FORCE_AND_TORQUE_DESCRIPTIVE_REDUCTION_NOT_BLADE_STRAIN_OR_FATIGUE",
      "source":"UNH RM2 original public figshare raw NI data; immutable upstream locator commit fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef",
      "source_manifest":"research/benchmarks/RM2_RAW_SIX_SOURCE_MANIFEST.json",
      "six_trials_acquired_and_sha_validated":len(trials),
      "measurements_available":"Calibrated in original metadata but not independently recalibrated: rig-support drag load cell, shaft torque, angle, carriage position, all original NI 2 kHz",
      "units":{"support_drag":"N","shaft_torque":"Nm","rotor_angle":"degree","tow_speed":"m/s","mechanical_power_proxy":"W"},
      "reduction_method":{
        "source_transform":"Upstream pyrm2tt/processing.py nominal load and tare corrections; centered difference for position/angle, respective 100/8-sample moving-average approximations",
        "drag":"drag_left + drag_right - first 2 s static offset - separate tare_drag at nominal tow speed",
        "torque":"torque_trans + 0.00104768276035 * RPM - 0.848866229797 (source's tare torque)",
        "rpm":"(dAngle/dt in degrees/s)/6 followed by 8-sample moving average",
        "trim":"Source processed table t1,t2 steady window, with published blade-pass t2 endpoints; 2000Hz samples",
        "phase_bins":"36 x 10 degree rotor-angle bins, point-estimate cycle-averaged rig force and torque across a short run; NOT stress cycles",
        "source_rho_kg_m3":1000,"source_area_m2":round(D*H,8),
        "reproduction_max_abs_error_rule":0.006
      },
      "trials":trials,"within_speed_pairs":pairs,
      "scientific_gates":{
        "measured_rig_force_and_shaft_torque":"SOURCE_REDUCED_DESCRIPTIVE",
        "blade_root_strain":"NOT_ACQUIRED",
        "strut_structural_stress":"NOT_ACQUIRED",
        "fatigue_damage":"NOT_EVALUABLE",
        "net_delivered_electrical_energy":"NOT_MEASURED",
        "controller_actuator_electricity":"NOT_MEASURED",
        "independent_replicate_significance":"NOT_ASSESSED",
        "qualified_2018_FORCE_inflow":"ZERO_APPROVED",
        "inwater_prototype_permission":"NOT_OBTAINED"
      },
      "decision":"Use raw rig shaft-torque and support-force time histories as descriptive controls for prospective synchronized cyclic-load and electric-PTO experiments; do NOT claim reduced damaging fatigue cycles or validated net electricity."
    }

def validate_committed():
    report=json.loads(REPORT.read_text("utf8"))
    m=load_manifest()
    if report["id"]!="RM2-RAW-LOADS-001" or report["six_trials_acquired_and_sha_validated"]!=6 or len(report["trials"])!=6 or len(report["within_speed_pairs"])!=3:
        raise ValueError("Invalid original NI observation report structure")
    if report["scientific_gates"]["fatigue_damage"]!="NOT_EVALUABLE" or report["scientific_gates"]["qualified_2018_FORCE_inflow"]!="ZERO_APPROVED":
        raise ValueError("Invalid research hold")
    for tr in report["trials"]:
        src=next((s for s in m["trials"] if s["trial_id"]==tr["trial_id"]),None)
        if not src or tr["raw_ni_sha256"]!=src["ni"]["sha256"] or tr["metadata_sha256"]!=src["metadata"]["sha256"] or tr["cp_reproduction_abs_error"]>0.006 or tr["cd_reproduction_abs_error"]>0.006:
            raise ValueError("Invalid source hash, source trial, or processed coefficient reproduction")
        if len(tr["rig_support_drag_phase_mean"]["means"])!=36 or len(tr["rig_shaft_torque_phase_mean"]["means"])!=36:
            raise ValueError("Missing phase bins")
    print("Raw RM2 report structural and source-consistency check passed; no physical fatigue validation.")
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--analyze-dir",type=Path)
    parser.add_argument("--out",type=Path)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if args.analyze_dir:
        result=make_report(args.analyze_dir)
        path=args.out or REPORT
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
        print(f"Reduced {len(result['trials'])} source-backed raw NI time-series, {len(result['within_speed_pairs'])} pairs.")
        for pair in result["within_speed_pairs"]:print(json.dumps(pair,sort_keys=True))
    if args.check or not args.analyze_dir:
        validate_committed()

if __name__=="__main__":
    main()
