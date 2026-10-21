import copy
import unittest
from tidal_screen.measured_load_gate import compare

class MeasuredLoadGateTests(unittest.TestCase):
    def run_fixture(self, id, bending, power, speed=1.0):
        return {'evidence_class':'SYNTHETIC_UNIT_TEST','source_id':'fabricated-test-only','source_sha256':'test-only',
                'test_id':id,'velocity_calibration_id':'fixture','load_calibration_id':'fixture',
                'electrical_calibration_id':'fixture','mean_inflow_m_s':speed,'turbulence_intensity':0.1,
                'samples':[{'time_s':float(j),'generator_terminal_w':p,'controller_consumption_w':1.0,
                    'auxiliary_consumption_w':1.0,'blade_root_bending_n_m':m} for j,(p,m) in enumerate(zip(power,bending))]}
    def test_synthetic_is_rejected_by_default(self):
        a=self.run_fixture('A',[1,2,3,4],[10]*4)
        b=self.run_fixture('B',[1,2,3,4],[10]*4)
        with self.assertRaisesRegex(ValueError,'Measured load-energy evidence required'):compare(a,b,tolerance_m_s=.01,tolerance_ti=.02)
    def test_analytical_energy_and_dynamic_load(self):
        a=self.run_fixture('A',[-2,2,-2,2],[12]*4)
        b=self.run_fixture('B',[-1,1,-1,1],[11]*4)
        r=compare(a,b,tolerance_m_s=0,tolerance_ti=0,allow_synthetic=True)
        self.assertEqual(r['baseline']['net_electrical_energy_j'],30)
        self.assertEqual(r['candidate']['net_electrical_energy_j'],27)
        self.assertEqual(r['energy_delta_j'],-3)
        self.assertEqual(r['baseline']['alternating_bending_rms_n_m'],2)
        self.assertEqual(r['candidate']['alternating_bending_rms_n_m'],1)
        self.assertEqual(r['evidence_class'],'SYNTHETIC_UNIT_TEST_ONLY')
    def test_inflow_mismatch_rejected(self):
        a=self.run_fixture('A',[1]*4,[10]*4)
        b=self.run_fixture('B',[1]*4,[10]*4,speed=1.1)
        with self.assertRaisesRegex(ValueError,'do not meet'):compare(a,b,tolerance_m_s=.01,tolerance_ti=.02,allow_synthetic=True)
    def test_missing_bending_rejected(self):
        a=self.run_fixture('A',[1]*4,[10]*4);b=self.run_fixture('B',[1]*4,[10]*4)
        del a['samples'][0]['blade_root_bending_n_m']
        with self.assertRaisesRegex(ValueError,'Missing synchronized'):compare(a,b,tolerance_m_s=.01,tolerance_ti=.02,allow_synthetic=True)
    def test_missing_calibration_rejected(self):
        a=self.run_fixture('A',[1]*4,[10]*4);b=self.run_fixture('B',[1]*4,[10]*4)
        del a['velocity_calibration_id']
        with self.assertRaisesRegex(ValueError,'Missing observed-run evidence'):compare(a,b,tolerance_m_s=.01,tolerance_ti=.02,allow_synthetic=True)
    def test_timing_and_negative_consumption_rejected(self):
        a=self.run_fixture('A',[1]*4,[10]*4);b=self.run_fixture('B',[1]*4,[10]*4)
        a['samples'][1]['time_s']=0
        with self.assertRaisesRegex(ValueError,'Out-of-order'):compare(a,b,tolerance_m_s=.01,tolerance_ti=.02,allow_synthetic=True)
        a=self.run_fixture('A',[1]*4,[10]*4);a['samples'][0]['controller_consumption_w']=-1
        with self.assertRaisesRegex(ValueError,'nonnegative'):compare(a,b,tolerance_m_s=.01,tolerance_ti=.02,allow_synthetic=True)
    def test_same_source_run_cannot_claim_replication(self):
        a=self.run_fixture('A',[1]*4,[10]*4)
        with self.assertRaisesRegex(ValueError,'same physical experiment'):compare(a,a,tolerance_m_s=.01,tolerance_ti=.02,allow_synthetic=True)
