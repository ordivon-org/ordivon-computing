from __future__ import annotations
import importlib.util,json,os,pathlib,sys
V3_PATH=pathlib.Path('/tmp/ordivon-rsi-lab-p4-p9/p9v3/trial.py')
spec=importlib.util.spec_from_file_location('p9v3',V3_PATH); v3=importlib.util.module_from_spec(spec); spec.loader.exec_module(v3); b=v3.b

def merge(total,u):
 for k in total: total[k]+=u[k]
def main():
 target=int(sys.argv[1]); rep=int(os.environ.get('ORDIVON_REPLICATE','1')); sec=b.secret(rep)
 msgs=[{'role':'system','content':'You are the primary evidence-acquisition Agent. Search/read selectively for current hostDependencies. A fresh synthesis will occur after a fixed observation checkpoint. Seek exact causal and negative-boundary evidence; every observation is costly.'},{'role':'user','content':b.QUESTION}]
 obs=[]; usage={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; protocol=[]
 while len(obs)<target:
  msg,calls,u=b.call(msgs,[t for t in b.tools() if t['function']['name'] in {'search','read'}],sec); merge(usage,u)
  for c in calls:
   fn=c.get('function') or {}; name=fn.get('name'); args=json.loads(fn.get('arguments') or '{}')
   if name=='search': out=b.search(str(args.get('pattern','')),str(args.get('pathPrefix','')))
   elif name=='read': out=b.read(str(args.get('path','')),int(args.get('startLine',1)),int(args.get('endLine',1)))
   else: continue
   obs.append({'id':f'O{len(obs)+1}','tool':name,'args':args,'output':out}); msgs.append({'role':'assistant','content':None,'tool_calls':[c]}); msgs.append({'role':'tool','tool_call_id':c['id'],'content':out})
   if len(obs)>=target: break
 final,su,sdiag=v3.synth(obs,sec); merge(usage,su); protocol.extend(sdiag)
 print(json.dumps({'schemaVersion':1,'kind':'ordivon.computing.p9-v4-synthesis-checkpoint-trial','checkpoint':target,'replicate':rep,'observationCount':len(obs),'observations':obs,'final':final,'protocolDiagnostics':protocol,'metrics':b.score(final),'usage':usage},sort_keys=True,separators=(',',':')))
if __name__=='__main__': main()
