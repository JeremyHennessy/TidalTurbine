"""Read-only, offline laboratory venue and idealized towing-window screen.

No contacts, network, files written, promises of test viability, or physical design.
The mathematical constant-speed window is an OPTIMISTIC upper bound under
assumed identical maximum acceleration and deceleration, zero extra margins,
and a previously published *usable length*, not a facility-approved work time.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN_FILE = "research/lab_venue_screen_20261023.json"


class ScreenError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ScreenError(message)


def load(root=ROOT):
    return json.loads((root / SCREEN_FILE).read_text(encoding="utf-8"))


def tow_time_upper_bound(speed, length, acceleration, braking, margin=0):
    """Calculate an idealized bound, returning None if target speed is unreachable.

    Acceleration and braking are positive magnitudes (m/s2).
    Travel begins and ends at rest. All available length is used; this is
    not a real safe test window and omits all stabilization/clearance needs.
    """
    values = (speed, length, acceleration, braking, margin)
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
               and math.isfinite(v) for v in values):
        raise ScreenError("Inputs must be finite real quantities")
    if speed <= 0 or length <= 0 or acceleration <= 0 or braking <= 0 or margin < 0 or margin >= length:
        raise ScreenError("Invalid or nonpositive kinematics / nonnegative margin")
    accel_distance = speed * speed / (2 * acceleration)
    braking_distance = speed * speed / (2 * braking)
    plateau_distance = length - margin - accel_distance - braking_distance
    if plateau_distance <= 0:
        return None
    return {
        "target_speed_m_s": speed,
        "assumed_ramp_distance_m": round(accel_distance + braking_distance, 4),
        "ideal_constant_speed_length_m": round(plateau_distance, 4),
        "ideal_constant_speed_time_upper_bound_s": round(plateau_distance / speed, 4),
        "physically_qualified": False,
    }


def check(data, root=ROOT):
    require(data.get("schema") == "TT-LAB-VENUE-SCREEN-1", "Unexpected schema")
    require(data.get("classification") == "SOURCE_REVIEW_PLUS_IDEALIZED_KINEMATICS_NO_NEW_MEASUREMENTS",
            "Do not promote desk calculations to measured evidence")
    hold = data.get("user_hold", {})
    require(hold == {
        "external_contacts": "ON_HOLD_BY_USER", "email_send_authorized": False,
        "booking_authorized": False, "purchase_authorized": False,
        "physical_test_authorized": False
    }, "Outreach / build is explicitly on hold")
    require(data.get("experimental_claims") == {
        "new_physical_tests": 0, "source_qualified_site_inflow_rows": 0,
        "measured_net_electricity": False, "calibrated_blade_stress": False,
        "prototype_winner": None
    }, "No project experiment, site qualification or design winner exists")
    require(len(data.get("measurement_gate", [])) >= 6, "Missing simultaneous physical gates")
    original = json.loads((root / "research/lab_pilot_readiness_20261023.json").read_text(encoding="utf-8"))
    proto = json.loads((root / "research/experiment_protocol_v1.json").read_text(encoding="utf-8"))
    require(original["permissions"]["external_contact_authorized"] is False and
            original["physics_status"]["physical_lab_trials_documented"] == 0 and
            original["physics_status"]["qualified_site_inflow_rows"] == 0 and
            proto["physical_experiments_run"] == 0, "Prior source evidence has changed")
    venues = data.get("venues", [])
    require(len(venues) == 4 and {v["id"] for v in venues} ==
            {"DAL-AQUATRON", "MUN-TOW", "MI-CSAR", "COVE-STELLA"},
            "Venue inventory incomplete or duplicated")
    source_ids = {v["id"] for v in original["venues"]}
    require(all(v["id"] in source_ids for v in venues), "Venue not supported by original qualified research")
    by_id = {v["id"]: v for v in venues}
    for venue in venues:
        require(venue["current_test_acceptance"] == "UNKNOWN" and
                venue["current_instrument_compatibility"] == "UNKNOWN" and
                len(venue.get("sources", [])) >= 1 and
                all(s["url"].startswith("https://") for s in venue["sources"]),
                "Do not invent test authorization, metrology or untraceable sources")
    dal = by_id["DAL-AQUATRON"]
    require(dal["historical_test_year"] == 2017 and
            dal["historical_tank_diameter_m"] == 15.24 and
            dal["historical_test_depth_m"] == 4.0 and
            dal["historical_turbine_diameter_m"] == 0.9 and
            dal["historical_pump_reported_speed_range_m_s"] == [0.6, 2.4] and
            "1.5" in dal["historical_flow_conflict"] and "2.0" in dal["historical_flow_conflict"] and
            dal["published_rate_amount"] is None,
            "Historical Aquatron parameters/contradiction must be retained")
    tow = by_id["MUN-TOW"]
    require(tow["published_usable_length_m"] == 35.0 and
            tow["published_width_m"] == 4.5 and
            tow["published_max_depth_m"] == 3.04 and
            tow["published_max_carriage_speed_m_s"] == 5.0 and
            tow["published_max_carriage_acceleration_m_s2"] == 2.0 and
            tow["published_rate_amount"] == 1000 and
            tow["published_rate_currency"] is None and
            tow["controlled_tow_time_verified"] is False,
            "Public towing tank specification/list rate not adopted as guaranteed trial capacity")
    flume = by_id["MI-CSAR"]
    require(flume["published_rate_amount"] == 5000 and
            flume["published_rate_currency"] == "CAD" and
            flume["rate_effective_date"] == "2026-04-01",
            "Do not mix rate or currency between separate facilities")
    require(by_id["COVE-STELLA"]["published_rate_amount"] is None,
            "No COVE project price has been verified")
    t = data.get("optimistic_tow_screen", {})
    require(t["applies_only_to"] == "MUN-TOW" and
            t["published_usable_length_m"] == tow["published_usable_length_m"] and
            t["published_max_carriage_acceleration_m_s2"] == tow["published_max_carriage_acceleration_m_s2"] and
            t["published_max_carriage_speed_m_s"] == tow["published_max_carriage_speed_m_s"] and
            t["assumed_initial_speed_m_s"] == 0.0 and
            t["assumed_final_speed_m_s"] == 0.0 and
            t["assumed_acceleration_m_s2"] == 2.0 and
            t["assumed_braking_m_s2"] == 2.0 and
            t["assumed_extra_safety_margin_m"] == 0.0 and
            t["modeled_speed_setpoints_m_s"] == [0.6, 1.0, 1.4] and
            t["usable_time_is_optimistic_bound"] is True and
            t["guaranteed_steady_speed_time_s"] is None,
            "An idealized tow calculation must never become a guaranteed real-world capability")
    require(len(t["does_not_include"]) >= 8, "Missing physical limitations")
    results = []
    for speed in t["modeled_speed_setpoints_m_s"]:
        require(speed <= t["published_max_carriage_speed_m_s"],
                "Planning setpoint exceeds published maximum carriage speed")
        results.append(tow_time_upper_bound(
            speed, t["published_usable_length_m"],
            t["assumed_acceleration_m_s2"], t["assumed_braking_m_s2"],
            t["assumed_extra_safety_margin_m"]
        ))
    require(len(data.get("blockers", [])) >= 6, "Unresolved qualification gates missing")
    return {
        "status": "DESK_ONLY_NOT_READY_FOR_TEST",
        "emails_or_contacts_permitted": False,
        "facility_accepted": False,
        "prototype_measured": False,
        "qualified_site_inflow_rows": 0,
        "project_quotes_verified": 0,
        "optimistic_tow_windows": results,
        "warning": "IDEALIZED upper bounds only: NOT guaranteed test duration or physical feasibility; published rate is not a project quote."
    }


if __name__ == "__main__":
    print(json.dumps(check(load()), indent=2))
