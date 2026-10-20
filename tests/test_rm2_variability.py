import csv, tempfile
from pathlib import Path
import unittest
from scripts.rm2_variability import summarize,SRC
from scripts.check_prototypes import verify
class VariabilityTest(unittest.TestCase):
    def test_descriptive_not_fatigue(self):
        r=summarize()
        self.assertEqual(len(r['source_rows']),6)
        self.assertAlmostEqual(r['descriptive_percent_change_candidate_vs_baseline']['mean_cp'],-1.8477)
        self.assertAlmostEqual(r['descriptive_percent_change_candidate_vs_baseline']['std_cp_per_rev'],-47.7563)
        self.assertIn('blade-root bending',r['definition'])
    def test_invalid_duplicate_run(self):
        with SRC.open(encoding='utf8',newline='') as source:
            rows=list(csv.DictReader(source));rows[0]['run']='10'
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.csv'
            with p.open('w') as f:
                w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
            with self.assertRaises(ValueError):summarize(p)
    def test_prototype_no_winner(self):
        self.assertEqual(len(verify()),3)
