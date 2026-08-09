#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as base  # noqa: E402

DISTRACTOR_COUNTS = (0, 2, 4, 8)
TASK_IDS = {'current-q2-growth', 'top-ten-concentration', 'eps-estimate-semantics'}
PROGRESS_PATH = HERE / '.r1-progress.json'


def catalog_entry(source_id: str, path: Path, body: dict[str, Any]) -> dict[str, Any]:
    return {
        'sourceId': source_id,
        'caseId': None,
        'subject': 'finance-schema',
        'sourceName': path.name,
        'observedAt': '0001-01-01T00:00:00Z',
        'availableFields': sorted(str(key) for key in body.keys()),
        'caseExtensionKeys': [],
    }


def distractor_pool() -> list[tuple[str, dict[str, Any], dict[str, Any], int]]:
    rows = []
    for path in (base.FINANCE_ROOT / 'schemas').glob('*.json'):
        raw = path.read_bytes()
        body = json.loads(raw)
        source_id = 'finance-file://schemas/' + path.name
        rows.append(
            (
                source_id,
                {'sourceId': source_id, 'path': 'schemas/' + path.name, 'body': body},
                catalog_entry(source_id, path, body),
                len(raw),
            )
        )
    rows.sort(key=lambda row: (-row[3], row[0]))
    return rows


def tier_inputs(count: int) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[tuple[str, dict[str, Any], dict[str, Any], int]]]:
    sources, catalog = base.load_sources()
    selected_tasks = [task for task in base.tasks(set(sources)) if task['taskId'] in TASK_IDS]
    distractors = distractor_pool()[:count]
    for source_id, content, meta, _size in distractors:
        sources[source_id] = content
        catalog.append(meta)
    catalog.sort(key=lambda x: x['sourceId'])
    selected_tasks.sort(key=lambda x: x['taskId'])
    return sources, catalog, selected_tasks, distractors


def num(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def progress_identity(settings: base.DeepSeekSettings) -> dict[str, Any]:
    tiers = []
    for count in DISTRACTOR_COUNTS:
        sources, catalog, selected_tasks, distractors = tier_inputs(count)
        tiers.append(
            {
                'distractorCount': count,
                'sourcePoolDigest': base.sha(sources),
                'catalogDigest': base.sha(catalog),
                'taskIds': [task['taskId'] for task in selected_tasks],
                'distractorSourceIds': [row[0] for row in distractors],
            }
        )
    return {
        'experimentId': 'WML-A6-FINANCE-v0',
        'round': 1,
        'financeRevision': base.FINANCE_REV,
        'harnessRevision': base.HARNESS_REV,
        'model': settings.model,
        'credentialScopeId': settings.credential_scope_id,
        'tiers': tiers,
    }


def empty_progress(identity: dict[str, Any]) -> dict[str, Any]:
    return {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a6-crossdomain-scale-progress',
        'identity': identity,
        'identityDigest': base.sha(identity),
        'selectionPhases': {},
        'records': {},
    }


def load_progress(identity: dict[str, Any]) -> dict[str, Any]:
    if not PROGRESS_PATH.exists():
        return empty_progress(identity)
    value = json.loads(PROGRESS_PATH.read_text())
    expected = empty_progress(identity)
    if (
        value.get('schemaVersion') != 1
        or value.get('kind') != expected['kind']
        or value.get('identityDigest') != expected['identityDigest']
        or value.get('identity') != identity
        or not isinstance(value.get('selectionPhases'), dict)
        or not isinstance(value.get('records'), dict)
    ):
        raise RuntimeError('R1 progress identity differs; remove progress only after explicit review')
    return value


def save_progress(progress: dict[str, Any]) -> None:
    tmp = PROGRESS_PATH.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(PROGRESS_PATH)


def selection_schema(sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
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


def run_record(
    *,
    count: int,
    task: dict[str, Any],
    treatment: str,
    sources: dict[str, dict[str, Any]],
    catalog: list[dict[str, Any]],
    settings: base.DeepSeekSettings,
    progress: dict[str, Any],
) -> dict[str, Any]:
    record_key = f'{count}:{task["taskId"]}:{treatment}'
    retained = progress['records'].get(record_key)
    if retained is not None:
        print(
            f'tier={count:2} {task["taskId"]:26} {treatment:5} '
            f'REPLAY ok={retained["correct"]} sources={len(retained["selectedSourceIds"]):2} '
            f'prompt={retained["providerPromptTokens"]:5}',
            flush=True,
        )
        return retained

    calls: list[dict[str, Any]] = []
    selection = None
    catalog_bytes = 0
    if treatment == 'FULL':
        selected_ids = sorted(sources)
    else:
        phase_key = f'{count}:{task["taskId"]}:AGENT:selection'
        retained_phase = progress['selectionPhases'].get(phase_key)
        if retained_phase is None:
            selection, call = base.structured_call(
                run_id=f'wml-a6-scale-{count}:{task["taskId"]}:select',
                sequence=1,
                prompt=base.select_prompt(task, catalog),
                result_kind='finance-source-selection-v0',
                schema=selection_schema(sources),
                settings=settings,
            )
            retained_phase = {
                'selection': selection,
                'modelEvidence': call,
                'catalogBytes': len(base.canonical(catalog).encode()),
            }
            progress['selectionPhases'][phase_key] = retained_phase
            save_progress(progress)
            print(
                f'tier={count:2} {task["taskId"]:26} AGENT SELECT '
                f'sources={len(selection["selectedSourceIds"]):2}',
                flush=True,
            )
        else:
            selection = retained_phase['selection']
            print(
                f'tier={count:2} {task["taskId"]:26} AGENT SELECT REPLAY '
                f'sources={len(selection["selectedSourceIds"]):2}',
                flush=True,
            )
        selection = retained_phase['selection']
        calls.append(retained_phase['modelEvidence'])
        catalog_bytes = int(retained_phase['catalogBytes'])
        selected_ids = list(selection['selectedSourceIds'])

    visible = {sid: sources[sid] for sid in selected_ids}
    answer, call = base.structured_call(
        run_id=f'wml-a6-scale-{count}:{task["taskId"]}:{treatment.lower()}',
        sequence=1,
        prompt=base.answer_prompt(task, visible, treatment),
        result_kind='finance-bounded-answer-v0',
        schema=base.answer_schema(task, selected_ids),
        settings=settings,
    )
    calls.append(call)
    record = {
        'taskId': task['taskId'],
        'treatment': treatment,
        'expected': task['expected'],
        'answer': answer['answer'],
        'correct': answer['answer'] == task['expected'],
        'requiredSourceIds': task['requiredSourceIds'],
        'selectedSourceIds': selected_ids,
        'selectedRequiredSource': all(x in selected_ids for x in task['requiredSourceIds']),
        'sourceContentBytes': sum(len(base.canonical(sources[sid]).encode()) for sid in selected_ids),
        'catalogBytes': catalog_bytes,
        'modelCalls': len(calls),
        'providerPromptTokens': sum(num(c['usage'].get('prompt_tokens')) for c in calls),
        'providerTotalTokens': sum(num(c['usage'].get('total_tokens')) for c in calls),
        'selection': selection,
        'answerResult': answer,
        'modelEvidence': calls,
    }
    progress['records'][record_key] = record
    save_progress(progress)
    print(
        f'tier={count:2} {task["taskId"]:26} {treatment:5} '
        f'ok={record["correct"]} sources={len(selected_ids):2} '
        f'prompt={record["providerPromptTokens"]:5}',
        flush=True,
    )
    return record


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {}
    for treatment in ('FULL', 'AGENT'):
        rows = [r for r in records if r['treatment'] == treatment]
        summary[treatment] = {
            'tasks': len(rows),
            'correct': sum(int(r['correct']) for r in rows),
            'accuracy': sum(int(r['correct']) for r in rows) / len(rows),
            'selectedRequiredSource': sum(int(r['selectedRequiredSource']) for r in rows),
            'sourceContentBytes': sum(r['sourceContentBytes'] for r in rows),
            'catalogBytes': sum(r['catalogBytes'] for r in rows),
            'modelCalls': sum(r['modelCalls'] for r in rows),
            'providerPromptTokens': sum(r['providerPromptTokens'] for r in rows),
            'providerTotalTokens': sum(r['providerTotalTokens'] for r in rows),
        }
    return summary


def main() -> None:
    base.require_clean_exact()
    settings = base.DeepSeekSettings.from_secret_file(
        base.SECRET, max_output_tokens=768, timeout_seconds=90.0
    )
    identity = progress_identity(settings)
    progress = load_progress(identity)
    save_progress(progress)
    tiers = []
    for count in DISTRACTOR_COUNTS:
        sources, catalog, selected_tasks, distractors = tier_inputs(count)
        records = []
        for task in selected_tasks:
            for treatment in ('FULL', 'AGENT'):
                records.append(
                    run_record(
                        count=count,
                        task=task,
                        treatment=treatment,
                        sources=sources,
                        catalog=catalog,
                        settings=settings,
                        progress=progress,
                    )
                )
        tiers.append(
            {
                'distractorCount': count,
                'distractorSourceIds': [row[0] for row in distractors],
                'sourcePoolCount': len(sources),
                'sourcePoolDigest': base.sha(sources),
                'catalogDigest': base.sha(catalog),
                'records': records,
                'summary': summarize(records),
            }
        )
    receipt = {
        'schemaVersion': 1,
        'kind': 'ordivon.world-model-a6-crossdomain-scale-sweep',
        'experimentId': 'WML-A6-FINANCE-v0',
        'round': 1,
        'computingRevision': base.git_head(base.COMPUTING_ROOT),
        'financeRevision': base.FINANCE_REV,
        'harnessRevision': base.HARNESS_REV,
        'model': settings.model,
        'credentialScopeId': settings.credential_scope_id,
        'taskIds': sorted(TASK_IDS),
        'progressIdentityDigest': progress['identityDigest'],
        'tiers': tiers,
        'externalFinancialWriteAttempted': False,
        'interpretationBoundary': (
            'Scale sweep over exact Git-bound Finance sources. It tests context-selection '
            'cost scaling, not investment quality or stable benchmark performance.'
        ),
    }
    digest = base.sha(receipt)
    receipt['integrity'] = {'algorithm': 'sha256', 'payloadDigest': digest}
    out = (
        base.COMPUTING_ROOT
        / 'research/evidence'
        / f'wml-a6-finance-scale-r1-{digest[7:19]}.json'
    )
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    PROGRESS_PATH.unlink(missing_ok=True)
    print('RECEIPT', out.relative_to(base.COMPUTING_ROOT), digest, flush=True)
    for tier in tiers:
        print(
            'TIER_SUMMARY',
            tier['distractorCount'],
            json.dumps(tier['summary'], sort_keys=True),
            flush=True,
        )


if __name__ == '__main__':
    main()
