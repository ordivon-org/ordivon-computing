import json
from pathlib import Path

p=Path('research/evidence/computing-deep-foundations-round-j-state-memory-persistence-20260818.json')
d=json.loads(p.read_text())
checks=[]
def check(n,c): checks.append((n,bool(c)))
check('cdf0-not-admitted', d['routeAdmission']['cdf0'] is False)
check('numbered-not-admitted', d['routeAdmission']['numberedFoundation'] is False)
check('next-cdf-unknown', d['routeAdmission']['nextCdf']=='UNKNOWN')
check('next-route-unknown', d['routeAdmission']['nextComputingRoute']=='UNKNOWN')
check('fifty-seven-probes', len(d['probes'])>=57)
for pid,token in [
 ('J-F1','InternalMemory'),('J-F4','SameSemanticState'),('J-F7','SameHistory'),('J-F9','StateSufficiency'),
 ('J-F11','HistoryRepresentation'),('J-F13','MemoryFootprintIdentity'),('J-F16','PhysicalStorageMedium'),
 ('J-F18','ObjectIdentity'),('J-F21','StablePersistentReference'),('J-F22','AuthoritativeState'),
 ('J-F25','CacheCoherence != MemoryConsistency'),('J-F26','MemoryModelSemantics'),('J-F28','Linearizability'),
 ('J-F29','CurrentlyVisible'),('J-F30','Visible != Durable'),('J-F31','Freshness != Consistency'),
 ('J-F34','DisruptionBoundary'),('J-F35','SemanticallyPersistentState'),('J-F37','RecoverableSemanticState'),
 ('J-F38','Recoverability'),('J-F39','MaterializedStateAlreadyFlushed'),('J-F41','LiveComputationState'),
 ('J-F42','RuntimeProcessIdentity'),('J-F43','CompleteContinuationState'),('J-F44','RestartCheckpoint'),
 ('J-F45','Log != Checkpoint'),('J-F47','Recovery != Rollback'),('J-F49','DatabaseRecovery'),
 ('J-F50','GlobalVisibility'),('J-F51','DurableCommit'),('J-F52','LogicalCommit'),('J-F53','GloballyMemoryless'),
 ('J-F55','CurrentContext'),('J-F56','ProviderSessionIdentity'),('J-F57','ActiveComputationalMemoryState')]:
    check(pid.lower().replace('-','_'), any(x['id']==pid and token in x['result'] for x in d['probes']))
check('many-deleted-primitives', len(d['deletedUniversalPrimitives'])>=19)
for x in ['State','Memory','Storage','History','Cache','Address','Snapshot','Checkpoint','Persistence','Durability','Visibility','Consistency','SequentialConsistency','Coherence','Recovery','Rollback']:
    check('deleted-'+x.lower(), x in d['deletedUniversalPrimitives'])
check('survivor-name', d['survivor']['name']=='ComputationalStateRetentionAndReconstructionResponsibility')
check('survivor-cross-cutting', d['survivor']['classification'].startswith('STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE'))
check('refines-a', 'REFINES_A_CONTINUATION' in d['survivor']['classification'])
check('references-c', 'REFERENCES_C_STATE_SEMANTICS' in d['survivor']['classification'])
check('delegates-g', 'DELEGATES_SHARED_VISIBILITY_TO_G' in d['survivor']['classification'])
check('delegates-h', 'DELEGATES_PHYSICAL_RETENTION_TO_H' in d['survivor']['classification'])
check('delegates-b', 'DELEGATES_RESOURCE_COST_TO_B' in d['survivor']['classification'])
check('not-clean-sibling', 'NOT_CLEAN_INDEPENDENT_SIBLING' in d['survivor']['classification'])
check('not-cdf0', 'NOT_CDF0' in d['survivor']['classification'])
check('twelve-burdens', len(d['survivor']['burden'])==12)
for b in ['AbstractStateModelReference','StateScopeOrComputationalBoundary','StateSufficiencyOrHiddenDependencyAssumptions','RetentionLifetimeOrDisruptionBoundary','CaptureSnapshotOrCheckpointRelation','ExternalDependencyCompletenessRelation','ReconstructionReplayOrRecoveryRelation','RetentionCurrentnessAuthorityOrVersionRelation','FidelityLossOrOmissionRelation','PhysicalRealizationOrDurabilityReference','ResourceReference','ContinuityConsequence']:
    check('burden-'+b.lower(), b in d['survivor']['burden'])
check('round-a-coupled', d['roundARelation']['status']=='DEEPLY_COUPLED_LIKELY_SHARED_ARCHITECTURE')
check('continuation-retention-separated', d['roundARelation']['law']=='Continuation != StateRetentionByIdentity')
check('round-b-separated', d['roundBRelation']['status']=='CLEANLY_SEPARATED_REFERENCE_ONLY')
check('memory-resource-separated', d['roundBRelation']['law']=='MemorySpaceResource != SemanticMemoryState')
check('round-c-state-identity', d['roundCRelation']['status']=='STATE_IDENTITY_PRIMARILY_C')
check('round-g-reduction', d['roundGRelation']['status']=='OWNERSHIP_REDUCTION')
check('round-h-linked', d['roundHRelation']['status']=='TIGHTLY_LINKED_NOT_ABSORBED')
check('physical-retention-separated', d['roundHRelation']['law']=='PhysicalRetention != ComputationalPersistenceByIdentity')
check('round-i-distinct', d['roundIRelation']['status']=='DISTINCT')
check('ordinary-retention-not-oracle', d['roundIRelation']['law']=='OrdinaryStateRetention != OracleOrAdvicePowerByIdentity')
for owner in ['Runtime','Network','WorldHardware','Human','Harness','Security']:
    check('owner-'+owner.lower(), owner in d['ownerSubtraction'])
check('six-external-pressure', len(d['externalPressure'])>=6)
for token in ['Lamport','Adve-Gharachorloo','Atkinson-Morrison','System R','Condor/HTCondor','Wisconsin']:
    check('pressure-'+token.lower().replace('/','-').replace(' ','-'), any(token in x for x in d['externalPressure']))
for key in ['stateUniversalPrimitive','memoryUniversalEssence','storageEqualsState','persistenceEqualsNonvolatileStorage','consistencyOneBoolean','checkpointEqualsIdentity','durabilityEqualsVisibility']:
    check('rejected-'+key, d['verdict'][key]=='REJECTED')
check('memory-consistency-moved-g', d['verdict']['memoryConsistencyOwnedByJ']=='REJECTED_MOVED_TO_G')
check('high-consolidating', d['verdict']['informationGain']=='HIGH_CONSOLIDATING')
check('candidate-survives', d['verdict']['candidateSurvives'] is True)
check('candidate-not-clean-sibling', d['verdict']['candidateCleanIndependentSibling'] is False)
check('local-consolidation', d['verdict']['localConsolidationSignal'] is True)
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
failed=[x for x in checks if not x[1]]
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
