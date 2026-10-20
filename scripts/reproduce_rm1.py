"""Independently check mechanical shaft power from the printed RM1 Appendix A.

Data are transcribed from Hill et al., 2014, Sandia RM1 experimental report,
printed page 20 (PDF page index 19), limited to seven performance/inflow columns.
This is NOT a predictive flow model or raw-signal reprocessing. The table reports
no measured thrust. The report text and its table differ slightly in stated
left-rotor peak CP; do not erase this conflict.
"""
from collections import Counter
import csv
import hashlib
import json
from math import isfinite, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'research/benchmarks/RM1_2014_APPENDIX_A_SELECTED.csv'
OUTPUT = ROOT / 'reports/RM1-OBS-001.json'
SOURCE_URL = 'https://www.sandia.gov/app/uploads/sites/273/dlm_uploads/RM1_Experimental_Results_Report_Final.pdf'


def reproduce(path=INPUT):
    path = Path(path)
    with path.open(encoding='utf8', newline='') as fp:
        rows = list(csv.DictReader(fp))
    if Counter(r['rotor'] for r in rows) != {'left': 16, 'right': 16}:
        raise ValueError('Expected 16 printed Appendix A operating points for each rotor')
    data = []
    for source in rows:
        rotor=source['rotor']
        point = {'rotor':rotor}
        for column in ('rpm','tsr','torque_nm','mechanical_power_w','reported_cp','approach_u_m_s'):
            point[column] = float(source[column])
            if not isfinite(point[column]) or point[column] <= 0:
                raise ValueError('Invalid RM1 measured value '+column)
        point['power_from_mean_torque_w'] = round(point['torque_nm'] * point['rpm'] * 2*pi/60,4)
        point['shaft_power_difference_w'] = round(point['power_from_mean_torque_w']-point['mechanical_power_w'],4)
        # Published RPM is nominal and averaging instantaneous torque x speed
        # does not necessarily equal product of rounded means. This is only a
        # gross transcription sanity gate, NOT an exact measurement identity.
        if abs(point['shaft_power_difference_w']) > max(0.05,0.01*point['mechanical_power_w']):
            raise ValueError(f'Shaft power mismatch > 1%/0.05 W at {rotor} {point["rpm"]}')
        if not 0<point['reported_cp']<1.0:
            raise ValueError('Reported Cp out of expected range for this experiment')
        data.append(point)
    by_rotor={}
    for rotor in ('right','left'):
        points=[p for p in data if p['rotor']==rotor]
        peak=max(p['reported_cp'] for p in points)
        by_rotor[rotor]={
            'tabulated_max_cp':peak,
            'source_points_at_max':[{'rpm':p['rpm'],'tsr':p['tsr']} for p in points if p['reported_cp']==peak],
            'n_points':len(points),
            'maximum_abs_shaft_power_difference_w':max(abs(p['shaft_power_difference_w']) for p in points),
            'maximum_relative_shaft_power_difference_percent':round(100*max(abs(p['shaft_power_difference_w'])/p['mechanical_power_w'] for p in points),4)
        }
    return {
        'id':'RM1-OBS-001',
        'classification':'PUBLISHED_TABLE_REPRODUCTION_PLUS_MECHANICAL_IDENTITY_NOT_PREDICTIVE_VALIDATION',
        'source':SOURCE_URL,
        'source_location':'2014 RM1: Experimental Results, Appendix A, printed p.20, PDF page 20 (index 19); setup sections II-III; performance section IV.c.',
        'transcription':'32 tabulated operating points; seven selected columns, printed precision retained; rotor side is separate, never averaged into a single universal Cp curve',
        'source_fixture_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'reference_geometry':{'single_rotor_diameter_m':0.5,'single_rotor_disk_area_m2':'pi*(0.5/2)^2','number_of_rotors':2,'blade_profile':'NACA 4415 scaled test rotor; NOT baseline RM1 full-scale NACA-63(4)-24'},
        'laboratory_environment':{'water_depth_m':1.0,'nominal_hub_speed_m_s':1.05,'water':'Mississippi River freshwater SAFL flume','blockage_uncorrected':True},
        'source_narrative':{'right_cp_approx':0.48,'left_cp_approx':0.43,'tsr_approx':5.1},
        'reported_table':by_rotor,
        'method':'Compute nominal P=mean torque*2*pi*reported RPM/60 from printed means; compare within a coarse 1%/0.05 W gross-transcription tolerance. Small residuals are expected because speed and power can be instantaneous averages and reported RPM is nominal; do not call this a raw-data reproduction. Tabulated Cp is transcribed as reported and is NOT inferred by ratio of averaged power and nominal inflow: averaging and correction conventions require raw signals.',
        'contradictions':['The 2014 narrative/figure states left Cp ~0.43 near TSR 5.1 while Appendix A left table has maxima 0.412 at TSR 4.57 and 5.15; exact difference cannot be resolved from rounded table alone.','The printed report introduction incorrectly labels RM1 as RM2 in one sentence; this test is the RM1 dual axial rotor.'],
        'unverified':['No source raw synchronized torque/velocity data processed','No model calibration/holdout, no predictive hydrodynamic validation','No direct measured thrust: Appendix A Ft and Ct are n/a','No structural blade cyclic load, fatigue or lifecycle evidence','Uncorrected facility blockage and different approach velocities prevent simple RM1-vs-RM2 Cp comparison'],
        'results':data,
    }


def main():
    report=reproduce()
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print('RM1 Appendix A: 32/32 printed runs and nominal mean-shaft-power sanity check; right table peak Cp',report['reported_table']['right']['tabulated_max_cp'],'left',report['reported_table']['left']['tabulated_max_cp'],'narrative mismatch unresolved.')

if __name__=='__main__':main()
