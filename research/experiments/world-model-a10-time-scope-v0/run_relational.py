#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as base  # noqa: E402

TREATMENTS = ('RAW_SCOPED', 'PROPERTY_TIMELINE')
REPLICATES = (1, 2)
CASE_IDS = {
    'c1n-current-after-unknown-effect',
    'c1n-historical-query-remains-valid',
    'c1n-new-current-truth-overrides-history',
    'ae2-old-truth-plus-new-conflict',
    'ae2-current-truth-resolves-new-conflict',
}
PROGRESS_PATH = HERE / '.relational-progress.json'


def selected_cases() -> list[dict[str, Any]]:
    return [case for case in base.cases() if case['caseId'] in CASE_IDS]


def property_timeline(case: dict[str, Any]) -> dict[str, Any]:
    cid = case['caseId']
    timelines: dict[str, dict[str, Any]] = {
        'c1n-current-after-unknown-effect': {
            'property': 'balance',
            'queryLogicalTime': 30,
            'priorStateEstablishingRecordId': 'record:c1n:witness-balance-1',
            'laterRelevantRecordIds': ['record:c1n:post-witness-effect-attempt'],
            'stateEstablishingRecordAfterLaterRelevantRecords': None,
        },
        'c1n-historical-query-remains-valid': {
            'property': 'balance',
            'queryLogicalTime': 10,
            'priorStateEstablishingRecordId': 'record:c1n:witness-balance-1',
            'laterRelevantRecordIds': [],
            'stateEstablishingRecordAfterLaterRelevantRecords': 'record:c1n:witness-balance-1',
        },
        'c1n-new-current-truth-overrides-history': {
            'property': 'balance',
            'queryLogicalTime': 30,
            'priorStateEstablishingRecordId': 'record:c1n:witness-balance-1',
            'laterRelevantRecordIds': ['record:c1n:post-witness-effect-applied'],
            'stateEstablishingRecordAfterLaterRelevantRecords': 'record:c1n:current-balance-truth-2',
        },
        'ae2-old-truth-plus-new-conflict': {
            'property': 'serviceCompromised',
            'queryLogicalTime': 25,
            'priorStateEstablishingRecordId': 'record:ae2:world-truth-false',
            'laterRelevantRecordIds': ['record:ae2:sensor-a-true', 'record:ae2:sensor-b-false'],
            'stateEstablishingRecordAfterLaterRelevantRecords': None,
        },
        'ae2-current-truth-resolves-new-conflict': {
            'property': 'serviceCompromised',
            'queryLogicalTime': 30,
            'priorStateEstablishingRecordId': 'record:ae2:world-truth-false',
            'laterRelevantRecordIds': ['record:ae2:sensor-a-true', 'record:ae2:sensor-b-false'],
            'stateEstablishingRecordAfterLaterRelevantRecords': 'record:ae2:new-world-truth-true',
        },
    }
    value = timelines[cid]
    visible_ids = {item['recordId'] for item in case['records']}
    ids = [value['priorStateEstablishingRecordId'], *value['laterRelevantRecordIds']]
    if value['stateEstablishingRecordAfterLaterRelevantRecords'] is not None:
        ids.append(value['stateEstablishingRecordAfterLaterRelevantRecords'])
    if any(item not in visible_ids for item in ids):
        raise RuntimeError(f'timeline references missing record: {cid}')
    return value


def project_case(case: dict[str, Any], treatment: str) -> dict[str, Any]:
    result = json.loads(json.dumps(case))
    result.pop('expected', None)
    result.pop('compatibleCurrentWorlds', None)
    result.pop('class', None)
    if treatment == 'PROPERTY_TIMELINE':
        result['propertyTimeline'] = property_timeline(case)
    return result


def prompt(case: dict[str, Any], treatment: str) -> str:
    return base.canonical(
        {
            'experiment': 'WML-A10-SECURITY-RELATIONAL-v0',
            'treatment': treatment,
            'instruction': (
                'Determine the value established for the query using only the supplied records. '
                'Authority applies only to the properties a record actually establishes. '
                'Do not invent hidden effect outcomes or hidden world state. If the query value is '
                'not established for the requested logical time, answer unknown. Historical records '
                'remain valid evidence for what they established at their own scope. If a propertyTimeline '
                'is present, it is only a deterministic index over the same records: it identifies the '
                'last state-establishing record before later relevant records, the later relevant record IDs, '
                'and whether another state-establishing record exists after those records. It does not itself '
                'state the answer or carry independent truth authority.'
            ),
            'case': project_case(case, treatment),
        }
    )


def identity(settings: base.DeepSeekSettings) -> dict[str, Any]:
    return {
        'experimentId': 'WML-A10-SECURITY-RELATIONAL-v0',
        'parentReceiptDigest': 'sha256:c9d33bc515405babcef8f3db434bdd7077583e5425b899ecb4277db0258655bc',
        'computingBaseRevision': base.COMPUTING_BASE,
        'securityRevision': base.SECURITY_REV,
        'harnessRevision': base.HARNESS_REV,
        'model': settings.model,
        'credentialScopeId': settings.credential_scope_id,
        'casesDigest': base.digest(selected_cases()),
        'timelineDigest': base.digest({case['caseId']: property_timeline(case) for case in selected_cases()}),
        'treatments': list(TREATMENTS),
        'replicates': list(REPLICATES),
        'ownerEvidence': base.source_evidence(),
    }


def empty_progress(experiment_identity: dict[str, Any]) -> dict[str, Any]:
    return {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a10-relational-progress',
        'identity': experiment_identity,
        'identityDigest': base.digest(experiment_identity),
        'records': {},
    }


def load_progress(experiment_identity: dict[str, Any]) -> dict[str, Any]:
    expected = empty_progress(experiment_identity)
    if not PROGRESS_PATH.exists():
        return expected
    value = json.loads(PROGRESS_PATH.read_text())
    if value.get('identityDigest') != expected['identityDigest'] or value.get('identity') != experiment_identity:
        raise RuntimeError('relational progress identity differs')
    return value


def save_progress(progress: dict[str, Any]) -> None:
    tmp = PROGRESS_PATH.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(PROGRESS_PATH)


def number(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def run_record(
    *,
    case: dict[str, Any],
    treatment: str,
    replicate: int,
    settings: base.DeepSeekSettings,
    progress: dict[str, Any],
) -> dict[str, Any]:
    key = f'{case["caseId"]}:{treatment}:r{replicate}'
    retained = progress['records'].get(key)
    if retained is not None:
        print(
            f'{case["caseId"]:46} {treatment:18} r{replicate} REPLAY '
            f'answer={retained["answer"]:7} expected={case["expected"]:7} ok={retained["correct"]}',
            flush=True,
        )
        return retained
    prompt_text = prompt(case, treatment)
    result, model_evidence = base.structured_call(
        run_id=f'wml-a10-rel:{case["caseId"]}:{treatment.lower()}:r{replicate}',
        prompt_text=prompt_text,
        schema=base.completion_schema(case),
        settings=settings,
    )
    answer = result['answer']
    error = base.classify_error(case['expected'], answer)
    value = {
        'caseId': case['caseId'],
        'caseClass': case['class'],
        'treatment': treatment,
        'replicate': replicate,
        'expected': case['expected'],
        'answer': answer,
        'correct': answer == case['expected'],
        'errorClass': error,
        'basisRecordIds': list(result['basisRecordIds']),
        'result': result,
        'promptDigest': 'sha256:' + __import__('hashlib').sha256(prompt_text.encode()).hexdigest(),
        'modelEvidence': model_evidence,
    }
    progress['records'][key] = value
    save_progress(progress)
    print(
        f'{case["caseId"]:46} {treatment:18} r{replicate} '
        f'answer={answer:7} expected={case["expected"]:7} ok={value["correct"]}',
        flush=True,
    )
    return value


def summarize(records: list[dict[str, Any]], treatment: str) -> dict[str, Any]:
    rows = [r for r in records if r['treatment'] == treatment]
    return {
        'decisions': len(rows),
        'correct': sum(int(r['correct']) for r in rows),
        'accuracy': sum(int(r['correct']) for r in rows) / len(rows),
        'falseCertainty': sum(int(r['errorClass'] == 'false-certainty') for r in rows),
        'falseAbstention': sum(int(r['errorClass'] == 'false-abstention') for r in rows),
        'wrongConcrete': sum(int(r['errorClass'] == 'wrong-concrete') for r in rows),
        'providerPromptTokens': sum(number(r['modelEvidence']['usage'].get('prompt_tokens')) for r in rows),
        'providerTotalTokens': sum(number(r['modelEvidence']['usage'].get('total_tokens')) for r in rows),
    }


def main() -> None:
    base.require_exact_sources()
    settings = base.DeepSeekSettings.from_secret_file(base.SECRET, max_output_tokens=640, timeout_seconds=90.0)
    experiment_identity = identity(settings)
    progress = load_progress(experiment_identity)
    save_progress(progress)
    records: list[dict[str, Any]] = []
    cases = selected_cases()
    for replicate in REPLICATES:
        order = TREATMENTS if replicate == 1 else tuple(reversed(TREATMENTS))
        for case in cases:
            for treatment in order:
                records.append(run_record(case=case, treatment=treatment, replicate=replicate, settings=settings, progress=progress))
    summaries = {t: summarize(records, t) for t in TREATMENTS}
    pairs = []
    for case in cases:
        for replicate in REPLICATES:
            raw = next(r for r in records if r['caseId'] == case['caseId'] and r['replicate'] == replicate and r['treatment'] == 'RAW_SCOPED')
            rel = next(r for r in records if r['caseId'] == case['caseId'] and r['replicate'] == replicate and r['treatment'] == 'PROPERTY_TIMELINE')
            pairs.append({
                'caseId': case['caseId'],
                'replicate': replicate,
                'rawCorrect': raw['correct'],
                'timelineCorrect': rel['correct'],
                'answerChanged': raw['answer'] != rel['answer'],
                'timelineFixedRawError': (not raw['correct']) and rel['correct'],
                'timelineHarmedRawCorrect': raw['correct'] and (not rel['correct']),
            })
    receipt = {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a10-relational-followup',
        'status': 'completed',
        'identity': experiment_identity,
        'cases': cases,
        'records': records,
        'summary': summaries,
        'pairedComparison': {
            'pairs': len(pairs),
            'answerChanged': sum(int(p['answerChanged']) for p in pairs),
            'timelineFixedRawError': sum(int(p['timelineFixedRawError']) for p in pairs),
            'timelineHarmedRawCorrect': sum(int(p['timelineHarmedRawCorrect']) for p in pairs),
            'details': pairs,
        },
        'externalSecurityEffectAttempted': False,
        'interpretationBoundary': (
            'Follow-up tests a deterministic relation index over the same Security-grounded records. '
            'The timeline carries no independent truth authority and does not establish a universal schema.'
        ),
    }
    payload_digest = base.digest(receipt)
    receipt['integrity'] = {'algorithm': 'sha256', 'payloadDigest': payload_digest}
    out = base.COMPUTING_ROOT / 'research/evidence' / f'wml-a10-security-relational-{payload_digest[7:19]}.json'
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    PROGRESS_PATH.unlink(missing_ok=True)
    print('RECEIPT', out.relative_to(base.COMPUTING_ROOT), payload_digest, flush=True)
    print('SUMMARY', json.dumps(summaries, sort_keys=True), flush=True)
    print('PAIRED', json.dumps(receipt['pairedComparison'], sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
