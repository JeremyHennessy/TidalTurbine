"""Offline metadata gate. A complete checklist is NOT scientific validation.

No downloads, source-data promotion, simulation, or physical authorization.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "force_native_inflow": {
        "instrument_configuration_and_serial", "per_beam_native_quality",
        "range_centres_and_absolute_vertical_reference", "zero_missing_and_transform_lineage",
        "surface_sidelobe_nearbed_and_motion_masks", "independent_mask_holdout_review",
    },
    "unh_concurrent_sample": {
        "instrument_readmes_units_and_license", "calibration_offsets_drift_and_ranges",
        "clock_epoch_timezone_sync_and_drift", "source_quality_flags_and_missing_encodings",
        "actual_common_interval_and_test_log", "upstream_flow_direction_and_adcp_geometry",
        "meter_boundary_sign_and_auxiliary_accounting",
    },
    "predictive_holdout": {
        "frozen_solver_commit_and_environment", "frozen_parameter_and_calibration_manifest",
        "group_disjoint_source_split_and_leakage_audit", "frozen_preprocessing_and_exclusions",
        "frozen_observables_units_and_denominators", "predeclared_numeric_acceptance_and_uncertainty",
        "independent_replicate_and_autocorrelation_plan",
        "prediction_artifact_before_target_unblinding", "independent_review_of_registered_protocol",
    },
}


def assess(document):
    """Return structural errors and unresolved gates; never approve ingestion."""
    errors, blocked = [], []
    if not isinstance(document, dict):
        return {"errors": ["document must be an object"], "blocked": [],
                "status": "INVALID", "scientific_validation": False}
    if document.get("schema_version") != "TT-RESEARCH-READINESS-V1":
        errors.append("unsupported schema_version")
    if document.get("classification") != "DESIGN_HYPOTHESIS":
        errors.append("readiness V1 requires DESIGN_HYPOTHESIS classification")
    counts = {"qualified_force_inflow_rows", "unh_original_samples_acquired",
              "independent_predictive_holdouts_completed"}
    claims = {"predictive_validation_claim", "net_electrical_validation_claim",
              "blade_stress_validation_claim"}
    results = document.get("current_results")
    if not isinstance(results, dict) or set(results) != counts | claims:
        errors.append("exact current_results keys required")
    else:
        for key in counts:
            if type(results[key]) is not int or results[key] < 0:
                errors.append(f"{key}: nonnegative integer required")
        for key in claims:
            if results[key] is not False:
                errors.append(f"{key}: metadata-only V1 cannot claim scientific validation")
    gates = document.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(REQUIRED):
        errors.append("exact gate families required")
        gates = gates if isinstance(gates, dict) else {}
    for family, names in REQUIRED.items():
        group = gates.get(family)
        if not isinstance(group, dict) or set(group) != names:
            errors.append(f"{family}: exact prerequisite set required")
            group = group if isinstance(group, dict) else {}
        for name in sorted(names):
            item = group.get(name)
            key = f"{family}.{name}"
            if not isinstance(item, dict) or set(item) != {"status", "evidence"}:
                errors.append(f"{key}: status/evidence object required")
                continue
            status, evidence = item["status"], item["evidence"]
            if status not in ("UNRESOLVED", "DOCUMENTED"):
                errors.append(f"{key}: unsupported status")
            if status == "DOCUMENTED":
                # Human review still must verify contents, not only this pointer.
                if not isinstance(evidence, str) or not evidence.strip():
                    errors.append(f"{key}: documented prerequisite needs an evidence pointer")
            else:
                if evidence is not None and not isinstance(evidence, str):
                    errors.append(f"{key}: unresolved evidence must be null or text")
                blocked.append(key)
    expected_status = "BLOCKED_NOT_EXECUTED" if blocked else "CHECKLIST_COMPLETE_REVIEW_REQUIRED"
    if document.get("status") != expected_status:
        errors.append("top-level status inconsistent with prerequisite states")
    return {"errors": errors, "blocked": blocked,
            "status": "INVALID" if errors else ("BLOCKED" if blocked else "CHECKLIST_COMPLETE_REVIEW_REQUIRED"),
            "scientific_validation": False}


def check():
    doc = json.loads((ROOT / "research/validation_readiness_v1.json").read_text())
    result = assess(doc)
    if result["errors"]:
        raise ValueError("; ".join(result["errors"]))
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    check()
