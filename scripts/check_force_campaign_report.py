"""Deterministic source-identity and arithmetic-consistency check; no third-party data required."""
from pathlib import Path
import csv
import json

ROOT=Path(__file__).resolve().parents[1]


def validate(report_path=None, daily_path=None):
    report_path=Path(report_path or ROOT/'reports/FORCE-CAMPAIGN-QA-001.json')
    daily_path=Path(daily_path or ROOT/'research/observations/FORCE_CAMPAIGN_DAILY_QA_2018.csv')
    r=json.loads(report_path.read_text(encoding='utf-8'))
    assert r['id']=='FORCE-CAMPAIGN-QA-001'
    assert r['source_approved_velocity_records']==0
    assert r['model_ingestion'].startswith('BLOCKED_')
    assert r['source_sha256']['currents.nc']=='be8acb1802786a0db7f5c2952e4554fc25f03508550b7478a19a2f47d86864e2'
    assert r['source_sha256']['waves.nc']=='d538b46f4b702382386721a43d39ec253f281f48522a377bf456b5d3373001ee'
    assert r['time_bursts']==5265 and r['cell_count']==50
    assert r['velocity_numeric_triplets']==r['time_bursts']*r['cell_count']==263250
    assert r['total_all_component_exact_zero']==97911
    assert r['preterminal_pressure_screen_bursts']==5175
    assert len(r['preterminal_pressure_screen_ranges_no_zero_m'])==26
    assert len(r['preterminal_pressure_screen_ranges_always_zero_m'])==12
    assert r['wave_maximum_period_fill_minus9_count']==431
    assert len(r['vertical_cell_summary'])==50
    with daily_path.open(encoding='utf-8',newline='') as f:days=list(csv.DictReader(f))
    assert len(days)==56==len(r['daily_arithmetic_summary'])
    assert sum(int(d['bursts']) for d in days)==r['time_bursts']
    assert sum(int(d['triplets_exact_zero']) for d in days)==r['total_all_component_exact_zero']
    assert sum(int(d['wave_period_fill_minus9_count']) for d in days)==431
    assert all(d['date_utc']==s['date_utc'] for d,s in zip(days,r['daily_arithmetic_summary']))
    assert r['prior_72h_crosscheck']['compared_triplets']==14400
    return r


if __name__=='__main__':
    r=validate()
    print(f"Verified immutable full-campaign evidence: {r['time_bursts']} bursts, {r['cell_count']} relative range cells; model access {r['model_ingestion']}")
