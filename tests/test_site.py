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
    def test_no_remote_script_or_font_dependencies(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf8')
        css=(ROOT/'site/styles.css').read_text(encoding='utf8')
        self.assertNotIn('http',css)
        self.assertNotIn('<script src="https',html)
