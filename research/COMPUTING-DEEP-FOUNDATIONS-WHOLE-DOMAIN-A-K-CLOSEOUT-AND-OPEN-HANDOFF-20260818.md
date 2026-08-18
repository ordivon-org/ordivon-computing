---
schema_version: 1
id: computing.research.deep-foundations.whole-domain-a-k-closeout-open-handoff
title: Ordivon Computing Deep Foundations — Whole-Domain A–K Closeout and Open Handoff
profile: research
lifecycle: completed
source_role: research-closeout-handoff
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Closeout of the first whole-Computing fresh domain-coverage campaign. Rounds A–K reconstructed boundary/behavior, resources, semantics, approximation, stochasticity, concurrency/distributed coordination, physical realization, computability/relative power, state/persistence and information/coding. Four strong sibling-level candidates currently survive (B, G, H, I); A/C/D/F/J/K appear more cross-cutting or mutually refactoring. No numbered Computing Deep Foundation has been admitted. The closeout explicitly distinguishes deeply explored space, partially touched space and major unexplored continents, and intentionally leaves NextCDF and NextComputingRoute UNKNOWN so a new conversation can perform a fresh information-gain search rather than inherit a roadmap.
evidence_status: closeout
readiness: FIRST_WHOLE_DOMAIN_CAMPAIGN_CLOSED_NEXT_ROUTE_OPEN
---
# Ordivon Computing Deep Foundations — Whole-Domain A–K Closeout and Open Handoff

## 0. Purpose

This document closes the first fresh whole-Computing domain-coverage campaign.

It does **not** claim that Computing as a whole is exhausted.
It does **not** admit `CDF0`.
It does **not** select the next research continent.

Its role is to preserve:

```text
what has been deeply explored
what has only been partially touched
what remains substantially unexplored
what architecture currently survives
what was rejected
what must not be inherited as a roadmap
```

Canonical frontier at closeout:

```text
WholeComputingSearchA-K = COMPLETED RESEARCH HISTORY
CDF0                    = NOT ADMITTED
NumberedCDFCount        = 0
NextCDF                 = UNKNOWN
NextComputingRoute      = UNKNOWN
WholeComputingClosure   = NOT CLAIMED
```

---

# 1. Starting point of the campaign

Before this campaign, Ordivon Computing had substantial local work on:

```text
Agent-era responsibility boundaries
PAL / RSI loops
causal explanation / experiment methodology
parallelism / data movement
compact state-computation-memory models
classical substrate vs Agent overlay
```

but no first-principles reconstruction of the entire referent called `Computing`.

The opening atlas therefore deliberately refused to inherit PAL, Runtime, programming-language curricula, complexity theory, AI or any other local tradition as the roadmap.

Seven rival whole-referent models were put under pressure:

```text
M1 Function Evaluation
M2 Controlled State Transition
M3 Information Transformation
M4 Effective Procedure
M5 Resource-Bounded Process
M6 Interactive Process
M7 Physical Realization
```

No rival was allowed to become canonical by familiarity alone.

---

# 2. Deeply explored space — Round A

## Closed Function / Effective Procedure vs Interactive / Reactive Behavior

Round A attacked the idea that computation is universally a terminating function evaluation.

Established separations include:

```text
SameFinalOutput != SameComputationalBehavior
NonTermination != Failure
FunctionEvaluation != universal behavior shape
Interaction != universal computation essence
ProgramText != ComputationOccurrence
Persistence != Interaction
ProviderSessionIdentity != ComputationalProcessIdentity
TerminationStatus != CorrectnessStatus
```

Strong survivor:

```text
ComputationalBoundaryAndBehaviorResponsibility
```

Current burden included:

```text
ComputationalBoundary
TransitionOrBehaviorSemantics
InteractionInterfaceWhenPresent
ObservationOrEquivalenceSemantics
ContinuationOrTerminationSemantics
EnvironmentAssumptions
```

Later rounds refactored parts of this burden, but A remains essential for computational boundary, ongoing behavior, continuation and environment semantics.

Information gain: `HIGH`.

---

# 3. Deeply explored space — Round B

## Computational Resource Plurality / Cost / Feasibility

Round B destructively separated:

```text
time
space
I/O
data movement
communication
parallel work/depth
energy
samples
queries
precision
tokens/tool calls
```

Key results:

```text
WallClockTime != ComputationalStepComplexity
TimeCost != SpaceCost
ArithmeticOperationCount != DataMovementCost
CommunicationComplexity != NetworkTrafficMeasurement
ParallelTime != Work != ProcessorCount
EnergyCost != function identity
Sample/query cost != local compute cost
Expected != worst-case != amortized != tail cost
OneScalarComplexity = rejected
```

Strong survivor:

```text
ComputationalResourceAndFeasibilityResponsibility
```

This remains one of the clearest independent sibling-level candidates.

Information gain: `VERY HIGH`.

---

# 4. Deeply explored space — Round C

## Representation / Semantics / Equivalence / Refinement

Round C attacked Program/Syntax/Type/Specification as universal primitives.

Key separations:

```text
ProgramText != AlgorithmIdentity
SyntaxDifference != SemanticDifference
RepresentationDifference != BehavioralDifference
SemanticPreservation != RepresentationIdentity
SemanticEquivalence != ResourceEquivalence
TypeSoundness != FullSpecificationCorrectness
Equivalence != Refinement != Simulation != Improvement
```

Strong survivor:

```text
ComputationalInterpretationAndSemanticRelationResponsibility
```

C overlaps A substantially, especially around behavior/observation semantics, but does not absorb A's boundary/continuation/environment structure.

C later became the primary owner for semantic state/representation identity used by J.

Information gain: `VERY HIGH`.

---

# 5. Deeply explored space — Round D

## Approximation / Numerical Error / Finite Precision / Validation

Round D attacked exactness as a hidden universal assumption.

It separated, among other things:

```text
mathematical target != machine representation
rounding error != model error != measurement error
precision != accuracy
accuracy != stability
stability != convergence
convergence != correctness
conditioning != algorithm stability
forward error != backward error
same nominal expression != same floating-point behavior
```

The Round D result was primarily cross-cutting rather than a clean sibling: approximation/error semantics connect C representation/semantics, B resource precision/iteration budgets, A stopping/continuation and later F probability.

D remains a strong validation/error layer.

Information gain: `VERY HIGH`.

---

# 6. Deeply explored space — Round F

## Probabilistic / Randomized Computation

The operator intentionally requested Round F; no missing Round E was fabricated.

Round F separated:

```text
internal random choice
random input
stochastic environment
nondeterministic/adversarial choice
epistemic uncertainty
numerical approximation error
```

Key results:

```text
RandomizedComputation != Hypercomputability
ObservedRandomizedRun != OutputDistribution
ProbabilisticChoice != NondeterministicChoice
ObjectiveRandomness != EpistemicIgnorance
FailureProbability != ApproximationErrorMagnitude
ExpectedBound != HighProbabilityBound != WorstCaseBound
RepeatedTrials != IndependentTrials
SamplingEntropy != AgentFailureProbability
```

Strong survivor:

```text
ComputationalStochasticityDistributionAndRiskResponsibility
```

Classification is cross-cutting: it refactors C toward distribution-valued semantics, extends B aggregation, composes with D and strengthens A's environment assumptions.

G later corrected provisional ownership of scheduler/adversary semantics: scheduler structure belongs primarily to G, while F owns probability/distribution/risk overlays.

Information gain: `VERY HIGH`.

---

# 7. Deeply explored space — Round G

## Concurrency / Distributed Coordination / Consistency / Impossibility

Round G separated:

```text
Concurrency != Parallelism
Parallelism != Coordination
SameFinalState != SameConcurrentCorrectness
Linearizability != Consistency != Serializability
Safety != Progress
Availability != Safety
LogicalClockOrder != CausalOrder
Crash != Byzantine != Partition
CAP != universal choose-two slogan
ObservedFailure != ImpossibilityTheorem
```

FLP and partial-synchrony pressure made model-relative solvability explicit.

Strong survivor:

```text
ComputationalCoordinationConsistencyAndProgressResponsibility
```

This remains one of the strongest sibling-level candidates because an irreducible bundle survives:

```text
multi-actor history/order
coordination safety specification
progress/liveness requirement
timing/synchrony assumptions
failure model
scheduler/fairness
coordination solvability context
```

Round I later moved generic solver-existence/impossibility theorem ownership upstream, while G retained coordination-specific task/model structure.

Information gain: `VERY HIGH`.

---

# 8. Deeply explored space — Round H

## Physical / Analog / Reversible / Quantum Realization

Round H directly attacked the long-standing anti-pancomputational grounding problem:

```text
What makes a physical process a computation
rather than arbitrary World dynamics
plus an observer-chosen mapping?
```

Key separations:

```text
PhysicalStateChange != ComputationalStateTransition
PostHocTrajectoryMapping != SufficientImplementation
ActualTraceMatch != CounterfactuallySupportedImplementation
StateEncoding != ComputationalRealization
LogicalReversibility != ZeroDissipation
ContinuousStateSpace != InfiniteUsablePrecision
QuantumSpeedup != Hypercomputability
Simulation != PhysicalSystemIdentity
HumanIntent != sufficient or necessary grounding by itself
```

Strong survivor:

```text
ComputationalPhysicalRealizationAndGroundingResponsibility
```

It requires at least abstract target, physical boundary, encoding/preparation, physical evolution, readout/decoding, counterfactual/domain support, fidelity/error, physical-model assumptions, resource references, validation evidence and miscomputation disposition.

This is another strong sibling-level candidate.

Physical Church-Turing remains a substantive unresolved thesis, not a definition.

Information gain: `VERY HIGH / ARCHITECTURALLY DECISIVE`.

---

# 9. Deeply explored space — Round I

## Computability / Decidability / Reducibility / Relative Power

Round I separated distinct notions of computational impossibility:

```text
undecidable
!= intractable
!= coordination-impossible
!= physically-unrealizable
!= empirically failed
```

Key results:

```text
PartialComputable != TotalComputable
Recognizable != Decidable
Enumerable != Decidable
Undecidable != EveryInstanceUnknown
Computable != Efficient
Reduction is directional and typed
ManyOneReducibility != TuringReducibility
OracleRelativeComputability != PhysicalRealizability
OneOracle != EndOfUndecidability
PerInstanceCorrectProgram != UniformComputability
```

Strong survivor:

```text
ComputationalEffectiveSolvabilityAndRelativePowerResponsibility
```

This is one of the strongest independent sibling-level candidates.

Important factorization correction:

```text
I owns generic solver-existence / effective solvability / impossibility theorem relation.
G owns coordination-specific computational model/specification that instantiates it.
```

Information gain: `VERY HIGH / ARCHITECTURALLY DECISIVE`.

---

# 10. Deeply explored space — Round J

## State / Memory / Persistence / Visibility / Reconstruction

Round J was the first major consolidation round.

Key separations:

```text
State != Memory != Storage != History
SameBytes != SameSemanticState
SameCurrentState != SameHistory
MemoryFootprint != AmountOfSemanticState
Address != ObjectIdentity
CacheCoherence != MemoryConsistency
Durable != Visible
Persistent != Immutable
LongLived != PersistentAcrossFailureBoundary
CheckpointArtifact != LiveState
ContinuationEquivalence != RuntimeProcessIdentity
Recovery != Rollback
```

Most of the apparent State/Memory continent reduced into existing responsibilities:

```text
state identity/representation        → C
shared visibility/order/consistency  → G
physical storage/nonvolatility       → H
memory/space/I/O cost                → B
continuation/environment boundary    → A
```

Narrower survivor:

```text
ComputationalStateRetentionAndReconstructionResponsibility
```

This is cross-cutting, not a clean independent sibling.

Information gain: `HIGH / CONSOLIDATING`.

---

# 11. Deeply explored space — Round K

## Information / Coding / Compression / Algorithmic Information

Round K resolved the last initially listed rival that had remained substantially open:

```text
M3 Computation = Information Transformation
= REJECTED AS UNIVERSAL DEFINITION
```

Key separations:

```text
ShannonInformation != SemanticMeaning
Entropy != object-intrinsic scalar without distribution
Compression != Computation
Redundancy != Waste
ChannelCapacity != MeasuredThroughput
MutualInformation != Causation or meaning
Lossless != Lossy compression
RequiredRate depends on distortion criterion
Description requirement depends on side information
KolmogorovComplexity != ShannonEntropy
CodecLength != KolmogorovComplexity
AlgorithmicRandomness != PhysicalRandomGeneration
InformationContent != ComputationalPower
TokenCount != SemanticInformation
```

Most apparent information ownership reduced into:

```text
meaning/representation          → C
resource bits/rates             → B
error/distortion                → D
probability/source model        → F
physical carriers/noise         → H
effective description model    → I
retention sufficiency           → J
actual transport                → Network
general theorems                → Mathematics
```

Narrower survivor:

```text
ComputationalInformationCodingAndRecoverabilityConstraintResponsibility
```

Again cross-cutting, not a clean sibling.

Information gain: `HIGH / CONSOLIDATING / RIVAL-RESOLVING`.

---

# 12. Current strongest provisional architecture

The first campaign does **not** justify a numbered foundation architecture yet, but the evidence currently factors most cleanly as follows.

## Strongest sibling-level candidates

```text
B — ComputationalResourceAndFeasibilityResponsibility

G — ComputationalCoordinationConsistencyAndProgressResponsibility

H — ComputationalPhysicalRealizationAndGroundingResponsibility

I — ComputationalEffectiveSolvabilityAndRelativePowerResponsibility
```

These four have survived the strongest independence/subtraction pressure so far.

## Cross-cutting / mutually refactoring responsibilities

```text
A — boundary / behavior / interaction / continuation / environment
C — interpretation / representation / semantic relations
D — approximation / error / validation
F — stochasticity / distribution / risk
J — state retention / reconstruction
K — information coding / recoverability constraints
```

Current provisional factorization:

```text
                         I
             effective solvability / power
                  /      |      \
                 G       B       H
          coordination resources realization
                 │       ▲       │
                 │       │ K     │
                 │   coding/info │
                 │   constraints │
                 └───┬───┴───┬───┘
                     ▼       ▼
                     C       J
                 semantics retention
                     ▲       │
                     └── A ◄─┘
                 behavior / continuation

D approximation/error and F probability/risk cross-cut relevant claims.
```

This diagram is **research history only**, not canonical CDF numbering.

---

# 13. Rival-model status after A–K

```text
M1 Function Evaluation
= REJECTED as universal definition
= retained as closed-function special regime

M2 Controlled State Transition
= PARTIAL / useful abstract pattern
= insufficient without boundary/semantics/grounding

M3 Information Transformation
= REJECTED as universal definition
= retained as analytic/coding constraint family

M4 Effective Procedure
= REJECTED as universal whole-Computing definition
= strongly reconstructed inside I effective-solvability claims

M5 Resource-Bounded Process
= REJECTED as universal definition
= strong independent B responsibility survives

M6 Interactive Process
= REJECTED as universal definition
= major A/G regime survives

M7 Physical Realization
= naive `computation = physical causal process` rejected
= strongly reconstructed as H robust realization/grounding relation
```

No original rival survives unchanged as `the essence of Computing`.

---

# 14. Spaces now deeply explored

The following spaces have received dedicated destructive treatment and should not be casually repeated:

```text
closed vs interactive/reactive computation
termination/continuation/environment assumptions
computational resource plurality and feasibility
representation/semantics/equivalence/refinement
numerical approximation/error/finite precision
probabilistic/randomized computation
probability vs nondeterminism/scheduler
concurrency/distributed coordination
consistency/safety/progress
synchrony/failure/model-relative impossibility
physical computation grounding
reversible/thermodynamic distinctions
analog/continuous/infinite-precision pressure
quantum computation vs hypercomputability
computability/decidability/recognition/enumeration
reducibility/oracle-relative power/uniformity
state vs memory/storage/history
persistence/checkpoint/recovery
memory consistency/coherence/visibility
information/entropy/coding/compression
rate-distortion/side information
algorithmic information/randomness
```

A future conversation should reopen these only when:

```text
- testing cross-factor architecture,
- applying a new regime that supplies genuine falsification pressure,
- or producing a concrete contradiction/reopen condition.
```

---

# 15. Spaces only partially explored / indirectly pressured

These spaces appear repeatedly but have **not** yet received their own full destructive tournament:

```text
algorithm design as a distinct semantic object
classical data structures beyond generic space/time/resource treatment
problem-specific lower-bound methodologies beyond B generic resource pluralism
online algorithms
competitive analysis
streaming algorithms and one-pass/sublinear-memory computation
external-memory/cache-oblivious structure beyond B pressure
real-time computation and deadlines
embedded/cyber-physical control computation
reactive synthesis / temporal specification beyond A/G pressure
learning/adaptation as computation after Human/Harness subtraction
nonuniform computation/advice beyond I pressure
proof systems / proof complexity / interactive proofs
cryptographic computation after Security subtraction
fault tolerance/error correction as a generic cross-layer responsibility
transactional atomicity beyond G/J examples
weak hardware/compiler memory models beyond J/G overview
quantum error correction / measurement-based computation / contextuality
continuous-time computation beyond H analog grounding
biological/molecular computation
neuromorphic computation
cellular automata / unconventional spatial computation as an independent regime
self-modifying computation
metacomputation / interpreters / reflective computation beyond C
program synthesis / synthesis-from-specification
formal verification / proof-carrying computation beyond C/I
```

These are **not canonical next steps**. They are only known partial-open areas.

---

# 16. Major still-unexplored or underexplored continents

The following remain large enough that Whole Computing closure cannot yet be claimed.

## U-A — Online / Streaming / Competitive Computation

Questions not yet destructively settled:

```text
Does irrevocable action under partial future information create a new foundation burden?
Is competitive ratio merely B resource/performance semantics or a distinct adversarial-information contract?
Does streaming/sublinear memory introduce a unique input-access/forgetting responsibility?
How do one-pass access and bounded memory interact with J/K/B/I?
```

## U-B — Real-Time / Embedded / Cyber-Physical Computation

Open pressure:

```text
correct value after deadline may be wrong
logical time vs physical time
hard/soft deadlines
schedulability vs ordinary resource complexity
control-loop stability vs computational correctness
sensor/actuator coupling across H/A/G/World
```

This space could falsify the current treatment of time as merely B/A/G/H references.

## U-C — Algorithms / Data Structures / Lower-Bound Structure

Round B established generic resource plurality, but not whether algorithm/data-structure structure contributes an independent burden involving:

```text
access models
query/update interfaces
preprocessing
adaptivity
amortization structure
cell-probe models
comparison/algebraic decision-tree models
fine-grained reductions
problem-specific lower bounds
space-time/query tradeoffs tied to representation structure
```

This may remain B/C/I, or expose a new structural axis.

## U-D — Biological / Molecular / Neuromorphic Computation

Still largely untested:

```text
chemical-reaction networks
DNA/molecular computing
neural/neuromorphic dynamics
population protocols
morphological computation
biological adaptation as computation
```

The key question is whether these only instantiate H + C/B/F/G or falsify current realization/semantics assumptions.

## U-E — Learning / Adaptation as Computation

Local PAL/Agent work exists, but a whole-referent destructive round has not yet separated:

```text
learning
optimization
adaptation
online updating
identification
memory
inference
control
```

against Human/Harness ownership.

## U-F — Proof / Verification / Synthesis / Meta-Computation

C and I touched semantics/specification/decidability, but not a dedicated cross-regime reconstruction of:

```text
proof objects
proof checking
proof search
program synthesis
model checking
interactive proof
proof complexity
reflection/self-interpretation
verified transformation
```

This could expose a new evidence/certification responsibility or reduce into C/I/B.

## U-G — Security/Cryptographic Computational Structure After Owner Subtraction

Security owns trust/adversarial compromise, but Computing may still have unexplored abstract burdens around:

```text
computational indistinguishability
one-wayness
reductions under adversarial computation
cryptographic hardness assumptions
zero knowledge
secure multiparty computation as computational relation
```

A careful owner-boundary search is still absent.

## U-H — Unconventional Spatial / Dynamical Regimes

Beyond H's grounding pass, there is not yet a dedicated tournament over:

```text
cellular automata
self-assembly
dynamical systems as computation
reservoir computing
reaction-diffusion computation
spatially embodied computation
self-modifying machines
```

These may be useful pressure on A/C/H.

---

# 17. What appears to be consolidating

The last two large rounds produced consolidation rather than new sibling expansion:

```text
J State/Memory
→ mostly C/G/H/B/A + narrow retention bridge

K Information/Coding
→ mostly C/B/D/F/H/I/J/Network/Mathematics + narrow coding bridge
```

This is the strongest current evidence that the search is moving from:

```text
continent discovery
```

toward:

```text
architecture consolidation / coverage-closure testing
```

But two rounds are not enough to claim whole-domain saturation because U-A through U-H still contain plausible orthogonal falsifiers.

---

# 18. Current stopping / continuation rule

The next conversation should **not** simply choose the next named CS field.

Instead, perform a fresh information-gain search over the remaining whole referent and ask:

```text
Which unexplored regime has the highest probability of:

1. falsifying B/G/H/I independence,
2. forcing A/C/D/F/J/K refactor,
3. exposing a missing owner boundary,
4. or revealing that remaining continents now mostly consolidate?
```

If several further large orthogonal continents also consolidate without adding or reopening a sibling-level burden, begin a formal whole-domain closure test.

---

# 19. Reopen discipline

Completed A–K research history should not be redone because a new conversation prefers another taxonomy.

A prior result may be reopened only by a concrete falsifier such as:

```text
- an explicit regime where a frozen anti-collapse law fails,
- a real counterexample to an owner-boundary claim,
- evidence that a supposedly cross-cutting responsibility is actually independent,
- or evidence that a supposedly independent candidate reduces into another owner/responsibility.
```

The reopen request should identify:

```text
which prior claim
which counterexample/regime
why the old distinction fails
```

---

# 20. New-conversation canonical state

The next conversation must begin from:

```text
WholeComputingSearchA-K
= completed research history

StrongSiblingCandidates
= {B, G, H, I}
= provisional only

CrossCuttingCandidates
= {A, C, D, F, J, K}
= provisional only

CDF0
= NOT ADMITTED

NumberedCDFCount
= 0

NextCDF
= UNKNOWN

NextComputingRoute
= UNKNOWN

WholeComputingClosure
= NOT CLAIMED
```

Do not turn `{B,G,H,I}` into numbered Foundations merely because they are currently strongest.
Do not treat U-A through U-H as a roadmap.

---

# 21. Recommended fresh-search procedure for the next conversation

The next conversation should first reconstruct the current unexplored-space map rather than immediately entering any candidate.

Suggested procedure:

```text
1. Read this closeout as the canonical research handoff.
2. Sample A–K artifacts only as needed; do not replay them.
3. Re-map the whole Computing referent:
   - deeply explored/frozen research history
   - partially explored/indirectly pressured
   - substantially unexplored
   - cross-owner regions
   - Agent-era newly salient regimes
4. Compare remaining continents by expected information gain / falsification value.
5. Select a next destructive tournament only after that comparison.
6. Keep CDF0 / NextCDF / NextComputingRoute UNKNOWN until evidence changes them.
```

---

# 22. New-conversation prompt

```text
继续 Ordivon Computing Deep Foundations，但不要预设下一轮研究对象，也不要创建 CDF0。

先读取：

1.
research/COMPUTING-DEEP-FOUNDATIONS-WHOLE-DOMAIN-A-K-CLOSEOUT-AND-OPEN-HANDOFF-20260818.md

如果需要核查某个具体结论，再按需读取 A–K 的对应 research artifacts / evidence；不要从头重做 A–K。

==================================================
当前 canonical 状态
==================================================

WholeComputingSearchA-K
= COMPLETED RESEARCH HISTORY

CDF0
= NOT ADMITTED

NumberedCDFCount
= 0

NextCDF
= UNKNOWN

NextComputingRoute
= UNKNOWN

WholeComputingClosure
= NOT CLAIMED

当前 provisional strong sibling-level candidates：

B — ComputationalResourceAndFeasibilityResponsibility
G — ComputationalCoordinationConsistencyAndProgressResponsibility
H — ComputationalPhysicalRealizationAndGroundingResponsibility
I — ComputationalEffectiveSolvabilityAndRelativePowerResponsibility

这些只是目前最强候选，不是 numbered Foundations，不得自动晋升。

当前主要 cross-cutting / mutually-refactoring responsibilities：

A — boundary / behavior / interaction / continuation / environment
C — interpretation / representation / semantic relations
D — approximation / error / validation
F — stochasticity / distribution / risk
J — state retention / reconstruction
K — information coding / recoverability constraints

==================================================
已经深度探索过的空间
==================================================

- closed function vs interactive/reactive behavior
- termination / continuation / environment assumptions
- resource plurality: time / space / I/O / communication / parallelism / energy / samples / queries / precision
- representation / semantics / equivalence / refinement
- numerical approximation / floating-point / error / stability / convergence
- probabilistic/randomized computation
- probability vs nondeterminism / scheduler / epistemic uncertainty
- concurrency / distributed coordination / consistency / safety / progress
- synchrony / failure models / model-relative distributed impossibility
- physical computation grounding / anti-pancomputationalism
- reversible vs thermodynamic computation
- analog/continuous/infinite-precision pressure
- quantum computation vs hypercomputability
- computability / decidability / recognizability / enumeration
- reductions / oracle-relative computation / uniformity
- state vs memory / storage / history
- persistence / checkpoint / recovery / durability / visibility
- cache coherence vs memory consistency
- Shannon information / entropy / mutual information
- coding / redundancy / channel capacity
- rate-distortion / side information
- Kolmogorov / algorithmic information and randomness

不要因为下一轮触及这些词就自动重做；只有出现具体 falsifier / reopen condition 才重开相应结论。

==================================================
部分探索但尚未完整 destructive test 的空间
==================================================

- algorithms as a distinct semantic object
- data structures beyond generic B resource analysis
- fine-grained / model-specific lower bounds
- online algorithms / competitive analysis
- streaming / sublinear-memory / one-pass computation
- real-time / embedded / cyber-physical computation
- reactive synthesis / temporal specification
- learning / adaptation after Human/Harness subtraction
- nonuniform advice beyond I pressure
- proof systems / proof complexity / interactive proofs
- program synthesis / model checking / verified transformations
- cryptographic computational structure after Security subtraction
- fault tolerance / generic error correction across layers
- transactional atomicity beyond G/J examples
- weak hardware/compiler memory models
- quantum error correction / measurement-based computation
- biological / molecular / neuromorphic computation
- cellular automata / self-assembly / reservoir / dynamical computation
- self-modifying / reflective / meta-computation

==================================================
大片仍未打开 / 信息量可能仍高的空间
==================================================

U-A Online / Streaming / Competitive Computation
U-B Real-Time / Embedded / Cyber-Physical Computation
U-C Algorithms / Data Structures / Problem-Specific Lower-Bound Structure
U-D Biological / Molecular / Neuromorphic Computation
U-E Learning / Adaptation as Computation
U-F Proof / Verification / Synthesis / Meta-Computation
U-G Cryptographic Computational Structure after Security-owner subtraction
U-H Unconventional Spatial / Dynamical Regimes

注意：这些只是 open-space map，不是 roadmap，也没有任何一项被 canonical 选为下一轮。

==================================================
本轮首先要做什么
==================================================

不要直接进入 U-A、U-B 或任何现成候选。

先从整个 Computing referent 重新做一次 fresh unexplored-space / information-gain search：

1. 明确哪些空间已经被 A–K 深度覆盖；
2. 明确哪些只是间接触及；
3. 主动寻找 closeout 没列出的未知大陆，不受 U-A→U-H 限制；
4. 对照前 Agent 时代主要理论体系、现代系统、非常规计算模型、跨学科边界与 Agent-era 扰动；
5. 继续做 Runtime / Harness / Network / World / Human / Security / Hardware / Mathematics / Media owner subtraction；
6. 比较剩余候选的 expected information gain，尤其优先那些可能 falsify 当前 B/G/H/I independence 或 A/C/D/F/J/K factorization 的空间；
7. 如果新的大型大陆开始连续只产生 reduction/consolidation，而不产生新的独立责任或 reopen condition，就开始评估 Whole Computing 是否接近 coverage closure；
8. 只有证据真正支持时才选择下一轮 destructive tournament。

不要把“剩余空间列表”继承成路线图。
不要为了编号而编号。
不要因为 B/G/H/I 当前最强就直接构建 Foundation architecture。

当前真正的问题是：

在 A–K 已经打开如此多空间以后，整个 Computing referent 还剩下哪些真正高信息量、可能改变当前 architecture 的未知大陆？
```

---

# 23. Closeout verdict

The first whole-domain Computing campaign has achieved **substantial architectural reconstruction**, but not whole-domain closure.

Evidence currently supports:

```text
- no single traditional definition captures all Computing;
- several independent responsibility axes exist;
- many traditional CS nouns are scoped constructs rather than ontology atoms;
- recent State/Memory and Information/Coding rounds consolidated rather than expanded the architecture;
- remaining unexplored continents are now best evaluated by falsification value rather than disciplinary completeness.
```

Final frontier:

```text
A–K research history   = CLOSED FOR THIS CAMPAIGN
WholeComputingClosure  = NOT CLAIMED
CDF0                   = NOT ADMITTED
NextCDF                = UNKNOWN
NextComputingRoute     = UNKNOWN
```
