"""Acquire a bounded FORCE ADCP window and produce strictly *provisional* numeric QC.

No source-provided beam quality/correlation, transform calibration, instrument-head
height or source-specific zero/fill convention is available in the ERDDAP table.
This script NEVER certifies any velocity as a valid rotor inflow profile.
Default is offline: --input existing.csv; --fetch makes an explicit network call.
Do not commit raw CSV. Python standard library only.
"""
from collections import Counter, defaultdict
import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from math import hypot, isfinite
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE='https://cioosatlantic.ca/erddap/tabledap/FORCE_Mar2018_ADCP_Currents.csv'
FIELDS=['time','latitude','longitude','cell_range','eastward_sea_water_velocity','northward_sea_water_velocity','upward_sea_water_velocity','sea_water_pressure','cell_size']
REQUIRED=FIELDS[:7]
START='2018-04-01T00:00:00Z'
END='2018-04-04T00:00:00Z'
MAX_BYTES=12*1024*1024
SOURCE_INFO='https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html'
PROTOCOL_SOURCE='https://oera.ca/sites/default/files/2020-04/FISH%20FINDER%20Final%20Report%2031-03-2020_0.pdf'


def query_url(start=START,end=END):
    a=datetime.fromisoformat(start.replace('Z','+00:00'))
    b=datetime.fromisoformat(end.replace('Z','+00:00'))
    if a.tzinfo is None or b.tzinfo is None or b<=a or (b-a).total_seconds()>72*3600 or a.year!=2018 or b.year!=2018:
        raise ValueError('Refuse windows over 72 h, reversed, unzoned or outside 2018')
    return BASE+'?'+','.join(FIELDS)+'&time%3E='+quote(start,safe=':-')+'&time%3C='+quote(end,safe=':-')


def acquire(opener=urlopen):
    req=Request(query_url(),headers={'User-Agent':'TidalTurbine-noncommercial-ocean-QA/0.4'})
    out=bytearray()
    with opener(req,timeout=90) as response:
        while True:
            chunk=response.read(min(131072,MAX_BYTES+1-len(out)))
            if not chunk:break
            out+=chunk
            if len(out)>MAX_BYTES:raise ValueError('Downloaded CSV exceeds safety size cap')
    if not out.startswith(b'time,'):
        raise ValueError('Unexpected response; not an ERDDAP tabledap CSV')
    return bytes(out)


def assess(raw,start=START,end=END):
    if len(raw)>MAX_BYTES:raise ValueError('CSV exceeds size cap')
    digest=sha256(raw).hexdigest()
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    if not reader.fieldnames or any(f not in reader.fieldnames for f in REQUIRED):raise ValueError('Missing required FORCE columns')
    count=0;bad=Counter();zero=Counter();per_cell=Counter();per_time=defaultdict(list);seen=set();pressure_by_time=defaultdict(list);cell_sizes=set();lat=set();lon=set()
    starts=datetime.fromisoformat(start.replace('Z','+00:00'));ends=datetime.fromisoformat(end.replace('Z','+00:00'))
    for r in reader:
        if r['time'].strip().lower() in ('utc','iso8601'):continue
        count+=1
        try:
            t=datetime.fromisoformat(r['time'].replace('Z','+00:00'))
            if t.tzinfo is None or not(starts<=t<=ends):raise ValueError('invalid timestamp')
            c=float(r['cell_range']);y=float(r['latitude']);x=float(r['longitude'])
            u=float(r['eastward_sea_water_velocity']);v=float(r['northward_sea_water_velocity']);w=float(r['upward_sea_water_velocity'])
            if not all(map(isfinite,(c,x,y,u,v,w))) or not (0<c<100 and -90<=y<=90 and -180<=x<=180):raise ValueError('nonfinite/range')
            # 8 m/s is a deliberately broad arithmetic plausibility test, NOT a speed rating.
            if max(abs(u),abs(v),abs(w))>8:raise ValueError('unresolved large velocity')
            key=(t,c)
            if key in seen:raise ValueError('duplicate UTC timestamp/range')
            seen.add(key);per_cell[c]+=1;per_time[t].append((c,u,v,w));lat.add(y);lon.add(x)
            if u==v==w==0:zero[c]+=1
            pressure=r.get('sea_water_pressure','')
            if pressure and pressure.strip().lower()!='nan':
                pressure=float(pressure)
                if isfinite(pressure):pressure_by_time[t].append(pressure)
            size=r.get('cell_size','')
            if size and size.strip().lower()!='nan':
                size=float(size)
                if isfinite(size):cell_sizes.add(size)
        except (ValueError,KeyError,TypeError) as e:
            bad[str(e)]+=1
    if not per_time:raise ValueError('No parseable observed records')
    times=sorted(per_time)
    differences=[(b-a).total_seconds() for a,b in zip(times,times[1:])]
    ranges=sorted(per_cell)
    zero_count=sum(zero.values())
    status={}
    for c in ranges:
        z=zero[c];n=per_cell[c]
        status[str(c)]={'numeric_records':n,'exact_zero_triples':z,'fraction_exact_zero':round(z/n,5),
            'classification':'ALL_ZERO_SUSPECT' if z==n else ('PARTIALLY_ZERO_SUSPECT' if z else 'NONZERO_NUMERIC_CANDIDATE_NOT_VALIDATED')}
    nonzero_upper=[]
    for t in times:
        valid_range=[c for c,u,v,w in per_time[t] if u!=0 or v!=0 or w!=0]
        nonzero_upper.append({'utc':t.isoformat().replace('+00:00','Z'),'highest_nonzero_range_m':max(valid_range) if valid_range else None,'zero_rows':len(per_time[t])-len(valid_range)})
    pressure_vals=[v for values in pressure_by_time.values() for v in values]
    return {
        'id':'FORCE-MULTIDAY-QA-001','status':'NUMERICALLY_SCREENED_OBSERVATIONS_NOT_QUALIFIED_FOR_TURBINE_MODEL',
        'source_dataset':SOURCE_INFO,'methodology_reference':PROTOCOL_SOURCE,
        'source_request':query_url(start,end),'source_sha256':digest,'source_bytes':len(raw),
        'requested_window_utc':[start,end],
        'observed_window_utc':[times[0].isoformat(),times[-1].isoformat()],
        'total_csv_observation_rows':count,'parseable_numeric_rows':sum(per_cell.values()),'rejected_rows':sum(bad.values()),'rejection_reasons':dict(bad),
        'distinct_time_bursts':len(times),'range_cells':len(ranges),
        'exact_all_component_zero_vectors':zero_count,'zero_fraction_numeric':round(zero_count/sum(per_cell.values()),6),
        'all_zero_cells_m':[c for c in ranges if zero[c]==per_cell[c]],
        'partially_zero_cells_m':[c for c in ranges if 0<zero[c]<per_cell[c]],
        'nonzero_throughout_numeric_cells_m':[c for c in ranges if not zero[c]],
        'nominal_utc_time_step_s':Counter(differences).most_common(1)[0][0] if differences else None,
        'min_max_utc_step_s':[min(differences),max(differences)] if differences else None,
        'rows_per_timestamp_range':[min(len(per_time[t]) for t in times),max(len(per_time[t]) for t in times)],
        'latitude_deg_north':sorted(lat),'longitude_deg_east':sorted(lon),
        'pressure_dbar_observed_min_max':[min(pressure_vals),max(pressure_vals)] if pressure_vals else None,
        'reported_cell_size_m_values':sorted(cell_sizes),
        'pressure_field_in_source_csv':'sea_water_pressure' in reader.fieldnames,
        'cell_size_field_in_source_csv':'cell_size' in reader.fieldnames,
        'range_cell_status':status,'observed_upper_nonzero_range_per_timestamp':nonzero_upper,
        'instrument':'Nortek Signature 500, serial 100258 identified in dataset; upward-facing FAST3 seabed platform described by FORCE/OERA report, sec. 3.2.2',
        'acquisition_provenance':'FORCE / CIOOS Atlantic ERDDAP CC BY 4.0; 2018-Mar-to-May dataset, processed product with unspecified invalid-zero convention',
        'known_processing_context':'OERA/FORCE report sec. 3.4.1: converted original Nortek ad2cp with Signature Deployment v3.4.17.0, averaged 5-min bursts, omitted upper 10% water column from their analyses to avoid side-lobes, corrected original SDU direction for -17.22-degree magnetic declination. DO NOT apply another heading correction blindly to ERDDAP ENU.',
        'scientific_restrictions':['Instrument ADCP transducer height above bed unspecified: reported cell_range is transducer-relative, not absolute water depth.','Per-cell beam correlation, tilt/heading quality, pressure-datum, near-surface sidelobe flag and explicit zero/fill encoding not provided in tabledap product.','NONZERO_NUMERIC_CANDIDATE means only parsed, not scientifically accepted water column.','Pressure is measured dbar, not automatically geodetic sea level or depth without additional assumptions and calibration.','Even a 72-hour sampled interval is insufficient for spring-neap, seasonal or extreme-load characterization.','NO values may be used as engineering-grade inflow or energy forecast until masks, geometries and publisher QC are verified.'],
        'model_ingestion':'BLOCKED_PENDING_NATIVE_QUALITY_METADATA_AND_VERIFIED_WATER_COLUMN',
        'raw_data_in_git':False,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fetch',action='store_true')
    p.add_argument('--input',type=Path)
    p.add_argument('--out',type=Path,default=Path('data/local/force_multiday'))
    args=p.parse_args()
    if args.fetch==bool(args.input):p.error('Choose --fetch or --input')
    raw=acquire() if args.fetch else args.input.read_bytes()
    stat=assess(raw)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'source.csv').write_bytes(raw)
    (args.out/'qa.json').write_text(json.dumps(stat,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:stat[k] for k in ('source_sha256','source_bytes','parseable_numeric_rows','distinct_time_bursts','exact_all_component_zero_vectors','all_zero_cells_m','model_ingestion')},indent=2))

if __name__=='__main__':main()
