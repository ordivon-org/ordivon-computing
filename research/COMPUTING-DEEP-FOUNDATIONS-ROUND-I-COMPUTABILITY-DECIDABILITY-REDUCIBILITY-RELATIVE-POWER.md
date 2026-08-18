---
schema_version: 1
id: computing.research.deep-foundations.round-i.computability-decidability-reducibility-relative-power
title: Ordivon Computing Deep Foundations — Round I: Computability / Decidability / Reducibility / Relative Power
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Destructive tournament over effective computability, decision/recognition/enumeration, reducibility, oracle-relative computation and model-relative computational power. The pass separates abstract effective solvability from complexity feasibility, coordination impossibility, physical realizability and observed execution failure. Pressure from Turing 1936, Turing 1939 oracle machines, Post 1944 recursively enumerable decision problems, Kleene recursive predicates and Rice 1953 semantic index-set undecidability establishes that partial computability is not total computability; recognizability/r.e. is not decidability; enumerability is not a terminating decision procedure; undecidability is a uniform-family theorem rather than per-instance unknowability; semantic properties can be undecidable even when syntactic properties remain decidable; reduction direction/type matters; and oracle-relative computability changes admitted power without making an oracle physically available. A strong genuinely independent candidate survives: ComputationalEffectiveSolvabilityAndRelativePowerResponsibility. It becomes a generic abstract-solvability layer that refactors G by moving generic solvability/impossibility ownership upstream while G retains coordination-specific task/model structure; it remains orthogonal to B resource feasibility and H physical realization. No CDF0 is admitted.
evidence_status: strong-local-plus-primary-source-pressure
readiness: ROUND_I_COMPLETE_STRONG_INDEPENDENT_EFFECTIVE_SOLVABILITY_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round I

## Computability / Decidability / Reducibility / Relative Power

## 0. Admission discipline

Round I is not `CDF0`.

The immediate pressure comes from the fact that earlier rounds already produced several distinct uses of `possible` and `impossible`:

```text
B — resource-feasible / infeasible
G — coordination-solvable / impossible under timing/failure model
H — physically realizable / unrealizable under preparation/readout/physics
I — effectively computable / decidable / recognizable / relatively computable
```

Round I asks whether effective solvability is merely a special case of those earlier relations or an independent Computing burden.

---

# 1. Internal coverage is still mostly pressure-level

The current Computing repo mentions Turing computability and hypercomputation in the atlas and earlier falsification rounds, but contains no dedicated reconstruction of:

```text
total vs partial computability
decidability vs recognizability
recursive vs recursively enumerable sets
enumeration vs decision
reducibility types/direction
oracle-relative computability
degrees/relative power
Rice-style semantic undecidability
```

Round I therefore remains genuine new whole-domain coverage.

---

# 2. Computation is not identical to total function computation

## I-F1 — partial computation

A machine/program can define a partial function: on some admitted inputs it returns a value; on others it may diverge.

Therefore:

```text
ComputablePartialFunction
!= TotalComputableFunctionByIdentity.
```

## I-F2 — concrete successful run does not establish total computability

Observing that program `P(x0)` returns does not show that `P(x)` returns for every input in its claimed domain.

Therefore:

```text
ObservedSuccessfulInstance
!= TotalityTheoremByIdentity.
```

## I-F3 — totality is stronger than per-output correctness when halted

A partial procedure can be correct on every input where it terminates while failing a total-function contract because it diverges elsewhere.

Therefore:

```text
PartialCorrectnessOnDomainOfTermination
!= TotalComputability.
```

This independently reinforces A/C distinctions between behavior, termination and correctness.

---

# 3. Function computation and decision are different claim shapes

## I-F4 — function output vs yes/no decision

Computing `f(x)` and deciding membership `x ∈ L` are different target specifications even when one can encode the other in some regimes.

Therefore:

```text
FunctionComputability
!= DecisionProblemIdentity.
```

## I-F5 — relation/search problem

A computational task may require producing any witness `y` satisfying relation `R(x,y)` rather than a unique function value or Boolean decision.

Therefore:

```text
ComputationalSolvability
!= FunctionEvaluationOrDecisionOnly.
```

The effective-solvability responsibility must admit multiple outcome modes.

---

# 4. Decidable is stronger than recognizable / recursively enumerable

Turing/Post/Kleene recursion-theoretic traditions distinguish sets whose membership can be decided by a terminating procedure from sets whose positive members can be effectively generated/recognized while negative cases may not terminate.

## I-F6 — recognizer with divergent negatives

A recognizer may halt/accept every member of `L` but diverge on some nonmembers.

Therefore:

```text
Recognizable
!= DecidableByIdentity.
```

## I-F7 — decider requires both sides terminate

A decider must eventually return yes or no for every admitted input.

Therefore:

```text
PositiveSemidecision
!= TotalDecisionProcedure.
```

## I-F8 — complement matters

If both a language and its complement are recognizable in the ordinary effective model, their recognizers can be dovetailed to obtain a decider.

Therefore:

```text
RecognizabilityOfOneSide
!= RecognizabilityOfBothSides.
```

The yes/no asymmetry is semantically material.

---

# 5. Enumeration is not a terminating membership decision

Post's recursively enumerable-set framing makes this pressure explicit.

## I-F9 — enumerator may never certify nonmembership

If an enumerator lists all members of an infinite set, waiting forever without seeing `x` does not in general prove `x` is not a member.

Therefore:

```text
Enumerable
!= DecidableByIdentity.
```

## I-F10 — enumeration and recognition may correspond extensionally under standard assumptions but remain different operational contracts

A conversion theorem does not make the claims identical:

```text
generate all members
```

and:

```text
halt-and-accept a supplied member
```

have different interfaces/termination behavior.

Therefore:

```text
EnumerationContract
!= RecognitionContractByIdentity.
```

---

# 6. Undecidable does not mean every instance is unknowable

## I-F11 — some instances can be easy

An undecidable decision problem can contain individual instances whose answer is directly provable/known.

Therefore:

```text
ProblemUndecidable
!= EveryInstanceUnanswerableByIdentity.
```

## I-F12 — undecidability is uniform-family failure

The relevant claim is that no admitted effective procedure correctly decides every instance in the problem domain.

Therefore:

```text
Undecidability
= uniform computational impossibility claim
not per-instance epistemic ignorance.
```

## I-F13 — mathematical truth vs effective uniform decision

A proposition can have a definite truth value under a mathematical semantics even when no single effective procedure decides all members of the corresponding family.

Therefore:

```text
TruthValueExistence
!= UniformDecidabilityByIdentity.
```

This preserves Computing/Human/Math ownership boundaries.

---

# 7. Undecidable is not intractable

## I-F14 — computable but expensive

A problem can have a total decider but require very large resources under a model.

Therefore:

```text
Computable
!= EfficientByIdentity.
```

## I-F15 — undecidable is not merely `very large complexity`

If no total decider exists in the model, the issue is not a finite/asymptotic resource bound on a total decision algorithm.

Therefore:

```text
Undecidable
!= IntractableByIdentity.
```

## I-F16 — B remains downstream/orthogonal

Complexity claims ask about resource cost of admitted computational procedures/problems; computability asks whether a procedure of the required kind exists at all.

Therefore:

```text
EffectiveSolvability
!= ResourceFeasibility.
```

---

# 8. Turing 1936 pressures `effective procedure` without defining all Computing

Turing's machine formalization provides a precise model for computable numbers/functions/predicates and the Entscheidungsproblem.

## I-F17 — effective function computation is a foundation regime, not universal behavior ontology

Long-running interactive systems from Round A and physical realization from H are not exhausted by asking for one total mathematical function.

Therefore:

```text
TuringFunctionComputability
!= WholeComputingDefinitionByIdentity.
```

## I-F18 — model equivalence evidence does not turn the Church-Turing thesis into a theorem about physical reality

Formal equivalence among major effective-calculation models supports a robust abstraction of effective calculability, but the bridge from intuitive/physical realizability to a formal class is a thesis/interpretive claim, not a theorem internal to one model.

Therefore:

```text
FormalModelEquivalence
!= PhysicalChurchTuringTheoremByIdentity.
```

H remains necessary.

---

# 9. Program halting and language decidability must not collapse

## I-F19 — halting of one run

`P(x)` halts is a property of a particular program/input pair.

## I-F20 — global halting decision problem

The question whether a universal procedure decides halting for all encoded program/input pairs is a family-level decision problem.

Therefore:

```text
ObservedHaltingOfInstance
!= DecidabilityOfHaltingFamily.
```

## I-F21 — halting behavior is not the only undecidable semantic property

Rice's 1953 result generalizes the pressure: nontrivial extensional/index properties of recursively enumerable/computed behavior are undecidable under the relevant indexing framework.

Therefore:

```text
Undecidability
!= HaltingProblemOnly.
```

---

# 10. Rice pressure sharpens C: syntax vs semantic property

## I-F22 — syntactic property may be decidable

A representation-level property such as `program text contains token X` can be mechanically decidable even though a nontrivial property of the function/language computed by arbitrary programs is undecidable.

Therefore:

```text
SyntacticPropertyDecidability
!= SemanticPropertyDecidabilityByIdentity.
```

## I-F23 — semantics rather than spelling controls Rice-style pressure

If a property includes/excludes programs solely according to the extensional behavior they compute, changing representation while preserving semantics does not change membership in the semantic property.

Therefore:

```text
RepresentationIdentity
!= SemanticIndexPropertyIdentity.
```

This strongly reinforces C's representation/semantics separation.

## I-F24 — Rice theorem is not `every program property is undecidable`

Trivial properties and many intensional/syntactic properties fall outside the simple nontrivial extensional form.

Therefore:

```text
ProgramProperty
!= AutomaticallyUndecidable.
```

Precise property scope matters.

---

# 11. Domain restriction / promise can change decidability

## I-F25 — global problem vs restricted domain

A property undecidable over all arbitrary programs can become decidable on a restricted family with strong structural guarantees.

Therefore:

```text
GlobalUndecidability
!= UndecidabilityOnEveryRestrictedDomain.
```

## I-F26 — finite explicit domain

A fully specified finite input domain can in principle be decided by a finite lookup relation even if an unbounded generalization is undecidable.

Therefore:

```text
ProblemDomainScope
can be constitutive of DecidabilityClaim.
```

## I-F27 — promise violation disposition matters

If a solver is required to behave correctly only for inputs satisfying a promise, behavior outside the promise does not belong to the same decision contract.

Therefore:

```text
PromiseProblem
!= UnrestrictedDecisionProblemByIdentity.
```

---

# 12. Reduction is directional, typed and model-relative

Post/Turing relative-computability traditions make `can solve A using B` a formal relation rather than vague similarity.

## I-F28 — reduction direction matters

If `A ≤ B`, then an algorithm/oracle for `B` may be sufficient to solve `A` under the declared reduction notion.

The converse does not follow.

Therefore:

```text
A_ReducesTo_B
!= B_ReducesTo_A.
```

## I-F29 — reduction does not imply semantic identity

Different problems can reduce to each other while asking entirely different semantic questions.

Therefore:

```text
MutualReducibility
!= SemanticIdentityByIdentity.
```

## I-F30 — reduction does not automatically preserve resource complexity

A computability reduction may incur arbitrary overhead or use an oracle in ways unsuitable for a fine-grained complexity claim.

Therefore:

```text
ComputabilityReduction
!= ComplexityPreservingReductionByIdentity.
```

Round B needs its own reduction/resource semantics when relevant.

---

# 13. Reduction notions themselves differ

## I-F31 — many-one vs oracle/Turing reduction

A many-one style reduction transforms one instance into one target instance and interprets its answer; a Turing/oracle reduction may make adaptive multiple queries during a computation.

Therefore:

```text
ManyOneReducibility
!= TuringReducibilityByIdentity.
```

## I-F32 — same problem pair can have different status under different reductions

Therefore:

```text
ReducibilityClaim
without ReductionType
= underspecified.
```

## I-F33 — completeness is reduction-relative

Calling a problem `complete` only makes sense relative to:

```text
problem class
reduction relation
computational model.
```

Therefore:

```text
CompleteProblem
without reduction/class semantics
= underspecified.
```

---

# 14. Turing 1939 oracle machines make computational power explicitly relative

Turing's `o-machine` construction augments an ordinary machine with answers to a specified non-machine-computable set/question source.

## I-F34 — oracle changes admitted primitive power

A set undecidable by an ordinary machine can be decidable relative to an oracle that answers exactly those membership questions.

Therefore:

```text
UndecidableInBaseModel
!= UndecidableRelativeToEveryStrongerModel.
```

## I-F35 — oracle answer is not an implementation explanation

Treating an undecidable set as an oracle primitive does not explain how to physically compute the oracle answers.

Therefore:

```text
OracleRelativeComputability
!= PhysicalRealizabilityByIdentity.
```

H survives.

## I-F36 — oracle access is power assumption, not only resource budget

An oracle can alter which tasks are computable at all, not merely make an already-computable task faster.

Therefore:

```text
OracleCapability
!= OrdinaryResourceDimensionByIdentity.
```

B does not absorb I.

---

# 15. Relative computability destroys a single binary `computable/uncomputable` ontology

## I-F37 — relative power hierarchy

A problem can be uncomputable relative to model `M` but computable relative to `M + oracle O`.

Therefore:

```text
Computable:Boolean
without model/power semantics
= underspecified in relative-computability contexts.
```

## I-F38 — different oracles produce different relative worlds

Two oracle sets can give different computational powers.

Therefore:

```text
HasOracle
!= OneUniversalEnhancedPowerByIdentity.
```

## I-F39 — oracle hierarchy can continue

Once one oracle is admitted, questions may remain undecidable relative to that oracle.

Therefore:

```text
OneOracle
!= EndOfUndecidabilityByIdentity.
```

Relative power is structured rather than a one-time escape hatch.

---

# 16. Reducibility / relative power is not empirical difficulty

## I-F40 — implementation happens to fail

A solver timing out, crashing or returning wrong results does not prove the target is uncomputable.

Therefore:

```text
ObservedSolverFailure
!= UncomputabilityTheoremByIdentity.
```

## I-F41 — successful finite test suite does not prove decidability

Passing many instances does not establish a uniform total decider for an unbounded domain.

Therefore:

```text
FiniteEmpiricalSuccess
!= DecidabilityTheoremByIdentity.
```

Runtime/Human evidence and abstract computability proofs remain separate.

---

# 17. G impossibility is not undecidability

## I-F42 — FLP-style coordination impossibility

G's FLP pressure states that no deterministic protocol satisfies a coordination contract under a specified asynchronous crash-failure execution model.

This quantifies over distributed protocols/executions with progress/safety assumptions.

## I-F43 — classical undecidability has a different task/model shape

A classical undecidability theorem denies a total effective decision procedure for an encoded family/property under a formal computation model.

Therefore:

```text
CoordinationImpossibility
!= UndecidabilityByIdentity.
```

## I-F44 — generic solvability interface can be shared

Both can be expressed as:

```text
under model M and required contract P,
there exists / does not exist an admitted solver A.
```

Therefore Round I can own the **generic effective solvability/impossibility theorem relation**, while G owns the coordination-specific model/specification that instantiates it.

This is a factorization correction to G.

---

# 18. H physical unrealizability is not abstract uncomputability

## I-F45 — abstractly computable but physically infeasible/unrealized

A Turing-computable function might lack a practical physical realization under a declared hardware/resource regime.

Therefore:

```text
AbstractlyComputable
!= PhysicallyRealizableHereByIdentity.
```

## I-F46 — abstract oracle-computable does not imply physical oracle

Already established:

```text
RelativeComputability
!= PhysicalRealizability.
```

## I-F47 — physical hypercomputation claims would change the model, not retroactively invalidate the relative structure

If a physical device genuinely realizes a stronger computational primitive, the correct response is to state a stronger model and re-evaluate relative computability under it.

Therefore:

```text
PhysicalModelExtension
!= ModelFreeCollapseOfComputabilityTheory.
```

H and I remain orthogonal but linked.

---

# 19. F probabilistic correctness is not exact decidability

## I-F48 — bounded-error randomized decision

A randomized algorithm can return the correct answer with high probability on every input while retaining a nonzero failure probability.

Therefore:

```text
BoundedErrorProbabilisticDecision
!= ExactDeterministicDeciderByIdentity.
```

## I-F49 — standard randomized power need not imply new recursive functions

Round F/Gill pressure already established that randomization in the cited probabilistic-TM regime does not automatically yield hypercomputability.

Therefore:

```text
ProbabilisticEfficiencyGain
!= EffectiveComputabilityBoundaryChangeByIdentity.
```

F overlays risk semantics on I rather than replacing it.

---

# 20. Quantum speedup likewise does not collapse I into H

## I-F50 — quantum model can alter efficient complexity without altering the semantic target

Round H/Bernstein-Vazirani pressure established:

```text
QuantumSpeedup != Hypercomputability.
```

Therefore:

```text
ComplexityModelAdvantage
!= DecidabilityBoundaryChangeByIdentity.
```

Any future stronger physical model must be stated explicitly in I's model/power field.

---

# 21. Uniformity matters

## I-F51 — one solver per individual instance is not a uniform algorithm

If for each finite instance one can manually construct an answer-specific program after already knowing the answer, that does not provide one effective procedure for the whole family.

Therefore:

```text
PerInstanceExistenceOfCorrectProgram
!= UniformComputabilityByIdentity.
```

## I-F52 — finite advice/lookup can shift what is encoded in algorithm vs auxiliary information

A computational claim must expose whether nonuniform advice/oracle tables are admitted rather than hiding them inside the solver description.

Therefore:

```text
SolverPower
depends on admitted auxiliary information regime.
```

---

# 22. `No algorithm` needs quantified model scope

## I-F53 — algorithm family quantifier

A proper impossibility claim must make clear which solver class/model is quantified over.

Therefore:

```text
NoAlgorithmExists
without ComputationalModelAndAdmittedPrimitives
= underspecified.
```

## I-F54 — target contract quantifier

A solver may exist for recognition but not decision, approximation but not exact output, promise domain but not unrestricted domain.

Therefore:

```text
Unsolvable
without OutcomeModeAndContract
= underspecified.
```

This is the central generalization of Round I.

---

# 23. Owner subtraction

## Mathematics / logic

Mathematics owns theorem truth and formal structures in general.

Computing owns the computational interpretation of:

```text
solver existence
decision/recognition contract
model-relative reducibility/oracle power
```

for computational tasks.

## Runtime

Runtime owns observed executions and termination of concrete runs.

It does not own universal decidability/uncomputability theorems.

## H / World / Hardware

H/World/Hardware own physical realization and physical-law truth.

Oracle-relative or abstract computability does not assert physical implementation.

## G / Network

G owns coordination-specific task/history/timing/failure semantics; Network owns actual transport.

I owns generic solver-existence/reduction/impossibility relation once those models are supplied.

## Human

Human knowledge/proof discovery and epistemic uncertainty are not the same as algorithmic decidability.

---

# 24. Round A relation

A survives.

A describes the behavior/termination semantics of a computation/run/process.

I adds a uniform task-level quantifier:

```text
Does there exist one admitted effective solver satisfying the required behavior for every input in the domain?
```

Therefore:

```text
RunTerminationSemantics
!= ProblemDecidabilityByIdentity.
```

A supplies solver behavior; I quantifies over solver existence across a family.

---

# 25. Round B relation

B remains cleanly orthogonal:

```text
EffectiveSolvability
!= ResourceFeasibility.
```

A computable problem can be infeasible under resources; an undecidable problem is not merely a computable problem with a high asymptotic cost.

B consumes I's admitted solver/problem/model when asking cost questions.

---

# 26. Round C relation

C supplies:

```text
representation/domain semantics
semantic property target
interpretation/equivalence/refinement
```

I supplies:

```text
existence/nonexistence of effective procedures deciding/computing those targets.
```

Rice pressure strongly links them but does not collapse them:

```text
SemanticMeaning
!= DecidabilityOfSemanticProperty.
```

C explains what the property means; I asks whether it is uniformly effectively solvable.

---

# 27. Round G relation — important ownership refactor

Round G currently contains:

```text
SolvabilityOrImpossibilityClaim
```

Round I shows the generic theorem form is not coordination-specific.

Current best refactor:

```text
I owns generic EffectiveSolvabilityOrImpossibility relation
G owns the coordination task/model:
  history/order
  safety/progress
  timing/synchrony
  failures
  scheduler/fairness
  shared-state/communication primitives
```

G then instantiates I's generic solver-existence theorem interface.

Thus:

```text
G SolvabilityOrImpossibilityClaim
→ reference to I generic responsibility
```

without eliminating G's irreducible coordination burden.

---

# 28. Round H relation

H owns physical implementation grounding.

I owns abstract model-relative effective power.

The bridge is explicit:

```text
H may establish that a physical system realizes model M.
I then determines/records effective power claims relative to M.
```

But:

```text
I theorem
!= H realization evidence.
```

Physical Church-Turing remains the substantive bridge thesis, not a definition.

---

# 29. Strong survivor — Computational Effective Solvability and Relative Power Responsibility

Round I leaves a strong genuinely independent burden:

```text
ComputationalEffectiveSolvabilityAndRelativePowerResponsibility
```

Minimum current burden:

## 29.1 Problem / function / relation specification

```text
what computational family/task is being solved?
```

## 29.2 Domain / promise / encoding scope

```text
which admitted inputs/instances and representations are quantified over?
```

## 29.3 Computational model and admitted primitives

```text
ordinary Turing/effective model?
oracle access?
quantum model?
other explicit model?
```

No model-free `computable` claim when relative power matters.

## 29.4 Required outcome mode

```text
total function
partial function
decision
recognition/semidecision
enumeration
search/relation
approximate/probabilistic variant
```

## 29.5 Totality / termination requirement

```text
must every admitted input receive a terminating answer?
which side may diverge?
```

## 29.6 Effective status claim

```text
computable
decidable
recognizable/r.e.
co-recognizable
noncomputable/undecidable
```

Typed rather than one Boolean.

## 29.7 Reduction / relative-computability relation

```text
many-one?
Turing/oracle?
other declared reduction?
direction?
```

## 29.8 Oracle / auxiliary-power assumptions

```text
which non-base primitive/advice/source is admitted?
```

## 29.9 Uniformity / quantification regime

```text
one uniform solver over family?
nonuniform advice?
finite restricted domain?
```

## 29.10 Solvability / impossibility theorem relation

```text
exists solver?
no solver exists?
relative to exactly which model and contract?
```

This becomes the generic upstream interface used by G and potentially other domains.

## 29.11 Proof / reduction / diagonalization witness basis

```text
constructive solver?
reduction?
diagonalization?
semantic-index theorem?
relative/oracle argument?
```

Evidence/theorem type remains explicit.

---

# 30. Why I is genuinely independent

C can define a computational property precisely without deciding it.

B can price algorithms without deciding whether a total solver exists for every task.

G can define a distributed coordination task and execution model, but its generic solver-existence quantifier is not inherently distributed.

H can realize a physical machine without determining all abstract tasks computable by its formal model.

Therefore the relation:

```text
problem + model + contract
→ exists / does not exist effective solver
```

survives all owner/candidate subtraction.

Round I is currently one of the strongest sibling-level candidates alongside B, G and H.

---

# 31. Candidate deletion results

Rejected as universal primitive/scalar:

```text
Computable
Decidable
Undecidable
Algorithm
HaltingProblem
RecursiveSet
RecursivelyEnumerable
Semidecidable
Reduction
TuringReduction
Oracle
DegreeOfUnsolvability
ChurchTuringThesis
Hypercomputation
CompleteProblem
```

All remain essential scoped constructs under explicit model/contract semantics.

---

# 32. Anti-collapse laws

```text
PartialComputable != TotalComputable
ObservedSuccessfulInstance != TotalityTheorem
PartialCorrectness != TotalComputability
FunctionComputability != DecisionProblemIdentity
ComputationalSolvability != FunctionOrDecisionOnly
Recognizable != Decidable
PositiveSemidecision != TotalDecision
RecognizabilityOneSide != RecognizabilityBothSides
Enumerable != Decidable
EnumerationContract != RecognitionContract
ProblemUndecidable != EveryInstanceUnanswerable
TruthValueExistence != UniformDecidability
Computable != Efficient
Undecidable != Intractable
EffectiveSolvability != ResourceFeasibility
TuringFunctionComputability != WholeComputingDefinition
FormalModelEquivalence != PhysicalChurchTuringTheorem
ObservedHaltingInstance != DecidabilityOfHaltingFamily
Undecidability != HaltingProblemOnly
SyntacticPropertyDecidability != SemanticPropertyDecidability
RepresentationIdentity != SemanticIndexPropertyIdentity
ProgramProperty != AutomaticallyUndecidable
GlobalUndecidability != UndecidabilityOnEveryRestrictedDomain
PromiseProblem != UnrestrictedDecisionProblem
A_ReducesTo_B != B_ReducesTo_A
MutualReducibility != SemanticIdentity
ComputabilityReduction != ComplexityPreservingReduction
ManyOneReducibility != TuringReducibility
ReductionWithoutType = underspecified
CompletenessWithoutReductionClass = underspecified
UndecidableBaseModel != UndecidableEveryStrongerModel
OracleRelativeComputability != PhysicalRealizability
OracleCapability != OrdinaryResourceDimension
ComputableWithoutModelCanBeUnderspecified
HasOracle != OneUniversalEnhancedPower
OneOracle != EndOfUndecidability
ObservedSolverFailure != UncomputabilityTheorem
FiniteEmpiricalSuccess != DecidabilityTheorem
CoordinationImpossibility != Undecidability
AbstractlyComputable != PhysicallyRealizableHere
PhysicalModelExtension != ModelFreeCollapseOfComputabilityTheory
BoundedErrorProbabilisticDecision != ExactDeterministicDecider
ProbabilisticEfficiencyGain != ComputabilityBoundaryChange
ComplexityModelAdvantage != DecidabilityBoundaryChange
PerInstanceCorrectProgram != UniformComputability
NoAlgorithmExistsWithoutModel = underspecified
UnsolvableWithoutOutcomeContract = underspecified
```

---

# 33. Rival-model update

## M1 Function evaluation

Still rejected as whole Computing definition, but function computability remains a canonical I outcome mode.

## M2 Controlled state transition

Does not answer whether there exists a uniform effective transition system solving a problem family.

## M3 Information transformation

Does not distinguish computable from noncomputable information transformations without an effective model.

## M4 Effective procedure

Substantially strengthened and reconstructed.

Naive universal form:

```text
Computation = terminating effective procedure
```

remains rejected by A.

Scoped form survives strongly:

```text
Effective solvability claim
= existence of an admitted procedure satisfying a declared outcome/termination contract
  over a declared domain under a declared computational model.
```

## M5 Resource-bounded process

B remains independent/downstream from existence of effective solver.

## M6 Interactive process

Interaction does not automatically change function computability; interactive tasks require their own behavior contract before I can state solvability.

## M7 Physical realization

H remains independent. Physical realization can instantiate/extend a computational model but does not replace abstract relative computability theory.

---

# 34. Current A/B/C/D/F/G/H/I factorization

```text
                         I
          Effective Solvability / Relative Power
            problem + model + contract
                exists / no solver
               /        |         \
              /         |          \
             ▼          ▼           ▼
             G          B           H
       coordination   resources   physical realization
             │          │           │
             └────┬─────┘           │
                  ▼                 │
                  C ◄───────────────┘
          semantics / interpretation
                  │
            ┌─────┴─────┐
            ▼           ▼
            D           F
       approximation probability/risk

A supplies boundary/behavior/termination semantics
used by solver/process contracts across the graph.
```

This is provisional factorization, not a numbered Foundation architecture.

---

# 35. Information gain

Round I information gain is **VERY HIGH / ARCHITECTURALLY DECISIVE**.

It establishes a fourth strong sibling-level axis:

```text
B — Resource / Feasibility
G — Coordination / Consistency / Progress
H — Physical Realization / Grounding
I — Effective Solvability / Relative Power
```

and it makes a concrete ownership correction:

```text
G generic SolvabilityOrImpossibilityClaim
→ I generic solver-existence theorem layer
```

while G keeps the coordination-specific semantic model.

---

# 36. Next frontier — deliberately unselected

High-value continents still open include:

```text
state / memory / persistence / memory consistency
information / coding / algorithmic information
online / streaming / advice / competitive computation
real-time / cyber-physical computation
biological / neuromorphic computation
algorithm/data-structure/lower-bound structure beyond B generic resources
```

State/memory now has particularly high falsification value because G assumes shared-state histories, H separates abstract state from physical storage, C separates representation from semantics and A already has process state/continuation. A dedicated pass can determine whether memory/state/persistence is an independent foundation or entirely derivative.

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 37. Primary-source pressure anchors

Used as pressure sources, not ontology authority:

- A. M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, Proceedings of the London Mathematical Society, 1936/1937.
- A. M. Turing, *Systems of Logic Based on Ordinals*, Proceedings of the London Mathematical Society, 1939 — oracle/o-machine and relative computation pressure.
- Emil L. Post, *Recursively Enumerable Sets of Positive Integers and Their Decision Problems*, Bulletin of the American Mathematical Society 50, 1944.
- S. C. Kleene, *Recursive Predicates and Quantifiers*, Transactions of the American Mathematical Society 53, 1943.
- H. G. Rice, *Classes of Recursively Enumerable Sets and Their Decision Problems*, Transactions of the American Mathematical Society 74, 1953.
