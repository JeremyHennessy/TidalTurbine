"""Offline, assumption-labelled rotor kinematics in the published Memorial towing tank.

Pure dimensional arithmetic; NOT hardware sizing, a flow test, a sampling rate,
a reliable number of independent observations, validated stress cycles, or power.
No network activity, files written, communications, or bookings.
"""
import argparse
import json
import math
from pathlib import Path
from scripts.check_lab_venue_screen import (
    ScreenError, check as check_venue, load as load_venue,
    tow_time_upper_bound
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "research/experiment_protocol_v1.json"


def positive_real(label, value):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value <= 0):
        raise ScreenError(label + " must be a finite positive real number")
    return float(value)


def make_row(speed_m_s, tsr, diameter_m, blade_count, kinematic):
    """Rotor-count arithmetic only, assuming the target TSR holds continuously."""
    plateau_s = kinematic["ideal_constant_speed_time_upper_bound_s"]
    rev_frequency_hz = tsr * speed_m_s / (math.pi * diameter_m)
    rotor_turns = plateau_s * rev_frequency_hz
    blade_passes = blade_count * rotor_turns
    if not all(math.isfinite(v) for v in (
            rev_frequency_hz, rotor_turns, blade_passes)):
        raise ScreenError("Calculated kinematic quantities must remain finite")
    return {
        "nominal_tsr": tsr,
        "nominal_carriage_speed_m_s": speed_m_s,
        "ideal_constant_speed_time_s": plateau_s,
        "hypothetical_rotor_frequency_hz": round(rev_frequency_hz, 6),
        "hypothetical_rotor_rpm": round(60 * rev_frequency_hz, 4),
        "hypothetical_rotor_revolutions_per_tow": round(rotor_turns, 4),
        "hypothetical_aggregate_blade_passages_per_tow": round(blade_passes, 4),
        "measured_rotor_revolutions": None,
        "calibrated_blade_root_stress_cycles": None,
        "independent_replicates": None,
        "actual_usable_steady_duration_s": None,
        "measurement_sampling_hz": None,
        "evidence_class": "ENGINEERING_ASSUMPTION_NOT_PHYSICAL_MEASUREMENT",
    }


def screen(assumed_diameter_m, assumed_blades, assumed_margin_m=0.0,
           venue_data=None, protocol_data=None):
    """Hypothetical rotor exposure for two source-based RM2 nominal TSR points."""
    diameter = positive_real("Assumed diameter", assumed_diameter_m)
    if (isinstance(assumed_blades, bool) or
            not isinstance(assumed_blades, int) or assumed_blades < 1):
        raise ScreenError("Assumed blade count must be a positive integer")
    if (isinstance(assumed_margin_m, bool)
            or not isinstance(assumed_margin_m, (int, float))
            or not math.isfinite(assumed_margin_m) or assumed_margin_m < 0):
        raise ScreenError("Assumed reserved travel must be finite nonnegative metres")
    venue_data = venue_data if venue_data is not None else load_venue()
    venue_report = check_venue(venue_data)
    if venue_report["status"] != "DESK_ONLY_NOT_READY_FOR_TEST" or venue_report["emails_or_contacts_permitted"]:
        raise ScreenError("Source is not in the expected blocked, no-contact state")
    proto = protocol_data if protocol_data is not None else json.loads(
        (ROOT / PROTOCOL).read_text(encoding="utf-8"))
    if (proto.get("schema_version") != "TT-EXPERIMENT-V1"
            or proto.get("physical_experiments_run") != 0
            or proto.get("prototype_winner") is not None
            or proto.get("field_deployment_authorized") is not False):
        raise ScreenError("The scientific protocol no longer matches the unexecuted source")
    comp = proto["comparator"]
    if comp.get("baseline_source_run") != 12 or comp.get("candidate_source_run") != 10:
        raise ScreenError("Source RM2 regime references changed; review before replay")
    tsrs = (
        {"role": "RM2_RUN_12_BASELINE",
         "value": positive_real("Baseline source TSR", comp["baseline_nominal_tsr"])},
        {"role": "RM2_RUN_10_CANDIDATE",
         "value": positive_real("Candidate source TSR", comp["candidate_nominal_tsr"])},
    )
    test = venue_data["optimistic_tow_screen"]
    length = test["published_usable_length_m"]
    accel = test["assumed_acceleration_m_s2"]
    braking = test["assumed_braking_m_s2"]
    if assumed_margin_m >= length:
        raise ScreenError("Reserved margin cannot consume or exceed the published 35m travel")
    outcome = []
    for flow in test["modeled_speed_setpoints_m_s"]:
        tow = tow_time_upper_bound(flow, length, accel, braking, assumed_margin_m)
        if tow is None:
            outcome.append({
                "assumed_speed_m_s": flow, "status": "NO_IDEAL_CONSTANT_SPEED_PLATEAU",
                "ideal_tow_bounds": None, "regimes": []
            })
        else:
            outcome.append({
                "assumed_speed_m_s": flow, "status": "ILLUSTRATIVE_WINDOW_ONLY",
                "ideal_tow_bounds": tow,
                "regimes": [
                    {"role": item["role"], **make_row(
                        flow, item["value"], diameter, assumed_blades, tow)}
                    for item in tsrs
                ]
            })
    return {
        "status": "SYNTHETIC_KINEMATIC_SCREEN_NOT_READY_FOR_LAB_OR_FIELD",
        "classification": "ENGINEERING_ASSUMPTION",
        "facility": "MUN-TOW",
        "assumed_rotor_diameter_m_not_a_design": diameter,
        "assumed_blade_count_not_a_design": assumed_blades,
        "assumed_reserved_travel_m_not_certified": float(assumed_margin_m),
        "reference_source": PROTOCOL,
        "input_setpoints_not_measured_site_currents": True,
        "assumed_tsr_held_constant_during_plateau": True,
        "results": outcome,
        "physical_build_or_operation_authorized": False,
        "outreach_authorized": False,
        "qualified_lab_or_field_data": False,
        "fatigue_life_prediction": None,
        "net_electricity_measurement": None,
        "statistically_sufficient_replicates": None,
        "required_next_evidence": [
            "facility-approved test envelope, braking, clearances and stabilization times",
            "measured rotor speed/phase and full inflow profile, actual test timing",
            "calibrated blade-root and support-strut stress history and material basis",
            "metered delivered electricity minus separately tracked controller/actuator draw",
            "independent paired replicated AB/BA protocol with preregistered statistical tolerances",
            "professional safety/guarding review and explicit facility authorization"
        ],
        "interpretation": "Blade passages and ideal turns are not measured strain cycles, "
                          "independent replicates, or fatigue-life evidence. Every assumed "
                          "rotor dimension is a what-if value, not a build specification."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assumed-diameter-m", type=float, required=True,
                        help="EXPLICIT example only; not a design-selected rotor diameter")
    parser.add_argument("--assumed-blades", type=int, required=True,
                        help="EXPLICIT illustrative blade count; not an engineered selection")
    parser.add_argument("--assumed-reserved-travel-m", type=float, default=0.0,
                        help="Extra total travel reserved beyond original published 35m usable length")
    args = parser.parse_args()
    result = screen(args.assumed_diameter_m, args.assumed_blades,
                    args.assumed_reserved_travel_m)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
