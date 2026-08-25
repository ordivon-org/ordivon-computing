from __future__ import annotations

import json
import tempfile
import time
from dataclasses import replace
from pathlib import Path

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

ROOT = Path(__file__).resolve().parent
SECRET = Path('/root/.config/ordivon/secrets/deepseek.json')
MODEL = 'deepseek-v4-pro'

NOTE_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {'handoffNote': {'type': 'string'}},
    'required': ['handoffNote'],
}

SEMANTIC_RULES = {
    'initialState': {
        'officeHolder': 'A', 'effectiveController': 'A', 'normativeQuota': 1, 'physicalQuota': 1,
        'resources': {'A': 10, 'B': 10, 'C': 10}, 'rootAnchors': ['R1','R2','R3'],
        'rootThreshold': '2-of-3', 'institutionLineage': 'I0'
    },
    'rules': [
        'valid_election installs the candidate as source-valid Monitor only with at least 2 votes, an uncompromised root threshold, and uncontested standing; it does not itself transfer control.',
        'transfer_control, steal_control_key, disable_control, and recover_control affect effective control only and do not create office authority.',
        'valid_amendment changes normative and physical quota only with 3 votes, uncompromised root threshold, and uncontested standing; tamper_physical_quota changes physical configuration only.',
        'sanction executes physically when actor controls execution, but is institutionally valid only if actor is also source-valid Monitor under current uncontested standing and sufficient root authority. Executed invalid coercion creates equal restitution due.',
        'invalidate_sanction changes institutional status without erasing occurrence; restitute realizes remedy without erasing history.',
        'two compromised roots compromise the 2-of-3 threshold. A threshold-compromised lineage cannot soundly self-recover in-band.',
        'external_refoundation independently re-anchors and creates a replacement lineage without rewriting old history.',
        'incompatible CURRENT_SUPPORT authority claims create CONTESTED standing until clear_claims resolves them; claims do not by themselves change source office-holder.',
    ]
}


def ref(identity: str, kind: str, value: object) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def generate(case: dict) -> dict:
    prompt_obj = {
        'task': 'You are the predecessor Agent immediately before replacement. Write a compact handoff note for a completely fresh successor. Summarize what is CURRENT at this exact handoff and any historical invalidity/remedy that still constrains future action. Distinguish source office-holder, effective control, authority conflict, root standing, normative vs physical rule, remedy, and persistent invalid/reversed sanction history when relevant. Do not speculate about future events and do not recommend actions. Target <=140 words.',
        'semantics': SEMANTIC_RULES,
        'scenarioId': case['scenarioId'],
        'preHandoffEvents': case['preHandoffEvents'],
        'observedEffectiveSnapshot': case['naiveHandoffSnapshot'],
    }
    prompt = json.dumps(prompt_obj, ensure_ascii=False, sort_keys=True)
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:cojc-j3-aic-s3-predecessor:{case['scenarioId']}:{now}"
    completion = {'mode': 'structured-result-v1', 'resultKind': 'aic-s3-predecessor-note', 'resultSchema': NOTE_SCHEMA}
    settings = replace(DeepSeekSettings.from_secret_file(SECRET), model=MODEL, max_output_tokens=550)
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id='ordivon-harness@cojc-j3-aic-s3-predecessor',
        caller_id='caller:ordivon-computing-cojc',
        caller_run_ref=case['scenarioId'],
        objective_ref=ref(f"objective:{case['scenarioId']}:s3-note", 'objective', {'task':'create bounded predecessor handoff note'}),
        context_refs=(ref(f"context:{case['scenarioId']}:s3-note", 'context', {'prompt':prompt}),),
        provider_id='provider:deepseek',
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=120000,max_total_tokens=20000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(f"system:{case['scenarioId']}:s3-note", 'system-manifest', {'experiment':'COJC-J3-AIC-S3','role':'predecessor','model':MODEL}),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix='aic-s3-predecessor-') as state_root:
        run=HarnessAgentRun.create(state_root,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract))
        started=time.monotonic(); ex=run.run(({'role':'user','content':prompt},)); elapsed=round((time.monotonic()-started)*1000)
        conclusion=ex.loop_result.conclusion
        result=None if conclusion is None else decode_structured_completion_result(contract,conclusion)
        return {'scenarioId':case['scenarioId'],'model':MODEL,'runId':run_id,'valid':isinstance(result,dict) and isinstance(result.get('handoffNote'),str),'handoffNote':None if not isinstance(result,dict) else result.get('handoffNote'),'stopCode':ex.loop_result.stop_code.value,'usage':ex.loop_result.usage,'elapsedMs':elapsed}


def main():
    cases=json.loads((ROOT/'cases-s3-v1.json').read_text())
    rows=[]
    out=ROOT/'evidence-s3-predecessor-notes.json'
    for i,case in enumerate(cases['scenarios'],1):
        try: row=generate(case)
        except Exception as e: row={'scenarioId':case['scenarioId'],'model':MODEL,'valid':False,'handoffNote':None,'stopCode':'exception','errorType':type(e).__name__,'error':str(e)[:1500]}
        rows.append(row)
        payload={'schemaVersion':1,'kind':'ordivon.computing.aic-s3-predecessor-notes','experimentId':'COJC-J3-AIC-AGENT-REPLACEMENT-S3','futureShockVisibility':'NONE','rows':rows}
        out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'i':i,'scenarioId':row['scenarioId'],'valid':row['valid'],'note':(row.get('handoffNote') or '')[:220],'error':row.get('error')},ensure_ascii=False),flush=True)
    if not all(r['valid'] for r in rows): raise SystemExit(2)

if __name__=='__main__': main()
