"""Mutation guards and pure mathematical toy examples, not laboratory data."""
import copy
import unittest

from scripts.check_metrology_protocol import (
    MetrologyGateError, audit_synthetic_energy, check_prereg,
    read, synthetic_fixture,
)


class MetrologyPreregTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = read("research/metrology_prereg_v1.json")
        cls.source = read("research/experiment_protocol_v1.json")
        cls.catalogue = read("research/catalogue.json")

    def test_current_plan_is_explicitly_blocked(self):
        r = check_prereg(self.plan, self.source, self.catalogue)
        self.assertEqual(r["status"], "BLOCKED_DESK_METROLOGY_UNFROZEN")
        self.assertEqual(r["required_channels"], 12)
        self.assertEqual(r["uncalibrated_or_undocumented_channels"], 11)
        self.assertEqual(r["unresolved_physical_acceptance_gates"], 9)
        self.assertFalse(r["external_contact_authorized"])
        self.assertFalse(r["lab_fatigue_and_net_power_validated"])
        self.assertIsNone(r["selected_sampling_rate_hz"])

    def reject_plan(self, edit):
        plan = copy.deepcopy(self.plan)
        edit(plan)
        with self.assertRaises(MetrologyGateError):
            check_prereg(plan, self.source, self.catalogue)

    def test_contact_and_result_claims_fail(self):
        self.reject_plan(lambda p: p["contact_and_physical_boundaries"].__setitem__(
            "contact_anyone_authorized", True))
        self.reject_plan(lambda p: p["contact_and_physical_boundaries"].__setitem__(
            "draft_preparation_authorized", True))
        self.reject_plan(lambda p: p["measured_results"].__setitem__(
            "project_net_electricity_measured", True))
        self.reject_plan(lambda p: p["measured_results"].__setitem__(
            "validated_fatigue_life_claim", True))
        self.reject_plan(lambda p: p["independent_acceptance_gates"][0].__setitem__(
            "state", "PASS"))

    def test_channels_frozen_to_original_units_and_uncalibrated(self):
        self.reject_plan(lambda p: p["channels"].pop())
        self.reject_plan(lambda p: p["channels"][0].__setitem__(
            "calibration_record", "faked-cert.pdf"))
        self.reject_plan(lambda p: p["channels"][1].__setitem__("units", "Nm"))
        self.reject_plan(lambda p: p["channels"][2].__setitem__(
            "raw_signal_sha256", "0" * 64))

    def test_no_numeric_sampling_or_statistical_threshold_guessed(self):
        self.reject_plan(lambda p: p["clock_and_signal_design"].__setitem__(
            "selected_sampling_rate_hz", 2000))
        self.reject_plan(lambda p: p["clock_and_signal_design"].__setitem__(
            "per_channel_latency_and_jitter_budget_s", 0.001))
        self.reject_plan(lambda p: p["paired_trial_design"].__setitem__(
            "sample_size_and_power_justification", "two replicates are enough"))
        self.reject_plan(lambda p: p["paired_trial_design"].__setitem__(
            "acceptable_energy_penalty", 0.02))
        self.reject_plan(lambda p: p["electrical_boundary"].__setitem__(
            "auxiliary_meter_inside_delivered_meter_boundary", False))

    def test_signed_energy_math_is_toy_only(self):
        x = audit_synthetic_energy(synthetic_fixture())
        self.assertEqual(x["synthetic_mechanical_work_j"], 12)
        self.assertEqual(x["synthetic_delivered_meter_energy_j"], 8)
        self.assertEqual(x["synthetic_auxiliary_energy_j"], 2)
        self.assertEqual(x["synthetic_net_energy_j"], 6)
        self.assertIsNone(x["calibrated_blade_stress_pa"])
        self.assertIsNone(x["fatigue_damage"])
        self.assertFalse(x["source_measured_power_or_load"])

    def test_double_count_protection(self):
        x = audit_synthetic_energy(synthetic_fixture(
            "ALREADY_INCLUDED_IN_LOAD_METER"))
        self.assertEqual(x["synthetic_net_energy_j"], 8)
        self.assertEqual(x["synthetic_auxiliary_energy_j"], 2)
        self.assertNotEqual(x["synthetic_net_energy_j"], 6)

    def test_negative_export_and_signed_auxiliary_recovery_not_clamped(self):
        toy = synthetic_fixture()
        toy["channels"]["delivered_electrical_power"]["values"] = [-2.0] * 3
        self.assertEqual(audit_synthetic_energy(toy)["synthetic_net_energy_j"], -6)
        toy["channels"]["control_and_actuator_power"]["values"] = [-1.0] * 3
        self.assertEqual(audit_synthetic_energy(toy)["synthetic_net_energy_j"], -2)

    def test_irregular_time_intervals_integrated_by_actual_dt(self):
        toy = synthetic_fixture()
        for ch in toy["channels"].values():
            ch["t_s"] = [0, 1, 3]
        out = audit_synthetic_energy(toy)
        self.assertEqual(out["synthetic_mechanical_work_j"], 18)
        self.assertEqual(out["synthetic_net_energy_j"], 9)

    def reject_toy(self, edit):
        toy = synthetic_fixture()
        edit(toy)
        with self.assertRaises(MetrologyGateError):
            audit_synthetic_energy(toy)

    def test_missing_channel_or_unresolved_boundary_rejected(self):
        self.reject_toy(lambda x: x["channels"].pop("blade_root_strain"))
        self.reject_toy(lambda x: x.__setitem__(
            "auxiliary_meter_boundary", None))
        self.reject_toy(lambda x: x.__setitem__(
            "auxiliary_meter_boundary", "MAYBE"))

    def test_bad_units_nonfinite_and_unsynchronized_clocks_rejected(self):
        self.reject_toy(lambda x: x["channels"]["shaft_torque"].__setitem__(
            "unit", "W"))
        self.reject_toy(lambda x: x["channels"]["shaft_torque"]["values"].__setitem__(
            0, float("nan")))
        self.reject_toy(lambda x: x["channels"]["rotor_position"].__setitem__(
            "t_s", [0, 1, 1]))
        self.reject_toy(lambda x: x["channels"]["rotor_speed"].__setitem__(
            "t_s", [0, 1.1, 2]))
        self.reject_toy(lambda x: x["channels"]["shaft_torque"].__setitem__(
            "clock_id", "OTHER"))
        self.reject_toy(lambda x: x["channels"]["blade_root_strain"].__setitem__(
            "values", [0, 1]))

    def test_toy_cannot_claim_physical_data_or_stress_calibration(self):
        self.reject_toy(lambda x: x.__setitem__("physical_run_id", "real-run"))
        self.reject_toy(lambda x: x.__setitem__(
            "material_calibration", {"youngs_modulus_pa": 2e11}))
        self.reject_toy(lambda x: x.__setitem__(
            "classification", "EXPERIMENTALLY_VALIDATED_FINDING"))


if __name__ == "__main__":
    unittest.main()
