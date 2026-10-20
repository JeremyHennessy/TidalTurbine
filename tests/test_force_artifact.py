"""Offline fixture tests; real artifact remains excluded from git and CI."""
import hashlib
import io
import json
import unittest
from zipfile import ZipFile
from scripts.review_force_artifact import review,load_raw
from scripts.qa_force_slice import qc

H='time,latitude,longitude,cell_range,eastward_sea_water_velocity,northward_sea_water_velocity,upward_sea_water_velocity\n'
U='UTC,degrees_north,degrees_east,m,m/s,m/s,m/s\n'
B=(H+U+'2018-03-30T20:03:00Z,45.3631,-64.4275,1.5,1,-1,0\n'
   +'2018-03-30T20:03:00Z,45.3631,-64.4275,31.5,0,0,0\n'
   +'2018-03-30T20:18:00Z,45.3631,-64.4275,1.5,0.5,-0.5,0\n'
   +'2018-03-30T20:18:00Z,45.3631,-64.4275,31.5,0,0,0\n').encode()
DIGEST=hashlib.sha256(B).hexdigest()

class ForceArtifactReplay(unittest.TestCase):
    def test_sha_required_and_zero_cells_blocked(self):
        with self.assertRaisesRegex(ValueError,'differ'):review(B)
        r=review(B,expected_sha=DIGEST)
        self.assertEqual(r['total_data_rows'],4)
        self.assertEqual(r['exact_zero_vector_rows'],2)
        self.assertEqual(r['entirely_zero_range_cells_m'],[31.5])
        self.assertIn('BLOCKED',r['model_ingestion'])
    def test_manifest_must_match_source(self):
        x=qc(B)
        x['valid_numeric_rows']=3
        with self.assertRaisesRegex(ValueError,'contradicts'):review(B,DIGEST,x)
    def test_zip_replay_and_checksum(self):
        data=io.BytesIO()
        with ZipFile(data,'w') as z:
            z.writestr('source.csv',B)
            z.writestr('qc.json',json.dumps(qc(B)))
        data.seek(0)
        raw,meta=load_raw(archive=data)
        self.assertEqual(raw,B)
        self.assertEqual(review(raw,DIGEST,meta)['exact_zero_vector_rows'],2)

if __name__=='__main__':unittest.main()

class FrozenObservedSampleManifest(unittest.TestCase):
    def test_public_derived_report_has_traceable_qc_hold(self):
        from pathlib import Path
        r=json.loads((Path(__file__).resolve().parents[1]/'reports/FORCE-SLICE-QA-001.json').read_text())
        self.assertEqual(r['original_sha256'],'1a19da1e3cd214fc904d8e821cc50c7e959693aaffa4dc9c8e84ee6c663ac4cb')
        self.assertEqual(r['total_data_rows'],450)
        self.assertEqual(r['valid_numeric_rows'],450)
        self.assertEqual(r['exact_zero_vector_rows'],206)
        self.assertEqual(r['nonzero_finite_vector_rows'],244)
        self.assertEqual(len(r['entirely_zero_range_cells_m']),21)
        self.assertEqual(sum(r['exact_zero_vectors_by_range_m'].values()),206)
        self.assertIn('BLOCKED',r['model_ingestion'])
        self.assertIn('NOT_SCIENTIFICALLY_QC',r['evidence_class'])
        self.assertEqual(r['acquisition_artifact_id'],12286987076)
