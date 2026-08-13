from __future__ import annotations

import argparse
import json
import tempfile
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from anc_canonical import canonical_digest
from ordivon_harness.api import (
    DeepSeekSettings,
    DeepSeekTurnAdapter,
    HarnessAgentRun,
    HarnessBoundReference,
    HarnessPrivacyPolicy,
    HarnessRunContract,
    NO_TOOL_AGENT_GRANT_DIGEST,
    NO_TOOL_AGENT_SURFACE_DIGEST,
    RunBudget,
    decode_structured_completion_result,
)

HARNESS_IMPLEMENTATION = 'ordivon-harness@acs-fresh-agent'

RESULT_SCHEMA: dict[str, Any] = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'selectedOperation': {'type': 'string'},
        'owner': {'type': 'string'},
        'needsMoreInfo': {'type': 'boolean'},
        'effectClass': {
            'type': 'string',
            'enum': ['read_only', 'local_state_write', 'external_effect', 'unknown'],
        },
        'authorityBoundary': {'type': 'string'},
        'reason': {'type': 'string'},
    },
    'required': [
        'selectedOperation',
        'owner',
        'needsMoreInfo',
        'effectClass',
        'authorityBoundary',
        'reason',
    ],
}
_RESULT_KEYS = frozenset(RESULT_SCHEMA['required'])
_EFFECT_CLASSES = frozenset(RESULT_SCHEMA['properties']['effectClass']['enum'])


def ref(identity: str, kind: str, value: Any) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def validate_result_shape(value: Any) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return False, ['result is not an object']
    keys = set(value)
    if keys != _RESULT_KEYS:
        errors.append(f'result fields differ: {sorted(keys ^ _RESULT_KEYS)}')
    for key in ('selectedOperation', 'owner', 'authorityBoundary', 'reason'):
        if key in value and not isinstance(value[key], str):
            errors.append(f'{key} is not a string')
    if 'needsMoreInfo' in value and type(value['needsMoreInfo']) is not bool:
        errors.append('needsMoreInfo is not a boolean')
    if value.get('effectClass') not in _EFFECT_CLASSES:
        errors.append('effectClass is outside the admitted enum')
    return not errors, errors


def run_one(*, prompt: str, case_id: str, treatment: str, replicate: int, model: str, secret: Path) -> dict[str, Any]:
    settings = replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=1200)
    now = time.time_ns() // 1_000_000
    run_id = f'harness-run:acs1:{case_id}:{treatment}:{model}:{replicate}:{now}'
    completion = {
        'mode': 'structured-result-v1',
        'resultKind': 'acs-fresh-agent-operation-selection',
        'resultSchema': RESULT_SCHEMA,
    }
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id=HARNESS_IMPLEMENTATION,
        caller_id='caller:ordivon-computing-acs',
        caller_run_ref=f'acs1:{case_id}:{treatment}:{replicate}',
        objective_ref=ref(f'objective:{case_id}', 'objective', {'case': case_id}),
        context_refs=(ref(f'context:{case_id}:{treatment}', 'context', {'prompt': prompt}),),
        provider_id='provider:deepseek',
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(
            max_model_calls=2,
            max_tool_calls=0,
            max_observation_bytes=65_536,
            max_wall_time_ms=90_000,
            max_total_tokens=24_000,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(
            f'system-manifest:{case_id}:{treatment}',
            'system-manifest',
            {'experiment': 'acs1', 'treatment': treatment, 'structured': True},
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(
            content_policy='bounded-private-content',
            allow_model_content=True,
            allow_tool_content=False,
        ),
    )
    with tempfile.TemporaryDirectory(prefix='ordivon-acs-harness-') as state_root:
        run = HarnessAgentRun.create(
            state_root,
            contract,
            lambda exact: DeepSeekTurnAdapter(settings, completion_contract=exact.completion_contract),
        )
        started = time.monotonic()
        execution = run.run(({'role': 'user', 'content': prompt},))
        elapsed_ms = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        decoded = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        schema_valid, schema_errors = validate_result_shape(decoded) if decoded is not None else (False, ['no structured conclusion'])
        terminal = execution.terminal_result
        diagnostic_tail = None
        if decoded is None or not schema_valid:
            diagnostic_tail = [dict(message) for message in execution.loop_result.messages[-6:]]
        return {
            'schemaVersion': 1,
            'kind': 'ordivon.computing.acs-fresh-agent-trial',
            'caseId': case_id,
            'treatment': treatment,
            'replicate': replicate,
            'model': model,
            'contractDigest': contract.digest,
            'runId': run_id,
            'stopCode': execution.loop_result.stop_code.value,
            'modelCalls': execution.loop_result.model_calls,
            'toolCalls': execution.loop_result.tool_calls,
            'usage': execution.loop_result.usage,
            'elapsedMs': elapsed_ms,
            'result': decoded,
            'resultSchemaValid': schema_valid,
            'resultSchemaErrors': schema_errors,
            'diagnosticMessageTail': diagnostic_tail,
            'receiptDigest': None if terminal is None else terminal.receipt.digest,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--case-file', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--model', default='deepseek-v4-flash', choices=['deepseek-v4-flash', 'deepseek-v4-pro'])
    parser.add_argument('--replicates', type=int, default=1)
    parser.add_argument('--secret', default='/root/.config/ordivon/secrets/deepseek.json')
    parser.add_argument('--only-case')
    parser.add_argument('--only-treatment', choices=['raw', 'compiled'])
    args = parser.parse_args()
    case_doc = json.loads(Path(args.case_file).read_text())
    trials: list[dict[str, Any]] = []
    for case in case_doc['cases']:
        if args.only_case and case['caseId'] != args.only_case:
            continue
        treatments = ['raw', 'compiled'] if args.only_treatment is None else [args.only_treatment]
        for treatment in treatments:
            packet = case[treatment + 'Packet']
            prompt = case_doc['instruction'].replace('{{TASK}}', case['task']).replace('{{PACKET}}', packet)
            for replicate in range(1, args.replicates + 1):
                trial = run_one(
                    prompt=prompt,
                    case_id=case['caseId'],
                    treatment=treatment,
                    replicate=replicate,
                    model=args.model,
                    secret=Path(args.secret),
                )
                trials.append(trial)
                print(json.dumps({
                    'caseId': trial['caseId'],
                    'treatment': trial['treatment'],
                    'replicate': trial['replicate'],
                    'stopCode': trial['stopCode'],
                    'resultSchemaValid': trial['resultSchemaValid'],
                    'result': trial['result'],
                }, ensure_ascii=False))
    evidence = {
        'schemaVersion': 1,
        'kind': 'ordivon.computing.acs-fresh-agent-campaign',
        'model': args.model,
        'caseSourceDigest': canonical_digest(case_doc),
        'trials': trials,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    print(json.dumps({'output': str(out), 'trialCount': len(trials), 'digest': canonical_digest(evidence)}, indent=2))


if __name__ == '__main__':
    main()
