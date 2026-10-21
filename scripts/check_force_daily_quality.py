"""Offline fail-closed audit of derived FORCE daily-by-range numerical QA grid."""
from collections import Counter
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GRID=ROOT/'research/observations/FORCE_DAILY_CELL_QUALITY_V1_2018.json'
MANIFEST=ROOT/'research/observations/FORCE_INFLOW_V0_MANIFEST_2018.json'
REPORT=ROOT/'reports/FORCE-CAMPAIGN-QA-001.json'

def check(grid_path=GRID):
    grid=json.loads(Path(grid_path).read_text(encoding='utf8'))
    manifest=json.loads(MANIFEST.read_text(encoding='utf8'))
    report=json.loads(REPORT.read_text(encoding='utf8'))
    if grid['schema']!='FORCE_DAY_RANGE_QA_V1' or grid['evidence_class']!='PROCESSED_OBSERVATION_ARITHMETIC_SCREEN_ONLY':raise ValueError('Changed evidence classification')
    if grid['source_sha256']!=manifest['currents_source_sha256'] or grid['companion_waves_sha256']!=manifest['waves_source_sha256']:raise ValueError('Unverified source data hash')
    if (grid['model_eligible_rows'],grid['scientific_approved_cells'],grid['native_beam_qc'])!=(0,0,'UNAVAILABLE'):raise ValueError('Premature scientific approval')
    if grid['native_qc_fields_present'] or len(grid['native_qc_fields_missing'])<4: raise ValueError('Publisher QC claim changed; review source')
    if grid['documented_nortek_velocity_sentinel_count_in_enu']!=0:raise ValueError('Sentinel claim changed; investigate')
    if grid['all_component_exact_zero_triplets']!=report['total_all_component_exact_zero']:raise ValueError('Raw source zero count mismatch')
    if (grid['n_time'],grid['n_cells'],grid['n_records'],grid['n_days'])!=(5265,50,263250,56):raise ValueError('Grid shape mismatch')
    ranges=grid['range_relative_m']
    if len(ranges)!=50 or sorted(set(ranges))!=ranges:raise ValueError('Missing or duplicate instrument bins')
    dates=set(); totals=Counter();cell_totals={str(r):Counter() for r in ranges}
    by_day={x['date_utc']:x for x in report['daily_arithmetic_summary']}
    for day in grid['daily']:
        d=day['day_utc']
        if d in dates or d not in by_day: raise ValueError('Missing or duplicate day')
        dates.add(d)
        n=int(day['bursts']);t=int(day['terminal_bursts'])
        if n!=by_day[d]['bursts'] or not 0<=t<=n:raise ValueError('Mismatched daily sample count')
        zero=day['suspect_zero_by_cell']; pending=day['pending_by_cell']
        if len(zero)!=50 or len(pending)!=50 or any(a<0 or b<0 or a+b+t!=n for a,b in zip(zero,pending)):
            raise ValueError('Daily cell states do not partition observations')
        totals['SUSPECT_EXACT_ZERO_ALL_COMPONENTS']+=sum(zero)
        totals['PENDING_NATIVE_QC_AND_GEOMETRY']+=sum(pending)
        totals['SUSPECT_LOW_PRESSURE_TRANSITION']+=t*50
        for r,a,b in zip(ranges,zero,pending):
            k=str(r)
            cell_totals[k]['SUSPECT_EXACT_ZERO_ALL_COMPONENTS']+=a
            cell_totals[k]['PENDING_NATIVE_QC_AND_GEOMETRY']+=b
            cell_totals[k]['SUSPECT_LOW_PRESSURE_TRANSITION']+=t
    if set(by_day)!=dates or dict(totals)!=grid['counts'] or totals!=Counter(manifest['counts']):raise ValueError('Day/source classification parity failure')
    for key,counts in cell_totals.items():
        if counts!=Counter(manifest['per_cell'][key]):raise ValueError('Cell/source classification parity failure: '+key)
    return True

if __name__=='__main__':
    check();print('PASS: 56 × 50 source-pinned daily/cell quality classes; zero eligible for turbine modelling')
