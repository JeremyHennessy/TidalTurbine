"""Schema/integrity verification for unranked cross-mechanism comparison gates."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'research/prototype_gates.json'
REQUIRED=('mechanical_reference_data','independent_predictive_model','qualified_site_inflow','net_electrical_power','fatigue','environment','manufacturing','maintenance')

def verify(path=P):
    d=json.loads(Path(path).read_text(encoding='utf8'))
    if d['classification']!='COMPARISON_PROTOCOL_NOT_PERFORMANCE_RANKING':raise ValueError('Invalid evidence gate description')
    if len(d['candidates'])!=3:raise ValueError('Three deliberately distinct mechanisms required')
    ids=[c['id'] for c in d['candidates']]
    if len(set(ids))!=3:raise ValueError('Duplicate architecture')
    for c in d['candidates']:
        if set(c['gates'])!=set(REQUIRED):raise ValueError('Missing separate critical gate')
        if any(v not in ('UNKNOWN','EVIDENCE_AVAILABLE_PARTIAL','PASS','FAIL') for v in c['gates'].values()):raise ValueError('Unsupported evidence status')
        if any(k in c for k in ('score','rank','winner','estimated_cp','estimated_kwh')):raise ValueError('Invented numerical ranking')
        for key in ('energy_denominator','PTO','loads','observed_benchmark','control','published_source'):
            if not c.get(key):raise ValueError('Missing physical comparability field '+key)
    return ids

if __name__=='__main__':print('Verified separate unrated evidence gates:',verify())
