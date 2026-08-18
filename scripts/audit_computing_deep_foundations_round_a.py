import json
from pathlib import Path

p = Path('research/evidence/computing-deep-foundations-round-a-interactive-behavior-20260818.json')
d = json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))

check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('twenty-five-probes', len(d['probes'])>=25)
for pid, token in [
 ('A-F1','SameFinalOutput'),('A-F2','NonTermination'),('A-F4','PriorOutput'),
 ('A-F6','MoreBehaviorallyExpressive'),('A-F7','BoundaryRelative'),('A-F8','Interaction != necessary'),
 ('A-F10','ProgramText'),('A-F12','SameTraceSet'),('A-F14','Persistence'),
 ('A-F15','WorldTruthStore'),('A-F16','NetworkTransport'),('A-F17','RuntimeJobContinuity'),
 ('A-F19','AgentEra'),('A-F21','Nondeterminism != Interaction'),('A-F23','ObserverUncertainty'),
 ('A-F24','TerminationDoesNotImplyCorrectness'),('A-F25','NonterminationDoesNotImplyIncorrectness')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('nine-deleted-primitives', len(d['deletedUniversalPrimitives'])>=9)
for x in ['FunctionEvaluation','FinalOutput','Termination','Interaction','Trace','Program']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('m1-rejected-universal', d['rivalModelUpdate']['M1_FunctionEvaluation'].startswith('REJECT_UNIVERSAL'))
check('m2-partial', d['rivalModelUpdate']['M2_ControlledStateTransition'].startswith('PARTIAL_SURVIVOR'))
check('m4-qualified', 'REJECT_IF_CLOSED_TERMINATING' in d['rivalModelUpdate']['M4_EffectiveProcedure'])
check('m6-rejected-universal', d['rivalModelUpdate']['M6_InteractiveProcess'].startswith('REJECT_UNIVERSAL'))
check('survivor-name', d['survivor']['name']=='ComputationalBoundaryAndBehaviorResponsibility')
check('survivor-strong', d['survivor']['classification'].startswith('STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE'))
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('survivor-six-burdens', len(d['survivor']['burden'])==6)
for b in ['ComputationalBoundary','TransitionOrBehaviorSemantics','InteractionInterfaceWhenPresent','ObservationOrEquivalenceSemantics','ContinuationOrTerminationSemantics','EnvironmentAssumptions']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('anti-collapse-rich', len(d['antiCollapse'])>=16)
check('hypercomputability-separated', any('HypercomputableFunctionPower' in x for x in d['antiCollapse']))
for owner in ['Runtime','Network','World','Human','Harness']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('external-pressure-six', len(d['externalPressure'])>=6)
check('interactive-rejected', d['verdict']['interactiveAsUniversalFoundation']=='REJECTED')
check('closed-function-rejected', d['verdict']['closedFunctionAsUniversalFoundation']=='REJECTED')
check('terminating-procedure-rejected', d['verdict']['finiteTerminatingProcedureAsUniversalFoundation']=='REJECTED')
check('hypercomputability-rejected', d['verdict']['interactionImpliesHypercomputability']=='REJECTED')
check('high-info-gain', d['verdict']['informationGain']=='HIGH')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)

for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
