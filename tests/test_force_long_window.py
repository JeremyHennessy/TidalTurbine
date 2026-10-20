import unittest, tempfile, csv, io
from pathlib import Path
from zipfile import ZipFile
from scripts.force_long_window import assess,query_url,MAX_BYTES

ARCHIVE=Path('/mnt/data/force-adcp-bounded-observations-ccby4.zip')
class ForceLongTest(unittest.TestCase):
    def test_query_has_bounded_unambiguous_comparators(self):
        u=query_url();self.assertIn('time%3E=',u);self.assertIn('time%3C=',u)
        self.assertIn('sea_water_pressure',u)
        with self.assertRaises(ValueError):query_url('2018-04-01T00:00:00Z','2018-04-20T00:00:00Z')
        with self.assertRaises(ValueError):query_url('2018-04-04T00:00:00Z','2018-04-01T00:00:00Z')
    def test_original_observation_if_available(self):
        if not ARCHIVE.exists():self.skipTest('Historic externally supplied original artifact not in CI')
        with ZipFile(ARCHIVE) as z:raw=z.read('source.csv')
        q=assess(raw,start='2018-03-30T20:02:33Z',end='2018-03-30T22:02:33Z')
        self.assertEqual(q['parseable_numeric_rows'],450)
        self.assertEqual(q['exact_all_component_zero_vectors'],206)
        self.assertEqual(len(q['all_zero_cells_m']),21)
        self.assertEqual(q['model_ingestion'],'BLOCKED_PENDING_NATIVE_QUALITY_METADATA_AND_VERIFIED_WATER_COLUMN')
    def test_fixture_zero_and_pressure_flags(self):
        hdr=['time','latitude','longitude','cell_range','eastward_sea_water_velocity','northward_sea_water_velocity','upward_sea_water_velocity','sea_water_pressure','cell_size']
        t=['2018-04-01T00:02:30Z','2018-04-01T00:17:30Z']
        rows=[['2018-04-01T00:02:30Z','45.3631','-64.4275','1.5','1','0.2','0.0','34.0','1'],
              ['2018-04-01T00:17:30Z','45.3631','-64.4275','1.5','1.2','0.3','0.0','34.1','1'],
              ['2018-04-01T00:02:30Z','45.3631','-64.4275','50.5','0','0','0','34.0','1'],
              ['2018-04-01T00:17:30Z','45.3631','-64.4275','50.5','0','0','0','34.1','1']]
        fp=io.StringIO();w=csv.writer(fp);w.writerow(hdr);w.writerow(['UTC','degrees_north','degrees_east','m','m/s','m/s','m/s','dbar','m']);w.writerows(rows)
        q=assess(fp.getvalue().encode())
        self.assertEqual(q['parseable_numeric_rows'],4)
        self.assertEqual(q['all_zero_cells_m'],[50.5])
        self.assertEqual(q['nonzero_throughout_numeric_cells_m'],[1.5])
        self.assertEqual(q['nominal_utc_time_step_s'],900)
        self.assertEqual(q['pressure_dbar_observed_min_max'],[34.0,34.1])
        self.assertEqual(q['reported_cell_size_m_values'],[1.0])
    def test_refuse_duplicate_timestamp_range(self):
        hdr=['time','latitude','longitude','cell_range','eastward_sea_water_velocity','northward_sea_water_velocity','upward_sea_water_velocity']
        row=['2018-04-01T00:02:30Z','45.3631','-64.4275','1.5','1','0.2','0.0']
        fp=io.StringIO();w=csv.writer(fp);w.writerow(hdr);w.writerow(['UTC','degrees_north','degrees_east','m','m/s','m/s','m/s']);w.writerow(row);w.writerow(row)
        q=assess(fp.getvalue().encode())
        self.assertEqual(q['rejected_rows'],1)
        self.assertEqual(q['parseable_numeric_rows'],1)
