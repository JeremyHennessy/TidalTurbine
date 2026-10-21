import copy
import json
import unittest
from scripts.check_tidal_channel_alignment import DEFAULT, check

class AlignmentTests(unittest.TestCase):
    def setUp(self): self.record = json.loads(DEFAULT.read_text())
    def test_actual_source_conflict_is_not_repaired(self):
        before = copy.deepcopy(self.record)
        r = check(self.record)
        self.assertEqual(self.record, before)
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertFalse(r['physical_validation'])
        c = r['comparisons'][-1]
        self.assertEqual(c['increment_ratio_to_reference'], 2000)
        self.assertAlmostEqual(c['relative_start_difference_s'], .098499)
        self.assertEqual(len(r['issues']), 4)
    def test_matching_synthetic_metadata_is_not_validation(self):
        self.record['channels'] = self.record['channels'][:4]
        self.record['phase_origin_evidence'] = 'SYNTHETIC TEST ONLY'
        self.assertEqual(check(self.record)['status'], 'METADATA_CONSISTENT_REVIEW_REQUIRED')
        self.assertFalse(check(self.record)['physical_validation'])
    def test_invalid_increment_count_and_duplicate_rejected(self):
        for field, value in [('sample_count', True), ('sample_count',0), ('increment_s',float('nan')), ('increment_s',0)]:
            x = copy.deepcopy(self.record); x['channels'][0][field] = value
            with self.assertRaises(ValueError): check(x)
        self.record['channels'][1]['name'] = self.record['channels'][0]['name']
        with self.assertRaises(ValueError): check(self.record)
    def test_missing_phase_evidence_blocks_even_matching_clocks(self):
        self.record['channels'] = self.record['channels'][:4]
        self.assertEqual(check(self.record)['status'],'BLOCKED')
    def test_empty_or_malformed_phase_evidence_stays_blocked(self):
        self.record['channels'] = self.record['channels'][:4]
        for value in ('', '  ', False, {}, [], 1):
            self.record['phase_origin_evidence'] = value
            self.assertEqual(check(self.record)['status'], 'BLOCKED')
    def test_ambiguous_timezone_not_silently_converted(self):
        self.record['channels'][0]['start_time_as_stored'] += '+00:00'
        with self.assertRaises(ValueError): check(self.record)

if __name__ == '__main__': unittest.main()
