"""Deterministic checks: discovery metadata is not ingested instrument observations."""
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'downloadable_not_acquired','metadata_only','permission_gate','portal_manual_download','discovery_portal','report_not_machine_read','source_reviewed'}
FIELDS = {'id','title','provider','category','region','source_url','variables','units','temporal_coverage','sampling_interval','position_wgs84','depth_reference','quality_flags','license','access_status','review_depth','metadata_checked_utc','next_action','limitations'}

def check(records):
    issues=[];ids=set()
    if not isinstance(records,list) or not records: return ['No records']
    for i,r in enumerate(records):
        miss=FIELDS-set(r)
        if miss:issues.append(f'{i}: missing {sorted(miss)}');continue
        rid=r['id']
        if rid in ids:issues.append(f'{rid}: duplicate identifier')
        ids.add(rid)
        if r['access_status'] not in ALLOWED:issues.append(f'{rid}: unknown status')
        if r['access_status']=='downloadable_not_acquired' and 'ingested' in r['next_action'].lower() and 'not' not in r['next_action'].lower():
            issues.append(f'{rid}: contradictory acquisition claim')
        for key in ('source_url','download_url'):
            if not r.get(key):continue
            u=urlparse(r[key]);
            if u.scheme!='https' or not u.netloc:issues.append(f'{rid}: invalid {key}')
        for key in ('provider','title','license','next_action','limitations','depth_reference','temporal_coverage'):
            if not str(r[key]).strip(): issues.append(f'{rid}: blank {key}')
        try: date.fromisoformat(r['metadata_checked_utc'])
        except (ValueError,TypeError): issues.append(f'{rid}: invalid checked date')
        if not isinstance(r['variables'],list) or not r['variables']:issues.append(f'{rid}: missing variables')
        if not isinstance(r['units'],list) or not r['units']:issues.append(f'{rid}: missing units')
        p=r['position_wgs84']
        if p is not None and (not isinstance(p,dict) or not -90<=p.get('latitude',999)<=90 or not -180<=p.get('longitude',999)<=180): issues.append(f'{rid}: invalid coordinates')
    return issues

def main():
    records=json.loads((ROOT/'research/ocean_datasets.json').read_text(encoding='utf8'))
    errors=check(records)
    if errors:
        for e in errors:print('FAIL:',e)
        raise SystemExit(1)
    print(f'OK: {len(records)} dataset-discovery records structurally checked; raw data ingestion NOT claimed')

if __name__=='__main__':main()
