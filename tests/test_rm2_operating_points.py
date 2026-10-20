import json
import unittest
from scripts.rm2_operating_points import generate,pareto_points,RHO_KG_M3,DIAMETER_M,HEIGHT_M

class RM2MeasuredOperatingPoints(unittest.TestCase):
    def test_observed_peak_is_exact_reference_run(self):
        r=generate()
        self.assertEqual(r['baseline']['run'],12)
        self.assertAlmostEqual(r['baseline']['cp'],0.3546025,places=7)
        self.assertAlmostEqual(r['baseline']['cd'],0.8458717,places=7)
        self.assertEqual(r['validation_status'],'REPRODUCTION_OF_PUBLISHED_PROCESSED_MEANS_ONLY')
    def test_candidate_is_selected_by_same_nominal_speed_mean_cd(self):
        r=generate(); o=r['within_lab_mechanical_power_budgets']
        self.assertEqual([p['minimum_fraction_of_peak_mechanical_cp'] for p in o],[0.9,0.95,0.98,0.99])
        self.assertEqual([p['selected_source_run'] for p in o],[9,10,10,11])
        self.assertGreater(o[0]['mechanical_cp_decrease_percent'],6)
        self.assertGreater(o[0]['mean_streamwise_cd_decrease_percent'],8)
        self.assertTrue(all(p['mechanical_cp_decrease_percent']>=0 and p['mean_streamwise_cd_decrease_percent']>=0 for p in o))
    def test_dimension_check_and_no_fatigue_claims(self):
        r=generate();b=r['baseline']
        nominal_f=0.5*RHO_KG_M3*DIAMETER_M*HEIGHT_M
        self.assertAlmostEqual(b['nominal_mechanical_power_w'],round(nominal_f*b['cp'],4),places=4)
        self.assertAlmostEqual(b['nominal_mean_rotor_drag_n'],round(nominal_f*b['cd'],4),places=4)
        self.assertIn('Cyclic blade loads',r['missing'][0]); self.assertIn('do not assign fatigue',r['decision'].lower())
    def test_dominance_is_descriptive_and_handles_tradeoff(self):
        pts=[{'run':0,'mean_cp':0.30,'mean_cd':0.8},{'run':1,'mean_cp':0.4,'mean_cd':0.7},{'run':2,'mean_cp':0.5,'mean_cd':0.9}]
        self.assertEqual([x['run'] for x in pareto_points(pts)],[1,2])
    def test_deterministic_report(self):
        r=generate();self.assertEqual(json.dumps(r,sort_keys=True),json.dumps(generate(),sort_keys=True))

if __name__=='__main__':unittest.main()
