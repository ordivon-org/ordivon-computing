---
schema_version: 1
id: computing.research.deep-foundations.round-f.probabilistic-randomized-computation
title: Ordivon Computing Deep Foundations — Round F: Probabilistic / Randomized Computation
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Destructive tournament over probabilistic/randomized computation, intentionally numbered F without inventing a missing E. The pass separates internal randomization, probabilistic semantics, nondeterministic/adversarial choice, stochastic input/environment, epistemic uncertainty, approximation error and empirical uncertainty. Classical pressure from Gill probabilistic Turing machines, Yao randomized complexity, Solovay-Strassen Monte Carlo primality, Kozen probabilistic program semantics and Segala/Lynch probabilistic automata shows that randomness does not create hypercomputability, a single run is not a distribution, support is not probability, expectation is not a tail guarantee, Monte Carlo error differs from Las Vegas runtime randomness, one-sided and two-sided error differ, and probabilistic choice must remain separate from nondeterministic scheduling. Randomness can change complexity/feasibility and semantic output distributions while remaining a scoped computational regime rather than the essence of all computation. A strong cross-cutting candidate survives: ComputationalStochasticityDistributionAndRiskResponsibility. It refactors Round C toward distribution-valued semantics, Round B toward probabilistic resource aggregation/random-bit/query costs, Round D toward probabilistic validation/risk distinct from numerical error magnitude, and Round A environment assumptions where stochastic and adversarial inputs coexist. It is not an independent universal sibling and not CDF0.
evidence_status: strong-local
readiness: ROUND_F_COMPLETE_STRONG_CROSS_CUTTING_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round F

## Probabilistic / Randomized Computation

## 0. Numbering discipline

This artifact is intentionally `Round F` because the operator requested `继续f`.

No missing Round E is fabricated here.

Round F is not `CDF0`.

The prior live factorization is:

```text
A — computational boundary / interaction / continuation
B — computational resources / feasibility
C — representation / interpretation / semantic relation
D — approximation / numerical error / validation
```

Round F attacks all four through a different source of plurality:

```text
randomness
probability distributions
stochastic transitions
probabilistic correctness
expected/tail resource claims
randomized complexity
probabilistic verification
```

The target is not to celebrate `randomized algorithms` as a new ontology noun.

The target is to determine which semantic burdens survive after separating:

```text
random choice
nondeterministic/adversarial choice
stochastic environment/input
unknown deterministic state
epistemic uncertainty
numerical approximation error
probability of algorithmic failure
resource variability
```

---

# 1. Classical pressure already rejects `randomness = hypercomputability`

John Gill's 1977 probabilistic Turing-machine analysis gives the machine unbiased coin-toss choices and defines probabilistic computation/complexity classes. Under his stated majority-output definition, probabilistic computability still yields only partial recursive functions.

Therefore:

```text
RandomizedComputation
!= HypercomputabilityByIdentity.
```

Randomness can alter:

```text
complexity
success probability
behavior distribution
resource distribution
```

without automatically enlarging classical computability.

This is a central anti-collapse law for Round F.

---

# 2. Candidate deletion — randomization is not universal computation

## F-F1 — deterministic exact algorithm

A deterministic sorting, parsing, hashing or arithmetic routine can compute correctly without any random choices.

Therefore:

```text
RandomChoice
!= necessary condition for Computation.
```

`ProbabilisticComputation` is a regime, not the universal essence.

## F-F2 — deterministic behavior with stochastic input

A deterministic program may receive a random sample supplied by an external environment.

Therefore:

```text
RandomInput
!= InternalRandomizedAlgorithmByIdentity.
```

## F-F3 — internal randomness with deterministic input

A randomized algorithm can receive a fixed deterministic input and still generate a distribution over runs/results because of internal random choices.

Therefore:

```text
StochasticInput
!= necessary for RandomizedComputation.
```

---

# 3. Random source, random variable, seed and output distribution are different

## F-F4 — fixed seed collapses implementation run variability

For many pseudorandom implementations, fixing program, input, seed and deterministic execution regime fixes the generated pseudorandom sequence.

Therefore:

```text
SeedValue
!= RandomnessDistributionByIdentity.
```

A seed identifies one realization/trajectory; the randomized-algorithm claim usually quantifies over a seed/randomness distribution.

## F-F5 — same seed space, different seed distribution

Uniformly selecting seeds versus heavily biasing one seed can produce different output probabilities despite identical seed support.

Therefore:

```text
SeedSupport
!= SeedDistribution.
```

## F-F6 — same random source, different transformation

The same stream of random bits can be mapped through different algorithms to different output distributions.

Therefore:

```text
RandomSourceDistribution
!= OutputDistributionByIdentity.
```

---

# 4. Support is not distribution

## F-F7 — same possible outputs, different probabilities

System A outputs:

```text
0 with 0.99
1 with 0.01
```

System B outputs:

```text
0 with 0.50
1 with 0.50
```

Both have support `{0,1}`.

Therefore:

```text
SameOutcomeSupport
!= SameProbabilisticSemantics.
```

Round C cannot represent probabilistic behavior using only possible-trace/result sets if probability mass matters to the claim.

---

# 5. A single run is not the probabilistic semantics

## F-F8 — one observed output

A single randomized run yields one realized trajectory/result.

That observation does not identify the full algorithmic distribution.

Therefore:

```text
ObservedRandomizedRun
!= OutputDistributionByIdentity.
```

## F-F9 — repeated empirical frequency is evidence, not theorem

An observed empirical frequency from finitely many trials may estimate a probability, but is not identical to the exact/model-level probability claim.

Therefore:

```text
EmpiricalFrequency
!= DeclaredOrProvedProbabilityByIdentity.
```

Runtime/evidence owners and Computing probabilistic semantics must remain distinct.

---

# 6. Probabilistic program semantics is richer than `most likely output`

Dexter Kozen's 1981 semantics gives probabilistic programs mathematically explicit probabilistic meanings, including measure/operator-based formulations.

## F-F10 — distribution-valued behavior

A probabilistic program's meaning can be a distribution/measure over possible outcomes rather than one representative output.

Therefore:

```text
ProbabilisticProgramMeaning
!= MostLikelyOutputByIdentity.
```

## F-F11 — expected value is not the whole distribution

Two distributions can have identical expectation while differing in variance and tail probabilities.

Therefore:

```text
SameExpectedOutput
!= SameOutputDistribution.
```

## F-F12 — probability mass can be semantically material

If one implementation returns an unsafe outcome with probability `10^-3` and another with probability `10^-12`, set-of-possible-outcomes semantics alone cannot distinguish their risk.

Therefore:

```text
PossibleOutcomeSet
!= CompleteProbabilisticBehaviorSemantics.
```

---

# 7. Randomness and nondeterminism must not collapse

Probabilistic automata work by Segala/Lynch explicitly models systems with both probabilistic and nondeterministic behavior, and uses schedulers/adversaries/strategies to resolve nondeterministic choices.

## F-F13 — same branching support, probability vs nondeterminism

A probabilistic choice:

```text
A with probability 1/2
B with probability 1/2
```

is not the same semantic object as an unresolved nondeterministic choice between `A` and `B`.

Therefore:

```text
ProbabilisticChoice
!= NondeterministicChoiceByIdentity.
```

## F-F14 — scheduler/adversary is not random source

A scheduler may resolve nondeterministic choices based on history while probabilistic transitions remain governed by declared distributions.

Therefore:

```text
SchedulerOrAdversary
!= RandomSourceByIdentity.
```

## F-F15 — probability after scheduler resolution is scheduler-relative

When probabilistic and nondeterministic choices coexist, event probabilities can depend on which scheduler/adversary policy is admitted.

Therefore:

```text
ProbabilityClaim
without scheduler/adversary semantics where material
= underspecified.
```

This is a major future pressure for concurrency/distributed rounds.

---

# 8. Randomness is not epistemic uncertainty

## F-F16 — known randomized mechanism

A program may intentionally flip a fair coin while the analyst knows the mechanism/distribution exactly.

Therefore:

```text
ObjectiveModelRandomness
!= EpistemicIgnoranceByIdentity.
```

## F-F17 — unknown deterministic state

An observer may be uncertain about a deterministic hidden state even when the computation has no random choice.

Therefore:

```text
EpistemicUncertainty
!= ComputationalRandomnessByIdentity.
```

This strengthens Round A's earlier:

```text
ObserverUncertainty != ComputationalNondeterminism.
```

Round F adds:

```text
ObserverUncertainty != ComputationalRandomness.
```

---

# 9. Internal randomness is not a stochastic environment

## F-F18 — fixed algorithm, random environment events

A deterministic controller/service interacting with arrivals sampled from a stochastic environment can have random observed trajectories.

Therefore:

```text
RandomObservedTrajectory
!= InternalRandomizedAlgorithmByIdentity.
```

## F-F19 — internal randomness plus adversarial environment

A randomized algorithm can intentionally randomize against an adversarially selected input/request sequence.

Therefore:

```text
InternalRandomness
and
EnvironmentUncertaintyOrAdversary
```

must be separately modeled.

Round A's `EnvironmentAssumptions` survives and becomes more typed.

---

# 10. Monte Carlo correctness and numerical approximation error are different

Solovay-Strassen gives a sharp pressure case: for the described primality test, prime inputs are not falsely rejected under the stated test, while composite inputs can be incorrectly accepted with bounded probability; independent repetition reduces that probability.

## F-F20 — one-sided algorithmic error

A randomized decision procedure may be exact on one class of inputs and probabilistically wrong on another.

Therefore:

```text
ProbabilityOfDecisionError
!= NumericalErrorMagnitudeByIdentity.
```

The output can be a discrete exact label that is either correct or wrong.

## F-F21 — two algorithms can have same error probability but different error magnitude

For estimation problems, Algorithm A and B may both fail with probability `0.01` but have very different discrepancy when failure occurs.

Therefore:

```text
FailureProbability
!= ErrorMagnitudeDistribution.
```

## F-F22 — approximate value can be always within tolerance

A deterministic approximation algorithm can always satisfy a metric tolerance without any algorithmic failure probability.

Therefore:

```text
Approximation
!= ProbabilisticErrorByIdentity.
```

Round D and Round F cannot be collapsed.

---

# 11. One-sided error and two-sided error are distinct

## F-F23 — asymmetric false-positive/false-negative regimes

A randomized decision algorithm may guarantee:

```text
one class always correct
other class bounded-error
```

while another permits error on both classes.

Therefore:

```text
OneSidedError
!= TwoSidedErrorByIdentity.
```

A generic `error_probability` field is insufficient when direction/class matters.

---

# 12. Monte Carlo and Las Vegas separate correctness from runtime randomness

Randomized-algorithm literature distinguishes regimes where correctness may be probabilistic from regimes where returned answers are correct but runtime/successful termination is random. Contemporary algorithm papers still use the Las Vegas/Monte Carlo distinction explicitly.

## F-F24 — random runtime, exact returned answer

A Las Vegas-style algorithm can always return a correct answer when it returns, while randomization affects time/attempt count.

Therefore:

```text
RandomizedRuntime
!= ProbabilisticCorrectnessByIdentity.
```

## F-F25 — bounded runtime, probabilistic result correctness

A Monte Carlo-style algorithm can enforce a fixed/bounded computational budget while tolerating a declared failure probability.

Therefore:

```text
BoundedRuntime
!= DeterministicCorrectnessByIdentity.
```

Round B and Round F interact without collapsing.

---

# 13. Amplification is a resource-risk tradeoff

Solovay-Strassen explicitly shows independent repetition `m` times reduces the one-sided error bound exponentially while arithmetic cost grows with `m`.

## F-F26 — repetition changes both risk and resource profile

Therefore:

```text
Amplification
couples
FailureProbability
with
ComputationalResourceCost.
```

But:

```text
RiskProfile
!= ResourceProfileByIdentity.
```

## F-F27 — amplification is not free correctness

Increasing repetitions can reduce declared error probability while consuming more time/random bits/queries.

Therefore:

```text
LowerFailureProbability
!= SameResourceClaim.
```

## F-F28 — independence assumption is material

The familiar multiplication of independent per-trial failure probabilities relies on independence or another explicitly justified dependence bound.

Therefore:

```text
RepeatedTrials
!= IndependentTrialsByIdentity.
```

and:

```text
AmplifiedErrorBound
requires declared dependence assumptions.
```

---

# 14. Expectation is not a tail guarantee

## F-F29 — same expected runtime, different tail

Two runtime distributions can have the same expected time but radically different probability of very long runs.

Therefore:

```text
SameExpectedRuntime
!= SameRuntimeRiskProfile.
```

## F-F30 — expected polynomial does not imply bounded worst-case instance runtime

An algorithm with good expected runtime can still have rare long trajectories unless a stronger tail/worst-case claim is proved.

Therefore:

```text
ExpectedResourceBound
!= HighProbabilityBound
!= WorstCaseBound.
```

Round B's aggregation semantics must explicitly support probabilistic distributions/tails.

## F-F31 — expected output is not correctness probability

An estimator can be unbiased in expectation yet have high variance and poor per-run accuracy.

Therefore:

```text
UnbiasedExpectation
!= HighProbabilityAccuracyByIdentity.
```

---

# 15. Bias, variance and tail risk are different

## F-F32 — unbiased high-variance estimator

An estimator can satisfy:

```text
E[X_hat] = X
```

while individual samples are often far from `X`.

Therefore:

```text
Unbiased
!= AccuratePerRunByIdentity.
```

## F-F33 — biased low-variance estimator

A biased estimator can cluster tightly around a slightly shifted value.

Therefore:

```text
LowVariance
!= UnbiasedByIdentity.
```

## F-F34 — variance does not uniquely determine tail risk

Distributions with similar variance can have different tail structure.

Therefore:

```text
Variance
!= CompleteRiskProfileByIdentity.
```

No single uncertainty scalar survives.

---

# 16. Input distributions and internal randomization must separate

Yao's probabilistic-computation/minimax line relates randomized algorithm performance to deterministic algorithms under input distributions. The relationship itself depends on distinguishing two distributions:

```text
algorithm's internal random choice
vs
input-instance distribution.
```

## F-F35 — average-case input distribution is not internal randomness

A deterministic algorithm can have an expected cost under a random input distribution.

Therefore:

```text
ExpectedCostOverInputs
!= ExpectedCostOverInternalRandomnessByIdentity.
```

## F-F36 — randomized worst-case analysis and distributional deterministic analysis are related but nonidentical claims

Therefore:

```text
InternalRandomization
!= RandomInputDistribution.
```

A complete probabilistic complexity claim must identify which probability space each expectation/risk quantifies over.

---

# 17. Probability space and conditioning context are part of the claim

## F-F37 — conditional probability changes under observed information

A probability claim before observing an event can differ from the corresponding conditional probability after evidence/context is incorporated.

Therefore:

```text
ProbabilityValue
without event/conditioning semantics
= underspecified.
```

Computing does not thereby own general epistemology/statistics; it must at least identify the probability space relevant to computational semantics.

## F-F38 — probability over outputs vs probability over runtime

One computation can have:

```text
output distribution
runtime distribution
resource distribution
failure-event distribution
```

These need not be identical or induced by the same projection.

Therefore:

```text
OneProbabilityDistributionForComputation
= REJECTED.
```

---

# 18. Random bits can be a resource without defining semantics alone

## F-F39 — same output distribution, different random-bit consumption

Two implementations can realize the same output distribution while consuming different expected/worst random-bit counts.

Therefore:

```text
DistributionalSemanticEquivalence
!= RandomBitResourceEquivalence.
```

Round B survives.

## F-F40 — same random-bit budget, different output semantics

Two algorithms can consume the same number of random bits while computing unrelated tasks/distributions.

Therefore:

```text
RandomBitComplexity
!= ComputationalBehaviorIdentity.
```

---

# 19. Pseudorandom realization does not make abstract randomness disappear

## F-F41 — deterministic generator from seed

A pseudorandom generator is deterministic conditional on its seed, while a higher-level algorithm may model the seed as sampled from a declared distribution and reason about induced behavior.

Therefore:

```text
DeterministicRealizationGivenSeed
!= AbsenceOfRandomizedAlgorithmSemantics.
```

## F-F42 — physical entropy is owner-external

Actual entropy generation, device noise and hardware random-number source truth belong to Hardware/World/Security owners.

Computing may specify an ideal/random-bit source assumption without claiming the physical source actually satisfies it.

Therefore:

```text
AbstractRandomSourceModel
!= PhysicalEntropyTruthStore.
```

---

# 20. Reproducibility and distributional correctness separate

## F-F43 — fixed seed reproducibility

Fixing seed may reproduce one trajectory exactly.

This does not prove the algorithm has the declared probability distribution over seeds/runs in production.

Therefore:

```text
SeededReplayReproducibility
!= DistributionalCorrectnessByIdentity.
```

## F-F44 — different seeds can both be semantically valid

Bitwise-identical output is not a universal correctness requirement for randomized computation.

Therefore:

```text
BitwiseReproducibility
!= RandomizedCorrectnessRequirementByNecessity.
```

Round D's reproducibility separation generalizes beyond floating point.

---

# 21. Probabilistic refinement/equivalence is richer than exact behavior equality

## F-F45 — equal support but different probability mass

Already established:

```text
same support != same distribution.
```

Therefore Round C's semantic comparison relation must support probability-sensitive comparison where material.

## F-F46 — probability thresholds are property semantics

A specification may require:

```text
P[failure] <= 10^-9
```

or:

```text
P[safety violation before T] <= epsilon.
```

Therefore:

```text
ProbabilisticPropertySatisfaction
!= ExactTraceSetInclusionByIdentity.
```

## F-F47 — probabilistic simulation under nondeterminism needs scheduler assumptions

Segala/Lynch-style probabilistic-process models show that probabilistic refinement/equivalence must handle both distributions and nondeterministic resolutions where both coexist.

Therefore:

```text
ProbabilisticRefinement
cannot be reduced to one unconditional output distribution
in all concurrent regimes.
```

---

# 22. Agent-era sampling does not create a new randomness ontology

## F-F48 — same model, different decoding policy

Hold model weights/context fixed; vary deterministic decoding versus sampling/temperature/top-p style policies.

Observed output variability changes.

Therefore:

```text
ModelIdentity
!= SamplingPolicyIdentity.
```

## F-F49 — sampling variability is not model epistemic uncertainty

A model can sample diverse outputs even when the sampling distribution is perfectly specified; conversely deterministic decoding can still be wrong/uncertain about the world.

Therefore:

```text
SamplingRandomness
!= EpistemicUncertaintyByIdentity.
```

## F-F50 — token-level randomness is not total Agent risk

Agent failure risk can come from model error, Tool/environment changes, nondeterministic external systems, approximate computation and policy choices in addition to sampling.

Therefore:

```text
SamplingEntropy
!= AgentFailureProbabilityByIdentity.
```

No Agent-specific stochasticity primitive is required.

---

# 23. Owner subtraction

## Runtime

Runtime owns actual run/seed/configuration/output/timing evidence.

It can report:

```text
seed S used
run produced Y
elapsed T
```

but one run cannot establish model-level probability/expected-complexity claims.

Therefore:

```text
ObservedRun
!= ProbabilisticAlgorithmTheorem.
```

## World / domain

World/domain owners retain actual stochastic physical/domain processes and measurement truth.

Computing owns only the admitted stochastic input/environment model used by a computational claim.

## Hardware / Security

Hardware/Security own physical entropy source, cryptographic trust and compromise properties.

Computing may consume an abstract random-bit/pseudorandom assumption.

## Human

Human belief/confidence/subjective uncertainty remains Human/epistemic owner territory unless explicitly encoded as an admitted computational probability model.

## Network

Network owns actual random packet loss/delay/transport behavior; Computing may analyze algorithms under declared stochastic/network-adversarial models without taking ownership of transport truth.

---

# 24. Round A relation — environment assumptions become typed

Round A survives.

Round F sharpens its `EnvironmentAssumptions` and `InteractionInterface` burden:

```text
internal random source
stochastic external input
deterministic but unknown environment
nondeterministic/adversarial scheduler
```

must not be merged.

Key laws:

```text
RandomObservedTrajectory != InternalRandomizedAlgorithm
InternalRandomness != EnvironmentAdversary
ProbabilityUnderScheduler != UnconditionalProbabilityByNecessity
```

Round A therefore gains typed source-of-branching semantics.

---

# 25. Round B relation — probability enters resource aggregation, not resource essence

Round B already has:

```text
AggregationSemantics
```

Round F proves this field must support at least:

```text
expectation
worst case
high probability
tail quantile
conditional expectation
random-bit/sample/query distributions
```

But:

```text
ExpectedCost != HighProbabilityCost != WorstCaseCost
```

and:

```text
DistributionalSemanticEquivalence
!= ResourceDistributionEquivalence.
```

Round B remains independent.

---

# 26. Round C relation — semantics must support probability distributions and stochastic relations

Round C is refactored again.

Its `SemanticInterpretationRelation` cannot assume a deterministic behavior object.

It may need to map representations/models into:

```text
distributions/measures over outputs
stochastic transition kernels
probabilistic traces
sets/families of distributions under nondeterminism
```

Likewise `SemanticComparisonOrApproximationRelation` must support probability-sensitive refinement/equivalence/property comparison.

Therefore:

```text
DeterministicSemanticObject
!= UniversalSemanticCodomain.
```

---

# 27. Round D relation — probabilistic risk is not numerical error magnitude

Round D remains distinct.

Round F adds a different validation axis:

```text
probability the returned answer violates the property
```

versus D's:

```text
magnitude/type of discrepancy from a reference target
```

Therefore:

```text
FailureProbability
!= ApproximationErrorMagnitude.
```

However combined claims are legitimate:

```text
P[relative error <= epsilon] >= 1 - delta.
```

This requires both:

```text
D: error metric/tolerance
F: probability/risk semantics.
```

So F cross-cuts and composes with D rather than absorbing it.

---

# 28. Strong surviving candidate — Computational Stochasticity / Distribution / Risk Responsibility

Round F rejects `Randomness` and `Probability` as one primitive.

A broad cross-cutting responsibility survives:

```text
ComputationalStochasticityDistributionAndRiskResponsibility
```

Minimum current burden:

## 28.1 Randomness / stochastic-source role

```text
internal random choice?
random seed?
stochastic external input?
probabilistic transition?
```

Typed role matters.

## 28.2 Probability-space / source distribution semantics

```text
what events/outcomes are assigned probability under what declared source/model?
```

## 28.3 Distributional semantic target

```text
output distribution?
trace distribution?
runtime/resource distribution?
joint distribution over several observables?
```

## 28.4 Nondeterministic / adversarial resolution semantics when co-present

```text
scheduler/adversary/strategy family
```

must be separate from random choice.

## 28.5 Independence / dependence / coupling assumptions

Required for repetition/amplification/composition where probability bounds depend on them.

## 28.6 Probabilistic correctness / risk property

Examples:

```text
one-sided error
two-sided error
failure probability
safety probability
tail event
```

No closed enumeration.

## 28.7 Distributional summary / aggregation semantics

Examples:

```text
expectation
variance
quantile
tail probability
high-probability bound
```

No one summary is universal.

## 28.8 Resource/randomness accounting relation

```text
random bits
samples
queries
expected runtime
high-probability runtime
repetition count
```

references Round B rather than duplicating it.

## 28.9 Amplification / composition relation

```text
how repeated/combined randomized procedures transform failure/resource guarantees
under declared dependence assumptions.
```

## 28.10 Evidence / certification / acceptance consequence

```text
proved probability bound?
empirical estimate?
confidence statement?
accepted threshold?
unresolved?
```

Evidence type and semantic guarantee must remain separate.

---

# 29. Why F is not a fourth independent universal sibling

Like D, F is strongly cross-cutting:

```text
probability-valued semantics
→ Round C

expected/tail/random-bit/sample/query resources
→ Round B

failure/acceptance risk
→ Round D validation layer

source/adversary/environment distinction
→ Round A
```

Therefore F currently classifies as:

```text
STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE
REFACTORS_ROUND_C
EXTENDS_ROUND_B_AGGREGATION
COMPOSES_WITH_ROUND_D_VALIDATION
STRENGTHENS_ROUND_A_ENVIRONMENT_ASSUMPTIONS
NOT_INDEPENDENT_UNIVERSAL_ESSENCE
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 30. Candidate deletion results

Rejected as universal primitives/scalars:

```text
Randomness
RandomSeed
RandomBit
Probability
ExpectedValue
Variance
FailureProbability
Confidence
MonteCarlo
LasVegas
RandomizedAlgorithm
OutputDistribution
Scheduler
SamplingEntropy
```

All remain useful scoped terms under explicit semantic roles.

---

# 31. Anti-collapse laws

```text
RandomChoice != necessary for Computation
RandomInput != InternalRandomizedAlgorithm
StochasticInput != necessary for RandomizedComputation
SeedValue != RandomnessDistribution
SeedSupport != SeedDistribution
RandomSourceDistribution != OutputDistribution
SameOutcomeSupport != SameProbabilisticSemantics
ObservedRandomizedRun != OutputDistribution
EmpiricalFrequency != DeclaredOrProvedProbability
ProbabilisticProgramMeaning != MostLikelyOutput
SameExpectedOutput != SameOutputDistribution
PossibleOutcomeSet != CompleteProbabilisticBehaviorSemantics
ProbabilisticChoice != NondeterministicChoice
SchedulerOrAdversary != RandomSource
ProbabilityWithoutSchedulerSemanticsCanBeUnderspecified
ObjectiveModelRandomness != EpistemicIgnorance
EpistemicUncertainty != ComputationalRandomness
RandomObservedTrajectory != InternalRandomizedAlgorithm
InternalRandomness != EnvironmentAdversary
ProbabilityOfDecisionError != NumericalErrorMagnitude
FailureProbability != ErrorMagnitudeDistribution
Approximation != ProbabilisticError
OneSidedError != TwoSidedError
RandomizedRuntime != ProbabilisticCorrectness
BoundedRuntime != DeterministicCorrectness
RiskProfile != ResourceProfile
RepeatedTrials != IndependentTrials
SameExpectedRuntime != SameRuntimeRiskProfile
ExpectedResourceBound != HighProbabilityBound != WorstCaseBound
UnbiasedExpectation != HighProbabilityAccuracy
Unbiased != AccuratePerRun
LowVariance != Unbiased
Variance != CompleteRiskProfile
ExpectedCostOverInputs != ExpectedCostOverInternalRandomness
InternalRandomization != RandomInputDistribution
OneProbabilityDistributionForComputation = rejected
DistributionalSemanticEquivalence != RandomBitResourceEquivalence
DeterministicRealizationGivenSeed != AbsenceOfRandomizedSemantics
AbstractRandomSourceModel != PhysicalEntropyTruth
SeededReplayReproducibility != DistributionalCorrectness
BitwiseReproducibility != RandomizedCorrectnessRequirement
ProbabilisticPropertySatisfaction != ExactTraceSetInclusion
ObservedRun != ProbabilisticAlgorithmTheorem
FailureProbability != ApproximationErrorMagnitude
SamplingRandomness != EpistemicUncertainty
SamplingEntropy != AgentFailureProbability
RandomizedComputation != Hypercomputability
```

---

# 32. Rival-model update

## M1 Function evaluation

Still not universal. A randomized computation may denote a distribution over values rather than one value.

## M2 Controlled state transition

Strengthened only if transition relations can be probabilistic and distinct from nondeterministic/adversarial transitions.

## M3 Information transformation

Pressure increases: random bits/information uncertainty clearly matter, but probability semantics does not automatically reduce to information quantity. M3 remains unresolved.

## M4 Effective procedure

Randomized effective procedures remain procedures, but the procedure alone does not specify risk/distribution semantics unless the random-source model is included.

## M5 Resource-bounded process

Round B survives. Random bits, expected runtime and tail resource bounds add dimensions/aggregation, not a universal resource essence.

## M6 Interactive process

Probabilistic interactive/concurrent systems strengthen the need for typed environment/scheduler/random-source assumptions, but interaction remains non-universal.

## M7 Physical realization

Physical randomness/entropy remains an owner-external realization question. Abstract probabilistic semantics can be specified independently of whether the source is physical entropy, pseudorandomness or another admitted realization. The grounding problem remains open.

---

# 33. Current A/B/C/D/F factorization

```text
A — Boundary / interaction / continuation / environment assumptions
    ↑ F types random vs adversarial vs stochastic-environment branching

C — Interpretation / semantics / comparison
    ↑ F generalizes semantic codomain to distributions/stochastic relations
    ↑ D generalizes exact relation to approximation/error/enclosure

B — Resource / feasibility
    ↑ F adds random-bit/sample/query and expected/tail aggregation
    ↑ D couples precision/iteration resources to approximation behavior

D — Approximation / error / validation
    ↔ F separates metric error magnitude from probability of violation

F — Stochasticity / distribution / risk
    = cross-cutting grammar over A/B/C/D
```

The architecture is increasingly a factorized grammar of computational claims rather than a flat taxonomy of computing subfields.

---

# 34. Agent-era result

Agent systems add practical probability surfaces:

```text
sampling/temperature/top-p
tool/environment stochasticity
model uncertainty estimates
randomized search
ensemble methods
probabilistic retrieval/ranking
```

but Round F finds no Agent-specific randomness primitive.

Critical separation:

```text
SamplingRandomness
!= ModelEpistemicUncertainty
!= EnvironmentUncertainty
!= ToolNondeterminism
!= AgentFailureProbability.
```

Agent-era systems mainly make source-of-variation provenance more important.

---

# 35. Round F verdict

```text
Randomness as universal essence of computation
= REJECTED

Randomized computation as hypercomputability
= REJECTED

Probability as one scalar
= REJECTED

Expected value as complete distributional semantics
= REJECTED

Probability = nondeterminism
= REJECTED

Randomness = uncertainty
= REJECTED

Failure probability = numerical approximation error
= REJECTED

Expected resource bound = tail/worst-case guarantee
= REJECTED
```

Strong survivor:

```text
ComputationalStochasticityDistributionAndRiskResponsibility
```

Classification:

```text
STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE
REFACTORS_ROUND_C
EXTENDS_ROUND_B_AGGREGATION
COMPOSES_WITH_ROUND_D_VALIDATION
STRENGTHENS_ROUND_A_ENVIRONMENT_ASSUMPTIONS
NOT_INDEPENDENT_UNIVERSAL_ESSENCE
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 36. Information gain

Round F information gain is **VERY HIGH**.

It destroys several common collapses at once:

```text
randomness = uncertainty
probability = nondeterminism
expected = typical
failure probability = numerical error
one randomized run = algorithm distribution
randomness = more computability
```

More importantly, it confirms the emerging architecture is not a list of independent `fields`.

The foundation-level structure is increasingly relational:

```text
semantic target
+ source of branching/variation
+ probability space
+ comparison/validation relation
+ resource aggregation
+ environment/adversary assumptions
+ evidence basis.
```

---

# 37. Next frontier — deliberately unselected

High-value unexplored orthogonal pressures remain:

```text
concurrency / distributed correctness / impossibility
physical / analog / reversible / quantum computation
computability / decidability / oracle-relative computation
state / memory / persistence models
information / coding / algorithmic information
online / streaming computation
```

Concurrency/distributed computation is now especially valuable because probabilistic automata already expose a hard unresolved interaction:

```text
probability
+ nondeterministic scheduler/adversary
+ failure model
+ communication/synchronization resources
+ safety/liveness/refinement.
```

Physical/unconventional computation remains mandatory before any numbered admission because the non-circular computational-interpretation/pancomputational grounding issue is still open.

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 38. Primary-source pressure anchors

Used as pressure sources, not ontology authority:

- John Gill, *Computational Complexity of Probabilistic Turing Machines*, SIAM Journal on Computing 6(4), 1977.
- Andrew C. Yao, *Probabilistic Computations: Toward a Unified Measure of Complexity*, 18th FOCS, 1977.
- R. Solovay and V. Strassen, *A Fast Monte-Carlo Test for Primality*, SIAM Journal on Computing 6(1), 1977, with later erratum.
- Dexter Kozen, *Semantics of Probabilistic Programs*, Journal of Computer and System Sciences 22(3), 1981.
- Roberto Segala and Nancy Lynch, *Probabilistic Simulations for Probabilistic Processes*, CONCUR 1994 / Nordic Journal of Computing 2(2), 1995.
- Randomized Las Vegas/Monte Carlo algorithm literature used only as regime pressure for separating random runtime from probabilistic correctness; no single terminology source is treated as ontology authority.
