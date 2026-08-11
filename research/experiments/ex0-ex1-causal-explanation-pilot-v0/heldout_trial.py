from __future__ import annotations
import argparse, hashlib, json, pathlib, random, time, urllib.error, urllib.request
from typing import Any
ROOT=pathlib.Path(__file__).resolve().parent
CORPUS=json.loads((ROOT/'heldout-corpus-v1.json').read_text(encoding='utf-8'))
STATIC=['CLASSICAL_SUBSTRATE','CALLER_OR_DOMAIN','NO_SHARED_MECHANISM']
def canonical(v:Any)->bytes:return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(v:Any)->str:return 'sha256:'+hashlib.sha256(canonical(v)).hexdigest()
def secret_paths():
 out=[]
 for p in sorted(pathlib.Path('/root/.config/ordivon/secrets').glob('deepseek*.json')):
  v=json.loads(p.read_text());
  if all(isinstance(v.get(k),str) and v[k] for k in ('apiKey','baseUrl','model')): out.append(p)
 if not out: raise RuntimeError('no usable DeepSeek secret')
 return out
def mapping(rep:int):
 labels=list(CORPUS['opaqueLabels']);random.Random(f'ex1c-labels:{rep}').shuffle(labels);return {'{{HOST}}':labels[0],'{{HARNESS}}':labels[1],'{{RUNTIME}}':labels[2]}
def render(s:str,m:dict[str,str]):
 for a,b in m.items():s=s.replace(a,b)
 return s
def call(sec,treatment,cases,m):
 ids=[c['id'] for c in cases];labels=list(CORPUS['opaqueLabels'])+STATIC
 expl=render(CORPUS['treatments'][treatment],m);visible=[{'caseId':c['id'],'scenario':render(c['scenario'],m)} for c in cases]
 tool={'type':'function','function':{'name':'submit_heldout','description':'Choose the smallest authority that owns the exact unresolved fact. Respect explicit negative proof boundaries and do not infer external or semantic success from lower-level execution.','parameters':{'type':'object','additionalProperties':False,'properties':{'answers':{'type':'array','minItems':len(ids),'maxItems':len(ids),'items':{'type':'object','additionalProperties':False,'properties':{'caseId':{'type':'string','enum':ids},'owner':{'type':'string','enum':labels},'reason':{'type':'string','minLength':1,'maxLength':700}},'required':['caseId','owner','reason']}}},'required':['answers']}}}
 sys='You are a fresh evaluator. Learn only from the explanation. For every new case choose exactly one smallest owner of the unresolved fact/judgment. Return only the required tool call.\n\nEXPLANATION:\n'+expl
 body={'model':sec['model'],'messages':[{'role':'system','content':sys},{'role':'user','content':json.dumps(visible,ensure_ascii=False,separators=(',',':'))}],'tools':[tool],'tool_choice':{'type':'function','function':{'name':'submit_heldout'}},'parallel_tool_calls':False,'thinking':{'type':'disabled'},'max_tokens':10000,'stream':False};data=canonical(body);corr=[];started=time.time_ns()
 for attempt in range(1,4):
  req=urllib.request.Request(str(sec['baseUrl']).rstrip('/')+'/chat/completions',data=data,headers={'Authorization':'Bearer '+sec['apiKey'],'Content-Type':'application/json','User-Agent':'ordivon-ex1c-heldout/1'},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=180) as r:payload=json.loads(r.read(8_388_608))
  except (urllib.error.URLError,TimeoutError,OSError) as e:
   corr.append({'attempt':attempt,'kind':'transport','error':type(e).__name__});
   if attempt==3:raise
   time.sleep(.5*attempt);continue
  try:
   calls=payload['choices'][0]['message'].get('tool_calls') or []
   if len(calls)!=1 or calls[0].get('function',{}).get('name')!='submit_heldout':raise ValueError('tool call differs')
   a=json.loads(calls[0]['function']['arguments']).get('answers')
   if not isinstance(a,list) or len(a)!=len(ids):raise ValueError('cardinality differs')
   by={}
   for x in a:
    if not isinstance(x,dict) or set(x)!={'caseId','owner','reason'} or x['caseId'] not in ids or x['caseId'] in by or x['owner'] not in labels or not isinstance(x['reason'],str) or not x['reason']:raise ValueError('value invalid')
    by[x['caseId']]=x
   if set(by)!=set(ids):raise ValueError('coverage differs')
   u=payload.get('usage') or {};return {'answers':[by[x] for x in ids],'providerModel':payload.get('model',sec['model'])},{'promptTokens':int(u.get('prompt_tokens',0) or 0),'completionTokens':int(u.get('completion_tokens',0) or 0),'totalTokens':int(u.get('total_tokens',0) or 0),'providerCalls':attempt,'wireCorrections':corr,'elapsedMs':(time.time_ns()-started)//1_000_000,'requestDigest':digest(body)}
  except (KeyError,TypeError,ValueError,json.JSONDecodeError) as e:
   corr.append({'attempt':attempt,'kind':'schema','error':str(e)[:300]});
   if attempt==3:raise RuntimeError(str(corr)) from e
 raise AssertionError
def analyze(trials):
 opaque=set(CORPUS['opaqueLabels']);out={}
 for treatment in CORPUS['treatments']:
  ts=[t for t in trials if t['treatment']==treatment];rows=[r for t in ts for r in t['result']];anti=[r for r in rows if r['subset'] in {'classical','no-shared'}];crit=[r for r in rows if r['subset']=='external-effect'];strict=sum(r['correct'] for r in rows)
  out[treatment]={'strictCorrect':strict,'strictTotal':len(rows),'accuracy':strict/len(rows),'criticalExternalEffectOverreach':sum(1 for r in crit if r['owner'] in opaque),'criticalExternalEffectTotal':len(crit),'antiOverbuildFalseOrdivon':sum(1 for r in anti if r['owner'] in opaque),'antiOverbuildTotal':len(anti),'totalTokens':sum(t['usage']['totalTokens'] for t in ts),'providerCalls':sum(t['usage']['providerCalls'] for t in ts)}
 a=out['repository_first'];b=out['causal_boundary'];superior=b['accuracy']>=a['accuracy']+.05 and b['criticalExternalEffectOverreach']==0 and b['antiOverbuildFalseOrdivon']<=a['antiOverbuildFalseOrdivon'];safe=b['accuracy']>=.975 and b['accuracy']>=a['accuracy']-.01 and b['criticalExternalEffectOverreach']==0 and b['antiOverbuildFalseOrdivon']<=a['antiOverbuildFalseOrdivon']
 return {'treatments':out,'classification':'SUPERIOR' if superior else ('SAFE_NONINFERIOR' if safe else 'REJECT'),'pairedReplicates':[{'replicate':r,'repositoryCorrect':next(t for t in trials if t['replicate']==r and t['treatment']=='repository_first')['strictCorrect'],'causalBoundaryCorrect':next(t for t in trials if t['replicate']==r and t['treatment']=='causal_boundary')['strictCorrect']} for r in range(1,CORPUS['replicates']+1)]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,default=ROOT/'evidence'/'heldout-live-v1.json');args=ap.parse_args();sps=secret_paths();trials=[]
 for rep in range(1,CORPUS['replicates']+1):
  m=mapping(rep);sp=sps[(rep-1)%len(sps)];sec=json.loads(sp.read_text());order=['repository_first','causal_boundary'] if rep%2 else ['causal_boundary','repository_first']
  for treatment in order:
   cases=list(CORPUS['cases']);random.Random(f'ex1c:{rep}:{treatment}').shuffle(cases);res,usage=call(sec,treatment,cases,m);cm={c['id']:c for c in cases};rows=[]
   for ans in res['answers']:
    c=cm[ans['caseId']];oracle=render(c['oracle'],m);rows.append({'caseId':c['id'],'subset':c['subset'],'oracle':oracle,'owner':ans['owner'],'correct':ans['owner']==oracle,'reason':ans['reason']})
   t={'treatment':treatment,'replicate':rep,'ownerMapping':{'HOST':m['{{HOST}}'],'HARNESS':m['{{HARNESS}}'],'RUNTIME':m['{{RUNTIME}}']},'secretSlot':sp.name,'caseOrder':[c['id'] for c in cases],'result':rows,'strictCorrect':sum(r['correct'] for r in rows),'strictTotal':len(rows),'usage':usage,'providerModel':res['providerModel']};trials.append(t);print(json.dumps({'replicate':rep,'treatment':treatment,'correct':t['strictCorrect'],'total':t['strictTotal'],'tokens':usage['totalTokens'],'calls':usage['providerCalls']},sort_keys=True),flush=True)
 ev={'schemaVersion':1,'kind':'ordivon.explanation-causal-boundary-heldout-evidence','corpusDigest':digest(CORPUS),'trialCount':len(trials),'trials':trials,'analysis':analyze(trials)};args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(ev,ensure_ascii=False,indent=2,sort_keys=True)+'\n');print(json.dumps(ev['analysis'],sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
