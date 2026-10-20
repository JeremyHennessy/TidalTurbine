"""Descriptive RM2 same-rig Cp-versus-mean-drag tradeoff, not a design solver.

Source fixture and provenance: reproduce_rm2.py (UNH Bachant et al. 2016).
Compare *observed mean coefficients* at nominal 1 m/s for one 1:6 cross-flow
rotor. Cd is streamwise apparatus-corrected rotor drag, not blade fatigue, bending
moment, acoustic output, biological impact, or field structural life.
"""
from hashlib import sha256
import json
from pathlib import Path
from math import isfinite
if __package__:
    from .reproduce_rm2 import INPUT, reproduce
else:
    from reproduce_rm2 import INPUT, reproduce

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'reports/RM2-TRADEOFF-001.json'
RHO_KG_M3=1000.0  # Source's nominal freshwater density, not seawater
DIAMETER_M=1.075
HEIGHT_M=0.8067
NOMINAL_U_M_S=1.0


def pareto_points(points):
    """Rows not dominated by another row with >= Cp AND <= Cd.

    Treats coefficients as exact *reported point estimates*. Uncertainty is
    preserved independently but NOT propagated into statistical dominance.
    """
    return [p for p in points if not any(
        (q['mean_cp']>=p['mean_cp'] and q['mean_cd']<=p['mean_cd'])
        and (q['mean_cp']>p['mean_cp'] or q['mean_cd']<p['mean_cd'])
        for q in points if q['run'] != p['run'])]


def generate():
    source=reproduce()
    data=source['data']
    # All are from one 1.0 m/s nominal tow speed matrix; not extrapolated.
    assert len(data)==23 and all(isfinite(p['mean_cp']) and isfinite(p['mean_cd']) for p in data)
    peak=max(data,key=lambda p:p['mean_cp'])
    area=DIAMETER_M*HEIGHT_M
    flux=0.5*RHO_KG_M3*area*NOMINAL_U_M_S**3
    dragref=0.5*RHO_KG_M3*area*NOMINAL_U_M_S**2
    viable=[]
    for frac in (0.9,0.95,0.98,0.99):
        choices=[p for p in data if p['mean_cp']>=frac*peak['mean_cp']]
        picked=min(choices,key=lambda p:(p['mean_cd'],-p['mean_cp']))
        viable.append({
            'minimum_fraction_of_peak_mechanical_cp':frac,
            'selected_source_run':picked['run'],
            'observed_tsr':picked['mean_tsr'],
            'observed_cp':picked['mean_cp'],
            'observed_cd':picked['mean_cd'],
            'reported_exp_unc_cp':picked['exp_unc_cp'],
            'reported_exp_unc_cd':picked['exp_unc_cd'],
            'mechanical_cp_decrease_percent':round(100*(1-picked['mean_cp']/peak['mean_cp']),4),
            'mean_streamwise_cd_decrease_percent':round(100*(1-picked['mean_cd']/peak['mean_cd']),4),
            'nominal_mechanical_power_w':round(flux*picked['mean_cp'],4),
            'nominal_mean_rotor_drag_n':round(dragref*picked['mean_cd'],4),
        })
    # Show same-rotor operational candidates; do not score or generalize.
    return {
        'id':'RM2-TRADEOFF-001',
        'classification':'DESCRIPTIVE_MEASURED_PROCESSED_COEFFICIENT_COMPARISON',
        'question':'At nominally equal 1 m/s laboratory inflow, how much observed mean rotor drag coefficient changes when operating below peak Cp at different measured tip-speed ratios?',
        'hypothesis':'A lower tip speed ratio might reduce mean axial drag at the cost of shaft mechanical Cp; this cannot establish fatigue or lifetime benefit.',
        'baseline':{'run':peak['run'],'tsr':peak['mean_tsr'],'cp':peak['mean_cp'],'cd':peak['mean_cd'],
                    'reported_exp_unc_cp':peak['exp_unc_cp'],'reported_exp_unc_cd':peak['exp_unc_cd'],
                    'nominal_mechanical_power_w':round(flux*peak['mean_cp'],4),
                    'nominal_mean_rotor_drag_n':round(dragref*peak['mean_cd'],4)},
        'source':source['source_url'],
        'source_git_blob_sha':source['source_git_blob_sha'],
        'source_fixture_sha256':sha256(INPUT.read_bytes()).hexdigest(),
        'doi':'10.1371/journal.pone.0163799',
        'evidence':'Same RM2 one-sixth-scale cross-flow rotor, previously processed laboratory towing runs; not new independent measurements.',
        'references':{'diameter_m':DIAMETER_M,'height_m':HEIGHT_M,'projected_frontal_area_m2':round(area,8),
                      'freshwater_density_kg_m3':RHO_KG_M3,'nominal_inflow_speed_m_s':NOMINAL_U_M_S,
                      'unit_factors':'P_ref = 0.5*rho*A*U^3 [W]; F_ref=0.5*rho*A*U^2 [N]'},
        'selection_rule':'Select lowest observed point-estimate mean CD meeting each fixed descriptive Cp fraction of peak, chosen during this analysis (not prospectively preregistered) (same rig and nominal speed). No statistical significance or optimized controller claimed.',
        'descriptive_nondominated_run_ids':[p['run'] for p in pareto_points(data)],
        'within_lab_mechanical_power_budgets':viable,
        'source_uncertainty':'Upstream exp_unc columns retained as reported. Published methodology describes expanded 95% intervals, but no covariance-aware significance or independent recalculation made here.',
        'validation_status':'REPRODUCTION_OF_PUBLISHED_PROCESSED_MEANS_ONLY',
        'missing':['Cyclic blade loads and bending moments','Torque ripple and fatigue spectrum',
                   'Actual control energy required to hold TSR in fluctuating currents',
                   'Paired uncertainty/covariance and repeated-condition independent replicates',
                   'Hydrodynamic blockage and Reynolds scaling, seawater and field turbulence',
                   'Maintenance and environmental evidence'],
        'decision':'Prioritize measured cyclic loads and power-vs-drag controls in issue #4; do not assign fatigue, availability, LCOE or site-specific energy gains.'
    }


def main():
    report=generate()
    OUTPUT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print('RM2 descriptive operating-point comparison:',len(report['within_lab_mechanical_power_budgets']),'thresholds; no structural or fatigue inference')
    for p in report['within_lab_mechanical_power_budgets']:
        print(' ',p['minimum_fraction_of_peak_mechanical_cp'],'run',p['selected_source_run'],'Cp cost',p['mechanical_cp_decrease_percent'],'%','Cd change',p['mean_streamwise_cd_decrease_percent'],'%')

if __name__=='__main__':main()
