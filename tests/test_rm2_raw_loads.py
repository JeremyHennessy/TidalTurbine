"""Original six NI trial provenance and physical claim regression checks (stdlib-only)."""
import json
import unittest
from pathlib import Path
from scripts.rm2_raw_loads import load_manifest, validate_committed, ROOT

REPORT=ROOT/"reports/RM2-RAW-LOADS-001.json"
BOM=ROOT/"research/prototype_test_rig_bom_v1.json"

class RawNiEvidence(unittest.TestCase):
    def test_six_source_sha256_pins_and_custody(self):
        m=load_manifest()
        self.assertEqual(len(m["trials"]),6)
        self.assertFalse(m["source_data_committed_to_git"])
        self.assertEqual({x["trial_id"] for x in m["trials"]},
                         {"Perf-0.4_10","Perf-0.4_12","Perf-1.0_10",
                          "Perf-1.0_12","Perf-1.2_10","Perf-1.2_12"})
        for t in m["trials"]:
            self.assertEqual(len(t["ni"]["sha256"]),64)
            self.assertGreater(t["ni"]["bytes"],1_000_000)
            self.assertGreater(t["metadata"]["bytes"],1000)

    def test_archive_numerical_reduction_matches_source_within_bound(self):
        r=validate_committed()
        self.assertEqual(r["six_trials_acquired_and_sha_validated"],6)
        self.assertEqual(len(r["within_speed_pairs"]),3)
        for t in r["trials"]:
            self.assertEqual(t["sample_rate_hz"],2000)
            self.assertGreater(t["steady_window_samples"],17000)
            self.assertLess(t["cp_reproduction_abs_error"],.006)
            self.assertLess(t["cd_reproduction_abs_error"],.006)

    def test_lower_drag_does_not_prove_all_rig_load_variability_decreases(self):
        r=json.loads(REPORT.read_text(encoding="utf8"))
        for pair in r["within_speed_pairs"]:
            self.assertLess(pair["support_mean_drag_change_percent"],0)
        one=next(p for p in r["within_speed_pairs"] if p["nominal_speed_m_s"]==1.)
        self.assertGreater(one["shaft_torque_std_change_percent"],0)
        self.assertLess(one["support_drag_p95_change_percent"],0)
        self.assertEqual(r["scientific_gates"]["fatigue_damage"],"NOT_EVALUABLE")
        self.assertEqual(r["scientific_gates"]["blade_root_strain"],"NOT_ACQUIRED")
        self.assertEqual(r["scientific_gates"]["net_delivered_electrical_energy"],"NOT_MEASURED")

    def test_rig_bom_not_a_purchase_order_or_equipment_certification(self):
        d=json.loads(BOM.read_text(encoding="utf8"))
        self.assertEqual(len(d["systems"]),20)
        self.assertFalse(d["approval_to_purchase"])
        self.assertFalse(d["physical_device_built"])
        self.assertFalse(d["costing"]["material_unit_prices_known"])
        self.assertEqual(d["costing"]["supplier_quotes_verified"],0)
        self.assertTrue(all(x["gate"] for x in d["systems"]))
        self.assertEqual(d["gates"]["physical_water_test"],"NOT_AUTHORIZED")

    def test_selected_raw_data_are_external_to_repository(self):
        d=json.loads(REPORT.read_text(encoding="utf8"))
        self.assertIn("NOT_BLADE_STRAIN_OR_FATIGUE",d["classification"])
        for t in d["trials"]:
            self.assertEqual(len(t["rig_shaft_torque_phase_mean"]["means"]),36)
            self.assertEqual(len(t["rig_support_drag_phase_mean"]["means"]),36)
        self.assertFalse((ROOT/"data/local/rm2_six_raw/Perf-1.0_10_nidata.h5").exists(),
                         "third-party binary should not enter source checkout")

if __name__=="__main__":
    unittest.main()
