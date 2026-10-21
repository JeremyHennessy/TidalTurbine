"""Fail closed on source provenance and any premature RM2 fatigue/site-current claim."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def check():
    b=json.loads((ROOT/"reports/RM2-RAW-B-001.json").read_text(encoding="utf8"))
    ns=json.loads((ROOT/"reports/NS-PASSAGES-7D-SUMMARY-001.json").read_text(encoding="utf8"))
    assert b["classification"].endswith("NOT_BLADE_FATIGUE")
    assert b["n_trials"]==len(b["trials"])==6
    assert len({r["trial_id"] for r in b["trials"]})==6
    assert {r["speed_m_s"] for r in b["trials"]}=={0.4,1.0,1.2}
    assert all(len(r["original_ni_sha256"])==64 for r in b["trials"])
    assert all(r["cp_abs_error"]<0.006 and r["cd_abs_error"]<0.006 for r in b["trials"])
    assert b["independent_blade_strain_measurements"]==0
    assert b["net_delivered_electricity_measurements"]==0
    assert b["model_eligible_force_inflow"]==0
    assert len(b["within_speed_pairs"])==3
    assert all(p["cd_change_percent"]<0 for p in b["within_speed_pairs"])
    assert b["within_speed_pairs"][1]["shaft_torque_sd_change_percent"]>0
    assert b["within_speed_pairs"][2]["shaft_torque_sd_change_percent"]>0
    assert ns["source_rows_total"]==21872 and ns["model_eligible_rows"]==0
    assert len(ns["sites"])==2
    assert {s["deployment_id"] for s in ns["sites"]}=={"DG012","DG002"}
    assert {s["deployment_year"] for s in ns["sites"]}=={2020,2010}
    for s in ns["sites"]:
        assert s["model_eligible_rows"]==0 and s["native_beam_quality_recovered"] is False
        assert s["source_datetime_offset_unverified"] is True
        assert len(s["original_source_sha256"])==64
        assert sum(s["source_flag_speed_counts"].values())==s["source_rows"]
    baseline=json.loads((ROOT/"reports/RM2-RAW-LOADS-001.json").read_text(encoding="utf8"))
    a=next(p for p in baseline["within_speed_pairs"] if p["nominal_speed_m_s"]==1)
    other=next(p for p in b["within_speed_pairs"] if p["speed_m_s"]==1)
    assert a["shaft_torque_std_change_percent"]>0 and other["shaft_torque_sd_change_percent"]>0
    assert baseline["scientific_gates"]["fatigue_damage"]=="NOT_EVALUABLE"
    return True

if __name__=="__main__":
    check()
    print("PASS: 6 measured sweep-B rig trials; 21872 site-profile rows; 0 model-qualified ocean records; fatigue remains unmeasured")
