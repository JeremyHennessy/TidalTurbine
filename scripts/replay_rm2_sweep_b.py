"""Reprocess six original UNH RM2 sweep-B NI files; mechanical rig values only.
Requires numpy and h5py from requirements-ocean.txt.
Not an independent instrument calibration, fatigue study, or electrical-PTO model.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np
import h5py

RHO=1000.0
AREA=1.075*0.807
TARES={0.4:8.092422052240382,1.0:46.64324118685838,1.2:66.90768309869615}
# t1,t2, printed source processed mean Cp,Cd, original NI source SHA256
RUNS={
"Perf-0.4-b_10":(20,59.79,0.10116164673753654,0.7446961910382325,"d3cd3622934475154c1b46c7c41589f71f9fcf505709eb317093e3de7c5d5feb"),
"Perf-0.4-b_12":(20,59.94,0.14155233293959807,0.8106809021443262,"01aea381ca06884c78d36f7daa647e853c377732140747c558d44016133184f6"),
"Perf-1.0-b_10":(20,30.87,0.3458978492049717,0.7963497937309771,"0ff4a4fbf393fc87299b9c63ed14572096eebe75e8d9cc312100f68a1e43529a"),
"Perf-1.0-b_12":(20,30.89,0.35412142964142224,0.8419407758434596,"e34bce02bdeb882dcd07d039de4b90b61a3cb51983e4449b13e82439b5c22b5b"),
"Perf-1.2-b_10":(18,26.73,0.36437932551797975,0.8035351861306229,"e2f5db93f329b9b226f60cc349a704a5ee46aa9f1150eac986b8c0050e24a1dd"),
"Perf-1.2-b_12":(18,26.78,0.3648414058009858,0.8586191558380484,"4a84ea95a1c0013d0cf8c31f935f22f1dca951343f2b61d739cb53b41b7b3a8c")
}
def describe_run(z,name):
    t1,t2,cp_ref,cd_ref,expected=RUNS[name]
    raw=z.read(name+"_nidata.h5")
    assert len(raw)<25000000 and hashlib.sha256(raw).hexdigest()==expected, "Original NI source bytes changed"
    meta_raw=z.read(name+"_metadata.json")
    info=json.loads(meta_raw)
    speed=float(info["Tow speed (m/s)"]); tsr=float(info["Tip speed ratio"])
    with h5py.File(io.BytesIO(raw),"r") as f:
        arrays={key:f["data/"+key][:] for key in
                ("time","carriage_pos","drag_left","drag_right","turbine_angle","torque_trans")}
    t=arrays["time"]
    dt=float(np.median(np.diff(t)))
    assert abs(dt-.0005)<1e-6
    rpm=np.convolve(np.gradient(arrays["turbine_angle"],dt)/6,np.ones(8)/8,mode="same")
    omega=rpm*np.pi/30
    u=np.convolve(np.gradient(arrays["carriage_pos"],dt),np.ones(100)/100,mode="same")
    torque=arrays["torque_trans"]+0.00104768276035*rpm-0.848866229797
    drag=arrays["drag_left"]+arrays["drag_right"]
    drag-=np.mean(drag[:4000])
    drag-=TARES[speed]
    keep=(t>=t1)&(t<t2)
    assert int(keep.sum())>10000 and float(np.min(u[keep]))>.2
    cp=float(np.mean(torque[keep]*omega[keep]/(.5*RHO*AREA*u[keep]**3)))
    cd=float(np.mean(drag[keep]/(.5*RHO*AREA*u[keep]**2)))
    assert abs(cp-cp_ref)<.006 and abs(cd-cd_ref)<.006, "Source processed coefficient check failed"
    def rounded(x):return round(float(x),6)
    return {"trial_id":name,"speed_m_s":speed,"tsr_nominal":tsr,
            "sample_rate_hz":2000,"steady_samples":int(keep.sum()),
            "original_ni_sha256":expected,
            "original_metadata_sha256":hashlib.sha256(meta_raw).hexdigest(),
            "upstream_processed_cp":cp_ref,"upstream_processed_cd":cd_ref,
            "recomputed_cp":rounded(cp),"recomputed_cd":rounded(cd),
            "cp_abs_error":rounded(abs(cp-cp_ref)),
            "cd_abs_error":rounded(abs(cd-cd_ref)),
            "shaft_torque_nm":{"mean":rounded(np.mean(torque[keep])),
                               "std":rounded(np.std(torque[keep]))},
            "support_drag_n":{"mean":rounded(np.mean(drag[keep])),
                              "std":rounded(np.std(drag[keep]))}}
def reduce(archive, published_A=None):
    with zipfile.ZipFile(archive) as z:
        trials=[describe_run(z,n) for n in RUNS]
    pairs=[]
    for speed in TARES:
        candidate=next(x for x in trials if x["speed_m_s"]==speed and x["tsr_nominal"]==2.9)
        reference=next(x for x in trials if x["speed_m_s"]==speed and x["tsr_nominal"]==3.1)
        def change(key,nested=None):
            a=candidate[nested][key] if nested else candidate[key]
            b=reference[nested][key] if nested else reference[key]
            return round(100*(a/b-1),4)
        pairs.append({"speed_m_s":speed,
          "cp_change_percent":change("recomputed_cp"),
          "cd_change_percent":change("recomputed_cd"),
          "shaft_torque_sd_change_percent":change("std","shaft_torque_nm"),
          "support_drag_sd_change_percent":change("std","support_drag_n")})
    report={"id":"RM2-RAW-B-001","classification":"MEASURED_RIG_TORQUE_AND_DRAG_DESCRIPTIVE_SOURCE_REPRODUCTION_NOT_BLADE_FATIGUE",
      "source":"UNH RM2 original Figshare raw article 1302029; 2015 NI 2000 Hz second sweeps",
      "n_trials":len(trials),"trials":trials,"within_speed_pairs":pairs,
      "model_eligible_force_inflow":0,
      "independent_blade_strain_measurements":0,
      "net_delivered_electricity_measurements":0,
      "repeatability_inference":"A/B historical sweeps are not independently powered matched structural-fatigue experiments",
      "scientific_limits":["Original source NI calibration metadata not independently verified",
          "Approximate upstream filtering and steady-window recipe with explicit +/-0.006 coefficient reproduction gate",
          "No calibration of blade-root strain or material fatigue cycles",
          "No controller or delivered electrical power"] }
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--archive",required=True)
    p.add_argument("--out",default="reports/RM2-RAW-B-001.json")
    a=p.parse_args();result=reduce(a.archive)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("RM2 original sweep B replay:",len(result["trials"]),"raw trials checked")
if __name__=="__main__":main()
