"""Fail-closed consistency checks for staged physical experiments and tidal test sites.

This is metadata qualification, never ocean QC or structural validation.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check():
    p = load("research/experiment_protocol_v1.json")
    proto = load("research/prototype_gates.json")
    rm2 = load("reports/RM2-TRADEOFF-001.json")
    cmar = load("research/observations/CMAR_DIGBY_DG013_2022_QA.json")
    force = load("research/observations/FORCE_INFLOW_V0_MANIFEST_2018.json")
    catalogue = load("research/catalogue.json")

    assert p["schema_version"] == "TT-EXPERIMENT-V1"
    assert p["classification"] == "DESIGN_HYPOTHESIS_PROSPECTIVE_PROTOCOL_NO_MEASURED_RESULT"
    assert p["physical_experiments_run"] == 0, "No experiment exists; refuse success"
    assert p["prototype_winner"] is None, "No physical winner exists"
    assert p["field_deployment_authorized"] is False, "No field authorization exists"
    assert p["qualified_site_inflow_rows"] == force["model_eligible_rows"] == cmar["model_eligible_rows"] == 0
    assert force["science_approved_cells"] == 0
    assert force["records"] == 263250
    assert sum(force["counts"].values()) == force["records"]
    assert set(force["counts"]) == {
        "PENDING_NATIVE_QC_AND_GEOMETRY", "SUSPECT_EXACT_ZERO_ALL_COMPONENTS",
        "SUSPECT_LOW_PRESSURE_TRANSITION",
    }
    assert cmar["native_sensor_qc"] == "UNVERIFIED"
    assert p["scientific_status"] == "NOT_EXECUTED_BLOCKED_SITE_QC_AND_PHYSICAL_TEST_ACCESS"
    assert all(s not in ("PASS", "COMPLETE", "VALIDATED", "ACCEPTED") for s in p["independent_gates"].values())
    assert all(isinstance(x, str) and x for x in p["falsifiers"])
    assert len(p["mandatory_synced_channels"]) >= 12
    channel_ids = {x["id"] for x in p["mandatory_synced_channels"]}
    assert len(channel_ids) == len(p["mandatory_synced_channels"])
    assert {"inflow_3d", "shaft_torque", "blade_root_strain", "strut_strain",
            "delivered_electrical_power", "control_and_actuator_power", "rotor_position",
            "rig_status"} <= channel_ids

    assert set(x["id"] for x in p["architectures"]) == set(
        x["id"] for x in proto["candidates"])
    assert len(p["architectures"]) == 3
    assert all(len(x["required_specific"]) >= 3 and x["reference_area"] for x in p["architectures"])
    env = p["prospective_lab_envelope_assumptions"]
    assert env["source_class"] == "ENGINEERING_ASSUMPTION_NOT_MEASURED_FIELD_RESOURCE"
    assert env["mean_inflow_setpoints_m_s"] == [0.6, 1.0, 1.4]
    assert len(env["directions"]) == 2
    assert env["condition_count_without_replicates"] == 6
    assert env["minimum_total_mean_condition_cells_without_replicates"] == 12

    baseline = rm2["baseline"]
    comparator = p["comparator"]
    candidate = next(x for x in rm2["within_lab_mechanical_power_budgets"]
                     if x["minimum_fraction_of_peak_mechanical_cp"] == 0.95)
    assert baseline["run"] == comparator["baseline_source_run"] == 12
    assert candidate["selected_source_run"] == comparator["candidate_source_run"] == 10
    for a, b in (("cp", "published_processed_mean_cp"), ("cd", "published_processed_mean_cd")):
        assert abs(comparator[b]["baseline"] - baseline[a]) < 1e-7
        assert abs(comparator[b]["candidate"] - candidate["observed_" + a]) < 1e-7

    with (ROOT / "research/TIDAL_TEST_SITE_SCREEN_2026-10-20.csv").open(
            newline="", encoding="utf-8") as f:
        sites = list(csv.DictReader(f))
    assert len(sites) == 7
    assert len({row["site_id"] for row in sites}) == 7
    assert {row["site_id"] for row in sites} == {
        "TT-01", "TT-02", "TT-03", "TT-04", "TT-05", "TT-06", "TT-07"}
    assert all(row["field_readiness"] and row["key_blockers"] and row["reference_urls"]
               for row in sites)
    assert all("AUTHORIZED" not in row["field_readiness"] or
               "NOT AUTHORIZED" in row["field_readiness"] for row in sites)
    assert "NOT A QUALIFIED TIDAL STREAM FLOW SITE" in next(
        row["flow_speed_m_s"] for row in sites if row["site_id"] == "TT-06")

    ids = [x["id"] for x in catalogue]
    assert len(set(ids)) == len(ids), "Duplicate research source"
    assert {"NS-TESTCENTRE-2018", "NS-SWRESOURCE-2013", "NRC-DIGBY-2025",
            "NS-GRAND-2018-PERMIT", "COVE-STELLA-2026",
            "NS-TIDAL-DEMO-GUIDE-2026", "TURB-NABEREZHNYKH-2023"} <= set(ids)
    print("Readiness gate OK: 7 sites, 3 unranked prototypes, 0 tested devices, "
          "0 approved FORCE/CMAR inflow rows; RM2 means source-matched.")


if __name__ == "__main__":
    check()
