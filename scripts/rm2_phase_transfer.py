"""Fixed A-to-B phase-template test; exploratory, not independent validation."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from scripts.rm2_raw_loads import ROOT, read_trial

FROZEN = ROOT / 'research/benchmarks/RM2_PHASE_TRANSFER_FROZEN_V2.json'
CHANNELS = ('rig_shaft_torque_phase_mean', 'rig_support_drag_phase_mean')

def metrics(predicted, observed):
    if len(predicted) != 36 or len(observed) != 36:
        raise ValueError('Exactly 36 phase bins required')
    if not all(type(x) in (int, float) and math.isfinite(x) for x in predicted + observed):
        raise ValueError('Finite numeric phase values required')
    baseline = sum(predicted) / 36
    mse = sum((p-o)**2 for p, o in zip(predicted, observed)) / 36
    constant_mse = sum((baseline-o)**2 for o in observed) / 36
    return {'rmse': math.sqrt(mse), 'bias': sum(p-o for p,o in zip(predicted,observed))/36,
            'constant_baseline_rmse': math.sqrt(constant_mse),
            'skill_vs_constant': None if constant_mse == 0 else 1-mse/constant_mse}

def compare(frozen, reduced):
    expected = {p['target_trial_id'] for p in frozen['predictions']}
    if len(reduced) != 2 or {r['trial_id'] for r in reduced} != expected:
        raise ValueError('Both preregistered target trials required; no selective reporting')
    output = []
    for p in frozen['predictions']:
        target = next(r for r in reduced if r['trial_id'] == p['target_trial_id'])
        for channel in CHANNELS:
            training = p['channels'][channel]
            observed = target[channel]
            if training['bin_midpoints_deg'] != observed['bin_midpoints_deg']:
                raise ValueError('Phase bins differ; no target-fitted alignment allowed')
            output.append({'target_trial_id': target['trial_id'], 'training_trial_id': p['training_trial_id'],
                           'channel': channel, 'units': 'Nm' if 'torque' in channel else 'N',
                           **metrics(training['means'], observed['means'])})
    return output

def validate_source_manifest(frozen, manifest):
    """Bind source assertions to the reviewed freeze before opening sample files."""
    expected = {p['target_trial_id']: p for p in frozen['predictions']}
    trials = manifest['trials']
    if len(trials) != len(expected) or {s['trial_id'] for s in trials} != set(expected):
        raise ValueError('Exact frozen target IDs required without duplicates')
    evidence = frozen['source_evidence']
    if manifest.get('phase_origin_status') != evidence['phase_origin_status']:
        raise ValueError('Caller cannot promote phase-origin evidence')
    if manifest.get('upstream_git_commit') != evidence['upstream_commit']:
        raise ValueError('Upstream commit differs from freeze')
    for source in trials:
        name = source['trial_id']
        prediction = expected[name]
        ref = evidence['target_reference'][name]
        if source['metadata']['sha256'] != evidence['metadata_sha256'][name]:
            raise ValueError('Metadata hash differs from freeze')
        if source['source_time_window_s'] != evidence['target_windows_s'][name]:
            raise ValueError('Steady window differs from freeze')
        if type(source['run']) is not int or source['run'] != ref['run']:
            raise ValueError('Run differs from freeze')
        if type(source['nominal_speed_m_s']) not in (int, float) or source['nominal_speed_m_s'] != prediction['nominal_speed_m_s']:
            raise ValueError('Operating point differs from freeze')
        if source['ni']['id'] != ref['ni_file_id'] or source['metadata']['id'] != ref['metadata_file_id']:
            raise ValueError('Original file IDs differ from freeze')
        for field in ('source_mean_cp', 'source_mean_cd', 'source_n_revolutions'):
            if source[field] != ref[field]:
                raise ValueError('Source reference differs from freeze: ' + field)
    return trials

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-dir', type=Path, required=True)
    parser.add_argument('--source-manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    frozen_bytes = FROZEN.read_bytes()
    frozen = json.loads(frozen_bytes)
    for name, expected in frozen['processing_sha256'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen processing hash mismatch: ' + name)
    if hashlib.sha256((ROOT / 'reports/RM2-RAW-LOADS-001.json').read_bytes()).hexdigest() != frozen['source_report_sha256']:
        raise ValueError('Frozen training report changed')
    manifest_bytes = args.source_manifest.read_bytes()
    manifest = json.loads(manifest_bytes)
    sources = validate_source_manifest(frozen, manifest)
    reduced = [read_trial(args.raw_dir, s) for s in sources]
    report = {'id': 'RM2-PHASE-TRANSFER-001', 'classification': frozen['classification'],
              'frozen_prediction_sha256': hashlib.sha256(frozen_bytes).hexdigest(),
              'source_manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
              'results': compare(frozen, reduced), 'target_reductions': reduced,
              'phase_origin_status': manifest['phase_origin_status'],
              'phase_transfer_eligibility': 'INELIGIBLE_UNVERIFIED_PHASE_ORIGIN',
              'limitations': frozen['limitations'],
              'independent_validation': False, 'FORCE_approved_rows': 0,
              'net_electricity_measured': False, 'blade_stress_validated': False}
    args.out.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps(report['results'], indent=2))

if __name__ == '__main__':
    main()
