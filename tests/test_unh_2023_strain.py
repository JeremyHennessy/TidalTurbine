"""Guard eight published per-revolution strain rows and source power constraints."""
import copy
import math
import unittest

from scripts.check_unh_2023_strain import (
    PublishedEvidenceError, check, read, TABLE_PATH, SOURCE_CATALOGUE,
    PREVIOUS_SOURCE,
)


class PublishedStrain2023Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = read(TABLE_PATH)
        cls.catalogue = read(SOURCE_CATALOGUE)
        cls.previous = read(PREVIOUS_SOURCE)

    def altered(self, mutate):
        fixture = copy.deepcopy(self.table)
        mutate(fixture)
        with self.assertRaises(PublishedEvidenceError):
            check(fixture, self.catalogue, self.previous)

    def test_table_transcription_and_units_remain_explicitly_unqualified(self):
        result = check(self.table, self.catalogue, self.previous)
        self.assertEqual(result["status"], "PUBLISHED_TABLE_ONLY_ORIGINAL_SENSOR_DATA_UNQUALIFIED")
        self.assertEqual(result["published_table_date"], "2022-11-22")
        self.assertEqual(result["published_table_evidence_count"], 8)
        self.assertIsNone(result["table_units"])
        self.assertEqual(result["strongest_reported_gauge_positions"], [3, 7])
        self.assertEqual(result["original_qualified_source_utc_intervals"], 0)
        self.assertFalse(result["grid_net_electricity_validated"])
        self.assertTrue(result["not_a_build_or_test_authorization"])

    def test_paper_reported_max_and_mean_are_distinct(self):
        self.assertEqual(self.table["table"]["values"][2]["mean"], 86.8)
        self.assertEqual(self.table["table"]["values"][2]["max"], 120.8)
        self.assertEqual(self.table["table"]["values"][6]["mean"], 69.7)
        self.assertEqual(self.table["table"]["values"][6]["std"], 8.0)
        self.assertNotEqual(self.table["table"]["values"][2]["mean"],
                            self.table["table"]["values"][2]["max"])

    def test_source_rpm_to_blade_pass_is_only_dimensional_arithmetic(self):
        result = check(self.table, self.catalogue, self.previous)
        self.assertEqual(result["idealized_blade_pass_frequency_range_hz_from_reported_rpm"],
                         [1.2, 2.066667])
        self.assertEqual(result["power_averaging_seconds"], 1)
        self.assertIsNone(self.table["derivations"]["inferred_measured_fatigue_cycles"])

    def test_cannot_assign_microstrain_or_original_source_bytes(self):
        self.altered(lambda x: x["table"].__setitem__("units", "microstrain"))
        self.altered(lambda x: x["source"].__setitem__("visual_pdf_screenshot_confirmed", True))
        self.altered(lambda x: x["source"].__setitem__("original_sensor_archives_acquired", True))
        self.altered(lambda x: x["table"].__setitem__("raw_trace_available", True))
        self.altered(lambda x: x["table"].__setitem__("stress_transfer_calibrated", True))
        self.altered(lambda x: x["table"].__setitem__("observed_cycles_count", 1000))

    def test_reported_2022_nov22_not_renamed_2025_late_nov_case(self):
        self.altered(lambda x: x["table"].__setitem__("source_date", "2022-11-24"))
        self.altered(lambda x: x["published_campaign_context"].__setitem__(
            "late_november_2025_analysed_ebb_same_as_Nov22_not_proven", False))

    def test_source_data_cannot_invent_grid_export_or_phase_power(self):
        self.altered(lambda x: x["experiment_system"].__setitem__(
            "instrumented_blade_operation", "GRID_CONNECTED"))
        self.altered(lambda x: x["experiment_system"].__setitem__(
            "grid_energy_delivery_in_described_test", "VALIDATED_NET_EXPORT"))
        self.altered(lambda x: x["experiment_system"].__setitem__(
            "phase_resolved_electric_power_validated", True))
        self.altered(lambda x: x["experiment_system"].__setitem__(
            "ADCP_and_CTD_linked_to_main_DAQ_during_paper", "YES"))
        self.altered(lambda x: x["experiment_system"].__setitem__(
            "ADV_probes_near_rotor_induced_velocity", False))

    def test_wrong_table_values_are_rejected(self):
        self.altered(lambda x: x["table"]["values"][2].__setitem__("mean", 120.8))
        self.altered(lambda x: x["table"]["values"][6].__setitem__("min", 1.5))
        self.altered(lambda x: x["table"]["values"][1].__setitem__("gauge", 3))
        self.altered(lambda x: x["table"]["values"].pop())
        self.altered(lambda x: x["table"]["values"][2].__setitem__("std", float("nan")))
        self.altered(lambda x: x["table"].__setitem__("source_highest_mean_gauges", [3]))

    def test_reported_campaign_numbers_cannot_be_forged_into_matched_trials(self):
        self.altered(lambda x: x["published_campaign_context"].__setitem__("rpm_min", 25))
        self.altered(lambda x: x["published_campaign_context"].__setitem__(
            "thrust_and_rpm_are_full_deployment_descriptions_not_paired_Table1_samples", False))
        self.altered(lambda x: x["project_scientific_boundary"].__setitem__(
            "project_blade_stress_measurements", 1))
        self.altered(lambda x: x["project_scientific_boundary"].__setitem__(
            "project_net_electricity_measurements", 1))

    def test_original_source_status_cannot_be_silently_promoted(self):
        original = copy.deepcopy(self.previous)
        original["scientifically_qualified_common_windows"] = 1
        with self.assertRaises(PublishedEvidenceError):
            check(self.table, self.catalogue, original)

    def test_source_citation_cannot_be_missing(self):
        missing = [x for x in self.catalogue
                   if x["id"] != "UNH-2023-OMAE-BLADE-010"]
        with self.assertRaises(PublishedEvidenceError):
            check(self.table, missing, self.previous)


if __name__ == "__main__":
    unittest.main()
