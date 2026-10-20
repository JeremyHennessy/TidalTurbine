import json
from pathlib import Path
import unittest
from scripts.check_ocean_catalogue import check, ROOT

class OceanCatalogueTests(unittest.TestCase):
    def setUp(self):
        self.records = json.loads((ROOT/'research/ocean_datasets.json').read_text(encoding='utf8'))
    def test_registry_valid(self):
        self.assertEqual(check(self.records), [])
        self.assertGreaterEqual(len(self.records), 15)
    def test_duplicate_id_rejected(self):
        self.assertTrue(any('duplicate identifier' in e for e in check(self.records+[self.records[0]])))
    def test_invalid_scheme_rejected(self):
        import copy
        data=copy.deepcopy(self.records)
        data[0]['source_url']='http://insecure.local'
        self.assertTrue(any('invalid source_url' in e for e in check(data)))
    def test_correct_metadata_gates(self):
        c=next(x for x in self.records if x['id']=='OCEAN-001')
        self.assertEqual(c['access_status'],'source_reviewed')
        self.assertIn('ZERO cells approved',c['acquisition_evidence'])
        self.assertEqual(c['position_wgs84'],{'latitude':45.3631,'longitude':-64.4275})
        self.assertIn('not',c['limitations'].lower())
        independent=next(x for x in self.records if x['id']=='OCEAN-021')
        self.assertEqual(independent['access_status'],'source_reviewed')
        self.assertIn('NOT Minas Passage',independent['limitations'])
        self.assertIn('60480-byte',independent['acquisition_evidence'])
        tide=next(x for x in self.records if x['id']=='OCEAN-004')
        self.assertEqual(tide['access_status'],'permission_gate')
