#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
import hashlib
import http.client
import json
import random
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONTRACT = json.loads((ROOT / 'contract-v1.json').read_text())
SECRET_ROOT = Path('/root/.config/ordivon/secrets')
EVIDENCE = ROOT / 'evidence'
EVIDENCE.mkdir(exist_ok=True)
SUBJECT_SYSTEM = (
    'You are a fresh documentation reader. Answer the question using only the supplied '
    'exact-revision documentation bundle. Do not rely on prior knowledge of Ordivon. '
    'Distinguish local execution, authority, semantic completion, external-world truth, '
    'current/target/history, and evidence scopes when relevant. If the supplied documentation '
    'does not establish a conclusion, say that it is not established. Call submit_answer exactly once.'
)
JUDGE_SYSTEM = (
    'You are an independent rubric judge. You receive a question, a frozen oracle, and one reader answer. '
    'You do not know whether the answer came from old or rewritten documentation. Score the answer against '
    'the oracle only. decisionCorrect means the central conclusion is materially consistent with the frozen '
    'decision; it does not require verbatim wording. Count only clearly asserted critical errors, unsupported '
    'authority claims, and current/target/history confusions. Call submit_score exactly once.'
)


def digest(data: bytes) -> str:
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def secrets() -> list[dict[str, str]]:
    out = []
    for path in sorted(SECRET_ROOT.glob('deepseek*.json')):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        if all(isinstance(data.get(k), str) and data[k] for k in ('apiKey', 'baseUrl', 'model')):
            out.append({
                'slot': path.name,
                'apiKey': data['apiKey'],
                'baseUrl': data['baseUrl'].rstrip('/'),
                'model': data['model'],
            })
    if not out:
        raise RuntimeError('no DeepSeek credentials')
    return out


def tool(name: str, params: dict[str, Any]) -> dict[str, Any]:
    return {'type': 'function', 'function': {'name': name, 'parameters': params}}


def call(
    sec: dict[str, str],
    messages: list[dict[str, str]],
    schema: dict[str, Any],
    name: str,
    request_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    body = {
        'model': sec['model'],
        'messages': messages,
        'tools': [tool(name, schema)],
        'tool_choice': {'type': 'function', 'function': {'name': name}},
        'temperature': 0,
        'thinking': {'type': 'disabled'},
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(',', ':')).encode()
    endpoint = sec['baseUrl'] + (
        '/chat/completions' if not sec['baseUrl'].endswith('/chat/completions') else ''
    )
    errors: list[dict[str, Any]] = []
    calls = 0
    started = time.monotonic()
    for attempt in range(1, 6):
        calls += 1
        req = urllib.request.Request(
            endpoint,
            data=encoded,
            headers={
                'Authorization': 'Bearer ' + sec['apiKey'],
                'Content-Type': 'application/json',
                'X-Ordivon-Request-Id': request_id,
            },
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read()
            data = json.loads(raw)
            msg = (data.get('choices') or [{}])[0].get('message') or {}
            calls_out = msg.get('tool_calls') or []
            if len(calls_out) != 1 or calls_out[0].get('function', {}).get('name') != name:
                raise ValueError('missing exact tool call')
            args = calls_out[0]['function'].get('arguments')
            parsed = json.loads(args) if isinstance(args, str) else args
            if not isinstance(parsed, dict):
                raise ValueError('tool arguments not object')
            usage = data.get('usage') or {}
            return parsed, {
                'providerCalls': calls,
                'promptTokens': int(usage.get('prompt_tokens') or 0),
                'completionTokens': int(usage.get('completion_tokens') or 0),
                'totalTokens': int(usage.get('total_tokens') or 0),
                'elapsedMs': round((time.monotonic() - started) * 1000),
                'requestDigest': digest(encoded),
                'corrections': errors,
            }
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            http.client.RemoteDisconnected,
            ConnectionError,
            TimeoutError,
            json.JSONDecodeError,
            ValueError,
            KeyError,
        ) as exc:
            errors.append({'attempt': attempt, 'type': type(exc).__name__, 'message': str(exc)[:400]})
            if attempt == 5:
                raise
            time.sleep(min(1.2 * attempt, 4))
    raise AssertionError('unreachable')


def git_show(repo: str, revision: str, path: str) -> str:
    proc = subprocess.run(
        ['git', '-C', repo, 'show', f'{revision}:{path}'],
        text=True,
        capture_output=True,
    )
    return proc.stdout if proc.returncode == 0 else ''


def docs_for(task: dict[str, Any], arm: str) -> tuple[str, int, list[str]]:
    arm_info = CONTRACT['arms'][task['owner']]
    revision = arm_info[arm]
    parts: list[str] = []
    paths: list[str] = []
    for path in task['sourcePaths']:
        text = git_show(arm_info['repository'], revision, path)
        if text:
            parts.append(f'===== {path} =====\n{text}')
            paths.append(path)
    if not parts:
        parts = ['[No root entry document for this task exists at this exact revision.]']
    text = '\n\n'.join(parts)
    return text, len(text.encode()), paths


def subject_prompt(task: dict[str, Any], docs: str) -> str:
    return (
        f'Documentation bundle:\n\n{docs}\n\nReader question:\n{task["prompt"]}\n\n'
        'Answer directly in at most four sentences. State what is established, who owns the relevant '
        'authority/truth if material, and the required next action when the outcome is uncertain.'
    )


def judge_prompt(task: dict[str, Any], answer: str) -> str:
    return (
        'Question:\n' + task['prompt'] + '\n\nFrozen oracle:\n'
        + json.dumps(task['oracle'], ensure_ascii=False, indent=2)
        + '\n\nReader answer:\n' + answer
    )


SUBJECT_SCHEMA = {
    'type': 'object',
    'properties': {'answer': {'type': 'string', 'minLength': 1, 'maxLength': 2400}},
    'required': ['answer'],
    'additionalProperties': False,
}


def judge_schema(task: dict[str, Any]) -> dict[str, Any]:
    count = len(task['oracle']['requiredPoints'])
    return {
        'type': 'object',
        'properties': {
            'decisionCorrect': {'type': 'boolean'},
            'requiredPointsCovered': {'type': 'integer', 'minimum': 0, 'maximum': count},
            'criticalOverinferenceCount': {'type': 'integer', 'minimum': 0, 'maximum': 10},
            'unsupportedAuthorityClaimCount': {'type': 'integer', 'minimum': 0, 'maximum': 10},
            'currentTargetHistoryConfusionCount': {'type': 'integer', 'minimum': 0, 'maximum': 10},
            'rationale': {'type': 'string', 'minLength': 1, 'maxLength': 1200},
        },
        'required': [
            'decisionCorrect',
            'requiredPointsCovered',
            'criticalOverinferenceCount',
            'unsupportedAuthorityClaimCount',
            'currentTargetHistoryConfusionCount',
            'rationale',
        ],
        'additionalProperties': False,
    }


def trial(item: tuple[int, dict[str, Any], str, int, dict[str, str]]) -> dict[str, Any]:
    _, task, arm, replicate, sec = item
    docs, nbytes, paths = docs_for(task, arm)
    blind = 'bundle-' + hashlib.sha256(
        f'{task["id"]}:{arm}:{replicate}:fd3'.encode()
    ).hexdigest()[:10]
    answer_obj, subject_usage = call(
        sec,
        [
            {'role': 'system', 'content': SUBJECT_SYSTEM},
            {'role': 'user', 'content': subject_prompt(task, docs)},
        ],
        SUBJECT_SCHEMA,
        'submit_answer',
        f'fd4runtimecompact:{task["id"]}:{blind}:r{replicate}:subject',
    )
    answer = str(answer_obj['answer']).strip()
    score, judge_usage = call(
        sec,
        [
            {'role': 'system', 'content': JUDGE_SYSTEM},
            {'role': 'user', 'content': judge_prompt(task, answer)},
        ],
        judge_schema(task),
        'submit_score',
        f'fd4runtimecompact:{task["id"]}:{blind}:r{replicate}:judge',
    )
    return {
        'taskId': task['id'],
        'owner': task['owner'],
        'arm': arm,
        'blindBundle': blind,
        'replicate': replicate,
        'providerModel': sec['model'],
        'secretSlot': sec['slot'],
        'sourceRevision': CONTRACT['arms'][task['owner']][arm],
        'sourcePaths': paths,
        'inputDocumentBytes': nbytes,
        'answer': answer,
        'subjectUsage': subject_usage,
        'score': score,
        'judgeUsage': judge_usage,
    }


def main() -> None:
    creds = secrets()
    items = []
    idx = 0
    for task in CONTRACT['tasks']:
        for arm in ('baseline', 'treatment'):
            for replicate in range(1, CONTRACT['replicates'] + 1):
                items.append((idx, task, arm, replicate, creds[idx % len(creds)]))
                idx += 1
    random.Random(20260812).shuffle(items)
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(6, len(creds))) as pool:
        futures = {pool.submit(trial, item): item for item in items}
        for future in concurrent.futures.as_completed(futures):
            item = futures[future]
            try:
                rows.append(future.result())
            except Exception as exc:
                failures.append({
                    'taskId': item[1]['id'],
                    'arm': item[2],
                    'replicate': item[3],
                    'type': type(exc).__name__,
                    'message': str(exc)[:1000],
                })
    rows.sort(key=lambda row: (row['taskId'], row['arm'], row['replicate']))
    summary: dict[str, Any] = {
        'acceptedTrials': len(rows),
        'failures': len(failures),
        'byTask': {},
        'totalSubjectTokens': sum(r['subjectUsage']['totalTokens'] for r in rows),
        'totalJudgeTokens': sum(r['judgeUsage']['totalTokens'] for r in rows),
        'physicalProviderCalls': sum(
            r['subjectUsage']['providerCalls'] + r['judgeUsage']['providerCalls'] for r in rows
        ),
    }
    for task_id in sorted({row['taskId'] for row in rows}):
        summary['byTask'][task_id] = {}
        for arm in ('baseline', 'treatment'):
            selected = [r for r in rows if r['taskId'] == task_id and r['arm'] == arm]
            correct = sum(bool(r['score']['decisionCorrect']) for r in selected)
            summary['byTask'][task_id][arm] = {
                'trials': len(selected),
                'correct': correct,
                'majorityCorrect': correct >= 2,
                'criticalOverinference': sum(
                    int(r['score']['criticalOverinferenceCount']) for r in selected
                ),
                'unsupportedAuthorityClaims': sum(
                    int(r['score']['unsupportedAuthorityClaimCount']) for r in selected
                ),
                'requiredPointsCoveredTotal': sum(
                    int(r['score']['requiredPointsCovered']) for r in selected
                ),
                'inputDocumentBytes': selected[0]['inputDocumentBytes'] if selected else None,
                'providerTokens': sum(
                    r['subjectUsage']['totalTokens'] + r['judgeUsage']['totalTokens'] for r in selected
                ),
            }
    blockers = []
    for task_id, values in summary['byTask'].items():
        baseline = values['baseline']
        treatment = values['treatment']
        if baseline['majorityCorrect'] and not treatment['majorityCorrect']:
            blockers.append({'taskId': task_id, 'reason': 'baseline-correct_to_treatment-wrong'})
        if treatment['criticalOverinference'] > baseline['criticalOverinference']:
            blockers.append({'taskId': task_id, 'reason': 'new-treatment-critical-overinference'})
    summary['publicationBlockers'] = blockers
    summary['admissible'] = not blockers and not failures and len(rows) == CONTRACT['expectedSubjectCalls']
    output = {
        'schemaVersion': 1,
        'kind': 'ordivon.feynman-documentation.runtime-contraction-preflight-evidence',
        'contractDigest': digest((ROOT / 'contract-v1.json').read_bytes()),
        'trials': rows,
        'failures': failures,
        'summary': summary,
    }
    (EVIDENCE / 'preflight-v1.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if not summary['admissible']:
        raise SystemExit(3)


if __name__ == '__main__':
    main()
