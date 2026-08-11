from __future__ import annotations
import json, os, pathlib, re, subprocess, sys, time, urllib.request, urllib.error
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/root/projects/ordivon-runtime')
QUESTION='''At current Runtime source dabb7b328c84288de2ec94e45a9299307f3491c7, what exactly does execution.hostDependencies guarantee across request identity, new admission, durable persistence, dispatch, target execution, and exact replay? What does it explicitly NOT guarantee? Decide whether it is correct to describe hostDependencies as immutable host dependencies or as a complete environment closure.'''
FIELDS={
 'scope': ['trusted_local_local_linux_only','other'],
 'pathContract': ['absolute_unique_regular_nonsymlink_sha256','other'],
 'inRequestIdentity': [True,False],
 'durablyPersisted': [True,False],
 'checkedAtNewAdmission': [True,False],
 'recheckedBeforeDispatch': [True,False],
 'runtimeDriftWitnessed': [True,False],
 'replayRevalidatesCurrentDependencyBytes': [True,False],
 'provesDependencyImmutability': [True,False],
 'coversUndeclaredDynamicDependencies': [True,False],
 'provesCompleteEnvironmentClosure': [True,False],
 'targetExecutableSeparatelyWitnessed': [True,False]
}
ORACLE={
 'scope':'trusted_local_local_linux_only','pathContract':'absolute_unique_regular_nonsymlink_sha256','inRequestIdentity':True,'durablyPersisted':True,'checkedAtNewAdmission':True,'recheckedBeforeDispatch':True,'runtimeDriftWitnessed':True,'replayRevalidatesCurrentDependencyBytes':False,'provesDependencyImmutability':False,'coversUndeclaredDynamicDependencies':False,'provesCompleteEnvironmentClosure':False,'targetExecutableSeparatelyWitnessed':True
}
MAX_OBS=28

def secret(rep):
 paths=sorted(pathlib.Path('/root/.config/ordivon/secrets').glob('deepseek*.json'))
 if not paths: raise RuntimeError('no provider secret')
 return json.loads(paths[(rep-1)%len(paths)].read_text())
def call(messages, tools, sec, max_tokens=7000):
 body={'model':sec['model'],'messages':messages,'tools':tools,'tool_choice':'required','parallel_tool_calls':False,'thinking':{'type':'disabled'},'max_tokens':max_tokens,'stream':False}
 data=json.dumps(body,separators=(',',':')).encode(); retries=0; total={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}
 while True:
  started=time.time_ns(); req=urllib.request.Request(str(sec['baseUrl']).rstrip('/')+'/chat/completions',data=data,headers={'Authorization':'Bearer '+str(sec['apiKey']),'Content-Type':'application/json','User-Agent':'ordivon-p9/1'},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=180) as resp: payload=json.loads(resp.read(4194304))
  except (urllib.error.URLError,TimeoutError,OSError):
   retries+=1
   if retries>2: raise
   time.sleep(.5*retries); continue
  total['elapsedMs']+=(time.time_ns()-started)//1_000_000; total['providerCalls']+=1; u=payload.get('usage') or {}; total['promptTokens']+=int(u.get('prompt_tokens',0) or 0); total['completionTokens']+=int(u.get('completion_tokens',0) or 0); total['totalTokens']+=int(u.get('total_tokens',0) or 0)
  msg=payload['choices'][0]['message']; calls=msg.get('tool_calls') or []
  if not calls:
   retries+=1
   if retries>2: raise RuntimeError('no tool call')
   continue
  return msg,calls,total

def tools():
 props={k:{'type':'string','enum':v} if all(isinstance(x,str) for x in v) else {'type':'boolean'} for k,v in FIELDS.items()}
 props['summary']={'type':'string'}
 props['unresolved']={'type':'array','items':{'type':'string'},'maxItems':8}
 return [
  {'type':'function','function':{'name':'search','description':'Literal/regex search over current tracked Runtime source. One call is one physical observation.','parameters':{'type':'object','properties':{'pattern':{'type':'string'},'pathPrefix':{'type':'string'}},'required':['pattern','pathPrefix'],'additionalProperties':False}}},
  {'type':'function','function':{'name':'read','description':'Read one bounded line range from one tracked Runtime file. One call is one physical observation.','parameters':{'type':'object','properties':{'path':{'type':'string'},'startLine':{'type':'integer','minimum':1},'endLine':{'type':'integer','minimum':1}},'required':['path','startLine','endLine'],'additionalProperties':False}}},
  {'type':'function','function':{'name':'submit','description':'Submit the final current hostDependencies model when evidence is sufficient.','parameters':{'type':'object','properties':props,'required':list(FIELDS)+['summary','unresolved'],'additionalProperties':False}}}
 ]
def search(pattern,prefix):
 if prefix.startswith('/') or '..' in pathlib.PurePosixPath(prefix).parts: return 'INVALID pathPrefix'
 try: re.compile(pattern)
 except re.error as e: return 'INVALID regex '+str(e)
 cmd=['/usr/bin/git','-C',str(REPO),'grep','-n','-I','-E',pattern,'HEAD','--']
 if prefix and prefix!='.': cmd.append(prefix)
 r=subprocess.run(cmd,capture_output=True,text=True); lines=(r.stdout or '').splitlines()[:60]
 return '\n'.join(lines) if lines else '(no matches)'
def read(path,start,end):
 if path.startswith('/') or '..' in pathlib.PurePosixPath(path).parts: return 'INVALID path'
 if end<start or end-start+1>220: return 'INVALID range: maximum 220 lines'
 p=REPO/path
 if not p.is_file(): return 'ABSENT file'
 lines=p.read_text(errors='replace').splitlines(); start=max(1,start); end=min(len(lines),end)
 return '\n'.join(f'{i}:{lines[i-1]}' for i in range(start,end+1))
def critic_tools():
 return [{'type':'function','function':{'name':'review','description':'Review whether the draft can close from the evidence already observed. ACCEPT only if no concrete decision-changing missing observation remains. Otherwise request exactly one search or read.','parameters':{'type':'object','properties':{'decision':{'type':'string','enum':['ACCEPT','REQUEST_SEARCH','REQUEST_READ']},'reason':{'type':'string'},'pattern':{'type':'string'},'pathPrefix':{'type':'string'},'path':{'type':'string'},'startLine':{'type':'integer'},'endLine':{'type':'integer'}},'required':['decision','reason','pattern','pathPrefix','path','startLine','endLine'],'additionalProperties':False}}}]
def score(d):
 correctness={k:d.get(k)==v for k,v in ORACLE.items()}; false=[k for k,v in correctness.items() if not v]
 return {'correctFields':sum(correctness.values()),'fieldCount':len(correctness),'strictAccepted':not false,'falseFields':false,'unresolvedCount':len(d.get('unresolved') or [])}
def main():
 treatment=sys.argv[1]; rep=int(os.environ.get('ORDIVON_REPLICATE','1')); sec=secret(rep)
 sysmsg='''You are a research Agent auditing current source. Use search/read selectively. Do not assume names imply semantics. You may submit whenever you believe the current world model is closed. Important: exact replay, admission, runtime drift, and negative scope claims can differ. Do not claim immutability or closure merely because digests are checked. Every search/read is costly. High budget is available but unnecessary observations are still evidence burden.'''
 msgs=[{'role':'system','content':sysmsg},{'role':'user','content':QUESTION}]
 observations=[]; usage={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; critic_calls=0; critic_requests=0; draft_attempts=0
 while len(observations)<MAX_OBS:
  msg,calls,u=call(msgs,tools(),sec); [usage.__setitem__(k,usage[k]+u[k]) for k in usage]
  # execute tool calls sequentially; submit must be sole meaningful close action
  submit_call=None
  for c in calls:
   fn=c.get('function') or {}; name=fn.get('name'); args=json.loads(fn.get('arguments') or '{}')
   if name=='submit': submit_call=args; break
   if name=='search': out=search(str(args.get('pattern','')),str(args.get('pathPrefix',''))); observations.append({'id':f'O{len(observations)+1}','tool':'search','args':args,'output':out})
   elif name=='read': out=read(str(args.get('path','')),int(args.get('startLine',1)),int(args.get('endLine',1))); observations.append({'id':f'O{len(observations)+1}','tool':'read','args':args,'output':out})
   else: out='INVALID tool'; observations.append({'id':f'O{len(observations)+1}','tool':'invalid','args':args,'output':out})
   msgs.append({'role':'assistant','content':None,'tool_calls':[c]}); msgs.append({'role':'tool','tool_call_id':c['id'],'content':out})
   if len(observations)>=MAX_OBS: break
  if submit_call is None: continue
  draft_attempts+=1
  if treatment=='open': final=submit_call; critic_history=[]; break
  # fresh critic sees only question, evidence and draft. It cannot search itself.
  evidence='\n\n'.join(f"{o['id']} {o['tool']} {json.dumps(o['args'],sort_keys=True)}\n{o['output']}" for o in observations)
  cmsgs=[{'role':'system','content':'''You are an independent stopping critic. You do not know a hidden answer key and must not rewrite the draft. Review only whether the draft is adequately closed by the observed evidence. ACCEPT if no concrete observation is likely to change any submitted field. If one decision-changing gap remains, request exactly one bounded search/read. Do not ask for generic more evidence, certainty, or exhaustive coverage.'''},{'role':'user','content':QUESTION+'\n\nOBSERVED EVIDENCE:\n'+evidence+'\n\nDRAFT:\n'+json.dumps(submit_call,sort_keys=True)}]
  cmsg,ccalls,cu=call(cmsgs,critic_tools(),sec,max_tokens=2500); critic_calls+=1; [usage.__setitem__(k,usage[k]+cu[k]) for k in usage]
  carg=json.loads((ccalls[0].get('function') or {}).get('arguments') or '{}'); decision=carg.get('decision')
  if decision=='ACCEPT' or critic_calls>=4:
   final=submit_call; critic_history=[{'decision':decision,'reason':carg.get('reason')}]; break
  if decision=='REQUEST_SEARCH': out=search(str(carg.get('pattern','')),str(carg.get('pathPrefix',''))); args={'pattern':carg.get('pattern',''),'pathPrefix':carg.get('pathPrefix','')}; toolname='search'
  else: out=read(str(carg.get('path','')),int(carg.get('startLine',1)),int(carg.get('endLine',1))); args={'path':carg.get('path',''),'startLine':carg.get('startLine',1),'endLine':carg.get('endLine',1)}; toolname='read'
  critic_requests+=1; observations.append({'id':f'O{len(observations)+1}','tool':toolname,'args':args,'output':out,'requestedByCritic':True})
  msgs.append({'role':'assistant','content':'I proposed a draft submission.'}); msgs.append({'role':'user','content':'Independent stopping critic rejected closure for this specific gap: '+str(carg.get('reason'))+'\nRequested observation result:\n'+out+'\nReassess. You remain the author of the final answer.'})
 else:
  final={k:(False if isinstance(ORACLE[k],bool) else 'other') for k in ORACLE}; final.update({'summary':'observation budget exhausted','unresolved':['budget exhausted']}); critic_history=[]
 result={'schemaVersion':1,'kind':'ordivon.computing.p9-stopping-trial','treatment':treatment,'replicate':rep,'question':QUESTION,'observations':observations,'observationCount':len(observations),'draftAttempts':draft_attempts,'criticCalls':critic_calls,'criticRequests':critic_requests,'final':final,'metrics':score(final),'usage':usage}
 print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__': main()
