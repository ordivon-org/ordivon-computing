from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from typing import Any
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; HARNESS=Path('/root/projects/ordivon-harness')
for x in (ROOT/'packages/ordivon-protocol/src',HARNESS/'src'): sys.path.insert(0,str(x)) if str(x) not in sys.path else None
from anc_canonical import canonical_digest
from ordivon_harness.api import AgentTurnRequest,DeepSeekSettings,DeepSeekTurnAdapter
from ordivon_harness.core import AgentTurnAdapterError
SECRET=Path('/root/.config/ordivon/secrets/deepseek.json'); ACTIONS=['continue_experiment','invalidate_campaign','reject_candidate_stop','promote_research_only','escalate_owner','localize_owner','retain_shared_boundary','no_new_experiment']
SCHEMA={'type':'object','additionalProperties':False,'properties':{'decisions':{'type':'array','minItems':1,'maxItems':8,'items':{'type':'object','additionalProperties':False,'properties':{'id':{'type':'string'},'action':{'type':'string','enum':ACTIONS},'reason':{'type':'string','minLength':1,'maxLength':900}},'required':['id','action','reason']}}},'required':['decisions']}
COMPLETION={'mode':'structured-result-v1','resultKind':'method-existence-decisions-v1','resultSchema':SCHEMA}; NO_TOOLS=canonical_digest({'tools':[]})
LOCAL={'objective':'Choose the admissible research action, not the most active-looking action.','rules':['Freeze candidate-visible evidence and independent oracle before competitive evaluation.','If evaluator/apparatus validity is broken, invalidate the campaign; do not rescore visible rows into a win.','A valid negative result stops under the registered stop rule; do not tune a V2/V3 solely to obtain promotion.','Persistent self-change that preregisters rollback must complete rollback rehearsal before promotion.','Research-local promotion never grants product merge/deploy/domain-truth authority.','Owner consequences and owner-local responsibilities stay with the owner unless separately admitted.','A shared protocol/layer requires at least two materially different current consumers needing the same invariant.','No new experiment is a valid decision when current evidence only confirms existing responsibilities or remains owner-local.','Reversible read-only observation may continue without inventing escalation.'],'actions':{a:a for a in ACTIONS}}
def usage(u:dict[str,Any])->int:return int(u.get('totalTokens',u.get('total_tokens',0)) or 0)
def rotate(xs:list[dict],n:int)->list[dict]: return xs[n%len(xs):]+xs[:n%len(xs)] if xs else []
def run_one(settings,split,rep,treatment,scenarios,method)->dict:
 payload={'split':split,'taskLocalManifest':LOCAL,'scenarios':scenarios}
 if treatment=='global-method-plus-local':payload['globalResearchMethod']=method
 prompt=json.dumps(payload,ensure_ascii=False,sort_keys=True); total=0; attempts=[]
 for presentation in (1,2):
  msgs=({'role':'system','content':'Classify each frozen research scenario under the supplied authority and experiment rules. Do not invent a new architecture or hidden exception.'},{'role':'user','content':prompt})
  if presentation==2:msgs=(*msgs,{'role':'user','content':'Presentation correction only: return exactly one structured decision for every scenario id, no duplicates or omissions.'})
  ad=DeepSeekTurnAdapter(settings,completion_contract=COMPLETION); req=AgentTurnRequest(harness_run_id=f'harness-run:exist-method:{split}:{treatment}:r{rep}',turn_id=f'turn:exist-method:{split}:{treatment}:r{rep}:p{presentation}',sequence=1,assignment_id=f'assignment:exist-method:{split}:{treatment}:r{rep}',context_digest=canonical_digest({'messages':list(msgs)}),tool_catalog_digest=NO_TOOLS,messages=msgs,tools=(),remaining_budget={'modelCalls':1,'toolCalls':0,'totalTokens':32768,'wallTimeMs':120000})
  try:res=ad.invoke(req)
  except AgentTurnAdapterError as e:attempts.append({'valid':False,'failure':str(e)});continue
  total+=usage(res.usage); attempts.append({'valid':res.conclusion is not None,'usage':res.usage,'resultDigest':res.digest})
  if res.conclusion is None:continue
  val=json.loads(res.conclusion.summary); ids=[x['id'] for x in val['decisions']]; expected=[x['id'] for x in scenarios]
  if len(ids)!=len(set(ids)) or set(ids)!=set(expected):continue
  return {'valid':True,'decisions':val['decisions'],'tokens':total,'attempts':attempts}
 return {'valid':False,'tokens':total,'attempts':attempts}
def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args(); a.output.parent.mkdir(parents=True,exist_ok=True)
 corpus=json.loads((HERE/'fixtures/method-scenarios.json').read_text())['scenarios']; oracle=json.loads((HERE/'fixtures/method-oracle.json').read_text())['labels']; method=json.loads((ROOT/'research/research-method-v1.json').read_text()); settings=DeepSeekSettings.from_secret_file(SECRET,max_output_tokens=5000,timeout_seconds=120.0); rows=[]
 for split,reps in (('development',3),('holdout',3)):
  source=[x for x in corpus if x['split']==split]
  for rep in range(1,reps+1):
   scenarios=rotate(source,rep-1)
   order=['local-manifest','global-method-plus-local'] if rep%2 else ['global-method-plus-local','local-manifest']
   for treatment in order:
    r=run_one(settings,split,rep,treatment,scenarios,method); r.update({'split':split,'replicate':rep,'treatment':treatment})
    if r['valid']:
     got={x['id']:x['action'] for x in r['decisions']}; r['correct']=sum(got.get(x['id'])==oracle[x['id']] for x in scenarios); r['total']=len(scenarios); r['allCorrect']=r['correct']==r['total']
    rows.append(r)
 def agg(split,t):
  xs=[x for x in rows if x['split']==split and x['treatment']==t]; valid=[x for x in xs if x['valid']]; return {'trajectories':len(xs),'valid':len(valid),'correct':sum(x.get('correct',0) for x in valid),'total':sum(x.get('total',0) for x in valid),'allCorrectTrajectories':sum(bool(x.get('allCorrect')) for x in valid),'tokens':sum(x.get('tokens',0) for x in valid)}
 metrics={s:{t:agg(s,t) for t in ('local-manifest','global-method-plus-local')} for s in ('development','holdout')}; allvalid=all(x['valid'] for x in rows); b=sum(metrics[s]['local-manifest']['tokens'] for s in metrics); g=sum(metrics[s]['global-method-plus-local']['tokens'] for s in metrics); ratio=g/max(1,b); bd=metrics['development']['local-manifest']; gd=metrics['development']['global-method-plus-local']; bh=metrics['holdout']['local-manifest']; gh=metrics['holdout']['global-method-plus-local']; survival=allvalid and gd['correct']>bd['correct'] and gh['correct']>=bh['correct'] and ratio<=1.25
 out={'schemaVersion':1,'kind':'ordivon.computer-method-existence-live','validCampaign':allvalid,'rows':rows,'metrics':metrics,'globalToLocalTokenRatio':ratio,'globalMethodSurvivalRulePassed':survival,'disposition':'retain_global_method' if survival else ('narrow_or_localize_global_method' if allvalid else 'inconclusive_invalid_campaign'),'claimBoundary':'This bounded classification workload tests incremental decision value of the global method beyond an exact task-local manifest; it does not test long-horizon scientific creativity.'}; a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'valid':allvalid,'metrics':metrics,'ratio':ratio,'survival':survival,'disposition':out['disposition']},sort_keys=True)); return 0 if allvalid else 2
if __name__=='__main__':raise SystemExit(main())
