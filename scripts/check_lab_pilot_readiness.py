"""Fail-closed, read-only laboratory pilot readiness and published list-rate check.

This tool certifies *metadata consistency only*, not physical performance, safety,
cost, facility access or permission. It performs no networking and writes no files.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = "research/lab_pilot_readiness_20261023.json"
SOURCE_PATHS = {
    "protocol": "research/experiment_protocol_v1.json",
    "bom": "research/prototype_test_rig_bom_v1.json",
    "shaft": "research/shaft_support_006.json",
    "force": "research/observations/FORCE_INFLOW_V0_MANIFEST_2018.json",
    "prototype": "research/prototype_gates.json",
}
REQUIRED_GATE_IDS = {
    "SOURCE-NATIVE-QC", "LAB-FACILITY", "LAB-CONTAINMENT",
    "LAB-CALIBRATION", "LAB-REPLICATION", "LAB-STRUCTURAL-LOADS",
    "LAB-NET-ELECTRICITY", "LAB-COMPARE", "ENGINEERING-GEOMETRY",
    "ENGINEERING-SHAFT", "ENGINEERING-MANUFACTURING",
    "ENGINEERING-BUDGET", "FIELD-FLOW", "FIELD-PERMISSIONS",
    "FIELD-RECOVERY",
}
CANONICAL_ID_SET = {
    "AXIAL-RM1-REFERENCE", "CROSSFLOW-RM2-REFERENCE",
    "FOIL-OSCILLATING-EXPERIMENTAL",
}


class ReadinessError(ValueError):
    """Research metadata contradicts its evidence or promotes an unearned gate."""


def load(relative_path, root=ROOT):
    return json.loads((root / relative_path).read_text(encoding="utf-8"))


def source_records(root=ROOT):
    return {name: load(path, root) for name, path in SOURCE_PATHS.items()}


def require(condition, message):
    if not condition:
        raise ReadinessError(message)


def validate(plan, records, root=ROOT):
    """Return a BLOCKED research summary; never label a component or field test ready."""
    require(plan.get("schema") == "TT-LAB-PILOT-READINESS-1", "Unknown schema")
    require(plan.get("classification") == "RESEARCH_AND_DESK_READINESS_ONLY",
            "A desk plan cannot claim certification")
    require(plan.get("physics_status") == {
        "qualified_site_inflow_rows": 0,
        "physical_lab_trials_documented": 0,
        "physical_field_deployments_documented": 0,
        "prototype_winner": None,
        "independent_predictive_validation": False,
        "measured_blade_fatigue_benefit": False,
        "measured_net_electricity_benefit": False,
    }, "Desk evidence cannot be promoted to physical proof")
    permission = plan.get("permissions", {})
    require(set(permission) == {
        "external_contact_authorized", "purchasing_authorized",
        "physical_lab_operation_authorized", "field_deployment_authorized",
        "environmental_approval_obtained",
    } and all(value is False for value in permission.values()),
            "No external action, spending, physical testing or permit approved")

    protocol, bom = records["protocol"], records["bom"]
    force, shaft, proto = records["force"], records["shaft"], records["prototype"]
    require(protocol["physical_experiments_run"] == 0 and
            protocol["prototype_winner"] is None and
            protocol["field_deployment_authorized"] is False,
            "Existing protocol shows no completed physical device trial or authorization")
    require(protocol["qualified_site_inflow_rows"] == 0 and
            force["model_eligible_rows"] == 0 and force["science_approved_cells"] == 0,
            "Unqualified FORCE ranges cannot be called site inflow")
    require(bom["approval_to_purchase"] is False and
            bom["physical_device_built"] is False and
            bom["quotes_acquired"] == 0,
            "Existing BOM has no purchased or fabricated test article")
    require(bom["costing"]["capital_budget_verified"] is False,
            "Existing BOM does not support an approved all-in budget")
    require(len(shaft["unknowns"]) >= 17 and
            all(value is None for value in shaft["unknowns"].values()) and
            all(not x["component_selected"] for x in shaft["architectures"]),
            "Shaft support is not selected or load-qualified")
    reference_ids = set(plan["reference_prototype_ids"])
    require(len(plan["reference_prototype_ids"]) == 3 and
            reference_ids == CANONICAL_ID_SET ==
            {x["id"] for x in protocol["architectures"]} ==
            {x["id"] for x in proto["candidates"]},
            "All three architecture IDs must match original unranked sources")
    comparator = plan.get("pilot_comparator", {})
    require(comparator.get("primary_design") == "CROSSFLOW-RM2-REFERENCE" and
            comparator.get("experimental_result_status") == "NO_NEW_PHYSICAL_TESTS" and
            comparator.get("registered_sample_size") is None and
            comparator.get("prespecified_acceptable_energy_penalty") is None and
            comparator.get("prespecified_load_benefit_threshold") is None,
            "Do not invent replicated measurements or statistical thresholds")
    env = protocol["prospective_lab_envelope_assumptions"]
    require(comparator["prospective_test_setpoints_m_s"] ==
            env["mean_inflow_setpoints_m_s"] and
            len(comparator["flow_direction_cases"]) == 2,
            "Lab speeds must remain assumption-labelled, not become site currents")
    existing_channels = {x["id"] for x in protocol["mandatory_synced_channels"]}
    require(set(comparator["mandatory_measurement_ids"]) <= existing_channels and
            {"blade_root_strain", "shaft_torque", "delivered_electrical_power",
             "control_and_actuator_power", "rotor_position", "inflow_3d"} <=
            set(comparator["mandatory_measurement_ids"]),
            "Cannot drop time-resolved structural or metered electrical channels")

    gates = plan.get("gates")
    require(isinstance(gates, list) and
            {g["id"] for g in gates} == REQUIRED_GATE_IDS and
            len(gates) == len(REQUIRED_GATE_IDS), "Missing or duplicated physical gates")
    for gate in gates:
        require(gate["phase"] in {"source", "lab", "engineering", "field"} and
                gate["status"] == "UNRESOLVED" and gate["evidence"] is None and
                all(isinstance(gate[x], str) and gate[x].strip()
                    for x in ("requirement", "reference", "required_evidence")),
                "A physical/qualification gate was silently promoted or made empty")
        require((root / gate["reference"]).is_file(), "Gate reference missing: " + gate["reference"])
    for path in plan.get("documentation", []):
        require((root / path).is_file(), "Missing evidence document: " + path)
    require(len(plan["documentation"]) >= 5, "Insufficient traceable scientific references")
    boundaries = plan.get("separation_of_workstreams", {})
    require(set(boundaries) == {"laboratory_test", "site_specific_energy_forecast",
                                "in_water_test"} and
            all(isinstance(x, str) and len(x) >= 40 for x in boundaries.values()),
            "Lab runs, site forecasting and deployment have separate gates")

    venues = plan.get("venues", [])
    require(isinstance(venues, list) and len(venues) >= 4 and
            len({x["id"] for x in venues}) == len(venues),
            "Duplicate or missing venue candidates")
    for venue in venues:
        require(all(venue[k] is False for k in (
                "operator_acceptance_confirmed", "available_dates_confirmed",
                "facility_instrumentation_confirmed_for_project")),
                "Current facility/rotating test suitability was not verified")
        require(all(url.startswith("https://") for url in venue["sources"]) and
                venue["location"] and venue["limitation"] and venue["candidate_role"],
                "Facility claim missing provenance or limitation")
        require(venue.get("published_daily_rate_cad") is None or
                venue["id"] == "MI-CSAR", "Do not transfer one venue's published price")
    priced = [v for v in venues if v["id"] == "MI-CSAR"]
    require(len(priced) == 1 and priced[0]["published_daily_rate_cad"] == 5000 and
            priced[0]["rate_effective_date"] == "2026-04-01",
            "Published 2026 facility rate/reference must remain exact")
    budget = plan.get("budget", {})
    require(budget.get("status") == "LIST_RATE_ONLY_NO_ALL_IN_QUOTE" and
            budget.get("currency") == "CAD" and
            budget.get("published_venue_id") == "MI-CSAR" and
            budget.get("published_daily_rate_cad") == 5000 and
            budget.get("published_rate_effective_date") == "2026-04-01" and
            budget.get("source_url") in priced[0]["sources"] and
            budget.get("supplier_quotes_received") == 0 and
            budget.get("all_in_project_cost_cad") is None and
            budget.get("approved_spending_cad") is None and
            budget.get("venue_booking_confirmed") is False,
            "Do not turn a posted daily rate into a quote/approved all-in cost")
    days = budget.get("illustrative_day_counts")
    require(days == [1, 2, 3] and len(budget.get("unpriced_categories", [])) >= 5,
            "Reference-day examples must not masquerade as a complete budget")
    guide = plan.get("regulatory_watch", {})
    require(guide.get("source_url") == "https://novascotia.ca/programs/tidal-demonstration-permit/" and
            guide.get("current_guide_version_released") == "2026-10-21" and
            guide.get("posted_application_close_date") == "2026-10-30" and
            all(guide.get(k) is False for k in (
                "project_eligibility_verified", "application_submitted", "permit_obtained")),
            "Do not infer eligibility/permit from the current public application deadline")
    require(len(plan.get("next_three_actions", [])) == 3,
            "Preserve three specific next activities")
    return {
        "status": "DESK_PLAN_PRESENT_PHYSICAL_AND_FACILITY_GATES_UNRESOLVED",
        "unresolved_gate_count": len(gates),
        "source_qualified_site_inflow_rows": force["model_eligible_rows"],
        "recorded_lab_tests": protocol["physical_experiments_run"],
        "supplier_quotes": bom["quotes_acquired"],
        "published_flume_list_rate_only_cad": {
            str(n): budget["published_daily_rate_cad"] * n for n in days
        },
        "not_a_complete_project_budget": True,
        "not_a_certification_or_permission": True,
    }


def check(root=ROOT):
    result = validate(load(PLAN_PATH, root), source_records(root), root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    check()
