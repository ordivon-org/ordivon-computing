import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-f-probabilistic-randomized-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))

check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('round-f-requested', d['numbering']['requestedRound']=='F')
check('round-e-not-fabricated', d['numbering']['roundEFabricated'] is False)
check('fifty-probes', len(d['probes'])>=50)
for pid,token in [
 ('F-F1','RandomChoice'),('F-F4','SeedValue'),('F-F7','SameOutcomeSupport'),
 ('F-F8','ObservedRandomizedRun'),('F-F10','MostLikelyOutput'),('F-F11','SameExpectedOutput'),
 ('F-F13','ProbabilisticChoice != NondeterministicChoice'),('F-F14','SchedulerOrAdversary'),
 ('F-F16','EpistemicIgnorance'),('F-F20','NumericalErrorMagnitude'),('F-F23','OneSidedError'),
 ('F-F24','RandomizedRuntime'),('F-F26','AmplificationCouples'),('F-F28','IndependentTrials'),
 ('F-F29','RuntimeRiskProfile'),('F-F30','HighProbabilityBound'),('F-F31','HighProbabilityAccuracy'),
 ('F-F34','CompleteRiskProfile'),('F-F35','ExpectedCostOverInputs'),('F-F38','OneProbabilityDistribution'),
 ('F-F39','RandomBitResourceEquivalence'),('F-F42','PhysicalEntropyTruthStore'),
 ('F-F43','DistributionalCorrectness'),('F-F46','ExactTraceSetInclusion'),
 ('F-F48','SamplingPolicyIdentity'),('F-F49','SamplingRandomness'),('F-F50','AgentFailureProbability')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=14)
for x in ['Randomness','RandomSeed','Probability','ExpectedValue','Variance','FailureProbability','MonteCarlo','LasVegas','RandomizedAlgorithm','Scheduler','SamplingEntropy']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalStochasticityDistributionAndRiskResponsibility')
check('survivor-cross-cutting', d['survivor']['classification'].startswith('STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE'))
check('survivor-refactors-c', 'REFACTORS_ROUND_C' in d['survivor']['classification'])
check('survivor-extends-b', 'EXTENDS_ROUND_B_AGGREGATION' in d['survivor']['classification'])
check('survivor-composes-d', 'COMPOSES_WITH_ROUND_D_VALIDATION' in d['survivor']['classification'])
check('survivor-strengthens-a', 'STRENGTHENS_ROUND_A_ENVIRONMENT_ASSUMPTIONS' in d['survivor']['classification'])
check('survivor-not-independent', 'NOT_INDEPENDENT_UNIVERSAL_ESSENCE' in d['survivor']['classification'])
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('ten-burdens', len(d['survivor']['burden'])==10)
for b in ['RandomnessOrStochasticSourceRole','ProbabilitySpaceOrSourceDistributionSemantics','DistributionalSemanticTarget','NondeterministicOrAdversarialResolutionSemanticsWhenPresent','IndependenceDependenceOrCouplingAssumptions','ProbabilisticCorrectnessOrRiskProperty','DistributionalSummaryOrAggregationSemantics','AmplificationOrCompositionRelation','EvidenceCertificationOrAcceptanceConsequence']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-typed', d['roundARelation']['status']=='STRENGTHENED_AND_TYPED')
check('round-b-extended', d['roundBRelation']['status']=='EXTENDED_NOT_ABSORBED')
check('round-b-separation', 'DistributionalSemanticEquivalence != ResourceDistributionEquivalence' in d['roundBRelation']['law'])
check('round-c-refactored', d['roundCRelation']['status']=='REFACTORED')
check('round-d-composes', d['roundDRelation']['status']=='COMPOSES_NOT_ABSORBS')
check('failure-vs-error', d['roundDRelation']['law']=='FailureProbability != ApproximationErrorMagnitude')
check('computability-not-hyper', d['computabilityResult']['law']=='RandomizedComputation != Hypercomputability')
for owner in ['Runtime','WorldDomain','HardwareSecurity','Human','Network','Harness']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('five-external-pressure', len(d['externalPressure'])>=5)
check('gill-pressure', any('Gill' in x for x in d['externalPressure']))
check('yao-pressure', any('Yao' in x for x in d['externalPressure']))
check('solovay-pressure', any('Solovay-Strassen' in x for x in d['externalPressure']))
check('kozen-pressure', any('Kozen' in x for x in d['externalPressure']))
check('segala-pressure', any('Segala-Lynch' in x for x in d['externalPressure']))
check('randomness-essence-rejected', d['verdict']['randomnessUniversalEssence']=='REJECTED')
check('hypercomputability-rejected', d['verdict']['randomnessHypercomputability']=='REJECTED')
check('one-probability-rejected', d['verdict']['oneProbabilityScalar']=='REJECTED')
check('expectation-semantics-rejected', d['verdict']['expectedValueCompleteSemantics']=='REJECTED')
check('probability-nondeterminism-rejected', d['verdict']['probabilityEqualsNondeterminism']=='REJECTED')
check('randomness-uncertainty-rejected', d['verdict']['randomnessEqualsUncertainty']=='REJECTED')
check('failure-approximation-rejected', d['verdict']['failureProbabilityEqualsApproximationError']=='REJECTED')
check('expected-tail-rejected', d['verdict']['expectedBoundEqualsTailWorstCase']=='REJECTED')
check('very-high-info', d['verdict']['informationGain']=='VERY_HIGH')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('not-independent-sibling', d['verdict']['candidateIndependentUniversalSibling'] is False)

for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
