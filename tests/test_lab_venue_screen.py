"""Offline kinematic guardrails and mutation tests, without contacts or equipment."""
import copy
import unittest
from scripts.check_lab_venue_screen import ScreenError, check, load, tow_time_upper_bound


class LabVenueScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.screen = load()

    def test_source_backed_report_is_still_blocked(self):
        result = check(self.screen)
        self.assertEqual(result["status"], "DESK_ONLY_NOT_READY_FOR_TEST")
        self.assertFalse(result["emails_or_contacts_permitted"])
        self.assertFalse(result["prototype_measured"])
        self.assertEqual(result["project_quotes_verified"], 0)
        self.assertEqual(result["qualified_site_inflow_rows"], 0)

    def test_published_tow_upper_bounds_but_not_guarantees(self):
        result = check(self.screen)
        speeds = result["optimistic_tow_windows"]
        self.assertEqual(len(speeds), 3)
        for row, speed in zip(speeds, [0.6, 1.0, 1.4]):
            self.assertEqual(row["target_speed_m_s"], speed)
            self.assertFalse(row["physically_qualified"])
        self.assertAlmostEqual(speeds[0]["ideal_constant_speed_time_upper_bound_s"], 58.0333, places=3)
        self.assertAlmostEqual(speeds[1]["ideal_constant_speed_time_upper_bound_s"], 34.5, places=3)
        self.assertAlmostEqual(speeds[2]["ideal_constant_speed_time_upper_bound_s"], 24.3, places=3)

    def test_time_decreases_if_protective_margin_added(self):
        baseline = tow_time_upper_bound(1.0, 35.0, 2.0, 2.0)
        shorter = tow_time_upper_bound(1.0, 35.0, 2.0, 2.0, 5.0)
        self.assertLess(shorter["ideal_constant_speed_time_upper_bound_s"],
                        baseline["ideal_constant_speed_time_upper_bound_s"])

    def test_unreachable_target_is_not_accepted(self):
        self.assertIsNone(tow_time_upper_bound(1.4, 0.5, 2.0, 2.0))
        for args in [(0, 35, 2, 2), (-1, 35, 2, 2), (1, 0, 2, 2),
                     (1, 35, 0, 2), (1, 35, 2, 0), (1, 35, 2, 2, 35),
                     (float("nan"), 35, 2, 2), (True, 35, 2, 2)]:
            with self.subTest(args=args), self.assertRaises(ScreenError):
                tow_time_upper_bound(*args)

    def reject(self, mutation):
        data = copy.deepcopy(self.screen)
        mutation(data)
        with self.assertRaises(ScreenError):
            check(data)

    def test_outreach_and_approval_cannot_be_silently_promoted(self):
        self.reject(lambda d: d["user_hold"].__setitem__("email_send_authorized", True))
        self.reject(lambda d: d["user_hold"].__setitem__("external_contacts", "APPROVED"))
        self.reject(lambda d: d["user_hold"].__setitem__("physical_test_authorized", True))
        self.reject(lambda d: d["experimental_claims"].__setitem__("new_physical_tests", 1))
        self.reject(lambda d: d["experimental_claims"].__setitem__("prototype_winner", "MUN-TOW"))

    def test_current_facility_and_quoted_costs_remain_unknown(self):
        self.reject(lambda d: d["venues"][0].__setitem__("current_test_acceptance", "APPROVED"))
        self.reject(lambda d: d["venues"][1].__setitem__("controlled_tow_time_verified", True))
        self.reject(lambda d: d["venues"][1].__setitem__("published_rate_currency", "CAD"))
        self.reject(lambda d: d["venues"][2].__setitem__("published_rate_amount", 1000))

    def test_must_not_loosen_idealized_tow_bounds(self):
        self.reject(lambda d: d["optimistic_tow_screen"].__setitem__("guaranteed_steady_speed_time_s", 24.3))
        self.reject(lambda d: d["optimistic_tow_screen"].__setitem__("assumed_extra_safety_margin_m", -1))
        self.reject(lambda d: d["optimistic_tow_screen"].__setitem__("modeled_speed_setpoints_m_s", [0.6, 1.0, 5.5]))
        self.reject(lambda d: d["optimistic_tow_screen"].__setitem__("usable_time_is_optimistic_bound", False))


if __name__ == "__main__":
    unittest.main()
