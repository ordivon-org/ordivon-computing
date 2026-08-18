---
schema_version: 1
id: computing.research.deep-foundations.post-xa.round-4.reliable-fault-tolerant-self-stabilizing
title: Ordivon Computing Deep Foundations — Post-X-A Round 4: Reliable / Fault-Tolerant / Self-Stabilizing Computation
profile: research
lifecycle: completed
source_role: research-round
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Destructive tournament over Reliable / Fault-Tolerant / Self-Stabilizing Computation under explicit fault/perturbation models. Cross-regime pressure from noisy Boolean formulas, dependability fault/error/failure separation, self-stabilization, distributed Byzantine/crash faults, coding/error correction, crash/restart and intermittent execution controls, replicated/coded computation, adversarial versus stochastic faults, quantum threshold fault tolerance, approximate-computing negative controls and Agent/provider/tool controls fails to produce a clean independent reliability sibling. The provisional ComputationalReliabilityAndResilienceUnderFaultsResponsibility is deleted into C semantic preservation/specification, F stochastic risk where applicable, G coordination-specific failure/safety/progress, H physical/noise realization, J retention/reconstruction where recovery is involved, K coding/recoverability when used, B resource/overhead/model feasibility, I solver/construction existence, with A environment/continuation assumptions and external owners as needed. Reliability is therefore a derived model-indexed preservation/existence profile, not a primitive substance. This is the fourth consecutive large-continent consolidation after J, K and X-A. Under the precommitted stopping rule, the next research phase is FORMAL WHOLE-COMPUTING COVERAGE/SATURATION TEST; whole-Computing closure itself is still NOT CLAIMED and no CDF is admitted.
evidence_status: strong-local-plus-primary-source-pressure
readiness: ROUND_4_COMPLETE_RELIABILITY_CONSOLIDATED_SATURATION_TEST_TRIGGERED_NO_CDF_ADMISSION
---
# Ordivon Computing Deep Foundations — Post-X-A Round 4
## Reliable / Fault-Tolerant / Self-Stabilizing Computation

# 0. Canonical entry state

Round 4 begins after R3 freshly selected the following route:

```text
Reliable / Fault-Tolerant / Self-Stabilizing Computation
under explicit Fault / Perturbation Models
```

with only the following provisional attack hypothesis:

```text
ComputationalReliabilityAndResilienceUnderFaultsResponsibility
= HYPOTHESIS ONLY
= NOT ADMITTED
= NOT A CDF
```

Entry frontier:

```text
WholeComputingSearchA-K = COMPLETED RESEARCH HISTORY
J                      = CONSOLIDATING
K                      = CONSOLIDATING
X-A Access/Change      = CONSOLIDATING
WholeComputingClosure  = NOT CLAIMED
CDF0                   = NOT ADMITTED
NumberedCDFCount       = 0
NextCDF                = UNKNOWN
```

The precommitted stopping rule says:

```text
If one further large orthogonal high-information continent consolidates with:

NewSibling = NONE
B/G/H/I falsified = NONE
A/C/D/F/J/K reopened = NONE
NewOwnerBoundary = NONE

then begin a formal Whole Computing coverage/saturation test.
```

Round 4 therefore has unusually high closure-discrimination value.

---

# 1. Term separation before any reliability ontology

Dependability research distinguishes related but non-identical notions around faults, erroneous states and service failures. The broad Computing tournament must preserve that separation without importing a whole systems-dependability taxonomy as primitive ontology.

Minimum anti-collapse laws:

```text
Fault
!= Error
!= Failure

Reliability
!= Availability

Reliability
!= CorrectnessByIdentity

FaultTolerance
!= Recovery

FaultTolerance
!= Redundancy

FaultTolerance
!= ErrorCorrection

FaultTolerance
!= Replication

FaultTolerance
!= SelfStabilization

FaultModel
!= FailureProbability

Masking
!= Detection
!= Correction
!= Recovery

GracefulDegradation
!= ExactFaultTolerance

ThresholdCondition
!= ResourceBudget

FaultContainment
!= FaultElimination

ObservedSuccessDespiteFault
!= GeneralFaultToleranceGuarantee
```

These separations are not terminological decoration. Each is needed to avoid hiding the actual relation being claimed.

---

# 2. Rival models

Seven explanations are attacked.

## RF-M1 — reliability is just ordinary correctness

Prediction:

```text
CorrectnessSpecification
already captures all fault-tolerance claims.
```

## RF-M2 — fault tolerance is error correction / coding

Prediction:

```text
FaultTolerance
= K coding/recoverability
```

## RF-M3 — fault tolerance is state recovery

Prediction:

```text
FaultTolerance
= J retention/reconstruction
```

## RF-M4 — fault tolerance is stochastic risk control

Prediction:

```text
FaultModel
= probability distribution
ReliabilityGuarantee
= failure probability bound
```

## RF-M5 — fault tolerance is coordination under failures

Prediction:

```text
FaultTolerance
= G failure/safety/progress
```

## RF-M6 — reliability is a model-indexed composition

Prediction:

```text
Fault/perturbation model
+ target semantics
+ preserving/resilient construction
+ success/failure criterion
+ resource/existence claims

can be expressed through existing responsibilities without a new sibling.
```

## RF-M7 — independent Computational Reliability / Resilience responsibility

Prediction:

```text
After D/F/G/H/J/K/B/C/I/A and external-owner subtraction,
a nontrivial reliability relation remains that cannot be represented as semantic preservation/existence under a declared perturbation model.
```

Round 4 is designed to destroy RF-M7 if possible.

---

# 3. Noisy Boolean formulas: reliability adds a fault regime and overhead, not a new semantic substance

Pippenger's reliable-computation result studies formulas built from gates that fail randomly. The key results establish both a tolerable-noise limitation and an unavoidable depth/slowdown pressure for formulas that tolerate failures.

This immediately separates:

```text
IdealBooleanFunction
!= NoisyFormulaRealization

GateFailureProbability
!= FormulaFailureProbabilityByIdentity

ReliableFormula
!= FaultFreeFormulaByIdentity

ReliabilityOverhead
!= ReliabilityGuarantee
```

The theorem is structurally rich, but its burdens factor cleanly:

```text
C:
  ideal Boolean function / noisy-formula semantic relation
  correctness/preservation criterion

F:
  random gate-failure model and output failure probability

B:
  depth / slowdown / size overhead and feasible fault-rate regime

I / Algorithmics:
  existence/nonexistence of a formula family satisfying the required reliability contract

H:
  only when actual physical noisy gates are claimed rather than an abstract noisy-gate model
```

K is not universally required. A noisy reliable formula need not be described fundamentally as an error-correcting code.

Therefore:

```text
ReliableComputationWithNoisyGates
!= ErrorCorrectingCodingByIdentity
```

and:

```text
NoisyGateReliabilityPressure
= C + F + B + I
(+ H for physical realization)
```

No independent reliability residue is forced.

---

# 4. Fault model is not failure probability

The stochastic noisy-gate regime might tempt the architecture to identify reliability with F.

Quantum fault tolerance blocks that move decisively.

Aharonov–Ben-Or prove a threshold result for quantum computation that explicitly covers a very general noise model that need not be probabilistic.

Therefore:

```text
FaultModel
!= ProbabilityDistribution

FaultTolerance
!= ProbabilisticCorrectnessByIdentity
```

F owns stochastic distributions when the model is probabilistic.
But adversarial, bounded, norm-constrained, set-valued or otherwise nonprobabilistic fault models can remain declared model assumptions without becoming probability objects.

RF-M4 is rejected as universal.

---

# 5. Quantum threshold fault tolerance: the strongest cross-owner test still composes

Aharonov–Ben-Or's threshold theorem supplies an exceptionally hostile regime because it combines:

```text
ideal quantum computation
noisy elementary realization
quantum error-correcting structure
fault-tolerant gate constructions
noise threshold condition
reliability guarantee
time/space overhead
universality
```

Important separations:

```text
QuantumComputation
!= FaultTolerantQuantumComputation

PhysicalQuantumRealization
!= ReliabilityUnderNoise

QuantumErrorCorrection
!= WholeFaultTolerantComputationByIdentity

ThresholdCondition
!= ResourceBudget

EncodedStateProtection
!= FaultTolerantLogicalOperationByIdentity
```

Yet the architectural factorization remains available:

```text
H:
  quantum physical-realization/noise interface
  preparation/operation/readout fidelity assumptions when physical

C:
  ideal logical computation ↔ encoded/noisy realized computation relation
  semantic preservation / simulation / acceptable output relation

K:
  code/decoder/recoverability structure where quantum coding is used

F:
  stochastic failure/risk only when the declared noise model is probabilistic

B:
  time/space/gate/ancilla/overhead feasibility
  threshold-indexed feasible regime

I:
  existence of a fault-tolerant construction/simulation under the declared model

D:
  only where an explicit approximation/error metric or validation layer is part of the contract
```

The cross-regime theorem does not require a new primitive merely because many responsibilities must compose.

Key conclusion:

```text
ReliableSimulationUnderNoise
can be expressed as
model-indexed semantic preservation/existence + feasibility
rather than a primitive Reliability substance.
```

---

# 6. Error correction and redundancy are mechanisms, not fault tolerance itself

Round K already established:

```text
Redundancy != Waste
CompressionObjective != ReliabilityObjective
```

Round 4 adds:

```text
Redundancy
!= FaultToleranceByIdentity

ErrorCorrectingCode
!= FaultToleranceByIdentity
```

Counterexamples in both directions are easy:

```text
redundant but correlated copies
can fail together

self-stabilizing transition rules
can recover without decoding a codeword

retry/recomputation
can tolerate some transient faults without a channel code

an error-correcting code
can protect representation while the surrounding computation still propagates logical faults unsafely
```

K therefore owns coding/recoverability only when coding is actually the resilience mechanism.

RF-M2 is rejected.

---

# 7. Self-stabilization: recovery without a checkpoint

Dijkstra's self-stabilizing systems give the strongest attack on RF-M3.

The system is required to reach a legitimate global state after finitely many moves regardless of initial state and permitted move selections under the stated daemon/model conditions.

This is not ordinary checkpoint restoration.

```text
RecoveryFromKnownRetainedState
!= SelfStabilizationFromAdmissibleArbitraryState
```

and:

```text
KnownPriorValidState
is not required by self-stabilization.
```

The correct factorization is:

```text
C:
  definition of legitimate state / global requirement
  semantic state relation

G:
  distributed participants
  daemon/scheduler assumptions
  global invariant/progress structure

A:
  admitted continuation/environment behavior assumptions

B:
  bounded/finitary convergence-step claims when cost/guarantee is material

I:
  existence of a self-stabilizing algorithm/system for the declared model

J:
  only if some retained/reconstructed state across a disruption boundary is explicitly used
```

Thus self-stabilization directly proves:

```text
FaultToleranceOrResilience
!= J RecoveryByIdentity
```

RF-M3 is rejected.

---

# 8. Self-stabilization does not generalize G into all reliability

Dijkstra's example is distributed and therefore heavily uses G.

But noisy formulas and quantum threshold computation demonstrate reliability pressure in regimes where the defining issue is not multi-actor coordination.

Therefore:

```text
CoordinationFailureModel
!= GenericComputationalFaultModel
```

and:

```text
G
owns coordination-specific
failure/scheduler/safety/progress structure,
not all reliable computation.
```

RF-M5 is rejected as universal.

---

# 9. Byzantine / arbitrary faults: G retains local ownership; Security remains external

The Byzantine Generals line demonstrates that arbitrary/traitorous participant behavior changes what agreement can be guaranteed and how many participants/communication assumptions are required.

This is a key hostile case because `fault` cannot be collapsed to crash-stop.

```text
CrashFailure
!= ByzantineFailure
!= OmissionFailure
!= CorruptionFault
```

Broad factorization:

```text
G:
  coordination task
  participant/failure model
  safety/agreement/progress
  scheduler/timing/communication assumptions

I:
  existence/impossibility of a solver/protocol under that model

B:
  communication/round/process/resource overhead

Security:
  actual malicious compromise, authority and adversarial security truth
```

Computing may quantify over an abstract Byzantine fault model without claiming that a real participant is malicious.

No generic reliability sibling is required.

---

# 10. Crash/restart and checkpoint recovery: J/Runtime control

A crash followed by restart can be made fault-tolerant through checkpointing, logs, replay, replication, idempotency, transactions or other mechanisms.

But:

```text
CrashTolerance
!= CheckpointingByIdentity

Recovery
!= FaultToleranceByIdentity
```

Round J already owns:

```text
retention lifetime
capture/snapshot relation
reconstruction sufficiency
external dependency completeness
continuity consequence
```

Runtime owns the actual Job/process/restart/checkpoint facts.

Computing-level fault tolerance only consumes those relations when a particular reliable-computation construction uses them.

Independent Runtime research supplies a useful owner control: intermittent/energy-harvesting execution established that logical continuation can span physically disconnected powered episodes and reduced its generic structure into existing Runtime recovery/idempotency/atomicity/resource/retention foundations rather than creating a new Runtime root.

This reinforces:

```text
ResilienceMechanism
can vary radically
without implying a new broad Computing primitive.
```

---

# 11. Detection, masking, correction and recovery are distinct

A reliability architecture can:

```text
detect an error without correcting it
mask a fault without explicitly detecting it
correct a corrupted representation without reconstructing a process
recover a valid continuation after a failure
```

Therefore:

```text
Detection
!= Masking
!= Correction
!= Recovery
```

Their ownership depends on the claim:

```text
C/D:
  detection/validation criteria and semantic deviation

K:
  correction through coding/recoverability when used

J:
  recovery/reconstruction from retained state when used

G:
  masking/replication/coordination under participant faults when coordination-specific

H:
  physical detection/correction mechanisms and device noise facts when realized physically

B:
  cost/overhead
```

No single mechanism is universal across fault-tolerant computation.

---

# 12. Replication / redundancy / coded computation

Replication is another candidate essence that fails.

```text
Replication
!= FaultTolerance
```

because:

```text
identically faulty replicas can reproduce the same wrong result
common-mode faults can defeat replication
Byzantine replicas require a coordination/voting/protocol contract
coding may replace literal replication
self-stabilization may use state dynamics rather than replicated results
```

When replication works, factorization is typed:

```text
G:
  replica coordination/order/agreement when multi-actor

C:
  equivalence/voting/acceptance semantics

F:
  independence/correlation/failure probability assumptions when stochastic

K:
  coded redundancy if coding is used

B:
  replica/resource overhead

H:
  physical common-mode/correlation facts when real devices are claimed
```

Again, no independent primitive remains.

---

# 13. Correlated faults and common-mode failure block naive amplification

Round F already established:

```text
RepeatedTrials
!= IndependentTrials
```

Round 4 applies the same pressure to redundant systems:

```text
MoreReplicas
!= LowerFailureProbabilityByNecessity
```

without an independence/dependence model.

Thus:

```text
RedundancyCount
!= ReliabilityGuarantee
```

F owns statistical dependence assumptions where probabilistic.
H/World/Hardware may own real common-mode physical causes.
Security may own deliberate correlated compromise.

The reliability claim remains model-indexed rather than object-intrinsic.

---

# 14. Fail-stop, omission, corruption and arbitrary faults are not one scalar severity axis

Different fault models permit different behaviors:

```text
fail-stop
omission
value corruption
timing fault
state perturbation
arbitrary/Byzantine behavior
```

These cannot in general be ordered by one universal scalar `fault severity` without a declared simulation/dominance relation.

Therefore:

```text
FaultModel
is a typed behavioral/model assumption,
not one universal numeric resource.
```

This mostly reinforces A/B/G/H/C model specificity rather than creating a new responsibility.

---

# 15. Reliability is not availability

A system may be:

```text
highly available but occasionally wrong
```

or:

```text
rarely available but correct whenever it provides a result
```

Hence:

```text
Reliability
!= Availability
```

In broad Computing:

```text
G/A:
  progress/response behavior when part of the computational contract

C/F:
  correctness/reliability property, potentially probabilistic

Runtime/Network:
  actual operational availability/reachability
```

This blocks importing service availability as the essence of computation reliability.

---

# 16. Reliability is not correctness by identity

Ordinary correctness can be stated under a fault-free model.
Fault-tolerance claims quantify over a richer set of admitted perturbed/faulty executions or realizations.

Therefore:

```text
CorrectUnderNominalModel
!= CorrectUnderDeclaredFaultModel
```

But this does not force a new primitive.
It is expressible as a change in the quantified computational/environment model plus a preservation/specification relation.

The strongest surviving reconstruction is:

```text
ReliabilityClaim
=
TargetSpecification
+
DeclaredFault/PerturbationModel
+
AdmittedConstruction/Realization
+
QuantifiedPreservation/SuccessCriterion
+
Bound/Probability/ProgressQualifierWhenRelevant
```

This is a model-indexed claim schema, not an ontological substance.

RF-M1 is rejected in its naive identity form, while RF-M6 is strengthened.

---

# 17. Approximate / graceful-degradation negative control

Approximate computation is deliberately used as a negative control.

A system may intentionally return a lower-quality but contract-valid answer even when no component fault occurred.

Therefore:

```text
GracefulDegradation
!= FaultToleranceByIdentity
```

and:

```text
ApproximationError
!= Fault-induced FailureByIdentity
```

Factorization:

```text
D:
  error/quality/tolerance criterion

C:
  specification/acceptance semantics

B:
  resource-quality tradeoff

F:
  probability if quality/failure is stochastic
```

A resilience system may use graceful degradation as one response policy, but degradation is not the primitive.

---

# 18. Agent/provider/tool failures — Harness owner control

Agent-era systems expose:

```text
provider failures
sample-level incorrectness
tool-call errors
timeouts
stale observations
context loss
partial external effects
```

These are important but do not create an Agent-specific Computing reliability primitive.

Owner subtraction:

```text
Harness:
  Agent run/tool/context/orchestration failure semantics

Runtime:
  concrete attempt/retry/cancel/recovery/execution truth

Network:
  actual delivery/reachability faults

World:
  actual environmental change/measurement truth

Security:
  malicious/adversarial compromise and authority
```

Computing retains only the abstract model-relative pieces:

```text
A — allowed external failure/revelation assumptions
B — retry/query/token/resource budgets
C — task/output/semantic acceptance
D — quality/error validation where relevant
F — sampled/stochastic failure risk where relevant
I — existence of a solver/strategy under the declared regime
```

Agent-era perturbation therefore increases practical importance without producing a new foundation.

---

# 19. Direct deletion of the provisional reliability burden bundle

R3 proposed a common structure:

```text
TargetComputationContract
+
FaultOrPerturbationModel
+
FaultyPrimitiveOrRealizationModel
+
ResilienceConstructionOrTransformation
+
PreservationOrRecoveryCriterion
+
ReliabilityGuarantee
+
OverheadOrThresholdOrFeasibilityClaim
```

Round 4 now deletes each field.

## 19.1 TargetComputationContract

```text
→ C semantic/specification relation
+ A boundary/behavior when interactive
+ I task/solver contract when solvability is asserted
```

No residue.

## 19.2 FaultOrPerturbationModel

```text
→ A environment/model assumptions generically
→ F when stochastic/probabilistic
→ G when participant/coordination failure-specific
→ H when physical noise/realization-specific
→ C when fault means a typed semantic transition/deviation class
→ Security/World/Network/Runtime when actual external fault truth belongs there
```

No residue.

## 19.3 FaultyPrimitiveOrRealizationModel

```text
→ B computational/admitted-operation model
→ H physical realization when physical
→ G when distributed participant/communication primitive
→ C semantic operation model
```

No residue.

## 19.4 ResilienceConstructionOrTransformation

```text
→ C transformation/refinement/simulation relation
→ I/Algorithmics construction existence
→ K/J/G conditionally according to mechanism
```

No residue.

## 19.5 PreservationOrRecoveryCriterion

```text
→ C preservation/correctness/equivalence/refinement
→ J only when reconstruction/retention is actually involved
→ D when tolerance/error metric is actually involved
→ G when safety/progress/coordination property is actually involved
```

No residue.

## 19.6 ReliabilityGuarantee

```text
→ C quantified correctness/preservation property
→ F if probabilistic
→ G if availability/progress under coordination failures
→ A if continuation/termination behavior
```

No residue.

## 19.7 OverheadOrThresholdOrFeasibilityClaim

```text
→ B resource/feasibility
→ I existence/nonexistence under declared regime
→ F/H/C supply model parameters as required
```

No residue.

Direct deletion result:

```text
IndependentReliabilityBurdenAfterSubtraction
= EMPTY AT CURRENT EVIDENCE FRONTIER
```

---

# 20. Rival-model verdicts

```text
RF-M1 Reliability = ordinary correctness by identity
= REJECTED

Reason:
nominal correctness and correctness over a declared fault model are distinct claims.

RF-M2 Fault tolerance = error correction/coding
= REJECTED

RF-M3 Fault tolerance = state recovery
= REJECTED

RF-M4 Fault tolerance = stochastic risk control
= REJECTED AS UNIVERSAL

RF-M5 Fault tolerance = G coordination under failures
= REJECTED AS UNIVERSAL

RF-M6 Reliability = model-indexed composition of existing responsibilities
= STRONG SURVIVOR

RF-M7 independent ComputationalReliabilityAndResilienceUnderFaultsResponsibility
= REJECTED AS CLEAN SIBLING AT CURRENT FRONTIER
```

---

# 21. What survives usefully: a derived reliability profile

Although no primitive survives, a reusable derived profile is useful for concrete claims:

```text
ComputationalFaultResilienceProfile

  TargetComputationOrSpecificationRef
  FaultOrPerturbationModelRef
  FaultLocation/Scope/Duration/CorrelationAssumptions
  FaultyPrimitiveOrRealizationModelRef
  Detection/Masking/Correction/RecoveryMechanismsWhenPresent
  ResilienceConstructionOrTransformationRef
  SemanticPreservationOrAcceptanceCriterion
  Probability/Adversary/UniversalQuantificationMode
  Progress/AvailabilityRequirementWhenPresent
  Retention/ReconstructionReferenceWhenPresent
  Coding/RedundancyReferenceWhenPresent
  PhysicalNoise/RealizationReferenceWhenPresent
  ResourceOverheadAndFeasibilityRef
  ThresholdOrAdmissibleFaultRegime
  Solver/ConstructionExistenceOrImpossibilityBasis
```

This profile is explicitly **derived**.
Its fields are typed references into existing responsibilities/owners.

Do not promote the profile into a Foundation merely because it is operationally useful.

---

# 22. Architecture impact

## B — strengthened, not reopened

B already owns the computational model plus resource/feasibility relation.
Round 4 confirms that fault-rate thresholds, redundancy overhead, depth slowdown, replication cost and resilience resource tradeoffs are B inputs/claims after the fault model is declared.

```text
ThresholdCondition
!= ResourceBudget
```

but both can participate in one B feasibility theorem.

## C — strengthened, not reopened

The central common relation across noisy formulas, self-stabilization and quantum fault tolerance is semantic:

```text
Does the perturbed/faulty construction preserve or eventually satisfy the declared target behavior/property under the quantified fault model?
```

C already has transformation, simulation, refinement and preservation slots.

This strengthens C's role but also preserves the previously identified closure-test risk of semantic contract stuffing. The future saturation phase must attack whether C is being used too permissively.

## F — conditional, not universal

Aharonov–Ben-Or's nonprobabilistic-noise result proves that F cannot own all fault models.
F remains essential only for stochastic/probabilistic fault/risk claims.

## G — coordination-specific

G continues to own participant failure, Byzantine/crash distinctions, safety/progress, timing/scheduler/fairness and coordination under faults.
It does not absorb noisy single-computation or quantum reliability generally.

## H — physical fault/noise interface

H owns actual physical noise, device fidelity, preparation/operation/readout error and the physical realization relation.
It does not own abstract reliability theorem structure by itself.

## J — narrower than resilience

New reinforced law:

```text
RecoveryFromRetainedState
!= SelfStabilizationFromArbitraryAdmissibleState
```

J owns retention/reconstruction only when present.

## K — mechanism-specific

K owns coding/recoverability/redundancy constraints when resilience uses codes.
Fault tolerance is not coding by identity.

## I — construction existence

I owns generic solver/construction existence/impossibility once target/fault models are supplied.
A threshold theorem can therefore include an I-style existential statement plus B/C/H/K/F typed conditions.

## D — typed error/validation only

D is not expanded into `all faults`.
It enters where a declared error/tolerance/approximation/validation relation is material.
Discrete crashes, Byzantine behaviors and arbitrary state perturbations need not be numerical-error objects.

No D reopen is triggered.

---

# 23. Owner subtraction

## Runtime

Runtime owns actual process/job/attempt/restart/checkpoint/retry/interruption/physical execution facts.
A Computing theorem may abstract over crash/restart models without owning those concrete events.

## Network

Network owns actual reachability, delivery, partition and transport failure.
G/Computing may use abstract channel/failure assumptions.

## World

World owns actual physical causation/noise/environmental fault facts.
H links those facts to computational realization claims.

## Hardware

Hardware owns concrete gate/device/memory fault modes and error rates of actual devices.
Computing can analyze abstract noisy-gate or machine models.

## Security

Security owns actual malicious compromise, authority, integrity/confidentiality goals and adversarial security truth.
Computing may quantify over an abstract Byzantine/arbitrary behavior class without re-owning the attack ontology.

## Harness

Harness owns Agent/provider/tool/run/context operational failure semantics.
Computing only consumes abstract task/failure/resource models after subtraction.

No new owner boundary is discovered.

---

# 24. Strong negative results

Round 4 establishes/reinforces the following reusable laws:

```text
Fault != Error != Failure
Reliability != Availability
Reliability != CorrectnessByIdentity
CorrectUnderNominalModel != CorrectUnderDeclaredFaultModel
FaultTolerance != Recovery
FaultTolerance != Redundancy
FaultTolerance != ErrorCorrection
FaultTolerance != Replication
FaultTolerance != SelfStabilization
FaultModel != FailureProbability
FaultModel != ProbabilityDistribution
Masking != Detection != Correction != Recovery
GracefulDegradation != ExactFaultTolerance
ThresholdCondition != ResourceBudget
FaultContainment != FaultElimination
ObservedSuccessDespiteFault != GeneralFaultToleranceGuarantee
GateFailureProbability != FormulaFailureProbability
ReliableComputationWithNoisyGates != ErrorCorrectingCodingByIdentity
QuantumComputation != FaultTolerantQuantumComputation
PhysicalQuantumRealization != ReliabilityUnderNoise
QuantumErrorCorrection != WholeFaultTolerantComputationByIdentity
EncodedStateProtection != FaultTolerantLogicalOperationByIdentity
RecoveryFromKnownRetainedState != SelfStabilizationFromAdmissibleArbitraryState
CoordinationFailureModel != GenericComputationalFaultModel
CrashFailure != ByzantineFailure != OmissionFailure != CorruptionFault
MoreReplicas != LowerFailureProbabilityByNecessity
RedundancyCount != ReliabilityGuarantee
ApproximationError != FaultInducedFailureByIdentity
```

These are first-class research results even though no sibling survives.

---

# 25. Round 4 classification

```text
Reliable / Fault-Tolerant / Self-Stabilizing Computation
= VERY-HIGH-INFORMATION CONSOLIDATION CONTINENT

ComputationalReliabilityAndResilienceUnderFaultsResponsibility
= REJECTED AS CLEAN INDEPENDENT SIBLING

ComputationalFaultResilienceProfile
= DERIVED / OPTIONAL TYPED PROFILE
```

No B/G/H/I claim is falsified.
No A/C/D/F/J/K FoundationReopenCondition is triggered.
No new owner boundary is discovered.

---

# 26. Saturation trigger fires

The campaign now has four consecutive large-continent consolidation outcomes:

```text
J State / Memory
→ consolidation

K Information / Coding
→ consolidation

X-A Access / Revelation / Change
→ consolidation

R4 Reliable / Fault-Tolerant / Self-Stabilizing Computation
→ consolidation
```

The Round-3 precommitted stopping conditions are all satisfied:

```text
NewSibling
= NONE

B/G/H/I falsified
= NONE

A/C/D/F/J/K reopened
= NONE

NewOwnerBoundary
= NONE
```

Therefore the next phase changes.

```text
WholeComputingCoverageSaturationTest
= SHOULD BEGIN NEXT
```

This is **not** a closure claim.

```text
WholeComputingClosure
= NOT CLAIMED
```

The next phase must attempt to falsify saturation by:

```text
1. unknown-continent search outside inherited vocabulary
2. adversarial recombination of surviving responsibilities
3. contract-stuffing tests against B and C
4. owner-boundary inversion tests
5. historical-discipline coverage checksum
6. modern/unconventional/Agent-era regime checksum
7. direct search for phenomena requiring two candidate siblings to merge/split
8. test whether any cross-cutting J/K-style responsibility still contains an unextracted sibling
9. test whether provisional B/G/H/I are genuinely independent rather than artifacts of research order
10. only after those attacks decide whether WholeComputingClosure may be admitted
```

Do not create CDF0 merely because saturation testing begins.

---

# 27. Foundation status

```text
CDF0
= NOT ADMITTED

NumberedCDFCount
= 0

NextCDF
= UNKNOWN
```

Current provisional architecture remains under attack:

```text
strong sibling candidates:
B Resource / Feasibility
G Coordination / Consistency / Progress
H Physical Realization / Grounding
I Effective Solvability / Relative Power

cross-cutting / refactoring:
A Boundary / Behavior / Environment
C Interpretation / Semantic Relations
D Approximation / Error / Validation
F Stochasticity / Distribution / Risk
J State Retention / Reconstruction
K Information Coding / Recoverability
```

Round 4 does not freeze this architecture.
It only provides another independent consolidation result.

---

# 28. Final Round 4 verdict

```text
PostXARound4ReliableFaultTolerantSelfStabilizing
= COMPLETED

InformationGain
= VERY HIGH / CONSOLIDATING

NewSibling
= NONE

ComputationalReliabilityAndResilienceUnderFaultsResponsibility
= REJECTED AS CLEAN SIBLING

ComputationalFaultResilienceProfile
= DERIVED / OPTIONAL

B/G/H/I Falsification
= NONE

A/C/D/F/J/K Reopen
= NONE

NewOwnerBoundary
= NONE

WholeComputingClosure
= NOT CLAIMED

CDF0
= NOT ADMITTED

NumberedCDFCount
= 0

NextCDF
= UNKNOWN

NextComputingResearchPhase
= FORMAL WHOLE-COMPUTING COVERAGE / SATURATION TEST
```

---

# 29. Primary and canonical research anchors

Used as hostile-regime evidence, not ontology authorities:

```text
Nicholas Pippenger.
Reliable Computation by Formulas in the Presence of Noise.
IEEE Transactions on Information Theory 34(2), 1988, 194–197.
DOI: 10.1109/18.2628.

Edsger W. Dijkstra.
Self-stabilizing systems in spite of distributed control.
Communications of the ACM 17(11), 1974, 643–644.
EWD426 author archive.

Dorit Aharonov and Michael Ben-Or.
Fault-Tolerant Quantum Computation With Constant Error Rate.
arXiv:quant-ph/9906129, extended threshold-theorem treatment.

Leslie Lamport, Robert Shostak and Marshall Pease.
The Byzantine Generals Problem.
ACM TOPLAS 4(3), 1982, 382–401.

Algirdas Avizienis, Jean-Claude Laprie, Brian Randell and Carl Landwehr.
Basic Concepts and Taxonomy of Dependable and Secure Computing.
IEEE Transactions on Dependable and Secure Computing 1(1), 2004, 11–33.
Earlier dependability-taxonomy lineage preserved by LAAS/IFIP WG10.4 archives.
```

Internal owner-control evidence:

```text
task:runtime-intermittent-criticality-dataplane-determinism-whole-space-tournament-20260818
revision 3 completed

- intermittent execution: LogicalContinuation != ContinuousPhysicalExecution
- no new Runtime Foundation

Current broad Computing A-K artifacts
- G already owns coordination-specific crash/Byzantine/partition failure models
- H already owns physical noise/realization separation
- J already owns retention/reconstruction rather than all resilience
- K already owns coding/recoverability rather than all reliability
- F already separates probabilistic failure from error magnitude and nondeterminism
```
