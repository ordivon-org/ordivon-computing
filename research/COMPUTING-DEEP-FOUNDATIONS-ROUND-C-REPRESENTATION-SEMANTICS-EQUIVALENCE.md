---
schema_version: 1
id: computing.research.deep-foundations.round-c.representation-semantics-equivalence
title: Ordivon Computing Deep Foundations — Round C: Representation / Semantics / Equivalence / Refinement
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Third destructive post-atlas Computing tournament. It attacks Program/Syntax/Semantics/Type/Specification/Equivalence as universal primitives and tests whether programming-language semantics absorbs Round A Boundary/Behavior or Round B Resource/Feasibility. Classical pressure from Hoare logic, operational/contextual equivalence, parametricity/representation independence and CompCert semantic preservation shows that representation identity, semantic identity, specification satisfaction, contextual equivalence, refinement and resource equivalence are distinct. Programming-language semantics is not universal because computations need not have source-program syntax, but a broader ComputationalInterpretationAndSemanticRelationResponsibility survives: a computational claim must declare the representation/model being interpreted, well-formedness/admissibility where relevant, semantic target/behavior relation, specification/property target, observation/context relation, equivalence/refinement order, transformation mapping and preservation claim. This partially absorbs/refactors Round A's TransitionOrBehaviorSemantics and ObservationOrEquivalenceSemantics while leaving Round A's boundary/interaction/continuation burdens and all of Round B's resource/feasibility burden distinct. No CDF0 is admitted.
evidence_status: strong-local
readiness: ROUND_C_COMPLETE_STRONG_OVERLAPPING_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round C

## Representation / Semantics / Equivalence / Refinement

## 0. Admission discipline

This round is not `CDF0`.

Round A survivor:

```text
ComputationalBoundaryAndBehaviorResponsibility
```

Round B survivor:

```text
ComputationalResourceAndFeasibilityResponsibility
```

Round C asks whether both are merely consequences of a general theory of program semantics.

The initial hypothesis under attack is:

```text
Computation
= Program
+ ProgrammingLanguageSemantics.
```

The rival hypothesis is broader:

```text
computational claims require an interpretation relation
between some representation/model and some semantic behavior/specification,
but need not be source programs in a programming language.
```

---

# 1. Classical semantics already separates several notions

Programming-language theory does not have one single thing called `semantics`.

At minimum, mature traditions distinguish:

```text
operational semantics
  meaning through allowed execution/evaluation behavior

denotational semantics
  meaning through mathematical denotations

axiomatic/program logic
  meaning/properties through assertions and inference rules

contextual/observational equivalence
  indistinguishability under admitted program contexts/observations

refinement / simulation
  one implementation behavior constrained relative to another
```

Hoare's 1969 work explicitly develops axioms/rules for proving properties of programs rather than identifying program text with behavior. Operational-semantics and contextual-equivalence work likewise distinguishes concrete evaluation from observational equivalence. CompCert makes the separation executable at industrial scale: source and target programs are different representations, with formal semantics relating each to possible observable behaviors, and compiler correctness stated as semantic preservation/refinement.

---

# 2. Candidate deletion — `Program` is not universal computation

## C-F1 — closed mathematical machine without source language

A Turing machine transition table, Boolean circuit, cellular automaton configuration, hardware dataflow graph or analog/physical computational model can be studied computationally without a high-level programming-language source program.

Therefore:

```text
SourceProgramText
!= necessary condition for Computation.
```

Programming-language semantics cannot be the whole Computing foundation.

## C-F2 — same algorithm, many programs

The same algorithmic idea can be represented in C, Rust, assembly, lambda calculus, a circuit or pseudocode.

Therefore:

```text
AlgorithmIdentity
!= ProgramTextIdentity.
```

## C-F3 — same program text under different languages/version contexts

Identical character/token sequences can receive different parse/type/evaluation meaning under different language grammars, editions, extensions or environments.

Therefore:

```text
TextIdentity
!= SemanticIdentityByNecessity.
```

The interpretation context/model matters.

---

# 3. Syntax is not semantics

## C-F4 — alpha-renaming

Renaming bound variables can change syntax while preserving meaning under standard lambda-calculus semantics.

```text
SyntacticDifference
!= SemanticDifferenceByIdentity.
```

## C-F5 — dead-code/normalization transformation

Representations can differ substantially while preserving observable behavior.

Therefore:

```text
RepresentationDifference
!= BehavioralDifferenceByIdentity.
```

## C-F6 — syntactically present but semantically inadmissible

A string may parse but fail typing/static admissibility; another may fail parsing entirely.

Therefore:

```text
TextExistence
!= WellFormedProgram
!= AdmittedComputation.
```

Well-formedness/admissibility is a separate relation.

---

# 4. Compiler correctness makes representation/semantics separation explicit

## C-F7 — CompCert source vs target representation

CompCert relates source C abstract-syntax trees to target assembly abstract-syntax trees and proves semantic preservation of observable behavior.

Therefore:

```text
SourceRepresentationIdentity
!= TargetRepresentationIdentity
```

while a preservation relation may still hold.

## C-F8 — semantic preservation is not representation preservation

A correct optimizing compiler is expected to change control flow, register allocation, instruction structure and representation.

Thus:

```text
CompilerCorrectness
!= TextualOrStructuralIdentity.
```

## C-F9 — preservation can be refinement rather than exact equality

CompCert's current high-level theorem permits generated code to select one allowed source behavior and, in some cases, improve a source behavior that would go wrong.

Therefore:

```text
SemanticPreservation
!= ExactBehaviorSetEqualityByNecessity.
```

Refinement/order direction must be explicit.

---

# 5. Observation semantics is unavoidable

## C-F10 — CompCert observable behavior deliberately abstracts resource use

CompCert's documented observable behavior includes termination/divergence and I/O/volatile traces, while explicitly excluding execution time and memory consumption.

Therefore:

```text
SemanticObservationBoundary
can intentionally abstract ResourceBehavior.
```

This is decisive:

```text
SemanticEquivalence
!= ResourceEquivalenceByIdentity.
```

Round B cannot be absorbed by ordinary behavioral semantics unless the semantic domain is explicitly enriched with resources.

## C-F11 — source/target may differ internally but match observably

Compiler passes can change many internal transitions while preserving admitted observations.

Therefore:

```text
InternalTransitionEquality
!= necessary for SemanticPreservation.
```

This strengthens Round A's explicit observation/equivalence semantics.

---

# 6. No one equivalence relation is universal

## C-F12 — contextual equivalence

Contextual equivalence asks whether two program phrases remain observationally indistinguishable in admitted program contexts.

This is different from literal syntax equality, step-by-step equality or arbitrary denotational equality.

Therefore:

```text
ProgramEquivalence
requires declared observation/context semantics.
```

## C-F13 — trace vs contextual equivalence

Two systems can coincide on one trace projection while a richer context distinguishes them through termination, failure, interaction or state effects.

Therefore:

```text
TraceEquivalence
!= ContextualEquivalenceByIdentity.
```

## C-F14 — denotational equality and full abstraction

A denotational model may be sound/adequate yet distinguish more or fewer terms than the operational/contextual observations do. Full abstraction is precisely an extra relation between semantic equality and observational equivalence.

Therefore:

```text
DenotationalEquality
!= ContextualEquivalenceByNecessity.
```

No universal `Equivalent:Boolean` exists without a declared semantics/query.

---

# 7. Specification is not semantics

## C-F15 — many implementations satisfy one Hoare-style contract

A specification such as a pre/postcondition can be satisfied by many operationally distinct implementations.

Therefore:

```text
SameSpecification
!= SameProgramSemanticsByIdentity.
```

## C-F16 — semantics can exist without the desired specification

A program can have a precise semantics yet violate its intended contract.

Therefore:

```text
SemanticMeaning
!= SpecificationSatisfaction.
```

## C-F17 — partial correctness vs termination

A partial-correctness assertion can state what holds if a program terminates without establishing that it terminates.

Therefore:

```text
PartialCorrectness
!= TotalCorrectnessByIdentity.
```

This independently supports Round A's separation of correctness from termination.

---

# 8. Type meaning does not replace behavioral meaning

## C-F18 — same type, different functions

Many different programs inhabit the same ordinary function type.

Therefore:

```text
TypeEquality
!= BehavioralEquivalenceByIdentity.
```

## C-F19 — well typed does not mean specification-correct

Type safety can exclude classes of runtime errors while leaving functional correctness unresolved.

Therefore:

```text
TypeSoundness
!= FullSpecificationCorrectness.
```

## C-F20 — parametricity gives relational constraints, not total behavior identity

Reynolds-style parametricity/abstraction can derive strong relational properties from polymorphic types and support representation independence.

But this does not imply that type alone identifies a unique implementation or cost behavior.

Therefore:

```text
ParametricityConstraint
!= CompleteComputationIdentity.
```

---

# 9. Representation independence is a direct anti-collapse pressure

## C-F21 — distinct ADT representations, same clients' observations

Two abstract-data-type implementations can use different internal representations yet be indistinguishable to clients when a suitable representation relation is preserved.

Therefore:

```text
InternalRepresentationIdentity
!= AbstractBehaviorIdentity.
```

This is a core reason that `representation` and `semantics` must be separate fields.

## C-F22 — representation relation itself is scoped

Two implementations may be equivalent under the exported abstraction boundary while distinguishable to a context that can inspect hidden representation.

Therefore:

```text
RepresentationIndependence
is boundary/context-relative.
```

Round A's ComputationalBoundary survives.

---

# 10. Translation correctness is a relation, not a new program identity

## C-F23 — compiler/transpiler translation

A translation has at least:

```text
source representation
source semantics
target representation
target semantics
translation mapping
preservation/refinement theorem.
```

Therefore:

```text
Translation
!= SemanticIdentityPrimitive.
```

## C-F24 — correctness can be compositional across passes

CompCert proves compiler correctness by composing pass-level semantic-preservation proofs.

This shows preservation is a relation that can compose across representation stages.

Therefore:

```text
OneCanonicalRepresentation
!= necessary for end-to-end semantic correctness.
```

---

# 11. Undefined behavior / nondeterminism pressures one-value semantics

## C-F25 — multiple allowed behaviors

A language/program can admit multiple possible behaviors due to nondeterminism or underspecification.

Therefore:

```text
ProgramSemantics
!= SingleOutputValueByIdentity.
```

This aligns with Round A.

## C-F26 — undefined/wrong behavior changes refinement direction

If the source semantics includes undefined behavior or going-wrong states, transformations may be allowed to produce more-defined target behavior under specific correctness theorems.

Therefore:

```text
SemanticRelationDirection
matters.
```

Equivalence, refinement, simulation and improvement must not be collapsed.

---

# 12. Round A is partially absorbed, but not eliminated

Programming-language semantics clearly owns part of what Round A called:

```text
TransitionOrBehaviorSemantics
ObservationOrEquivalenceSemantics.
```

Round C therefore **refactors** Round A rather than leaving it untouched.

But PL semantics does not eliminate:

```text
ComputationalBoundary
InteractionInterfaceWhenPresent
ContinuationOrTerminationSemantics
EnvironmentAssumptions
```

because these also apply to systems that are not conveniently modeled as source-language programs and because the computational boundary determines what counts as context/environment in the first place.

Thus:

```text
Round C overlaps and extends Round A;
it does not fully absorb Round A.
```

---

# 13. Round B remains orthogonal

## C-F27 — semantic preservation with changed optimization cost

A compiler optimization may preserve the source program's admitted observable behavior while changing time, memory, code size, energy or data movement.

Therefore:

```text
SemanticPreservation
!= ResourcePreservationByIdentity.
```

## C-F28 — same contextual behavior, different complexity

Two contextually equivalent implementations can have radically different asymptotic costs.

Therefore:

```text
ContextualEquivalence
!= ComplexityEquivalence.
```

## C-F29 — resource-sensitive semantics is optional enrichment

A semantic model can deliberately include cost, probability, timing or resource annotations, but ordinary semantics need not.

Therefore:

```text
ResourceAwareSemantics
!= UniversalSemanticsRequirement.
```

Round B remains a separate burden.

---

# 14. Agent-era representation does not create a new semantic primitive

## C-F30 — generated code

An Agent/LLM can emit source code, plans, DSL expressions, SQL, proof terms or Tool calls.

The generated representation still requires:

```text
language/schema interpretation
well-formedness/admission
semantic meaning
execution/translation relation
```

Therefore:

```text
AgentGeneratedRepresentation
!= NewAgentEraSemanticKind.
```

## C-F31 — natural language can be program-adjacent without being self-interpreting

A natural-language instruction may be interpreted by an Agent/Harness into actions or code, but the text alone does not uniquely determine an executable computational semantics without an interpreter/model/context.

Therefore:

```text
NaturalLanguageText
!= SelfContainedProgramSemanticsByIdentity.
```

Harness owns the current model/provider interpretation mechanism; Computing can study the representation-to-semantics relation abstractly.

---

# 15. Strong surviving candidate

Programming-language semantics as a universal foundation is rejected.

A broader Computing-owned responsibility survives:

```text
ComputationalInterpretationAndSemanticRelationResponsibility
```

For a computational representation/specification claim, enough of the following must be declared:

## 15.1 Representation / model domain

```text
what artifact/configuration/program/machine description is being interpreted?
```

## 15.2 Well-formedness / static admissibility when relevant

```text
what makes the representation syntactically/structurally/type valid enough to receive semantics?
```

Optional in models where every configuration is admitted.

## 15.3 Semantic interpretation relation

```text
what mathematical/operational relation maps or relates the representation to behavior/denotation?
```

## 15.4 Specification / property target

```text
what claim/property is being checked or proved about the meaning?
```

Optional if only raw semantics is requested.

## 15.5 Observation / context semantics

```text
which distinctions are observable to the query/context?
```

This partially subsumes Round A's observation/equivalence field.

## 15.6 Equivalence / refinement / preorder relation

```text
syntax equality?
contextual equivalence?
denotational equality?
simulation?
behavior inclusion/refinement?
```

Direction matters.

## 15.7 Translation / transformation mapping

```text
if representations change, what mapping relates source and target?
```

Optional when no transformation occurs.

## 15.8 Preservation / correctness claim

```text
what semantic property must the transformation preserve/refine?
```

## 15.9 Semantic regime/currentness/provenance

```text
which language/model/version/semantics definition is authoritative for the claim?
```

This prevents identical syntax from silently changing meaning across models/versions.

---

# 16. Why this is genuinely Computing-owned

Runtime can execute a concrete binary/process but cannot infer what source-level semantics, contextual equivalence or refinement theorem that execution is intended to satisfy.

Harness can interpret Agent-facing prompts/tools, but its current Provider/runtime behavior does not define general representation independence, compiler correctness or program semantics.

World owns physical facts, not the abstract interpretation relation that makes an artifact a program/model under a declared computational semantics.

Therefore a Computing-owned semantic responsibility survives owner subtraction.

---

# 17. Anti-collapse laws

```text
SourceProgramText != necessary condition for Computation
AlgorithmIdentity != ProgramTextIdentity
TextIdentity != SemanticIdentity
TextExistence != WellFormedProgram != AdmittedComputation
SyntacticDifference != SemanticDifferenceByIdentity
RepresentationDifference != BehavioralDifferenceByIdentity
SourceRepresentationIdentity != TargetRepresentationIdentity
CompilerCorrectness != RepresentationIdentity
SemanticPreservation != ExactBehaviorSetEqualityByNecessity
SemanticEquivalence != ResourceEquivalence
InternalTransitionEquality != necessary for SemanticPreservation
ProgramEquivalence requires declared observation/context semantics
TraceEquivalence != ContextualEquivalence
DenotationalEquality != ContextualEquivalenceByNecessity
SameSpecification != SameProgramSemantics
SemanticMeaning != SpecificationSatisfaction
PartialCorrectness != TotalCorrectness
TypeEquality != BehavioralEquivalence
TypeSoundness != FullSpecificationCorrectness
ParametricityConstraint != CompleteComputationIdentity
InternalRepresentationIdentity != AbstractBehaviorIdentity
RepresentationIndependence is boundary/context-relative
Translation != SemanticIdentity
ProgramSemantics != SingleOutputValue
Equivalence != Refinement != Simulation != Improvement
SemanticPreservation != ResourcePreservation
ContextualEquivalence != ComplexityEquivalence
NaturalLanguageText != SelfContainedProgramSemantics
```

---

# 18. Candidate deletion results

Rejected as universal Computing primitives:

```text
Program
SourceCode
Syntax
ProgrammingLanguage
Type
Specification
Denotation
OperationalTrace
ContextualEquivalence
SemanticEquality
CompilerTranslation
```

All remain useful scoped constructs.

---

# 19. Rival-model update

## M1 Function evaluation

Still rejected universal. Program semantics may denote functions in pure regimes but also effects, divergence, interaction and nondeterminism.

## M2 Controlled state transition

Strengthened but still incomplete: transitions require an interpretation/model and observation relation to become computational semantics rather than arbitrary World dynamics.

## M3 Information transformation

Still unresolved. Round C shows that even if information is transformed, representation and interpretation relations remain necessary to state computational meaning.

## M4 Effective procedure

Still partial. A procedure representation needs semantics; semantics need not be one terminating procedure.

## M5 Resource-bounded process

Round B strong burden remains separate; CompCert-style semantics can deliberately abstract execution time/memory.

## M6 Interactive process

Still a major regime; its observable behavior/context semantics are a specialization of the broader interpretation relation.

## M7 Physical realization

Still unresolved. Round C sharpens the anti-pancomputational issue: a physical trajectory becomes a computational realization only relative to some representation/model/interpretation relation, but the non-circular grounding of that relation is still open.

---

# 20. Relationship among A/B/C

Current best factorization:

```text
Round A
ComputationalBoundaryAndBehaviorResponsibility
  - boundary
  - interaction interface
  - continuation/termination
  - environment assumptions
  - behavior semantics      <overlap with C>
  - observation/equivalence <overlap with C>

Round C
ComputationalInterpretationAndSemanticRelationResponsibility
  - representation/model domain
  - well-formedness/admission
  - interpretation relation
  - specification/property
  - observation/context
  - equivalence/refinement
  - translation
  - preservation
  - semantics provenance/currentness

Round B
ComputationalResourceAndFeasibilityResponsibility
  - remains orthogonal
```

Do not merge A and C yet.
The overlap may mean:

```text
A becomes a behavioral specialization of a larger semantic-claim foundation
```

or:

```text
C is an upstream interpretation responsibility consumed by A.
```

Further pressure from numerical/approximate/probabilistic and physical computation is required.

---

# 21. Round C verdict

```text
ProgrammingLanguageSemantics as universal Computing foundation
= REJECTED

Program/Syntax/Type/Specification as universal primitive
= REJECTED

One universal equivalence relation
= REJECTED

Semantic preservation = representation preservation
= REJECTED

Semantic equivalence = resource equivalence
= REJECTED
```

Strong survivor:

```text
ComputationalInterpretationAndSemanticRelationResponsibility
```

Classification:

```text
STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE
OVERLAPS_AND_REFACTORS_ROUND_A
DOES_NOT_ABSORB_ROUND_B
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 22. Information gain

Round C information gain is **VERY HIGH**.

It shows that the current A/B architecture cannot simply be collapsed into `semantics`:

```text
semantics needs representation/interpretation/context/refinement structure,
while resource semantics can be intentionally abstracted away.
```

At the same time, Round C reveals that A's `behavior semantics` and `observation/equivalence` were not independent atoms; they sit inside a broader interpretation/semantic-relation theory.

This is genuine candidate refactoring, not only addition.

---

# 23. Next pressure — deliberately unselected

Do not automatically create `Round D = Numerical` by naming inertia, but numerical/approximate computation now has unusually high falsification value because it can attack all three survivors simultaneously:

```text
A: what counts as equivalent behavior under bounded error/convergence?
B: precision/error/sample/iteration as resources
C: exact denotation vs approximate implementation/refinement
```

Probabilistic/randomized computation is similarly strong because it pressures:

```text
distributional semantics
probabilistic equivalence/refinement
expected/high-probability resource bounds.
```

Physical/unconventional computation remains necessary to attack the interpretation-grounding problem.

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 24. Primary-source pressure anchors

Used as pressure sources, not ontology authority:

- C. A. R. Hoare, *An Axiomatic Basis for Computer Programming*, Communications of the ACM 12(10), 1969.
- Andrew M. Pitts, work on operational semantics and program/contextual equivalence, including *Operational Semantics and Program Equivalence*.
- John C. Reynolds, *Types, Abstraction, and Parametric Polymorphism*, IFIP 1983, and his broader work on semantics of types/representation abstraction.
- Xavier Leroy / CompCert, semantic-preservation proofs relating CompCert C source ASTs to assembly ASTs through formal semantics and observable behaviors.
