"""Check source-declared channel clocks; never repair timing or certify data."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'research/benchmarks/RVAT_RUN13_CLOCK_METADATA.json'

def check(record):
    channels = record['channels']
    if not isinstance(channels, list) or len(channels) < 2:
        raise ValueError('At least two channel records required')
    names = [c['name'] for c in channels]
    if len(set(names)) != len(names):
        raise ValueError('Duplicate channels')
    for c in channels:
        if type(c['sample_count']) is not int or c['sample_count'] <= 0:
            raise ValueError('Positive integer sample count required')
        if type(c['increment_s']) not in (int, float) or not math.isfinite(c['increment_s']) or c['increment_s'] <= 0:
            raise ValueError('Finite positive time increment required')
        datetime.fromisoformat(c['start_time_as_stored'])
    base = channels[0]
    issues = []
    comparisons = []
    for c in channels[1:]:
        start = datetime.fromisoformat(c['start_time_as_stored'])
        first = datetime.fromisoformat(base['start_time_as_stored'])
        if (start.tzinfo is None) != (first.tzinfo is None):
            raise ValueError('Cannot mix timezone-aware and unspecified clocks')
        delta = (start-first).total_seconds()
        comparisons.append({'channel': c['name'], 'relative_start_difference_s': delta,
                            'increment_ratio_to_reference': c['increment_s']/base['increment_s']})
        if c['sample_count'] != base['sample_count']:
            issues.append(c['name'] + ': sample-count mismatch')
        if c['increment_s'] != base['increment_s']:
            issues.append(c['name'] + ': declared sampling increment mismatch')
        if delta != 0:
            issues.append(c['name'] + ': declared starting timestamp mismatch')
        if not c.get('units'):
            issues.append(c['name'] + ': measurement units absent')
    if not base.get('units'):
        issues.append(base['name'] + ': measurement units absent')
    if not isinstance(record.get('phase_origin_evidence'), str) or not record['phase_origin_evidence'].strip():
        issues.append('Intertrial physical encoder-zero evidence absent')
    return {'id': record['id'] + '-CHECK',
            'status': 'BLOCKED' if issues else 'METADATA_CONSISTENT_REVIEW_REQUIRED',
            'reference_channel': base['name'], 'comparisons': comparisons, 'issues': issues,
            'raw_samples_acquired': False, 'physical_validation': False,
            'timestamp_interpretation': 'As stored; no timezone or corrected clock inferred',
            'decision': 'Do not synthesize common timestamps or shift signals to force agreement. Resolve source clock and encoder conventions first.'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=DEFAULT)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = check(json.loads(args.input.read_text()))
    text = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if args.out: args.out.write_text(text)
    print(text, end='')

if __name__ == '__main__': main()
