"""Reproducible full-campaign numerical QA of FORCE spring-2018 processed NetCDF.

Not publisher/native AD2CP QC, not a model-ready measured inflow, and not a
fatigue/power/annual-resource calculation. h5py and numpy are *only* required
for this separate scientific-data pipeline, not for the baseline simulator.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from statistics import median
import argparse
import csv
import io
import json
import math
import zipfile

import h5py
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "currents.nc": {
        "sha256": "be8acb1802786a0db7f5c2952e4554fc25f03508550b7478a19a2f47d86864e2",
        "bytes": 3348741,
        "url": "https://cioosatlantic.ca/erddap/files/FORCE_Mar2018_ADCP_Currents/Burst.VTC.DSEL.AVER.classic.nc",
    },
    "waves.nc": {
        "sha256": "d538b46f4b702382386721a43d39ec253f281f48522a377bf456b5d3373001ee",
        "bytes": 119465,
        "url": "https://cioosatlantic.ca/erddap/files/FORCE_Mar2018_ADCP_Waves/Burst.VTC.WAVES.classic.nc",
    },
}
# Exploratory arithmetic cutoffs ONLY; do not describe them as sensor-maker QC.
LOW_PRESSURE_SCREEN_DBAR = 20.0
PRESSURE_COMPARISON_TOLERANCE_DBAR = 0.1
TIME_MATCH_TOLERANCE_SECONDS = 0.5
FILL_WAVE_PERIOD_S = -9.0
STATUS = "NUMERICAL_QA_ONLY_ZERO_SOURCE_APPROVED_ROTOR_INFLOW_BINS"


def verify_archive(archive: Path, *, expected=True):
    """Return file bytes and manifest; reject malicious names, missing or changed source."""
    source = Path(archive)
    with zipfile.ZipFile(source) as z:
        found = set(z.namelist())
        required = set(SOURCES) | {"manifest.json"}
        if found != required:
            raise ValueError(f"Unexpected archive members: {sorted(found ^ required)}")
        if any(i.file_size > 5_000_000 for i in z.infolist()):
            raise ValueError("Oversized archive entry")
        raw = {n: z.read(n) for n in SOURCES}
        manifest = json.loads(z.read("manifest.json"))
    for name, b in raw.items():
        info = SOURCES[name]
        actual = sha256(b).hexdigest()
        if expected and (len(b) != info["bytes"] or actual != info["sha256"]):
            raise ValueError(f"SOURCE FILE HASH/SIZE CHANGED: {name}")
        if not b.startswith(b"\x89HDF\r\n\x1a\n"):
            raise ValueError(f"Not a NetCDF4/HDF5 file: {name}")
        m = next((m for m in manifest.get("files", []) if m.get("file") == name), None)
        if m is None or m.get("sha256") != actual or m.get("size_bytes") != len(b):
            raise ValueError(f"Manifest conflicts with archived {name}")
    return raw, manifest


def _read_arrays(path: Path, kind: str):
    with h5py.File(path, "r") as ds:
        wanted = (["time", "cell_range", "cell_size", "sea_water_pressure", "eastward_sea_water_velocity",
                   "northward_sea_water_velocity", "upward_sea_water_velocity"] if kind == "currents"
                  else ["time", "sea_water_pressure", "sea_surface_wave_significant_height",
                        "sea_surface_wave_maximum_period"])
        missing = set(wanted) - set(ds.keys())
        if missing:
            raise ValueError(f"Missing NetCDF variables in {kind}: {sorted(missing)}")
        out = {k: ds[k][:] for k in wanted}
        units = {k: ds[k].attrs.get("units", b"").decode("utf-8") for k in wanted}
        expected = {"time": "seconds since 1970-01-01T00:00:00 UTC", "sea_water_pressure": "dbar"}
        if kind == "currents":
            expected.update({"cell_range": "m", "cell_size": "m",
                "eastward_sea_water_velocity": "m/s", "northward_sea_water_velocity": "m/s",
                "upward_sea_water_velocity": "m/s"})
        else:
            expected.update({"sea_surface_wave_significant_height": "m", "sea_surface_wave_maximum_period": "s"})
        for k, val in expected.items():
            if units[k] != val:
                raise ValueError(f"Units for {k}: expected {val}, got {units[k]}")
        out["_attrs"] = {k: (v.decode("utf-8") if isinstance(v, bytes) else str(v))
                         for k, v in ds.attrs.items() if k in ("instrument", "geospatial_lat_max", "geospatial_lon_max", "history")}
    return out


def assess_arrays(c, waves):
    """Arithmetic checks; return one JSON-friendly report, no engineering qualification."""
    t = np.asarray(c["time"], dtype=float)
    tw = np.asarray(waves["time"], dtype=float)
    ranges = np.asarray(c["cell_range"], dtype=float)
    u, v, w = (np.asarray(c[k], dtype=float) for k in
               ("eastward_sea_water_velocity", "northward_sea_water_velocity", "upward_sea_water_velocity"))
    p = np.asarray(c["sea_water_pressure"], dtype=float)
    pw = np.asarray(waves["sea_water_pressure"], dtype=float)
    cs = np.asarray(c["cell_size"], dtype=float)
    hs = np.asarray(waves["sea_surface_wave_significant_height"], dtype=float)
    period = np.asarray(waves["sea_surface_wave_maximum_period"], dtype=float)
    if t.ndim != 1 or t.size < 3 or not np.isfinite(t).all() or not (np.diff(t) > 0).all():
        raise ValueError("Time vector is invalid or not strictly increasing")
    if tw.shape != t.shape or np.max(abs(tw - t)) > TIME_MATCH_TOLERANCE_SECONDS:
        raise ValueError("Waves and currents timestamps cannot be safely paired")
    if ranges.ndim != 1 or not (np.diff(ranges) > 0).all() or not np.isfinite(ranges).all():
        raise ValueError("Invalid instrument-relative ranges")
    if any(a.shape != (len(ranges), len(t)) for a in (u, v, w)):
        raise ValueError("Velocity component shapes must be (range_cell,time)")
    if any(a.shape != t.shape for a in (p, pw, cs, hs, period)):
        raise ValueError("Ancillary measurement shape mismatch")
    if not all(np.isfinite(a).all() for a in (u, v, w, p, pw, cs, hs)):
        raise ValueError("Non-finite measurements require separate missing-data handling")
    if not np.logical_or(np.isclose(period, FILL_WAVE_PERIOD_S), np.isfinite(period)).all():
        raise ValueError("Invalid wave period encoding")
    if np.any(p < 0) or np.any(cs < 0):
        raise ValueError("Pressure/cell size contains invalid negative values")
    if np.max(np.abs(np.stack((u, v, w)))) > 15:
        raise ValueError("Velocity has values outside deliberately wide numeric bound")

    z = (u == 0) & (v == 0) & (w == 0)
    low = p < LOW_PRESSURE_SCREEN_DBAR
    allzero = np.all(z, axis=0)
    zero_per_cell = np.sum(z, axis=1)
    comparison_window = ~low  # SCREEN ONLY: excludes suspicious pressure-collapse interval, not publisher-QC.
    preterminal_zeros = np.sum(z[:, comparison_window], axis=1)
    preterminal_count = int(np.sum(comparison_window))
    nonzero_counts = len(t) - zero_per_cell
    flags = ["ALL_ZERO_UNQUALIFIED" if v == len(t) else ("INTERMITTENT_ZERO_UNQUALIFIED" if v else "NONZERO_NUMERIC_ONLY_UNQUALIFIED")
             for v in zero_per_cell]
    by_cell = [
        {"range_m_instrument_relative": float(r), "samples": int(t.size), "exact_zero_triples": int(q),
         "fraction_zero": round(float(q / len(t)), 6), "nonzero_numeric_only": int(nonzero_counts[i]),
         "quality_status": flags[i],
         "comparison_window_nonlowpressure_bursts":preterminal_count,
         "comparison_window_zero_triples":int(preterminal_zeros[i]),
         "comparison_window_numeric_nonzero_bursts":int(preterminal_count-preterminal_zeros[i]),
         "comparison_window_only_status":("ALWAYS_ZERO_UNQUALIFIED" if preterminal_zeros[i]==preterminal_count else
            "INTERMITTENT_ZERO_UNQUALIFIED" if preterminal_zeros[i] else "NO_ZERO_NUMERIC_ONLY_UNQUALIFIED")}
        for i, (r, q) in enumerate(zip(ranges, zero_per_cell))
    ]
    zero_full = np.where(allzero)[0]
    high_nonzero = np.array([float(np.max(ranges[~z[:, i]])) if np.any(~z[:, i]) else np.nan for i in range(len(t))])
    crosspress = abs(p - pw)
    gaps = Counter(int(round(v)) for v in np.diff(t))
    # Hs=0 remains numeric, not automatically interpreted as truly zero wave height.
    period_valid = np.isfinite(period) & (~np.isclose(period, FILL_WAVE_PERIOD_S)) & (period > 0)
    hs_valid = np.isfinite(hs) & (hs >= 0)
    dayids = [datetime.fromtimestamp(float(x), timezone.utc).strftime("%Y-%m-%d") for x in t]
    day_index = defaultdict(list)
    for i, day in enumerate(dayids):
        day_index[day].append(i)
    days = []
    for day in sorted(day_index):
        ix = day_index[day]
        zi = z[:, ix]
        hi = hs[ix]
        pi = p[ix]
        finite_hs = hi[np.isfinite(hi) & (hi >= 0) & (~low[ix])]  # unqualified numeric, pressure-collapse excluded
        days.append({"date_utc": day, "bursts": len(ix), "triplets_total": int(zi.size),
            "triplets_exact_zero": int(zi.sum()), "fraction_exact_zero": round(float(zi.mean()), 6),
            "all_cell_zero_bursts": int(np.sum(allzero[ix])),
            "low_pressure_suspect_bursts": int(np.sum(low[ix])),
            "pressure_dbar_min": round(float(np.min(pi)), 5), "pressure_dbar_max": round(float(np.max(pi)), 5),
            "wave_hs_m_median_numeric_not_qc": round(float(np.median(finite_hs)), 5) if len(finite_hs) else None,
            "wave_period_fill_minus9_count": int(np.sum(~period_valid[ix])),
            "wave_hs_bursts_excluded_lowpressure":int(np.sum(low[ix]))})

    cand = np.isfinite(high_nonzero) & (~low)
    corr = float(np.corrcoef(p[cand], high_nonzero[cand])[0, 1]) if np.sum(cand) > 2 and np.std(high_nonzero[cand]) > 0 else None
    fmt = lambda x: datetime.fromtimestamp(float(x), timezone.utc).isoformat().replace("+00:00", "Z")
    return {
      "id":"FORCE-CAMPAIGN-QA-001",
      "status":STATUS,
      "source_type":"full published PROCESSED NetCDF source files, not original raw native .ad2cp",
      "research_instrument":"Nortek Signature 500 serial 100258; FAST3 upward-facing; transducer 0.7m above bed per reviewed article",
      "source_sha256":{n:SOURCES[n]["sha256"] for n in SOURCES},
      "source_license":"CC BY 4.0, FORCE / CIOOS Atlantic",
      "source_processing_lineage": c.get("_attrs", {}).get("history", "unknown"),
      "location":{"lat_deg_n":c.get("_attrs", {}).get("geospatial_lat_max"),
                  "lon_deg_e":c.get("_attrs", {}).get("geospatial_lon_max"),
                  "instrument_range_coordinate":"transducer-relative; first-cell centre inconsistent across metadata and paper"},
      "observed_utc_start":fmt(t[0]), "observed_utc_end":fmt(t[-1]),
      "time_bursts":int(t.size), "cell_count":int(ranges.size), "velocity_numeric_triplets":int(z.size),
      "cadence_differences_seconds":{str(k):v for k,v in sorted(gaps.items())},
      "max_current_wave_time_disagreement_s":round(float(np.max(abs(t-tw))),6),
      "pressure_comparison_dbar_abs_median":round(float(np.median(crosspress)),6),
      "pressure_comparison_dbar_abs_max":round(float(np.max(crosspress)),6),
      "pressure_comparison_above_0p1_dbar":int(np.sum(crosspress > PRESSURE_COMPARISON_TOLERANCE_DBAR)),
      "pressure_dbar_min":round(float(np.min(p)),6), "pressure_dbar_max":round(float(np.max(p)),6),
      "cell_size_m_reported_unique":sorted(map(float,np.unique(cs))),
      "cell_size_zero_bursts":int(np.sum(cs==0)),
      "total_all_component_exact_zero":int(np.sum(z)),
      "fraction_exact_zero":round(float(np.mean(z)),6),
      "all_zero_velocity_bursts":int(np.sum(allzero)),
      "all_zero_bursts_start_utc":fmt(t[zero_full[0]]) if len(zero_full) else None,
      "all_zero_bursts_end_utc":fmt(t[zero_full[-1]]) if len(zero_full) else None,
      "pressure_below_arithmetic_20dbar":int(np.sum(low)),
      "pressure_below_20dbar_and_allzero":int(np.sum(low & allzero)),
      "preterminal_pressure_screen_bursts":preterminal_count,
      "preterminal_pressure_screen_exactzero_triplets":int(np.sum(z[:,comparison_window])),
      "preterminal_pressure_screen_fraction_exactzero":round(float(np.mean(z[:,comparison_window])),6),
      "preterminal_pressure_screen_ranges_no_zero_m":[float(ranges[i]) for i in range(len(ranges)) if preterminal_zeros[i]==0],
      "preterminal_pressure_screen_ranges_always_zero_m":[float(ranges[i]) for i in range(len(ranges)) if preterminal_zeros[i]==preterminal_count],
      "preterminal_pressure_screen_ranges_partially_zero_m":[float(ranges[i]) for i in range(len(ranges)) if 0<preterminal_zeros[i]<preterminal_count],
      "preterminal_screen_is_sufficient_for_turbine_modelling":False,
      "pressure_vs_highest_nonzero_cell_r_excluding_lowpressure":round(corr,6) if corr is not None else None,
      "ranges_all_zero_m":[float(ranges[i]) for i in range(len(ranges)) if zero_per_cell[i]==len(t)],
      "ranges_intermittently_zero_m":[float(ranges[i]) for i in range(len(ranges)) if 0<zero_per_cell[i]<len(t)],
      "ranges_never_zero_m":[float(ranges[i]) for i in range(len(ranges)) if zero_per_cell[i]==0],
      "wave_significant_height_numeric_count":int(np.sum(hs_valid)),
      "wave_significant_height_zero_count":int(np.sum(hs==0)),
      "wave_significant_height_m_numeric_min_max":[round(float(np.min(hs[hs_valid])),6),round(float(np.max(hs[hs_valid])),6)] if np.any(hs_valid) else [],
      "wave_maximum_period_fill_minus9_count":int(np.sum(~period_valid)),
      "wave_hs_numeric_comparison_excluding_pressure_collapse":[round(float(np.min(hs[hs_valid & (~low)])),6),
           round(float(np.max(hs[hs_valid & (~low)])),6)] if np.any(hs_valid & (~low)) else [],
      "wave_maximum_period_numeric_count":int(np.sum(period_valid)),
      "vertical_cell_summary":by_cell,
      "daily_arithmetic_summary":days,
      "quality_critical_findings":[
          "Exactly zero velocity triples in a depth/pressure-structured pattern may encode missing/masked data; do NOT treat as slack flow.",
          "At source end pressure abruptly drops and 88 bursts show all-zero profiles: instrument recovery/out-of-water HYPOTHESIS not verified deployment record.",
          "Source HDF5 current components have no per-cell native correlation/amplitude/percent-good/tilt flags; source-specific QC and first-cell centre remain unresolved.",
          "An exploratory >=20 dbar comparison window separates the end-of-deployment pressure collapse. This threshold is NOT a manufacturer QC rule and does not certify the 26 lower cells as true measured inflow.",
          "Companion wave pressure does not exactly match current product; quantify differences and reconcile source processing before combining engineering quantities.",
          "Numerical checks and 55-day/56-calendar-day series do NOT certify usable depth cells, annual resource, load extremes or deployment feasibility."
      ],
      "model_ingestion":"BLOCKED_ZERO_SCIENTIFICALLY_QUALIFIED_BINS",
      "source_approved_velocity_records":0,
      "provenance_notes":"Original full source archived in 7-day GitHub Actions artifact; SHA-pinned; no third-party binary data committed to Git."
    }


def process_files(current_file, wave_file):
    return assess_arrays(_read_arrays(Path(current_file),"currents"), _read_arrays(Path(wave_file),"waves"))


def verify_prior_72h(prior_archive: Path, currents_path: Path):
    """Compare every prior 72-hour ERDDAP triple against original full NetCDF."""
    with zipfile.ZipFile(prior_archive) as z:
        raw=z.read("source.csv")
    sha=sha256(raw).hexdigest()
    if sha!="d05f2a1258d9908b04fc7017cdb818ca318ac47c38e6b40244eac8c378ec4c7a":
        raise ValueError("Old 72-hour observation checksum changed")
    with h5py.File(currents_path,"r") as h:
        t=h["time"][:]; zz=h["cell_range"][:]
        times={datetime.fromtimestamp(float(v),timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'):i for i,v in enumerate(t)}
        cells={float(r):i for i,r in enumerate(zz)}
        data={k:h[k][:] for k in ("eastward_sea_water_velocity","northward_sea_water_velocity","upward_sea_water_velocity")}
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    compared=0;biggest=0
    for row in rows:
        if row["time"]=="UTC":continue
        i=times[row["time"]];j=cells[float(row["cell_range"])]
        for field,mat in data.items():
            delta=abs(float(row[field])-float(mat[j,i]));biggest=max(biggest,delta)
            if delta>1e-5:raise ValueError(f"Full NetCDF disagrees with earlier ERDDAP slice: {field}")
        compared+=1
    if compared!=14400:raise ValueError(f"Expected 14400 prior observations, got {compared}")
    return {"older_source_sha256":sha,"compared_triplets":compared,"max_component_absolute_difference_m_s":round(biggest,10)}


def write_results(report, json_path: Path, daily_path: Path):
    json_path.parent.mkdir(parents=True,exist_ok=True)
    daily_path.parent.mkdir(parents=True,exist_ok=True)
    json_path.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    daily=report["daily_arithmetic_summary"]
    with daily_path.open("w",newline="",encoding="utf-8") as f:
        dw=csv.DictWriter(f,fieldnames=list(daily[0].keys()))
        dw.writeheader();dw.writerows(daily)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive",type=Path,required=True)
    parser.add_argument("--out",type=Path,default=ROOT/"reports/FORCE-CAMPAIGN-QA-001.json")
    parser.add_argument("--daily-out",type=Path,default=ROOT/"research/observations/FORCE_CAMPAIGN_DAILY_QA_2018.csv")
    parser.add_argument("--prior-72h-archive",type=Path)
    args=parser.parse_args()
    raw,manifest=verify_archive(args.archive)
    # In-memory HDF5 via BytesIO avoids emitting another untracked copy of source into repo.
    with h5py.File(io.BytesIO(raw["currents.nc"]),"r") as cf, h5py.File(io.BytesIO(raw["waves.nc"]),"r") as wf:
        def grab(h,which):
            cols=("time", "cell_range", "cell_size", "sea_water_pressure", "eastward_sea_water_velocity","northward_sea_water_velocity","upward_sea_water_velocity") if which=="c" else ("time","sea_water_pressure","sea_surface_wave_significant_height","sea_surface_wave_maximum_period")
            return {**{k:h[k][:] for k in cols},"_attrs":{k:(v.decode() if isinstance(v,bytes) else str(v)) for k,v in h.attrs.items() if k in ("geospatial_lat_max","geospatial_lon_max","history")}}
        report=assess_arrays(grab(cf,"c"),grab(wf,"w"))
        if args.prior_72h_archive:
            # The prior checker operates with a file path; do not persist source under Git.
            import tempfile
            with tempfile.TemporaryDirectory() as d:
                fn=Path(d)/"currents.nc";fn.write_bytes(raw["currents.nc"])
                report["prior_72h_crosscheck"]=verify_prior_72h(args.prior_72h_archive,fn)
    write_results(report,args.out,args.daily_out)
    print(f"FORCE full campaign: {report['time_bursts']} times × {report['cell_count']} ranges, "
          f"{report['total_all_component_exact_zero']} zero vectors, "
          f"{len(report['daily_arithmetic_summary'])} UTC calendar days; model intake BLOCKED")


if __name__=="__main__":main()
