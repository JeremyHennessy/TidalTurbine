import unittest
from scripts.qa_force_slice import qc,request_url
class QA(unittest.TestCase):
    def test_bounded_url(self):
        u=request_url()
        self.assertIn('&time%3E=2018-03-30T20:02:33Z',u)
        self.assertIn('&time%3C=2018-03-30T22:02:33Z',u)
        self.assertNotIn('time%3E%3D=',u)
        self.assertNotIn('time%3C%3D=',u)
    def test_qc_detects_invalid_duplicate_and_does_not_call_it_validated(self):
        h='time,latitude,longitude,cell_range,eastward_sea_water_velocity,northward_sea_water_velocity,upward_sea_water_velocity\n'
        units='UTC,degrees_north,degrees_east,m,m/s,m/s,m/s\n'
        s=h+units+'2018-03-30T20:03:00Z,45.3631,-64.4275,10.5,1,-1,0\n2018-03-30T20:04:00Z,45.3631,-64.4275,10.5,2,-2,0\n2018-03-30T20:04:00Z,45.3631,-64.4275,10.5,2,-2,0\n2018-03-30T20:05:00Z,45.3631,-64.4275,10.5,NaN,3,0\n'
        r=qc(s.encode());self.assertEqual(r['valid_numeric_rows'],2);self.assertEqual(r['rejected_rows'],2)
        self.assertEqual(r['nominal_timestep_s'],60)
        self.assertEqual(r['model_ingestion'],'BLOCKED_PENDING_INSTRUMENT_GEOMETRY_AND_QC')
    def test_zero_filled_vectors_flagged_not_counted_as_physically_valid(self):
        header='time,latitude,longitude,cell_range,eastward_sea_water_velocity,northward_sea_water_velocity,upward_sea_water_velocity\n'
        units='UTC,degrees_north,degrees_east,m,m/s,m/s,m/s\n'
        rows=('2018-03-30T20:03:00Z,45.3631,-64.4275,1.5,1,-1,0\n'
              '2018-03-30T20:03:00Z,45.3631,-64.4275,30.5,0,0,0\n'
              '2018-03-30T20:18:00Z,45.3631,-64.4275,1.5,2,-2,0\n'
              '2018-03-30T20:18:00Z,45.3631,-64.4275,30.5,0,0,0\n')
        data=qc((header+units+rows).encode())
        self.assertEqual(data['valid_numeric_rows'],4)
        self.assertEqual(data['exact_zero_vector_rows'],2)
        self.assertEqual(data['nonzero_finite_vector_rows'],2)
        self.assertEqual(data['entirely_zero_range_cells_m'],[30.5])
        self.assertIn('MASK',data['zero_vector_quality_interpretation'])
        self.assertIn('BLOCKED',data['model_ingestion'])
    def test_empty_observation_rejected(self):
        with self.assertRaises(ValueError):qc(b'time,latitude,longitude,cell_range,eastward_sea_water_velocity,northward_sea_water_velocity,upward_sea_water_velocity\n')
if __name__=='__main__':unittest.main()
