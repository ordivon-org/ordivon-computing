import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-c-semantics-equivalence-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))

check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('thirty-one-probes', len(d['probes'])>=31)
for pid,token in [
 ('C-F1','SourceProgramText'),('C-F3','SemanticIdentity'),('C-F6','WellFormedProgram'),
 ('C-F7','TargetRepresentationIdentity'),('C-F9','ExactBehaviorSetEquality'),
 ('C-F10','AbstractResourceBehavior'),('C-F12','ObservationContextSemantics'),
 ('C-F14','ContextualEquivalence'),('C-F17','PartialCorrectness'),('C-F20','ParametricityConstraint'),
 ('C-F21','AbstractBehaviorIdentity'),('C-F22','BoundaryContextRelative'),
 ('C-F24','EndToEndSemanticCorrectness'),('C-F26','Equivalence != Refinement'),
 ('C-F27','ResourcePreservation'),('C-F28','ComplexityEquivalence'),
 ('C-F30','AgentEraSemanticKind'),('C-F31','SelfContainedProgramSemantics')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=11)
for x in ['Program','Syntax','ProgrammingLanguage','Type','Specification','ContextualEquivalence','CompilerTranslation']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalInterpretationAndSemanticRelationResponsibility')
check('survivor-strong', d['survivor']['classification'].startswith('STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE'))
check('survivor-refactors-a', 'OVERLAPS_AND_REFACTORS_ROUND_A' in d['survivor']['classification'])
check('survivor-does-not-absorb-b', 'DOES_NOT_ABSORB_ROUND_B' in d['survivor']['classification'])
check('survivor-not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('nine-burdens', len(d['survivor']['burden'])==9)
for b in ['RepresentationOrModelDomain','SemanticInterpretationRelation','ObservationOrContextSemantics','EquivalenceRefinementOrPreorderRelation','PreservationOrCorrectnessClaim','SemanticRegimeCurrentnessAndProvenance']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-overlap', d['roundARelation']['status']=='OVERLAPS_AND_REFACTORS_NOT_FULLY_ABSORBED')
check('round-a-two-generalized', len(d['roundARelation']['absorbedOrGeneralized'])==2)
check('round-a-four-distinct', len(d['roundARelation']['remainingDistinct'])==4)
check('round-b-orthogonal', d['roundBRelation']['status']=='REMAINS_ORTHOGONAL')
check('semantic-resource-separated', d['roundBRelation']['law']=='SemanticEquivalence != ResourceEquivalence')
check('m2-interpretation-required', 'INTERPRETATION_AND_OBSERVATION' in d['rivalModelUpdate']['M2_ControlledStateTransition'])
check('m7-grounding-pressure', 'GROUNDING_PRESSURE' in d['rivalModelUpdate']['M7_PhysicalRealization'])
for owner in ['Runtime','Harness','World','Human','Security']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('four-external-pressure', len(d['externalPressure'])>=4)
check('hoare-pressure', any('Hoare' in x for x in d['externalPressure']))
check('pitts-pressure', any('Pitts' in x for x in d['externalPressure']))
check('reynolds-pressure', any('Reynolds' in x for x in d['externalPressure']))
check('compcert-pressure', any('CompCert' in x for x in d['externalPressure']))
check('pl-semantics-universal-rejected', d['verdict']['programmingLanguageSemanticsUniversal']=='REJECTED')
check('one-equivalence-rejected', d['verdict']['oneUniversalEquivalence']=='REJECTED')
check('representation-preservation-rejected', d['verdict']['semanticPreservationEqualsRepresentationPreservation']=='REJECTED')
check('resource-equivalence-rejected', d['verdict']['semanticEquivalenceEqualsResourceEquivalence']=='REJECTED')
check('very-high-info', d['verdict']['informationGain']=='VERY_HIGH')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('round-a-refactored', d['verdict']['roundAPartiallyRefactored'] is True)
check('round-b-survives', d['verdict']['roundBSurvives'] is True)

for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
