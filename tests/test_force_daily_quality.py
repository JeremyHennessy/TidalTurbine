"""No native QC is implied by numerical flags or successful source checks."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from scripts.check_force_daily_quality import check, GRID

class ForceDailyGrid(unittest.TestCase):
    def test_full_grid_matches_pinned_source_report(self):
        self.assertTrue(check())
    def test_no_native_qc_or_modelling_claim(self):
        a=json.loads(GRID.read_text())
        self.assertEqual(a['model_eligible_rows'],0)
        self.assertEqual(a['scientific_approved_cells'],0)
        self.assertEqual(a['native_beam_qc'],'UNAVAILABLE')
        self.assertEqual(a['documented_nortek_velocity_sentinel_count_in_enu'],0)
    def test_reject_unsafe_approval(self):
        a=json.loads(GRID.read_text());a['model_eligible_rows']=1
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'a.json';p.write_text(json.dumps(a))
            with self.assertRaisesRegex(ValueError,'Premature'):check(p)
    def test_reject_corrupt_daily_classification(self):
        a=json.loads(GRID.read_text());a['daily'][0]['suspect_zero_by_cell'][0]+=1
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'a.json';p.write_text(json.dumps(a))
            with self.assertRaisesRegex(ValueError,'partition'):check(p)
    def test_direct_source_reproduction_when_available(self):
        try:from scripts.build_force_quality_grid import analyze_archive
        except ImportError:self.skipTest('Optional pinned ocean dependencies not installed')
        archive=Path('/mnt/data/force-spring2018-complete-processed-netcdf.zip')
        if not archive.exists():self.skipTest('Original FORCE source archive not present in CI checkout')
        actual=analyze_archive(archive)
        self.assertEqual(actual,json.loads(GRID.read_text()))
