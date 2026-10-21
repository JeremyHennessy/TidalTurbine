"""Regression: original NI source effects are not fatigue or site-resource validation."""
import json
from pathlib import Path
import unittest
from scripts.check_followon_gates import check,ROOT

class FollowonGates(unittest.TestCase):
    def test_all_fail_closed_scientific_gates(self):
        self.assertTrue(check())
    def test_second_sweep_has_same_sign_of_1ms_shaft_variability(self):
        b=json.loads((ROOT/"reports/RM2-RAW-B-001.json").read_text())
        a=json.loads((ROOT/"reports/RM2-RAW-LOADS-001.json").read_text())
        one=next(x for x in b["within_speed_pairs"] if x["speed_m_s"]==1)
        self.assertGreater(one["shaft_torque_sd_change_percent"],0)
        self.assertLess(one["support_drag_sd_change_percent"],0)
        historical=next(x for x in a["within_speed_pairs"] if x["nominal_speed_m_s"]==1)
        self.assertGreater(historical["shaft_torque_std_change_percent"],0)
        self.assertEqual(a["scientific_gates"]["fatigue_damage"],"NOT_EVALUABLE")
    def test_profile_flags_include_fail_and_suspect_not_just_pass(self):
        r=json.loads((ROOT/"reports/NS-PASSAGES-7D-SUMMARY-001.json").read_text())
        self.assertEqual(len(r["sites"]),2)
        self.assertEqual(r["source_rows_total"],21872)
        for s in r["sites"]:
            self.assertGreater(s["source_flag_speed_counts"]["Fail"],0)
            self.assertGreater(s["source_flag_speed_counts"]["Suspect/Of Interest"],0)
            self.assertTrue(s["source_datetime_offset_unverified"])
            self.assertEqual(s["model_eligible_rows"],0)
        self.assertNotEqual(r["sites"][0]["deployment_year"],r["sites"][1]["deployment_year"])
    def test_no_binary_source_committed(self):
        self.assertFalse((ROOT/"data/local/rm2-sweep-b-grand-petit-originals.zip").exists())
        self.assertFalse((ROOT/"data/local/DG012_7d_profiles.json").exists())

if __name__=="__main__":
    unittest.main()
