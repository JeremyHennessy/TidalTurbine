"""Stdlib provenance and model-safety checks independent of raw ocean archives."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'research/observations'
FORCE=ROOT/'FORCE_INFLOW_V0_MANIFEST_2018.json'
CMAR=ROOT/'CMAR_DIGBY_DG013_2022_QA.json'
CSV=ROOT/'CMAR_DIGBY_DG013_2022_QA.csv'
def check():
    f=json.loads(FORCE.read_text());d=json.loads(CMAR.read_text())
    if (f['schema_version'],f['records'],f['n_time'],f['n_cells'])!=('FORCE_INFLOW_QA_V0_20261020',263250,5265,50):raise ValueError('FORCE shape/version mismatch')
    if f['counts']!={'PENDING_NATIVE_QC_AND_GEOMETRY':165323,'SUSPECT_EXACT_ZERO_ALL_COMPONENTS':93427,'SUSPECT_LOW_PRESSURE_TRANSITION':4500}:raise ValueError('FORCE QA classification drift')
    if len(f['per_cell'])!=50 or any(sum(c.values())!=5265 for c in f['per_cell'].values()):raise ValueError('Missing cell flags')
    if f['model_eligible_rows']!=0 or f['science_approved_cells']!=0:raise ValueError('FORCE premature approval')
    if d['n_records']!=531 or d['deployment_id']!='DG013' or d['station']!='Long Beach':raise ValueError('CMAR identity')
    if d['derived_sha256']!=hashlib.sha256(CSV.read_bytes()).hexdigest():raise ValueError('CMAR derivative checksum changed')
    if d['model_eligible_rows']!=0 or d['turbine_inflow_validated'] is not False:raise ValueError('CMAR prematurely approved')
    for k,v in d['publisher_gross_range_flags'].items():
        if v!={'Pass':531}:raise ValueError('CMAR QC flags changed')
    return True
if __name__=='__main__':
    check();print('OK FORCE 263250 masked and CMAR 531 annotated; 0 model-qualified observations')
