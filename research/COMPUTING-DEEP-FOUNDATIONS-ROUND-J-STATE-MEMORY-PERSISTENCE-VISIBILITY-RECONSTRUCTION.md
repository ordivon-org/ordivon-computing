---
schema_version: 1
id: computing.research.deep-foundations.round-j.state-memory-persistence-visibility-reconstruction
title: Ordivon Computing Deep Foundations — Round J: State / Memory / Persistence / Visibility / Reconstruction
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Destructive tournament over state, memory, storage, persistence, visibility, cache coherence, memory consistency, checkpoint/restart, recovery and identity. The pass rejects State, Memory, Storage, Persistence, Cache, Address, Checkpoint, Snapshot, Durability and Consistency as universal primitives. Lamport sequential-consistency pressure, Adve/Gharachorloo memory-model work, orthogonal-persistence research, System R recovery, and checkpoint/restart systems establish that abstract state is not physical storage; state is not memory by identity; internal memory is not necessary for every computation; history is not current state; state sufficiency is model/boundary-relative; address is not object identity; cache coherence is not memory consistency; durability is not visibility; checkpoint is not process identity; persistence is survival/reconstruction across a declared boundary rather than mere long duration or nonvolatility. Most apparent memory foundations reduce into C semantic state/representation, G shared visibility/order, H physical realization, B space/storage resource, and A continuation. A residual cross-cutting candidate survives: ComputationalStateRetentionAndReconstructionResponsibility. It governs model-relative state sufficiency, retention lifetime, capture/snapshot relation, reconstruction/recovery sufficiency, external dependency completeness, and continuity consequences. It is not a clean independent sibling and not CDF0.
evidence_status: strong-local-plus-primary-source-pressure
readiness: ROUND_J_COMPLETE_STRONG_CROSS_CUTTING_STATE_RETENTION_RECONSTRUCTION_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round J

## State / Memory / Persistence / Visibility / Reconstruction

## 0. Admission discipline

Round J is not `CDF0`.

This round attacks a vocabulary cluster that traditional software systems often compress into one intuitive noun:

```text
state
memory
storage
history
cache
address
snapshot
checkpoint
persistence
durability
visibility
consistency
recovery
identity
```

The objective is to determine whether `State/Memory` is an independent foundation axis or a composite of earlier responsibilities.

Current pressure comes from:

```text
A — continuation / interaction / process behavior
B — space / memory / I/O resource
C — representation / semantic interpretation / equivalence
G — shared-state history / visibility / ordering / consistency
H — abstract computation ↔ physical realization
I — model-relative effective power
```

---

# 1. Internal coverage is partial rather than foundational

Current Computing knowledge has a compact `state-computation-and-memory` treatment and repeatedly uses state in PAL/Agent-era work, but it does not reconstruct:

```text
state vs memory
state vs history
abstract state vs physical storage
persistence vs durability
checkpoint vs identity
cache coherence vs memory consistency
address/reference vs object identity
retention vs visibility
recovery vs continuation
```

Round J is therefore a genuine destructive reconstruction rather than repetition.

---

# 2. `State` is not `Memory`

## J-F1 — stateless combinational computation

A pure combinational circuit/function evaluator can map current input to output without retaining semantically relevant information from prior invocations.

Therefore:

```text
InternalMemory
!= necessary condition for every Computation.
```

## J-F2 — machine configuration without user-visible storage

An abstract machine state can include control location/current configuration even when there is no persistent user-addressable memory.

Therefore:

```text
ComputationalState
!= UserAddressableMemoryByIdentity.
```

## J-F3 — memory as retained past influence

A useful scoped notion of computational memory is that some information from earlier computational history can influence later behavior across a declared boundary.

Therefore:

```text
MemoryRole
= retained influence / recoverable information relation
not one storage device class.
```

---

# 3. State is model-relative, not a bag of bytes

## J-F4 — same bytes, different interpretation

The same bit pattern under different schema/type/control-state interpretations can denote different abstract computational states.

Therefore:

```text
SameStoredBytes
!= SameSemanticStateByIdentity.
```

## J-F5 — different representations, same abstract state

Two representations can encode the same abstract value/configuration.

Therefore:

```text
DifferentStoredRepresentation
!= DifferentSemanticStateByNecessity.
```

## J-F6 — address-space relocation

A process/object graph can be relocated while preserving the abstract state under a representation/relocation relation.

Therefore:

```text
SameSemanticState
!= SamePhysicalOrVirtualAddressesByNecessity.
```

C remains primary for representation/equivalence semantics.

---

# 4. State is not history

## J-F7 — multiple histories converge to same state

Different action/event histories can reach the same current abstract configuration.

Therefore:

```text
SameCurrentState
!= SameHistoryByIdentity.
```

## J-F8 — history may matter under a richer model

If future behavior depends on hidden prior events not represented in the proposed current state, then that proposed state abstraction is insufficient.

Therefore:

```text
ApparentSameState
!= FutureBehavioralEquivalence
when hidden relevant history remains.
```

## J-F9 — state sufficiency is model-relative

A state abstraction is sufficient only relative to the future queries/inputs/observations and environment assumptions for which it preserves relevant continuation behavior.

Therefore:

```text
StateSufficiency
without boundary/model/observation semantics
= underspecified.
```

This links J tightly to A/C.

---

# 5. State can be a quotient of history without being history itself

## J-F10 — future-equivalent histories

If two histories yield indistinguishable future behavior under all admitted future interactions, they can be represented by the same abstract state for that model.

Therefore:

```text
State
can summarize / quotient relevant history
without storing full history.
```

## J-F11 — event log can reconstruct state

An event-sourced representation may retain history and derive current state by replay/folding.

Therefore:

```text
HistoryRepresentation
!= StateRepresentationByIdentity.
```

## J-F12 — snapshot can discard causal/history detail

A snapshot may preserve current continuation-relevant state while losing the sequence that produced it.

Therefore:

```text
SnapshotState
!= HistoricalRecordByIdentity.
```

---

# 6. Memory resource and semantic state are different axes

## J-F13 — same abstract state, different footprint

Two encodings/implementations of the same state can consume different bytes/pages/cache lines.

Therefore:

```text
SemanticStateIdentity
!= MemoryFootprintIdentity.
```

## J-F14 — more allocated memory does not mean more relevant state

Unused buffers, duplicated caches, fragmentation and redundant encoding can increase memory usage without increasing semantic state.

Therefore:

```text
MemoryCapacityOrUsage
!= AmountOfSemanticStateByIdentity.
```

## J-F15 — compressed state

A smaller representation can preserve the same abstract state under a decoder.

Therefore:

```text
LessStorage
!= LessComputationalStateByNecessity.
```

Round B owns storage/space cost; C/J own semantic/retention relations.

---

# 7. Physical storage is not abstract memory

## J-F16 — one abstract memory, many substrates

Registers, SRAM, DRAM, flash, disk, magnetic/optical media and other substrates can realize retained computational information with different persistence/resource properties.

Therefore:

```text
AbstractMemoryRole
!= PhysicalStorageMediumByIdentity.
```

## J-F17 — physical medium contains bits but may not realize current computation state

A disk block containing stale, orphaned or uninterpretable bytes is not automatically current abstract state.

Therefore:

```text
StoredPhysicalBits
!= CurrentComputationalStateByIdentity.
```

H owns physical realization; J owns retention/reconstruction semantics.

---

# 8. Address is not identity

## J-F18 — virtual-memory relocation

A logical object/value can move to another physical frame while preserving its program-visible identity.

Therefore:

```text
PhysicalAddress
!= ObjectIdentityByIdentity.
```

## J-F19 — address reuse

The same virtual/physical address can hold different objects at different times.

Therefore:

```text
SameAddressAcrossTime
!= SameObjectIdentity.
```

## J-F20 — copying

Two distinct addresses may hold equal values but remain distinct mutable locations/objects.

Therefore:

```text
ValueEquality
!= LocationOrObjectIdentity.
```

## J-F21 — persistent reference needs a stable naming/binding relation

A raw transient address generally does not by itself provide identity across restart/relocation/persistence boundaries.

Therefore:

```text
PointerOrAddress
!= StablePersistentReferenceByIdentity.
```

---

# 9. Cache is not authoritative state

## J-F22 — derived copy

A cache can hold a derived copy of data whose authority/currentness is governed elsewhere.

Therefore:

```text
CachedCopy
!= AuthoritativeStateByIdentity.
```

## J-F23 — authoritative state need not be one physical copy

Replicated/encoded state can have no single unique physical copy that alone constitutes authority.

Therefore:

```text
AuthoritativeLogicalState
!= OneAuthoritativePhysicalCopyByNecessity.
```

## J-F24 — cache hit is not visibility theorem

Reading a local cached value does not by itself establish what writes another participant is required/permitted to observe under the memory model.

Therefore:

```text
CacheHit
!= MemoryVisibilityGuaranteeByIdentity.
```

---

# 10. Cache coherence is not memory consistency

Lamport's 1979 sequential-consistency pressure arose precisely because per-processor caching and reordering can break naive assumptions about one shared memory. Adve/Gharachorloo later systematize multiple shared-memory consistency models.

## J-F25 — per-location coherence can coexist with cross-location ordering differences

Maintaining an agreed order of writes to each individual location does not by itself determine the complete ordering/visibility constraints across multiple locations and processors.

Therefore:

```text
CacheCoherence
!= MemoryConsistencyByIdentity.
```

## J-F26 — coherence mechanism is not consistency contract

Different mechanisms can implement the same memory model, and one coherence protocol can be embedded within systems exposing different higher-level consistency rules.

Therefore:

```text
CoherenceMechanism
!= MemoryModelSemanticsByIdentity.
```

## J-F27 — sequential consistency is one model

Lamport's sequential consistency requires behavior equivalent to some total order of operations consistent with each processor's program order.

Therefore:

```text
SequentialConsistency
!= MemoryConsistencyInGeneral.
```

This confirms memory-model semantics reduce primarily into G/C.

---

# 11. Sequential consistency is not linearizability

## J-F28 — real-time constraint difference

Sequential consistency preserves each participant's program order but does not impose the same external real-time precedence requirement as linearizability for nonoverlapping operations.

Therefore:

```text
SequentialConsistency
!= LinearizabilityByIdentity.
```

This is another reason `Consistent:Boolean` is not admissible.

---

# 12. Visibility is not retention

## J-F29 — durable but not currently visible

A committed log record can be durably stored while ordinary readers have not yet reconstructed/observed the corresponding logical state through their interface.

Therefore:

```text
Durable
!= CurrentlyVisibleByIdentity.
```

## J-F30 — visible but volatile

A value can be visible to all current participants in RAM yet disappear after power loss/crash.

Therefore:

```text
Visible
!= DurableByIdentity.
```

## J-F31 — stale but model-valid read

Under a weaker consistency contract, a read can legitimately observe older state while that state is still retained.

Therefore:

```text
Freshness
!= ConsistencyByIdentity.
```

and:

```text
Retention
!= VisibilityOrder.
```

G owns visibility/order; J owns retention/reconstruction.

---

# 13. Persistence is not duration or immutability

Orthogonal-persistence research explicitly treats longevity as separable from type/other object attributes.

## J-F32 — mutable persistent object

An object can survive program executions/restarts and still be mutable.

Therefore:

```text
Persistent
!= ImmutableByIdentity.
```

## J-F33 — long-lived volatile state

A value can remain in a running machine for months yet vanish on process/power failure.

Therefore:

```text
LongLived
!= PersistentAcrossFailureBoundaryByIdentity.
```

## J-F34 — persistence boundary is contractual

Persistence may mean survival across:

```text
function call
process restart
machine reboot
power failure
software upgrade
migration
```

These are different claims.

Therefore:

```text
Persistent
without declared lifetime/disruption boundary
= underspecified.
```

---

# 14. Persistence is not `stored on disk`

## J-F35 — disk write can be nonauthoritative/incomplete

A file/block can exist on disk without being a committed/current/recoverable representation of application state.

Therefore:

```text
OnPersistentMedium
!= SemanticallyPersistentStateByIdentity.
```

## J-F36 — persistence can be realized without exposing a file abstraction

Persistent object systems can hide storage tier distinctions from programming semantics.

Therefore:

```text
Persistence
!= FileStorageByIdentity.
```

## J-F37 — physical nonvolatility does not provide schema/identity/currentness

Bits surviving power loss do not tell us which object/version/schema they belong to.

Therefore:

```text
NonvolatileBits
!= RecoverableSemanticStateByIdentity.
```

H/J/C must compose.

---

# 15. Durability is not recoverability

System R recovery work demonstrates that durable logs, checkpoints, undo/redo information and recovery procedures jointly reconstruct a valid database state after faults.

## J-F38 — durable bytes with missing reconstruction semantics

A durable log/blob that cannot be correctly interpreted/replayed is not sufficient recovery state.

Therefore:

```text
DurableEvidence
!= RecoverabilityByIdentity.
```

## J-F39 — data page persistence can lag logical commit

A transaction can become recoverably committed through logging even if all data pages have not yet reached their final persistent locations, provided the recovery protocol can redo as needed.

Therefore:

```text
LogicalDurability
!= AllMaterializedStateAlreadyFlushedByIdentity.
```

## J-F40 — recoverability depends on protocol/currentness

Recovery needs enough metadata/order/checkpoint/log semantics to determine what to redo/undo/retain.

Therefore:

```text
Recovery
!= MereByteSurvival.
```

---

# 16. Checkpoint is not state identity

Checkpoint/restart systems such as Condor explicitly create a saved representation from which a new process is manipulated to emulate the old process's continuation.

## J-F41 — checkpoint artifact vs live state

A checkpoint is a captured representation of selected computational state at some boundary.

Therefore:

```text
CheckpointArtifact
!= LiveComputationStateByIdentity.
```

## J-F42 — restored process is not numerically the same OS process

A restart may create a new process and reconstruct enough state that user-level execution continues equivalently.

Therefore:

```text
ContinuationEquivalence
!= RuntimeProcessIdentityByNecessity.
```

## J-F43 — checkpoint completeness is environment-relative

Open files, remote services, sockets, devices, external clocks and shared state may lie outside a local process checkpoint.

Therefore:

```text
CapturedLocalState
!= CompleteContinuationStateByIdentity.
```

unless external dependencies/assumptions are accounted for.

---

# 17. Snapshot is not checkpoint and neither is log

## J-F44 — snapshot vs restartable checkpoint

A logical read snapshot can provide a consistent view for observation without containing enough runtime control/resource state to restart computation.

Therefore:

```text
Snapshot
!= RestartCheckpointByIdentity.
```

## J-F45 — event log vs checkpoint

A log may encode changes/history that reconstruct state only after replay, while a checkpoint may encode a direct state image.

Therefore:

```text
Log
!= CheckpointByIdentity.
```

## J-F46 — either can be sufficient under a protocol

A combination of checkpoint + suffix log, or full replayable history, can reconstruct current logical state.

Therefore:

```text
OneUniversalPersistenceRepresentation
= REJECTED.
```

---

# 18. Recovery is not rollback

## J-F47 — redo without rollback

After a crash, committed effects missing from materialized pages may need redo.

## J-F48 — undo of uncommitted effects

Other effects may need undo.

Therefore:

```text
Recovery
!= RollbackByIdentity.
```

and:

```text
RecoveryDirection
can include redo + undo + reconstruction.
```

## J-F49 — checkpoint restart can resume rather than revert application semantics

A process checkpoint may restore continuation from an earlier captured state, but transaction recovery may reconstruct a later committed state from checkpoint + log.

Therefore:

```text
CheckpointRestart
!= DatabaseRecoveryByIdentity.
```

---

# 19. `Write complete` is level-relative

## J-F50 — CPU store completion vs global visibility

A store may leave an instruction pipeline/store buffer before becoming observable by every participant under the memory model.

Therefore:

```text
LocalStoreCompletion
!= GlobalVisibilityByIdentity.
```

## J-F51 — global visibility vs persistence

A write can be globally visible in volatile memory before becoming recoverably durable.

Therefore:

```text
GlobalVisibility
!= DurableCommitByIdentity.
```

## J-F52 — persistent-medium arrival vs logical commit

A low-level block write reaching nonvolatile media does not necessarily establish application-level transaction commit.

Therefore:

```text
PhysicalWritePersistence
!= LogicalCommitByIdentity.
```

No single universal `written=true` survives.

---

# 20. State boundary can move

## J-F53 — stateless service with external database

A service process can retain no local session state while future behavior still depends on externally stored state.

Therefore:

```text
LocallyStateless
!= GloballyMemorylessComputationByIdentity.
```

## J-F54 — environment as memory carrier

An interactive computation can externalize state to environment/client and later receive it back.

Therefore:

```text
InternalMemoryAbsence
!= NoCrossInteractionMemoryEffectByIdentity.
```

State/memory ownership is boundary-relative, reinforcing A.

---

# 21. Agent-era `memory` decomposes immediately

## J-F55 — context window vs durable history

Current model context can be reconstructed from durable run history, retrieval indexes or summaries.

Therefore:

```text
CurrentContext
!= DurableMemoryByIdentity.
```

## J-F56 — provider session vs computational state

A provider/session can disappear while higher-level Agent task state survives in other stores and is reconstructed.

Therefore:

```text
ProviderSessionIdentity
!= ComputationalStateIdentity.
```

## J-F57 — stored conversation/history vs remembered semantic facts

A raw transcript can persist while the currently reconstructed WorkingSet/summary omits parts; conversely a compact summary can preserve selected continuation-relevant information without retaining full transcript.

Therefore:

```text
StoredHistory
!= ActiveComputationalMemoryStateByIdentity.
```

No Agent-specific memory primitive is required.

---

# 22. Owner subtraction

## Round C / semantics

C owns:

```text
state representation
state interpretation
semantic equality/equivalence
schema/type meaning
```

J must not duplicate generic semantic representation.

## Round G / coordination

G owns shared-state:

```text
visibility
ordering
memory/consistency contracts
concurrent history
synchronization
```

J references those when retained state is shared.

## Round H / physical realization

H owns physical medium/device realization and physical retention truth.

J owns the abstract lifetime/reconstruction contract once the physical realization is admitted.

## Round B / resources

B owns:

```text
space
memory footprint
cache/storage hierarchy cost
I/O cost
```

J does not equate memory resource with semantic memory.

## Round A / continuation

A owns generic continuation/termination/environment boundary.

J specifies what state must be retained/reconstructed for a continuation claim to survive a disruption/lifetime boundary.

## Runtime

Runtime owns actual process/job/checkpoint/restart/file/session facts.

J owns generic state-capture/reconstruction semantics rather than concrete lifecycle truth.

---

# 23. Round A relation — deeply coupled

A already contains continuation semantics.

J adds the question:

```text
what state information must survive or be reconstructed
so that continuation under A's behavioral contract remains valid?
```

Therefore:

```text
Continuation
!= StateRetentionByIdentity
```

but J is a major dependency of stateful continuation/restart.

Current classification:

```text
A and J likely belong to the same broader behavior/continuation architecture,
not clean sibling foundations.
```

---

# 24. Round B relation — clean separation

```text
MemorySpaceResource
!= SemanticMemoryState.
```

B asks:

```text
how much storage/state space/I/O is consumed?
```

J asks:

```text
what information must be retained/reconstructed across the declared boundary?
```

Compression/duplication/caches make the separation decisive.

---

# 25. Round C relation — state identity belongs primarily to semantics

C owns state representation and semantic equivalence.

J cannot define `same state` independently of C.

Therefore J's state field should reference C rather than duplicate it.

However C does not itself express:

```text
survival across disruption
capture completeness
reconstruction sufficiency
retention lifetime
```

so a cross-cutting J burden survives.

---

# 26. Round G relation — visibility/memory consistency mostly reduces into G

Memory consistency is fundamentally a shared-observation/order contract.

Therefore:

```text
MemoryConsistency
→ G CoordinationConsistencyOrSafetySpecification / HistoryEventAndOrderStructure
```

with C supplying values/operation semantics.

This is an ownership correction:

```text
J does NOT own generic memory consistency.
```

J only references G when retained state is concurrently/shared observed.

---

# 27. Round H relation — persistence needs realization, but is not realization

H can establish:

```text
physical medium/device preserves encoded distinctions under condition X.
```

J still must establish:

```text
those preserved distinctions are sufficient/current/complete
for reconstructing the required computational state after boundary Y.
```

Therefore:

```text
PhysicalRetention
!= ComputationalPersistenceByIdentity.
```

H and J remain distinct but tightly linked.

---

# 28. Round I relation

Ordinary retained state does not automatically change effective computability power: a Turing machine already has unbounded abstract tape within the standard model.

But auxiliary nonuniform advice/oracle state can change the admitted model power.

Therefore:

```text
OrdinaryStateRetention
!= OracleOrAdvicePowerByIdentity.
```

If retained information is treated as nonuniform/advice/oracle capability, I must declare it explicitly.

---

# 29. Strong residual candidate — Computational State Retention and Reconstruction Responsibility

After subtraction, the survivor is:

```text
ComputationalStateRetentionAndReconstructionResponsibility
```

Minimum current burden:

## 29.1 Abstract state model reference

```text
which C-defined abstract state/configuration is meant?
```

## 29.2 State scope / computational boundary

```text
local process?
composite system?
external service/database included?
```

References A.

## 29.3 State sufficiency / hidden-dependency assumptions

```text
is the declared state sufficient to preserve future behavior under admitted interactions/environment?
```

## 29.4 Retention/lifetime/disruption boundary

```text
what must state survive?
call / turn / process restart / crash / reboot / migration / upgrade / other declared boundary
```

## 29.5 Capture / snapshot / checkpoint relation

```text
what representation is captured and at what logical point?
```

## 29.6 External-dependency completeness relation

```text
which external resources/state are included, rebound, assumed unchanged or explicitly excluded?
```

## 29.7 Reconstruction / replay / recovery relation

```text
how does captured/history/logged information reconstruct a continuation-valid abstract state?
```

## 29.8 Retention currentness / authority / version relation

```text
which retained version is current/committed/admissible?
```

References C/G where appropriate.

## 29.9 Fidelity / loss / omission relation

```text
exact state preservation?
lossy summary?
approximate state?
what future behavioral consequences are admitted?
```

References D when approximate.

## 29.10 Physical realization / durability reference

Links to H for actual storage/nonvolatility/failure assumptions.

## 29.11 Resource reference

Links to B for footprint/I/O/replay/checkpoint cost.

## 29.12 Continuity consequence

```text
does successful reconstruction preserve the A-level computation/task/process behavior contract,
without requiring same Runtime process identity?
```

---

# 30. Why J is not a clean sibling

The residual is real, but most of J's apparent domain is already owned elsewhere:

```text
state meaning / identity      → C
shared visibility/order       → G
physical medium               → H
memory/storage cost           → B
continuation boundary         → A
```

What remains is a cross-cutting relation connecting those pieces over time/disruption:

```text
retain / capture / reconstruct enough abstract state
for continuation-valid behavior.
```

Therefore current classification:

```text
STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE
REFINES_A_CONTINUATION
REFERENCES_C_STATE_SEMANTICS
DELEGATES_SHARED_VISIBILITY_TO_G
DELEGATES_PHYSICAL_RETENTION_TO_H
DELEGATES_RESOURCE_COST_TO_B
NOT_CLEAN_INDEPENDENT_SIBLING
NOT_CDF0
NOT_ROUTE_SELECTED
```

This is an important negative result: `State/Memory` does not automatically deserve its own numbered foundation despite its ubiquity.

---

# 31. Candidate deletion results

Rejected as universal primitives:

```text
State
Memory
Storage
History
Cache
Address
Pointer
Snapshot
Checkpoint
Persistence
Durability
Visibility
Consistency
SequentialConsistency
Coherence
Recovery
Rollback
File
NonvolatileMemory
```

All remain scoped concepts under explicit semantic/physical/lifetime/coordination roles.

---

# 32. Anti-collapse laws

```text
InternalMemory != necessary for every Computation
ComputationalState != UserAddressableMemory
SameBytes != SameSemanticState
DifferentRepresentation != DifferentStateByNecessity
SameState != SameAddresses
SameCurrentState != SameHistory
StateSufficiencyWithoutModel = underspecified
HistoryRepresentation != StateRepresentation
SnapshotState != HistoricalRecord
SemanticState != MemoryFootprint
MemoryUsage != AmountOfSemanticState
AbstractMemory != PhysicalStorageMedium
StoredBits != CurrentComputationalState
PhysicalAddress != ObjectIdentity
SameAddressAcrossTime != SameObject
ValueEquality != ObjectIdentity
Address != StablePersistentReference
CachedCopy != AuthoritativeState
AuthoritativeLogicalState != OnePhysicalCopy
CacheHit != MemoryVisibilityGuarantee
CacheCoherence != MemoryConsistency
CoherenceMechanism != MemoryModelSemantics
SequentialConsistency != MemoryConsistencyInGeneral
SequentialConsistency != Linearizability
Durable != Visible
Visible != Durable
Freshness != Consistency
Retention != VisibilityOrder
Persistent != Immutable
LongLived != PersistentAcrossFailureBoundary
PersistenceWithoutBoundary = underspecified
PersistentMedium != SemanticallyPersistentState
Persistence != FileStorage
NonvolatileBits != RecoverableSemanticState
DurableEvidence != Recoverability
LogicalDurability != AllStateFlushed
Recovery != ByteSurvival
CheckpointArtifact != LiveState
ContinuationEquivalence != RuntimeProcessIdentity
CapturedLocalState != CompleteContinuationState
Snapshot != RestartCheckpoint
Log != Checkpoint
Recovery != Rollback
CheckpointRestart != DatabaseRecovery
LocalStoreCompletion != GlobalVisibility
GlobalVisibility != DurableCommit
PhysicalWritePersistence != LogicalCommit
LocallyStateless != GloballyMemoryless
InternalMemoryAbsence != NoCrossInteractionMemoryEffect
CurrentContext != DurableMemory
ProviderSessionIdentity != ComputationalStateIdentity
StoredHistory != ActiveMemoryState
MemorySpaceResource != SemanticMemoryState
PhysicalRetention != ComputationalPersistence
OrdinaryStateRetention != OracleOrAdvicePower
```

---

# 33. Rival-model update

## M1 Function evaluation

Stateless function evaluation remains a valid regime; memory cannot define all computation.

## M2 Controlled state transition

Substantially strengthened, but with a warning:

```text
state
```

must be a declared model-relative sufficient configuration, not arbitrary physical state or stored bytes.

M2 therefore survives as an abstract description pattern but still does not by itself solve boundary/semantics/realization.

## M3 Information transformation

Retention is information-related, but `information stored` does not identify semantic state, persistence boundary or authority. M3 remains insufficient as universal ontology.

## M4 Effective procedure

I remains primary; memory/state affects solver model but does not replace effective-solvability semantics.

## M5 Resource-bounded process

B remains separate because storage footprint/cost differs from semantic retained state.

## M6 Interactive process

State/memory is common in interaction but not required for every interactive mapping and can be externalized across the boundary.

## M7 Physical realization

H remains primary for physical storage. J supplies persistence/reconstruction consequence above physical retention.

---

# 34. Current A/B/C/D/F/G/H/I/J factorization

```text
                         I
            Effective Solvability / Power
                 /       |       \
                G        B        H
      coordination   resources   physical realization
            │            │         │
            │            │         │
            └──────┬─────┴────┬────┘
                   ▼          ▼
                   C          J
             semantics     retention /
             state model   reconstruction
                   ▲          │
                   │          │
                   └──── A ◄──┘
                    behavior /
                    continuation

D approximation and F probability cross-cut contracts where needed.
```

J is a temporal/continuity bridge, not a new isolated field node.

---

# 35. Information gain

Round J information gain is **HIGH / CONSOLIDATING**.

Unlike H/I, it does not uncover another clean independent sibling. Its value is architectural consolidation:

```text
- rejects ubiquitous noun `Memory` as one foundation
- moves memory consistency decisively into G
- moves state identity into C
- moves physical storage into H
- moves memory cost into B
- preserves a narrower retention/reconstruction cross-cutting burden
```

This is the first meaningful sign that some newly tested continents are starting to **factor into the existing architecture rather than expanding the sibling count**.

That is not yet whole-domain diminishing returns, but it is a local consolidation signal.

---

# 36. Next frontier — deliberately unselected

The largest remaining pressure continent is now plausibly:

```text
Information / Coding / Compression / Algorithmic Information
```

because M3 `Information Transformation` has remained unresolved through every round, while B contains communication/storage/sample resources, C contains representation/semantics, H contains physical realization and J now separates retained semantic state from stored bits.

A direct information round can test whether:

```text
entropy
mutual information
coding
compression
Kolmogorov complexity
algorithmic randomness
channel capacity
sufficient information
```

supply an independent Computing burden or reduce into mathematics + Media/Network + B/C/H/J.

Other still-open continents include:

```text
online / streaming / advice / competitive computation
real-time / cyber-physical computation
biological / neuromorphic computation
algorithm/data-structure/lower-bound structure beyond generic B
```

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 37. Primary/direct research pressure anchors

Used as pressure sources, not ontology authority:

- Leslie Lamport, *How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs*, IEEE Transactions on Computers, 1979 — sequential-consistency pressure.
- Sarita V. Adve and Kourosh Gharachorloo, *Shared Memory Consistency Models: A Tutorial*, IEEE Computer, 1996, plus the earlier technical-report research line.
- M. P. Atkinson and R. Morrison, orthogonal/persistent programming work, especially *An Approach to Persistent Programming* (1983) and *Orthogonally Persistent Object Systems* (1995).
- Jim Gray et al., *The Recovery Manager of the System R Database Manager*, ACM Computing Surveys, 1981 — logging/checkpoint/undo/redo/recovery pressure.
- Condor/HTCondor checkpoint/restart research and documentation — reconstruction of process state in a newly created process rather than runtime-process identity.
- Wisconsin shared-memory/cache-coherence research is used as additional pressure for coherence mechanism vs memory-model semantics.
