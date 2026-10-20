import unittest
from scripts.check_ingestion_reports import check
class SafetyChecks(unittest.TestCase):
    def test_published_count_and_sha(self):self.assertTrue(check())
    def test_publisher_gate_not_equal_numerical_gate(self):
        from scripts.check_ingestion_reports import CMAR,FORCE
        import json
        c=json.loads(CMAR.read_text());f=json.loads(FORCE.read_text())
        self.assertEqual(c['model_eligible_rows'],0)
        self.assertEqual(f['science_approved_cells'],0)
    def test_source_metadata_no_axial_sweep_inference(self):
        from scripts.check_ingestion_reports import CMAR
        import json
        self.assertIn('NOT a 3D current profile',json.loads(CMAR.read_text())['source_type'])
try:
    from scripts.export_force_inflow_v0 import flag,PENDING,ZERO,LOW,MISSING
except ImportError:
    flag=None
@unittest.skipUnless(flag is not None,'Optional h5py/numpy required to test complete FORCE numeric flags')
class InflowFlags(unittest.TestCase):
    def test_zero_is_not_slack_current(self):self.assertEqual(flag(0,0,0,35),ZERO)
    def test_nonzero_never_means_native_qc(self):self.assertEqual(flag(1.2,-0.3,0,35),PENDING)
    def test_recovery_screen_precedes_zero_mask(self):self.assertEqual(flag(0,0,0,0.6),LOW)
    def test_nonfinite_is_missing(self):self.assertEqual(flag(float('nan'),0,0,36),MISSING)
if __name__=='__main__':unittest.main()
