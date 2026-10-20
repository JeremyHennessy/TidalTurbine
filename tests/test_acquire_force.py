import io
import tempfile
import unittest
from pathlib import Path
from scripts.acquire_force_adcp import source_url, acquire, FILES

class FakeResponse(io.BytesIO):
    def __enter__(self):return self
    def __exit__(self,*args):self.close()

class ForceDownloadTests(unittest.TestCase):
    def test_source_url_fixed_allowlist(self):
        self.assertIn('FORCE_Mar2018_ADCP_Currents',source_url('currents'))
        with self.assertRaises(ValueError):source_url('https://evil.example')
    def test_manifest_preserves_no_qc_claim(self):
        # Only a synthetic byte stream for downloader mechanics. Not field data.
        data=b'CDF\x02'+b'\x00'*(FILES['waves'][2]-4)
        data=data[:FILES['waves'][2]]
        with tempfile.TemporaryDirectory() as p:
            meta=acquire('waves',p,opener=lambda req,timeout:FakeResponse(data))
            self.assertFalse(meta['ingested_into_simulator'])
            self.assertEqual(meta['scientific_qc'],'NOT_PERFORMED')
            self.assertEqual(meta['bytes'],len(data))
            self.assertTrue((Path(p)/FILES['waves'][1]).exists())
    def test_invalid_binary_magic_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaisesRegex(ValueError,'not a recognized NetCDF'):
                acquire('waves',p,opener=lambda req,timeout:FakeResponse(b'X'*FILES['waves'][2]))
            self.assertFalse(list(Path(p).glob('*.partial')))
    def test_overlimit_cleans_partial(self):
        data=b'x'*500
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaises(ValueError):acquire('waves',p,opener=lambda req,timeout:FakeResponse(data),maximum_bytes=200)
            self.assertFalse(list(Path(p).glob('*.partial')))
