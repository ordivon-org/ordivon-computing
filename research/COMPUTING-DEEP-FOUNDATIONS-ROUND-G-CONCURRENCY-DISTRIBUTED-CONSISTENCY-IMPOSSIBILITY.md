---
schema_version: 1
id: computing.research.deep-foundations.round-g.concurrency-distributed-consistency-impossibility
title: Ordivon Computing Deep Foundations — Round G: Concurrency / Distributed Coordination / Consistency / Impossibility
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Destructive tournament over concurrent and distributed computation. The pass attacks Concurrency, Parallelism, Atomicity, Consistency, Consensus, GlobalOrder, Synchrony, Failure and Availability as universal primitives. Pressure from Lamport event ordering, Herlihy-Wing linearizability, FLP asynchronous consensus impossibility, Dwork-Lynch-Stockmeyer partial synchrony, Herlihy wait-free synchronization and Gilbert-Lynch CAP shows that concurrent correctness is a relation over histories/orders rather than final state; causal order is partial rather than a universal total order; safety and progress are distinct; solvability is relative to timing, communication/shared-state, failure, scheduler/fairness and primitive assumptions; and impossibility claims are model-scoped rather than absolute. Network owns actual transport/reachability, Runtime owns actual thread/process/job execution, while Computing retains abstract coordination-task, history-consistency, progress and solvability claims. A strong partially orthogonal candidate survives: ComputationalCoordinationConsistencyAndProgressResponsibility. It overlaps A/B/C/F but leaves an irreducible multi-actor coordination/solvability burden. It is not CDF0 and no route is selected.
evidence_status: strong-local
readiness: ROUND_G_COMPLETE_STRONG_PARTIALLY_ORTHOGONAL_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round G

## Concurrency / Distributed Coordination / Consistency / Impossibility

## 0. Admission discipline

Round G is not `CDF0`.

Current live structure before this pass:

```text
A — boundary / interaction / continuation / environment assumptions
B — resource / feasibility
C — interpretation / semantic comparison / refinement
D — approximation / error / validation
F — stochasticity / distribution / risk
```

Round G asks whether multi-actor concurrency/distribution contributes a genuinely new Computing burden after subtracting Network transport, Runtime execution, C semantic relations, B communication resources and F scheduler/adversary probability structure.

---

# 1. Current internal coverage remains thin

Current Computing Core/Knowledge has no dedicated reconstruction of:

```text
linearizability / consistency models
partial-order event semantics
consensus solvability/impossibility
synchrony assumptions
wait-free / lock-free progress
shared-memory synchronization power
CAP-style model-relative tradeoffs
```

The active atlas and earlier rounds mention these only as pressure cases.

Round G is therefore new whole-domain coverage rather than replay.

---

# 2. Concurrency is not parallelism

## G-F1 — concurrent interleaving on one processor

Two logical activities can be concurrent in the sense that their executions overlap/interleave in one computation even when only one physical instruction executes at a time.

Therefore:

```text
Concurrency
!= PhysicalParallelExecutionByIdentity.
```

## G-F2 — parallel independent work without coordination

Two independent numerical kernels may run physically in parallel while sharing no coordination protocol/state relation relevant to their correctness.

Therefore:

```text
Parallelism
!= CoordinationByIdentity.
```

Round B's work/depth theory and Round G's coordination semantics remain distinct.

---

# 3. Final state is not concurrent correctness

## G-F3 — same final state, different concurrent histories

Two histories can finish with the same object state while one violates the abstract operation ordering/specification and the other does not.

Therefore:

```text
SameFinalState
!= SameConcurrentCorrectnessByIdentity.
```

## G-F4 — same operation multiset, different order relation

Histories with identical calls/returns but different order constraints can have different validity.

Therefore:

```text
SameOperationMultiset
!= SameConcurrentHistorySemantics.
```

Concurrent correctness must preserve enough history/order structure.

---

# 4. Linearizability is one scoped correctness relation, not `Consistency` itself

Herlihy and Wing define linearizability for concurrent objects by requiring each operation to appear to take effect atomically at a point between invocation and response while respecting the object's sequential specification and real-time precedence of nonoverlapping operations.

## G-F5 — representation can be highly concurrent while abstract behavior is sequentially explainable

Therefore:

```text
ConcurrentImplementation
!= ConcurrentAbstractSpecificationByNecessity.
```

## G-F6 — linearizable history need not identify the actual physical instant of effect

Linearizability asks for an admissible abstract linearization witness/order, not a unique observable hardware instant.

Therefore:

```text
LinearizationPointAsProofWitness
!= PhysicalWorldInstantByIdentity.
```

## G-F7 — real-time precedence is semantic input

If operation A completes before B begins, a linearization cannot reverse them.

Therefore:

```text
InvocationResponseHistory
contains semantic order information beyond final state.
```

## G-F8 — linearizability is not universal consistency

Other applications may choose weaker/stronger/different consistency or transactional semantics.

Therefore:

```text
Linearizability
!= ConsistencyByIdentity.
```

No `Consistent:Boolean` survives without a named model/specification.

---

# 5. Linearizability and serializability are not identical notions

## G-F9 — concurrent object vs transaction abstraction

Linearizability is a correctness condition over concurrent object operations respecting real-time order; serializability traditionally concerns equivalence of transactional executions to some serial transaction order and need not by itself impose the same external real-time constraint.

Therefore:

```text
Linearizability
!= SerializabilityByIdentity.
```

A stronger relation such as strict serializability can combine transaction serial order with real-time constraints, but this reinforces rather than erases the distinction.

---

# 6. Safety and liveness/progress are orthogonal

## G-F10 — safe system that never responds

A system can preserve an invariant forever by refusing to complete operations.

Therefore:

```text
Safety
!= ProgressByIdentity.
```

## G-F11 — responsive but unsafe system

A system can always return quickly while violating its consistency specification.

Therefore:

```text
AvailabilityOrTermination
!= SafetyCorrectnessByIdentity.
```

## G-F12 — termination of one operation vs system-wide progress

One completed operation does not establish a wait-free/lock-free/global progress theorem.

Therefore:

```text
ObservedCompletion
!= ProgressGuaranteeByIdentity.
```

---

# 7. Progress conditions are plural

Herlihy's wait-free synchronization line distinguishes progress/synchronization power of concurrent objects and shows that different shared object types can have different consensus power.

## G-F13 — wait-free and lock-free are not the same guarantee

A system can guarantee that some operation completes under continued execution without guaranteeing that every nonfaulty individual operation completes in bounded own steps.

Therefore:

```text
SystemWideProgress
!= PerOperationWaitFreedomByIdentity.
```

## G-F14 — blocking mutual exclusion can be safe but vulnerable to stalled owner

Therefore:

```text
MutualExclusionSafety
!= NonblockingProgress.
```

No universal `Progress:Boolean` survives.

---

# 8. Scheduler/fairness assumptions are semantic for liveness, not Runtime scheduler truth

## G-F15 — unfair schedule can starve an enabled process

An algorithm may have a liveness theorem only under fairness assumptions.

Therefore:

```text
AlgorithmText
!= LivenessGuaranteeWithoutSchedulerAssumptions.
```

## G-F16 — abstract scheduler is not OS scheduler identity

A proof-level scheduler/adversary represents an admitted class of execution choices; the actual Linux/Runtime scheduler is one physical realization/evidence source.

Therefore:

```text
AbstractScheduler
!= RuntimeSchedulerByIdentity.
```

## G-F17 — fairness affects liveness more directly than safety

The same safety invariant may hold under both fair and unfair schedules while progress changes.

Therefore:

```text
FairnessAssumption
!= SafetySpecificationByIdentity.
```

---

# 9. Distributed order is partial, not universally total

Lamport's happened-before relation orders events by local program order and message-send/receive causality and closes transitively.

## G-F18 — causally unrelated events can remain incomparable

Therefore:

```text
DistributedCausalOrder
!= UniversalTotalOrder.
```

## G-F19 — logical clocks preserve implication, not converse identity

Lamport clocks can be assigned so that if `a -> b`, then `C(a) < C(b)`; the converse does not make clock order identical to causality.

Therefore:

```text
LogicalClockOrder
!= CausalOrderByIdentity.
```

## G-F20 — total order extension can be useful without being causal truth

A system can impose a deterministic total order extending a partial order for serialization/coordination.

Therefore:

```text
ChosenTotalOrder
!= PreexistingWorldCausalOrderByIdentity.
```

Computing must preserve which order relation is asserted.

---

# 10. Global time is not required for all distributed correctness

## G-F21 — causal/order reasoning without synchronized physical clocks

Lamport's model shows meaningful distributed ordering can be defined without assuming a single synchronized real-time clock.

Therefore:

```text
GlobalPhysicalClock
!= necessary condition for DistributedComputationCorrectness.
```

## G-F22 — physical time may still be constitutive for stronger contracts

Real-time deadlines, leases or strict real-time order can make clock/timing bounds part of a specific contract.

Therefore:

```text
ClockIrrelevance
!= universal law either.
```

Timing model is query/specification-relative.

---

# 11. Consensus is a task with separable properties

## G-F23 — agreement, validity and termination are distinct

A consensus task typically separates at least:

```text
agreement
validity / decision admissibility
termination / decision progress
```

A protocol can preserve agreement/validity while failing to terminate on some admissible execution.

Therefore:

```text
ConsensusSafety
!= ConsensusTermination.
```

## G-F24 — consensus task is not one implementation primitive

Different protocols/models can solve or fail to solve the same abstract coordination task.

Therefore:

```text
ConsensusTask
!= ConsensusAlgorithmByIdentity.
```

---

# 12. FLP makes impossibility explicitly model-relative

Fischer, Lynch and Paterson show that in a completely asynchronous deterministic message-passing model, even one process that may fail by stopping is enough to prevent a protocol from guaranteeing consensus termination on all admissible executions.

## G-F25 — FLP does not mean `consensus is impossible`

It is scoped to its assumptions.

Therefore:

```text
ConsensusImpossible
without model/failure/progress qualifiers
= underspecified / false as a universal claim.
```

## G-F26 — impossibility targets guaranteed termination, not all safety

An execution can remain undecided while preserving agreement/validity.

Therefore:

```text
FLPImpossibility
!= ImpossibilityOfConsensusSafetyByIdentity.
```

## G-F27 — one crash possibility can change solvability

Therefore:

```text
FailureModel
can be constitutive of ComputationalPossibilityClaim.
```

This is a new strong pressure beyond mere performance metadata.

---

# 13. Partial synchrony shows that tiny assumption changes can restore solvability

Dwork, Lynch and Stockmeyer define partial-synchrony regimes between fully synchronous and asynchronous models and give fault-tolerant consensus protocols under such assumptions.

## G-F28 — asynchronous vs partially synchronous is not an implementation detail

Therefore:

```text
SynchronyAssumption
can change task solvability.
```

## G-F29 — known bounds vs eventually holding bounds are different models

Therefore:

```text
TimingBoundExists
!= TimingBoundKnownFromStart
!= TimingBoundEventuallyHolds.
```

## G-F30 — same protocol idea under changed model can receive a different proof obligation

Therefore:

```text
AlgorithmIdentity
!= SolvabilityClaimByIdentity.
```

The computational model is part of the theorem.

---

# 14. Failure is not one primitive

## G-F31 — crash vs Byzantine behavior

A crash-stop process ceases steps; a Byzantine process may emit arbitrary/malicious/inconsistent behavior.

Therefore:

```text
CrashFailure
!= ByzantineFailureByIdentity.
```

Security owns actual malicious compromise/authority truth; Computing may still quantify over an abstract Byzantine/adversarial failure model.

## G-F32 — process failure vs network partition

A reachable process isolated by communication failure is not identical to a crashed process.

Therefore:

```text
ProcessCrash
!= NetworkPartitionByIdentity.
```

Network owns actual reachability/partition truth.

## G-F33 — delay can be observationally indistinguishable from failure in pure asynchrony

A process waiting without timing bounds may not be able to determine whether a peer crashed or a message/process is merely slow.

Therefore:

```text
NonresponseObservation
!= GroundTruthCrashByIdentity.
```

This distinction is central to impossibility reasoning.

---

# 15. CAP-style tradeoffs are model-specific, not a slogan ontology

Gilbert and Lynch formalize a version of Brewer's conjecture: under their asynchronous network model with partitions, it is impossible to implement a read/write object providing both atomic consistency and availability under the stated definitions.

## G-F34 — consistency/availability/partition are scoped definitions

Therefore:

```text
CAP
!= UniversalChooseAnyTwoLawByIdentity.
```

## G-F35 — atomic consistency is not every consistency model

Therefore:

```text
CAPConsistency
!= ConsistencyInGeneral.
```

## G-F36 — actual partition belongs to Network; impossibility under partition model belongs to Computing theorem space

Therefore:

```text
NetworkPartitionTruth
!= CAPImpossibilityClaimByIdentity.
```

---

# 16. Shared-memory primitive choice can change synchronization power

Herlihy's wait-free synchronization work establishes a hierarchy in which different shared object types have different consensus numbers/synchronization power.

## G-F37 — shared register abstraction is not equivalent to arbitrary atomic object

Therefore:

```text
SharedMemoryExists
!= UniversalSynchronizationPower.
```

## G-F38 — stronger primitive can change solvability

A coordination task unsolvable wait-free with one primitive family may become solvable with another.

Therefore:

```text
AdmittedOperationPrimitiveFamily
can be constitutive of ComputationalSolvability.
```

This connects Round G directly to Round C's semantic model and Round B's admitted operations, but does not reduce to cost.

---

# 17. Communication model and shared-memory model are not Network-vs-Computing aliases

## G-F39 — abstract communication primitive vs physical transport

A proof may assume reliable FIFO channels, lossy channels, broadcast, atomic registers or message passing.

These are computational-model abstractions.

Network owns actual routes/links/latency/capacity/reachability.

Therefore:

```text
AbstractCommunicationModel
!= NetworkTopologyOrTransportByIdentity.
```

## G-F40 — communication reliability can be an assumption rather than measured fact

Therefore:

```text
ModelAssumption
!= RuntimeOrNetworkObservationByIdentity.
```

Observed evidence can validate/refute the assumption for one realization, but does not become the abstract theorem itself.

---

# 18. Safety proof, liveness proof and impossibility proof are different claim types

## G-F41 — one implementation may satisfy safety under broad schedules but liveness only under restricted schedules

Therefore:

```text
CorrectnessClaim
cannot be one untyped Boolean.
```

## G-F42 — impossibility theorem quantifies over all algorithms in a model

An impossibility result is not an observed failure of one implementation.

Therefore:

```text
ObservedAlgorithmFailure
!= ImpossibilityTheoremByIdentity.
```

## G-F43 — existence theorem is not implementation evidence

Showing some algorithm exists under a model does not prove a deployed Runtime instance realizes its assumptions.

Therefore:

```text
SolvabilityTheorem
!= DeploymentCorrectnessEvidence.
```

---

# 19. Coordination correctness is compositional but not purely local

## G-F44 — local correctness does not imply global coordination property automatically

Each component may individually satisfy its local transition rules while the composed system violates agreement, ordering or global invariant requirements.

Therefore:

```text
AllComponentsLocallyValid
!= GlobalCoordinationCorrectnessByIdentity.
```

## G-F45 — global property does not require one central coordinator

Consensus/linearizable/shared-object abstractions can be realized without a unique semantic central controller.

Therefore:

```text
GlobalCoordinationProperty
!= CentralCoordinatorExistenceByIdentity.
```

This aligns with broader Ordivon anti-centralization findings without importing Host ontology.

---

# 20. Agent-era multi-agent systems do not create a new concurrency primitive

## G-F46 — multiple Agents sharing Tools/state

Human/Agent/synthetic participants can instantiate the same coordination problems:

```text
concurrent writes
leader election
agreement
exclusive ownership
version conflicts
barriers
quorum decisions
```

Therefore:

```text
AgentConcurrency
!= NewAgentEraCoordinationPrimitive.
```

## G-F47 — model sampling is not scheduler ordering

Two Agent calls may each sample internally while Runtime/coordination decides their relative completion/application order.

Therefore:

```text
ModelSamplingRandomness
!= ConcurrencyScheduleByIdentity.
```

F and G remain distinct.

## G-F48 — same Agent outputs, different commit order

Identical proposed writes/actions applied in different admissible orders can yield different shared-state histories.

Therefore:

```text
SameAgentProposalSet
!= SameConcurrentSystemOutcomeByIdentity.
```

Agent-era systems amplify the need for typed proposal/commit/order semantics rather than inventing a new computing substance.

---

# 21. Round A relation

Round A is strengthened and partially consumed.

G depends on:

```text
ComputationalBoundary
InteractionInterfaceWhenPresent
ContinuationOrTerminationSemantics
EnvironmentAssumptions
```

but adds multi-actor ordering, progress and model-relative solvability that A alone did not express.

Therefore:

```text
G != mere A specialization.
```

---

# 22. Round B relation

Round B already owns abstract resource/feasibility dimensions such as:

```text
communication bits/messages/rounds
synchronization rounds
work/depth
```

G adds a different question:

```text
is the coordination task solvable/correct at all under this model?
```

Therefore:

```text
CoordinationSolvability
!= CommunicationOrSynchronizationCostByIdentity.
```

B remains orthogonal.

---

# 23. Round C relation

C absorbs much of G's specification/refinement machinery:

```text
history semantics
linearizability/refinement relation
consistency specification
property target
```

but C alone does not supply the concurrency-specific bundle of:

```text
partial order
component/participant relation
timing/synchrony
failure model
scheduler/fairness
progress
coordination solvability/impossibility.
```

Therefore G overlaps C but leaves an irreducible coordination/model burden.

---

# 24. Round F relation

F's scheduler/adversary distinction is clarified.

In G:

```text
scheduler/adversary
```

exists even in deterministic algorithms with no probabilistic choice.

Therefore:

```text
SchedulerSemantics
belongs primarily to concurrent/distributed execution-model structure;
F references it when probability coexists.
```

This is a real factorization correction:

```text
F should not own scheduler/adversary by itself.
```

F retains probability-space/distribution/risk semantics.

---

# 25. Strong surviving candidate — Computational Coordination / Consistency / Progress Responsibility

A new burden survives destructive subtraction:

```text
ComputationalCoordinationConsistencyAndProgressResponsibility
```

Minimum current burden:

## 25.1 Component / participant / operation model

```text
what concurrent computational actors/objects/operations participate?
```

## 25.2 History / event / order structure

```text
invocation-response order?
program order?
causal/happened-before relation?
transaction/order graph?
```

No universal total order is assumed.

## 25.3 Shared-state / communication / synchronization primitive model

```text
message passing?
registers?
queues?
atomic objects?
broadcast?
```

This is abstract Computing model, not physical Network topology.

## 25.4 Coordination / consistency / safety specification

Examples:

```text
linearizability
serial order relation
agreement
mutual exclusion
invariant preservation
```

No closed enumeration.

## 25.5 Progress / liveness requirement

```text
termination
wait-freedom
lock-freedom
system-wide progress
availability
```

Must remain separate from safety.

## 25.6 Timing / synchrony assumptions

```text
asynchronous
synchronous
partial synchrony
bounded/unbounded delay
clock assumptions
```

## 25.7 Failure / adversary model

```text
crash
omission
partition
Byzantine/adversarial
bounded number of failures
```

Actual fault truth remains owner-external.

## 25.8 Scheduler / fairness assumptions

```text
which interleavings/resolutions are admissible?
what fairness/progress assumptions hold?
```

## 25.9 Solvability / impossibility claim

```text
exists algorithm?
no algorithm can satisfy all properties?
under exactly which model and quantifiers?
```

## 25.10 Resource / bound references

Links to Round B for:

```text
messages
bits
rounds
shared-state operations
step complexity
```

## 25.11 Witness / refinement / proof relation

Links to Round C for:

```text
linearization witness
simulation/refinement
invariant proof
impossibility argument
```

---

# 26. Is G an independent sibling?

Current answer:

```text
partially, but not cleanly.
```

G is more independent than D/F because it introduces an irreducible multi-actor coordination/solvability burden not already represented by probability or approximation.

But it still depends heavily on A/C/B:

```text
A → boundary/continuation/environment
C → history semantics/refinement/specification
B → resource costs
F → probability when randomized
```

Therefore current classification:

```text
STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE
PARTIALLY_ORTHOGONAL_TO_A_B_C_F
WITH_IRREDUCIBLE_COORDINATION_SOLVABILITY_BURDEN
NOT_YET_PROVEN_INDEPENDENT_NUMBERED_FOUNDATION
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 27. Candidate deletion results

Rejected as universal primitives:

```text
Concurrency
Parallelism
Atomicity
Linearizability
Serializability
Consistency
Consensus
GlobalOrder
GlobalClock
Synchrony
Asynchrony
Failure
Availability
Scheduler
Fairness
WaitFreedom
LockFreedom
PartitionTolerance
```

All remain useful scoped concepts under a declared computational model/specification.

---

# 28. Anti-collapse laws

```text
Concurrency != PhysicalParallelism
Parallelism != Coordination
SameFinalState != SameConcurrentCorrectness
SameOperationMultiset != SameConcurrentHistorySemantics
Linearizability != Consistency
Linearizability != Serializability
LinearizationWitness != PhysicalWorldInstant
Safety != Progress
AvailabilityOrTermination != SafetyCorrectness
ObservedCompletion != ProgressGuarantee
SystemWideProgress != PerOperationWaitFreedom
MutualExclusionSafety != NonblockingProgress
AlgorithmText != LivenessGuaranteeWithoutSchedulerAssumptions
AbstractScheduler != RuntimeScheduler
Fairness != SafetySpecification
DistributedCausalOrder != UniversalTotalOrder
LogicalClockOrder != CausalOrder
ChosenTotalOrder != WorldCausalOrder
GlobalPhysicalClock != necessary for all distributed correctness
ConsensusSafety != ConsensusTermination
ConsensusTask != ConsensusAlgorithm
ConsensusImpossible without model qualifiers = invalid universalization
FLPImpossibility != ImpossibilityOfConsensusSafety
FailureModel can change solvability
SynchronyAssumption can change solvability
TimingBoundExists != BoundKnownFromStart != BoundEventuallyHolds
CrashFailure != ByzantineFailure
ProcessCrash != NetworkPartition
NonresponseObservation != GroundTruthCrash
CAP != UniversalChooseAnyTwoLaw
CAPConsistency != ConsistencyInGeneral
NetworkPartitionTruth != CAPImpossibilityClaim
SharedMemoryExists != UniversalSynchronizationPower
AdmittedPrimitiveFamily can change solvability
AbstractCommunicationModel != NetworkTransport
ModelAssumption != RuntimeOrNetworkObservation
ObservedAlgorithmFailure != ImpossibilityTheorem
SolvabilityTheorem != DeploymentCorrectnessEvidence
AllComponentsLocallyValid != GlobalCoordinationCorrectness
GlobalCoordinationProperty != CentralCoordinatorExistence
AgentConcurrency != NewAgentEraPrimitive
ModelSamplingRandomness != ConcurrencySchedule
SameAgentProposalSet != SameConcurrentOutcome
CoordinationSolvability != CommunicationCost
```

---

# 29. Rival-model update

## M1 Function evaluation

Further rejected as universal: concurrent/distributed systems require history/order/progress semantics beyond extensional values.

## M2 Controlled state transition

Strengthened but insufficient unless transitions compose into a multi-actor event/order model with consistency/progress assumptions.

## M3 Information transformation

Still unresolved. Communication/information availability matters to coordination, but consistency/progress/impossibility do not collapse into information quantity alone.

## M4 Effective procedure

Partial. Procedure text alone does not determine solvability under timing/failure/scheduler models.

## M5 Resource-bounded process

Round B remains strong. Resource limits differ from model-relative coordination possibility.

## M6 Interactive process

Strongly relevant to distributed/concurrent systems but still not universal. G sharpens interaction into multi-actor coordination/history semantics.

## M7 Physical realization

Still unresolved. Actual network, clocks, hardware faults and schedulers remain physical realizations of abstract models rather than the models themselves.

---

# 30. Current A/B/C/D/F/G factorization

```text
A — boundary / interaction / continuation / environment
      ↑
      │ G specializes multi-actor environment + continuation
      │
G — coordination / consistency / progress / solvability
      ├── C supplies history/spec/refinement relations
      ├── B supplies communication/round/synchronization resource accounting
      └── F supplies probability/risk when randomization is present

C — interpretation / semantic relation
D — approximation / error / validation
F — stochasticity / distribution / risk
B — resource / feasibility
```

G is the first post-B candidate that again carries a plausible irreducible sibling-level burden, but it is not yet admitted as a numbered foundation.

---

# 31. Agent-era result

Agent societies, multi-agent workflows and concurrent Tool users do not create a new concurrency ontology.

They increase practical frequency of:

```text
concurrent proposals
commit races
version conflicts
shared-resource contention
leader/owner election
quorum decisions
partial failures
nondeterministic completion ordering
```

The same pre-Agent coordination semantics apply.

Agent-era novelty is primarily composition pressure across Harness/Runtime/Network/Computing owners.

---

# 32. Round G verdict

```text
Concurrency as universal essence of computation
= REJECTED

Consistency as one Boolean/property
= REJECTED

Consensus as universal coordination primitive
= REJECTED

Global total order as universal distributed truth
= REJECTED

Synchrony/asynchrony as implementation-only detail
= REJECTED

Failure as one primitive
= REJECTED

Impossibility as model-free statement
= REJECTED
```

Strong survivor:

```text
ComputationalCoordinationConsistencyAndProgressResponsibility
```

Classification:

```text
STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE
PARTIALLY_ORTHOGONAL_TO_A_B_C_F
WITH_IRREDUCIBLE_COORDINATION_SOLVABILITY_BURDEN
NOT_YET_PROVEN_INDEPENDENT_NUMBERED_FOUNDATION
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 33. Information gain

Round G information gain is **VERY HIGH**.

It exposes a new foundation axis not captured by simple interaction or semantics:

```text
multi-actor coordination
under partial order
with explicit progress goals
under timing/failure/scheduler assumptions
where solvability itself can change when assumptions change.
```

Most importantly it corrects Round F's provisional ownership: scheduler/adversary semantics are primarily concurrency/execution-model structure; F references them when probability is composed with nondeterminism.

---

# 34. Next frontier — deliberately unselected

Still-open high-value continents include:

```text
physical / analog / reversible / quantum computation
computability / decidability / oracle-relative computation
state / memory / persistence / memory-consistency models
information / coding / algorithmic information
online / streaming computation
real-time / cyber-physical computation
biological / neuromorphic computation
```

Physical/unconventional computation remains mandatory before numbered admission because the deepest unresolved question still stands:

```text
what non-circular relation makes a physical process a computation,
rather than arbitrary World dynamics interpreted after the fact?
```

Computability/decidability also remains important because FLP-like impossibility is model-relative coordination impossibility, not the same kind of impossibility as undecidability/uncomputability.

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 35. Primary-source pressure anchors

Used as pressure sources, not ontology authority:

- Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, Communications of the ACM 21(7), 1978.
- Maurice Herlihy and Jeannette Wing, *Linearizability: A Correctness Condition for Concurrent Objects*, ACM TOPLAS 12(3), 1990.
- Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, *Impossibility of Distributed Consensus with One Faulty Process*, JACM 32(2), 1985.
- Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, *Consensus in the Presence of Partial Synchrony*, JACM 35(2), 1988.
- Maurice Herlihy, *Wait-Free Synchronization*, ACM TOPLAS 13(1), 1991.
- Seth Gilbert and Nancy Lynch, *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services*, SIGACT News 33(2), 2002.
- Roberto Segala / Nancy Lynch probabilistic-process work remains a cross-anchor for the scheduler/probability separation inherited from Round F.
