"""Fail-closed measurement preregistration and synthetic signed-energy arithmetic.

No hardware communication, data acquisition, external contact, source downloads,
or raw-file modifications. This checker verifies a BLOCKED desk state only.
Synthetic trace arithmetic is a unit-test convenience, NOT qualified measurements.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "research/metrology_prereg_v1.json"
SOURCE_PROTOCOL = "research/experiment_protocol_v1.json"
REQUIRED_SOURCE_IDS = {
    "NIST-METROLOGY-007", "NIST-TN1297-007", "NI-STRAIN-007",
    "ASTM-E1049-007", "IEC-POWER-007",
}
REQUIRED_GATES = {
    "SOURCE_INFLOW", "CALIBRATION_CHAIN", "MECHANICAL_PHASE",
    "STRAIN_TRANSFER", "ANTI_ALIAS", "ELECTRIC_METER_BOUNDARY",
    "INDEPENDENT_REPLICATES", "STRUCTURAL_DAMAGE", "SAFETY_AND_AUTHORITIES",
}
TOY_UNITS = {
    "rotor_position": "rad",
    "rotor_speed": "rad/s",
    "shaft_torque": "N*m",
    "blade_root_strain": "microstrain",
    "delivered_electrical_power": "W",
    "control_and_actuator_power": "W",
}


class MetrologyGateError(ValueError):
    """Missing, contradictory, or falsely promoted engineering evidence."""


def require(condition, reason):
    if not condition:
        raise MetrologyGateError(reason)


def read(relative_path, root=ROOT):
    return json.loads((root / relative_path).read_text(encoding="utf-8"))


def check_prereg(registry=None, source=None, catalogue=None, root=ROOT):
    """Validate source mapping and explicit unknowns; ALWAYS yield a blocked plan."""
    p = read(REGISTRY_PATH, root) if registry is None else registry
    s = read(SOURCE_PROTOCOL, root) if source is None else source
    c = read("research/catalogue.json", root) if catalogue is None else catalogue
    old = read("research/lab_pilot_readiness_20261023.json", root)
    require(p.get("schema") == "TT-METROLOGY-PREREG-V1", "Unknown metrology schema")
    require(p.get("status") == "BLOCKED_REQUIRES_INDEPENDENT_METROLOGY_AND_STATISTICAL_REVIEW"
            and p.get("evidence_class") == "DESIGN_HYPOTHESIS_UNFROZEN_NOT_EXECUTED",
            "Plan cannot self-approve or claim measured findings")
    require(p.get("contact_and_physical_boundaries") == {
        "contact_anyone_authorized": False,
        "email_send_authorized": False,
        "draft_preparation_authorized": False,
        "purchasing_authorized": False,
        "laboratory_operation_authorized": False,
        "field_operation_authorized": False,
    }, "No contact, equipment or physical test approved")
    require(old["permissions"]["external_contact_authorized"] is False
            and old["physics_status"]["physical_lab_trials_documented"] == 0
            and old["physics_status"]["qualified_site_inflow_rows"] == 0,
            "Prior approved readiness/evidence is not a physical test")
    require(p.get("measured_results") == {
        "project_physical_test_count": 0,
        "qualified_force_site_inflow_rows": 0,
        "physical_blade_stress_measured": False,
        "project_net_electricity_measured": False,
        "independent_replicated_trials_completed": 0,
        "validated_fatigue_life_claim": False,
        "prototype_winner": None,
    }, "Desk evidence cannot become physical results")
    require(s["physical_experiments_run"] == 0 and
            s["qualified_site_inflow_rows"] == 0 and
            s["prototype_winner"] is None and
            s["field_deployment_authorized"] is False,
            "Original physical experiment not executed")
    comp = s["comparator"]
    pcomp = p.get("comparator", {})
    require(pcomp.get("architecture") == "CROSSFLOW-RM2-REFERENCE"
            and pcomp.get("baseline_historic_run") == comp["baseline_source_run"] == 12
            and pcomp.get("candidate_historic_run") == comp["candidate_source_run"] == 10
            and pcomp.get("baseline_nominal_tsr") == comp["baseline_nominal_tsr"]
            and pcomp.get("candidate_nominal_tsr") == comp["candidate_nominal_tsr"]
            and pcomp.get("source_means_are_historic_and_exposed") is True
            and pcomp.get("previous_raw_rig_force_is_not_blade_root_stress") is True,
            "Historical reference cannot be treated as new stress/power evidence")
    channels = p.get("channels", [])
    source_channels = {ch["id"]: ch["si"] for ch in s["mandatory_synced_channels"]}
    require(isinstance(channels, list)
            and len(channels) == len(source_channels) == 12
            and {ch.get("id") for ch in channels} == set(source_channels),
            "All 12 measurement channels required without duplicates")
    zero_fields = (
        "serial_number", "calibration_record", "calibration_uncertainty_statement",
        "pre_test_zero_check", "post_test_drift_check",
        "signed_axis_and_wiring_mapping", "common_clock_channel_latency_evidence",
        "raw_signal_sha256", "quality_mask_definition",
    )
    for ch in channels:
        require(ch["units"] == source_channels[ch["id"]] and
                isinstance(ch.get("role"), str) and ch["role"] and
                ch.get("calibration_required") is (ch["id"] != "rig_status") and
                all(k in ch and ch[k] is None for k in zero_fields),
                "Cannot invent instruments, calibration, signed axes, timebase or raw traces")
    clock = p.get("clock_and_signal_design", {})
    required_clock = {
        "common_clock_source", "utc_epoch_anchor_and_timezone",
        "per_channel_latency_and_jitter_budget_s",
        "measured_cross_channel_delay_s",
        "highest_mechanically_relevant_frequency_hz",
        "selected_sampling_rate_hz", "anti_alias_filter_design_and_phase_response",
        "encoder_zero_and_direction_validation",
        "transient_bandwidth_and_overload_limits",
        "planned_lab_flow_stabilization_window_s",
        "selected_blade_strain_bridge_type", "selected_bridge_excitation_v",
        "selected_bridge_remote_sense_and_shunt_check",
        "material_specific_microstrain_to_stress_transfer",
    }
    require(set(clock) == required_clock and all(v is None for v in clock.values()),
            "Time, strain conditioning and sample rate require actual device evidence")
    power = p.get("electrical_boundary", {})
    require(power.get("meter_sign_convention_delivered") ==
            "POSITIVE_EXPORT_NEGATIVE_IMPORT" and
            power.get("meter_sign_convention_auxiliary") ==
            "POSITIVE_CONSUMPTION_NEGATIVE_RECOVERY" and
            power.get("separate_auxiliary_subtraction_rule") ==
            "SUBTRACT_ONLY_IF_OUTSIDE_DELIVERED_METER_BOUNDARY",
            "Signed power boundaries and no-double-count rule must stay explicit")
    power_undecided = {
        "delivered_meter_position", "generator_meter_position",
        "auxiliary_meter_inside_delivered_meter_boundary",
        "signed_control_regeneration_handling",
        "storage_state_matched_or_corrected",
        "synchronized_meter_calibration_and_uncertainty",
    }
    require(power_undecided <= set(power) and
            all(power[k] is None for k in power_undecided),
            "No metering topology or storage assumptions have been selected")
    trial = p.get("paired_trial_design", {})
    require(trial.get("prospective_order") == "RANDOMIZED_AB_BA"
            and trial.get("trial_unit") ==
                "SEPARATELY_PREPARED_EXPERIMENTAL_RUN_NOT_SAMPLES_OR_ROTOR_CYCLES",
            "Time samples/turns are NOT independent replicate runs")
    trial_frozen = {
        "independent_group_definition",
        "randomization_seed_and_frozen_allocation",
        "matched_flow_and_turbulence_tolerances",
        "primary_peak_or_cycle_stress_metric",
        "phase_bin_definition",
        "material_fatigue_law_and_validity_evidence",
        "signed_net_energy_metric_and_test_period",
        "acceptable_energy_penalty",
        "minimum_relevant_stress_reduction",
        "sample_size_and_power_justification",
        "preregistered_uncertainty_and_autocorrelation_method",
        "failure_exclusion_and_trip_policy",
        "independently_reviewed_protocol_receipt", "preregistration_timestamp_utc",
    }
    require(trial_frozen <= set(trial) and
            all(trial[k] is None for k in trial_frozen),
            "No numeric inference criteria can be retroactively invented")
    integrity = p.get("data_integrity", {})
    require(integrity and all(v is None for v in integrity.values()),
            "No physical logs/calibration/source hash or facility authority obtained")
    gates = p.get("independent_acceptance_gates", [])
    require(len(gates) == len(REQUIRED_GATES) and
            {g.get("id") for g in gates} == REQUIRED_GATES and
            all(g.get("state") == "UNRESOLVED"
                and isinstance(g.get("required"), str) and g["required"]
                for g in gates),
            "No physical, safety, uncertainty or statistics gate has passed")
    seen = {x["id"]: x for x in c}
    require(set(p.get("referenced_sources", [])) == REQUIRED_SOURCE_IDS
            and all(x in seen and seen[x]["url"].startswith("https://")
                    and seen[x]["limitations"] for x in REQUIRED_SOURCE_IDS),
            "Source provenance must be linked to reviewed catalogue records")
    for path in p.get("canonical_documents", []):
        require((root / path).is_file(), "Missing canonical document: " + path)
    return {
        "status": "BLOCKED_DESK_METROLOGY_UNFROZEN",
        "required_channels": len(channels),
        "uncalibrated_or_undocumented_channels": sum(
            ch["calibration_required"] for ch in channels),
        "unresolved_physical_acceptance_gates": len(gates),
        "selected_sampling_rate_hz": None,
        "registered_sample_size": None,
        "physical_test_authorized": False,
        "external_contact_authorized": False,
        "lab_fatigue_and_net_power_validated": False,
    }


def _checked_series(name, channel):
    """Strict synthetic-only per-channel timestamps and units; no interpolation."""
    require(isinstance(channel, dict)
            and channel.get("unit") == TOY_UNITS[name]
            and channel.get("clock_id") == "SYNTHETIC_SINGLE_CLOCK",
            f"Malformed synthetic channel: {name}")
    times, values = channel.get("t_s"), channel.get("values")
    require(isinstance(times, list) and isinstance(values, list)
            and len(times) == len(values) and len(times) >= 2,
            f"{name}: times and values must have at least two matching samples")
    for t, value in zip(times, values):
        require(type(t) in (int, float) and type(value) in (int, float)
                and math.isfinite(t) and math.isfinite(value),
                f"{name}: nonfinite or nonnumeric synthetic data")
    require(all(b > a for a, b in zip(times, times[1:])),
            f"{name}: time repeats or moves backwards")
    return times, values


def _trapz(times, values):
    return math.fsum((b - a) * (y0 + y1) / 2.0
                     for a, b, y0, y1 in zip(times, times[1:],
                                              values, values[1:]))


def audit_synthetic_energy(toy):
    """Check signed energy math for a toy trace, never a physical run.

    Meter boundary: SEPARATE_FROM_LOAD_METER subtracts separately metered
    auxiliaries; ALREADY_INCLUDED_IN_LOAD_METER does not subtract twice.
    This function is NOT a general observed-data analysis/qualification API.
    """
    require(isinstance(toy, dict) and
            toy.get("classification") == "SYNTHETIC_UNIT_TEST_ONLY" and
            toy.get("physical_run_id") is None and
            toy.get("material_calibration") is None,
            "No physical run, stress calibration or provenance may be asserted")
    boundary = toy.get("auxiliary_meter_boundary")
    require(boundary in {
        "SEPARATE_FROM_LOAD_METER", "ALREADY_INCLUDED_IN_LOAD_METER"
    }, "Unresolved or invalid auxiliary boundary: prevent double counting")
    channels = toy.get("channels")
    require(isinstance(channels, dict) and set(channels) == set(TOY_UNITS),
            "Toy includes exact time-aligned torque, rotation, strain and electric signals")
    series = {name: _checked_series(name, channels[name]) for name in TOY_UNITS}
    times = series["rotor_position"][0]
    require(all(t == times for t, _ in series.values()),
            "Toy sample clocks differ; never silently resample/merge")
    torque = series["shaft_torque"][1]
    speed = series["rotor_speed"][1]
    delivered = series["delivered_electrical_power"][1]
    aux = series["control_and_actuator_power"][1]
    mechanical = _trapz(times, [a*b for a, b in zip(torque, speed)])
    delivered_j = _trapz(times, delivered)
    aux_j = _trapz(times, aux)
    net_j = delivered_j - aux_j if boundary == "SEPARATE_FROM_LOAD_METER" else delivered_j
    require(all(math.isfinite(x) for x in (mechanical, delivered_j, aux_j, net_j)),
            "Arithmetic overflow is not physical evidence")
    return {
        "status": "SYNTHETIC_MATH_ONLY_NOT_MEASURED",
        "synthetic_mechanical_work_j": round(mechanical, 9),
        "synthetic_delivered_meter_energy_j": round(delivered_j, 9),
        "synthetic_auxiliary_energy_j": round(aux_j, 9),
        "synthetic_net_energy_j": round(net_j, 9),
        "auxiliary_boundary": boundary,
        "source_measured_power_or_load": False,
        "calibrated_blade_stress_pa": None,
        "fatigue_damage": None,
        "independent_replicates": None,
    }


def synthetic_fixture(boundary="SEPARATE_FROM_LOAD_METER"):
    values = {
        "rotor_position": [0.0, 1.0, 2.0],
        "rotor_speed": [3.0, 3.0, 3.0],
        "shaft_torque": [2.0, 2.0, 2.0],
        "blade_root_strain": [-10.0, 0.0, 10.0],
        "delivered_electrical_power": [4.0, 4.0, 4.0],
        "control_and_actuator_power": [1.0, 1.0, 1.0],
    }
    return {
        "classification": "SYNTHETIC_UNIT_TEST_ONLY",
        "physical_run_id": None,
        "material_calibration": None,
        "auxiliary_meter_boundary": boundary,
        "channels": {
            name: {
                "unit": TOY_UNITS[name],
                "clock_id": "SYNTHETIC_SINGLE_CLOCK",
                "t_s": [0.0, 1.0, 2.0],
                "values": vals
            } for name, vals in values.items()
        },
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toy", action="store_true",
                        help="Show synthetic arithmetic, not experimental validation")
    args = parser.parse_args()
    result = check_prereg()
    if args.toy:
        result["separate_aux_example"] = audit_synthetic_energy(synthetic_fixture())
        result["already_in_meter_example"] = audit_synthetic_energy(
            synthetic_fixture("ALREADY_INCLUDED_IN_LOAD_METER"))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
