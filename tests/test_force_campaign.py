"""Small artificial source arrays: guard numerical screening from being called scientific QC."""
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

try:
    import h5py
    import numpy as np
    from scripts.process_force_campaign import assess_arrays, verify_archive, write_results, SOURCES, STATUS
    HAS_OCEAN_DEPS=True
except ImportError:
    HAS_OCEAN_DEPS=False


def fixture():
    times = np.array([1_522_440_153.0 + 900 * i for i in range(5)])
    current = {
        "time": times,
        "cell_range": np.array([1.5, 2.5, 3.5]),
        "cell_size": np.array([1., 1., 1., 1., 0.]),
        "sea_water_pressure": np.array([34., 35., 36., 0.6, 0.7]),
        "eastward_sea_water_velocity": np.array([[1,2,3,0,0], [3,2,2,0,0], [0,0,0,0,0]],float),
        "northward_sea_water_velocity": np.zeros((3,5)),
        "upward_sea_water_velocity": np.zeros((3,5)),
        "_attrs": {"geospatial_lat_max":"45.3631389", "geospatial_lon_max":"-64.4274722", "history":"fixture"},
    }
    waves = {
        "time": times + 0.0002,
        "sea_water_pressure": np.array([34.01, 35.02, 36.01, 0.6, 0.7]),
        "sea_surface_wave_significant_height": np.array([0.2,0.3,0.4,3.4,0.2]),
        "sea_surface_wave_maximum_period": np.array([4,5,-9,11,3.5]),
    }
    return current, waves


@unittest.skipUnless(HAS_OCEAN_DEPS, "Install optional requirements-ocean.txt for full-campaign HDF5 QA tests")
class FullCampaignTests(unittest.TestCase):
    def test_allzero_interval_and_preterminal_nozero_cells_are_distinguished(self):
        c, w = fixture()
        r=assess_arrays(c,w)
        self.assertEqual(r["time_bursts"],5)
        self.assertEqual(r["total_all_component_exact_zero"],9)
        self.assertEqual(r["preterminal_pressure_screen_bursts"],3)
        self.assertEqual(r["preterminal_pressure_screen_ranges_no_zero_m"],[1.5,2.5])
        self.assertEqual(r["preterminal_pressure_screen_ranges_always_zero_m"],[3.5])
        self.assertEqual(r["all_zero_velocity_bursts"],2)
        self.assertEqual(r["pressure_below_20dbar_and_allzero"],2)
        self.assertEqual(r["wave_maximum_period_fill_minus9_count"],1)
        self.assertEqual(r["wave_hs_numeric_comparison_excluding_pressure_collapse"],[0.2,0.4])
        self.assertEqual(r["source_approved_velocity_records"],0)
        self.assertEqual(r["status"],STATUS)
        self.assertIn("BLOCKED",r["model_ingestion"])

    def test_misaligned_companion_time_rejected(self):
        c,w=fixture()
        w["time"]=w["time"]+1.0
        with self.assertRaisesRegex(ValueError,"timestamps"):
            assess_arrays(c,w)

    def test_shuffled_source_times_rejected(self):
        c,w=fixture()
        c["time"][2]=c["time"][1]
        with self.assertRaisesRegex(ValueError,"increasing"):
            assess_arrays(c,w)

    def test_shapes_rejected_not_silently_broadcast(self):
        c,w=fixture()
        c["northward_sea_water_velocity"]=np.zeros((5,3))
        with self.assertRaisesRegex(ValueError,"shapes"):
            assess_arrays(c,w)

    def test_wave_missing_is_not_zero(self):
        c,w=fixture()
        report=assess_arrays(c,w)
        self.assertEqual(report["wave_maximum_period_numeric_count"],4)
        self.assertEqual(report["wave_maximum_period_fill_minus9_count"],1)

    def test_reproduced_reports_written_with_deterministic_keys(self):
        c,w=fixture()
        r=assess_arrays(c,w)
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)/"r.json";d=Path(folder)/"days.csv"
            write_results(r,out,d)
            self.assertEqual(json.loads(out.read_text())["source_approved_velocity_records"],0)
            self.assertIn("date_utc",d.read_text())
            before=out.read_bytes()
            write_results(r,out,d)
            self.assertEqual(before,out.read_bytes())

    def test_archive_rejects_mismatched_member_and_missing_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"source.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("currents.nc",b"not netcdf")
                z.writestr("waves.nc",b"not netcdf")
            with self.assertRaisesRegex(ValueError,"Unexpected archive members"):
                verify_archive(p)


if __name__=='__main__':
    unittest.main()
