"""Compare published RM2 within-run coefficient variability (not blade fatigue).

This is a curated, explicitly attributed six-run subset of Bachant et al.'s
processed 1.0 m/s tow-tank table, not a raw-torque data reduction.
"""
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'research/benchmarks/RM2_1MS_VARIABILITY_SELECTED.csv'
OUT=ROOT/'reports/RM2-VARIABILITY-001.json'
FIELDS=('mean_tsr','mean_cp','mean_cd','std_cp','std_cd','std_cp_per_rev','std_cd_per_rev','exp_unc_cp','exp_unc_cd')

def summarize(path=SRC):
    path=Path(path)
    with path.open(encoding='utf8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    if sorted(int(r['run']) for r in rows)!=list(range(9,15)):raise ValueError('Six unique RM2 source runs 9-14 required')
    data=[]
    for r in rows:
        x={'run':int(r['run']),'n_revs':int(r['n_revs'])}
        for field in FIELDS:
            x[field]=float(r[field])
            if not 0 <= x[field] < 10 or not __import__('math').isfinite(x[field]):
                raise ValueError('Out-of-range published coefficient statistic: '+field)
        if x['n_revs']<3:raise ValueError('Too few revolutions')
        data.append(x)
    a=next(r for r in data if r['run']==12)
    b=next(r for r in data if r['run']==10)
    percent=lambda f:round(100*(b[f]/a[f]-1),4)
    return {
        'id':'RM2-VARIABILITY-001','evidence_class':'DESCRIPTIVE_PUBLISHED_PROCESSED_DATA_NOT_CYCLIC_LOAD_VALIDATION',
        'source':'https://github.com/UNH-CORE/RM2-tow-tank/blob/master/Data/Processed/Perf-1.0.csv',
        'upstream_source_blob_sha':'1f284211d5c19593cf753e63727ae62a62356439',
        'upstream_method':'https://github.com/UNH-CORE/RM2-tow-tank/blob/master/pyrm2tt/processing.py (calc_perf_stats and calc_perf_per_rev)',
        'fixture_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'source_attribution':'Bachant, Wosnik, Gunawan, Neary (2016), CC BY 4.0 source data, doi:10.6084/m9.figshare.1373899',
        'definition':'std_cp and std_cd are spread of instantaneous derived coefficients over trimmed tow; std_cp_per_rev and std_cd_per_rev are between-revolution standard deviations of revolution MEANS. Neither yields instantaneous blade-root bending nor within-cycle torque spectrum.',
        'baseline_run_12':a,'alternative_run_10':b,
        'descriptive_percent_change_candidate_vs_baseline':{k:percent(k) for k in ('mean_cp','mean_cd','std_cp','std_cd','std_cp_per_rev','std_cd_per_rev')},
        'source_rows':data,
        'uncertainty':'Only nine or ten complete revolutions in these runs. No paired covariance, frequency spectrum, independent replicate significance or material fatigue damage calculated.',
        'decision':'Request simultaneous torque-phase, blade-bending, strut and actuator load traces before claiming load benefit; tentative operating-point trend is worth testing but not validated.',
        'excluded_conclusions':['No proof of reduced blade structural fatigue','No source raw instantaneous signal reprocessing','No improvement in turbine lifetime energy or maintenance','No extrapolation of Cp/Cd from freshwater tow tank to high-turbulence Fundy'],
    }

def main():
    d=summarize();OUT.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8')
    print('RM2 same-run coefficient statistics: source runs 10 vs 12; not a fatigue model',d['descriptive_percent_change_candidate_vs_baseline'])
if __name__=='__main__':main()
