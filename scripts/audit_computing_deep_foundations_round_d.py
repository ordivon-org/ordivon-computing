import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-d-numerical-approximate-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))

check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('thirty-nine-probes', len(d['probes'])>=39)
for pid,token in [
 ('D-F1','FloatingPointSemanticEquivalence'),('D-F3','AcrossPrecisions'),('D-F5','PrecisionResourceRole'),
 ('D-F6','NumericalError != RoundoffError'),('D-F9','ForwardError != BackwardError'),
 ('D-F10','ProblemConditioning != AlgorithmStability'),('D-F13','BackwardStability'),
 ('D-F15','SmallResidual'),('D-F18','NormwiseError'),('D-F20','ApproximateResult'),
 ('D-F21','Tolerance != Error'),('D-F23','CurrentIterateAccurate'),('D-F25','FinitePrecisionRunConvergence'),
 ('D-F26','Stopped != Converged'),('D-F28','DominantWorkingPrecision'),('D-F30','BetterProblemConditioning'),
 ('D-F31','LowerTotalError'),('D-F33','PointEstimate'),('D-F34','CertifiedAccuracy'),
 ('D-F36','ExceptionalArithmeticOutcome'),('D-F37','BitwiseReproducible'),('D-F39','DeclaredPropertyMetricAcceptance')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('thirteen-deleted-primitives', len(d['deletedUniversalPrimitives'])>=13)
for x in ['ExactResult','Error','Precision','Tolerance','Residual','ConditionNumber','Stability','Accuracy','Convergence','PointEstimate','BitwiseEquality']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalApproximationErrorAndValidationResponsibility')
check('survivor-cross-cutting', d['survivor']['classification'].startswith('STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE'))
check('survivor-refactors-c', 'REFACTORS_ROUND_C' in d['survivor']['classification'])
check('survivor-couples-b', 'PARTIALLY_COUPLES_ROUND_B' in d['survivor']['classification'])
check('survivor-strengthens-a', 'STRENGTHENS_ROUND_A' in d['survivor']['classification'])
check('survivor-not-independent-essence', 'NOT_INDEPENDENT_UNIVERSAL_ESSENCE' in d['survivor']['classification'])
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('nine-burdens', len(d['survivor']['burden'])==9)
for b in ['ReferenceTargetOrProblem','ArithmeticRepresentationAndPrecisionRegime','ApproximationOrComparisonRelation','ConditioningOrSensitivityClaim','AlgorithmicStabilityOrBackwardRelation','ConvergenceAndStoppingSemantics','ErrorBoundCertificationEnclosureOrEvidence','AcceptanceOrValidityConsequence']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-strengthened', d['roundARelation']['status']=='STRENGTHENED')
check('round-b-partial-coupling', d['roundBRelation']['status']=='PARTIALLY_COUPLED_NOT_ABSORBED')
check('resource-error-separated', d['roundBRelation']['law']=='ResourceProfile != ErrorProfile')
check('round-c-refactored', d['roundCRelation']['status']=='REFACTORED')
check('exact-finite-separated', d['roundCRelation']['law']=='ExactDenotationalEquality != FinitePrecisionBehavioralEquivalence')
for owner in ['Runtime','WorldDomain','Hardware','Human','Harness']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('six-external-pressure', len(d['externalPressure'])>=6)
check('ieee-pressure', any('IEEE 754' in x for x in d['externalPressure']))
check('wilkinson-pressure', any('Wilkinson' in x for x in d['externalPressure']))
check('rice-pressure', any('Rice' in x for x in d['externalPressure']))
check('carson-higham-pressure', any('Carson-Higham' in x for x in d['externalPressure']))
check('moore-pressure', any('Moore' in x for x in d['externalPressure']))
check('exact-result-rejected', d['verdict']['exactResultUniversal']=='REJECTED')
check('one-error-rejected', d['verdict']['oneErrorScalar']=='REJECTED')
check('precision-resource-only-rejected', d['verdict']['precisionOnlyResource']=='REJECTED')
check('precision-semantic-only-rejected', d['verdict']['precisionOnlySemantic']=='REJECTED')
check('tolerance-accuracy-rejected', d['verdict']['toleranceEqualsAccuracy']=='REJECTED')
check('residual-error-rejected', d['verdict']['residualEqualsSolutionError']=='REJECTED')
check('stability-accuracy-rejected', d['verdict']['stabilityEqualsAccuracy']=='REJECTED')
check('convergence-correctness-rejected', d['verdict']['convergenceEqualsFiniteRunCorrectness']=='REJECTED')
check('very-high-info', d['verdict']['informationGain']=='VERY_HIGH')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('not-independent-sibling', d['verdict']['candidateIndependentUniversalSibling'] is False)

for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
