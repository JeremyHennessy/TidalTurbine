"""Offline, fail-closed reproduction of Bharath et al. OMAE2023 Table 1.

This script reads published summary *transcription*, NOT the original source
strain, clock, QC, shaft speed, thrust or electrical waveforms. No network.
No files written. Passing does not validate physical fatigue or net energy.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_PATH = "research/UNH_2023_PUBLISHED_STRAIN_001.json"
SOURCE_CATALOGUE = "research/catalogue.json"
PREVIOUS_SOURCE = "research/UNH_2022_SOURCE_ACCESS_001.json"
SOURCE_URL = "https://tethys-engineering.pnnl.gov/sites/default/files/publications/Bharath_et_al_2023.pdf"
SOURCE_ID = "UNH-2023-OMAE-BLADE-010"
# Exact numbers extracted from p8 Table 1, the 2022-11-22 sample.
# Numerical Table 1 unit is not qualified in accessible PDF extraction.
TABLE1 = (
    (1, 8.1, 12.1, 4.3, 1.1),
    (2, 37.1, 118.3, 21.7, 5.7),
    (3, 86.8, 120.8, 51.0, 11.4),
    (4, 55.6, 91.3, 24.2, 10.8),
    (5, 21.5, 37.3, 9.7, 4.5),
    (6, 35.7, 63.3, 17.8, 7.0),
    (7, 69.7, 100.1, 40.6, 8.0),
    (8, 6.3, 10.1, 4.1, 0.7),
)


class PublishedEvidenceError(ValueError):
    """Source/provenance or scientific qualification boundary violated."""


def require(condition, message):
    if not condition:
        raise PublishedEvidenceError(message)


def read(path, root=ROOT):
    return json.loads((root / path).read_text(encoding="utf-8"))


def check(record=None, catalogue=None, original=None):
    item = read(TABLE_PATH) if record is None else record
    sources = read(SOURCE_CATALOGUE) if catalogue is None else catalogue
    previous = read(PREVIOUS_SOURCE) if original is None else original
    require(item.get("schema") == "TT-UNH-2023-PUBLISHED-STRAIN-V1"
            and item.get("classification") ==
            "PUBLISHED_TABLE_TRANSCRIPTION_AND_BOUNDARY_REVIEW_NOT_ORIGINAL_SENSOR_DATA",
            "Published descriptive data must not be promoted to original source validation")
    src = item.get("source", {})
    require(src.get("id") == SOURCE_ID and src.get("url") == SOURCE_URL
            and src.get("conference") == "OMAE 2023"
            and src.get("paper_number") == "OMAE2023-101076"
            and src.get("source_text_extracted") is True
            and src.get("visual_pdf_screenshot_confirmed") is False
            and src.get("original_sensor_archives_acquired") is False
            and src.get("original_raw_strain_SI_units_confirmed") is False,
            "Original/visually verified data cannot be invented")
    matching = [c for c in sources if c.get("id") == SOURCE_ID]
    require(len(matching) == 1
            and matching[0].get("url") == SOURCE_URL
            and matching[0].get("evidence_class") == "PUBLISHED_EVIDENCE"
            and matching[0].get("review_depth") == "sections_reviewed"
            and len(matching[0].get("limitations", [])) >= 4,
            "Published table must retain source catalogue lineage and reviewed limits")
    table = item.get("table", {})
    require(table.get("source_date") == "2022-11-22"
            and table.get("event_description") ==
                "TABLE_1_NOV22_PUBLISHED_PER_REV_PEAK_TO_TROUGH_STRAIN_DIFFERENCES"
            and table.get("units") is None
            and table.get("unit_status") ==
                "NOT_PRESENT_IN_EXTRACTED_TABLE_1_TEXT_DO_NOT_ASSIGN_MICROSTRAIN_OR_PASCAL"
            and table.get("statistic_headers") == ["MEAN", "MAX", "MIN", "STD"]
            and table.get("source_highest_mean_gauges") == [3, 7]
            and table.get("raw_trace_available") is False
            and table.get("stress_transfer_calibrated") is False
            and table.get("observed_cycles_count") is None
            and table.get("material_fatigue_curve") is None,
            "Nov22 table unit, source sample or fatigue qualifications are unknown")
    rows = table.get("values")
    require(isinstance(rows, list) and len(rows) == 8,
            "Require all eight original-gauge rows")
    require(len({x.get("gauge") for x in rows}) == 8,
            "Gauge identifiers missing/duplicated")
    for row, (gauge, mean, maximum, minimum, std) in zip(rows, TABLE1):
        require(row.get("gauge") == gauge
                and tuple(row.get(k) for k in ("mean", "max", "min", "std")) ==
                    (mean, maximum, minimum, std)
                and all(type(row.get(k)) in (int, float) and math.isfinite(row[k])
                        for k in ("mean", "max", "min", "std"))
                and row["min"] <= row["mean"] <= row["max"]
                and row["std"] >= 0,
                "Published descriptive gauge statistics altered or nonsensical")
        position = row.get("position")
        expected = ("ABOVE_UPPER_STRUT_NEAREST" if gauge == 3
                    else "BELOW_LOWER_STRUT_NEAREST" if gauge == 7
                    else "ABOVE_UPPER_STRUT" if gauge <= 2
                    else "BETWEEN_STRUTS" if gauge <= 6
                    else "BELOW_LOWER_STRUT")
        require(position == expected,
                "Strut-relative source gauge locations may not be invented")
    turbine = item.get("published_device", {})
    require(turbine.get("blade_count") == 4
            and turbine.get("diameter_m") == 3.2
            and turbine.get("height_m") == 1.7
            and turbine.get("blade_chord_m") == 0.25
            and turbine.get("pitch_deg") == 4
            and turbine.get("blades_with_strain_gauges") == 1
            and turbine.get("gauges_on_blade") == 8
            and turbine.get("rotor_fabrication_selected_for_our_project") is False,
            "Published turbine is not our fabrication specification")
    system = item.get("experiment_system", {})
    require(system.get("instrumented_blade_operation") == "OFF_GRID_DUMP_LOAD"
            and system.get("rectifier_to_dump_resistor_capacity_kW") == 25
            and system.get("grid_energy_delivery_in_described_test") ==
                "NOT_A_NET_GRID_EXPORT_MEASUREMENT"
            and system.get("auxiliary_energy_meter_boundary_verified") is False
            and system.get("power_data_average_duration_seconds") == 1
            and system.get("phase_resolved_electric_power_validated") is False
            and system.get("time_resolved_power_and_strain_common_raw_interval_verified") is False
            and system.get("ADCP_and_CTD_linked_to_main_DAQ_during_paper") == "NO"
            and system.get("ADCP_CTD_external_clock_pre_sync_and_drift_estimated") is True
            and system.get("ADV_probes_near_rotor_induced_velocity") is True
            and system.get("sensor_retrofit_changes_geometry_and_drag") is True,
            "Grid export, raw clock or undisturbed inflow not source-validated")
    campaign = item.get("published_campaign_context", {})
    require(campaign.get("rpm_min") == 18
            and campaign.get("rpm_max") == 31
            and campaign.get("thrust_mean_kN") == 6.4
            and campaign.get("thrust_peak_kN") == 11.5
            and campaign.get("thrust_and_rpm_are_full_deployment_descriptions_not_paired_Table1_samples") is True
            and campaign.get("late_november_2025_analysed_ebb_same_as_Nov22_not_proven") is True
            and campaign.get("ADV_upstream_support_pipe_damaged_utc_date") == "2022-11-27"
            and campaign.get("upstream_ADV_removed_date") == "2022-12-08"
            and campaign.get("sample_specific_undisturbed_upstream_speed_qualified") is False,
            "Unpaired campaign-wide context cannot be misrepresented as matched Nov22 condition")
    gate = item.get("project_scientific_boundary", {})
    require(gate == {
        "original_source_archives_acquired": 0,
        "qualified_original_sensor_windows": 0,
        "project_blade_stress_measurements": 0,
        "project_net_electricity_measurements": 0,
        "project_physical_trials": 0,
        "source_specific_strain_fatigue_life_confirmed": False,
        "cross_turbine_winner": None,
        "external_contacts_authorized": False,
        "field_authorization": False,
        "source_access_bypass": False,
    }, "No physical turbine evidence or contact may be asserted")
    require(previous["verified_original_archives"] == 0
            and previous["scientifically_qualified_common_windows"] == 0
            and previous["qualified_net_electricity_runs"] == 0
            and previous["contact_authorized"] is False,
            "Original source access remains blocked")
    deriv = item.get("derivations", {})
    require(deriv.get("evidence_class") ==
                "ENGINEERING_ASSUMPTION_DIMENSIONAL_IDENTITY_ONLY"
            and deriv.get("inferred_measured_fatigue_cycles") is None
            and deriv.get("dynamically_resolved_power_from_1_second_averages") is False
            and deriv.get("frequency_unit") == "Hz",
            "Blade passage arithmetic cannot prove measured fatigue/power")
    blade_count = turbine["blade_count"]
    rpm_lo, rpm_hi = campaign["rpm_min"], campaign["rpm_max"]
    blade_pass_hz = [round(blade_count * rpm / 60, 6)
                     for rpm in (rpm_lo, rpm_hi)]
    return {
        "status": "PUBLISHED_TABLE_ONLY_ORIGINAL_SENSOR_DATA_UNQUALIFIED",
        "published_table_date": table["source_date"],
        "published_table_evidence_count": len(rows),
        "published_mean_peak_to_trough_by_gauge": [
            {"gauge": r["gauge"], "mean_as_printed": r["mean"]} for r in rows],
        "table_units": None,
        "strongest_reported_gauge_positions": [3, 7],
        "published_campaign_thrust_mean_kN_not_sample_matched": 6.4,
        "published_campaign_thrust_peak_kN_not_sample_matched": 11.5,
        "idealized_blade_pass_frequency_range_hz_from_reported_rpm": blade_pass_hz,
        "power_averaging_seconds": 1,
        "power_mode": "OFF_GRID_DUMP_LOAD",
        "grid_net_electricity_validated": False,
        "original_qualified_source_utc_intervals": 0,
        "project_fatigue_or_net_energy_result": False,
        "not_a_build_or_test_authorization": True,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
