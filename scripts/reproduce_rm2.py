"""Reproduce published *processed* RM2 Cp and CD series (NOT predictive modelling).

Values are rounded to 7 decimal places from upstream table. Upstream repository:
UNH-CORE/RM2-tow-tank, master Git blob 1f284211d5c19593cf753e63727ae62a62356439.
Attribution: Bachant, Wosnik, Gunawan & Neary (2016), CC BY 4.0;
DOI 10.6084/m9.figshare.1373899. Do not infer marine-site applicability.
"""
import csv
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'research/benchmarks/RM2_PERF_1MS_REDUCED.csv'
OUT=ROOT/'reports/RM2-OBS-001.json'
FIELDS=('mean_tsr','mean_cp','mean_cd','mean_tow_speed_m_s','exp_unc_cp','exp_unc_cd')


def reproduce(path=INPUT):
    p=Path(path)
    with p.open(encoding='utf-8',newline='') as f:
        values=[dict(row) for row in csv.DictReader(f)]
    if len(values)!=23 or sorted(int(row['run']) for row in values)!=list(range(23)):
        raise ValueError('RM2 fixture must contain the original 23 run IDs exactly once')
    obs=[]
    for row in values:
        item={'run':int(row['run'])}
        for field in FIELDS: item[field]=float(row[field])
        if not(0 < item['mean_tow_speed_m_s'] < 2 and 0 < item['mean_tsr'] < 10):
            raise ValueError('Suspicious tow speed or TSR')
        if not all(0 <= item[f] < 10 for f in ('mean_cp','mean_cd','exp_unc_cp','exp_unc_cd')):
            raise ValueError('Coefficient/uncertainty outside basic bounds')
        obs.append(item)
    obs.sort(key=lambda r:r['mean_tsr'])
    peak=max(obs,key=lambda r:r['mean_cp'])
    return {
       'id':'RM2-OBS-001',
       'classification':'EXPERIMENTAL_PROCESSED_DATA_REPRODUCTION_NOT_PREDICTIVE_VALIDATION',
       'question':'Reproduce the observed RM2 Cp-versus-tip-speed-ratio and CD series from UNH processed tow tank data.',
       'source':'UNH-CORE/RM2-tow-tank/Data/Processed/Perf-1.0.csv',
       'source_url':'https://github.com/UNH-CORE/RM2-tow-tank/blob/master/Data/Processed/Perf-1.0.csv',
       'source_git_blob_sha':'1f284211d5c19593cf753e63727ae62a62356439',
       'upstream_test_family':'RM2 1:6 model, 1.0 m/s nominal tow speed, freshwater laboratory tow tank',
       'geometry':{'diameter_m':1.075,'height_m':0.8067,'frontal_area_m2':round(1.075*0.8067,8)},
       'performance_reference_area':'D*H projected frontal area; coefficients in upstream processing (verify detailed processing for boundary).',
       'provenance':'Published processed table subset transcribed to seven decimal places from original Git blob; not independently recomputed from ~10 GB raw signals.',
       'license':'CC BY 4.0 source data / attribution Bachant, Wosnik, Gunawan, Neary (2016), DOI 10.6084/m9.figshare.1373899',
       'source_fixture_sha256':sha256(p.read_bytes()).hexdigest(),
       'n_observations':len(obs),
       'peak_observed':peak,
       'data':obs,
       'decisions_supported':['Processed RM2 observed performance is suitable as a benchmark target for a future independent cross-flow model.','Cross-flow cannot be modelled by changing horizontal-axis Cp only.'],
       'not_established':['No predictive model or independent raw-signal recalculation.','The fields exp_unc_cp and exp_unc_cd retain upstream names; no assumption about confidence or percent interpretation.','Not a tidal-site resource prediction, net electrical performance, annual yield, ecological safety or fatigue validation.','Does not generalize to helical, Savonius, oscillating-foil or other converter families.']
    }

def main():
    result=reproduce()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    p=result['peak_observed']
    print(f"Reproduced {result['n_observations']} published processed RM2 observations; observed peak Cp={p['mean_cp']:.7f} at TSR={p['mean_tsr']:.7f} (uncertainty field={p['exp_unc_cp']:.7f}); NOT a predictive validation")
if __name__=='__main__':main()
