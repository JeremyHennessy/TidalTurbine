import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile
from scripts.force_72h_summary import reproduce, EXPECTED_SOURCE_SHA

LOCAL=Path('/mnt/data/force-adcp-72h-raw-qa-ccby4.zip')
class SourceReproductionTests(unittest.TestCase):
    def test_bounded_original_measurements_if_available(self):
        if not LOCAL.exists(): self.skipTest('Original source artifact not checked into Git or remote CI')
        r=reproduce(LOCAL)
        self.assertEqual(r['numeric_qa']['parseable_numeric_rows'],14400)
        self.assertEqual(r['numeric_qa']['exact_all_component_zero_vectors'],5160)
        self.assertEqual(len(r['numeric_qa']['all_zero_cells_m']),12)
        self.assertEqual(r['qualified_current_bins'],[])
        self.assertAlmostEqual(r['pressure_vs_highest_nonzero_range']['pearson_correlation'],0.996882,places=5)
    def test_immutable_source_sha(self):
        self.assertEqual(len(EXPECTED_SOURCE_SHA),64)
        if LOCAL.exists():
            with self.assertRaises(ValueError): reproduce(LOCAL,expected_sha='0'*64)
    def test_report_must_stay_explicitly_unqualified(self):
        from scripts.force_72h_summary import REPORT
        r=json.loads(REPORT.read_text())
        self.assertFalse(r['qualified_current_bins'])
        self.assertTrue(r['model_ingestion'].startswith('BLOCKED'))
        self.assertIn('discrepancy',r['verified_deployment_geometry']['critical_mapping_discrepancy'].lower())
