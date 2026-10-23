"""Actual LOCAL CSV timing checks using synthetic source fixtures only.

No 2022 original source was acquired, downloaded or scientifically validated.
Even complete toy manifests cannot produce APPROVED source data or fatigue/power.
"""
import copy
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.qualify_unh_2022_overlap import (
    SourceEligibilityError, blocked_status, candidate_intersections,
    source_registry, MAX_CSV_BYTES
)

GOOD = "SOURCE_QC_ACCEPT"
BAD = "SOURCE_QC_REJECT"
DUMMY = "a" * 64


class UNH2022OverlapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.catalogue = source_registry()
        self.originals = {s["id"]: s["source_archive_url"]
                          for s in self.catalogue["streams"]}
        self.manifest = {
            "schema": "TT-UNH-2022-LOCAL-CLIPS-V1",
            "dataset_id": "DOE-UNH-STRAIN-CATALOG-008",
            "classification": "USER_SUPPLIED_SOURCE_SLICES_NOT_SCIENTIFICALLY_VALIDATED",
            "screen_minimum_seconds": 3.0,
            "streams": []
        }
        self.set_rows("STRAIN", list(range(0, 11)))
        self.set_rows("FLOW_ADCP", list(range(1, 11)))
        self.set_rows("THRUST", list(range(2, 11)))
        self.set_rows("VOLTSYS", list(range(3, 10)))

    def set_rows(self, role, seconds, quality=None, times=None, values=None):
        cols = (["u", "v", "w"] if role.startswith("FLOW_") else ["reading"])
        stamp = lambda s: "2022-11-10T00:00:{:02d}Z".format(s)
        target = self.base / (role + ".csv")
        with target.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time_utc", "native_qc", *cols])
            for i, second in enumerate(seconds):
                flag = quality.get(second, GOOD) if quality else GOOD
                when = times[i] if times else stamp(second)
                row_values = (values[i] if values else [1.0] * len(cols))
                writer.writerow([when, flag, *row_values])
        blob = target.read_bytes()
        entry = {
            "role": role,
            "source_archive_url": self.originals[role],
            "csv_relative_path": target.name,
            "csv_sha256": hashlib.sha256(blob).hexdigest(),
            "original_archive_sha256": DUMMY,
            "source_readme_sha256": DUMMY,
            "calibration_evidence_sha256": DUMMY,
            "quality_evidence_sha256": DUMMY,
            "clock_evidence_sha256": DUMMY,
            "processing_manifest_sha256": DUMMY,
            "timestamp_column": "time_utc",
            "quality_column": "native_qc",
            "good_quality_token": GOOD,
            "bad_quality_token": BAD,
            "value_columns": cols,
            "declared_si_unit": {
                "STRAIN": "microstrain", "FLOW_ADCP": "m/s",
                "FLOW_ADV": "m/s", "THRUST": "N", "VOLTSYS": "W"
            }[role],
            "clock_uncertainty_seconds": 0.1,
            "max_contiguous_gap_seconds": 1.01,
        }
        if role.startswith("FLOW_"):
            entry["flow_geometry_evidence_sha256"] = DUMMY
        if role == "VOLTSYS":
            entry["meter_boundary_evidence_sha256"] = DUMMY
        existing = [s for s in self.manifest["streams"] if s["role"] != role]
        existing.append(entry)
        self.manifest["streams"] = existing

    def run_candidate(self):
        return candidate_intersections(self.manifest, self.base)

    def target(self, role):
        return next(x for x in self.manifest["streams"] if x["role"] == role)

    def test_registry_stays_genuinely_blocked(self):
        r = blocked_status()
        self.assertEqual(r["status"], "BLOCKED_NO_ORIGINAL_2022_SENSOR_FILES_OR_CLOCK_QC")
        self.assertEqual(r["original_archives_acquired"], 0)
        self.assertEqual(r["candidate_timestamp_windows"], [])
        self.assertEqual(r["scientifically_qualified_windows"], 0)
        self.assertFalse(r["source_native_calibration_qc_clocks_known"])
        self.assertFalse(r["contact_authorized"])
        self.assertEqual(self.catalogue["publisher_doi"], "10.15473/2481243")
        self.assertEqual(self.catalogue["catalog_resource_count"], 17)
        self.assertFalse(self.catalogue["campaign_window_is_instrument_overlap"])
        self.assertEqual(len(self.catalogue["streams"]), 6)

    def test_synthetic_four_stream_overlap_is_only_candidate(self):
        r = self.run_candidate()
        self.assertEqual(r["status"], "LOCAL_TIMESTAMP_OVERLAP_CANDIDATES_REVIEW_REQUIRED")
        self.assertEqual(len(r["candidate_timestamp_windows"]), 1)
        x = r["candidate_timestamp_windows"][0]
        self.assertEqual(x["candidate_start_utc"], "2022-11-10T00:00:03.100000Z")
        self.assertEqual(x["candidate_end_utc"], "2022-11-10T00:00:08.900000Z")
        self.assertAlmostEqual(x["time_label_overlap_seconds"], 5.8)
        self.assertEqual(r["scientifically_qualified_windows"], 0)
        for key in (
            "calibration_and_clock_evidence_reviewed_by_program",
            "flow_geometry_and_representativeness_verified",
            "platform_inertial_load_compensation_verified",
            "signed_net_system_electricity_verified",
            "physical_fatigue_or_power_validation", "external_contact_authorized"
        ):
            self.assertFalse(r[key], key)

    def test_rejected_rows_split_source_coverage_no_interpolation(self):
        self.set_rows("VOLTSYS", list(range(3, 10)), quality={5: BAD})
        self.manifest["screen_minimum_seconds"] = 2.0
        r = self.run_candidate()
        self.assertEqual(len(r["candidate_timestamp_windows"]), 1)
        self.assertEqual(r["candidate_timestamp_windows"][0]["candidate_start_utc"],
                         "2022-11-10T00:00:06.100000Z")
        self.assertEqual(r["stream_counts"][-1]["rejected"], 1)

    def test_missing_sample_breaks_long_contiguous_window(self):
        self.set_rows("VOLTSYS", [3, 4, 6, 7, 8, 9])
        self.manifest["screen_minimum_seconds"] = 2.0
        r = self.run_candidate()
        self.assertEqual(len(r["candidate_timestamp_windows"]), 1)
        self.assertEqual(r["candidate_timestamp_windows"][0]["candidate_start_utc"],
                         "2022-11-10T00:00:06.100000Z")

    def test_separate_slices_no_fake_overlap(self):
        self.set_rows("VOLTSYS", list(range(40, 49)))
        r = self.run_candidate()
        self.assertEqual(r["status"], "NO_TIMESTAMP_OVERLAP_IN_SUPPLIED_BOUNDED_SLICES")
        self.assertEqual(r["candidate_timestamp_windows"], [])
        self.assertEqual(r["scientifically_qualified_windows"], 0)

    def test_can_select_an_adv_flow_slice_instead_of_adcp(self):
        self.manifest["streams"] = [
            x for x in self.manifest["streams"] if x["role"] != "FLOW_ADCP"
        ]
        self.set_rows("FLOW_ADV", list(range(1, 11)))
        self.assertEqual(len(self.run_candidate()["candidate_timestamp_windows"]), 1)
        self.set_rows("FLOW_ADCP", list(range(1, 11)))
        with self.assertRaisesRegex(SourceEligibilityError, "Exactly four"):
            self.run_candidate()

    def test_wrong_2021_archive_is_rejected(self):
        self.target("VOLTSYS")["source_archive_url"] = (
            "https://mhkdr.openei.org/files/394/Voltsys.zip")
        with self.assertRaisesRegex(SourceEligibilityError, "Archive identity"):
            self.run_candidate()

    def test_missing_docs_and_meter_boundary_rejected(self):
        self.target("STRAIN")["clock_evidence_sha256"] = None
        with self.assertRaisesRegex(SourceEligibilityError, "pinned SHA"):
            self.run_candidate()
        self.target("STRAIN")["clock_evidence_sha256"] = DUMMY
        self.target("VOLTSYS")["meter_boundary_evidence_sha256"] = None
        with self.assertRaisesRegex(SourceEligibilityError, "meter_boundary"):
            self.run_candidate()
        self.target("VOLTSYS")["meter_boundary_evidence_sha256"] = DUMMY
        self.target("FLOW_ADCP")["flow_geometry_evidence_sha256"] = None
        with self.assertRaisesRegex(SourceEligibilityError, "flow_geometry"):
            self.run_candidate()

    def test_wrong_si_unit_and_undefined_quality_rejected(self):
        self.target("VOLTSYS")["declared_si_unit"] = "kW"
        with self.assertRaisesRegex(SourceEligibilityError, "SI unit mismatch"):
            self.run_candidate()
        self.target("VOLTSYS")["declared_si_unit"] = "W"
        self.set_rows("STRAIN", list(range(0, 11)), quality={4: "UNKNOWN"})
        with self.assertRaisesRegex(SourceEligibilityError, "Undeclared"):
            self.run_candidate()

    def test_file_sha_mismatch_and_unsafe_relative_path(self):
        self.target("THRUST")["csv_sha256"] = "b" * 64
        with self.assertRaisesRegex(SourceEligibilityError, "Local CSV hash"):
            self.run_candidate()
        self.target("THRUST")["csv_sha256"] = hashlib.sha256(
            (self.base / "THRUST.csv").read_bytes()).hexdigest()
        self.target("THRUST")["csv_relative_path"] = "../private.csv"
        with self.assertRaisesRegex(SourceEligibilityError, "Unsafe"):
            self.run_candidate()

    def test_reject_unspecified_utc_duplicate_and_campaign_mismatch(self):
        self.set_rows("STRAIN", [0, 1], times=[
            "2022-11-10T00:00:00", "2022-11-10T00:00:01"])
        with self.assertRaisesRegex(SourceEligibilityError, "explicit UTC"):
            self.run_candidate()
        self.set_rows("STRAIN", [0, 1], times=[
            "2022-11-10T00:00:00Z", "2022-11-10T00:00:00Z"])
        with self.assertRaisesRegex(SourceEligibilityError, "Duplicate/reordered"):
            self.run_candidate()
        self.set_rows("STRAIN", [0, 1], times=[
            "2021-11-10T00:00:00Z", "2021-11-10T00:00:01Z"])
        with self.assertRaisesRegex(SourceEligibilityError, "outside 2022"):
            self.run_candidate()

    def test_reject_nonfinite_accepted_values(self):
        self.set_rows("STRAIN", [0, 1], values=[[1], ["NaN"]])
        with self.assertRaisesRegex(SourceEligibilityError, "Nonfinite"):
            self.run_candidate()

    def test_missing_required_role_and_forged_physical_claims(self):
        self.manifest["streams"] = self.manifest["streams"][:-1]
        with self.assertRaisesRegex(SourceEligibilityError, "Exactly four"):
            self.run_candidate()
        registry = copy.deepcopy(self.catalogue)
        registry["scientifically_qualified_common_windows"] = 1
        with self.assertRaisesRegex(SourceEligibilityError, "No original measured"):
            blocked_status(registry)

    def test_file_bounds_and_no_automatic_source_download(self):
        self.assertLess(len((self.base / "STRAIN.csv").read_bytes()), MAX_CSV_BYTES)
        self.assertFalse(self.catalogue["automated_original_downloads"])
        self.assertFalse(self.catalogue["source_bypass_authorized"])


if __name__ == "__main__":
    unittest.main()
