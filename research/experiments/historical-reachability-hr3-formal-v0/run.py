from __future__ import annotations
import json, random
from dataclasses import dataclass
from pathlib import Path

ROOT=Path(__file__).resolve().parent

@dataclass(frozen=True)
class Action:
    name:str
    requires:frozenset[str]
    adds:frozenset[str]
    removes:frozenset[str]=frozenset()
    admissible:bool=True

def closure(initial:set[str], actions:list[Action], admissible_only=True):
    s=set(initial); fired=[]
    changed=True
    while changed:
        changed=False
        for a in actions:
            if admissible_only and not a.admissible: continue
            if a.name in fired: continue
            if a.requires <= s:
                s-=set(a.removes); s|=set(a.adds); fired.append(a.name); changed=True
    return s,fired

def case_results():
    cases=[]
    # C1: current-basis nonreachability does not imply nonreachability after basis change.
    initial={'specification'}
    actions=[Action('access_fabrication',frozenset({'specification'}),frozenset({'artifact'})),Action('access_metrology',frozenset({'artifact'}),frozenset({'verified_artifact'}))]
    static='verified_artifact' in initial; final,path=closure(initial,actions)
    cases.append({'id':'C1_DYNAMIC_BASIS','staticReachable':static,'afterBasisChangeReachable':'verified_artifact' in final,'path':path,'supports':'PossibilityUnderCurrentBasis != CandidateReachabilityUnderBasisChange'})
    # C2: hard contradiction remains hard; basis-change prior is not universal optimism.
    cases.append({'id':'C2_HARD_CONTRADICTION','target':'P AND NOT_P','staticReachable':False,'afterBasisChangeReachable':False,'supports':'CandidateReachabilityPressure != GuaranteedReachability'})
    # C3: provider existence without authority is not current capability.
    initial={'supplier_exists','specification','funds'}
    actions=[Action('order_without_authority',frozenset({'supplier_exists','specification','funds'}),frozenset({'artifact'}),admissible=False),Action('obtain_authority',frozenset({'funds'}),frozenset({'authority'})),Action('authorized_order',frozenset({'supplier_exists','specification','funds','authority'}),frozenset({'artifact'})),Action('verify',frozenset({'artifact'}),frozenset({'verified_artifact'}))]
    pre,_=closure(initial,[actions[0],actions[3]],admissible_only=True); post,path=closure(initial,actions,admissible_only=True)
    cases.append({'id':'C3_PROVIDER_AUTHORITY','supplierExists':True,'currentCapabilityBeforeAuthority':'verified_artifact' in pre,'qualifiedPath':path,'currentCapabilityAfterAdmissibleClosure':'verified_artifact' in post,'supports':'SupplierExists != CurrentCapability; PhysicalReachability != AuthorizedReachability'})
    # C4: more primitive actions can add no valid capability.
    safe=[Action('measure',frozenset({'sample'}),frozenset({'evidence'}))]
    expanded=safe+[Action('unsafe_destroy_sample',frozenset({'sample'}),frozenset({'interesting_debris'}),frozenset({'sample'}),admissible=False)]
    base,_=closure({'sample'},safe); ext,_=closure({'sample'},expanded)
    cases.append({'id':'C4_RAW_ACTION_NON_GAIN','rawActionCountBefore':len(safe),'rawActionCountAfter':len(expanded),'validReachableBefore':sorted(base),'validReachableAfter':sorted(ext),'supports':'MoreRawActions != MoreValidCapability'})
    # C5: constraints can increase robust reachability under adversarial/nondeterministic primitive selection.
    # Robust one-step reachability: every admissible first action must leave some path to target.
    def robust(actions):
        start={'sealant','leak'}
        for first in actions:
            if not first.requires <= start: continue
            s=(start-set(first.removes))|set(first.adds)
            rest=[a for a in actions if a.name!=first.name]
            fin,_=closure(s,rest)
            if 'sealed_hull' not in fin: return False
        return True
    good=Action('seal_hull',frozenset({'sealant','leak'}),frozenset({'sealed_hull'}))
    bad=Action('waste_sealant',frozenset({'sealant'}),frozenset({'decorated_panel'}),frozenset({'sealant'}))
    cases.append({'id':'C5_CONSTRAINT_ROBUSTNESS','robustWithBothActions':robust([good,bad]),'robustAfterConstraint':robust([good]),'supports':'Constraint can preserve future valid reachability'})
    # C6: external mature carrier compresses construction chain but verification remains.
    internal=[Action('buy_machine',frozenset({'spec'}),frozenset({'machine'})),Action('learn_process',frozenset({'machine'}),frozenset({'process_skill'})),Action('fabricate',frozenset({'machine','process_skill','spec'}),frozenset({'part'})),Action('verify',frozenset({'part'}),frozenset({'verified_part'}))]
    external=[Action('invoke_vendor',frozenset({'spec','funds'}),frozenset({'part'})),Action('verify',frozenset({'part'}),frozenset({'verified_part'}))]
    _,ip=closure({'spec','funds'},internal); _,ep=closure({'spec','funds'},external)
    cases.append({'id':'C6_EXTERNAL_COMPRESSION','internalPath':ip,'externalPath':ep,'internalSteps':len(ip),'externalSteps':len(ep),'verificationStillRequired':ep[-1]=='verify','supports':'External carrier can compress historical construction path without collapsing verification'})
    # C7: scale changes the governing blocker.
    local={'prototype','local_safety','throughput_1'}; scaled_target='throughput_1000'
    scale_actions=[Action('add_parallel_capacity',frozenset({'prototype'}),frozenset({'throughput_1000'})),Action('scale_safety_case',frozenset({'throughput_1000','local_safety'}),frozenset({'scaled_safety'}))]
    fin,path=closure(local,scale_actions)
    cases.append({'id':'C7_SCALE_BOUNDARY','localReachable':True,'scaledThroughputReached':scaled_target in fin,'scaledSystemQualified':'scaled_safety' in fin,'path':path,'supports':'PathQualified(target,scale1) != PathQualified(target,scale2)'})
    # C8: instrument changes epistemic discriminability.
    worlds={'w1':{'old_signal':'same','new_signal':'A'},'w2':{'old_signal':'same','new_signal':'B'}}
    old_distinguishable=worlds['w1']['old_signal']!=worlds['w2']['old_signal']; new_distinguishable=(worlds['w1']['old_signal'],worlds['w1']['new_signal'])!=(worlds['w2']['old_signal'],worlds['w2']['new_signal'])
    cases.append({'id':'C8_INSTRUMENT_DISCRIMINATION','beforeInstrumentDistinguishable':old_distinguishable,'afterInstrumentDistinguishable':new_distinguishable,'supports':'Observation capability can change question reachability'})
    # C9: lock-in can contract later composition options.
    open_state={'artifact','open_interface'}; locked_state={'artifact','closed_interface'}
    compose=Action('compose_future_module',frozenset({'artifact','open_interface'}),frozenset({'new_capability'}))
    o,_=closure(open_state,[compose]); l,_=closure(locked_state,[compose])
    cases.append({'id':'C9_LOCKIN_CONTRACTION','openInterfaceFutureCapability':'new_capability' in o,'closedInterfaceFutureCapability':'new_capability' in l,'supports':'ReachabilityGrowth != MonotonicProgress'})
    # C10: dormant reconstructible option vs active instance.
    dormant={'design','supplier_relation'}; active={'design','supplier_relation','active_fixture'}
    future=[Action('reconstruct_fixture',frozenset({'design','supplier_relation'}),frozenset({'active_fixture'})),Action('serve_new_target',frozenset({'active_fixture'}),frozenset({'new_target_served'}))]
    d,dp=closure(dormant,future); a,ap=closure(active,[future[1]])
    cases.append({'id':'C10_RECONSTRUCTIBLE_OPTION','dormantCanRecover':'new_target_served' in d,'activeCanServe':'new_target_served' in a,'dormantRecoveryPath':dp,'activePath':ap,'supports':'CapabilityInstance != ReconstructibleDesignOption; inactive != zero option value'})
    return cases

def random_dynamic_probe(seed=20260826,n=5000):
    rng=random.Random(seed); counterexamples=0; hard_stops=0; samples=[]
    for i in range(n):
        caps=[f'c{j}' for j in range(8)]; initial={caps[0]}; target=caps[-1]; actions=[]
        # guaranteed acyclic candidate construction edges, randomly omit some.
        for j in range(1,len(caps)):
            if rng.random()<0.78:
                req={caps[rng.randrange(0,j)]}
                if rng.random()<0.35 and j>1: req.add(caps[rng.randrange(0,j)])
                actions.append(Action(f'a{j}',frozenset(req),frozenset({caps[j]})))
        static=target in initial; final,path=closure(initial,actions); dynamic=target in final
        if (not static) and dynamic:
            counterexamples+=1
            if len(samples)<5: samples.append({'initial':sorted(initial),'target':target,'actions':[{'name':a.name,'requires':sorted(a.requires),'adds':sorted(a.adds)} for a in actions],'path':path})
        if not dynamic: hard_stops+=1
    return {'seed':seed,'worlds':n,'staticUnreachableButDynamicallyReachable':counterexamples,'stillUnreachableAfterClosure':hard_stops,'sampleCountermodels':samples,'interpretation':'Descriptive frequency has no empirical meaning; the generated model family only demonstrates that static-unreachable => permanently-unreachable is invalid without assumptions that freeze the capability basis.'}

def main():
    out={'schemaVersion':1,'kind':'ordivon.computing.historical-reachability-hr3-formal-countermodels','claimCeiling':['Formal/synthetic mechanism evidence only; not current-world prevalence.','Model construction can refute an unrestricted implication by counterexample but cannot establish that a real target has the modeled transition path.'], 'cases':case_results(),'randomProbe':random_dynamic_probe()}
    (ROOT/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(out['cases']),'randomProbe':{k:v for k,v in out['randomProbe'].items() if k!='sampleCountermodels'}},indent=2))
if __name__=='__main__': main()
