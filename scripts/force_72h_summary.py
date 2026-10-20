"""Reproduce pinned SOURCE-LEVEL numerical screening from a zipped FORCE ADCP sample.

The source report lacks native per-cell acoustic quality flags in its public ERDDAP
representation. No source bin is declared scientifically qualified by this script.
Raw CSV is never copied to the repository. Python standard library only.
"""
import argparse
import csv
from collections import defaultdict
from hashlib import sha256
import io
import json
from pathlib import Path
from statistics import correlation, linear_regression
from zipfile import ZipFile

if __package__:
    from .force_long_window import assess, MAX_BYTES
else:
    from force_long_window import assess, MAX_BYTES

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'reports/FORCE-72H-QA-001.json'
EXPECTED_SOURCE_SHA = 'd05f2a1258d9908b04fc7017cdb818ca318ac47c38e6b40244eac8c378ec4c7a'


def reproduce(artifact, expected_sha=EXPECTED_SOURCE_SHA):
    with ZipFile(artifact) as archive:
        if set(archive.namelist()) != {'source.csv', 'qa.json'}:
            raise ValueError('Archive must have exactly source.csv and qa.json')
        if archive.getinfo('source.csv').file_size > MAX_BYTES:
            raise ValueError('Source CSV exceeds bounded byte cap')
        raw = archive.read('source.csv')
        original = json.loads(archive.read('qa.json'))
    checksum = sha256(raw).hexdigest()
    if checksum != expected_sha or original['source_sha256'] != checksum:
        raise ValueError('The original source SHA-256 is not the expected acquisition')
    qa = assess(raw)
    for field in ('parseable_numeric_rows','distinct_time_bursts','exact_all_component_zero_vectors',
                  'range_cells','rejected_rows','all_zero_cells_m','partially_zero_cells_m',
                  'nonzero_throughout_numeric_cells_m'):
        if qa[field] != original[field]:
            raise ValueError('Archived acquisition QA conflicts with independent replay: '+field)
    per_time = defaultdict(list)
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    for row in reader:
        if row['time'] == 'UTC':
            continue
        t = row['time']
        vals = [float(row[k]) for k in ('eastward_sea_water_velocity', 'northward_sea_water_velocity', 'upward_sea_water_velocity')]
        if any(vals):
            per_time[t].append(float(row['cell_range']))
    if len(per_time) != qa['distinct_time_bursts']:
        raise ValueError('An entire burst contains only zero/fill candidates')
    pressure = {}
    for row in csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))):
        if row['time'] == 'UTC':
            continue
        t = row['time']; p = float(row['sea_water_pressure'])
        if t in pressure and abs(p-pressure[t]) > 1e-8:
            raise ValueError('Inconsistent pressure within timestamp')
        pressure[t] = p
    keys = sorted(per_time)
    x = [pressure[t] for t in keys]
    y = [max(per_time[t]) for t in keys]
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        raise ValueError('Correlation is not identifiable for this source sample')
    slope = linear_regression(x, y)
    return {
        'id':'FORCE-72H-QA-001',
        'evidence_class':'MEASURED_SOURCE_ARITHMETIC_QA_NOT_SCIENTIFICALLY_QUALIFIED',
        'repository_source':'https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html',
        'source_request':qa['source_request'],
        'source_sha256':checksum,
        'source_bytes':len(raw),
        'archived_git_actions_run':'https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39482098852',
        'archived_artifact_id':12292085881,
        'source_license':'CC BY 4.0 (attribution FORCE/CIOOS Atlantic)',
        'observed_utc':qa['observed_window_utc'],
        'numeric_qa':{
            k:qa[k] for k in ('total_csv_observation_rows','parseable_numeric_rows','rejected_rows','distinct_time_bursts','range_cells','exact_all_component_zero_vectors','zero_fraction_numeric','all_zero_cells_m','partially_zero_cells_m','nonzero_throughout_numeric_cells_m','nominal_utc_time_step_s','min_max_utc_step_s','pressure_dbar_observed_min_max','reported_cell_size_m_values')
        },
        'pressure_vs_highest_nonzero_range':{
            'n_bursts':len(keys),
            'pearson_correlation':round(correlation(x,y),6),
            'regression_slope_m_per_dbar':round(slope.slope,6),
            'regression_intercept_range_m':round(slope.intercept,6),
            'min_max_highest_nonzero_range_m':[min(y),max(y)],
            'interpretation':'Strong association between pressure and boundary of exact-zero processed vectors; compatible with vertical range clipping, but cannot independently establish source zero/fill convention. Pressure dbar is not an instrument-calibrated sea surface height in metres.'
        },
        'independent_deployment_primary_source':'https://doi.org/10.3389/fmars.2022.851400',
        'verified_deployment_geometry':{
            'device':'upward-looking Nortek Signature 500 on FAST-3',
            'face_elevation_above_seabed_m_reported':0.7,
            'blanking_distance_m_reported':1.0,
            'cell_size_m_reported':1.0,
            'first_cell_center_distance_from_face_m_reported':2.0,
            'public_erddap_first_cell_range_label_m':1.5,
            'critical_mapping_discrepancy':'Peer-reviewed description places first cell center 2 m from transducer, but ERDDAP labels begin 1.5 m; unclear if labels encode different reference point/edge, processing shift or discrepancy. Do not automatically compute absolute bin elevations.'
        },
        'native_qc_missing':['per-beam correlation/amplitude and percent-good','tilt and platform motion','beam sidelobe masks and near-surface signal quality','source-specific meaning of exactly zero vectors','evidence of ERDDAP transformations and declination handling'],
        'spatial_representativeness':'ONE fixed FORCE location and THREE days in April 2018; not spring-neap cycle, season or annual resource; no spatial transfer to test-site shortlist',
        'qualified_current_bins':[],
        'model_ingestion':'BLOCKED_PENDING_NATIVE_BEAM_QC_ZERO_FILL_AND_RANGE_MAPPING',
        'energy_and_load_model_status':'NOT_RUN_ON_MEASURED_FORCEDATA',
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--zip',type=Path,required=True,help='Exact publicly archived one-shot GitHub Actions artifact ZIP')
    p.add_argument('--out',type=Path,default=REPORT)
    a=p.parse_args()
    r=reproduce(a.zip)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8')
    print('Replayed FORCE 72h measurement QA, numeric only; source=',r['source_sha256'],'correlation=',r['pressure_vs_highest_nonzero_range']['pearson_correlation'])

if __name__=='__main__': main()
