"""Bounded *measurement acquisition* and arithmetic QC for FORCE ADCP ERDDAP CSV.

Default: no network. --fetch downloads one short source interval to an ignored
local data directory, preserving raw CSV, SHA256 and QC manifest. QC is NOT
scientific validation: this metadata product has no per-measurement QC flag
listed and orientation/transducer datum remain unresolved.
"""
import argparse
import csv
from collections import Counter,defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from math import hypot, isfinite
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[1]
DATASET='FORCE_Mar2018_ADCP_Currents'
BASE='https://cioosatlantic.ca/erddap/tabledap/'+DATASET+'.csv'
START='2018-03-30T20:02:33Z'
END='2018-03-30T22:02:33Z'
FIELDS=['time','latitude','longitude','cell_range','eastward_sea_water_velocity','northward_sea_water_velocity','upward_sea_water_velocity']
MAX_BYTES=8*1024*1024

def request_url():
    # Escape ampersands/inequalities correctly, retaining a literal comma in variables.
    # The URL uses server-side time filters, so never request the full campaign.
    return BASE+'?'+','.join(FIELDS)+'&'+urlencode({'time>=':START,'time<=':END})

def download(opener=urlopen,cap=MAX_BYTES):
    req=Request(request_url(),headers={'User-Agent':'TidalTurbine-academic-research/0.3'})
    with opener(req,timeout=35) as resp:
        out=bytearray()
        while True:
            block=resp.read(min(131072,cap+1-len(out)))
            if not block:break
            out.extend(block)
            if len(out)>cap:raise ValueError('ERDDAP response exceeds allowed byte budget')
    if len(out)<80:raise ValueError('CSV response too short for even one observation')
    data=bytes(out)
    if not data.lstrip().startswith(b'time,'):raise ValueError('Expected ERDDAP CSV columns, not an HTML error')
    return data

def qc(raw):
    parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if not parsed:raise ValueError('No rows')
    # ERDDAP .csv files generally include units in second line, unlike .csv0.
    units_row=parsed[0] if parsed[0].get('time','').lower() in ('utc','iso8601','') else None
    rows=parsed[1:] if units_row else parsed
    for field in FIELDS:
        if field not in parsed[0]:raise ValueError('Missing field '+field)
    valid=[];failure=Counter();uniques=set();bins=defaultdict(list);lat=set();lon=set()
    for row in rows:
        try:
            d=datetime.fromisoformat(row['time'].replace('Z','+00:00'))
            if d.tzinfo is None or not (START<=d.strftime('%Y-%m-%dT%H:%M:%SZ')<=END):raise ValueError('bad time or zone')
            y=float(row['latitude']);x=float(row['longitude']);z=float(row['cell_range'])
            u=float(row['eastward_sea_water_velocity']);v=float(row['northward_sea_water_velocity']);w=float(row['upward_sea_water_velocity'])
            if not all(isfinite(n) for n in (x,y,z,u,v,w)):raise ValueError('nonfinite')
            if not(-90<=y<=90 and -180<=x<=180 and z>=0):raise ValueError('coordinates/range')
            if any(abs(c)>15 for c in (u,v,w)):raise ValueError('above arithmetic screening threshold (not a physics conclusion)')
            key=(d,z)
            if key in uniques:raise ValueError('duplicate time/range cell')
            uniques.add(key);bins[z].append(d);lat.add(y);lon.add(x)
            valid.append((d,z,u,v,w))
        except (ValueError,TypeError,KeyError) as ex:failure[str(ex)]+=1
    all_times=sorted({r[0] for r in valid})
    gaps_s=[(b-a).total_seconds() for a,b in zip(all_times,all_times[1:])]
    all_ranges=sorted(bins)
    by_time=Counter(t for t,*_ in valid)
    return {
     'source_id':'OCEAN-001','classification':'OBSERVED_SOURCE_SLICE_ARITHMETIC_QC_ONLY',
     'source_url':request_url(),'original_sha256':sha256(raw).hexdigest(),
     'total_data_rows':len(rows),'valid_numeric_rows':len(valid),'rejected_rows':sum(failure.values()),
     'rejection_reasons':dict(failure),'times_utc':len(all_times),
     'observed_period_utc':([all_times[0].isoformat(),all_times[-1].isoformat()] if all_times else []),
     'cell_range_m':all_ranges,'cell_ranges_are_not_geodetic_depths':True,
     'observed_latitudes':sorted(lat),'observed_longitudes':sorted(lon),
     'nominal_timestep_s':Counter(gaps_s).most_common(1)[0][0] if gaps_s else None,
     'time_step_range_s':[min(gaps_s),max(gaps_s)] if gaps_s else [],
     'cells_per_timestamp_min_max':[min(by_time.values()),max(by_time.values())] if by_time else [],
     'quality_flags':'NO_PER_ROW_QC_FLAG_IN_LISTED_PRODUCT; numerical filters do not replace publisher QC',
     'geometry_flags':'Transducer height, facing, instrument orientation, sidelobe/near-surface masking and pressure datum UNVERIFIED',
     'model_ingestion':'BLOCKED_PENDING_INSTRUMENT_GEOMETRY_AND_QC','license':'CC BY 4.0; FORCE/CIOOS Atlantic',
     'limitation':'Two-hour measurement slice cannot estimate annual energy, extremes or resource; cell_range is transducer-relative.'
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fetch',action='store_true',help='Explicit real network acquisition of bounded 2-hour FORCE observations')
    p.add_argument('--input',type=Path,help='QC an already acquired CSV (no network)')
    p.add_argument('--out',type=Path,default=ROOT/'data/local/force_adcp_slice')
    a=p.parse_args()
    print('SOURCE',request_url())
    if not a.fetch and a.input is None:
        print('DRY RUN: no observation has been downloaded and no QC has been performed')
        return
    if a.fetch and a.input: p.error('Choose --fetch OR --input')
    raw=download() if a.fetch else a.input.read_bytes()
    stats=qc(raw)
    if stats['valid_numeric_rows']==0:raise ValueError('Acquisition has zero usable numeric measurements')
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'source.csv').write_bytes(raw)
    (a.out/'qc.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:stats[k] for k in ('classification','total_data_rows','valid_numeric_rows','rejected_rows','times_utc','original_sha256','model_ingestion')},indent=2))
if __name__=='__main__':main()
