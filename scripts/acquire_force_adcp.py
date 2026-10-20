"""Opt-in acquisition of original public FORCE ADCP NetCDF files.

No third-party scientific data stored in Git. SHA256 records exact downloaded bytes.
Passing the download step does NOT imply quality-control, datum reconstruction,
or representativeness for a physical turbine at the site.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://cioosatlantic.ca/erddap/files/'
FILES = {
    'currents': ('FORCE_Mar2018_ADCP_Currents','Burst.VTC.DSEL.AVER.classic.nc',3_348_741),
    'waves': ('FORCE_Mar2018_ADCP_Waves','Burst.VTC.WAVES.classic.nc',119_465),
}
LICENSE = 'CC BY 4.0 (as displayed in CIOOS Atlantic ERDDAP dataset metadata 2026-10-20)'
MAX_SIZE = 30 * 1024 * 1024

def source_url(dataset):
    if dataset not in FILES:raise ValueError('unknown dataset')
    item=FILES[dataset]
    return f'{BASE}{item[0]}/{item[1]}'

def acquire(dataset, out_dir, opener=urlopen, maximum_bytes=MAX_SIZE):
    """Write download into ignored raw directory; streaming bound and atomic replace."""
    dataset_dir,filename,listed_size=FILES[dataset]
    dest=Path(out_dir)/filename
    dest.parent.mkdir(parents=True,exist_ok=True)
    req=Request(source_url(dataset),headers={'User-Agent':'TidalTurbine-research/0.2 (+https://github.com/JeremyHennessy/TidalTurbine)'})
    hasher=sha256();total=0
    temp=dest.with_suffix('.partial')
    try:
        with opener(req,timeout=50) as response,temp.open('wb') as fp:
            while True:
                chunk=response.read(131072)
                if not chunk:break
                total+=len(chunk)
                if total>maximum_bytes:raise ValueError(f'download exceeds bounded size {maximum_bytes} bytes')
                fp.write(chunk);hasher.update(chunk)
        if total!=listed_size:raise ValueError(f'ERDDAP listed {listed_size} bytes but downloaded {total}; inspect upstream change')
        with temp.open('rb') as check:
            signature=check.read(8)
        if not (signature.startswith(b'CDF\x01') or signature.startswith(b'CDF\x02') or signature == b'\x89HDF\r\n\x1a\n'):
            raise ValueError('Download is not a recognized NetCDF classic or NetCDF4/HDF5 file')
        temp.replace(dest)
    finally:
        temp.unlink(missing_ok=True)
    meta={'dataset':dataset_dir,'source_url':source_url(dataset),'file':str(dest),'bytes':total,'sha256':hasher.hexdigest(),'retrieved_utc':datetime.now(timezone.utc).isoformat(),'published_license':LICENSE,'scientific_qc':'NOT_PERFORMED','instrument_alignment_and_range_datum':'NOT_VERIFIED','ingested_into_simulator':False}
    manifest=dest.with_suffix(dest.suffix+'.manifest.json')
    manifest.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf8')
    return meta

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dataset',choices=FILES,default='currents')
    ap.add_argument('--download',action='store_true',help='Explicitly download one original CC-BY dataset file (default prints plan only)')
    ap.add_argument('--out-dir',default='data/raw/force-adcp-2018')
    args=ap.parse_args(argv)
    print('Source URL:',source_url(args.dataset),'\nLicense:',LICENSE,'\nNote: not QA validated or simulator-ready')
    if not args.download:
        print('Dry run: no network request; run again with --download after checking publisher attribution and terms')
        return
    meta=acquire(args.dataset,ROOT/args.out_dir)
    print('Downloaded instrument file and manifest:',meta['sha256'],'bytes:',meta['bytes'])

if __name__=='__main__':main()
