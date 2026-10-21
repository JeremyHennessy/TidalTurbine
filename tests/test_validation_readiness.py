"""Regression checks: no fake site authorizations or hydrodynamic results."""
import unittest
from scripts.check_validation_readiness import check, load


class ReadinessTests(unittest.TestCase):
    def test_fail_closed_checks(self):
        check()

    def test_no_physical_experiment_or_winner(self):
        report = load("research/experiment_protocol_v1.json")
        self.assertEqual(report["physical_experiments_run"], 0)
        self.assertIsNone(report["prototype_winner"])
        self.assertFalse(report["field_deployment_authorized"])
        self.assertTrue(all(x != "PASS" for x in report["independent_gates"].values()))

    def test_qualified_current_remains_zero(self):
        report = load("research/observations/FORCE_INFLOW_V0_MANIFEST_2018.json")
        self.assertEqual(report["model_eligible_rows"], 0)
        self.assertEqual(report["science_approved_cells"], 0)
        self.assertEqual(sum(report["counts"].values()), report["records"])

    def test_rm2_means_match_source(self):
        plan = load("research/experiment_protocol_v1.json")
        study = load("reports/RM2-TRADEOFF-001.json")
        comparator = plan["comparator"]
        self.assertEqual(comparator["baseline_source_run"], study["baseline"]["run"])
        candidate = next(x for x in study["within_lab_mechanical_power_budgets"]
                         if x["minimum_fraction_of_peak_mechanical_cp"] == 0.95)
        self.assertEqual(comparator["candidate_source_run"], candidate["selected_source_run"])
        self.assertAlmostEqual(comparator["published_processed_mean_cd"]["candidate"],
                               candidate["observed_cd"], places=7)


if __name__ == "__main__":
    unittest.main()
