"""Checklist fixtures test software semantics, not a real scientific pass."""
import copy
import json
import unittest
from scripts.check_predictive_readiness import ROOT, REQUIRED, assess


class PredictiveReadinessTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((ROOT / 'research/validation_readiness_v1.json').read_text())

    def test_repository_is_blocked_and_no_claims(self):
        result = assess(self.doc)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertEqual(len(result['blocked']), sum(map(len, REQUIRED.values())))
        self.assertFalse(result['scientific_validation'])
        self.assertEqual(self.doc['current_results'], {
            'qualified_force_inflow_rows': 0, 'unh_original_samples_acquired': 0,
            'independent_predictive_holdouts_completed': 0,
            'predictive_validation_claim': False, 'net_electrical_validation_claim': False,
            'blade_stress_validation_claim': False})
        force = json.loads((ROOT / 'research/observations/FORCE_INFLOW_V0_MANIFEST_2018.json').read_text())
        self.assertEqual(force['model_eligible_rows'], self.doc['current_results']['qualified_force_inflow_rows'])

    def test_every_required_prerequisite_is_fail_closed(self):
        for group, items in REQUIRED.items():
            for name in items:
                with self.subTest(group=group, prerequisite=name):
                    altered = copy.deepcopy(self.doc)
                    del altered['gates'][group][name]
                    self.assertEqual(assess(altered)['status'], 'INVALID')

    def test_documentation_requires_pointer(self):
        item = self.doc['gates']['predictive_holdout']['frozen_solver_commit_and_environment']
        item['status'] = 'DOCUMENTED'
        for evidence in (None, '', ' ', True, []):
            item['evidence'] = evidence
            self.assertEqual(assess(self.doc)['status'], 'INVALID')

    def test_complete_fixture_does_not_validate_science(self):
        for group in self.doc['gates'].values():
            for item in group.values():
                item.update(status='DOCUMENTED', evidence='TEST FIXTURE ONLY')
        self.doc['status'] = 'CHECKLIST_COMPLETE_REVIEW_REQUIRED'
        result = assess(self.doc)
        self.assertEqual(result['status'], 'CHECKLIST_COMPLETE_REVIEW_REQUIRED')
        self.assertFalse(result['scientific_validation'])

    def test_invalid_structure_and_premature_pass_rejected(self):
        for doc in (None, [], {}, {'schema_version': 'wrong', 'gates': []}):
            self.assertEqual(assess(doc)['status'], 'INVALID')
        self.doc['gates']['force_native_inflow']['per_beam_native_quality']['status'] = 'PASS'
        self.assertEqual(assess(self.doc)['status'], 'INVALID')

    def test_scientific_claims_cannot_be_smuggled_through_metadata(self):
        for key in ('predictive_validation_claim', 'net_electrical_validation_claim',
                    'blade_stress_validation_claim'):
            for value in (True, 0, None, 'false'):
                altered = copy.deepcopy(self.doc)
                altered['current_results'][key] = value
                self.assertEqual(assess(altered)['status'], 'INVALID')

    def test_counts_schema_and_status_are_checked(self):
        for key in ('qualified_force_inflow_rows', 'unh_original_samples_acquired',
                    'independent_predictive_holdouts_completed'):
            for value in (-1, True, 1.5, '0', None):
                altered = copy.deepcopy(self.doc)
                altered['current_results'][key] = value
                self.assertEqual(assess(altered)['status'], 'INVALID')
        for key, value in (('classification', 'EXPERIMENTALLY_VALIDATED_FINDING'),
                           ('status', 'PASS'), ('current_results', {})):
            altered = copy.deepcopy(self.doc)
            altered[key] = value
            self.assertEqual(assess(altered)['status'], 'INVALID')

    def test_unresolved_evidence_type_is_checked(self):
        self.doc['gates']['force_native_inflow']['per_beam_native_quality']['evidence'] = []
        self.assertEqual(assess(self.doc)['status'], 'INVALID')

    def test_unknown_or_substituted_gate_rejected(self):
        self.doc['gates']['extra'] = {}
        self.assertEqual(assess(self.doc)['status'], 'INVALID')


if __name__ == '__main__':
    unittest.main()
