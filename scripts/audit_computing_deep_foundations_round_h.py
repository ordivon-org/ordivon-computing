import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-h-physical-realization-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))
check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('forty-eight-probes', len(d['probes'])>=48)
for pid,token in [
 ('H-F1','PhysicalStateChange'),('H-F2','PostHocTrajectoryMapping'),('H-F3','CounterfactuallySupported'),
 ('H-F6','StateEncoding'),('H-F8','ComputationallyObservableDifference'),('H-F10','ManyToOneAbstractFunction'),
 ('H-F11','PhysicalEnergyDissipation'),('H-F12','ZeroDissipation'),('H-F14','SameResourceProfile'),
 ('H-F16','ThermodynamicReversibility'),('H-F18','AnalogComputation'),('H-F20','InfiniteUsablePrecision'),
 ('H-F22','AccessibleComputationalInformation'),('H-F24','EffectivelyComputableEvolution'),('H-F25','PhysicallyUsableHypercomputer'),
 ('H-F26','RepresentationAndAccessSemantics'),('H-F28','QuantumComputation'),('H-F30','QuantumSpeedup'),
 ('H-F31','ClassicalQuantumResourceProfile'),('H-F34','PhysicalDeviceTruth'),('H-F35','SemanticallyPassive'),
 ('H-F37','CompleteComputationalImplementation'),('H-F39','SuccessfulComputationalRealization'),('H-F40','UnconstrainedMappingAccount'),
 ('H-F42','CounterfactualAndFidelity'),('H-F43','TraceReplay'),('H-F44','Programmability'),
 ('H-F45','CorrectPhysicalImplementation'),('H-F48','AlgorithmicComplexityLowerBound')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=17)
for x in ['PhysicalProcess','InformationProcessing','Reversibility','LogicalReversibility','AnalogContinuity','InfinitePrecision','Qubit','Measurement','Simulation','HumanIntent','Programmability']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalPhysicalRealizationAndGroundingResponsibility')
check('survivor-strong', d['survivor']['classification'].startswith('STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE'))
check('anti-pancomputational', 'ANTI_PANCOMPUTATIONAL_GROUNDING' in d['survivor']['classification'])
check('not-reducible-c', 'NOT_REDUCIBLE_TO_C' in d['survivor']['classification'])
check('bridge-world-hardware', 'CROSS_OWNER_BRIDGE_TO_WORLD_HARDWARE' in d['survivor']['classification'])
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('eleven-burdens', len(d['survivor']['burden'])==11)
for b in ['AbstractComputationalTargetOrModel','PhysicalSubstrateOrSystemBoundary','EncodingOrPreparationRelation','PhysicalEvolutionOrOperationRelation','ReadoutDecodingOrObservationRelation','CounterfactualOrDomainSupport','FidelityToleranceOrErrorRelation','PhysicalModelAssumptionsAndCurrentness','RealizationEvidenceOrValidationBasis','MiscomputationOrOutOfModelDisposition']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-grounding', d['roundARelation']['status']=='SURVIVES_H_UPSTREAM_GROUNDING')
check('round-b-linked', d['roundBRelation']['status']=='SURVIVES_STRONGLY_LINKED')
check('abstract-physical-resource-separated', d['roundBRelation']['law']=='AbstractResourceModel != ActualPhysicalResourceProfile')
check('round-c-refactored', d['roundCRelation']['status']=='STRONGLY_REFACTORED_BOUNDARY_CLARIFIED')
check('semantic-physical-relation-separated', d['roundCRelation']['law']=='SemanticInterpretationRelation != PhysicalImplementationRelationByIdentity')
check('round-d-composes', d['roundDRelation']['status']=='COMPOSES_NOT_ABSORBS')
check('round-f-composes', d['roundFRelation']['status']=='COMPOSES_NOT_ABSORBS')
check('round-g-survives', d['roundGRelation']['status']=='SURVIVES_REALIZATION_DISTINCT')
check('m7-reconstructed', 'SUBSTANTIALLY_RECONSTRUCTED' in d['rivalModelUpdate']['M7_PhysicalRealization'])
check('hypercomputation-not-admitted', d['hypercomputation']['admitted'] is False)
check('hyper-law', 'PhysicallyUsableHypercomputer' in d['hypercomputation']['law'])
check('pct-not-definition', d['physicalChurchTuring']['admittedAsDefinition'] is False)
check('pct-unresolved', d['physicalChurchTuring']['status']=='SUBSTANTIVE_UNRESOLVED_THESIS')
for owner in ['World','Hardware','Runtime','Human','Security','Network']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('six-external-pressure', len(d['externalPressure'])>=6)
for token in ['Landauer','Bennett','Shannon','Pour-El/Richards','Bernstein-Vazirani','Horsman']:
    check('pressure-'+token.lower().replace('/','-'), any(token in x for x in d['externalPressure']))
for key in ['physicalProcessUniversal','informationProcessingUniversalGrounding','pureMappingSufficient','pureIntentSufficient','logicalReversibilityEqualsZeroDissipation','continuousStateEqualsInfiniteUsablePrecision','quantumSpeedupEqualsHypercomputability','mathematicalNoncomputableEvolutionEqualsPhysicalHypercomputer']:
    check('rejected-'+key, d['verdict'][key]=='REJECTED')
check('very-high-decisive', d['verdict']['informationGain']=='VERY_HIGH_ARCHITECTURALLY_DECISIVE')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('grounding-addressed', d['verdict']['antiPancomputationalGroundingAddressed'] is True)
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
