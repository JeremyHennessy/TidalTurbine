import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ShaftSupport(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=json.loads((ROOT/'research/shaft_support_006.json').read_text());cls.html=(ROOT/'site/index.html').read_text()
 def test_sources_exist(self):
  c={x['id']:x for x in json.loads((ROOT/'research/catalogue.json').read_text())}
  for s in self.d['source_ids']:self.assertIn(s,c)
  self.assertIn('2011',c['SKF-SUPPORT-006']['publication_date']);self.assertTrue(c['SKF-SUPPORT-006']['limitations'])
 def test_surface_conditions_distinct(self):
  d=self.d['source_facts']['sxl_guide_surface'];self.assertEqual(d['ideal_initial_finish'],.4);self.assertEqual(d['initial_finish_up_to'],1.6);self.assertEqual(d['maintenance_finish_strictly_less_than'],1.6);self.assertFalse(d['selected_project_specification'])
 def test_no_route_transfer(self):
  d=self.d['source_facts']['sxl_bonded_route'];self.assertTrue(d['finish_machine_bore_after_bonding']);self.assertFalse(d['interchangeable_with_tapered_key_route_established'])
 def test_unknowns_preserved(self):
  self.assertGreaterEqual(len(self.d['unknowns']),17);self.assertTrue(all(x is None for x in self.d['unknowns'].values()))
 def test_no_selection_or_torque_substitution(self):
  d=self.d['source_facts'];self.assertFalse(d['coupling_torque']['spider_rating_is_shaft_hub_rating']);self.assertIsNone(d['support_roles']['selected_arrangement'])
  for a in self.d['architectures']:self.assertFalse(a['component_selected']);self.assertFalse(a['support_loads_qualified'])
 def test_service_states_and_uncertainty_required(self):
  self.assertIn('coupling removed',self.d['required_load_cases']);self.assertIn('guide-bearing component removed',self.d['required_load_cases']);self.assertTrue(any('uncertainty' in x for x in self.d['minimum_load_record_fields']))
 def test_visible_boundary(self):
  for x in ['shaft-support-details','shaft-selection-boundary','shaft-requirements-source','No bearing or shaft selected','No physical gate promoted','below 1.6']:self.assertIn(x,self.html)
if __name__=='__main__':unittest.main()
