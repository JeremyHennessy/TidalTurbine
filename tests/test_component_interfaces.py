"""Traceability and presentation consistency, not physical qualification."""
import json
from pathlib import Path
import unittest
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids={};self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:
   if d['id'] in self.ids:raise AssertionError('duplicate ID '+d['id'])
   self.ids[d['id']]=tag
  if tag=='a':self.links.append(d.get('href',''))
class Interfaces(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'research/component_interfaces_005.json').read_text());cls.h=(ROOT/'site/index.html').read_text();cls.a=(ROOT/'site/app.js').read_text()
 def test_source_traceability(self):
  c={x['id']:x for x in json.loads((ROOT/'research/catalogue.json').read_text())}
  for sid in self.r['source_ids']:
   self.assertIn(sid,c);self.assertEqual(c[sid]['evidence_class'],'MANUFACTURER_OR_PROJECT_CLAIM');self.assertTrue(c[sid]['limitations'])
 def test_catalogue_dimensions_not_turbine_geometry(self):
  e=self.r['catalogue_example'];self.assertFalse(e['selected']);self.assertEqual(e['dimensions'],dict(L=114,E=24,DH=80,W=15,bore_min=24,bore_max=45));self.assertIsNone(e['complete_service_envelope_mm'])
 def test_unknowns_stay_unknown(self):
  self.assertGreaterEqual(len(self.r['unknowns']),9);self.assertTrue(all(x is None for x in self.r['unknowns'].values()))
 def test_no_architecture_qualified(self):
  rows={x['id']:x for x in self.r['architectures']};self.assertEqual(len(rows),3)
  for r in rows.values():self.assertFalse(r['full_retrieval_qualified']);self.assertFalse(r['component_size_selected'])
  self.assertTrue(rows['CF-LIFT-2']['dry_coupling_candidate']);self.assertTrue(rows['AX-DRY-2']['dry_coupling_candidate']);self.assertFalse(rows['AX-POD-2']['dry_coupling_candidate'])
 def test_hypothesis_can_be_falsified(self):
  for k in ['question','comparator','mechanism','falsifier','necessary_evidence']:self.assertTrue(self.r['hypothesis'][k])
 def test_views_and_sources_present(self):
  t=Tags(self.h)
  for sid in ['research-progress','research-next-evidence','research-status-boundary','component-interface-lab','component-boundary']:self.assertIn(sid,t.ids)
  self.assertIn('#designs',t.links);self.assertIn('https://www.ktr.com/fileadmin/ktr/media/Manuals/40229en000000.pdf',t.links)
 def test_service_stage_not_silently_promoted(self):
  self.assertIn("'DESK STUDY IN PROGRESS · FIELD EVIDENCE PENDING', 'pending'",self.a)
  self.assertNotIn("'Serviceability & lifecycle cost', 'Maintenance histories, realistic weather access windows, failure and repair uncertainty.', 'NOT STARTED'",self.a)
  self.assertIn('No physical gate promoted',self.h)
 def test_source_blockers_preserved(self):
  for token in ['Zero qualified cells','B10/B12','physical encoder zero','Catalogue dimensions do not replace']:self.assertIn(token,self.h)
if __name__=='__main__':unittest.main()
