"""Protect prior reports, status classification and additive TidalLab research assets."""
import json
from pathlib import Path
import unittest
from scripts.build_site import FILES,ROOT

class FieldResearchTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads((ROOT/'research/field_strain_evidence_20261023.json').read_text())
  cls.plan=json.loads((ROOT/'research/metrology_prereg_v1.json').read_text())
  cls.catalogue=json.loads((ROOT/'research/catalogue.json').read_text())
  cls.html=(ROOT/'site/index.html').read_text()
 def test_research_classification_and_missing_originals(self):
  self.assertEqual(self.e['schema'],'TT-FIELD-STRAIN-EVIDENCE-001')
  self.assertTrue(all(x==0 for x in self.e['project_measurements'].values()))
  self.assertEqual(self.e['field_dataset']['resource_count'],17)
  self.assertEqual(self.e['field_dataset']['original_archives_acquired'],0)
  self.assertEqual(self.e['field_dataset']['qualified_joint_intervals'],0)
  self.assertEqual(self.e['hard_gates']['calibration_channels_unverified'],11)
  self.assertFalse(self.e['hard_gates']['contact_authorized'])
 def test_studies_have_catalogue_and_limitations(self):
  c={x['id']:x for x in self.catalogue}
  self.assertEqual(len(c),55)
  self.assertIn('CLOCK-SKEW-BLADE-2021-009',c)
  self.assertTrue(c['CLOCK-SKEW-BLADE-2021-009']['limitations'])
  original=json.loads((ROOT/'research/UNH_2022_SOURCE_ACCESS_001.json').read_text())
  self.assertEqual(self.e['publication_reported_case'],original['publisher_reported_case'])
  self.assertIsNone(original['publisher_reported_case']['exact_interval_start_utc'])
  self.assertEqual(original['scientifically_qualified_common_windows'],0)
  self.assertEqual(len(self.e['studies']),3)
  for x in self.e['studies']:
   self.assertEqual(x['url'],c[x['id']]['url'])
   self.assertTrue(c[x['id']]['limitations'])
   self.assertGreater(len(x['limitation']),30)
 def test_metrology_keeps_nine_unresolved_gates(self):
  self.assertEqual(len(self.plan['channels']),12)
  self.assertTrue(all(x['calibration_record'] is None for x in self.plan['channels']))
  self.assertEqual(len(self.plan['independent_acceptance_gates']),9)
  self.assertTrue(all(x['state']=='UNRESOLVED' for x in self.plan['independent_acceptance_gates']))
 def test_additive_research_view_assets(self):
  for asset in ('site/field_research.js','site/field_research.css','research/field_strain_evidence_20261023.json','research/metrology_prereg_v1.json'):
   self.assertIn(asset,FILES)
  self.assertIn('id="field-evidence-lab"',self.html)
  self.assertIn('id="field-channel-filters"',self.html)
  self.assertLess(self.html.index('src="app.js"'),self.html.index('src="field_research.js"'))
  for text in ('id="research-progress"','id="comparison-grid"','id="component-interface-lab"','NO BLADE STRESS DATA','No physical gate promoted.','97,911','263,250'):
   self.assertIn(text,self.html)
if __name__=='__main__':unittest.main()
