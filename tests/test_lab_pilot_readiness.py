"""Mutation and source-parity checks for unapproved lab pilot metadata."""
import copy
import unittest
from scripts.check_lab_pilot_readiness import (
    ROOT, PLAN_PATH, ReadinessError, check, load, source_records, validate
)


class LabPilotReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = load(PLAN_PATH)
        cls.sources = source_records()

    def changed(self, patch):
        candidate = copy.deepcopy(self.plan)
        patch(candidate)
        with self.assertRaises(ReadinessError):
            validate(candidate, self.sources, ROOT)

    def test_current_evidence_remains_blocked_and_source_mapped(self):
        result = check()
        self.assertEqual(result["unresolved_gate_count"], 15)
        self.assertEqual(result["source_qualified_site_inflow_rows"], 0)
        self.assertEqual(result["recorded_lab_tests"], 0)
        self.assertTrue(result["not_a_certification_or_permission"])

    def test_public_rate_is_partial_and_arithmetic_is_consistent(self):
        result = validate(self.plan, self.sources)
        self.assertEqual(result["published_flume_list_rate_only_cad"],
                         {"1": 5000, "2": 10000, "3": 15000})
        self.assertTrue(result["not_a_complete_project_budget"])

    def test_cannot_claim_approved_build_or_contact(self):
        self.changed(lambda x: x["permissions"].__setitem__("physical_lab_operation_authorized", True))
        self.changed(lambda x: x["permissions"].__setitem__("purchasing_authorized", True))
        self.changed(lambda x: x["permissions"].__setitem__("external_contact_authorized", True))
        self.changed(lambda x: x["physics_status"].__setitem__("physical_lab_trials_documented", 1))

    def test_cannot_claim_real_inflow_or_fatigue(self):
        self.changed(lambda x: x["physics_status"].__setitem__("qualified_site_inflow_rows", 1))
        self.changed(lambda x: x["physics_status"].__setitem__("measured_blade_fatigue_benefit", True))
        self.changed(lambda x: x["physics_status"].__setitem__("prototype_winner", "CROSSFLOW-RM2-REFERENCE"))

    def test_source_mutations_also_fail(self):
        sources = copy.deepcopy(self.sources)
        sources["force"]["model_eligible_rows"] = 1
        with self.assertRaises(ReadinessError):
            validate(self.plan, sources)
        sources = copy.deepcopy(self.sources)
        sources["protocol"]["physical_experiments_run"] = 1
        with self.assertRaises(ReadinessError):
            validate(self.plan, sources)

    def test_cannot_promote_a_gate_without_actual_validation(self):
        self.changed(lambda x: x["gates"][0].__setitem__("status", "PASS"))
        self.changed(lambda x: x["gates"][0].__setitem__("evidence", "assumed"))
        self.changed(lambda x: x["gates"].pop())
        self.changed(lambda x: x["gates"].append(copy.deepcopy(x["gates"][0])))

    def test_cannot_claim_venue_booking_or_authorized_machinery(self):
        self.changed(lambda x: x["venues"][0].__setitem__("operator_acceptance_confirmed", True))
        self.changed(lambda x: x["budget"].__setitem__("venue_booking_confirmed", True))

    def test_cannot_fake_comprehensive_cost(self):
        self.changed(lambda x: x["budget"].__setitem__("all_in_project_cost_cad", 10000))
        self.changed(lambda x: x["budget"].__setitem__("approved_spending_cad", 15000))
        self.changed(lambda x: x["budget"].__setitem__("published_daily_rate_cad", 4000))
        self.changed(lambda x: x["budget"].__setitem__("illustrative_day_counts", [1, 2, 4]))

    def test_registered_inference_thresholds_are_missing_not_guessed(self):
        self.changed(lambda x: x["pilot_comparator"].__setitem__(
            "prespecified_load_benefit_threshold", 0.05))
        self.changed(lambda x: x["pilot_comparator"].__setitem__(
            "registered_sample_size", 2))
        self.changed(lambda x: x["pilot_comparator"].__setitem__(
            "experimental_result_status", "VALIDATED"))

    def test_regulatory_and_lab_permission_remain_distinct(self):
        self.changed(lambda x: x["regulatory_watch"].__setitem__("permit_obtained", True))
        self.changed(lambda x: x["regulatory_watch"].__setitem__("project_eligibility_verified", True))


if __name__ == "__main__":
    unittest.main()
