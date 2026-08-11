#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / 'run_stage.py'

spec = importlib.util.spec_from_file_location('run_stage', RUNNER)
assert spec and spec.loader
run_stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_stage)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=sorted(run_stage.STAGE_TREATMENTS))
    args = ap.parse_args()
    stage = args.stage
    path = ROOT / 'evidence' / f'{stage}-live-v1.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    original_failures = list(data.get('failures', []))
    if not original_failures:
        print(json.dumps({'stage': stage, 'repaired': 0, 'complete': data.get('complete')}, indent=2))
        return 0

    corpus = json.loads((ROOT / f'{stage}-corpus-v1.json').read_text(encoding='utf-8'))
    case_by_family = {c['familyId']: c for c in corpus['cases']}
    secret_by_slot = {s['slot']: s for s in run_stage.secrets()}
    existing = {(t['familyId'], t['treatment'], t['replicate']) for t in data['trials']}
    repairs = list(data.get('apparatusRepairs', []))
    remaining = []
    repaired = 0

    for failure in original_failures:
        key = (failure['familyId'], failure['treatment'], failure['replicate'])
        if key in existing:
            continue
        case = case_by_family[failure['familyId']]
        secret = secret_by_slot[failure['secretSlot']]
        try:
            row = run_stage.one_trial(stage, case, failure['treatment'], failure['replicate'], secret)
        except Exception as exc:
            remaining.append({**failure, 'repairFailureType': type(exc).__name__, 'repairFailureMessage': str(exc)[:1000]})
            continue
        data['trials'].append(row)
        existing.add(key)
        repaired += 1
        repairs.append({
            'familyId': failure['familyId'],
            'treatment': failure['treatment'],
            'replicate': failure['replicate'],
            'originalFailureType': failure['type'],
            'originalFailureMessage': failure['message'],
            'preRepairPhysicalProviderCalls': 1,
            'note': 'RemoteDisconnected was outside the original retry catch, so the failed task exited after its first physical Provider call. The missing semantic trial was replayed with identical frozen case/treatment/replicate identity after transport retry handling was repaired.',
        })

    data['trials'].sort(key=lambda x: (x['treatment'], x['familyId'], x['replicate']))
    data['failures'] = remaining
    data['apparatusRepairs'] = repairs
    data['analysis'] = run_stage.analyze(data['trials'], data['treatments'])
    pre_repair_calls = sum(int(x.get('preRepairPhysicalProviderCalls', 0)) for x in repairs)
    data['analysis']['preRepairFailedPhysicalProviderCalls'] = pre_repair_calls
    data['analysis']['physicalProviderCallsAllAttempts'] = data['analysis']['physicalProviderCalls'] + pre_repair_calls
    data['complete'] = len(data['trials']) == data['expectedAcceptedTrials'] and not remaining
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'stage': stage, 'repaired': repaired, 'remainingFailures': len(remaining), 'complete': data['complete'], 'analysis': data['analysis']}, indent=2, ensure_ascii=False))
    return 0 if data['complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
