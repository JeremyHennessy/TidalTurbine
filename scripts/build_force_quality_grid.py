"""Source-pinned FORCE time/range arithmetic *quality-state* grid (not native QC).

No velocity data nor estimated hydrodynamic power is written into the source tree.
All reported cells remain INELIGIBLE as turbine model inflow until native beam QC and
geometry/producer zero-fill decoding are independently documented.
"""
from collections import Counter
from datetime import datetime, timezone
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
from zipfile import ZipFile

import h5py
import numpy as np

from scripts.export_force_inflow_v0 import CURRENT_SHA, WAVE_SHA

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'research/observations/FORCE_DAILY_CELL_QUALITY_V1_2018.json'
PENDING = 'PENDING_NATIVE_QC_AND_GEOMETRY'
ZERO = 'SUSPECT_EXACT_ZERO_ALL_COMPONENTS'
TERMINAL = 'SUSPECT_LOW_PRESSURE_TRANSITION'


def classify_arrays(time, ranges, pressure, u, v, w):
    time, ranges, pressure = map(np.asarray, (time, ranges, pressure))
    u, v, w = (np.asarray(x) for x in (u, v, w))
    if time.ndim != 1 or ranges.ndim != 1 or len(time) == 0 or len(ranges) == 0:
        raise ValueError('Expected 1-D time and range arrays')
    if not np.isfinite(time).all() or not (np.diff(time) > 0).all():
        raise ValueError('Time must be finite, strictly increasing')
    if not np.isfinite(ranges).all() or not (np.diff(ranges) > 0).all():
        raise ValueError('Range labels must be finite, strictly increasing')
    if pressure.shape != time.shape or any(q.shape != (len(ranges),len(time)) for q in (u,v,w)):
        raise ValueError('Pressure/velocity shape inconsistent with sampling axes')
    if not all(np.isfinite(q).all() for q in (pressure,u,v,w)):
        raise ValueError('Nonfinite source requires separate explicit missingness handling')
    zero = (u == 0) & (v == 0) & (w == 0)
    terminal = pressure < 20  # explicitly analyst-selected, NOT native instrument QC
    day_labels = [datetime.fromtimestamp(float(t),timezone.utc).date().isoformat() for t in time]
    unique_days = list(dict.fromkeys(day_labels))
    ranges_m = [float(v) for v in ranges]
    daily=[]; grand=Counter()
    for day in unique_days:
        indices=np.array([i for i,v in enumerate(day_labels) if v==day],dtype=int)
        n=len(indices)
        tmask=terminal[indices]
        zz=zero[:,indices]
        terminal_count=int(np.count_nonzero(tmask))
        # Terminal precedence avoids duplicate assignment of a zero measurement.
        zeros=np.count_nonzero(zz & ~tmask[np.newaxis,:],axis=1).astype(int)
        pending=np.full(len(ranges),n-terminal_count,dtype=int)-zeros
        if np.any(pending < 0): raise ValueError('Count partition underflow')
        rec={'day_utc':day,'bursts':n,'terminal_bursts':terminal_count,
            'suspect_zero_by_cell':[int(v) for v in zeros],
            'pending_by_cell':[int(v) for v in pending]}
        daily.append(rec)
        grand[ZERO]+=int(zeros.sum())
        grand[PENDING]+=int(pending.sum())
        grand[TERMINAL]+=terminal_count*len(ranges)
    total=len(time)*len(ranges)
    if sum(grand.values())!=total:raise AssertionError('Every source cell must have one numeric-QA state')
    return {'schema':'FORCE_DAY_RANGE_QA_V1','evidence_class':'PROCESSED_OBSERVATION_ARITHMETIC_SCREEN_ONLY',
        'source_sha256':CURRENT_SHA,'companion_waves_sha256':WAVE_SHA,
        'range_relative_m':ranges_m, 'n_time':len(time),'n_cells':len(ranges),
        'n_records':total, 'n_days':len(daily), 'counts':dict(grand),
        'pressure_rule':'<20 dbar is an exploratory analyst flag; NOT publisher QC',
        'exact_zero_rule':'all three processed ENU components exactly 0; suspected encoding, NOT slack velocity',
        'native_beam_qc':'UNAVAILABLE', 'cell_centre_geometry':'UNRESOLVED_1p5_VS_2m',
        'model_eligible_rows':0,'scientific_approved_cells':0,
        'daily':daily}


def analyze_archive(archive):
    with ZipFile(archive) as zipfile:
        if set(zipfile.namelist()) != {'currents.nc','waves.nc','manifest.json'}:
            raise ValueError('Unexpected FORCE archive layout')
        if any(x.file_size>5_000_000 for x in zipfile.infolist()):raise ValueError('Oversized archive source member')
        current=zipfile.read('currents.nc')
        wave=zipfile.read('waves.nc')
        manifest=json.loads(zipfile.read('manifest.json'))
        for name, blob, expected in [('currents.nc',current,CURRENT_SHA),('waves.nc',wave,WAVE_SHA)]:
            actual=sha256(blob).hexdigest()
            if actual!=expected or not blob.startswith(b'\x89HDF\r\n\x1a\n'):
                raise ValueError(f'Unpinned source or wrong NetCDF4 format: {name}')
            if not any(x.get('file')==name and x.get('sha256')==expected and x.get('size_bytes')==len(blob)
                      for x in manifest['files']):
                raise ValueError(f'Archived manifest mismatch: {name}')
    with h5py.File(io.BytesIO(current),'r') as ds:
        grid=classify_arrays(ds['time'][:],ds['cell_range'][:],ds['sea_water_pressure'][:],
            ds['eastward_sea_water_velocity'][:],ds['northward_sea_water_velocity'][:],ds['upward_sea_water_velocity'][:])
        required_native=['percent_good','beam_correlation','beam_amplitude','tilt','heading']
        grid['native_qc_fields_present']=[name for name in required_native if name in ds]
        grid['native_qc_fields_missing']=[name for name in required_native if name not in ds]
        raw=[ds[k][:] for k in ('eastward_sea_water_velocity','northward_sea_water_velocity','upward_sea_water_velocity')]
        grid['documented_nortek_velocity_sentinel_count_in_enu']=int(sum(np.count_nonzero(v==-32.767) for v in raw))
        grid['all_component_exact_zero_triplets']=int(np.count_nonzero((raw[0]==0)&(raw[1]==0)&(raw[2]==0)))
    if grid['n_time']!=5265 or grid['n_cells']!=50:raise ValueError('Unexpected FORCE source dimensions')
    if grid['native_qc_fields_present']:raise ValueError('Source schema changed: reassess native quality metadata')
    return grid


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',required=True)
    p.add_argument('--out',type=Path,default=OUTPUT)
    a=p.parse_args()
    result=analyze_archive(a.archive)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n',encoding='utf8')
    print('FORCE daily/range grid:',result['n_days'],'days;',result['n_records'],'cell observations;',
          result['model_eligible_rows'],'model-eligible; source checksums pinned')

if __name__=='__main__':main()
