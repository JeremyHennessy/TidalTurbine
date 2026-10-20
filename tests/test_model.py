import math
import unittest

from tidal_screen.model import SyntheticCurrent, Turbine, electrical_power_kw, integrate
from tidal_screen.cli import run


class PowerModelTests(unittest.TestCase):
    def setUp(self):
        self.t = Turbine()

    def test_zero_slack_and_cut_in(self):
        self.assertEqual(electrical_power_kw(self.t, 0), 0)
        self.assertEqual(electrical_power_kw(self.t, 0.69), 0)
        self.assertGreater(electrical_power_kw(self.t, 0.7), 0)

    def test_signed_inflow_symmetric(self):
        self.assertEqual(electrical_power_kw(self.t, 1.2), electrical_power_kw(self.t, -1.2))

    def test_cube_in_unrated_regime(self):
        slow = electrical_power_kw(self.t, 0.8)
        fast = electrical_power_kw(self.t, 1.6)
        self.assertAlmostEqual(fast / slow, 8, places=10)

    def test_exact_analytical_power(self):
        u = 1.0
        expected = min(0.5 * 1025 * math.pi * 25 * .4 * .9 * u ** 3 / 1000, 750)
        self.assertAlmostEqual(electrical_power_kw(self.t, u), expected)

    def test_rated_cap(self):
        self.assertEqual(electrical_power_kw(self.t, 20), self.t.rated_power_kw)

    def test_constant_zero_current_zero_energy(self):
        c = SyntheticCurrent(primary_amplitude_m_s=0, secondary_amplitude_m_s=0)
        self.assertEqual(integrate(self.t, c, 3, 3600)["energy_kwh"], 0)

    def test_constant_flow_integrates_analytically(self):
        class ConstantFlow:
            @staticmethod
            def velocity_m_s(_time_s):
                return 1.3
        duration_hours = 37.0
        for dt in (30, 300, 7000):
            observed = integrate(self.t, ConstantFlow(), duration_hours / 24, dt)
            predicted = electrical_power_kw(self.t, 1.3) * duration_hours
            self.assertAlmostEqual(observed["energy_kwh"], predicted, places=6)

    def test_cap_does_not_improve_export(self):
        c = SyntheticCurrent()
        base = integrate(self.t, c, 1, 300)
        limited = integrate(self.t, c, 1, 300, 0.8)
        self.assertLessEqual(limited["energy_kwh"], base["energy_kwh"])
        # At sufficiently high inflow a low cap must bind.
        strict_cap = integrate(self.t, c, 1, 300, 0.05)
        self.assertLess(strict_cap["energy_kwh"], base["energy_kwh"])
        self.assertAlmostEqual(limited["export_curtailment_kwh"], base["energy_kwh"] - limited["energy_kwh"])

    def test_unit_cap_has_zero_curtailment(self):
        r = integrate(self.t, SyntheticCurrent(), 1, 300, 1)
        self.assertEqual(r["export_curtailment_kwh"], 0)

    def test_dt_partial_last_interval(self):
        c = SyntheticCurrent()
        r = integrate(self.t, c, 1, 700)
        self.assertEqual(r["samples"], math.ceil(86400 / 700))
        self.assertEqual(r["duration_days"], 1)

    def test_time_step_convergence(self):
        c = SyntheticCurrent()
        e300 = integrate(self.t, c, 2, 300)["energy_kwh"]
        e150 = integrate(self.t, c, 2, 150)["energy_kwh"]
        e75 = integrate(self.t, c, 2, 75)["energy_kwh"]
        self.assertLess(abs(e150 - e75) / e75, .001)
        self.assertLess(abs(e300 - e150) / e150, .003)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            Turbine(power_coefficient=.7)
        with self.assertRaises(ValueError):
            Turbine(rated_power_kw=0)
        with self.assertRaises(ValueError):
            Turbine(conversion_efficiency=float('nan'))
        with self.assertRaises(ValueError):
            electrical_power_kw(self.t, float('nan'))
        with self.assertRaises(ValueError):
            SyntheticCurrent(primary_period_hours=0)
        with self.assertRaises(ValueError):
            integrate(self.t, SyntheticCurrent(), -1, 300)
        with self.assertRaises(ValueError):
            integrate(self.t, SyntheticCurrent(), 1, 300, 1.1)

    def test_screen_rejects_unlabelled_site_data(self):
        with self.assertRaises(ValueError):
            run({"inflow_kind": "measured_Fundy_site"})


if __name__ == '__main__':
    unittest.main()
