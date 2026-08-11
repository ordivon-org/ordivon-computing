from __future__ import annotations
import importlib.util,json,os,pathlib
BASE_PATH=pathlib.Path('/tmp/ordivon-rsi-lab-p4-p9/p9/trial.py')
spec=importlib.util.spec_from_file_location('p9base',BASE_PATH); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
CHECKPOINT=8; MAX_OBS=28
BOOL_FIELDS=[k for k,v in b.FIELDS.items() if all(isinstance(x,bool) for x in v)]
STR_FIELDS=[k for k,v in b.FIELDS.items() if all(isinstance(x,str) for x in v)]
def merge_usage(total,u):
 for k in total: total[k]+=u[k]
def synth_tools():
 props={k:({'type':'string','enum':v} if k in STR_FIELDS else {'type':'boolean'}) for k,v in b.FIELDS.items()}; props['summary']={'type':'string'}; props['unresolved']={'type':'array','items':{'type':'string'},'maxItems':8}
 return [{'type':'function','function':{'name':'candidate','description':'Produce a provisional current world model from observed evidence only. Boolean fields MUST be JSON booleans, never strings.','parameters':{'type':'object','properties':props,'required':list(b.FIELDS)+['summary','unresolved'],'additionalProperties':False}}}]
def valid_candidate(x):
 if not isinstance(x,dict): return False,'candidate must be object'
 for k in BOOL_FIELDS:
  if type(x.get(k)) is not bool: return False,f'{k} must be JSON boolean, got {type(x.get(k)).__name__}'
 for k in STR_FIELDS:
  if x.get(k) not in b.FIELDS[k]: return False,f'{k} invalid enum'
 if not isinstance(x.get('summary'),str): return False,'summary must be string'
 if not isinstance(x.get('unresolved'),list) or any(not isinstance(y,str) for y in x['unresolved']): return False,'unresolved must be string array'
 return True,''
def evidence_text(obs): return '\n\n'.join(f"{o['id']} {o['tool']} {json.dumps(o['args'],sort_keys=True)}\n{o['output']}" for o in obs)
def synth(obs,sec):
 msgs=[{'role':'system','content':'Form a provisional answer from only supplied observations. Do not infer closure or immutability from digest checks. Tool boolean fields must be literal JSON true/false, never strings.'},{'role':'user','content':b.QUESTION+'\n\nOBSERVED EVIDENCE:\n'+evidence_text(obs)}]
 total={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; diagnostics=[]
 for attempt in range(1,4):
  msg,calls,u=b.call(msgs,synth_tools(),sec,max_tokens=5000); merge_usage(total,u)
  try: args=json.loads(calls[0]['function']['arguments'])
  except Exception as e: args={}; diagnostics.append(f'attempt{attempt}: invalid JSON {e}')
  ok,why=valid_candidate(args)
  if ok: return args,total,diagnostics
  diagnostics.append(f'attempt{attempt}: {why}')
  msgs.append({'role':'user','content':'PROTOCOL ERROR ONLY; do not change the scientific interpretation merely to satisfy me. Re-emit candidate with the same evidence, but obey JSON Schema types exactly. '+why})
 raise RuntimeError('candidate protocol failed after bounded retries: '+repr(diagnostics))
def valid_critic(x):
 if not isinstance(x,dict): return False,'critic output must object'
 if x.get('decision') not in {'ACCEPT','REQUEST_SEARCH','REQUEST_READ'}: return False,'invalid decision'
 if not isinstance(x.get('reason'),str): return False,'reason must string'
 for k in ['pattern','pathPrefix','path']:
  if not isinstance(x.get(k),str): return False,f'{k} must string'
 for k in ['startLine','endLine']:
  if type(x.get(k)) is not int: return False,f'{k} must integer'
 return True,''
def review(obs,cand,sec):
 tools=b.critic_tools(); msgs=[{'role':'system','content':'You are an independent closure critic. You cannot search. ACCEPT only if no concrete missing observation is likely to change any structured field in the candidate. Otherwise request exactly one bounded search/read targeting one disputed field. Do not request generic completeness. Obey Tool JSON types exactly.'},{'role':'user','content':b.QUESTION+'\n\nOBSERVED EVIDENCE:\n'+evidence_text(obs)+'\n\nCANDIDATE:\n'+json.dumps(cand,sort_keys=True)}]
 total={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; diagnostics=[]
 for attempt in range(1,4):
  msg,calls,u=b.call(msgs,tools,sec,max_tokens=2500); merge_usage(total,u)
  try: args=json.loads(calls[0]['function']['arguments'])
  except Exception as e: args={}; diagnostics.append(f'attempt{attempt}: invalid JSON {e}')
  ok,why=valid_critic(args)
  if ok: return args,total,diagnostics
  diagnostics.append(f'attempt{attempt}: {why}'); msgs.append({'role':'user','content':'PROTOCOL ERROR ONLY. Re-emit the same review decision but obey Tool JSON types exactly. '+why})
 raise RuntimeError('critic protocol failed after bounded retries: '+repr(diagnostics))
def main():
 rep=int(os.environ.get('ORDIVON_REPLICATE','1')); sec=b.secret(rep)
 msgs=[{'role':'system','content':'You are the primary evidence-acquisition Agent. Search/read selectively for current hostDependencies. You do NOT decide stopping; external closure checkpoints occur after bounded observation batches. Seek causal and negative-boundary evidence, not keyword coverage. Every observation is costly.'},{'role':'user','content':b.QUESTION}]
 obs=[]; usage={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; checkpoints=[]; protocol=[]; final=None; next_checkpoint=CHECKPOINT
 while len(obs)<MAX_OBS and final is None:
  msg,calls,u=b.call(msgs,[t for t in b.tools() if t['function']['name'] in {'search','read'}],sec); merge_usage(usage,u)
  for c in calls:
   fn=c.get('function') or {}; name=fn.get('name'); args=json.loads(fn.get('arguments') or '{}')
   if name=='search': out=b.search(str(args.get('pattern','')),str(args.get('pathPrefix','')))
   elif name=='read': out=b.read(str(args.get('path','')),int(args.get('startLine',1)),int(args.get('endLine',1)))
   else: continue
   obs.append({'id':f'O{len(obs)+1}','tool':name,'args':args,'output':out}); msgs.append({'role':'assistant','content':None,'tool_calls':[c]}); msgs.append({'role':'tool','tool_call_id':c['id'],'content':out})
   if len(obs)>=MAX_OBS: break
  if len(obs)<next_checkpoint and len(obs)<MAX_OBS: continue
  cand,su,sdiag=synth(obs,sec); merge_usage(usage,su); crit,cu,cdiag=review(obs,cand,sec); merge_usage(usage,cu); protocol.extend(sdiag+cdiag); checkpoints.append({'atObservation':len(obs),'candidate':cand,'critic':crit})
  if crit['decision']=='ACCEPT': final=cand; break
  if len(obs)<MAX_OBS:
   if crit['decision']=='REQUEST_SEARCH': args={'pattern':crit['pattern'],'pathPrefix':crit['pathPrefix']}; out=b.search(args['pattern'],args['pathPrefix']); name='search'
   else: args={'path':crit['path'],'startLine':crit['startLine'],'endLine':crit['endLine']}; out=b.read(args['path'],args['startLine'],args['endLine']); name='read'
   obs.append({'id':f'O{len(obs)+1}','tool':name,'args':args,'output':out,'requestedByCritic':True}); msgs.append({'role':'user','content':'External closure critic found one specific gap: '+crit['reason']+'\nRequested observation:\n'+out+'\nContinue only if needed.'})
  next_checkpoint=((len(obs)//CHECKPOINT)+1)*CHECKPOINT
 if final is None:
  final,su,sdiag=synth(obs,sec); merge_usage(usage,su); protocol.extend(sdiag)
 print(json.dumps({'schemaVersion':1,'kind':'ordivon.computing.p9-v3-checkpointed-stopping-trial','treatment':'checkpointed_critic_strict','replicate':rep,'observationCount':len(obs),'observations':obs,'checkpoints':checkpoints,'protocolDiagnostics':protocol,'final':final,'metrics':b.score(final),'usage':usage},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
