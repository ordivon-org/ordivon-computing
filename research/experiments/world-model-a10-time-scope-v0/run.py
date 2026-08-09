#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

COMPUTING_ROOT = Path(__file__).resolve().parents[3]
SECURITY_ROOT = Path('/var/lib/ordivon/runtime/workspaces/security-wml-a10-source-20260809')
HARNESS_ROOT = Path('/var/lib/ordivon/runtime/workspaces/harness-wml-a10-equipment-20260809')
DEPENDENCY_SITE = Path('/root/projects/ordivon-harness/.venv/lib/python3.12/site-packages')
SECRET = Path('/root/.config/ordivon/secrets/deepseek.json')
COMPUTING_BASE = 'cadc0154a2fee54504b8fe680cc6751107c9ae57'
SECURITY_REV = 'ad24160ab0a3eaec7656ffd8f530a6a86ba55b75'
HARNESS_REV = 'f09c3795fc811c5a564a5285cf227b2a44283cf5'
TREATMENTS = ('RAW_SCOPED', 'EXPLICIT_TEMPORAL_ADMISSION')
REPLICATES = (1, 2)
PROGRESS_PATH = Path(__file__).resolve().parent / '.progress.json'
NO_TOOL_DIGEST = 'sha256:' + hashlib.sha256(b'wml-a10-no-tool').hexdigest()

sys.path.insert(0, str(DEPENDENCY_SITE))
sys.path.insert(0, str(HARNESS_ROOT / 'src'))
from ordivon_harness.ordivon.deepseek import DeepSeekSettings, DeepSeekTurnAdapter  # noqa: E402
from ordivon_harness.ordivon.model import AgentTurnRequest  # noqa: E402


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value: Any) -> str:
    return 'sha256:' + hashlib.sha256(canonical(value).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(root: Path) -> str:
    return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()


def git_dirty(root: Path) -> bool:
    return bool(subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True))


def require_exact_sources() -> None:
    checks = ((SECURITY_ROOT, SECURITY_REV), (HARNESS_ROOT, HARNESS_REV))
    for root, expected in checks:
        actual = git_head(root)
        if actual != expected:
            raise RuntimeError(f'{root.name} revision drift: {actual} != {expected}')
        if git_dirty(root):
            raise RuntimeError(f'{root.name} source workspace is dirty')


def record(
    record_id: str,
    *,
    role: str,
    property_name: str,
    authority: str,
    logical_time: int,
    **fields: Any,
) -> dict[str, Any]:
    return {
        'recordId': record_id,
        'role': role,
        'property': property_name,
        'authority': authority,
        'logicalTime': logical_time,
        **fields,
    }


def cases() -> list[dict[str, Any]]:
    c1n_witness = record(
        'record:c1n:witness-balance-1',
        role='state-witness',
        property_name='balance',
        authority='truth-recovery:c1n-sealed-state-witness-v1',
        logical_time=10,
        value='1',
        integrity='valid',
        statement='The witness establishes balance=1 at its observation point.',
    )
    unknown_effect = record(
        'record:c1n:post-witness-effect-attempt',
        role='effect-attempt',
        property_name='balance',
        authority='experiment-local-counterfactual-effect',
        logical_time=20,
        outcome='unknown',
        semantics='If committed, this effect changes balance from 1 to 2. Its physical outcome is not known.',
        producesWorldTruth=False,
    )
    applied_effect = record(
        'record:c1n:post-witness-effect-applied',
        role='effect-receipt',
        property_name='balance',
        authority='experiment-local-counterfactual-effect',
        logical_time=20,
        outcome='known-applied',
        semantics='The effect changed balance from 1 to 2.',
        producesWorldTruth=False,
    )
    balance_truth_2 = record(
        'record:c1n:current-balance-truth-2',
        role='world-truth',
        property_name='balance',
        authority='owned-downstream-current-observer',
        logical_time=30,
        value='2',
    )
    old_healthy_truth = record(
        'record:ae2:world-truth-false',
        role='world-truth',
        property_name='serviceCompromised',
        authority='owned-range-prior-adjudication',
        logical_time=10,
        value='false',
    )
    sensor_a_true = record(
        'record:ae2:sensor-a-true',
        role='sensor-observation',
        property_name='serviceCompromised',
        authority='range-owned-independent-sensor-not-world-truth',
        logical_time=20,
        sourceId='sensor:ae2-a',
        value='true',
    )
    sensor_b_false = record(
        'record:ae2:sensor-b-false',
        role='sensor-observation',
        property_name='serviceCompromised',
        authority='range-owned-independent-sensor-not-world-truth',
        logical_time=21,
        sourceId='sensor:ae2-b',
        value='false',
    )
    current_truth_true = record(
        'record:ae2:new-world-truth-true',
        role='world-truth',
        property_name='serviceCompromised',
        authority='owned-range-current-adjudication',
        logical_time=30,
        value='true',
    )
    quarantine_truth = record(
        'record:ae3b:quarantine-truth',
        role='world-truth',
        property_name='serviceQuarantined',
        authority='owned-range-current-observer',
        logical_time=20,
        value='true',
        compromiseTruthRevealed=False,
    )
    history = [
        record(
            f'record:ae3b:episode-{i}',
            role='adjudicated-prior-episode',
            property_name='serviceCompromised',
            authority='owned-range-prior-adjudication',
            logical_time=i,
            sensorA=str(a).lower(),
            sensorB=str(b).lower(),
            adjudicatedTruth=str(t).lower(),
        )
        for i, (a, b, t) in enumerate(
            ((True, False, True), (False, True, False), (True, False, True), (False, True, False)),
            start=1,
        )
    ]
    return [
        {
            'caseId': 'c1n-current-after-unknown-effect',
            'query': {'property': 'balance', 'logicalTime': 30, 'question': 'What is the current balance at logical time 30?'},
            'records': [c1n_witness, unknown_effect],
            'allowedAnswers': ['1', '2', 'unknown'],
            'expected': 'unknown',
            'compatibleCurrentWorlds': ['1', '2'],
            'class': 'expected-unknown',
        },
        {
            'caseId': 'c1n-historical-query-remains-valid',
            'query': {'property': 'balance', 'logicalTime': 10, 'question': 'What balance did the authoritative witness establish at logical time 10?'},
            'records': [c1n_witness],
            'allowedAnswers': ['1', '2', 'unknown'],
            'expected': '1',
            'compatibleCurrentWorlds': ['not-a-current-query'],
            'class': 'expected-concrete',
        },
        {
            'caseId': 'c1n-new-current-truth-overrides-history',
            'query': {'property': 'balance', 'logicalTime': 30, 'question': 'What is the current balance at logical time 30?'},
            'records': [c1n_witness, applied_effect, balance_truth_2],
            'allowedAnswers': ['1', '2', 'unknown'],
            'expected': '2',
            'compatibleCurrentWorlds': ['2'],
            'class': 'expected-concrete',
        },
        {
            'caseId': 'ae2-old-truth-plus-new-conflict',
            'query': {'property': 'serviceCompromised', 'logicalTime': 25, 'question': 'What is the current serviceCompromised value at logical time 25?'},
            'records': [old_healthy_truth, sensor_a_true, sensor_b_false],
            'allowedAnswers': ['true', 'false', 'unknown'],
            'expected': 'unknown',
            'compatibleCurrentWorlds': ['true', 'false'],
            'class': 'expected-unknown',
        },
        {
            'caseId': 'ae2-current-truth-resolves-new-conflict',
            'query': {'property': 'serviceCompromised', 'logicalTime': 30, 'question': 'What is the current serviceCompromised value at logical time 30?'},
            'records': [old_healthy_truth, sensor_a_true, sensor_b_false, current_truth_true],
            'allowedAnswers': ['true', 'false', 'unknown'],
            'expected': 'true',
            'compatibleCurrentWorlds': ['true'],
            'class': 'expected-concrete',
        },
        {
            'caseId': 'ae3c-history-pattern-does-not-prove-current',
            'query': {'property': 'serviceCompromised', 'logicalTime': 12, 'question': 'What is the current serviceCompromised value at logical time 12?'},
            'records': history + [sensor_a_true | {'logicalTime': 10}, sensor_b_false | {'logicalTime': 11}],
            'allowedAnswers': ['true', 'false', 'unknown'],
            'expected': 'unknown',
            'compatibleCurrentWorlds': ['true', 'false'],
            'class': 'expected-unknown',
        },
        {
            'caseId': 'ae2-truth-at-query-time-is-admissible',
            'query': {'property': 'serviceCompromised', 'logicalTime': 10, 'question': 'What serviceCompromised value is established at logical time 10?'},
            'records': [old_healthy_truth],
            'allowedAnswers': ['true', 'false', 'unknown'],
            'expected': 'false',
            'compatibleCurrentWorlds': ['false'],
            'class': 'expected-concrete',
        },
        {
            'caseId': 'ae3b-other-property-truth-does-not-prove-compromise',
            'query': {'property': 'serviceCompromised', 'logicalTime': 20, 'question': 'What is the current serviceCompromised value at logical time 20?'},
            'records': [quarantine_truth],
            'allowedAnswers': ['true', 'false', 'unknown'],
            'expected': 'unknown',
            'compatibleCurrentWorlds': ['true', 'false'],
            'class': 'expected-unknown',
        },
    ]


def temporal_admission(case: dict[str, Any], item: dict[str, Any]) -> str:
    cid = case['caseId']
    rid = item['recordId']
    mapping: dict[str, dict[str, str]] = {
        'c1n-current-after-unknown-effect': {
            'record:c1n:witness-balance-1': 'not-current-enough-after-unresolved-relevant-effect',
            'record:c1n:post-witness-effect-attempt': 'not-truth',
        },
        'c1n-historical-query-remains-valid': {
            'record:c1n:witness-balance-1': 'eligible-for-query-time',
        },
        'c1n-new-current-truth-overrides-history': {
            'record:c1n:witness-balance-1': 'historical-for-query',
            'record:c1n:post-witness-effect-applied': 'not-truth',
            'record:c1n:current-balance-truth-2': 'eligible-for-query-time',
        },
        'ae2-old-truth-plus-new-conflict': {
            'record:ae2:world-truth-false': 'historical-for-query',
            'record:ae2:sensor-a-true': 'not-world-truth',
            'record:ae2:sensor-b-false': 'not-world-truth',
        },
        'ae2-current-truth-resolves-new-conflict': {
            'record:ae2:world-truth-false': 'historical-for-query',
            'record:ae2:sensor-a-true': 'not-world-truth',
            'record:ae2:sensor-b-false': 'not-world-truth',
            'record:ae2:new-world-truth-true': 'eligible-for-query-time',
        },
        'ae3c-history-pattern-does-not-prove-current': {
            **{f'record:ae3b:episode-{i}': 'historical-for-query' for i in range(1, 5)},
            'record:ae2:sensor-a-true': 'not-world-truth',
            'record:ae2:sensor-b-false': 'not-world-truth',
        },
        'ae2-truth-at-query-time-is-admissible': {
            'record:ae2:world-truth-false': 'eligible-for-query-time',
        },
        'ae3b-other-property-truth-does-not-prove-compromise': {
            'record:ae3b:quarantine-truth': 'different-property',
        },
    }
    return mapping[cid][rid]


def project_case(case: dict[str, Any], treatment: str) -> dict[str, Any]:
    result = json.loads(json.dumps(case))
    result.pop('expected', None)
    result.pop('compatibleCurrentWorlds', None)
    result.pop('class', None)
    if treatment == 'EXPLICIT_TEMPORAL_ADMISSION':
        for item in result['records']:
            item['temporalAdmission'] = temporal_admission(case, item)
    return result


def completion_schema(case: dict[str, Any]) -> dict[str, Any]:
    ids = [item['recordId'] for item in case['records']]
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'answer': {'type': 'string', 'enum': case['allowedAnswers']},
            'basisRecordIds': {
                'type': 'array',
                'items': {'type': 'string', 'enum': ids},
                'minItems': 1,
                'uniqueItems': True,
            },
            'reason': {'type': 'string', 'minLength': 1},
        },
        'required': ['answer', 'basisRecordIds', 'reason'],
    }


def prompt(case: dict[str, Any], treatment: str) -> str:
    visible = project_case(case, treatment)
    return canonical(
        {
            'experiment': 'WML-A10-SECURITY-v0',
            'treatment': treatment,
            'instruction': (
                'Determine the value established for the query using only the supplied records. '
                'Authority applies only to the properties a record actually establishes. '
                'Do not invent hidden effect outcomes or hidden world state. If the query value is '
                'not established for the requested logical time, answer unknown. Historical records '
                'remain valid evidence for what they established at their own scope.'
            ),
            'case': visible,
        }
    )


def structured_call(
    *,
    run_id: str,
    prompt_text: str,
    schema: dict[str, Any],
    settings: DeepSeekSettings,
) -> tuple[dict[str, Any], dict[str, Any]]:
    completion = {
        'mode': 'structured-result-v1',
        'resultKind': 'time-scoped-truth-admission-v0',
        'resultSchema': schema,
    }
    adapter = DeepSeekTurnAdapter(settings, completion_contract=completion)
    request = AgentTurnRequest(
        harness_run_id=run_id,
        turn_id=f'turn:{run_id}',
        sequence=1,
        assignment_id=f'assignment:{run_id}',
        context_digest='sha256:' + hashlib.sha256(prompt_text.encode()).hexdigest(),
        tool_catalog_digest=NO_TOOL_DIGEST,
        messages=({'role': 'user', 'content': prompt_text},),
        tools=(),
        remaining_budget={'modelCalls': 1, 'toolCalls': 0, 'totalTokens': 32768},
    )
    result = adapter.invoke(request)
    if result.conclusion is None:
        raise RuntimeError('Provider did not submit a structured conclusion')
    value = json.loads(result.conclusion.summary)
    return value, {
        'requestDigest': request.digest,
        'resultDigest': result.digest,
        'modelCallId': result.model_call_id,
        'modelId': result.model_id,
        'effectiveModelId': result.effective_model,
        'usage': result.usage,
        'rawResponseDigest': result.raw_response_digest,
    }


def source_evidence() -> list[dict[str, Any]]:
    refs = [
        'evidence/acceptance/c1n-downstream-truth-failure-88d068b.json',
        'evidence/acceptance/ae2-conflicting-observations-990e71f.json',
        'evidence/acceptance/ae3c-evidence-reduction-7667668.json',
    ]
    out = []
    for ref in refs:
        path = SECURITY_ROOT / ref
        if not path.is_file():
            raise FileNotFoundError(path)
        value = json.loads(path.read_text())
        if value.get('status') != 'accepted':
            raise RuntimeError(f'owner evidence not accepted: {ref}')
        out.append({'ref': ref, 'sha256': file_sha256(path), 'kind': value.get('kind')})
    return out


def identity(settings: DeepSeekSettings) -> dict[str, Any]:
    payload = {
        'experimentId': 'WML-A10-SECURITY-v0',
        'computingBaseRevision': COMPUTING_BASE,
        'securityRevision': SECURITY_REV,
        'harnessRevision': HARNESS_REV,
        'model': settings.model,
        'credentialScopeId': settings.credential_scope_id,
        'casesDigest': digest(cases()),
        'treatments': list(TREATMENTS),
        'replicates': list(REPLICATES),
        'ownerEvidence': source_evidence(),
    }
    return payload


def empty_progress(experiment_identity: dict[str, Any]) -> dict[str, Any]:
    return {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a10-progress',
        'identity': experiment_identity,
        'identityDigest': digest(experiment_identity),
        'records': {},
    }


def load_progress(experiment_identity: dict[str, Any]) -> dict[str, Any]:
    expected = empty_progress(experiment_identity)
    if not PROGRESS_PATH.exists():
        return expected
    value = json.loads(PROGRESS_PATH.read_text())
    if value.get('identityDigest') != expected['identityDigest'] or value.get('identity') != experiment_identity:
        raise RuntimeError('existing progress belongs to a different experiment identity')
    if not isinstance(value.get('records'), dict):
        raise RuntimeError('progress records invalid')
    return value


def save_progress(progress: dict[str, Any]) -> None:
    tmp = PROGRESS_PATH.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(PROGRESS_PATH)


def classify_error(expected: str, answer: str) -> str | None:
    if answer == expected:
        return None
    if expected == 'unknown' and answer != 'unknown':
        return 'false-certainty'
    if expected != 'unknown' and answer == 'unknown':
        return 'false-abstention'
    return 'wrong-concrete'


def number(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def run_record(
    *,
    case: dict[str, Any],
    treatment: str,
    replicate: int,
    settings: DeepSeekSettings,
    progress: dict[str, Any],
) -> dict[str, Any]:
    key = f'{case["caseId"]}:{treatment}:r{replicate}'
    retained = progress['records'].get(key)
    if retained is not None:
        print(
            f'{case["caseId"]:46} {treatment:29} r{replicate} REPLAY '
            f'answer={retained["answer"]:7} expected={case["expected"]:7} ok={retained["correct"]}',
            flush=True,
        )
        return retained
    prompt_text = prompt(case, treatment)
    result, model_evidence = structured_call(
        run_id=f'wml-a10:{case["caseId"]}:{treatment.lower()}:r{replicate}',
        prompt_text=prompt_text,
        schema=completion_schema(case),
        settings=settings,
    )
    answer = result['answer']
    error = classify_error(case['expected'], answer)
    basis = list(result['basisRecordIds'])
    visible_ids = {item['recordId'] for item in case['records']}
    record_value = {
        'caseId': case['caseId'],
        'caseClass': case['class'],
        'treatment': treatment,
        'replicate': replicate,
        'expected': case['expected'],
        'answer': answer,
        'correct': answer == case['expected'],
        'errorClass': error,
        'compatibleCurrentWorlds': case['compatibleCurrentWorlds'],
        'basisRecordIds': basis,
        'basisValid': bool(basis) and set(basis).issubset(visible_ids),
        'result': result,
        'promptDigest': 'sha256:' + hashlib.sha256(prompt_text.encode()).hexdigest(),
        'modelEvidence': model_evidence,
    }
    progress['records'][key] = record_value
    save_progress(progress)
    print(
        f'{case["caseId"]:46} {treatment:29} r{replicate} '
        f'answer={answer:7} expected={case["expected"]:7} ok={record_value["correct"]}',
        flush=True,
    )
    return record_value


def summarize(records: list[dict[str, Any]], treatment: str) -> dict[str, Any]:
    rows = [r for r in records if r['treatment'] == treatment]
    errors = {'false-certainty': 0, 'false-abstention': 0, 'wrong-concrete': 0}
    for row in rows:
        if row['errorClass'] is not None:
            errors[row['errorClass']] += 1
    unknown_rows = [r for r in rows if r['expected'] == 'unknown']
    concrete_rows = [r for r in rows if r['expected'] != 'unknown']
    return {
        'decisions': len(rows),
        'correct': sum(int(r['correct']) for r in rows),
        'accuracy': sum(int(r['correct']) for r in rows) / len(rows),
        'unknownDecisionAccuracy': sum(int(r['correct']) for r in unknown_rows) / len(unknown_rows),
        'concreteDecisionAccuracy': sum(int(r['correct']) for r in concrete_rows) / len(concrete_rows),
        'falseCertainty': errors['false-certainty'],
        'falseAbstention': errors['false-abstention'],
        'wrongConcrete': errors['wrong-concrete'],
        'basisValid': sum(int(r['basisValid']) for r in rows),
        'providerPromptTokens': sum(number(r['modelEvidence']['usage'].get('prompt_tokens')) for r in rows),
        'providerTotalTokens': sum(number(r['modelEvidence']['usage'].get('total_tokens')) for r in rows),
    }


def main() -> None:
    require_exact_sources()
    settings = DeepSeekSettings.from_secret_file(SECRET, max_output_tokens=640, timeout_seconds=90.0)
    experiment_identity = identity(settings)
    progress = load_progress(experiment_identity)
    save_progress(progress)
    all_cases = cases()
    records: list[dict[str, Any]] = []
    for replicate in REPLICATES:
        treatment_order = TREATMENTS if replicate == 1 else tuple(reversed(TREATMENTS))
        for case in all_cases:
            for treatment in treatment_order:
                records.append(
                    run_record(
                        case=case,
                        treatment=treatment,
                        replicate=replicate,
                        settings=settings,
                        progress=progress,
                    )
                )
    summaries = {treatment: summarize(records, treatment) for treatment in TREATMENTS}
    paired = []
    for case in all_cases:
        for replicate in REPLICATES:
            raw = next(r for r in records if r['caseId'] == case['caseId'] and r['replicate'] == replicate and r['treatment'] == 'RAW_SCOPED')
            projected = next(r for r in records if r['caseId'] == case['caseId'] and r['replicate'] == replicate and r['treatment'] == 'EXPLICIT_TEMPORAL_ADMISSION')
            paired.append(
                {
                    'caseId': case['caseId'],
                    'replicate': replicate,
                    'rawCorrect': raw['correct'],
                    'projectedCorrect': projected['correct'],
                    'answerChanged': raw['answer'] != projected['answer'],
                    'projectionFixedRawError': (not raw['correct']) and projected['correct'],
                    'projectionHarmedRawCorrect': raw['correct'] and (not projected['correct']),
                }
            )
    receipt = {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a10-time-scope-experiment',
        'status': 'completed',
        'identity': experiment_identity,
        'cases': all_cases,
        'records': records,
        'summary': summaries,
        'pairedComparison': {
            'pairs': len(paired),
            'answerChanged': sum(int(p['answerChanged']) for p in paired),
            'projectionFixedRawError': sum(int(p['projectionFixedRawError']) for p in paired),
            'projectionHarmedRawCorrect': sum(int(p['projectionHarmedRawCorrect']) for p in paired),
            'details': paired,
        },
        'externalSecurityEffectAttempted': False,
        'interpretationBoundary': (
            'This is a bounded Agent truth-admission falsifier grounded in accepted Security semantics. '
            'It does not claim that Security physically executed witness-freshness C1-O, and it does not '
            'promote the experiment-local temporalAdmission projection into architecture.'
        ),
    }
    payload_digest = digest(receipt)
    receipt['integrity'] = {'algorithm': 'sha256', 'payloadDigest': payload_digest}
    out = COMPUTING_ROOT / 'research/evidence' / f'wml-a10-security-time-scope-{payload_digest[7:19]}.json'
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    PROGRESS_PATH.unlink(missing_ok=True)
    print('RECEIPT', out.relative_to(COMPUTING_ROOT), payload_digest, flush=True)
    print('SUMMARY', json.dumps(summaries, sort_keys=True), flush=True)
    print('PAIRED', json.dumps(receipt['pairedComparison'], sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
