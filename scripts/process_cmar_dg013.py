"""Reproduce source-pinned CMAR Long Beach DG013 wave/current-speed observations.

Gross-range Pass is NOT native beam-level QC or proof of rotor-depth inflow.
"""
import csv,hashlib,io,json,argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean
from zipfile import ZipFile
SHA='27bd18b64f2c71fb1502a663ede62f1d04b47a019dbb2fc5191190e028493ee8'
FLAGS=['grossrange_flag_sea_water_speed','grossrange_flag_sea_water_to_direction','grossrange_flag_sea_surface_wave_significant_height','grossrange_flag_sensor_depth_below_surface']
COLS=['time','latitude','longitude','station','deployment_id','sea_water_speed','sea_water_to_direction','sea_surface_wave_significant_height','sensor_depth_below_surface',*FLAGS]
def process(archive,out):
    with ZipFile(archive) as z:
        if set(z.namelist())!={'cmar_dg013.csv','manifest.json'}:raise ValueError('Wrong archive members')
        raw=z.read('cmar_dg013.csv');source=json.loads(z.read('manifest.json'))
    if len(raw)!=60480 or hashlib.sha256(raw).hexdigest()!=SHA or source.get('sha256')!=SHA:raise ValueError('Source identity mismatch')
    rdr=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    if not set(COLS).issubset(rdr.fieldnames or []):raise ValueError('Unexpected columns')
    rows=list(rdr)
    if rows and rows[0]['time']=='UTC':rows=rows[1:]
    if len(rows)!=531:raise ValueError('Unexpected observation count')
    coords={};flagcounts={k:Counter() for k in FLAGS};times=[];speed=[];waves=[]
    out=Path(out);out.mkdir(parents=True,exist_ok=True);p=out/'CMAR_DIGBY_DG013_2022_QA.csv'
    with p.open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(COLS+['quality_scope','model_eligible'])
        for r in rows:
            if r['waterbody']!='St. Marys Bay' or r['station']!='Long Beach' or r['deployment_id']!='DG013':raise ValueError('Station identity')
            c=(float(r['latitude']),float(r['longitude']))
            if c!=(44.40473,-66.1627):raise ValueError('Coordinates changed')
            t=datetime.fromisoformat(r['time'].replace('Z','+00:00'))
            if t.tzinfo is None:raise ValueError('UTC not supplied')
            times.append(t);speed.append(float(r['sea_water_speed']));waves.append(float(r['sea_surface_wave_significant_height']))
            for k in FLAGS:
                if r[k] not in ('Pass','Fail','Suspect/Of Interest','Not Evaluated'):raise ValueError('Unknown quality state')
                flagcounts[k][r[k]]+=1
            writer.writerow([r[k] for k in COLS]+['CMAR_GROSS_RANGE_ONLY',0])
    if any(b<=a for a,b in zip(times,times[1:])):raise ValueError('Nonincreasing times')
    gaps=Counter(int((b-a).total_seconds()) for a,b in zip(times,times[1:]))
    m={'id':'CMAR-DG013-QA-001','status':'OBSERVED_PROCESSED_GROSS_RANGE_QC_ONLY',
       'source_sha256':SHA,'source_bytes':len(raw),'derived_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
       'source_url':source['source_url'],'metadata_url':'https://cioosatlantic.ca/erddap/info/7iig-p4yk/index.html',
       'license':'Nova Scotia Open Government Licence — attribute Centre for Marine Applied Research (CMAR)',
       'station':'Long Beach','waterbody':'St. Marys Bay','deployment_id':'DG013','lat':44.40473,'lon':-66.1627,
       'n_records':len(rows),'utc_start':rows[0]['time'],'utc_end':rows[-1]['time'],
       'cadence_seconds':{str(k):v for k,v in sorted(gaps.items())},
       'publisher_gross_range_flags':{k:dict(v) for k,v in flagcounts.items()},
       'sea_water_speed_m_s':{'min':min(speed),'max':max(speed),'arithmetic_mean':round(mean(speed),8)},
       'significant_wave_height_m':{'min':min(waves),'max':max(waves),'arithmetic_mean':round(mean(waves),8)},
       'source_type':'CMAR Wave dataset includes a sensor sea_water_speed, NOT a 3D current profile',
       'native_sensor_qc':'UNVERIFIED','model_eligible_rows':0,'turbine_inflow_validated':False}
    (out/'CMAR_DIGBY_DG013_2022_QA.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    return m
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    print(json.dumps(process(a.archive,a.out),indent=2))
