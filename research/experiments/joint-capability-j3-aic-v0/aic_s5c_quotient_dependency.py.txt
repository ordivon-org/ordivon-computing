from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(path)
    mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod); return mod

sem=load('aic_sem_s5c',ROOT/'aic_semantic_falsify.py')
s2=load('aic_s2_s5c',ROOT/'aic_s2_cases.py')
s5a=load('aic_s5a_s5c',ROOT/'aic_s5a_future_sufficiency.py')


def canon(x): return sem.canonical(x)

def action_signature(st):
    o=s2.expected(st)
    return {
      'consequentialAuthorityStatus':o['consequentialAuthorityStatus'],
      'officeHolder':o['officeHolder'],
      'effectiveController':o['effectiveController'],
      'requiredResponses':o['requiredResponses'],
    }

def frontier(st): return s5a.frontier_core(st)
def kernel(st): return s5a.continuation_kernel(st)

def random_history(rng,max_len=8): return [s5a.random_event(rng) for _ in range(rng.randint(0,max_len))]


def quotient_analysis(seed,n):
    rng=random.Random(seed)
    h_seen=set(); kmap=defaultdict(list); fmap=defaultdict(list); amap=defaultdict(list)
    states=[]
    for i in range(n):
        h=random_history(rng); hk=canon(h)
        if hk in h_seen: continue
        h_seen.add(hk); st=sem.replay(h); states.append((h,st))
        kmap[canon(kernel(st))].append(h); fmap[canon(frontier(st))].append(h); amap[canon(action_signature(st))].append(h)
    violations={'kernelToFrontier':None,'frontierToAction':None}
    # Functional refinement checks over observed collision classes.
    for bucket in kmap.values():
        vals={canon(frontier(sem.replay(h))) for h in bucket}
        if len(vals)>1: violations['kernelToFrontier']={'histories':bucket[:5],'frontiers':list(vals)[:5]}; break
    for bucket in fmap.values():
        vals={canon(action_signature(sem.replay(h))) for h in bucket}
        if len(vals)>1: violations['frontierToAction']={'histories':bucket[:5],'actions':list(vals)[:5]}; break
    def example_same(mapping,distinct_projection=None):
        for bucket in mapping.values():
            if len(bucket)<2: continue
            for a,b in itertools.combinations(bucket[:20],2):
                if canon(a)==canon(b): continue
                if distinct_projection is None or distinct_projection(sem.replay(a),sem.replay(b)):
                    return {'left':a,'right':b}
        return None
    ex_same_kernel=example_same(kmap)
    ex_same_frontier_diff_kernel=example_same(fmap,lambda a,b: canon(kernel(a))!=canon(kernel(b)))
    ex_same_action_diff_frontier=example_same(amap,lambda a,b: canon(frontier(a))!=canon(frontier(b)))
    return {
      'uniqueHistories':len(states),
      'uniqueContinuationKernels':len(kmap),
      'uniqueFrontierCores':len(fmap),
      'uniqueImmediateActionSignatures':len(amap),
      'compressionRatios':{
        'historyPerKernel':round(len(states)/max(1,len(kmap)),3),
        'kernelPerFrontier':round(len(kmap)/max(1,len(fmap)),3),
        'frontierPerActionSignature':round(len(fmap)/max(1,len(amap)),3),
      },
      'collisionClasses':{
        'kernel':sum(len(v)>=2 for v in kmap.values()),
        'frontier':sum(len(v)>=2 for v in fmap.values()),
        'action':sum(len(v)>=2 for v in amap.values()),
      },
      'refinementViolations':violations,
      'examples':{
        'distinctHistoriesSameKernel':ex_same_kernel,
        'sameFrontierDifferentKernel':ex_same_frontier_diff_kernel,
        'sameActionDifferentFrontier':ex_same_action_diff_frontier,
      },
    }, states

# Named templates deliberately keep finite domains so pair labels aggregate.
def event_template(rng):
    choices=[
      ('election_B',{'type':'valid_election','candidate':'B','votes':2}),
      ('election_C',{'type':'valid_election','candidate':'C','votes':2}),
      ('transfer_B',{'type':'transfer_control','actor':'B'}),
      ('theft_C',{'type':'steal_control_key','actor':'C'}),
      ('disable_control',{'type':'disable_control'}),
      ('amend_q2',{'type':'valid_amendment','votes':3,'quota':2,'revision':'DX'}),
      ('tamper_q2',{'type':'tamper_physical_quota','quota':2,'physicalRevision':'TX'}),
      ('compromise_R1',{'type':'compromise_root','root':'R1'}),
      ('compromise_R2',{'type':'compromise_root','root':'R2'}),
      ('rotate',{'type':'in_band_root_rotation','newAnchor':'ROT-DYN'}),
      ('claim_A',{'type':'authority_claim','claimant':'A','source':'dyn-a','standing':'CURRENT_SUPPORT'}),
      ('claim_B',{'type':'authority_claim','claimant':'B','source':'dyn-b','standing':'CURRENT_SUPPORT'}),
      ('clear_claims',{'type':'clear_claims'}),
      ('sanction_A',{'type':'sanction','actor':'A','target':'C','amount':1,'sanctionId':'DS'}),
      ('invalidate_DS',{'type':'invalidate_sanction','sanctionId':'DS'}),
      ('restitute_C',{'type':'restitute','target':'C','amount':1}),
    ]
    return rng.choice(choices)

def commute(base,a,b):
    s1=sem.replay(base+[a,b]); s2s=sem.replay(base+[b,a])
    return canon(kernel(s1))==canon(kernel(s2s)) and canon(frontier(s1))==canon(frontier(s2s))

def dynamic_independence(seed,contexts,pairs_per_context):
    rng=random.Random(seed+91); pair_stats=defaultdict(lambda:{'commute':0,'noncommute':0,'exampleCommute':None,'exampleNoncommute':None})
    for _ in range(contexts):
        base=random_history(rng,6)
        for _ in range(pairs_per_context):
            n1,e1=event_template(rng); n2,e2=event_template(rng)
            if n1==n2: continue
            key=' | '.join(sorted([n1,n2])); ok=commute(base,e1,e2); d=pair_stats[key]
            if ok:
                d['commute']+=1
                if d['exampleCommute'] is None: d['exampleCommute']={'base':base,'events':[e1,e2]}
            else:
                d['noncommute']+=1
                if d['exampleNoncommute'] is None: d['exampleNoncommute']={'base':base,'events':[e1,e2]}
    summary={'observed-always-commutative':0,'context-dependent':0,'observed-never-commutative':0}
    rows=[]
    for key,d in sorted(pair_stats.items()):
        if d['commute'] and d['noncommute']: cls='context-dependent'
        elif d['commute']: cls='observed-always-commutative'
        else: cls='observed-never-commutative'
        summary[cls]+=1; rows.append({'pair':key,'classification':cls,**d,'commutePct':round(100*d['commute']/max(1,d['commute']+d['noncommute']),2)})
    context_dep=sorted([r for r in rows if r['classification']=='context-dependent'],key=lambda x:abs(x['commutePct']-50))[:20]
    never=[r for r in rows if r['classification']=='observed-never-commutative'][:20]
    always=[r for r in rows if r['classification']=='observed-always-commutative'][:20]
    return {'contexts':contexts,'pairSamplesPerContext':pairs_per_context,'classificationCounts':summary,'pairTypeCount':len(rows),'contextDependentExamples':context_dep,'observedNeverExamples':never,'observedAlwaysExamples':always}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--seed',type=int,default=202608262); ap.add_argument('--histories',type=int,default=150000); ap.add_argument('--contexts',type=int,default=50000); ap.add_argument('--pairs-per-context',type=int,default=6); args=ap.parse_args()
    q,_=quotient_analysis(args.seed,args.histories); dep=dynamic_independence(args.seed,args.contexts,args.pairs_per_context)
    out={'schemaVersion':1,'kind':'ordivon.computing.aic-s5c-quotient-dependency-result','experimentId':'COJC-J3-AIC-QUOTIENT-DEPENDENCY-S5C','quotient':q,'dynamicIndependence':dep}; Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
