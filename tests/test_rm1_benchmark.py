import csv
from pathlib import Path
import tempfile
import unittest
from scripts.reproduce_rm1 import INPUT,reproduce

class RM1Test(unittest.TestCase):
    def test_complete_two_rotor_curve(self):
        r=reproduce()
        self.assertEqual(len(r['results']),32)
        self.assertEqual(r['reported_table']['right']['tabulated_max_cp'],0.477)
        self.assertEqual(r['reported_table']['left']['tabulated_max_cp'],0.412)
        self.assertEqual(r['reference_geometry']['number_of_rotors'],2)
        self.assertIn('No direct measured thrust',r['unverified'][2])
        self.assertTrue(r['contradictions'])
        self.assertLess(r['reported_table']['right']['maximum_relative_shaft_power_difference_percent'],1)
    def test_reject_suspicious_mechanical_power(self):
        with INPUT.open(encoding='utf8',newline='') as source:
            rows=list(csv.DictReader(source))
        rows[0]['mechanical_power_w']='500000.0'
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'tampered.csv'
            with f.open('w') as o:
                out=csv.DictWriter(o,fieldnames=rows[0].keys());out.writeheader();out.writerows(rows)
            with self.assertRaises(ValueError):reproduce(f)
    def test_reject_duplicate_rotor_run(self):
        with INPUT.open(encoding='utf8',newline='') as source:
            rows=list(csv.DictReader(source));rows[0]['rotor']='left'
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'bad.csv'
            with f.open('w') as o:
                out=csv.DictWriter(o,fieldnames=rows[0].keys());out.writeheader();out.writerows(rows)
            with self.assertRaises(ValueError):reproduce(f)
