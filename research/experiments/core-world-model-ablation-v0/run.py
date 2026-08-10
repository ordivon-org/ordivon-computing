from __future__ import annotations
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; HARNESS=Path('/root/projects/ordivon-harness')
for x in (ROOT/'packages/ordivon-protocol/src',HARNESS/'src'):
 if str(x) not in sys.path: sys.path.insert(0,str(x))
from anc_canonical import canonical_digest
from ordivon_harness.api import AgentTurnRequest,DeepSeekSettings,DeepSeekTurnAdapter
from ordivon_harness.core import AgentTurnAdapterError
SECRET=Path('/root/.config/ordivon/secrets/deepseek.json')
ACTIONS=['no_new_shared_layer','bounded_not_open_ended','owner_runtime','owner_local_plus_runtime','compatibility_migration','narrow_metadata_only','no_new_phase']
SCHEMA={'type':'object','additionalProperties':False,'properties':{'decisions':{'type':'array','minItems':8,'maxItems':8,'items':{'type':'object','additionalProperties':False,'properties':{'id':{'type':'string'},'action':{'type':'string','enum':ACTIONS},'reason':{'type':'string','minLength':1,'maxLength':700}},'required':['id','action','reason']}}},'required':['decisions']}
CONTRACT={'mode':'structured-result-v1','resultKind':'core-ablation-decisions-v1','resultSchema':SCHEMA}; NO_TOOLS=canonical_digest({'tools':[]})
def read(p):return p.read_text(errors='replace')
def core_context():return '\n\n'.join(f'===== {p} =====\n{read(p)}' for p in sorted((ROOT/'core').glob('*.md')))
def raw_context():
 paths=[ROOT/'research/portfolio.json',ROOT/'research/computer-responsibility-map-v1.json',ROOT/'research/experiments/computer-existence-gauntlet-v0/existence-gauntlet-v1-closeout.json']
 return '\n\n'.join(f'===== {p.relative_to(ROOT)} =====\n{read(p)}' for p in paths)
def rotate(xs,n):return xs[n%len(xs):]+xs[:n%len(xs)]
def tokens(u):return int(u.get('totalTokens',u.get('total_tokens',0)) or 0)
def invoke(settings,treatment,rep,cards):
 ctx=raw_context() if treatment=='raw-control' else core_context(); payload={'task':'For every exact evidence card, choose the narrowest justified architecture/responsibility conclusion. Null action is valid. Do not invent a shared layer.','cards':cards,'contextKind':treatment,'context':ctx}; prompt=json.dumps(payload,ensure_ascii=False,sort_keys=True)
 total_tokens=0; failures=[]
 for attempt in (1,2):
  ad=DeepSeekTurnAdapter(settings,completion_contract=CONTRACT); req=AgentTurnRequest(harness_run_id=f'harness-run:core-ablation:{treatment}:r{rep}',turn_id=f'turn:core-ablation:{treatment}:r{rep}:a{attempt}',sequence=1,assignment_id=f'assignment:core-ablation:{treatment}:r{rep}',context_digest=canonical_digest({'messages':[{'role':'user','content':prompt}]}),tool_catalog_digest=NO_TOOLS,messages=({'role':'system','content':'Use only supplied exact evidence/context. Prefer owner-local or no-new-layer conclusions unless the evidence proves a shared invariant.'},{'role':'user','content':prompt}),tools=(),remaining_budget={'modelCalls':1,'toolCalls':0,'totalTokens':65536,'wallTimeMs':120000})
  try:r=ad.invoke(req)
  except AgentTurnAdapterError as e:
   failures.append(str(e)); continue
  total_tokens+=tokens(r.usage)
  if r.conclusion is None:return {'valid':False,'error':'missing structured conclusion','tokens':total_tokens,'transportFailures':failures}
  d=json.loads(r.conclusion.summary); ids=[x['id'] for x in d['decisions']]; expected=[x['id'] for x in cards]
  if len(ids)!=8 or len(set(ids))!=8 or set(ids)!=set(expected):return {'valid':False,'error':'id set mismatch','tokens':total_tokens,'decisions':d.get('decisions'),'transportFailures':failures}
  return {'valid':True,'tokens':total_tokens,'decisions':d['decisions'],'resultDigest':r.digest,'transportFailures':failures}
 return {'valid':False,'error':failures[-1] if failures else 'adapter failure','tokens':total_tokens,'transportFailures':failures}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args(); cards=json.loads((HERE/'fixtures/cards.json').read_text())['cards']; oracle=json.loads((HERE/'fixtures/oracle.json').read_text())['labels']; settings=DeepSeekSettings.from_secret_file(SECRET,max_output_tokens=5000,timeout_seconds=120); rows=[]
 for rep in range(1,4):
  ordered=rotate(cards,rep-1); treatments=['raw-control','core-compressed'] if rep%2 else ['core-compressed','raw-control']
  for t in treatments:
   x=invoke(settings,t,rep,ordered); x.update({'treatment':t,'replicate':rep});
   if x['valid']:
    got={d['id']:d['action'] for d in x['decisions']}; x['correct']=sum(got[k]==oracle[k] for k in oracle); x['wrong']=[{'id':k,'got':got[k],'expected':oracle[k]} for k in oracle if got[k]!=oracle[k]]
   rows.append(x)
 def agg(t):
  xs=[x for x in rows if x['treatment']==t]; return {'valid':sum(x['valid'] for x in xs),'correct':sum(x.get('correct',0) for x in xs),'tokens':sum(x.get('tokens',0) for x in xs),'replicateCorrect':[x.get('correct') for x in xs]}
 raw=agg('raw-control'); core=agg('core-compressed'); valid=raw['valid']==3 and core['valid']==3; ratio=core['tokens']/max(1,raw['tokens']); rep_ok=all(c is not None and r is not None and c>=r-1 for c,r in zip(core['replicateCorrect'],raw['replicateCorrect'])); retain=valid and core['correct']>=raw['correct']-1 and rep_ok and ratio<=0.75; delete=valid and raw['correct']>core['correct'] and raw['tokens']<=core['tokens']; disposition='retain_core_compression' if retain else ('delete_core_candidate' if delete else 'narrow_core')
 out={'schemaVersion':1,'kind':'ordivon.core-world-model-ablation-result','validCampaign':valid,'rows':rows,'metrics':{'raw-control':raw,'core-compressed':core},'coreToRawTokenRatio':ratio,'retainRulePassed':retain,'deleteRulePassed':delete,'disposition':disposition,'claimBoundary':'Tests bounded current architecture/responsibility decisions from exact evidence cards; does not prove every future reader benefits from Core.'}; a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+'\n'); print(json.dumps({'valid':valid,'raw':raw,'core':core,'ratio':ratio,'disposition':disposition},indent=2)); return 0 if valid else 2
if __name__=='__main__':raise SystemExit(main())
