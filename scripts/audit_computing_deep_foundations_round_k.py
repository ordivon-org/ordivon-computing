import json
from pathlib import Path
p=Path('research/evidence/computing-deep-foundations-round-k-information-coding-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))
check('cdf0-not-admitted', not d['routeAdmission']['cdf0'])
check('numbered-not-admitted', not d['routeAdmission']['numberedFoundation'])
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('sixty-probes', len(d['probes'])>=60)
for pid,token in [('K-F1','SemanticMeaning'),('K-F4','ShannonEntropyCarrier'),('K-F6','SameSourceDistribution'),('K-F8','ShannonEntropy'),('K-F11','CompressionByIdentity'),('K-F14','UselessDuplication'),('K-F16','ReliabilityObjective'),('K-F19','MeasuredThroughput'),('K-F21','CapacityClaim'),('K-F23','SemanticRelevance'),('K-F24','CausalInfluence'),('K-F26','DefinitionOfComputation'),('K-F28','LossyCompression'),('K-F31','SourceOnlyIntrinsicScalar'),('K-F34','SideInformation'),('K-F36','DecoderContextRelative'),('K-F39','ShannonEntropyOfSource'),('K-F43','MachineIndependent'),('K-F45','KolmogorovComplexity'),('K-F46','AlgorithmicIncompressibility'),('K-F48','HighAlgorithmicComplexity'),('K-F50','EffectivelyComputableObservable'),('K-F51','OracleCapability'),('K-F53','AccessSemantics'),('K-F55','ContinuationRelevantState'),('K-F57','UsableInformationCapacity'),('K-F58','SemanticInformation'),('K-F60','TaskStateSufficiency')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('deleted-many', len(d['deletedUniversalPrimitives'])>=14)
for x in ['Information','Entropy','MutualInformation','Compression','Redundancy','ChannelCapacity','DescriptionLength','KolmogorovComplexity','AlgorithmicRandomness','Distortion']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalInformationCodingAndRecoverabilityConstraintResponsibility')
check('survivor-cross-cutting', d['survivor']['classification'].startswith('STRONG_CROSS_CUTTING_ANALYTIC_CANDIDATE'))
check('m3-rejected-class', 'M3_INFORMATION_TRANSFORMATION_REJECTED_AS_UNIVERSAL_DEFINITION' in d['survivor']['classification'])
check('feeds-b', 'FEEDS_B_RESOURCE_BOUNDS' in d['survivor']['classification'])
check('not-clean-sibling', 'NOT_CLEAN_INDEPENDENT_SIBLING' in d['survivor']['classification'])
check('not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('thirteen-burdens', len(d['survivor']['burden'])==13)
for b in ['SourceEnsembleOrIndividualObjectModel','ProbabilityOrEffectiveDescriptionModelReference','InformationQuantityOrMeasureType','EncodingOrCodeRelation','DecoderOrReconstructionRelation','SideInformationCorrelationOrConditioningAssumptions','LosslessOrDistortionRecoverabilityCriterion','RateCapacityCompressionOrRedundancyClaim','AsymptoticFiniteBlockOrIndividualObjectRegime','SemanticOrTaskRelevanceDisclaimerReference','ProofOrCodingTheoremBasis']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('b-linked', d['roundBRelation']['status']=='TIGHTLY_LINKED_ANALYTIC_INPUT')
check('b-law', d['roundBRelation']['law']=='InformationTheoreticLowerBound != ResourceUsageObservationByIdentity')
check('c-separated', d['roundCRelation']['status']=='SEMANTICS_SEPARATED')
check('c-law', d['roundCRelation']['law']=='InformationQuantity != SemanticInterpretation')
check('d-dep', d['roundDRelation']['status']=='LOSSY_CODING_DEPENDS_ON_D')
check('f-ref', d['roundFRelation']['status']=='PROBABILITY_MODEL_REFERENCE')
check('h-sep', d['roundHRelation']['status']=='PHYSICAL_REALIZATION_SEPARATED')
check('i-ref', d['roundIRelation']['status']=='ALGORITHMIC_INFORMATION_REFERENCES_EFFECTIVE_MODEL')
check('j-sep', d['roundJRelation']['status']=='RETENTION_SUFFICIENCY_SEPARATED')
for owner in ['Mathematics','Network','Media','WorldHardware','Runtime','Human']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('six-sources', len(d['externalPressure'])>=6)
for token in ['Shannon 1948','Hamming 1950','Shannon 1959','Slepian-Wolf 1973','Kolmogorov 1965','Chaitin 1966']:
    check('source-'+token.lower().replace(' ','-'), any(token in x for x in d['externalPressure']))
check('m3-rival-rejected', d['rivalModelUpdate']['M3_InformationTransformation'].startswith('REJECTED_AS_UNIVERSAL_DEFINITION'))
for key in ['informationUniversalEssence','entropyEqualsMeaning','compressionDefinesComputation','redundancyEqualsWaste','channelCapacityEqualsNetworkBandwidth','mutualInformationEqualsCausationOrMeaning','shannonEqualsAlgorithmicInformation','codecLengthEqualsKolmogorovComplexity','informationContentEqualsComputationalPower']:
    check('rejected-'+key, d['verdict'][key]=='REJECTED')
check('high-consolidating', d['verdict']['informationGain']=='HIGH_CONSOLIDATING_RIVAL_RESOLVING')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('not-clean-independent', d['verdict']['candidateCleanIndependentSibling'] is False)
check('m3-resolved', d['verdict']['m3Resolved'] is True)
check('second-consolidation', d['verdict']['secondConsecutiveConsolidationSignal'] is True)
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
