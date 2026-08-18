import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-b-resource-plurality-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))

check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('thirty-six-probes', len(d['probes'])>=36)
for pid,token in [
 ('B-F1','WallClockTime'),('B-F3','TimeCost != SpaceCost'),('B-F5','DataMovementCost'),
 ('B-F8','CommunicationComplexity'),('B-F10','BitComplexity != MessageComplexity'),
 ('B-F11','ParallelTime != TotalWork'),('B-F15','SameEnergyCost'),('B-F17','FirstClassComputationalResource'),
 ('B-F19','QueryComplexity'),('B-F20','BitComplexity'),('B-F22','BehavioralEquivalence'),
 ('B-F24','ResourceBoundCanBeSemanticallyConstitutive'),('B-F26','Underspecified'),
 ('B-F29','AverageCost != WorstCaseCost'),('B-F31','ComplexityTheorem'),
 ('B-F32','ResourceVectorsCanBeIncomparable'),('B-F34','TokenCount'),('B-F35','ModelCompute != ToolQueryCost')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=17)
for x in ['Time','Space','OperationCount','IO','CommunicationBits','ParallelDepth','Energy','Samples','Queries','Precision','TokenCount','SingleScalarComplexity']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalResourceAndFeasibilityResponsibility')
check('survivor-strong', d['survivor']['classification'].startswith('STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE'))
check('survivor-orthogonal-a', 'ORTHOGONAL_TO_ROUND_A' in d['survivor']['classification'])
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('eight-burdens', len(d['survivor']['burden'])==8)
for b in ['ComputationOrProblemTargetRef','ComputationalModelAndAdmittedOperations','ResourceDimensions','UnitsAndAccountingScope','ScaleOrInstanceSizeSemantics','AggregationSemantics','BoundBudgetOrComparisonClaim','FeasibilityOrAdmissibilityConsequence']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-orthogonal', d['roundARelation']['status']=='ORTHOGONAL_BUT_COUPLED')
check('behavior-cost-separated', d['roundARelation']['law']=='ComputationalBehavior != ComputationalCostProfile')
check('m5-rejected-universal-strong-burden', 'REJECT_UNIVERSAL_DEFINITION' in d['rivalModelUpdate']['M5_ResourceBoundedProcess'])
check('m7-physical-pressure', 'ENERGY_PRECISION_DATA_MOVEMENT' in d['rivalModelUpdate']['M7_PhysicalRealization'])
for owner in ['Runtime','Network','WorldHardware','Human','Harness']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('eight-external-pressure', len(d['externalPressure'])>=8)
check('blum-pressure', any('Blum' in x for x in d['externalPressure']))
check('yao-pressure', any('Yao' in x for x in d['externalPressure']))
check('hong-kung-pressure', any('Hong-Kung' in x for x in d['externalPressure']))
check('landauer-pressure', any('Landauer' in x for x in d['externalPressure']))
check('time-space-only-rejected', d['verdict']['timeSpaceOnly']=='REJECTED')
check('single-scalar-rejected', d['verdict']['singleUniversalScalar']=='REJECTED')
check('resources-metadata-rejected', d['verdict']['resourcesAlwaysMetadata']=='REJECTED')
check('resource-essence-rejected', d['verdict']['resourceBoundUniversalEssence']=='REJECTED')
check('very-high-info', d['verdict']['informationGain']=='VERY_HIGH')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('round-a-survives', d['verdict']['roundASurvives'] is True)

for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
