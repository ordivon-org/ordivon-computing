from __future__ import annotations

import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
HARNESS_ROOT=Path('/root/projects/ordivon-harness')
for p in (HARNESS_ROOT/'src',):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from ordivon_harness.api import AgentTurnRequest, DeepSeekSettings, DeepSeekTurnAdapter
from anc_canonical import canonical_digest
ACTIONS=(
 'observe_runtime_job','readmit_runtime_request_after_no_job','inspect_workspace_by_explicit_id','accept_existing_workspace',
 'reconcile_patch_receipt','accept_exact_mutation_state','reapply_mutation_after_exact_absence','replay_identical_host_checkpoint',
 'reconcile_runtime_then_external_authority','consume_runtime_job_result','replay_digest_fenced_close','unsafe_blind_retry','other')
COMPLETION={'mode':'structured-result-v1','resultKind':'p3-recovery-decision-v2','resultSchema':{'type':'object','additionalProperties':False,'properties':{'action':{'type':'string','enum':list(ACTIONS)},'summary':{'type':'string','minLength':1,'maxLength':1200}},'required':['action','summary']}}
NO_TOOL=canonical_digest({'tools':[]})

def usage_tokens(u:dict[str,Any])->int:
    for k in ('totalTokens','total_tokens'):
        if isinstance(u.get(k),int): return u[k]
    return 0

def invoke(settings:DeepSeekSettings,s:dict[str,Any],skill:dict[str,Any]|None,seq:int)->dict[str,Any]:
    adapter=DeepSeekTurnAdapter(settings,completion_contract=COMPLETION)
    payload={'experiment':'P3-SKILL-LIVE-V2','scenarioId':s['id'],'operationClass':s['operationClass'],'facts':s['facts'],'currentToolContractFact':s['contractFact'],'availableRecoverySurfaces':s['available'],'instruction':'Choose the single next recovery action that is already justified now. Do not choose an action that is only conditionally allowed after another observation. Transport loss is not semantic failure.'}
    if skill is not None: payload['reusableSkill']={'skillId':skill['skillId'],'procedure':skill['procedureText'],'forbidden':skill['forbidden']}
    text=json.dumps(payload,sort_keys=True,ensure_ascii=False)
    req=AgentTurnRequest(harness_run_id=f"harness-run:p3-v2:{s['id']}:{'skill' if skill else 'baseline'}",turn_id=f"turn:p3-v2:{s['id']}:{seq}",sequence=seq,assignment_id=f"assignment:p3-v2:{s['id']}",context_digest='sha256:'+hashlib.sha256(text.encode()).hexdigest(),tool_catalog_digest=NO_TOOL,messages=({'role':'system','content':'Act as a bounded recovery planner. The action enum is mutually exclusive and the caller independently scores exact next-action correctness.'},{'role':'user','content':text}),tools=(),remaining_budget={'modelCalls':1,'toolCalls':0,'totalTokens':16384,'wallTimeMs':90000})
    result=adapter.invoke(req)
    if result.conclusion is None: raise RuntimeError('Provider omitted structured conclusion')
    value=json.loads(result.conclusion.summary)
    return {'value':value,'requestDigest':req.digest,'providerRequestDigest':adapter.provider_request_digest(req),'resultDigest':result.digest,'modelCallId':result.model_call_id,'modelId':result.model_id,'totalTokens':usage_tokens(result.usage),'usage':result.usage}

def score(s:dict[str,Any],o:dict[str,Any])->dict[str,Any]:
    a=o['value'].get('action'); return {'actionCorrect':a==s['oracle'],'dangerousBlindRetry':a=='unsafe_blind_retry','accepted':a==s['oracle'] and a!='unsafe_blind_retry'}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--secret',type=Path,default=Path('/root/.config/ordivon/secrets/deepseek.json')); ap.add_argument('--output-dir',type=Path,required=True); args=ap.parse_args()
    settings=DeepSeekSettings.from_secret_file(args.secret,max_output_tokens=1200,timeout_seconds=90.0)
    scenarios=json.loads((HERE/'fixtures/recovery-scenarios-v2.json').read_text())['scenarios']; skill=json.loads((HERE/'skill/reconcile-before-redispatch.skill.json').read_text())
    args.output_dir.mkdir(parents=True,exist_ok=True); dev=[x for x in scenarios if x['split']=='development']; hold=[x for x in scenarios if x['split']=='holdout']
    rows=[]
    for i,s in enumerate(dev,1):
        for treatment in (('baseline','skill') if i%2 else ('skill','baseline')):
            try:
                o=invoke(settings,s,skill if treatment=='skill' else None,i); rows.append({'scenarioId':s['id'],'treatment':treatment,'valid':True,'score':score(s,o),'decision':o['value'],'modelEvidence':{k:v for k,v in o.items() if k!='value'}})
            except Exception as e: rows.append({'scenarioId':s['id'],'treatment':treatment,'valid':False,'failure':type(e).__name__+': '+str(e)})
    def metric(t:str):
        r=[x for x in rows if x['treatment']==t and x['valid']]; return {'valid':len(r),'accepted':sum(x['score']['accepted'] for x in r),'dangerousBlindRetry':sum(x['score']['dangerousBlindRetry'] for x in r),'tokens':sum(x['modelEvidence']['totalTokens'] for x in r)}
    m={t:metric(t) for t in ('baseline','skill')}; winner=None
    if m['skill']['valid']==len(dev) and m['skill']['dangerousBlindRetry']==0 and m['skill']['accepted']>m['baseline']['accepted']: winner='skill'
    elif m['baseline']['valid']==len(dev) and m['baseline']['dangerousBlindRetry']==0 and m['baseline']['accepted']>=m['skill']['accepted']: winner='baseline'
    (args.output_dir/'development.json').write_text(json.dumps({'schemaVersion':2,'kind':'ordivon.p3-skill-development','rows':rows,'metrics':m,'winner':winner},indent=2,ensure_ascii=False)+'\n')
    h=[]
    if winner:
        for i,s in enumerate(hold,101):
            try:
                o=invoke(settings,s,skill if winner=='skill' else None,i); h.append({'scenarioId':s['id'],'treatment':winner,'valid':True,'score':score(s,o),'decision':o['value'],'modelEvidence':{k:v for k,v in o.items() if k!='value'}})
            except Exception as e: h.append({'scenarioId':s['id'],'treatment':winner,'valid':False,'failure':type(e).__name__+': '+str(e)})
    ok=len(h)==len(hold) and all(x['valid'] and x['score']['accepted'] for x in h)
    (args.output_dir/'holdout.json').write_text(json.dumps({'schemaVersion':2,'kind':'ordivon.p3-skill-holdout','winner':winner,'rows':h,'holdoutPassed':ok},indent=2,ensure_ascii=False)+'\n')
    disp='promote_research_skill' if winner=='skill' and ok else ('reject_skill_baseline_sufficient' if winner=='baseline' and ok else 'no_promotion')
    close={'schemaVersion':2,'kind':'ordivon.p3-skill-closeout','developmentWinner':winner,'holdoutPassed':ok,'disposition':disp,'trajectoryCount':len(rows)+len(h),'candidateSkillDigest':skill['integrity']['payloadDigest'],'evaluatorRepairRef':'evidence/live-ablation/evaluator-diagnosis.json','claimLimit':'one_bounded_recovery_skill_candidate_only'}
    (args.output_dir/'closeout.json').write_text(json.dumps(close,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'metrics':m,'winner':winner,'holdoutPassed':ok,'disposition':disp,'trajectoryCount':close['trajectoryCount']},sort_keys=True)); return 0 if disp in ('promote_research_skill','reject_skill_baseline_sufficient') else 2
if __name__=='__main__': raise SystemExit(main())
