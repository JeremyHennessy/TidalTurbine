"""Independent arithmetic and boundary tests: no implied fatigue or net energy."""
import copy
import math
import unittest
from scripts.check_lab_venue_screen import ScreenError
from scripts.screen_rotor_exposure import screen, make_row


class RotorExposureTests(unittest.TestCase):
    def test_full_hypothetical_grid_remains_unqualified(self):
        data = screen(0.6, 3)
        self.assertEqual(data["classification"], "ENGINEERING_ASSUMPTION")
        self.assertFalse(data["physical_build_or_operation_authorized"])
        self.assertFalse(data["outreach_authorized"])
        self.assertFalse(data["qualified_lab_or_field_data"])
        self.assertIsNone(data["fatigue_life_prediction"])
        self.assertIsNone(data["net_electricity_measurement"])
        self.assertEqual(len(data["results"]), 3)
        for point in data["results"]:
            self.assertEqual(len(point["regimes"]), 2)
            for row in point["regimes"]:
                self.assertIsNone(row["calibrated_blade_root_stress_cycles"])
                self.assertIsNone(row["independent_replicates"])
                self.assertIsNone(row["measurement_sampling_hz"])

    def test_exact_dimensional_identity_without_claiming_data(self):
        data = screen(0.6, 3)
        for point in data["results"]:
            for row in point["regimes"]:
                u, lam = row["nominal_carriage_speed_m_s"], row["nominal_tsr"]
                t = row["ideal_constant_speed_time_s"]
                f = lam * u / (math.pi * 0.6)
                self.assertAlmostEqual(row["hypothetical_rotor_frequency_hz"], f, places=5)
                self.assertAlmostEqual(row["hypothetical_rotor_revolutions_per_tow"], f*t, places=3)
                self.assertAlmostEqual(row["hypothetical_aggregate_blade_passages_per_tow"], 3*f*t, places=3)
                self.assertAlmostEqual(row["hypothetical_rotor_rpm"], f*60, places=3)

    def test_example_is_a_few_dozen_rotor_turns_not_fatigue_life(self):
        data = screen(0.6, 3)
        middle = data["results"][1]
        self.assertEqual(middle["assumed_speed_m_s"], 1)
        self.assertAlmostEqual(middle["ideal_tow_bounds"]["ideal_constant_speed_time_upper_bound_s"], 34.5)
        regimes = {x["role"]:x for x in middle["regimes"]}
        self.assertAlmostEqual(regimes["RM2_RUN_10_CANDIDATE"]["hypothetical_rotor_revolutions_per_tow"], 53.0775, places=2)
        self.assertAlmostEqual(regimes["RM2_RUN_12_BASELINE"]["hypothetical_rotor_revolutions_per_tow"], 56.727, places=1)
        self.assertNotEqual(regimes["RM2_RUN_10_CANDIDATE"]["hypothetical_rotor_revolutions_per_tow"], regimes["RM2_RUN_12_BASELINE"]["hypothetical_rotor_revolutions_per_tow"])

    def test_smaller_diameter_increases_kinematic_turn_count_not_power(self):
        smaller = screen(0.3, 3)
        larger = screen(0.9, 3)
        one = smaller["results"][1]["regimes"][0]["hypothetical_rotor_revolutions_per_tow"]
        two = larger["results"][1]["regimes"][0]["hypothetical_rotor_revolutions_per_tow"]
        self.assertGreater(one, two)
        self.assertEqual(smaller["fatigue_life_prediction"], None)

    def test_extra_reserve_can_only_reduce_exposure(self):
        small = screen(0.6, 3, 5.0)
        base = screen(0.6, 3, 0.0)
        for first, second in zip(small["results"], base["results"]):
            self.assertLess(first["regimes"][0]["hypothetical_rotor_revolutions_per_tow"],
                            second["regimes"][0]["hypothetical_rotor_revolutions_per_tow"])

    def test_margin_can_exhaust_steady_plateau(self):
        # The source model explicitly returns None if the travel is consumed by ramps.
        out = screen(0.6, 3, 34.9)
        self.assertEqual(len(out["results"]), 3)
        self.assertTrue(all(p["status"] == "NO_IDEAL_CONSTANT_SPEED_PLATEAU" for p in out["results"]))
        self.assertTrue(all(p["regimes"] == [] for p in out["results"]))

    def test_blade_count_changes_passage_events_not_rotor_turns(self):
        a, b = screen(0.6, 2), screen(0.6, 5)
        aa,bb = a["results"][1]["regimes"][0], b["results"][1]["regimes"][0]
        self.assertEqual(aa["hypothetical_rotor_revolutions_per_tow"],
                         bb["hypothetical_rotor_revolutions_per_tow"])
        self.assertGreater(bb["hypothetical_aggregate_blade_passages_per_tow"],
                           aa["hypothetical_aggregate_blade_passages_per_tow"])

    def test_nonsensical_dimensions_and_inputs_fail_closed(self):
        for diameter, blades, reserve in [
            (0,3,0), (-1,3,0), (float("nan"),3,0), (float("inf"),3,0),
            (True,3,0), (0.6,0,0), (0.6,True,0), (0.6,3,True),
            (0.6,3,-1), (0.6,3,35), (0.6,3,float("inf"))
        ]:
            with self.subTest(diameter=diameter,blades=blades,reserve=reserve):
                with self.assertRaises(ScreenError):
                    screen(diameter,blades,reserve)

    def test_source_prohibition_enforced_even_if_scenarios_are_numeric(self):
        from scripts.check_lab_venue_screen import load
        venue = copy.deepcopy(load())
        venue["user_hold"]["email_send_authorized"] = True
        with self.assertRaises(ScreenError):
            screen(0.6,3,venue_data=venue)

    def test_original_protocol_cannot_pretend_physical_trial(self):
        from scripts.screen_rotor_exposure import ROOT,PROTOCOL
        import json
        original = json.loads((ROOT/PROTOCOL).read_text(encoding="utf-8"))
        original["physical_experiments_run"] = 1
        with self.assertRaises(ScreenError):
            screen(0.6,3,protocol_data=original)


if __name__ == "__main__":
    unittest.main()
