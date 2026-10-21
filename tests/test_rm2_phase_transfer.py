import copy
import json
import math
import unittest
from scripts.rm2_phase_transfer import FROZEN, CHANNELS, compare, metrics

class PhaseTransferTests(unittest.TestCase):
    def test_exact_waveform_beats_constant(self):
        x = list(range(36))
        r = metrics(x, x)
        self.assertEqual(r['rmse'], 0)
        self.assertEqual(r['skill_vs_constant'], 1)

    def test_unchanged_constant_has_no_skill(self):
        r = metrics([1]*36, list(range(36)))
        self.assertEqual(r['skill_vs_constant'], 0)
        self.assertEqual(metrics([1]*36, [1]*36)['skill_vs_constant'], None)

    def test_bad_values_rejected(self):
        for values in ([1]*35, [float('nan')]*36, [True]*36):
            with self.assertRaises(ValueError): metrics(values, [1]*36)

    def test_no_selection_or_phase_alignment(self):
        f = json.loads(FROZEN.read_text())
        rows = [{'trial_id': p['target_trial_id'], **copy.deepcopy(p['channels'])} for p in f['predictions']]
        self.assertEqual(len(compare(f, rows)), 4)
        with self.assertRaises(ValueError): compare(f, rows[:1])
        rows[0][CHANNELS[0]]['bin_midpoints_deg'][0] = 10
        with self.assertRaises(ValueError): compare(f, rows)

    def test_frozen_discloses_prior_exposure(self):
        f = json.loads(FROZEN.read_text())
        self.assertTrue(f['target_processed_means_previously_exposed'])
        self.assertIn('NOT_INDEPENDENT_VALIDATION', f['classification'])
        self.assertEqual({p['target_trial_id'] for p in f['predictions']}, {'Perf-1.0-b_10', 'Perf-1.0-b_12'})


class FrozenSourceTests(unittest.TestCase):
    def setUp(self):
        from scripts.rm2_phase_transfer import validate_source_manifest
        self.validate = validate_source_manifest
        self.f = json.loads(FROZEN.read_text())
        evidence = self.f['source_evidence']
        self.m = {'upstream_git_commit': evidence['upstream_commit'], 'phase_origin_status': evidence['phase_origin_status'], 'trials': []}
        for p in self.f['predictions']:
            name = p['target_trial_id']; ref = evidence['target_reference'][name]
            self.m['trials'].append({'trial_id':name,'run':ref['run'],'nominal_speed_m_s':p['nominal_speed_m_s'],
                'metadata':{'sha256':evidence['metadata_sha256'][name], 'id':ref['metadata_file_id']},
                'ni':{'id':ref['ni_file_id']},'source_time_window_s':evidence['target_windows_s'][name],
                **{k:ref[k] for k in ('source_mean_cp','source_mean_cd','source_n_revolutions')}})
    def test_exact_frozen_metadata_matches(self):
        self.assertEqual(len(self.validate(self.f,self.m)),2)
    def test_window_units_identity_and_source_reference_cannot_be_retuned(self):
        for field,value in [('source_time_window_s',[21,30]),('nominal_speed_m_s',1.2),('run',12),('source_mean_cp',.9),('source_mean_cd',.9),('source_n_revolutions',20)]:
            m=copy.deepcopy(self.m);m['trials'][0][field]=value
            with self.assertRaises(ValueError):self.validate(self.f,m)
        for parent,key,value in [('metadata','sha256','0'*64),('metadata','id',1),('ni','id',1)]:
            m=copy.deepcopy(self.m);m['trials'][0][parent][key]=value
            with self.assertRaises(ValueError):self.validate(self.f,m)
    def test_caller_cannot_promote_origin_or_duplicate_trials(self):
        m=copy.deepcopy(self.m);m['phase_origin_status']='DOCUMENTED_EQUIVALENT'
        with self.assertRaises(ValueError):self.validate(self.f,m)
        m=copy.deepcopy(self.m);m['trials'][1]=m['trials'][0]
        with self.assertRaises(ValueError):self.validate(self.f,m)
        m=copy.deepcopy(self.m);m['upstream_git_commit']='0'*40
        with self.assertRaises(ValueError):self.validate(self.f,m)
    def test_original_freeze_preserved_and_predictions_unchanged(self):
        import hashlib
        old=FROZEN.with_name('RM2_PHASE_TRANSFER_FROZEN.json')
        self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(),'554b46a72b0bd202ab30120e90d938a3c16f62cc3ac2ef628d947552c0d10c40')
        self.assertEqual(json.loads(old.read_text())['predictions'],self.f['predictions'])

if __name__ == '__main__': unittest.main()
