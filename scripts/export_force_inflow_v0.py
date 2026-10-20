"""FORCE 2018 NetCDF: versioned numeric QA flags, NEVER model-eligible inflow.

Optional numpy/h5py required; use source archive from Actions 39484948868.
"""
import argparse,csv,gzip,hashlib,io,json
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from datetime import datetime,timezone
import h5py,numpy as np
CURRENT_SHA='be8acb1802786a0db7f5c2952e4554fc25f03508550b7478a19a2f47d86864e2'
WAVE_SHA='d538b46f4b702382386721a43d39ec253f281f48522a377bf456b5d3373001ee'
VERSION='FORCE_INFLOW_QA_V0_20261020'
PENDING='PENDING_NATIVE_QC_AND_GEOMETRY'
ZERO='SUSPECT_EXACT_ZERO_ALL_COMPONENTS'
LOW='SUSPECT_LOW_PRESSURE_TRANSITION'
MISSING='MISSING_NONFINITE'
HEAD=['time_utc','latitude_deg_n','longitude_deg_e','cell_range_m_from_transducer','eastward_m_s_unapproved','northward_m_s_unapproved','upward_m_s_unapproved','pressure_dbar','quality_state','native_sensor_qc','cell_centre_mapping','model_eligible']
def flag(u,v,w,pressure):
    if not all(np.isfinite(x) for x in (u,v,w,pressure)):return MISSING
    if pressure<20:return LOW  # analyst screen only; not manufacturer QC
    if u==v==w==0:return ZERO
    return PENDING

def export(archive,out):
    with ZipFile(archive) as z:
        if set(z.namelist())!={'currents.nc','waves.nc','manifest.json'}:raise ValueError('Unrecognized source set')
        if any(x.file_size>5000000 for x in z.infolist()):raise ValueError('Oversized archive')
        raw=z.read('currents.nc');wave=z.read('waves.nc');source=json.loads(z.read('manifest.json'))
        if len(raw)!=3348741 or hashlib.sha256(raw).hexdigest()!=CURRENT_SHA:raise ValueError('Unpinned current source')
        if len(wave)!=119465 or hashlib.sha256(wave).hexdigest()!=WAVE_SHA:raise ValueError('Unpinned wave source')
        for name,data in (('currents.nc',raw),('waves.nc',wave)):
            if not any(x.get('file')==name and x.get('sha256')==hashlib.sha256(data).hexdigest() for x in source['files']):raise ValueError('Manifest mismatch')
    with h5py.File(io.BytesIO(raw),'r') as nc:
        time=nc['time'][:];ranges=nc['cell_range'][:];pressure=nc['sea_water_pressure'][:]
        u,v,w=[nc[key][:] for key in ['eastward_sea_water_velocity','northward_sea_water_velocity','upward_sea_water_velocity']]
    if time.shape!=(5265,) or ranges.shape!=(50,) or any(x.shape!=(50,5265) for x in (u,v,w)) or pressure.shape!=(5265,):raise ValueError('Source shape drift')
    if not (np.isfinite(time).all() and np.all(np.diff(time)>0) and np.all(np.diff(ranges)>0)):raise ValueError('Axes invalid')
    out=Path(out);out.mkdir(parents=True,exist_ok=True);destination=out/'FORCE_INFLOW_V0_ALL_FLAGGED.csv.gz'
    counts=Counter();cells={f'{r:.1f}':Counter() for r in ranges}
    with destination.open('wb') as fp,gzip.GzipFile(filename='',fileobj=fp,mode='wb',mtime=0,compresslevel=9) as gz,io.TextIOWrapper(gz,encoding='utf8',newline='') as txt:
        writer=csv.writer(txt,lineterminator='\n');writer.writerow(HEAD)
        for j,t in enumerate(time):
            stamp=datetime.fromtimestamp(float(t),timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
            for i,r in enumerate(ranges):
                vals=[float(a[i,j]) for a in (u,v,w)];state=flag(*vals,float(pressure[j]))
                data=[f'{v:.8g}' for v in vals] if state==PENDING else ['','','']
                writer.writerow([stamp,'45.3631389','-64.4274722',f'{r:.1f}',*data,f'{float(pressure[j]):.8g}',state,'UNAVAILABLE','1.5_vs_2m_UNRESOLVED',0])
                counts[state]+=1;cells[f'{r:.1f}'][state]+=1
    compressed=destination.read_bytes()
    m={'schema_version':VERSION,'records':sum(counts.values()),'n_time':len(time),'n_cells':len(ranges),
       'counts':dict(counts),'per_cell':{k:dict(v) for k,v in cells.items()},
       'currents_source_sha256':CURRENT_SHA,'waves_source_sha256':WAVE_SHA,
       'source_license':'CC BY 4.0; FORCE via CIOOS Atlantic',
       'source_url':'https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html',
       'csv_gzip_sha256':hashlib.sha256(compressed).hexdigest(),
       'csv_logical_sha256':hashlib.sha256(gzip.decompress(compressed)).hexdigest(),
       'source_cell_range':'instrument-relative m, NOT bed elevation',
       'zero_rule':'zero triplets masked as suspect, NEVER interpreted as slack',
       'pressure_rule':'pressure <20 dbar is analyst screen, NOT source-native QC',
       'science_approved_cells':0,'model_eligible_rows':0,'model_ingestion':'BLOCKED_PUBLISHER_BEAM_QC_AND_GEOMETRY_UNAVAILABLE'}
    if m['records']!=263250:raise ValueError('Count mismatch')
    (out/'FORCE_INFLOW_V0_MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    return m
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();m=export(args.archive,args.out)
    print(json.dumps({k:m[k] for k in ('records','counts','model_eligible_rows','csv_logical_sha256')},indent=2))
