---
schema_version: 1
id: computing.research.deep-foundations.round-b.resource-plurality-feasibility
title: Ordivon Computing Deep Foundations — Round B: Computational Resource Plurality / Cost / Feasibility
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Second destructive post-atlas Computing tournament. It attacks Resource = Time/Space and Resource = mere performance metadata across machine-independent complexity, time-space relations, I/O/data movement, communication complexity, parallel work/depth, physical energy, learning/sample/query resources and Agent-era budgets. The pass rejects a single universal resource scalar, wall-clock time, operation count, memory bytes, I/O, communication, energy, sample count and token count as universal complexity primitives. Round A's ComputationalBoundaryAndBehaviorResponsibility survives: behavior and cost are nonidentical. A second strong unnumbered candidate survives orthogonally—ComputationalResourceAndFeasibilityResponsibility—requiring a declared computational model, counted resource dimensions, units/accounting scope, scaling/reference family, aggregation/worst-average-amortized semantics, budget/bound/complexity claim and feasibility/optimality relation. Resource constraints can be semantically constitutive when the computational claim includes a bound, but they do not define all computation. No CDF0 is admitted.
evidence_status: strong-local
readiness: ROUND_B_COMPLETE_SECOND_STRONG_UNNUMBERED_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round B

## Computational Resource Plurality / Cost / Feasibility

## 0. Admission discipline

This round is **not CDF0**.

Round A established a strong unnumbered candidate:

```text
ComputationalBoundaryAndBehaviorResponsibility
```

but deliberately left M5 `ResourceBoundedProcess` nearly untested.

Round B asks:

```text
Are computational resources merely performance metadata attached after semantics?

or

Can resource assumptions/bounds be part of the computational claim itself?
```

The test spans:

```text
time
space
I/O / data movement
communication
parallel work/depth/processors
energy / erasure
samples
queries
precision / representation size
synchronization / rounds
Agent/model/tool budgets
```

No one resource receives priority by inheritance.

---

# 1. Classical pressure — complexity already starts by rejecting machine/run-time naïveté

## 1.1 Blum complexity measures

Blum's machine-independent complexity work begins from the fact that step counts depend on machine, program and coding, then develops general complexity-measure conditions broad enough to support machine-independent theorems.

The immediate lesson is not that one complexity measure is universal.

It is:

```text
ComplexityClaim
requires an explicit admissible measure/model.
```

## 1.2 Savitch and resource-specific simulation

Savitch's theorem studies storage required to simulate nondeterministic space-bounded computation deterministically.

The theorem itself is a warning against flattening:

```text
computational power / simulation relation
```

into one total resource number.

Space can be transformed differently from time and other costs.

---

# 2. First deletion — wall-clock time is not computational time by identity

## B-F1 — same abstract step count, different hardware speed

Run the same abstract algorithm/model on faster and slower physical hardware.

```text
same abstract transition count
!= same wall-clock duration.
```

Therefore:

```text
WallClockTime
!= ComputationalStepComplexityByIdentity.
```

Runtime/Hardware owns measured duration.
Computing owns only a declared abstract time/cost measure when making a complexity claim.

## B-F2 — same wall-clock time, different operation count

Parallel/vector/accelerated hardware can complete many operations in the same elapsed interval.

Therefore:

```text
SameWallClockDuration
!= SameComputationalWork.
```

---

# 3. Time is not the universal resource

## B-F3 — same function, time-space tradeoff

Algorithms/simulations can trade additional computation for reduced working memory, or additional memory for faster lookup/precomputation.

Therefore:

```text
TimeCost
!= SpaceCost
```

and neither scalar dominates the other universally.

## B-F4 — Savitch-style space relation

A nondeterministic space-bounded computation can be simulated deterministically with a polynomial increase in space while potentially changing time drastically.

Therefore:

```text
SpaceSimulationBound
!= TimeSimulationBoundByIdentity.
```

Complexity must remain resource-dimension-specific.

---

# 4. Operation count is not I/O cost

## B-F5 — Hong–Kung red/blue pebble model

Hong and Kung model data movement between fast and slow memory separately from arithmetic computation and prove I/O lower bounds for FFT, matrix multiplication and related computational DAGs.

Therefore:

```text
ArithmeticOperationCount
!= DataMovementCostByIdentity.
```

A computation can have an efficient arithmetic DAG yet remain communication/data-movement constrained.

## B-F6 — external-memory sorting

Aggarwal and Vitter give tight I/O bounds for sorting and related problems under a block-transfer external-memory model.

The abstract problem `sort records` remains the same while the dominant asymptotic resource changes under a memory-hierarchy model.

Therefore:

```text
AlgorithmicProblemIdentity
!= DominantResourceMetricByIdentity.
```

## B-F7 — memory hierarchy parameters matter

I/O complexity depends on model parameters such as fast-memory capacity, block size and available parallel transfer channels.

Therefore:

```text
IOMeasure
without resource-model parameters
= underspecified.
```

---

# 5. Communication is an independent abstract computational resource

## B-F8 — Yao communication complexity

Yao's two-party model asks how many bits two parties must exchange to compute a function when each initially knows only part of the input.

Local computation can be abstracted away while communication remains the quantity of interest.

Therefore:

```text
LocalComputationTime
!= CommunicationComplexityByIdentity.
```

## B-F9 — Network transport subtraction

Network owns whether messages are actually delivered, latency, routing, reachability and capacity.

Communication complexity instead asks an abstract lower-bound question such as:

```text
how many bits/messages/rounds must be exchanged under the declared information partition and protocol model?
```

Therefore:

```text
CommunicationComplexity
!= NetworkTrafficMeasurementByIdentity.
```

A Computing-owned burden survives Network subtraction.

## B-F10 — bits, messages and rounds are different

A protocol may reduce number of messages while increasing bits per message, or reduce total bits while increasing rounds.

Therefore:

```text
BitComplexity
!= MessageComplexity
!= RoundComplexity.
```

No single communication scalar is universal.

---

# 6. Parallel computation needs at least work/depth/resource-capacity separation

## B-F11 — Brent work/depth/processor tradeoff

Brent's parallel evaluation results relate total operations, parallel depth/time and available processor count.

Therefore:

```text
ParallelTime
!= TotalWork
!= ProcessorCount.
```

A parallel computation cannot be characterized by sequential operation count alone.

## B-F12 — same work, different span

Two dependency DAGs can contain the same number of operations while one has a long critical path and another exposes wide parallelism.

Therefore:

```text
SameWork
!= SameParallelDepth.
```

## B-F13 — unlimited-processor depth is not realizable runtime by identity

Theoretical span/depth under unlimited processors and actual time on `p` processors differ.

Therefore:

```text
AbstractParallelDepth
!= RuntimeElapsedTimeByIdentity.
```

Hardware/Runtime owns realized scheduling duration; Computing owns the abstract work/depth relation under the chosen model.

---

# 7. Energy is real, but does not collapse computation into physics

## B-F14 — Landauer logical irreversibility pressure

Landauer links logically irreversible operations/information erasure with a minimal physical heat cost under thermodynamic assumptions.

This shows:

```text
logical transformation structure
can constrain physical energy dissipation.
```

But it does **not** imply:

```text
EnergyCost
= universal abstract complexity measure.
```

## B-F15 — same abstract function, different reversible realization

A logically irreversible implementation and a reversible simulation can realize the same extensional function while having different information-erasure structure and physical cost profile.

Therefore:

```text
SameComputedFunction
!= SameEnergyCostByIdentity.
```

## B-F16 — physical energy belongs partly to World/Hardware

Actual joules, temperature, switching physics and device losses belong to physical/hardware owners.

Computing may own a model-relative claim such as:

```text
this abstract transformation requires/avoids a class of logically irreversible operations
```

without becoming the source of actual thermodynamic truth.

Therefore:

```text
ComputationalEnergyModel
!= PhysicalEnergyTruthStore.
```

---

# 8. Sample and query resources falsify time/space-only complexity

## B-F17 — Valiant learnability

Valiant's learnability framework makes information acquisition protocol and polynomially bounded learning steps central to computational learnability.

This pressures the view that only CPU steps and memory matter.

```text
SampleOrExampleAccess
can be a first-class computational resource.
```

## B-F18 — computation vs information acquisition

Two learners may have similar local compute but different access to examples, membership queries, labels or environment interactions.

Therefore:

```text
LocalComputeBudget
!= InformationAcquisitionBudgetByIdentity.
```

## B-F19 — query model changes feasible algorithm family

An oracle/query algorithm can count expensive queries while treating local computation differently.

Therefore:

```text
QueryComplexity
!= TimeComplexityByIdentity.
```

The oracle's real-world truth remains external; Computing owns only the declared query interface and count model.

---

# 9. Precision/representation size pressures unit-cost arithmetic

## B-F20 — arithmetic operation count hides operand size

Treating addition/multiplication as unit-cost regardless of operand bit length can assign the same operation count to computations with radically different representation sizes.

Therefore:

```text
ArithmeticOperationCount
!= BitComplexityByIdentity.
```

This round does not yet reconstruct numerical/finite-precision computation; it only preserves `precision / representation size` as a distinct resource dimension for the later numerical round.

## B-F21 — exact vs finite-precision resource model

An exact real/arbitrary-precision abstraction and a fixed-word finite-precision model can assign different feasibility/cost to the same mathematical specification.

Therefore:

```text
MathematicalOperationVocabulary
!= CompleteComputationalCostModel.
```

---

# 10. Resource metric is not computational behavior

## B-F22 — same behavior, different implementations/cost profiles

Two implementations can be behaviorally equivalent under Round A's declared observation semantics while one uses more time and less space than the other.

Therefore:

```text
BehavioralEquivalence
!= ResourceEquivalenceByIdentity.
```

Round A survives orthogonal attack.

## B-F23 — same resource bound, different behavior

Two programs can both run in linear time yet compute different functions/protocol behaviors.

Therefore:

```text
SameComplexityClass
!= SameComputationalBehavior.
```

Resource profile cannot replace behavior semantics.

---

# 11. But resource bounds can be part of the computational claim

## B-F24 — bounded feasibility

Consider:

```text
compute f(x)
```

versus:

```text
compute f(x) using O(log n) space
```

These are different claims even if they target the same extensional result.

Therefore:

```text
ResourceBound
can be semantically constitutive of a computational problem/claim.
```

This rejects the view that resources are always mere after-the-fact metadata.

## B-F25 — real-time/deadline preview

For a control/real-time query, producing the correct value after the relevant deadline may fail the declared computational contract.

Therefore:

```text
CorrectValue
!= SuccessfulBoundedComputationByIdentity.
```

The physical deadline truth belongs to Runtime/World, but Computing must be able to state that a resource bound is part of correctness/feasibility when the problem says so.

This is only a preview; real-time/cyber-physical computation remains a later continent.

---

# 12. Complexity is a relation, not a property of a function alone

## B-F26 — model dependence

The same task/function can receive different cost bounds under:

```text
single-tape TM
RAM/word model
external-memory model
parallel model
communication model
query model
reversible model.
```

Therefore:

```text
Complexity(Function)
```

without a computational/resource model is underspecified.

## B-F27 — algorithm/program dependence

Different algorithms for the same task can have different resource profiles.

Therefore:

```text
ProblemComplexity
!= ParticularAlgorithmCostByIdentity.
```

Problem complexity normally involves an optimum/lower bound over an admitted algorithm/model family.

## B-F28 — input-scaling dependence

A resource claim such as `O(n log n)` requires a declared size/scale function.

For graphs, numbers, compressed objects, streams or structured data, `n` is not metaphysically given.

Therefore:

```text
AsymptoticComplexity
requires a declared input/instance scaling measure.
```

---

# 13. Aggregation semantics are part of a cost claim

## B-F29 — worst vs average

An algorithm can have good expected/average behavior and poor worst-case behavior.

Therefore:

```text
AverageCost
!= WorstCaseCost.
```

## B-F30 — amortized vs per-operation

A data structure can have an expensive individual operation while maintaining a good amortized sequence cost.

Therefore:

```text
AmortizedCost
!= PerOperationWorstCaseCost.
```

## B-F31 — observed run vs complexity bound

A single fast execution does not prove a good asymptotic/worst-case complexity bound.

Therefore:

```text
ObservedRuntimeSample
!= ComplexityTheoremByIdentity.
```

Runtime evidence and Computing complexity claims must remain separate.

---

# 14. Optimization is multiobjective and partial-order-like

## B-F32 — Pareto tradeoff

Algorithm A:

```text
less time / more memory
```

Algorithm B:

```text
more time / less memory.
```

Without a declared objective/budget, neither is universally `better`.

Therefore:

```text
ResourceVectorA
and
ResourceVectorB
may be incomparable.
```

## B-F33 — weighted scalarization is policy, not ontology

A deployment can assign weights/prices to time, energy, communication or memory and produce one scalar score.

But changing weights can reverse the ranking.

Therefore:

```text
WeightedTotalCost
!= UniversalComputationalComplexityByIdentity.
```

---

# 15. Agent-era budgets are additional resource regimes, not new primitives

## B-F34 — token/context budget

Two Agent executions may target the same behavior but differ in:

```text
model tokens
context length
Tool calls
retrieval queries
wall time
GPU work
human review
```

Therefore:

```text
TokenCount
!= UniversalAgentComputationComplexity.
```

## B-F35 — Tool-call/query budget

An Agent can trade more local reasoning for fewer external Tool calls, or use more Tool calls to reduce internal inference burden.

Therefore:

```text
ModelCompute
!= ToolQueryCost.
```

This is a new practical regime, not a new Agent-era foundation primitive.

## B-F36 — Human attention is cross-owner

Human review/approval time may constrain a system workflow, but Human attention remains Human-owned.

Computing may model an admitted external resource budget/reference without owning human cognitive truth.

Therefore:

```text
ComputationalResourceModel
can reference owner-external scarce resources
without absorbing their ontology.
```

---

# 16. Strong surviving candidate — Computational Resource & Feasibility Responsibility

Round B rejects `Resource` as one substance and `Complexity` as one scalar.

A broader responsibility survives:

```text
ComputationalResourceAndFeasibilityResponsibility
```

A meaningful computational cost/feasibility claim needs enough of the following to be explicit:

## 16.1 Computational/problem target

```text
what behavior/problem/result is being costed?
```

This references Round A rather than duplicating it.

## 16.2 Computational model / admitted operation family

```text
what machine/protocol/oracle/memory/parallelism assumptions define legal computation?
```

## 16.3 Resource dimensions

Examples:

```text
time/steps
space/storage
I/O/data movement
communication bits/messages/rounds
work/depth/processors
energy/irreversibility model
samples/examples
queries
precision/bit length
synchronization
external admitted budget dimensions
```

No closed enumeration is frozen.

## 16.4 Units and accounting scope

```text
what counts as one unit?
which internal/external operations are charged or free?
```

## 16.5 Scale / instance-size semantics

```text
what parameter(s) define input/problem growth?
```

## 16.6 Aggregation semantics

```text
worst case
average/expected
distributional
amortized
per-instance
high-probability
```

## 16.7 Bound / budget / comparison claim

```text
upper bound
lower bound
tight bound
budget/admission constraint
optimality/Pareto relation
competitive/regret-like relation
```

Some later terms remain to be reconstructed in their own continents.

## 16.8 Feasibility/admissibility consequence

```text
Does exceeding the bound merely mean slower/more expensive,
or does it make the computational contract unsatisfied/infeasible?
```

---

# 17. Round A and Round B are orthogonal but coupled

Round A answers:

```text
What computational behavior is being claimed/observed?
```

Round B answers:

```text
Under what computational/resource model and budget is that behavior feasible/costed?
```

Neither absorbs the other.

```text
BehaviorWithoutResourceModel
can state semantics but not efficiency/feasibility.

ResourceModelWithoutBehaviorTarget
cannot say what is being computed.
```

Therefore:

```text
ComputationalBehavior
!= ComputationalCostProfile
```

but a complete bounded-computation claim may require both.

---

# 18. Why this is genuinely Computing-owned

## Runtime subtraction

Runtime can report:

```text
elapsed time
peak RSS
bytes transferred
job duration
actual Tool calls
```

but cannot infer a theorem-level statement such as:

```text
this algorithm is O(n log n)
this problem requires Ω(n log n) I/Os in model M
this protocol requires k bits under partition P
this implementation is asymptotically optimal.
```

Therefore:

```text
MeasuredResourceUsage
!= ComputationalComplexityClaim.
```

## Network subtraction

Network owns actual transport conditions.
Computing owns abstract communication cost/lower bounds under declared protocol/information assumptions.

## World/Hardware subtraction

World/Hardware owns actual energy, temperature, device physics and physical limits.
Computing may own abstract logical/reversible/resource models and their implications.

## Human subtraction

Human/sample/attention sources remain externally owned; Computing can count admitted interactions without asserting the underlying human truth.

---

# 19. Anti-collapse laws

```text
WallClockTime != AbstractStepComplexity
SameWallClock != SameWork
Time != Space
OperationCount != I/O
OperationCount != BitComplexity
LocalComputation != CommunicationComplexity
Bits != Messages != Rounds
Work != ParallelDepth != ProcessorCount
SameFunction != SameEnergyCost
ComputationalEnergyModel != PhysicalEnergyTruth
LocalComputeBudget != InformationAcquisitionBudget
QueryComplexity != TimeComplexity
BehavioralEquivalence != ResourceEquivalence
SameComplexityClass != SameBehavior
ResourceBound can be part of computational claim
Complexity(Function) without model = underspecified
ProblemComplexity != ParticularAlgorithmCost
AsymptoticComplexity requires scale semantics
Average != WorstCase
Amortized != PerOperationWorstCase
ObservedRuntime != ComplexityTheorem
Resource vectors can be incomparable
WeightedCost != UniversalComplexity
TokenCount != UniversalAgentComplexity
```

---

# 20. Candidate deletion results

Rejected as universal Computing foundation primitives:

```text
Time
WallClockTime
Space
MemoryBytes
OperationCount
I/O
CommunicationBits
Messages
Rounds
ParallelDepth
ProcessorCount
Energy
Samples
Queries
Precision
TokenCount
SingleScalarComplexity
```

All remain valid dimensions under declared models.

---

# 21. Rival-model update

## M1 Function evaluation

Still rejected as universal.
Resource analysis shows that identical extensional functions can have radically different feasible algorithm/resource profiles.

## M2 Controlled state transition

Still partial.
Transitions alone do not specify which resources are charged or how feasibility is evaluated.

## M3 Information transformation

Receives new pressure from communication/sample/query resources but remains unresolved; information quantity is not automatically total computational cost.

## M4 Effective procedure

Survives as a procedural notion but does not explain resource-relative feasibility by itself.

## M5 Resource-bounded process

```text
REJECT AS UNIVERSAL DEFINITION OF COMPUTATION
SURVIVES AS STRONG INDEPENDENT FOUNDATION BURDEN FOR COMPLEXITY/FEASIBILITY CLAIMS.
```

Unbounded computability questions remain meaningful, so resource bounds cannot define all computation.

## M6 Interactive process

Still a major regime but not universal. Round B adds communication/query/round/sample resources to interactive claims.

## M7 Physical realization

Strengthened as an unresolved pressure source because energy/precision/data movement expose physical assumptions, but actual physical truth remains World/Hardware-owned.

---

# 22. Round B verdict

```text
Resource = Time/Space only
= REJECTED

Resource = one universal scalar
= REJECTED

Resource = mere performance metadata in every case
= REJECTED

ResourceBound = universal essence of computation
= REJECTED
```

Strong surviving candidate:

```text
ComputationalResourceAndFeasibilityResponsibility
```

Current minimum burden:

```text
1. ComputationOrProblemTargetRef
2. ComputationalModelAndAdmittedOperations
3. ResourceDimensions
4. UnitsAndAccountingScope
5. ScaleOrInstanceSizeSemantics
6. AggregationSemantics
7. BoundBudgetOrComparisonClaim
8. FeasibilityOrAdmissibilityConsequence
```

Classification:

```text
STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE
ORTHOGONAL_TO_ROUND_A
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 23. Information gain

Round B information gain is **very high**.

It discovers that Computing currently lacks not one missing complexity theory but a generic **resource-claim grammar** capable of representing many incomparable regimes without flattening them.

This materially changes the candidate architecture:

```text
Round A:
ComputationalBoundaryAndBehaviorResponsibility

Round B:
ComputationalResourceAndFeasibilityResponsibility
```

The two may later become siblings inside a larger computational-claim foundation, but merging them now would be premature.

---

# 24. Orthogonal next pressure

Do not automatically continue `Complexity C`.

The strongest next falsifiers are:

```text
program/language semantics and representation equivalence
numerical/approximate/error semantics
physical/unconventional computation
probabilistic/randomized computation
concurrency/distributed correctness/impossibility
```

Especially important:

```text
Can PL semantics absorb Round A behavior identity?
Can approximation force Round A observation semantics and Round B resource semantics to merge through error/precision budgets?
Can physical realization falsify the current abstract model/resource split?
```

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 25. Primary-source pressure anchors

Used as pressure sources, not ontology authority:

- Manuel Blum, *A Machine-Independent Theory of the Complexity of Recursive Functions*, JACM 14(2), 1967.
- Walter J. Savitch, *Relationships between nondeterministic and deterministic tape complexities*, JCSS 4(2), 1970.
- Richard P. Brent, *The Parallel Evaluation of General Arithmetic Expressions*, JACM 21(2), 1974.
- Andrew C.-C. Yao, *Some Complexity Questions Related to Distributive Computing*, STOC 1979.
- Jia-Wei Hong and H. T. Kung, *I/O Complexity: The Red-Blue Pebble Game*, STOC 1981.
- Alok Aggarwal and Jeffrey S. Vitter, *The Input/Output Complexity of Sorting and Related Problems*, CACM 31(9), 1988.
- Rolf Landauer, *Irreversibility and Heat Generation in the Computing Process*, IBM Journal of Research and Development 5(3), 1961.
- Leslie G. Valiant, *A Theory of the Learnable*, Communications of the ACM 27(11), 1984.
