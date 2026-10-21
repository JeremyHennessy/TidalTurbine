"""Network-free checks for exact-asset Pages release parity helper."""
from pathlib import Path
import unittest
from scripts.verify_pages_live import ASSETS, SITE, ROOT, git_blob_sha, check_once


class PagesLiveParityFixtureTests(unittest.TestCase):
    def test_expected_fixed_public_domain_and_assets(self):
        self.assertEqual(SITE, "https://jeremyhennessy.github.io/TidalTurbine/")
        self.assertEqual(len(ASSETS), len(set(ASSETS)))
        for path in ASSETS:
            self.assertFalse(path.startswith("/"))
            self.assertNotIn("..", path)
            self.assertTrue((ROOT / path).exists())

    def test_original_lab_and_processed_reports_are_packaged(self):
        self.assertIn("reports/RM2-RAW-LOADS-001.json", ASSETS)
        self.assertIn("reports/RM2-CROSSSPEED-001.json", ASSETS)
        self.assertIn("site/app.js", ASSETS)

    def test_git_blob_sha_deterministic_and_exact(self):
        self.assertEqual(git_blob_sha(b"test content"), "08cf6101416f0ce0dda3c80e627f333854c4085c")

    def test_arbitrary_urls_and_paths_rejected_before_any_network(self):
        with self.assertRaises(ValueError):
            check_once("https://some-other-host.invalid/raw")
        with self.assertRaises(ValueError):
            check_once("../unsafe")

if __name__ == "__main__":
    unittest.main()
