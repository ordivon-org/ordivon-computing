from __future__ import annotations
import importlib.util,json,os,pathlib,sys
BASE_PATH=pathlib.Path('/tmp/ordivon-rsi-lab-p4-p9/p9/trial.py')
spec=importlib.util.spec_from_file_location('p9base',BASE_PATH); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
CHECKPOINT=8; MAX_OBS=28

def synth_tools():
 props={k:({'type':'string','enum':v} if all(isinstance(x,str) for x in v) else {'type':'boolean'}) for k,v in b.FIELDS.items()}; props['summary']={'type':'string'}; props['unresolved']={'type':'array','items':{'type':'string'},'maxItems':8}
 return [{'type':'function','function':{'name':'candidate','description':'Produce a provisional current world model from observed evidence only.','parameters':{'type':'object','properties':props,'required':list(b.FIELDS)+['summary','unresolved'],'additionalProperties':False}}}]
def critic_tools(): return b.critic_tools()
def evidence_text(obs): return '\n\n'.join(f"{o['id']} {o['tool']} {json.dumps(o['args'],sort_keys=True)}\n{o['output']}" for o in obs)
def synth(obs,sec):
 msgs=[{'role':'system','content':'Form a provisional answer from only the supplied observations. Do not infer a complete environment closure or immutability merely from digest checks. Use candidate exactly once.'},{'role':'user','content':b.QUESTION+'\n\nOBSERVED EVIDENCE:\n'+evidence_text(obs)}]
 msg,calls,u=b.call(msgs,synth_tools(),sec,max_tokens=5000); args=json.loads(calls[0]['function']['arguments']); return args,u
def review(obs,cand,sec):
 msgs=[{'role':'system','content':'You are an independent closure critic. You cannot search. ACCEPT only if no concrete missing observation is likely to change any structured field in the candidate. Otherwise request exactly one bounded search/read that targets one specific disputed field. Do not request generic completeness, more confidence, or exhaustive coverage.'},{'role':'user','content':b.QUESTION+'\n\nOBSERVED EVIDENCE:\n'+evidence_text(obs)+'\n\nCANDIDATE:\n'+json.dumps(cand,sort_keys=True)}]
 msg,calls,u=b.call(msgs,critic_tools(),sec,max_tokens=2500); args=json.loads(calls[0]['function']['arguments']); return args,u
def main():
 rep=int(os.environ.get('ORDIVON_REPLICATE','1')); sec=b.secret(rep)
 sysmsg='''You are the primary evidence-acquisition Agent. Search/read selectively for the current hostDependencies question. You do NOT decide when the run stops; an external closure checkpoint will occur after bounded observation batches. Seek exact causal and negative-boundary evidence rather than keyword coverage. Every observation is costly.'''
 msgs=[{'role':'system','content':sysmsg},{'role':'user','content':b.QUESTION}]; obs=[]; usage={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; checkpoints=[]; final=None; next_checkpoint=CHECKPOINT
 while len(obs)<MAX_OBS and final is None:
  msg,calls,u=b.call(msgs,[t for t in b.tools() if t['function']['name'] in {'search','read'}],sec); [usage.__setitem__(k,usage[k]+u[k]) for k in usage]
  for c in calls:
   fn=c.get('function') or {}; name=fn.get('name'); args=json.loads(fn.get('arguments') or '{}')
   if name=='search': out=b.search(str(args.get('pattern','')),str(args.get('pathPrefix','')))
   elif name=='read': out=b.read(str(args.get('path','')),int(args.get('startLine',1)),int(args.get('endLine',1)))
   else: continue
   obs.append({'id':f'O{len(obs)+1}','tool':name,'args':args,'output':out}); msgs.append({'role':'assistant','content':None,'tool_calls':[c]}); msgs.append({'role':'tool','tool_call_id':c['id'],'content':out})
   if len(obs)>=MAX_OBS: break
  if len(obs)<next_checkpoint and len(obs)<MAX_OBS: continue
  cand,su=synth(obs,sec); [usage.__setitem__(k,usage[k]+su[k]) for k in usage]
  crit,cu=review(obs,cand,sec); [usage.__setitem__(k,usage[k]+cu[k]) for k in usage]
  checkpoint={'atObservation':len(obs),'candidate':cand,'critic':crit}; checkpoints.append(checkpoint)
  if crit.get('decision')=='ACCEPT': final=cand; break
  # execute exactly one critic-requested discriminator, then resume primary.
  if len(obs)<MAX_OBS:
   if crit.get('decision')=='REQUEST_SEARCH': args={'pattern':crit.get('pattern',''),'pathPrefix':crit.get('pathPrefix','')}; out=b.search(str(args['pattern']),str(args['pathPrefix'])); name='search'
   else: args={'path':crit.get('path',''),'startLine':crit.get('startLine',1),'endLine':crit.get('endLine',1)}; out=b.read(str(args['path']),int(args['startLine']),int(args['endLine'])); name='read'
   obs.append({'id':f'O{len(obs)+1}','tool':name,'args':args,'output':out,'requestedByCritic':True})
   msgs.append({'role':'user','content':'External closure critic found one decision-changing evidence gap: '+str(crit.get('reason'))+'\nThe requested observation was executed:\n'+out+'\nContinue evidence acquisition only if needed.'})
  next_checkpoint=((len(obs)//CHECKPOINT)+1)*CHECKPOINT
 if final is None:
  final,su=synth(obs,sec); [usage.__setitem__(k,usage[k]+su[k]) for k in usage]
 result={'schemaVersion':1,'kind':'ordivon.computing.p9-checkpointed-stopping-trial','treatment':'checkpointed_critic','replicate':rep,'observationCount':len(obs),'observations':obs,'checkpoints':checkpoints,'final':final,'metrics':b.score(final),'usage':usage}
 print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__': main()
