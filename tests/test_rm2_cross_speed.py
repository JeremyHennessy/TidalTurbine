"""Regression coverage for published RM2 multi-speed processed mean comparisons."""
import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import rm2_cross_speed as study


class RM2CrossSpeedEvidenceTests(unittest.TestCase):
    def test_ten_source_series_and_fixed_nominal_tsr_pair(self):
        report = study.generate()
        self.assertEqual(report["series_count"], 10)
        self.assertEqual(report["nominal_tow_speeds_m_s"], [0.4, 0.6, 0.8, 1.0, 1.2])
        self.assertEqual(report["descriptive_sign_count"],
                         {"candidate_cp_lower_than_reference": 10,
                          "candidate_cd_lower_than_reference": 10})
        self.assertEqual({s["series_id"] for s in report["series"]},
                         {f"RM2-{str(speed).replace('.', 'p')}-{series}"
                          for speed in ("0.4", "0.6", "0.8", "1.0", "1.2")
                          for series in ("A", "B")})
        for pair in report["series"]:
            self.assertEqual(pair["candidate_tsr_2p9"]["source_run"], 10)
            self.assertEqual(pair["reference_tsr_3p1"]["source_run"], 12)
            self.assertGreater(pair["candidate_relative_to_tsr3p1"]
                               ["mechanical_cp_point_decrease_percent"], 0)
            self.assertGreater(pair["candidate_relative_to_tsr3p1"]
                               ["mean_streamwise_cd_point_decrease_percent"], 0)

    def test_significant_speed_dependence_without_significance_claim(self):
        report = study.generate()
        observations = {item["series_id"]: item for item in report["series"]}
        cp_loss = lambda sid: observations[sid]["candidate_relative_to_tsr3p1"]["mechanical_cp_point_decrease_percent"]
        cd_loss = lambda sid: observations[sid]["candidate_relative_to_tsr3p1"]["mean_streamwise_cd_point_decrease_percent"]
        self.assertAlmostEqual(cp_loss("RM2-0p4-A"), 29.8571, places=4)
        self.assertAlmostEqual(cd_loss("RM2-0p4-A"), 7.7026, places=4)
        self.assertAlmostEqual(cp_loss("RM2-1p0-A"), 1.8477, places=4)
        self.assertAlmostEqual(cd_loss("RM2-1p0-A"), 5.5063, places=4)
        self.assertAlmostEqual(cp_loss("RM2-1p2-B"), 0.1267, places=4)
        self.assertGreater(cp_loss("RM2-0p4-A"), cp_loss("RM2-1p0-A") * 10)
        self.assertIn("NOT recomputed", report["uncertainty_and_limits"][1])
        self.assertIn("None of the observed coefficient differences establishes statistical significance",
                      report["uncertainty_and_limits"][3])

    def test_independent_published_1ms_baseline_unchanged(self):
        latest = study.generate()
        saved = json.loads((study.ROOT / "reports/RM2-TRADEOFF-001.json").read_text(encoding="utf8"))
        s = next(x for x in latest["series"] if x["series_id"] == "RM2-1p0-A")
        baseline = saved["baseline"]
        selection = next(x for x in saved["within_lab_mechanical_power_budgets"]
                         if x["minimum_fraction_of_peak_mechanical_cp"] == 0.95)
        self.assertAlmostEqual(s["reference_tsr_3p1"]["mean_cp"], baseline["cp"], places=6)
        self.assertAlmostEqual(s["candidate_tsr_2p9"]["mean_cd"], selection["observed_cd"], places=6)
        self.assertEqual(s["source_git_blob_sha"], saved["source_git_blob_sha"])

    def test_source_selected_role_is_not_assumed_cp_peak_at_each_speed(self):
        values = {x["series_id"]: x for x in study.generate()["series"]}
        # At 0.4 m/s published peak is at a later TSR; do not call
        # nominal 3.1 a universal Cp-peak setting.
        a = values["RM2-0p4-A"]
        self.assertEqual(a["posthoc_source_series_max_cp"]["source_run"], 15)
        self.assertGreater(a["posthoc_source_series_max_cp"]["mean_cp"],
                           a["reference_tsr_3p1"]["mean_cp"])
        self.assertEqual(values["RM2-1p0-A"]["posthoc_source_series_max_cp"]["source_run"], 12)

    def test_modified_fixture_fails_closed(self):
        original = study.SOURCE_FIXTURE.read_text(encoding="utf8")
        lines = original.splitlines()
        head = lines[0].split(",")
        tsr_col = head.index("tsr_nom")
        candidate = lines[1].split(",")
        self.assertEqual(candidate[head.index("role")], "candidate_tsr_2p9")
        candidate[tsr_col] = "2.95"
        lines[1] = ",".join(candidate)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tampered.csv"
            path.write_text("\n".join(lines) + "\n", encoding="utf8")
            with patch.object(study, "SOURCE_FIXTURE", path):
                with self.assertRaises(ValueError):
                    study.series_rows()

    def test_report_is_exactly_reproducible_from_frozen_fixture(self):
        published = json.loads(study.OUTPUT.read_text(encoding="utf8"))
        self.assertEqual(study.generate(), published)
        self.assertEqual(published["source"]["source_immutable_commit"],
                         "fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef")
        self.assertEqual(published["source"]["reduced_fixture_git_blob_sha"],
                         study.git_blob_sha(study.SOURCE_FIXTURE.read_bytes()))


if __name__ == "__main__":
    unittest.main()
