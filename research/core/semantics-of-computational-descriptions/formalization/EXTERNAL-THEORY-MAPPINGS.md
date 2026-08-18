# External Theory Mappings — Reuse Before Invent

Status: **research navigation map**, not closure theorem.

SCD does not claim mature local mathematics as its invention. External theories are treated as formal suppliers/instantiations for responsibility regimes; they do not become SCD semantic owners.

## Relational / refinement / workflow regimes

Relevant mature traditions include refinement calculi, Unifying Theories of Programming (UTP), CSP behavioural refinement, and process-algebraic workflow specification/refinement.

Typical K0.2 mapping:

- `D`: program, specification, relational predicate or process;
- `Σ`: state/alphabet/behavioural model plus refinement or healthiness assumptions;
- `φ`: refinement/equivalence/property judgment;
- `v`: refinement/development/composition step;
- `μ`: often identity, embedding, refinement or conformance relation;
- `Δ`: proof premises/assumptions where currentness matters.

Implication for SCD: SCDF2/3 local composition/refinement mathematics should normally reuse these frameworks.

## Abstract Interpretation

Patrick Cousot and Radhia Cousot's abstract-interpretation programme supplies mature theory for abstraction/approximation, abstract domains, soundness and fixpoint approximation.

Typical mapping:

- `D`: concrete program or semantic object;
- `Σ`: concrete/abstract domains, order/fixpoint structures and interpretation rules;
- `φ`: property/invariant;
- `v`: abstraction/approximation regime;
- `μ`: abstraction/concretization or framework soundness correspondence;
- `Δ`: domain/soundness assumptions.

Implication: SCDF4 should not recreate lattice/fixpoint abstraction theory under SCD names.

## Verified translation / CompCert-style simulation

CompCert supplies formal source and target language semantics and proves compiler semantic preservation through forward/backward simulations and matching relations.

Typical mapping:

- `Ds/Dt`: source/target programs;
- `Σs/Σt`: source/target formal semantics and observable behaviours;
- `v`: compiler pass or whole compilation;
- `φ`: behaviour/property claim;
- `μ`: `match_prog`, `match_states`, forward/backward simulation and induced behaviour correspondence;
- `Δ`: compiler/pass preconditions and proof assumptions.

Implication: `μ` cannot be understood only as a literal claim-to-claim function. It is a framework-supplied SemanticCorrespondence witness family whose internal carrier can be states or behaviours.

## Institution Theory

Goguen/Burstall Institution Theory abstracts signatures, sentences, models and satisfaction and requires satisfaction coherence under change of notation.

Typical mapping:

- `D`: sentence, theory or specification;
- `Σ`: signature/notation, sentence/model spaces and satisfaction structure;
- `v`: signature/notation or institution morphism/change;
- `μ`: sentence translation plus model reduct/translation constrained by satisfaction coherence;
- `φ`: satisfaction/property claim.

Implication: `Σ` must be able to expose signature/vocabulary/interface structure when a framework requires it. No universal standalone vocabulary primitive is yet admitted.

## Truth Maintenance / ATMS

Doyle/de Kleer truth-maintenance traditions record justifications or assumption sets and revise belief standing when support changes.

Typical SCD use:

- `Δ`: explicit support/assumption structure;
- standing: derived from current support, not stored as timeless truth;
- branching contexts: alternative assumption sets may coexist.

Implication: dependency/currentness maintenance is not primitive SCD novelty. SCD must justify any additional contribution through typed computational-description semantics, contract/model scope and external owner authority.

## Interface theories / open components

Interface Automata and related interface theories provide mature machinery for behavioural compatibility and assumptions/guarantees between components.

Implication: SCDF2 open-interface formalization must reuse or directly compare against interface-theory structures before inventing SCD-specific component semantics.

## Type systems / static admissibility

Wright/Felleisen-style syntactic type-soundness traditions provide mature well-formedness/classification/soundness machinery for programming-language regimes.

Implication: SCDF6 does not own type checking itself. Its broader SCD role concerns static semantic admissibility/classification across heterogeneous ComputationalDescriptionRoles.

## Operational / contextual equivalence

Operational-semantics and program-equivalence traditions provide mature observational/contextual equivalence concepts and methods.

Implication: SCDF1/3 local observational relations are reuse territory; SCD's broader role is to type the observation environment and coordinate standing across heterogeneous regimes.

## Nominal techniques

Nominal sets, nominal logic, FreshML and nominal unification provide mature mathematics for names, binding, freshness, permutations and alpha-equivalence.

Implication: historical Name Identity/Generativity pressure cannot justify a new SCD Foundation merely from alpha-renaming/freshness difficulty.

# K0.2 conclusion from cross-framework mapping

K0.2 is best treated as a proof-obligation coordination interface:

```text
Situation S = (ρ ⊢ D @ Σ)
Claim     φ
Change    χ = (v, μ)
Support   Δ
Standing  Stand(φ | S, Δ)
```

The actual semantics and proof mechanisms remain framework-specific.
