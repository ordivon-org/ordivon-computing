import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-i-effective-solvability-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))
check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('fifty-four-probes', len(d['probes'])>=54)
for pid,token in [
 ('I-F1','TotalComputableFunction'),('I-F6','Recognizable != Decidable'),('I-F9','Enumerable != Decidable'),
 ('I-F11','EveryInstanceUnanswerable'),('I-F13','UniformDecidability'),('I-F15','Undecidable != Intractable'),
 ('I-F16','ResourceFeasibility'),('I-F18','PhysicalChurchTuringTheorem'),('I-F19','HaltingFamily'),
 ('I-F21','HaltingProblemOnly'),('I-F22','SemanticPropertyDecidability'),('I-F24','AutomaticallyUndecidable'),
 ('I-F25','RestrictedDomain'),('I-F27','PromiseProblem'),('I-F28','A_ReducesTo_B'),
 ('I-F29','SemanticIdentity'),('I-F30','ComplexityPreservingReduction'),('I-F31','ManyOneReducibility'),
 ('I-F32','ReductionType'),('I-F34','EveryStrongerModel'),('I-F35','PhysicalRealizability'),
 ('I-F36','OrdinaryResourceDimension'),('I-F39','EndOfUndecidability'),('I-F40','UncomputabilityTheorem'),
 ('I-F41','DecidabilityTheorem'),('I-F43','CoordinationImpossibility != Undecidability'),('I-F44','GenericSolvabilityInterface'),
 ('I-F45','PhysicallyRealizableHere'),('I-F47','ModelFreeCollapse'),('I-F48','ExactDeterministicDecider'),
 ('I-F51','UniformComputability'),('I-F53','ComputationalModelAndPrimitives'),('I-F54','OutcomeModeAndContract')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=15)
for x in ['Computable','Decidable','Undecidable','Algorithm','HaltingProblem','RecursivelyEnumerable','Reduction','Oracle','ChurchTuringThesis','Hypercomputation','CompleteProblem']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalEffectiveSolvabilityAndRelativePowerResponsibility')
check('survivor-strong', d['survivor']['classification'].startswith('STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE'))
check('independent-axis', 'INDEPENDENT_EFFECTIVE_POSSIBILITY_AXIS' in d['survivor']['classification'])
check('upstream-g', 'GENERIC_SOLVABILITY_LAYER_UPSTREAM_OF_G' in d['survivor']['classification'])
check('orthogonal-b-h', 'ORTHOGONAL_TO_B_RESOURCE_FEASIBILITY_AND_H_PHYSICAL_REALIZATION' in d['survivor']['classification'])
check('not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('eleven-burdens', len(d['survivor']['burden'])==11)
for b in ['ProblemFunctionOrRelationSpecification','DomainPromiseAndEncodingScope','ComputationalModelAndAdmittedPrimitives','RequiredOutcomeMode','TotalityOrTerminationRequirement','EffectiveStatusClaim','ReductionOrRelativeComputabilityRelation','OracleOrAuxiliaryPowerAssumptions','UniformityOrQuantificationRegime','SolvabilityOrImpossibilityTheoremRelation','ProofReductionDiagonalizationOrWitnessBasis']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-distinct', d['roundARelation']['status']=='DISTINCT_BUT_CONSUMES_BEHAVIOR_CONTRACT')
check('run-vs-decision', d['roundARelation']['law']=='RunTerminationSemantics != ProblemDecidabilityByIdentity')
check('round-b-orthogonal', d['roundBRelation']['status']=='CLEANLY_ORTHOGONAL')
check('solvability-vs-feasibility', d['roundBRelation']['law']=='EffectiveSolvability != ResourceFeasibility')
check('round-c-linked', d['roundCRelation']['status']=='STRONGLY_LINKED_NOT_ABSORBED')
check('semantic-vs-decidability', d['roundCRelation']['law']=='SemanticMeaning != DecidabilityOfSemanticProperty')
check('round-g-refactor', d['roundGRelation']['status']=='OWNERSHIP_REFACTOR')
check('round-h-linked', d['roundHRelation']['status']=='ORTHOGONAL_BUT_LINKED')
check('oracle-vs-physical', d['roundHRelation']['law']=='OracleRelativeOrAbstractComputability != PhysicalRealizability')
check('round-f-overlay', d['roundFRelation']['status']=='OVERLAY_NOT_REPLACEMENT')
check('m4-reconstructed', 'SUBSTANTIALLY_RECONSTRUCTED' in d['rivalModelUpdate']['M4_EffectiveProcedure'])
for owner in ['Runtime','WorldHardware','Network','Human','Harness','MathematicsLogic']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('five-external-pressure', len(d['externalPressure'])>=5)
for token in ['Turing 1936','Turing 1939','Post 1944','Kleene 1943','Rice 1953']:
    check('pressure-'+token.lower().replace(' ','-'), any(token in x for x in d['externalPressure']))
for key in ['computableUniversalBoolean','undecidableEqualsIntractable','undecidableEqualsEveryInstanceUnknown','reductionEqualsSemanticIdentity','oracleEqualsPhysicalCapability','haltingProblemExhaustsUndecidability','churchTuringAsPhysicalTheorem']:
    check('rejected-'+key, d['verdict'][key]=='REJECTED')
check('very-high-decisive', d['verdict']['informationGain']=='VERY_HIGH_ARCHITECTURALLY_DECISIVE')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('candidate-independent', d['verdict']['candidateStrongIndependentAxis'] is True)
check('refactors-g', d['verdict']['genericSolvabilityOwnershipRefactorsG'] is True)
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
