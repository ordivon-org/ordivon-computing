import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-g-concurrency-distributed-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))

check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('forty-eight-probes', len(d['probes'])>=48)
for pid,token in [
 ('G-F1','Concurrency != PhysicalParallelExecution'),('G-F3','SameFinalState'),('G-F8','Linearizability != Consistency'),
 ('G-F9','Linearizability != Serializability'),('G-F10','Safety != Progress'),('G-F13','WaitFreedom'),
 ('G-F16','RuntimeScheduler'),('G-F18','UniversalTotalOrder'),('G-F19','LogicalClockOrder'),
 ('G-F23','ConsensusSafety'),('G-F25','InvalidUniversalization'),('G-F26','ConsensusSafety'),
 ('G-F27','ComputationalPossibility'),('G-F28','TaskSolvability'),('G-F29','EventuallyHolds'),
 ('G-F31','ByzantineFailure'),('G-F32','NetworkPartition'),('G-F33','GroundTruthCrash'),
 ('G-F34','UniversalChooseAnyTwo'),('G-F36','CAPImpossibilityClaim'),('G-F38','ComputationalSolvability'),
 ('G-F39','NetworkTopologyOrTransport'),('G-F42','ImpossibilityTheorem'),('G-F43','DeploymentCorrectnessEvidence'),
 ('G-F44','GlobalCoordinationCorrectness'),('G-F45','CentralCoordinatorExistence'),('G-F47','ConcurrencySchedule'),
 ('G-F48','ConcurrentSystemOutcome')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=18)
for x in ['Concurrency','Parallelism','Linearizability','Consistency','Consensus','GlobalOrder','GlobalClock','Synchrony','Failure','Availability','Scheduler','Fairness','WaitFreedom','PartitionTolerance']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalCoordinationConsistencyAndProgressResponsibility')
check('survivor-strong', d['survivor']['classification'].startswith('STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE'))
check('survivor-partial-orthogonal', 'PARTIALLY_ORTHOGONAL_TO_A_B_C_F' in d['survivor']['classification'])
check('survivor-irreducible', 'IRREDUCIBLE_COORDINATION_SOLVABILITY_BURDEN' in d['survivor']['classification'])
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('eleven-burdens', len(d['survivor']['burden'])==11)
for b in ['HistoryEventAndOrderStructure','CoordinationConsistencyOrSafetySpecification','ProgressOrLivenessRequirement','TimingOrSynchronyAssumptions','FailureOrAdversaryModel','SchedulerOrFairnessAssumptions','SolvabilityOrImpossibilityClaim','WitnessRefinementOrProofRelation']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-strengthened', d['roundARelation']['status']=='STRENGTHENED_NOT_ABSORBED')
check('round-b-orthogonal', d['roundBRelation']['status']=='ORTHOGONAL_BUT_REFERENCED')
check('solvability-cost-separated', d['roundBRelation']['law']=='CoordinationSolvability != CommunicationOrSynchronizationCostByIdentity')
check('round-c-overlap', d['roundCRelation']['status']=='OVERLAPS_NOT_ABSORBED')
check('round-f-corrected', d['roundFRelation']['status']=='OWNERSHIP_CORRECTION')
for owner in ['Runtime','Network','World','Security','Harness','Human']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('seven-external-pressure', len(d['externalPressure'])>=7)
for token in ['Lamport','Herlihy-Wing','Fischer-Lynch-Paterson','Dwork-Lynch-Stockmeyer','Herlihy 1991','Gilbert-Lynch','Segala-Lynch']:
    check('pressure-'+token.lower().replace(' ','-'), any(token in x for x in d['externalPressure']))
check('concurrency-essence-rejected', d['verdict']['concurrencyUniversalEssence']=='REJECTED')
check('consistency-boolean-rejected', d['verdict']['oneConsistencyBoolean']=='REJECTED')
check('consensus-primitive-rejected', d['verdict']['consensusUniversalPrimitive']=='REJECTED')
check('global-order-rejected', d['verdict']['globalTotalOrderUniversal']=='REJECTED')
check('timing-implementation-rejected', d['verdict']['timingModelImplementationOnly']=='REJECTED')
check('failure-primitive-rejected', d['verdict']['oneFailurePrimitive']=='REJECTED')
check('model-free-impossibility-rejected', d['verdict']['modelFreeImpossibility']=='REJECTED')
check('very-high-info', d['verdict']['informationGain']=='VERY_HIGH')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('not-clean-sibling', d['verdict']['candidateCleanIndependentSibling'] is False)
check('irreducible-burden', d['verdict']['irreducibleCoordinationSolvabilityBurden'] is True)

for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
