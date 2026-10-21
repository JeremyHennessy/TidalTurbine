"""Conservative net-electricity and load *measurement* comparison.

Accepts synchronized, physically measured traces only with supplied provenance and
sensor calibration identifiers. Descriptive alternating-load RMS and peak are NOT
fatigue damage or a proof of lifetime improvement. No measured traces ship with repo.
"""
from math import isfinite, sqrt
from statistics import mean


def _finite(v):
    if isinstance(v, bool) or not isinstance(v,(int,float)) or not isfinite(v):
        raise ValueError('All observed quantities must be finite numbers')
    return float(v)


def _validate_run(run, *, allow_synthetic=False):
    required=('evidence_class','source_id','source_sha256','test_id','velocity_calibration_id',
              'load_calibration_id','electrical_calibration_id','mean_inflow_m_s',
              'turbulence_intensity','samples')
    if any(k not in run for k in required):raise ValueError('Missing observed-run evidence or calibration provenance')
    if run['evidence_class']!='MEASURED_EXPERIMENT':
        if not(allow_synthetic and run['evidence_class']=='SYNTHETIC_UNIT_TEST'):
            raise ValueError('Measured load-energy evidence required; synthetic screen is not validation')
    if any(not str(run[k]).strip() for k in required[:7]):raise ValueError('Empty source or calibration identity')
    u=_finite(run['mean_inflow_m_s']);ti=_finite(run['turbulence_intensity'])
    if u<=0 or not 0<=ti<=1:raise ValueError('Invalid inflow or turbulence metadata')
    a=run['samples']
    if not isinstance(a,list) or len(a)<4:raise ValueError('At least four synchronized samples required')
    required_samples=('time_s','generator_terminal_w','controller_consumption_w',
                      'auxiliary_consumption_w','blade_root_bending_n_m')
    for r in a:
        if any(x not in r for x in required_samples):raise ValueError('Missing synchronized bending/electricity channel')
        for k in required_samples:_finite(r[k])
        if r['controller_consumption_w']<0 or r['auxiliary_consumption_w']<0:raise ValueError('Measured consumption must be nonnegative')
    t=[_finite(r['time_s']) for r in a]
    if any(y<=x for x,y in zip(t,t[1:])):raise ValueError('Out-of-order / duplicate timestamps')
    return t


def compare(observed_baseline, observed_candidate, *, tolerance_m_s, tolerance_ti,
            allow_synthetic=False):
    """Descriptive paired comparison only; caller specifies allowed measured inflow mismatch.

    Source/replicate identity is verified syntactically, not independently authenticated.
    Matching mean velocity and TI alone cannot prove full inflow equivalence.
    """
    ta=_validate_run(observed_baseline,allow_synthetic=allow_synthetic)
    tb=_validate_run(observed_candidate,allow_synthetic=allow_synthetic)
    if ta!=tb:raise ValueError('Samples not synchronized on identical relative timebase')
    if observed_baseline['source_id']==observed_candidate['source_id'] and observed_baseline['test_id']==observed_candidate['test_id']:
        raise ValueError('Cannot compare the same physical experiment to itself')
    speed_tol=_finite(tolerance_m_s);ti_tol=_finite(tolerance_ti)
    if speed_tol<0 or ti_tol<0:raise ValueError('Match tolerances must be nonnegative')
    delta_speed=abs(observed_baseline['mean_inflow_m_s']-observed_candidate['mean_inflow_m_s'])
    delta_ti=abs(observed_baseline['turbulence_intensity']-observed_candidate['turbulence_intensity'])
    if delta_speed>speed_tol or delta_ti>ti_tol:raise ValueError('Inflow conditions do not meet declared matched-run tolerance')

    def evaluate(run):
        a=run['samples']
        net=[r['generator_terminal_w']-r['controller_consumption_w']-r['auxiliary_consumption_w'] for r in a]
        bending=[r['blade_root_bending_n_m'] for r in a]
        energy=sum((y['time_s']-x['time_s'])*(m+n)/2 for x,y,m,n in zip(a,a[1:],net,net[1:]))
        mu=mean(bending)
        dynamic_rms=sqrt(mean((b-mu)**2 for b in bending))
        return {'net_electrical_energy_j':round(energy,8),
                'mean_blade_root_bending_n_m':round(mu,8),
                'alternating_bending_rms_n_m':round(dynamic_rms,8),
                'max_abs_blade_root_bending_n_m':max(abs(v) for v in bending),
                'n_synchronized_samples':len(a)}
    a=evaluate(observed_baseline);b=evaluate(observed_candidate)
    return {'evidence_class':'MEASURED_TRACE_DESCRIPTIVE_NOT_FATIGUE_VALIDATION' if not allow_synthetic else 'SYNTHETIC_UNIT_TEST_ONLY',
            'baseline':a,'candidate':b,'inflow_match':{'difference_m_s':delta_speed,'difference_ti':delta_ti,
              'tolerances_m_s':speed_tol,'tolerance_ti':ti_tol},
            'energy_delta_j':round(b['net_electrical_energy_j']-a['net_electrical_energy_j'],8),
            'alternating_bending_rms_delta_n_m':round(b['alternating_bending_rms_n_m']-a['alternating_bending_rms_n_m'],8),
            'limitations':['Two compared traces are not independent fatigue tests or a lifetime forecast.',
                'Blade-root bending is not a calibrated blade stress without structural section modulus.',
                'Synchronized traces + mean/TI tolerance alone cannot remove confounding or establish causality.',
                'Uncertainty, repeated replicates, spectra, S-N and wet-environment damage require separate validation.']}
