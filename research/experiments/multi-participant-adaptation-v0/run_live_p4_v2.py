from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
HERE=Path(__file__).resolve().parent
COMPUTING_ROOT=HERE.parents[2]
HOST_ROOT=Path('/root/projects/ordivon-host'); HARNESS_ROOT=Path('/root/projects/ordivon-harness'); RUNTIME_ROOT=Path('/root/projects/ordivon-runtime')
for p in (COMPUTING_ROOT/'packages/ordivon-protocol/src',HOST_ROOT/'src',HARNESS_ROOT/'src',HERE):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from anc_canonical import canonical_digest
from ordivon_harness.api import AgentTurnRequest, DeepSeekSettings, DeepSeekTurnAdapter
from ordivon_harness.core import AgentTurnAdapterError
from evaluator import evaluate_candidate, join_verified
from host_coordination import exercise_host_coordination
COMPLETION={'mode':'structured-result-v1','resultKind':'p4-repair-candidate-v1','resultSchema':{'type':'object','additionalProperties':False,'properties':{'source':{'type':'string','minLength':1,'maxLength':12000},'summary':{'type':'string','minLength':1,'maxLength':1600}},'required':['source','summary']}}
NO_TOOLS=canonical_digest({'tools':[]})

def git(repo:Path,*args:str)->str:
    return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True,text=True).stdout.strip()
def usage_tokens(u:dict[str,Any])->int:
    for k in ('totalTokens','total_tokens'):
        if isinstance(u.get(k),int): return u[k]
    return 0

def prompt_for(s:dict[str,Any],participant:str)->str:
    return json.dumps({'experiment':'P4-MULTI-LIVE','participantRef':participant,'objective':'Repair the bounded pure-Python function from the exact visible specification.','rules':['Return complete Python module source defining exactly the requested function.','Do not use imports, file/network/process I/O, eval/exec/compile, or hidden-test claims.','The visible examples are evidence; an independent verifier owns acceptance.','Prefer a direct implementation of the written specification rather than patching only visible examples.'],'functionName':s['functionName'],'spec':s['spec'],'buggySource':s['buggySource'],'visibleCases':s['visibleCases']},sort_keys=True,ensure_ascii=False)
def invoke(settings:DeepSeekSettings,*,scenario:dict[str,Any],participant:str,run_id:str,assignment_id:str,sequence:int,messages:tuple[dict[str,str],...])->dict[str,Any]:
    attempts=[]; total_tokens=0; last_failure=None
    for attempt_index in (1,2):
        effective_messages=messages
        if attempt_index==2:
            correction={'role':'user','content':'Provider presentation correction only: submit the required structured candidate result with exactly source and summary fields. Do not change the task, evidence, participant role, or hidden-verifier assumptions.'}
            effective_messages=(*messages,correction)
        adapter=DeepSeekTurnAdapter(settings,completion_contract=COMPLETION)
        context=canonical_digest({'messages':list(effective_messages),'participantRef':participant,'scenarioId':scenario['scenarioId'],'presentationAttempt':attempt_index})
        req=AgentTurnRequest(harness_run_id=run_id,turn_id=f'turn:{run_id.split(":",1)[-1]}:{sequence}:presentation-{attempt_index}',sequence=sequence,assignment_id=assignment_id,context_digest=context,tool_catalog_digest=NO_TOOLS,messages=effective_messages,tools=(),remaining_budget={'modelCalls':1,'toolCalls':0,'totalTokens':16384,'wallTimeMs':90000})
        try:
            result=adapter.invoke(req)
        except AgentTurnAdapterError as error:
            attempts.append({'attempt':attempt_index,'requestDigest':req.digest,'providerRequestDigest':adapter.provider_request_digest(req),'validPresentation':False,'failure':type(error).__name__+': '+str(error),'failureCode':getattr(error.failure_code,'value',str(error.failure_code)),'dispatchSafety':getattr(error.dispatch_safety,'value',str(error.dispatch_safety))})
            last_failure=type(error).__name__+': '+str(error)
            continue
        tokens=usage_tokens(result.usage); total_tokens+=tokens
        evidence={'attempt':attempt_index,'requestDigest':req.digest,'providerRequestDigest':adapter.provider_request_digest(req),'resultDigest':result.digest,'modelCallId':result.model_call_id,'modelId':result.model_id,'effectiveModelId':result.effective_model,'usage':result.usage,'totalTokens':tokens,'rawResponseDigest':result.raw_response_digest,'validPresentation':result.conclusion is not None}
        if result.conclusion is None:
            evidence['failure']='missing_structured_conclusion'; attempts.append(evidence); last_failure='Provider omitted structured conclusion'; continue
        value=json.loads(result.conclusion.summary)
        if set(value)!={'source','summary'}: raise RuntimeError('candidate result fields differ')
        attempts.append(evidence)
        return {'source':value['source'],'summary':value['summary'],'modelEvidence':{'attempts':attempts,'providerAttempts':len(attempts),'presentationCorrections':len(attempts)-1,'totalTokens':total_tokens,'acceptedAttempt':attempt_index,'modelId':result.model_id,'effectiveModelId':result.effective_model}}
    raise RuntimeError('Provider presentation remained invalid after one correction: '+str(last_failure))

def artifact(candidate_id:str,participant:str,value:dict[str,Any],evaluation:dict[str,Any])->dict[str,Any]:
    source_digest='sha256:'+hashlib.sha256(value['source'].encode()).hexdigest(); payload={'schemaVersion':1,'kind':'ordivon.p4-candidate-artifact','candidateId':candidate_id,'participantRef':participant,'sourceDigest':source_digest,'summary':value['summary']}; digest=canonical_digest(payload)
    return {'candidateId':candidate_id,'participantRef':participant,'source':value['source'],'sourceDigest':source_digest,'summary':value['summary'],'artifactDigest':digest,'evaluation':evaluation,'modelEvidence':value['modelEvidence']}
def visible_feedback(ev:dict[str,Any])->dict[str,Any]:
    v=ev['visible']; failures=[{'caseIndex':i,'observed':r.get('observed')} for i,r in enumerate(v['caseResults']) if not r.get('ok')]
    return {'safe':v['safe'],'gateReason':v.get('gateReason'),'passed':v['passed'],'total':v['total'],'allPassed':v['allPassed'],'failures':failures}
def run_treatment(settings:DeepSeekSettings,s:dict[str,Any],hidden:list[dict[str,Any]],treatment:str)->dict[str,Any]:
    sid=s['scenarioId']; system={'role':'system','content':'You are one bounded repository-repair participant. Work from explicit visible evidence; independent verification owns acceptance.'}
    candidates=[]
    if treatment=='single-reflect':
        participant='participant:p4:single'; base=prompt_for(s,participant); run_id=f'harness-run:p4:{sid}:single'; assignment=f'assignment:p4:{sid}:single'
        first=invoke(settings,scenario=s,participant=participant,run_id=run_id,assignment_id=assignment,sequence=1,messages=(system,{'role':'user','content':base})); first_vis=evaluate_candidate(s,first['source']); candidates.append(artifact(f'{sid}:single:first',participant,first,evaluate_candidate(s,first['source'],hidden)))
        feedback=json.dumps({'previousCandidate':{'source':first['source'],'summary':first['summary']},'visibleVerifier':visible_feedback(first_vis),'instruction':'Produce the final revision candidate. You may keep the previous source unchanged if the written spec is already satisfied; otherwise repair it. Hidden verifier results are unavailable.'},sort_keys=True,ensure_ascii=False)
        reflection_context=json.dumps({'frozenTask':json.loads(base),'priorCandidate':{'source':first['source'],'summary':first['summary']},'visibleVerifier':visible_feedback(first_vis),'instruction':'Produce the second semantic candidate slot as a revision or justified retention of the prior candidate. Hidden verifier results are unavailable.'},sort_keys=True,ensure_ascii=False)
        second=invoke(settings,scenario=s,participant=participant,run_id=run_id,assignment_id=assignment,sequence=2,messages=(system,{'role':'user','content':reflection_context})); candidates.append(artifact(f'{sid}:single:revision',participant,second,evaluate_candidate(s,second['source'],hidden)))
    else:
        for label in ('a','b'):
            participant=f'participant:p4:branch-{label}'; base=prompt_for(s,participant); run_id=f'harness-run:p4:{sid}:branch-{label}'; assignment=f'assignment:p4:{sid}:branch-{label}'; value=invoke(settings,scenario=s,participant=participant,run_id=run_id,assignment_id=assignment,sequence=1,messages=(system,{'role':'user','content':base})); candidates.append(artifact(f'{sid}:branch-{label}',participant,value,evaluate_candidate(s,value['source'],hidden)))
    join=join_verified(candidates); host=exercise_host_coordination(scenario_id=sid,treatment=treatment,candidates=candidates,join=join)
    return {'scenarioId':sid,'treatment':treatment,'valid':True,'candidates':candidates,'join':join,'hostCoordination':host,'tokens':sum(c['modelEvidence']['totalTokens'] for c in candidates),'providerAttempts':sum(c['modelEvidence']['providerAttempts'] for c in candidates),'presentationCorrections':sum(c['modelEvidence']['presentationCorrections'] for c in candidates),'acceptedCandidateCount':sum(c['evaluation']['authoritative']['allPassed'] for c in candidates),'authoritativeCasesPassed':sum(c['evaluation']['authoritative']['passed'] for c in candidates),'authoritativeCasesTotal':sum(c['evaluation']['authoritative']['total'] for c in candidates)}
def aggregate(rows:list[dict[str,Any]],treatment:str)->dict[str,Any]:
    r=[x for x in rows if x['treatment']==treatment and x.get('valid')]; invalid=sum(1 for x in rows if x['treatment']==treatment and not x.get('valid'))
    return {'scenarios':len(r),'invalidScenarios':invalid,'acceptedGoals':sum(x['join']['accepted'] for x in r),'acceptedCandidates':sum(x['acceptedCandidateCount'] for x in r),'authoritativeCasesPassed':sum(x['authoritativeCasesPassed'] for x in r),'authoritativeCasesTotal':sum(x['authoritativeCasesTotal'] for x in r),'totalTokens':sum(x['tokens'] for x in r),'providerAttempts':sum(x['providerAttempts'] for x in r),'presentationCorrections':sum(x['presentationCorrections'] for x in r),'branchEffectIntents':sum(x['hostCoordination']['branchEffectIntentCount'] for x in r),'responsibilityAmbiguities':sum(x['hostCoordination']['responsibilityAmbiguous'] for x in r),'recoveryFailures':sum(not x['hostCoordination']['partialApplyRecoveryPassed'] for x in r),'rejectedAdvanceFailures':sum(x['join']['accepted'] is False and x['hostCoordination']['rejectedAdvanceBlocked'] is not True for x in r)}
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--secret',type=Path,default=Path('/root/.config/ordivon/secrets/deepseek.json')); ap.add_argument('--output-dir',type=Path,required=True); args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    settings=DeepSeekSettings.from_secret_file(args.secret,max_output_tokens=3200,timeout_seconds=90.0); corpus=json.loads((HERE/'fixtures/corpus.json').read_text())['scenarios']; hidden=json.loads((HERE/'fixtures/evaluator-cases.json').read_text())['casesByScenario']; plan=json.loads((HERE/'plan-v2.json').read_text())
    owners={'computing':git(COMPUTING_ROOT,'rev-parse','HEAD'),'host':git(HOST_ROOT,'rev-parse','HEAD'),'harness':git(HARNESS_ROOT,'rev-parse','HEAD'),'runtime':git(RUNTIME_ROOT,'rev-parse','HEAD')}
    all_rows=[]
    for split in ('development','holdout'):
        rows=[]
        scenarios=[s for s in corpus if s['split']==split]
        for index,s in enumerate(scenarios):
            order=('single-reflect','multi-independent') if index%2==0 else ('multi-independent','single-reflect')
            for treatment in order:
                try: rows.append(run_treatment(settings,s,hidden[s['scenarioId']],treatment))
                except Exception as e: rows.append({'scenarioId':s['scenarioId'],'treatment':treatment,'valid':False,'failure':type(e).__name__+': '+str(e)})
        metrics={t:aggregate(rows,t) for t in ('single-reflect','multi-independent')}; record={'schemaVersion':1,'kind':f'ordivon.p4-{split}','ownerRevisions':owners,'provider':{'adapterId':DeepSeekTurnAdapter.adapter_id,'model':settings.model,'credentialScopeId':settings.credential_scope_id},'rows':rows,'metrics':metrics}; (args.output_dir/f'{split}.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n'); all_rows.extend(rows)
    dev=json.loads((args.output_dir/'development.json').read_text())['metrics']; hold=json.loads((args.output_dir/'holdout.json').read_text())['metrics']; bdev=dev['single-reflect']; mdev=dev['multi-independent']; bhold=hold['single-reflect']; mhold=hold['multi-independent']
    token_ratio=(mdev['totalTokens']+mhold['totalTokens'])/max(1,bdev['totalTokens']+bhold['totalTokens']); gain_dev=mdev['acceptedGoals']-bdev['acceptedGoals']; gain_hold=mhold['acceptedGoals']-bhold['acceptedGoals']; safety=all(m[k]==0 for m in (mdev,mhold) for k in ('branchEffectIntents','responsibilityAmbiguities','recoveryFailures','rejectedAdvanceFailures')); valid=all(x.get('valid') for x in all_rows)
    positive=valid and gain_dev>0 and gain_hold>0 and gain_dev+gain_hold>=plan['multiPromotionRule']['combinedMinimumAcceptedGoalGain'] and token_ratio<=plan['multiPromotionRule']['maxTokenRatio'] and safety
    disposition='retain_multi_participant_pattern_existing_host_primitives' if positive else ('reject_generic_multi_agent_advantage' if valid else 'incomplete_provider_or_apparatus_failure')
    close={'schemaVersion':2,'kind':'ordivon.p4-multi-closeout','ownerRevisions':owners,'validCampaign':valid,'developmentMetrics':dev,'holdoutMetrics':hold,'acceptedGoalGain':{'development':gain_dev,'holdout':gain_hold,'combined':gain_dev+gain_hold},'tokenRatioMultiToBaseline':token_ratio,'coordinationSafetyPassed':safety,'multiPromotionRulePassed':positive,'disposition':disposition,'newCoordinationPrimitiveAuthorized':False,'reason':'Even positive cognitive diversity does not authorize a new coordination layer unless existing Task/Artifact/Goal coordination fails a repeated responsibility.','providerPresentationPolicy':plan['presentationRepair']['providerRetryPolicy'],'claimLimit':'one bounded pure-Python repository-repair family; no open-ended multi-Agent or RSI claim'}; (args.output_dir/'closeout.json').write_text(json.dumps(close,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'dev':dev,'hold':hold,'gain':close['acceptedGoalGain'],'tokenRatio':token_ratio,'safety':safety,'disposition':disposition},sort_keys=True)); return 0 if valid else 2
if __name__=='__main__': raise SystemExit(main())
