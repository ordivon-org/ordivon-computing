---
schema_version: 1
id: computing.research.deep-foundations.round-d.numerical-approximate-finite-precision
title: Ordivon Computing Deep Foundations — Round D: Numerical / Approximate / Finite-Precision Computation
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Fourth destructive post-atlas Computing tournament. It attacks ExactResult, Error, Precision, Tolerance, Residual, Stability, Conditioning and Convergence as universal numerical primitives across IEEE floating point, rounding error, condition/sensitivity, forward and backward error, mixed precision, iterative refinement, interval arithmetic and approximate/iterative computation. The pass establishes that finite arithmetic semantics can differ from exact algebraic semantics; conditioning is a property of the problem/query, stability a relation between algorithm and perturbation model, forward error and backward error are distinct, residual is not solution error, convergence is not finite-run accuracy, stopping tolerance is not truth, and precision is both a resource dimension and—when it changes representable values/rounding/exceptions—a semantic-regime parameter. Round D partially couples and refactors Round B and Round C, while strengthening Round A's observation/completion distinctions. A strong cross-cutting candidate survives: ComputationalApproximationErrorAndValidationResponsibility, with explicit reference target, arithmetic/representation regime, approximation relation, error measure, conditioning/sensitivity, algorithmic stability/backward relation, convergence/stopping semantics, certification/enclosure/evidence, and acceptance consequence. It is not an independent universal essence of computation and is not CDF0.
evidence_status: strong-local
readiness: ROUND_D_COMPLETE_STRONG_CROSS_CUTTING_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round D

## Numerical / Approximate / Finite-Precision Computation

## 0. Admission discipline

Round D is not `CDF0`.

It attacks the current A/B/C factorization from a regime in which exact equality is often unavailable, irrelevant, or actively misleading:

```text
Round A
  boundary / interaction / continuation / observation

Round B
  resources / precision / feasibility

Round C
  representation / interpretation / equivalence / refinement
```

The key question is:

```text
Does numerical/approximate computation require a new independent foundation,
or does it force A/B/C to be refactored around approximation/error relations?
```

---

# 1. Current internal coverage is nearly absent

A bounded scan of current Computing Core/Knowledge and the active whole-domain artifacts finds no dedicated internal reconstruction of:

```text
floating-point semantics
roundoff analysis
condition numbers
forward/backward error
numerical stability
interval arithmetic
finite-precision convergence
certified numerical enclosure
```

The only substantial mentions occur in the whole-domain atlas and Round B/C as deliberately preserved future pressure.

Therefore Round D is a genuine underexplored-continent pass, not a replay of existing Core theory.

---

# 2. Floating-point arithmetic is a semantic regime, not merely smaller real numbers

The current IEEE 754-2019 standard specifies binary/decimal floating-point formats and arithmetic, exception handling, and result determination relative to input values, operation sequence and destination formats. A revision project is active, but 754-2019 remains the active published IEEE standard at this evidence horizon.

The important foundation pressure is:

```text
finite floating-point arithmetic
!= exact real arithmetic with hidden implementation noise.
```

It has its own representable domain, rounding behavior, exceptional values/conditions and operation semantics.

---

# 3. Exact algebraic laws need not survive finite arithmetic

## D-F1 — associativity failure

In ordinary binary floating-point arithmetic, evaluation order can change the result.

A standard pressure shape is:

```text
(a + b) + c
!=
a + (b + c)
```

for suitable magnitudes because an intermediate value rounds differently.

Therefore:

```text
RealAlgebraicEquivalence
!= FloatingPointSemanticEquivalenceByNecessity.
```

This directly pressures Round C:

```text
semantic regime/currentness
```

must include the arithmetic model, not only source-language syntax.

## D-F2 — mathematically equivalent transformation can be numerically inequivalent

Algebraic rewriting, reassociation or cancellation can preserve the exact real-valued expression while changing finite-precision error behavior.

Therefore:

```text
ExactDenotationalEquality
!= FinitePrecisionBehavioralEquivalence.
```

Compiler/numerical optimization correctness must declare which semantic regime/property is preserved.

---

# 4. Precision is both resource and semantic parameter

## D-F3 — same algorithm, different destination precision

Execute the same operation sequence under two precision/format regimes.

The representable states, rounding results, overflow/underflow thresholds and exceptional outcomes can differ.

Therefore:

```text
SameAlgorithmicStructure
!= SameFiniteArithmeticBehaviorAcrossPrecisions.
```

This means precision is not only Round B metadata.

## D-F4 — precision as cost/resource

Higher precision can increase storage, arithmetic cost, bandwidth and energy/data-movement burden.

Therefore:

```text
Precision
can be a Round B resource dimension.
```

## D-F5 — precision as semantic-regime input

Because precision/format can alter the actual transition/result relation:

```text
Precision
can also parameterize Round C semantic interpretation.
```

Thus:

```text
PrecisionResourceRole
!= PrecisionSemanticRoleByIdentity.
```

The same physical parameter can participate in two different claims.

---

# 5. Roundoff error is not the whole numerical error problem

## D-F6 — multiple error sources

A numerical result can differ from an ideal target due to:

```text
input/data uncertainty
model/discretization error
truncation/approximation error
iterative termination error
roundoff/finite arithmetic error
algorithmic instability
```

Therefore:

```text
NumericalError
!= RoundoffErrorByIdentity.
```

## D-F7 — exact discrete solve can still approximate the wrong/idealized target

A discretized differential equation can be solved exactly as a discrete system while remaining only an approximation to the continuous problem/model.

Therefore:

```text
ExactDiscreteSolution
!= ExactContinuousTargetByIdentity.
```

Mathematical/model truth may belong partly to Math/World/domain owners; Computing must preserve the reference-target relation rather than silently identify them.

---

# 6. Forward error and backward error are different questions

Wilkinson's error-analysis tradition made backward error analysis central: instead of only asking how far the computed answer is from the exact answer, ask whether the computed answer is the exact answer to a nearby input/problem.

## D-F8 — forward error

```text
forward error
= distance(computed result, exact target result)
```

under a declared metric/norm/scale.

## D-F9 — backward error

```text
backward error
= smallest admitted perturbation of input/problem
  for which the computed result is exact.
```

Therefore:

```text
ForwardError
!= BackwardErrorByIdentity.
```

A method can have a small backward error while forward error is amplified by problem sensitivity.

---

# 7. Conditioning belongs to the problem/query, not the algorithm

John Rice's theory of condition and the Wilkinson/Higham tradition separate problem sensitivity from numerical algorithm quality.

## D-F10 — same problem, different algorithms

Hold the mathematical problem fixed; vary the algorithm.

The condition/sensitivity of the problem does not become a property of whichever implementation happened to be chosen.

Therefore:

```text
ProblemConditioning
!= AlgorithmStabilityByIdentity.
```

## D-F11 — same algorithm family, different problem instances

A backward-stable method can be applied to both well-conditioned and ill-conditioned instances.

Forward accuracy can differ sharply even though algorithmic stability properties are similar.

Therefore:

```text
StableAlgorithm
!= AccurateResultByIdentity.
```

## D-F12 — conditioning is target/metric-relative

Sensitivity depends on:

```text
which input perturbations are admitted
which output quantity is observed
which norm/metric/scaling is used.
```

Therefore:

```text
ConditionNumber(problem)
without perturbation/output metric semantics
= underspecified.
```

---

# 8. Stability is not accuracy

## D-F13 — backward stable on ill-conditioned problem

Suppose an algorithm returns the exact solution to a nearby problem with tiny backward perturbation.

If the problem is highly sensitive, the corresponding forward result can still be far from the target solution.

Therefore:

```text
BackwardStability
!= SmallForwardErrorByIdentity.
```

## D-F14 — accurate result can occur from an unstable method on a benign instance

A numerically unstable algorithm can happen to produce a highly accurate result on a particular easy/fortunate input.

Therefore:

```text
ObservedAccuracyOnOneInstance
!= AlgorithmStabilityTheorem.
```

This mirrors Round B's:

```text
ObservedRuntimeSample != ComplexityTheorem.
```

---

# 9. Residual is not solution error

## D-F15 — small residual, large forward error

For a poorly conditioned linear system, an approximate solution can have a small residual while being far from the exact solution in the chosen solution metric.

Therefore:

```text
SmallResidual
!= SmallForwardErrorByIdentity.
```

## D-F16 — residual is still valuable evidence

Residual can enter error bounds together with conditioning/stability information.

Therefore:

```text
Residual
= evidence/diagnostic quantity
not universal Accuracy scalar.
```

This is a strong practical boundary for verification tooling.

---

# 10. Error measure itself is part of the claim

## D-F17 — absolute vs relative error

For values at different scales:

```text
small absolute error
```

and:

```text
small relative error
```

can disagree about quality.

Therefore:

```text
AbsoluteError
!= RelativeError.
```

## D-F18 — normwise vs componentwise error

A vector/matrix result can look small under a normwise measure while one component has unacceptable relative error, or vice versa.

Therefore:

```text
NormwiseError
!= ComponentwiseErrorByIdentity.
```

## D-F19 — task-specific error metric

An application may care about a derived quantity, conserved invariant, rank decision or classification boundary rather than raw coordinate distance.

Therefore:

```text
OneUniversalNumericalDistance
= REJECTED.
```

Round C's observation/property target is necessary for any error claim.

---

# 11. Approximate correctness is not failed exact correctness

## D-F20 — tolerance-bounded answer

A specification can explicitly require:

```text
|computed - target| <= epsilon.
```

If satisfied, the computation can be fully correct relative to that specification despite not returning the exact mathematical value.

Therefore:

```text
ApproximateResult
!= IncorrectResultByIdentity.
```

## D-F21 — tolerance is a specification threshold, not the measured error

```text
tolerance = allowed bound
error     = observed/proven discrepancy
```

Therefore:

```text
Tolerance
!= ErrorByIdentity.
```

## D-F22 — loose tolerance can be satisfied by a bad-for-purpose result

A tolerance is only meaningful relative to the actual property/metric/purpose.

Therefore:

```text
ToleranceSatisfied
!= UniversallyUsefulOrAccurateByIdentity.
```

---

# 12. Convergence is not finite-run accuracy

## D-F23 — convergent method before convergence

A mathematically convergent iterative method can be stopped too early and return an inaccurate answer.

Therefore:

```text
MethodConvergesAsymptotically
!= CurrentIterateAccurateByIdentity.
```

## D-F24 — accurate iterate without general convergence guarantee

A particular iterate/run can happen to be close to the target even if the method lacks a general convergence guarantee for the wider domain.

Therefore:

```text
CurrentIterateAccuracy
!= GeneralConvergenceTheorem.
```

## D-F25 — finite precision can alter convergence behavior

In finite arithmetic, iterations can stagnate, cycle, overflow or reach a representational fixed point even when the ideal exact-arithmetic iteration has a different asymptotic limit.

Therefore:

```text
ExactArithmeticConvergence
!= FinitePrecisionRunConvergenceByNecessity.
```

---

# 13. Stopping is a decision rule, not convergence truth

## D-F26 — stopping threshold

An algorithm may stop when:

```text
residual <= tau
change between iterates <= tau
max iterations reached
estimated error <= tau
```

These have different semantics.

Therefore:

```text
Stopped
!= ConvergedByIdentity.
```

## D-F27 — stagnation mistaken for convergence

Tiny iterate change can arise because finite precision prevents further movement, not because the iterate is near the desired exact target.

Therefore:

```text
SmallStep
!= SmallTargetErrorByIdentity.
```

Round A's continuation/termination semantics is strengthened: termination of an iterative computation must carry its stopping basis.

---

# 14. Mixed precision falsifies `working precision = result accuracy`

Carson and Higham's three-precision iterative-refinement analysis combines different precisions for factorization/solve, working solution and residual calculation and derives conditions for convergence plus forward/backward error bounds.

## D-F28 — low-precision bulk work, higher-accuracy result

A solver can perform major computational work in a lower precision while using higher precision strategically for residual/refinement to obtain substantially higher final accuracy.

Therefore:

```text
DominantWorkingPrecision
!= FinalAccuracyByIdentity.
```

## D-F29 — one run can contain multiple precision regimes

```text
Precision
```

cannot always be attached as one scalar property of the whole algorithm/run.

Therefore:

```text
ComputationPrecision
may be operation/phase-role-typed.
```

Round B must support structured resource/semantic regimes, not one `precision_bits` field.

---

# 15. More precision is not a universal cure

## D-F30 — ill-conditioning remains

Increasing arithmetic precision can reduce roundoff but does not alter the intrinsic sensitivity/conditioning of the mathematical problem under the same perturbation model.

Therefore:

```text
MoreArithmeticPrecision
!= BetterProblemConditioningByIdentity.
```

## D-F31 — model/discretization error remains

Higher arithmetic precision does not automatically reduce model/discretization error.

Therefore:

```text
MoreArithmeticPrecision
!= LowerTotalErrorByIdentity.
```

## D-F32 — unstable algorithm can still amplify rounding

Merely increasing precision may postpone or reduce instability effects without turning an unstable method into a stable one as a theorem.

Therefore:

```text
HigherPrecision
!= AlgorithmicStabilityByIdentity.
```

---

# 16. Interval arithmetic changes the shape of a valid result

Moore's interval-analysis tradition represents uncertain/approximate quantities as intervals and uses directed/proper rounding to produce enclosures that contain exact real-arithmetic results under suitable conditions.

## D-F33 — enclosure rather than point

A valid numerical answer can be:

```text
[target_lower, target_upper]
```

rather than one point estimate.

Therefore:

```text
NumericalResult
!= PointEstimateByIdentity.
```

## D-F34 — wider interval can be more trustworthy than a prettier point

A point estimate with no justified error bound can be less epistemically informative than a certified interval containing the target.

Therefore:

```text
ApparentNumericPrecision
!= CertifiedAccuracyByIdentity.
```

## D-F35 — enclosure width is not truth status

A wide interval can be correct but uninformative; a narrow interval can be valuable only if its enclosure guarantee is justified.

Therefore:

```text
NarrowInterval
!= ValidEnclosureByIdentity.
```

Certification/proof relation must remain explicit.

---

# 17. Floating-point exceptions are semantic outcomes, not just `large error`

IEEE floating-point semantics includes exceptional conditions/default handling and special representations such as infinities/NaNs in the standard regime.

## D-F36 — overflow/invalid is not ordinary approximation error

An operation that overflows or produces invalid-operation semantics is not adequately summarized by a finite scalar error from an exact real target.

Therefore:

```text
ExceptionalArithmeticOutcome
!= OrdinaryApproximationErrorByIdentity.
```

Round C semantic regime must represent exceptional behaviors where material.

---

# 18. Reproducibility and semantic equality can diverge

## D-F37 — different legal evaluation/reduction order

Parallel reduction or transformed evaluation order can produce different floating-point results while approximating the same exact mathematical quantity.

Therefore:

```text
SameMathematicalTarget
!= BitwiseReproducibleResultByIdentity.
```

## D-F38 — bitwise equality is stronger than many numerical correctness claims

Two outputs can differ in low-order bits while both satisfy the declared error bound/property.

Therefore:

```text
BitwiseEquality
!= NumericalCorrectnessRequirementByNecessity.
```

This is a direct Round C equivalence pressure.

---

# 19. Approximation relation is query-relative

## D-F39 — task-specific acceptance

For one task:

```text
relative error <= 1e-6
```

may be correct.

For another:

```text
sign must be exact
```

or:

```text
conservation law must hold
```

may dominate coordinate error.

Therefore:

```text
ApproximationQuality
requires declared property/metric/acceptance semantics.
```

No universal accuracy scalar survives.

---

# 20. Owner subtraction

## World / domain truth

World/domain owners retain:

```text
actual physical state
measurement truth
model adequacy to reality
experimental uncertainty
```

Computing may consume bounds/uncertainty models but must not claim that numerical solver error exhausts world-model error.

## Runtime

Runtime owns actual execution evidence:

```text
which binary ran
which precision/configuration was used
what values/exceptions occurred
how many iterations executed
```

Computing owns abstract/proven relations such as:

```text
conditioning
stability
error bound
convergence guarantee
certified enclosure semantics.
```

Therefore:

```text
ObservedNumericOutput
!= NumericalCorrectnessProof.
```

## Hardware

Hardware owns physical realization; IEEE/declared arithmetic semantics provide an abstract interface. Actual implementation conformance/effects remain external evidence.

## Human

Human tolerance/preferences and subjective usefulness remain Human/domain owned; Computing owns only the explicit acceptance contract once admitted.

---

# 21. Round A pressure result

Round D strengthens rather than absorbs A.

A's remaining fields include:

```text
ComputationalBoundary
InteractionInterfaceWhenPresent
ContinuationOrTerminationSemantics
EnvironmentAssumptions
```

Round D adds:

```text
termination/stopping basis
```

as crucial for iterative numerical processes.

Key laws:

```text
Stopped != Converged
ConvergedMethod != AccurateCurrentIterate
ExactArithmeticConvergence != FinitePrecisionRunConvergence
```

Thus Round A continuation semantics survives and becomes more precise.

---

# 22. Round B pressure result — partial coupling, not absorption

Round B already preserved precision as a resource dimension.

Round D proves precision can simultaneously affect:

```text
resource cost
AND
semantic transition/result regime.
```

Also iterations/tolerance can create a tradeoff:

```text
more computation
→ potentially smaller approximation error
```

but not universally or monotonically across all methods/problems.

Therefore:

```text
ResourceAndErrorRelations
can be coupled
without ResourceProfile == ErrorProfile.
```

Round B remains distinct, but its `ResourceDimensions` must permit dimensions that also parameterize semantics.

---

# 23. Round C pressure result — exact equivalence must generalize

Round C's:

```text
EquivalenceRefinementOrPreorderRelation
```

must be broad enough to include approximation/error relations such as:

```text
metric-bound approximation
forward error relation
backward relation
interval enclosure
convergence relation
property-preserving approximate refinement.
```

Therefore Round D **refactors C**:

```text
semantic relation
!= exact equivalence/refinement only.
```

A later merged semantic foundation may need a generic:

```text
SemanticComparisonOrApproximationRelation
```

rather than a binary equivalence-centric vocabulary.

---

# 24. Strong surviving candidate — Computational Approximation / Error / Validation Responsibility

Round D rejects `Error` and `Precision` as single primitives.

A broad cross-cutting responsibility survives:

```text
ComputationalApproximationErrorAndValidationResponsibility
```

Minimum current burden:

## 24.1 Reference target/problem

```text
what exact/ideal/discrete/continuous/specification target is the numerical result compared against?
```

## 24.2 Arithmetic / representation / precision regime

```text
exact arithmetic?
IEEE floating point format/rounding?
arbitrary precision?
interval arithmetic?
mixed precision?
```

## 24.3 Approximation/comparison relation

```text
point distance
relative/absolute error
normwise/componentwise error
backward perturbation
enclosure
application property
```

No closed enumeration.

## 24.4 Error/uncertainty decomposition when material

```text
input uncertainty
model/discretization
truncation/iteration
roundoff
other admitted components
```

## 24.5 Conditioning / sensitivity claim

```text
how does the target respond to admitted perturbations under the chosen metric/model?
```

## 24.6 Algorithmic stability / backward relation

```text
how does the computational method map arithmetic/perturbation effects into an equivalent nearby problem/result relation?
```

## 24.7 Convergence / stopping semantics

```text
what asymptotic guarantee exists?
what finite-run stopping rule fired?
what does stopping actually certify?
```

## 24.8 Error bound / certification / enclosure evidence

```text
measured estimate?
a priori theorem?
a posteriori bound?
interval enclosure?
formal certificate?
```

Evidence type matters.

## 24.9 Acceptance / validity consequence

```text
does the result satisfy the declared specification/tolerance/property?
is it unresolved, approximate-valid, certified, or invalid for the query?
```

---

# 25. Why this is not a fourth fully orthogonal sibling

Round D is foundationally important, but its structure is strongly cross-cutting:

```text
Reference target / semantic relation / acceptance
→ overlaps Round C

Precision / iterations / computational budget
→ overlaps Round B

Stopping / continuation
→ overlaps Round A
```

Therefore its current classification is not:

```text
independent sibling like B.
```

Instead:

```text
STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE
that forces A/B/C factorization changes.
```

It may later become:

```text
an approximation/error section of a larger ComputationalClaim foundation
```

rather than a separate numbered foundation.

Do not decide yet.

---

# 26. Candidate deletion results

Rejected as universal primitives/scalars:

```text
ExactResult
Error
RoundoffError
Precision
Tolerance
Residual
ConditionNumber
Stability
Accuracy
Convergence
IterationCount
PointEstimate
BitwiseEquality
```

All remain valid scoped concepts under explicit reference/metric/regime semantics.

---

# 27. Anti-collapse laws

```text
FiniteFloatingPointArithmetic != ExactRealArithmetic
RealAlgebraicEquivalence != FloatingPointSemanticEquivalence
ExactDenotationalEquality != FinitePrecisionBehavioralEquivalence
PrecisionResourceRole != PrecisionSemanticRole
NumericalError != RoundoffError
ExactDiscreteSolution != ExactContinuousTarget
ForwardError != BackwardError
ProblemConditioning != AlgorithmStability
StableAlgorithm != AccurateResult
ConditionNumberWithoutPerturbationMetric = underspecified
BackwardStability != SmallForwardError
ObservedAccuracy != StabilityTheorem
SmallResidual != SmallForwardError
AbsoluteError != RelativeError
NormwiseError != ComponentwiseError
ApproximateResult != IncorrectResult
Tolerance != Error
ToleranceSatisfied != UniversalAccuracy
MethodConverges != CurrentIterateAccurate
CurrentIterateAccurate != GeneralConvergenceTheorem
ExactArithmeticConvergence != FinitePrecisionRunConvergence
Stopped != Converged
SmallStep != SmallTargetError
DominantWorkingPrecision != FinalAccuracy
MorePrecision != BetterConditioning
MorePrecision != LowerTotalError
HigherPrecision != Stability
NumericalResult != PointEstimate
ApparentNumericPrecision != CertifiedAccuracy
NarrowInterval != ValidEnclosure
ExceptionalArithmeticOutcome != OrdinaryApproximationError
SameMathematicalTarget != BitwiseReproducibility
BitwiseEquality != NumericalCorrectnessRequirement
ObservedNumericOutput != NumericalCorrectnessProof
ResourceProfile != ErrorProfile
```

---

# 28. Rival-model update

## M1 Function evaluation

Further weakened as universal. Numerical computation often targets an approximate relation/enclosure rather than one exact extensional value.

## M2 Controlled state transition

Survives only with arithmetic/interpretation regime. Exact-real and finite-floating transitions are not interchangeable.

## M3 Information transformation

Still unresolved; error/precision can be described informationally but conditioning/stability/reference-target relations are not automatically reduced to information quantity.

## M4 Effective procedure

Partial. A procedure does not specify error semantics, conditioning or approximation validity.

## M5 Resource-bounded process

Round B remains strong but cannot absorb approximation correctness. Precision/iterations may be resources while also affecting semantics.

## M6 Interactive process

Not central this round. Iterative interaction/stopping cases strengthen A but do not make interaction universal.

## M7 Physical realization

Pressure increases: finite arithmetic depends on physically realizable formats/precision, but abstract floating-point semantics remains distinct from actual device physics. The grounding problem remains open.

---

# 29. Current A/B/C/D factorization

```text
A — Boundary / interaction / continuation
    - strengthened by stopping vs convergence

C — Interpretation / semantics / comparison
    - generalized from exact equivalence toward approximation/error relations

B — Resource / feasibility
    - precision/iterations remain resources
    - some resource dimensions also parameterize semantic regime

D — Approximation / error / validation
    - cross-cuts A/B/C
    - exposes conditioning/stability/error/certification distinctions
```

The architecture is now clearly **not a flat list of foundations**.

---

# 30. Agent-era pressure

Agent/ML systems intensify approximate computation through:

```text
low/mixed precision inference
quantization
approximate retrieval
iterative Tool/reasoning loops
approximate numerical Tools
uncertain learned surrogates
```

But Round D finds no Agent-specific numerical primitive.

The same distinctions remain:

```text
reference target
semantic/arithmetic regime
error metric
resource budget
stability/conditioning
acceptance/certification.
```

Agent era mainly increases the number of approximation layers that must not be collapsed.

---

# 31. Round D verdict

```text
ExactResult as universal correctness target
= REJECTED

Error as one scalar
= REJECTED

Precision as only a resource
= REJECTED

Precision as only semantics
= REJECTED

Tolerance = accuracy
= REJECTED

Residual = solution error
= REJECTED

Stability = accuracy
= REJECTED

Convergence = finite-run correctness
= REJECTED
```

Strong survivor:

```text
ComputationalApproximationErrorAndValidationResponsibility
```

Classification:

```text
STRONG_CROSS_CUTTING_FOUNDATIONAL_CANDIDATE
REFACTORS_ROUND_C
PARTIALLY_COUPLES_ROUND_B
STRENGTHENS_ROUND_A
NOT_INDEPENDENT_UNIVERSAL_ESSENCE
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 32. Information gain

Round D information gain is **VERY HIGH**.

It destroys another hidden binary:

```text
correct
vs
incorrect
```

and replaces it with a richer computational claim space:

```text
reference target
+ arithmetic/representation regime
+ approximation relation
+ conditioning
+ algorithmic stability
+ finite-run error evidence
+ convergence/stopping
+ acceptance/certification.
```

More importantly, it changes the factorization of existing candidates instead of merely adding vocabulary.

---

# 33. Next frontier — deliberately unselected

Several orthogonal high-value pressures remain:

```text
probabilistic/randomized computation
concurrency/distributed correctness and impossibility
physical/analog/reversible/quantum computation
computability/decidability
state/memory models
information/coding
```

Probabilistic/randomized computation is now particularly strong because it can test whether D's error/validation grammar generalizes from metric error to distributional correctness and whether B's expected/high-probability aggregation and C's probabilistic semantics are sufficient.

Physical/unconventional computation remains necessary before any numbered admission because the interpretation-grounding/pancomputational problem remains unresolved.

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 34. Primary-source pressure anchors

Used as pressure sources, not ontology authority:

- IEEE 754-2019, *IEEE Standard for Floating-Point Arithmetic*; current published standard at the evidence horizon, with P754 revision project active.
- J. H. Wilkinson, *Rounding Errors in Algebraic Processes* (1963) and *Modern Error Analysis* (SIAM Review, 1971), for systematic rounding/backward-error analysis.
- John R. Rice, *A Theory of Condition*, SIAM Journal on Numerical Analysis 3(2), 1966.
- David Goldberg, *What Every Computer Scientist Should Know About Floating-Point Arithmetic*, ACM Computing Surveys 23(1), 1991 (used as a systems-facing pressure exposition of finite floating-point behavior).
- Erin Carson and Nicholas J. Higham, *Accelerating the Solution of Linear Systems by Iterative Refinement in Three Precisions*, SIAM Journal on Scientific Computing 40(2), 2018.
- Ramon E. Moore, interval-analysis work, including *Methods and Applications of Interval Analysis* and the earlier interval-arithmetic/error-analysis line.
