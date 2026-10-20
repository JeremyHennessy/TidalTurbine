"""Offline replay of archived *numerical* FORCE ADCP QC; not physical cell validation.

Inputs are an explicitly acquired raw CSV or GitHub Actions ZIP artifact (kept
outside Git). Refuses mismatched source SHA-256; never silently substitutes data.
No network access, predictive generation model, or scientific cell masks.
"""
import argparse
import json
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, BadZipFile

try:
    from .qa_force_slice import qc
except ImportError:
    from qa_force_slice import qc

ROOT=Path(__file__).resolve().parents[1]
KNOWN_SHA256='1a19da1e3cd214fc904d8e821cc50c7e959693aaffa4dc9c8e84ee6c663ac4cb'
REPORT=ROOT/'reports/FORCE-SLICE-QA-001.json'
RUN='https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39470715965'


def load_raw(archive=None, csv_path=None):
    if (archive is None)==(csv_path is None):
        raise ValueError('Supply exactly one of --zip and --csv')
    if archive is not None:
        with ZipFile(archive) as z:
            if 'source.csv' not in z.namelist() or 'qc.json' not in z.namelist():
                raise ValueError('Not the expected two-file acquisition artifact')
            if z.getinfo('source.csv').file_size > 8*1024*1024:
                raise ValueError('Archive source exceeds bounded acquisition budget')
            raw=z.read('source.csv')
            archived_qc=json.loads(z.read('qc.json').decode('utf-8'))
        if archived_qc.get('original_sha256')!=sha256(raw).hexdigest():
            raise ValueError('Acquisition manifest hash does not match source.csv')
        return raw,archived_qc
    raw=Path(csv_path).read_bytes()
    if len(raw)>8*1024*1024:raise ValueError('CSV exceeds bounded acquisition budget')
    return raw,None


def review(raw,expected_sha=KNOWN_SHA256,archived_qc=None):
    digest=sha256(raw).hexdigest()
    if digest!=expected_sha:raise ValueError('Raw bytes differ from declared FORCE source SHA-256')
    new=qc(raw)
    if archived_qc:
        for field in ('original_sha256','total_data_rows','valid_numeric_rows','rejected_rows','times_utc'):
            if archived_qc.get(field)!=new.get(field):
                raise ValueError('Archived QC manifest contradicts source for '+field)
    if new['valid_numeric_rows']==0:raise ValueError('No numerically parseable observations')
    return {
        'report_id':'FORCE-SLICE-QA-001',
        'evidence_class':'OBSERVED_DATA_NUMERIC_SCREEN_NOT_SCIENTIFICALLY_QC_APPROVED',
        'acquisition_utc':'2026-10-20T17:58:45Z',
        'acquisition_runner_commit':'3a3ffa54998c2a24428c87cf0f22ab7c1392b659',
        'acquisition_actions_run':RUN,
        'acquisition_artifact_id':12286987076,
        'raw_csv_bytes':len(raw),
        'attribution':'FORCE and CIOOS Atlantic, CC BY 4.0 per source metadata',
        'replay_command':'python scripts/review_force_artifact.py --zip <acquired-artifact.zip>',
        'observations_not_representative':'Only nine timestamps spanning two hours; unknown quality of individual range cells. No annual resource, turbine swept-depth, tidal statistics, extremes or device output may be inferred.',
        'decision':'BLOCK model ingestion. Resolve zero-fill/mask semantics, cell geometry and publisher QA flags before applying any velocity measurements to a rotor.',
        **new,
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    inp=ap.add_mutually_exclusive_group(required=True)
    inp.add_argument('--zip',type=Path,help='Downloaded two-file GitHub Actions artifact ZIP')
    inp.add_argument('--csv',type=Path,help='Original source.csv retained outside Git')
    ap.add_argument('--expected-sha256',default=KNOWN_SHA256,help='Pinned source SHA-256; mismatch aborts')
    ap.add_argument('--out',type=Path,default=REPORT)
    args=ap.parse_args()
    raw,prior=load_raw(archive=args.zip,csv_path=args.csv)
    data=review(raw,expected_sha=args.expected_sha256,archived_qc=prior)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('Observed rows:',data['valid_numeric_rows'],'exact all-component zero vectors:',data['exact_zero_vector_rows'],'fully zero cells:',len(data['entirely_zero_range_cells_m']))
    print('Model ingestion:',data['model_ingestion'])

if __name__=='__main__':main()
