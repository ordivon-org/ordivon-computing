from __future__ import annotations

import importlib.util, json, sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(path)
    mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod); return mod

sem=load('aic_sem_s4b',ROOT/'aic_semantic_falsify.py')
s2=load('aic_s2_s4b',ROOT/'aic_s2_cases.py')


def core(events:list[dict[str,Any]])->dict[str,Any]:
    f=deepcopy(s2.orthogonal_frontier(sem.replay(events))); f.pop('occurrenceDigest',None); f.pop('eventCount',None); return f

def variant(pair_id,side,relation,description,events):
    st=sem.replay(events)
    return {'scenarioId':f'{pair_id}-{side}','pairId':pair_id,'side':side,'relation':relation,'description':description,'events':events,'fullFrontierV1':sem.current_binding_frontier(st),'orthogonalFrontierV2':s2.orthogonal_frontier(st),'oracle':s2.expected(st)}

def pair(pair_id,relation,description,left,right):
    return {'pairId':pair_id,'relation':relation,'description':description,'left':variant(pair_id,'L',relation,description,left),'right':variant(pair_id,'R',relation,description,right)}

def build():
    pairs=[]
    base=[{'type':'valid_election','candidate':'B','votes':2},{'type':'transfer_control','actor':'B'}]
    pairs.append(pair('AIC-S4B-P1','MR1_INVALID_ELECTION_INSERTION','Invalid election noise must not alter current binding.',base,base+[{'type':'invalid_election','candidate':'C','votes':1}]))
    pairs.append(pair('AIC-S4B-P2','MR4_ROOT_COMPROMISE_ORDER','Order of independent root compromises must not alter current binding.',[{'type':'compromise_root','root':'R1'},{'type':'compromise_root','root':'R2'}],[{'type':'compromise_root','root':'R2'},{'type':'compromise_root','root':'R1'}]))
    base=[{'type':'valid_election','candidate':'B','votes':2},{'type':'transfer_control','actor':'B'}]
    transient=[{'type':'authority_claim','claimant':'A','source':'s4b-a','standing':'CURRENT_SUPPORT'},{'type':'authority_claim','claimant':'C','source':'s4b-c','standing':'CURRENT_SUPPORT'},{'type':'clear_claims'}]
    pairs.append(pair('AIC-S4B-P3','MR6_TRANSIENT_CONTEST_CLEAR','A resolved transient contest must not contaminate later current binding.',base,base+transient))
    left=[{'type':'compromise_root','root':'R1'},{'type':'compromise_root','root':'R2'},{'type':'in_band_root_rotation','newAnchor':'FAILED-S4B'},{'type':'external_refoundation','anchor':'S4B-EXT','lineage':'I1','monitor':'C'},{'type':'transfer_control','actor':'C'}]
    right=[{'type':'compromise_root','root':'R1'},{'type':'compromise_root','root':'R2'},{'type':'external_refoundation','anchor':'S4B-EXT','lineage':'I1','monitor':'C'},{'type':'transfer_control','actor':'C'}]
    pairs.append(pair('AIC-S4B-P4','MR7_FAILED_INBAND_BEFORE_REFOUNDATION','Failed in-band resurrection before independent refoundation must not alter final current binding.',left,right))
    prefix=[{'type':'steal_control_key','actor':'B'},{'type':'sanction','actor':'B','target':'C','amount':2,'sanctionId':'S4B-S1'},{'type':'recover_control','actor':'A'}]
    pairs.append(pair('AIC-S4B-P5','MR8_RESTITUTION_PARTITION','Equivalent restitution partition must preserve final current binding and history standing.',prefix+[{'type':'restitute','target':'C','amount':2}],prefix+[{'type':'restitute','target':'C','amount':1},{'type':'restitute','target':'C','amount':1}]))
    once=[{'type':'sanction','actor':'A','target':'C','amount':2,'sanctionId':'S4B-S2'},{'type':'invalidate_sanction','sanctionId':'S4B-S2'}]
    pairs.append(pair('AIC-S4B-P6','MR9_REPEAT_INVALIDATION_IDEMPOTENT','Repeated invalidation must not rewrite current/historical standing.',once,once+[{'type':'invalidate_sanction','sanctionId':'S4B-S2'}]))
    pairs.append(pair('AIC-S4B-P7','MR11_ELECTION_TRANSFER_COMMUTE','Lawful election and matching control transfer commute when no consequential event intervenes.',[{'type':'valid_election','candidate':'B','votes':2},{'type':'transfer_control','actor':'B'}],[{'type':'transfer_control','actor':'B'},{'type':'valid_election','candidate':'B','votes':2}]))
    base=[{'type':'valid_amendment','votes':3,'quota':2,'revision':'S4B-C1'}]
    pairs.append(pair('AIC-S4B-P8','MR12_NOOP_PHYSICAL_TAMPER','No-op physical tamper adds invalid history but must not alter orthogonal current binding.',base,base+[{'type':'tamper_physical_quota','quota':2,'physicalRevision':'S4B-NOOP'}]))
    return pairs

def main():
    pairs=build(); gates=[]; variants=[]
    response_catalog=set(s2.RESPONSE_CATALOG)
    for p in pairs:
        l,r=p['left'],p['right']; variants += [l,r]
        same_oracle=l['oracle']==r['oracle']; same_core=core(l['events'])==core(r['events']); different_history=sem.canonical(l['events'])!=sem.canonical(r['events'])
        no_leak=all('requiredResponses' not in sem.canonical(v['orthogonalFrontierV2']) and not any(x in sem.canonical(v['orthogonalFrontierV2']) for x in response_catalog) for v in [l,r])
        gates.append({'pairId':p['pairId'],'relation':p['relation'],'sameOracle':same_oracle,'sameOrthogonalCore':same_core,'differentHistory':different_history,'noActionLeak':no_leak,'ok':same_oracle and same_core and different_history and no_leak})
    result={'schemaVersion':1,'kind':'ordivon.computing.aic-s4b-pairs','experimentId':'COJC-J3-AIC-METAMORPHIC-S4B','pairs':pairs,'variants':variants}
    evidence={'schemaVersion':1,'kind':'ordivon.computing.aic-s4b-deterministic-preflight','experimentId':result['experimentId'],'pairCount':len(pairs),'variantCount':len(variants),'gates':gates,'mandatoryPass':all(g['ok'] for g in gates),'casesDigest':sem.digest(result)}
    (ROOT/'cases-s4b-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); (ROOT/'evidence-s4b-deterministic.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(evidence,ensure_ascii=False,sort_keys=True)); raise SystemExit(0 if evidence['mandatoryPass'] else 2)
if __name__=='__main__': main()
