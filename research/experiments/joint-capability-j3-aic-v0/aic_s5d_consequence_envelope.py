from __future__ import annotations
import argparse,importlib.util,json,random,sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load(n,p):
 s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); sys.modules[n]=m; s.loader.exec_module(m); return m
sem=load('sem5d',ROOT/'aic_semantic_falsify.py'); s2=load('s25d',ROOT/'aic_s2_cases.py'); s5a=load('s5a5d',ROOT/'aic_s5a_future_sufficiency.py'); s5b=load('s5b5d',ROOT/'aic_s5b_partial_order.py')

def binding_key(ex): return sem.canonical(ex['frontierCore'])
def binding_set(a):
 seen={};
 for ex in a['executions']: seen[binding_key(ex)]=ex
 return list(seen.values())
def envelope_from_execs(execs):
 return {
  'possibleConsequentialAuthorityStatuses':sorted({x['oracle']['consequentialAuthorityStatus'] for x in execs}),
  'possibleOfficeHolders':sorted({x['oracle']['officeHolder'] for x in execs}),
  'possibleEffectiveControllers':sorted({x['oracle']['effectiveController'] for x in execs}),
 }
def safe(env):
 return env['possibleConsequentialAuthorityStatuses']==['AUTHORIZED'] and len(env['possibleOfficeHolders'])==1 and len(env['possibleEffectiveControllers'])==1 and env['possibleOfficeHolders'][0]==env['possibleEffectiveControllers'][0]
def multiplicity(a): return 'MULTIPLE' if a['uniqueBindingCores']>1 else 'ONE'

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--batches',type=int,default=100000); ap.add_argument('--seed',type=int,default=202608263); args=ap.parse_args(); rng=random.Random(args.seed)
 unique_sets={}; unique_envs={}; action_counts={'ALLOW':0,'HOLD':0}; mult_action=defaultdict(int); examples={}
 envelope_violation=None; monotonic_violation=None
 targeted=s5b.targeted()
 for x in targeted:
  env=envelope_from_execs(binding_set(x)); key=f"{multiplicity(x)}|{'ALLOW' if safe(env) else 'HOLD'}"; examples.setdefault(key,{'case':x['case'],'envelope':env,'bindings':x['uniqueBindingCores']})
 for _ in range(args.batches):
  base=[s5a.random_event(rng) for _ in range(rng.randint(0,5))]; batch=[s5a.random_event(rng) for _ in range(rng.choice([2,2,2,3]))]; a=s5b.analyze_partial(base,batch); execs=binding_set(a); env=envelope_from_execs(execs); sk=sem.canonical([x['frontierCore'] for x in sorted(execs,key=binding_key)]); ek=sem.canonical(env); unique_sets[sk]=1; unique_envs[ek]=1; act='ALLOW' if safe(env) else 'HOLD'; action_counts[act]+=1; mult_action[f"{multiplicity(a)}|{act}"]+=1
  # Verify envelope rule matches S5B independent checker.
  expected=a['safeFreshConsequentialAction']=='ALLOW'
  if safe(env)!=expected and envelope_violation is None: envelope_violation={'base':base,'batch':batch,'analysis':a,'envelope':env}
  # Information refinement law: if full set is safe, all sampled nonempty singleton/subsets must remain safe.
  if safe(env) and len(execs)>1:
   for ex in execs:
    if not safe(envelope_from_execs([ex])):
     monotonic_violation={'base':base,'batch':batch,'envelope':env,'badSingleton':ex}; break
  if monotonic_violation: break
 out={'schemaVersion':1,'kind':'ordivon.computing.aic-s5d-consequence-envelope-result','experimentId':'COJC-J3-AIC-CONSEQUENCE-ENVELOPE-S5D','batchesChecked':args.batches,'uniqueBindingSets':len(unique_sets),'uniqueConsequenceEnvelopes':len(unique_envs),'actionCounts':action_counts,'multiplicityActionCounts':dict(mult_action),'envelopeSafetyViolation':envelope_violation,'refinementMonotonicityViolation':monotonic_violation,'targetedExamples':examples,'candidateLawsPass':envelope_violation is None and monotonic_violation is None and 'MULTIPLE|ALLOW' in examples and 'ONE|HOLD' in examples}; Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
