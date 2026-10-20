"""Deterministic source/claim and model-status consistency checks."""
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'id','name','scope','energy_source','capture_mechanism','motion','axis','power_takeoff','support','augmentation','controls','maintenance','demonstrated_scale_or_output','power_boundary_and_denominator','model_status','evidence_class','evidence_depth','source_url','review_depth','limitation','questions','checked_utc'}
VALID_CLASSES={'PUBLISHED_EVIDENCE','MANUFACTURER_OR_PROJECT_CLAIM','UNKNOWN_OR_CONFLICT','ENGINEERING_ASSUMPTION','DESIGN_HYPOTHESIS','SIMULATION_RESULT','EXPERIMENTALLY_VALIDATED_FINDING'}

def check():
    rows=json.loads((ROOT/'research/mechanisms.json').read_text())
    ids=set()
    assert len(rows)>=14
    for n,row in enumerate(rows):
        assert not(REQUIRED-set(row)),f'{n}: missing {REQUIRED-set(row)}'
        rid=row['id']; assert rid not in ids and rid.strip()
        ids.add(rid)
        assert row['scope']=='tidal_stream' and row['energy_source']=='free_stream_kinetic'
        assert row['evidence_class'] in VALID_CLASSES
        assert row['power_boundary_and_denominator'].strip()
        assert row['limitation'].strip()
        assert urlparse(row['source_url']).scheme=='https'
        assert row['model_status'] and not 'predictive_validated' in row['model_status']
    assert {'foil','screw','eel','viv','rim','pressure','kite','crossflow','helical','counter','savonius','duct'}.issubset(ids)
    with (ROOT/'research/CLAIM_AUDIT.csv').open(newline='') as f:claims=list(csv.DictReader(f))
    assert len(claims)>=12 and len({c['id'] for c in claims})==len(claims)
    assert all(c['assessment'] and c['unknown_or_counterevidence'] for c in claims)
    report=json.loads((ROOT/'reports/RM2-OBS-001.json').read_text())
    assert report['classification']=='EXPERIMENTAL_PROCESSED_DATA_REPRODUCTION_NOT_PREDICTIVE_VALIDATION'
    assert report['n_observations']==23
    print(f'OK: {len(rows)} classified mechanism/configuration cases, {len(claims)} audited claims, RM2 23-run processed-data reproduction (structural / provenance only)')
if __name__=='__main__':check()
