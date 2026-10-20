"""Invariants protecting data classification and non-generic converter modelling."""
import json
import unittest
from pathlib import Path
from scripts.reproduce_rm2 import reproduce, INPUT
from tidal_screen.foil_balance import FoilSample, instant_balance, integrate
ROOT=Path(__file__).resolve().parents[1]
class TaxonomyTests(unittest.TestCase):
    def test_mechanism_records_are_unique_and_provenanced(self):
        rows=json.loads((ROOT/'research/mechanisms.json').read_text())
        self.assertEqual(len(rows),14)
        self.assertEqual(len({r['id'] for r in rows}),len(rows))
        self.assertTrue(all(r['source_url'].startswith('https://') for r in rows))
        self.assertTrue(all(r['scope']=='tidal_stream' and r['power_boundary_and_denominator'] for r in rows))
    def test_no_false_predictive_validated_status(self):
        rows=json.loads((ROOT/'research/mechanisms.json').read_text())
        self.assertTrue(all('validated_prediction' not in r['model_status'] for r in rows))
    def test_alternatives_not_all_cubic_cp(self):
        text=(ROOT/'tidal_screen/foil_balance.py').read_text()
        self.assertNotIn('power_coefficient',text)
class RM2Tests(unittest.TestCase):
    def test_observation_count_and_peak(self):
        result=reproduce()
        self.assertEqual(result['n_observations'],23)
        p=result['peak_observed']
        self.assertAlmostEqual(p['mean_tsr'],3.0993495,places=6)
        self.assertAlmostEqual(p['mean_cp'],0.3546025,places=6)
    def test_data_reproduction_not_physical_validation(self):
        r=reproduce()
        self.assertIn('NOT_PREDICTIVE_VALIDATION',r['classification'])
        self.assertIn('not independently',r['provenance'].lower())
        self.assertEqual(len({o['run'] for o in r['data']}),23)
    def test_fixture_tampering_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/'missing.csv'
            path.write_text(INPUT.read_text().splitlines()[0]+'\n')
            with self.assertRaises(ValueError):reproduce(path)
class FoilTests(unittest.TestCase):
    @staticmethod
    def sample(time, f=100, velocity=2, moment=40, rate=1, actuator=20, losses=30):
        return FoilSample(time,f,velocity,moment,rate,actuator,losses)
    def test_dimensional_sign_and_balance(self):
        r=instant_balance(self.sample(0))
        self.assertEqual(r['gross_mechanical_w'],240)
        self.assertEqual(r['net_delivered_w'],190)
    def test_parasitic_consumption_can_exceed_capture(self):
        r=instant_balance(self.sample(0,f=0,moment=0))
        self.assertEqual(r['net_delivered_w'],-50)
    def test_time_integration_trapezoid(self):
        data=[self.sample(0),self.sample(1),self.sample(3)]
        r=integrate(data)
        self.assertEqual(r['net_delivered_j'],570)
        self.assertAlmostEqual(r['gross_mechanical_j']-r['actuation_j']-r['conversion_loss_j'],r['net_delivered_j'])
    def test_reject_repeated_timestamps(self):
        with self.assertRaises(ValueError):integrate([self.sample(0),self.sample(0)])
    def test_reject_negative_actuation_loss(self):
        with self.assertRaises(ValueError):instant_balance(self.sample(0,actuator=-1))
    def test_reject_nonfinite_values(self):
        with self.assertRaises(ValueError):instant_balance(self.sample(0,f=float('nan')))
if __name__=='__main__':unittest.main()
