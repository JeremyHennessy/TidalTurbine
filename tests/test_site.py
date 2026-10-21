import tempfile
from pathlib import Path
import unittest
from scripts.build_site import build, ROOT, FILES

class SiteTests(unittest.TestCase):
    def test_every_file_present(self):
        for rel in FILES:self.assertTrue((ROOT/rel).is_file(),rel)
    def test_site_build_matches_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'site-out'
            build(target)
            for rel in FILES:
                self.assertEqual((ROOT/rel).read_bytes(),(target/rel).read_bytes(),rel)
            self.assertTrue((target/'.nojekyll').is_file())
    def test_never_label_measured_as_simulated(self):
        code=(ROOT/'site/app.js').read_text(encoding='utf8')
        self.assertIn('SIMULATION_RESULT_SYNTHETIC_NOT_VALIDATED',code)
        self.assertIn('NOT_PERFORMED',(ROOT/'scripts/acquire_force_adcp.py').read_text())
        self.assertIn('NOT TO SCALE',(ROOT/'site/app.js').read_text())
    def test_new_measured_evidence_panels_are_source_backed(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf8')
        self.assertIn('id="rm2-speed-bars"',html)
        self.assertIn('id="rm2-raw-chart"',html)
        self.assertIn('NOT A LOAD OR FIELD RESULT',html)
        self.assertIn('NO BLADE STRESS DATA',html)
        self.assertIn('reports/RM2-CROSSSPEED-001.json',FILES)
        self.assertIn('reports/RM2-RAW-LOADS-001.json',FILES)
    def test_overview_links_to_real_rm2_evidence_with_boundaries(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf8')
        self.assertIn('NEW LAB EVIDENCE',html)
        self.assertIn('Explore laboratory data',html)
        self.assertIn('Full FORCE campaign acquired',html)
        self.assertIn('blade-root stress or net electricity',html)
        self.assertIn('SCREEN-001 ONLY — SYNTHETIC, NOT VALIDATED',html)
        self.assertIn('NOT A LOAD OR FIELD RESULT',html)
        self.assertIn('NO BLADE STRESS DATA',html)
    def test_additional_source_checked_reports_are_packaged_not_misrepresented(self):
        self.assertIn('reports/RM2-RAW-B-001.json',FILES)
        self.assertIn('reports/NS-PASSAGES-7D-SUMMARY-001.json',FILES)
        self.assertEqual(__import__('json').loads((ROOT/'reports/NS-PASSAGES-7D-SUMMARY-001.json').read_text())['model_eligible_rows'],0)
        self.assertEqual(__import__('json').loads((ROOT/'reports/RM2-RAW-B-001.json').read_text())['independent_blade_strain_measurements'],0)

    def test_no_remote_script_or_font_dependencies(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf8')
        css=(ROOT/'site/styles.css').read_text(encoding='utf8')
        self.assertNotIn('http',css)
        self.assertNotIn('<script src="https',html)

class ForceQAEvidenceLinkTests(unittest.TestCase):
    def test_ocean_view_links_actual_acquired_qa_and_discloses_hold(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf8')
        self.assertIn('Full processed campaign · QC blocked',html)
        self.assertIn('FORCE-CAMPAIGN-QA-001.json',html)
        self.assertIn('FORCE-72H-QA-001.json',html)
        self.assertIn('FORCE-SLICE-QA-001.json',html)
        self.assertIn('not fit for rotor modelling',html)
        self.assertNotIn('physically validated ADCP velocity',html)

class EvidenceVisualizationPackagingTests(unittest.TestCase):
    def test_qualified_evidence_displays_use_canonical_reports(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf8')
        self.assertIn('id="rm1-plot"',html)
        self.assertIn('id="force-cells"',html)
        self.assertIn('0 SCIENTIFICALLY QUALIFIED CELLS',html)
        self.assertIn('≥20 dbar pressure screen · NOT source QC',html)
        self.assertIn('reports/RM1-OBS-001.json',FILES)
        self.assertIn('reports/FORCE-CAMPAIGN-QA-001.json',FILES)
