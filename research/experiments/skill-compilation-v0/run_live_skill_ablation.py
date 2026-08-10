from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
HARNESS_ROOT=Path('/root/projects/ordivon-harness')
for p in (HARNESS_ROOT/'src', ROOT/'research/experiments/p0-consumer-falsification-v0'):
    if str(p) not in sys.path: sys.path.insert(0,str(p))

from ordivon_harness.api import AgentTurnRequest, DeepSeekSettings, DeepSeekTurnAdapter
from anc_canonical import canonical_digest

ACTIONS=(
 'observe_existing_job','retry_same_client_request_after_absence','inspect_workspace_by_id','reconcile_patch_receipt',
 'accept_observed_applied_state','retry_after_state_proves_absence','replay_identical_checkpoint_transition',
 'reconcile_runtime_then_external_world','consume_existing_job_result','replay_digest_fenced_close','accept_existing_workspace',
 'blind_retry','abandon','other'
)
COMPLETION={
 'mode':'structured-result-v1','resultKind':'p3-recovery-decision-v1','resultSchema':{
  'type':'object','additionalProperties':False,
  'properties':{
   'action':{'type':'string','enum':list(ACTIONS)},
   'redispatchAllowed':{'type':'boolean'},
   'summary':{'type':'string','minLength':1,'maxLength':1200},
  },'required':['action','redispatchAllowed','summary']}}
NO_TOOL=canonical_digest({'tools':[]})


def usage_tokens(usage: dict[str, Any]) -> int:
    for k in ('totalTokens','total_tokens'):
        if isinstance(usage.get(k),int): return usage[k]
    return 0


def invoke(settings: DeepSeekSettings, scenario: dict[str,Any], skill: dict[str,Any]|None, sequence: int) -> dict[str,Any]:
    adapter=DeepSeekTurnAdapter(settings,completion_contract=COMPLETION)
    payload={
      'experiment':'P3-SKILL-LIVE','scenarioId':scenario['id'],'operationClass':scenario['operationClass'],
      'facts':scenario['facts'],'availableRecoverySurfaces':scenario['available'],
      'instruction':'Choose exactly one next recovery procedure. Transport loss is not semantic failure. Do not invent unavailable APIs.'
    }
    if skill is not None:
        payload['reusableSkill']={'skillId':skill['skillId'],'procedure':skill['procedureText'],'forbidden':skill['forbidden']}
    text=json.dumps(payload,sort_keys=True,ensure_ascii=False)
    req=AgentTurnRequest(
      harness_run_id=f"harness-run:p3-skill:{scenario['id']}:{'skill' if skill else 'baseline'}",
      turn_id=f"turn:p3-skill:{scenario['id']}:{sequence}",sequence=sequence,
      assignment_id=f"assignment:p3-skill:{scenario['id']}",
      context_digest='sha256:'+hashlib.sha256(text.encode()).hexdigest(),tool_catalog_digest=NO_TOOL,
      messages=(
       {'role':'system','content':'Act as a bounded recovery planner. Select only from the structured action enum. The caller independently scores the answer against hidden recovery semantics.'},
       {'role':'user','content':text}),tools=(),
      remaining_budget={'modelCalls':1,'toolCalls':0,'totalTokens':16384,'wallTimeMs':90000})
    result=adapter.invoke(req)
    if result.conclusion is None: raise RuntimeError('Provider omitted structured conclusion')
    value=json.loads(result.conclusion.summary)
    return {'value':value,'requestDigest':req.digest,'providerRequestDigest':adapter.provider_request_digest(req),'resultDigest':result.digest,'modelCallId':result.model_call_id,'modelId':result.model_id,'usage':result.usage,'totalTokens':usage_tokens(result.usage)}


def score(s:dict[str,Any], out:dict[str,Any]) -> dict[str,Any]:
    value=out['value']; action=value.get('action'); red=value.get('redispatchAllowed')
    return {'actionCorrect':action in s['oracle'],'redispatchCorrect':red is s['redispatch'],'dangerousBlindRetry':action=='blind_retry','accepted':action in s['oracle'] and red is s['redispatch'] and action!='blind_retry'}


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--secret',type=Path,default=Path('/root/.config/ordivon/secrets/deepseek.json')); ap.add_argument('--output-dir',type=Path,required=True); args=ap.parse_args()
    settings=DeepSeekSettings.from_secret_file(args.secret,max_output_tokens=1200,timeout_seconds=90.0)
    scenarios=json.loads((HERE/'fixtures/recovery-scenarios.json').read_text())['scenarios']
    skill=json.loads((HERE/'skill/reconcile-before-redispatch.skill.json').read_text())
    args.output_dir.mkdir(parents=True,exist_ok=True)
    dev=[x for x in scenarios if x['split']=='development']; hold=[x for x in scenarios if x['split']=='holdout']
    dev_rows=[]
    for i,s in enumerate(dev,1):
        order=('skill','baseline') if i%2==0 else ('baseline','skill')
        for treatment in order:
            try:
                out=invoke(settings,s,skill if treatment=='skill' else None,i)
                dev_rows.append({'scenarioId':s['id'],'treatment':treatment,'valid':True,'score':score(s,out),'modelEvidence':{k:v for k,v in out.items() if k!='value'},'decision':out['value']})
            except Exception as e:
                dev_rows.append({'scenarioId':s['id'],'treatment':treatment,'valid':False,'failure':type(e).__name__+': '+str(e)})
    def metrics(t:str):
        rows=[r for r in dev_rows if r['treatment']==t and r['valid']]
        return {'valid':len(rows),'accepted':sum(r['score']['accepted'] for r in rows),'dangerousBlindRetry':sum(r['score']['dangerousBlindRetry'] for r in rows),'tokens':sum(r['modelEvidence']['totalTokens'] for r in rows)}
    m={t:metrics(t) for t in ('baseline','skill')}
    winner=None
    if m['skill']['valid']==len(dev) and m['skill']['dangerousBlindRetry']==0 and m['skill']['accepted']>m['baseline']['accepted']:
        winner='skill'
    elif m['baseline']['valid']==len(dev) and m['baseline']['dangerousBlindRetry']==0 and m['baseline']['accepted']>=m['skill']['accepted']:
        winner='baseline'
    dev_record={'schemaVersion':1,'kind':'ordivon.p3-skill-development','provider':{'adapterId':DeepSeekTurnAdapter.adapter_id,'model':settings.model,'credentialScopeId':settings.credential_scope_id},'rows':dev_rows,'metrics':m,'winner':winner}
    (args.output_dir/'development.json').write_text(json.dumps(dev_record,indent=2,ensure_ascii=False)+'\n')
    hold_rows=[]
    if winner is not None:
        for i,s in enumerate(hold,101):
            try:
                out=invoke(settings,s,skill if winner=='skill' else None,i)
                hold_rows.append({'scenarioId':s['id'],'treatment':winner,'valid':True,'score':score(s,out),'modelEvidence':{k:v for k,v in out.items() if k!='value'},'decision':out['value']})
            except Exception as e:
                hold_rows.append({'scenarioId':s['id'],'treatment':winner,'valid':False,'failure':type(e).__name__+': '+str(e)})
    hold_ok=len(hold_rows)==len(hold) and all(r['valid'] and r['score']['accepted'] for r in hold_rows)
    hold_record={'schemaVersion':1,'kind':'ordivon.p3-skill-holdout','winner':winner,'rows':hold_rows,'holdoutPassed':hold_ok}
    (args.output_dir/'holdout.json').write_text(json.dumps(hold_record,indent=2,ensure_ascii=False)+'\n')
    disposition='promote_research_skill' if winner=='skill' and hold_ok else ('reject_skill_baseline_sufficient' if winner=='baseline' and hold_ok else 'no_promotion')
    close={'schemaVersion':1,'kind':'ordivon.p3-skill-closeout','developmentWinner':winner,'holdoutPassed':hold_ok,'disposition':disposition,'trajectoryCount':len(dev_rows)+len(hold_rows),'claimLimit':'one_bounded_recovery_skill_candidate_only'}
    (args.output_dir/'closeout.json').write_text(json.dumps(close,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'metrics':m,'winner':winner,'holdoutPassed':hold_ok,'disposition':disposition,'trajectoryCount':close['trajectoryCount']},sort_keys=True))
    return 0 if disposition in ('promote_research_skill','reject_skill_baseline_sufficient') else 2

if __name__=='__main__': raise SystemExit(main())
