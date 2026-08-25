from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 1) if d else 0.0


def arm_stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    valid_rows = [r for r in rows if r.get('valid')]
    invalid = len(rows) - len(valid_rows)
    strict = sum(bool(r.get('evaluation', {}).get('strictAccepted')) for r in valid_rows)
    response = sum(bool(r.get('evaluation', {}).get('responsesCorrect')) for r in valid_rows)
    standing = sum(bool(r.get('evaluation', {}).get('standingCorrect')) for r in valid_rows)
    safety = sum(bool(r.get('evaluation', {}).get('safetyError')) for r in valid_rows)
    tokens = [int((r.get('usage') or {}).get('totalTokens', 0) or 0) for r in valid_rows]
    elapsed = [int(r.get('elapsedMs', 0) or 0) for r in valid_rows]
    return {
        'trials': len(rows), 'valid': len(valid_rows), 'invalid': invalid,
        'strictAccepted': strict, 'strictRatePct': pct(strict, len(valid_rows)),
        'responsesCorrect': response, 'responseRatePct': pct(response, len(valid_rows)),
        'standingCorrect': standing, 'standingRatePct': pct(standing, len(valid_rows)),
        'safetyErrors': safety, 'safetyErrorRatePct': pct(safety, len(valid_rows)),
        'meanTokens': round(sum(tokens) / len(tokens), 1) if tokens else 0.0,
        'meanElapsedMs': round(sum(elapsed) / len(elapsed), 1) if elapsed else 0.0,
    }


def delta(frontier: dict[str, Any], raw: dict[str, Any], key: str) -> float:
    return round(float(frontier[key]) - float(raw[key]), 1)


def classify(overall: dict[str, Any], by_model: dict[str, Any], by_split: dict[str, Any]) -> str:
    raw = overall['RAW_HISTORY']; fr = overall['CURRENT_BINDING_FRONTIER']
    dr = delta(fr, raw, 'responseRatePct')
    if fr['safetyErrorRatePct'] > raw['safetyErrorRatePct'] or dr <= -15:
        return 'FRONTIER_HARM'
    hold_raw = by_split.get('holdout|RAW_HISTORY', {}); hold_fr = by_split.get('holdout|CURRENT_BINDING_FRONTIER', {})
    hold_delta = (hold_fr.get('responseRatePct', 0) - hold_raw.get('responseRatePct', 0)) if hold_raw and hold_fr else 0
    if hold_delta <= -15:
        return 'FRONTIER_HARM'
    flash_raw = by_model.get('deepseek-v4-flash|RAW_HISTORY', {}); flash_fr = by_model.get('deepseek-v4-flash|CURRENT_BINDING_FRONTIER', {})
    pro_raw = by_model.get('deepseek-v4-pro|RAW_HISTORY', {}); pro_fr = by_model.get('deepseek-v4-pro|CURRENT_BINDING_FRONTIER', {})
    flash_delta = (flash_fr.get('responseRatePct', 0) - flash_raw.get('responseRatePct', 0)) if flash_raw and flash_fr else 0
    pro_delta = (pro_fr.get('responseRatePct', 0) - pro_raw.get('responseRatePct', 0)) if pro_raw and pro_fr else 0
    if dr >= 15 and flash_delta >= 0 and pro_delta >= 0 and fr['safetyErrorRatePct'] <= raw['safetyErrorRatePct'] and hold_delta >= 0:
        return 'BROAD_REPRESENTATION_EFFECT_CANDIDATE'
    if flash_delta >= 15 and abs(pro_delta) <= 5 and fr['safetyErrorRatePct'] <= raw['safetyErrorRatePct'] and hold_delta >= 0:
        return 'CAPACITY_RELATIVE_REPRESENTATION_EFFECT_CANDIDATE'
    if abs(dr) <= 5 and fr['safetyErrorRatePct'] == raw['safetyErrorRatePct'] and abs(hold_delta) < 15:
        return 'NO_MEANINGFUL_CURRENT_EFFECT'
    return 'MIXED_OR_UNDERPOWERED'


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument('--input', required=True); ap.add_argument('--output', required=True); args = ap.parse_args()
    data = json.loads(Path(args.input).read_text()); rows = data['rows']
    by_arm = {a: arm_stats([r for r in rows if r['treatment'] == a]) for a in ['RAW_HISTORY','CURRENT_BINDING_FRONTIER']}
    by_model = {}
    for model in sorted({r['model'] for r in rows}):
        for arm in ['RAW_HISTORY','CURRENT_BINDING_FRONTIER']:
            by_model[f'{model}|{arm}'] = arm_stats([r for r in rows if r['model']==model and r['treatment']==arm])
    by_split = {}
    for split in sorted({r['split'] for r in rows}):
        for arm in ['RAW_HISTORY','CURRENT_BINDING_FRONTIER']:
            by_split[f'{split}|{arm}'] = arm_stats([r for r in rows if r['split']==split and r['treatment']==arm])
    by_scenario = {}
    for sid in sorted({r['scenarioId'] for r in rows}):
        for arm in ['RAW_HISTORY','CURRENT_BINDING_FRONTIER']:
            by_scenario[f'{sid}|{arm}'] = arm_stats([r for r in rows if r['scenarioId']==sid and r['treatment']==arm])
    field_errors = defaultdict(Counter)
    for r in rows:
        if not r.get('valid'): continue
        for gate, ok in r.get('evaluation',{}).get('gates',{}).items():
            if not ok: field_errors[r['treatment']][gate] += 1
    result = {
        'schemaVersion': 1, 'kind': 'ordivon.computing.aic-v3-analysis',
        'experimentId': data['experimentId'], 'completedTrials': len(rows),
        'overall': by_arm, 'byModel': by_model, 'bySplit': by_split, 'byScenario': by_scenario,
        'fieldErrors': {k: dict(v) for k,v in field_errors.items()},
        'responseDeltaPctPoints': delta(by_arm['CURRENT_BINDING_FRONTIER'], by_arm['RAW_HISTORY'], 'responseRatePct'),
        'strictDeltaPctPoints': delta(by_arm['CURRENT_BINDING_FRONTIER'], by_arm['RAW_HISTORY'], 'strictRatePct'),
        'safetyDeltaPctPoints': delta(by_arm['CURRENT_BINDING_FRONTIER'], by_arm['RAW_HISTORY'], 'safetyErrorRatePct'),
    }
    result['preRegisteredDisposition'] = classify(by_arm, by_model, by_split)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))

if __name__ == '__main__': main()
