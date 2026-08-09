#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

COMPUTING_ROOT = Path(__file__).resolve().parents[3]
FINANCE_ROOT = Path('/root/projects/ordivon-finance')
HARNESS_ROOT = Path('/root/projects/ordivon-harness')
FINANCE_REV = 'ef3739d774037298af66a325f6a3314b92aefa8b'
HARNESS_REV = '487e0ac8eb945256842347b5371cbbdd70bfce55'
SECRET = Path('/root/.config/ordivon/secrets/deepseek.json')
NO_TOOL_DIGEST = 'sha256:' + hashlib.sha256(b'wml-a6-no-tool').hexdigest()

sys.path.insert(0, str(HARNESS_ROOT / '.venv/lib/python3.12/site-packages'))
sys.path.insert(0, str(HARNESS_ROOT / 'src'))
from ordivon_harness.ordivon.deepseek import DeepSeekSettings, DeepSeekTurnAdapter  # noqa: E402
from ordivon_harness.ordivon.model import AgentTurnRequest  # noqa: E402


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def sha(value: Any) -> str:
    return 'sha256:' + hashlib.sha256(canonical(value).encode()).hexdigest()


def git_head(root: Path) -> str:
    return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()


def require_clean_exact() -> None:
    pairs = [(FINANCE_ROOT, FINANCE_REV), (HARNESS_ROOT, HARNESS_REV)]
    for root, expected in pairs:
        actual = git_head(root)
        if actual != expected:
            raise RuntimeError(f'{root.name} HEAD moved: {actual} != {expected}')
        dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True)
        if dirty:
            raise RuntimeError(f'{root.name} source repository is dirty')


def load_sources() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    base = json.loads((FINANCE_ROOT / 'research/economic/spy-economic-case-v0.json').read_text())
    refresh = json.loads((FINANCE_ROOT / 'research/economic/spy-q2-earnings-progress-2026-08-05.json').read_text())
    sources: dict[str, dict[str, Any]] = {}
    catalog: list[dict[str, Any]] = []
    for item in base['evidenceItems']:
        sid = 'finance-source://' + item['evidenceId']
        content = {
            'sourceId': sid,
            'caseId': base['caseId'],
            'subject': base['subject'],
            'economicExposure': base['economicExposure'],
            'evidenceItem': item,
        }
        sources[sid] = content
        catalog.append({
            'sourceId': sid,
            'caseId': base['caseId'],
            'subject': base['subject'],
            'sourceName': item['sourceName'],
            'observedAt': item['observedAt'],
            'availableFields': sorted(item.get('facts', {}).keys()),
            'caseExtensionKeys': [],
        })
    item = refresh['evidenceItems'][0]
    sid = 'finance-source://' + item['evidenceId']
    content = {
        'sourceId': sid,
        'caseId': refresh['caseId'],
        'subject': refresh['subject'],
        'economicExposure': refresh['economicExposure'],
        'evidenceItem': item,
        'caseExtensions': refresh['extensions'],
    }
    sources[sid] = content
    catalog.append({
        'sourceId': sid,
        'caseId': refresh['caseId'],
        'subject': refresh['subject'],
        'sourceName': item['sourceName'],
        'observedAt': item['observedAt'],
        'availableFields': sorted(item.get('facts', {}).keys()),
        'caseExtensionKeys': sorted(refresh.get('extensions', {}).keys()),
    })
    return sources, sorted(catalog, key=lambda x: x['sourceId'])


def tasks(source_ids: set[str]) -> list[dict[str, Any]]:
    ids = {sid.split('finance-source://', 1)[1]: sid for sid in source_ids}
    return [
        {
            'taskId': 'current-q2-growth',
            'question': 'Using the most advanced Q2 reporting evidence in the fixed source pool, what adjusted Q2 S&P 500 earnings growth percentage is the current evidence value?',
            'choices': ['31.1', '37.9', '25.9', 'unknown'],
            'expected': '31.1',
            'requiredSourceIds': [ids['sp500-q2-earnings-progress-2026-08-05']],
        },
        {
            'taskId': 'top-ten-concentration',
            'question': 'What top-ten holdings weight percentage is explicitly supported for SPY/S&P 500 by the fixed source pool?',
            'choices': ['38.15', '37.64', '14.92', 'unknown'],
            'expected': '38.15',
            'requiredSourceIds': [ids['spy-index-characteristics-2026-08-06']],
        },
        {
            'taskId': 'q2-complete-quarter',
            'question': 'Does the most advanced Q2 earnings source establish a completed-quarter observation?',
            'choices': ['yes', 'no', 'unknown'],
            'expected': 'no',
            'requiredSourceIds': [ids['sp500-q2-earnings-progress-2026-08-05']],
        },
        {
            'taskId': 'latest-forward-pe',
            'question': 'What forward P/E value appears in the most advanced Q2 earnings refresh that also reports a 4.63% nominal 10-year Treasury yield?',
            'choices': ['20.4', '20.1', '21.58', 'unknown'],
            'expected': '20.4',
            'requiredSourceIds': [ids['sp500-q2-earnings-progress-2026-08-05']],
        },
        {
            'taskId': 'alphabet-adjusted-july24',
            'question': 'In the July 24 partial-quarter FactSet evidence, what Q2 blended earnings growth percentage was reported excluding Alphabet?',
            'choices': ['25.9', '37.9', '31.1', 'unknown'],
            'expected': '25.9',
            'requiredSourceIds': [ids['sp500-q2-earnings-2026-07-24']],
        },
        {
            'taskId': 'eps-estimate-semantics',
            'question': 'Is the 18.44% estimated three-to-five-year EPS growth figure an observed future outcome?',
            'choices': ['yes', 'no', 'unknown'],
            'expected': 'no',
            'requiredSourceIds': [ids['spy-index-characteristics-2026-08-06']],
        },
    ]


def structured_call(*, run_id: str, sequence: int, prompt: str, result_kind: str, schema: dict[str, Any], settings: DeepSeekSettings) -> tuple[dict[str, Any], dict[str, Any]]:
    completion = {'mode': 'structured-result-v1', 'resultKind': result_kind, 'resultSchema': schema}
    adapter = DeepSeekTurnAdapter(settings, completion_contract=completion)
    request = AgentTurnRequest(
        harness_run_id=run_id,
        turn_id=f'turn:{sequence}',
        sequence=sequence,
        assignment_id=f'assignment:{run_id}',
        context_digest='sha256:' + hashlib.sha256(prompt.encode()).hexdigest(),
        tool_catalog_digest=NO_TOOL_DIGEST,
        messages=({'role': 'user', 'content': prompt},),
        tools=(),
        remaining_budget={'modelCalls': 1, 'toolCalls': 0, 'totalTokens': 32768},
    )
    result = adapter.invoke(request)
    if result.conclusion is None:
        raise RuntimeError('model did not submit a structured conclusion')
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


def answer_schema(task: dict[str, Any], visible_ids: list[str]) -> dict[str, Any]:
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'answer': {'type': 'string', 'enum': task['choices']},
            'usedSourceIds': {
                'type': 'array',
                'items': {'type': 'string', 'enum': visible_ids},
                'minItems': 1,
                'uniqueItems': True,
            },
            'rationale': {'type': 'string', 'minLength': 1},
        },
        'required': ['answer', 'usedSourceIds', 'rationale'],
    }


def answer_prompt(task: dict[str, Any], visible: dict[str, dict[str, Any]], treatment: str) -> str:
    return canonical({
        'experiment': 'WML-A6-FINANCE-v0',
        'treatment': treatment,
        'rule': 'Use only the visible exact Finance sources. If the requested value or semantic relation is not established by them, answer unknown. Do not answer from pretrained memory. Cite only sourceIds actually used.',
        'task': {'taskId': task['taskId'], 'question': task['question'], 'allowedAnswers': task['choices']},
        'visibleSources': [visible[sid] for sid in sorted(visible)],
    })


def select_prompt(task: dict[str, Any], catalog: list[dict[str, Any]]) -> str:
    return canonical({
        'experiment': 'WML-A6-FINANCE-v0',
        'phase': 'agent-select-view',
        'rule': 'Select one or two exact Finance sources whose declared fields/provenance are sufficient to answer the task. Catalog metadata contains no fact values. Prefer the smallest sufficient set. Do not guess the answer yet.',
        'task': {'taskId': task['taskId'], 'question': task['question'], 'allowedAnswers': task['choices']},
        'sourceCatalog': catalog,
    })


def num(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def main() -> None:
    require_clean_exact()
    sources, catalog = load_sources()
    tks = tasks(set(sources))
    settings = DeepSeekSettings.from_secret_file(SECRET, max_output_tokens=768, timeout_seconds=90.0)
    latest_id = max(catalog, key=lambda x: x['observedAt'])['sourceId']
    records: list[dict[str, Any]] = []
    seq = 0
    for task in tks:
        for treatment in ('FULL', 'LATEST', 'AGENT'):
            model_calls: list[dict[str, Any]] = []
            selection = None
            catalog_bytes = 0
            if treatment == 'FULL':
                selected_ids = sorted(sources)
            elif treatment == 'LATEST':
                selected_ids = [latest_id]
            else:
                seq += 1
                sp = select_prompt(task, catalog)
                catalog_bytes = len(canonical(catalog).encode())
                selection_schema = {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'selectedSourceIds': {
                            'type': 'array',
                            'items': {'type': 'string', 'enum': sorted(sources)},
                            'minItems': 1,
                            'maxItems': 2,
                            'uniqueItems': True,
                        },
                        'rationale': {'type': 'string', 'minLength': 1},
                    },
                    'required': ['selectedSourceIds', 'rationale'],
                }
                selection, call = structured_call(
                    run_id=f'wml-a6-r0:{task["taskId"]}:agent-select', sequence=seq,
                    prompt=sp, result_kind='finance-source-selection-v0', schema=selection_schema, settings=settings)
                model_calls.append(call)
                selected_ids = list(selection['selectedSourceIds'])
            visible = {sid: sources[sid] for sid in selected_ids}
            seq += 1
            ap = answer_prompt(task, visible, treatment)
            answer, call = structured_call(
                run_id=f'wml-a6-r0:{task["taskId"]}:{treatment.lower()}', sequence=seq,
                prompt=ap, result_kind='finance-bounded-answer-v0',
                schema=answer_schema(task, selected_ids), settings=settings)
            model_calls.append(call)
            source_bytes = sum(len(canonical(sources[sid]).encode()) for sid in selected_ids)
            cited = list(answer['usedSourceIds'])
            provider_prompt_tokens = sum(num(c['usage'].get('prompt_tokens')) for c in model_calls)
            provider_total_tokens = sum(num(c['usage'].get('total_tokens')) for c in model_calls)
            record = {
                'taskId': task['taskId'],
                'treatment': treatment,
                'expected': task['expected'],
                'answer': answer['answer'],
                'correct': answer['answer'] == task['expected'],
                'requiredSourceIds': task['requiredSourceIds'],
                'selectedSourceIds': selected_ids,
                'selectedRequiredSource': all(x in selected_ids for x in task['requiredSourceIds']),
                'usedSourceIds': cited,
                'citationValid': bool(cited) and set(cited).issubset(selected_ids),
                'sourceContentBytes': source_bytes,
                'catalogBytes': catalog_bytes,
                'modelCalls': len(model_calls),
                'providerPromptTokens': provider_prompt_tokens,
                'providerTotalTokens': provider_total_tokens,
                'selection': selection,
                'answerResult': answer,
                'modelEvidence': model_calls,
            }
            records.append(record)
            print(f"{task['taskId']:28} {treatment:6} answer={answer['answer']:7} expected={task['expected']:7} ok={record['correct']} sources={len(selected_ids)} calls={len(model_calls)}")
    summary: dict[str, Any] = {}
    for treatment in ('FULL', 'LATEST', 'AGENT'):
        rows = [r for r in records if r['treatment'] == treatment]
        summary[treatment] = {
            'tasks': len(rows),
            'correct': sum(int(r['correct']) for r in rows),
            'accuracy': sum(int(r['correct']) for r in rows) / len(rows),
            'selectedRequiredSource': sum(int(r['selectedRequiredSource']) for r in rows),
            'citationValid': sum(int(r['citationValid']) for r in rows),
            'sourceContentBytes': sum(r['sourceContentBytes'] for r in rows),
            'catalogBytes': sum(r['catalogBytes'] for r in rows),
            'modelCalls': sum(r['modelCalls'] for r in rows),
            'providerPromptTokens': sum(r['providerPromptTokens'] for r in rows),
            'providerTotalTokens': sum(r['providerTotalTokens'] for r in rows),
        }
    receipt = {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a6-crossdomain-calibration',
        'experimentId': 'WML-A6-FINANCE-v0',
        'round': 0,
        'computingRevision': git_head(COMPUTING_ROOT),
        'financeRevision': FINANCE_REV,
        'harnessRevision': HARNESS_REV,
        'model': settings.model,
        'credentialScopeId': settings.credential_scope_id,
        'sourcePoolDigest': sha(sources),
        'sourceCatalogDigest': sha(catalog),
        'latestStaticSourceId': latest_id,
        'tasks': tks,
        'records': records,
        'summary': summary,
        'externalFinancialWriteAttempted': False,
        'interpretationBoundary': 'Calibration only. This receipt validates or falsifies the apparatus; it is not by itself a stable model-performance estimate or Core revision.',
    }
    digest = sha(receipt)
    receipt['integrity'] = {'algorithm': 'sha256', 'payloadDigest': digest}
    out = COMPUTING_ROOT / 'research/evidence' / f'wml-a6-finance-selection-r0-{digest[7:19]}.json'
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print('RECEIPT', out.relative_to(COMPUTING_ROOT), digest)
    print('SUMMARY', json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
