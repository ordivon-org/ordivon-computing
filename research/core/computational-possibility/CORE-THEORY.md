# Computational Possibility — Canonical Core Theory v1

## 1. Status of this document

This is the canonical first statement of the current Computational Possibility theory surface. It compresses already established research; it does not introduce a new Foundation, specialist result, owner transfer, or theorem claim.

The project remains zero-Foundation. The purpose of the core theory is to state, in one place, the typed computational situation, admissible-witness semantics, and the main derived structures that survive the completed architecture/falsification programme.

## 2. Computational situation

A computational claim is interpreted relative to an explicitly declared computational situation

`C = <Sigma, I, G, P, O, T, Phi, A_ext>`

where the coordinates have the following roles.

### `Sigma` — source / target semantics and representation

The constituted meaning, representation and satisfaction/evaluation semantics needed to state the computational obligation. These semantics are imported from SCD/source/shared owners rather than re-owned by Computational Possibility.

### `I` — information / revelation interface

The information available to the computational witness: observations, queries, samples, messages, advice, side information, copy/oracle access, revelation order and related access structure.

### `G` — witness / strategy / family / trajectory grammar

The theorem-independent grammar of admissible computational witnesses and their closure/composition rules. A witness may be a program, strategy, protocol, circuit/family object, sampler, controller, interactive/distributed process, approximation procedure, trajectory, transformer, or higher-order/meta construction when explicitly admitted by `G`.

### `P` — interaction / environment / process / causal-availability structure

The declared process in which computation unfolds: roles, events, interaction, adversarial/stochastic/endogenous evolution, causal availability, synchronization/commit rules, histories or other process grammar. No universal scalar time or classical event-poset assumption is required.

### `O` — obligation / output / benchmark / quantifier structure

The constituted success condition: decision, search, realization, semidecision, approximation, sampling, certification, competitive/regret target, totality, probability threshold, family-level condition, or another explicitly typed obligation and quantifier pattern.

### `T` — transformation / transport structure

Any reduction, simulation, translation, transformer, capability-access, semantic-preservation or distortion structure that is itself part of the formal computational claim. Cross-owner actual applicability is handled separately by the theorem-transport bridge.

### `Phi` — resource / performance structure, composition and aggregation

The declared abstract resource/performance constraints and their algebra: scalar/vector/preorder, worst/expected/tail/smoothed, amortized/cumulative/regret, reusable/consumable/catalytic/convertible resources, aggregation and trade-off structure as appropriate.

### `A_ext` — actual-realization external-owner boundary

A marker that actual capability, execution, physical realization, connectivity, orchestration and other current operational facts remain externally authoritative. `A_ext` prevents formal computational possibility from being silently identified with actual realization.

The eight coordinates are a current coverage schema, not eight Foundations, proven orthogonal/minimal dimensions, or eight universal data fields. Internal representations may refine, combine or refactor them provided the theorem-independent distinctions remain recoverable through an appropriate preservation/transport argument.

## 3. Claim formation and admissible witness space

`Achievable` is formed only for an already constituted computational situation. A useful judgment is `C : ConstitutedComputationalSituation`; underconstituted descriptions do not become computational impossibility claims merely because no witness can yet be stated or found.

Constitution is load-bearing but does not require eight fixed fields. Only the semantic, obligation, witness, information/process, quantifier and resource distinctions that affect the theorem must be explicit/recoverable.

For a declared situation `C`, let `Adm(C)` denote the witnesses admitted by its representation, information, witness-grammar, process and other formal conditions.

A witness `w` is not admitted merely because it makes the target theorem true. Admission must be independently constituted by `Sigma`, `I`, `G`, `P`, `T` and other declared coordinates.

This is the core anti-stuffing condition:

`theorem conclusion != witness-admission rule`.

Dynamic or self-modifying computation is permitted when the changing state/rules form part of an admissible trajectory under a fixed theorem-independent outer transition or whole-history condition. Self-ratifying future rules without such a condition are underconstituted, not a stronger regime.

## 4. Achievability

The central derived relation is ordinary typed witness existence:

`Achievable(C)  iff  exists w in Adm(C) such that w satisfies O and Phi under the constituted semantics of C.`

This outer existential is a guarded strategy normal form, not permission to hide load-bearing quantifier, role, uniformity, visibility, probability or causal-dependency structure inside an opaque satisfaction predicate. Such structure must remain explicit/recoverable through the constituted situation.

Where a problem/regime/constraint notation is useful, the historical style

`CExists_R(Omega; Gamma)`

or equivalent `Achievable_R(Omega; Gamma)` may be used as shorthand. It does not denote a primitive relation beyond ordinary existential quantification over admissible witnesses.

This definitional eliminability is why historical `AlgF0 — Regime-Relative Computational Existence` is preserved as genuine discovery history but is withdrawn/superseded as a numbered Foundation.

## 5. Impossibility

For the same declared situation:

`Impossible(C)  iff  not Achievable(C)`.

Impossibility therefore introduces no second primitive. The negative claim is only as strong as the declared computational situation. A restricted/proxy/proof-method barrier cannot be promoted to a target-regime impossibility without an explicit transport/coverage argument.

Permanent controls:

- `Underconstituted != Impossible`.
- `NoWitnessFound != NoWitnessExists`.
- `ProofMethodBarrier != ComputationalLowerBound`.
- `ProxyModelBarrier != TargetRegimeComputationalBarrier`.

## 6. Complexity, bounds and frontiers

Complexity is the structure obtained by varying `Phi` while the relevant obligation and other coordinates are controlled.

For a constraint profile `phi`:

`Achievable(C | Phi <= phi)`

or the appropriate preorder/vector/aggregation analogue asks whether a witness exists within that constraint region.

From these constraint-indexed achievability sets arise:

- upper bounds;
- lower bounds;
- complexity classes;
- expected/tail/amortized/cumulative regimes;
- multi-resource trade-offs;
- Pareto and other frontiers.

No universal scalar resource, total order, attained optimum, or single cost semantics is assumed.

## 7. Transformations, reductions, simulations and capability substitution

A reduction/simulation/translation is a typed higher-order computational witness or transformer between declared situations. The translated object kind must be clear where direction matters: an instance/obligation map and a solver/witness/capability lift may run in opposite directions.

At minimum, a useful transformer claim identifies, where load-bearing:

- source and target obligations/situations/scopes;
- the object being translated (instance, obligation, witness, capability, interaction contract or related typed object);
- admitted access to source/target capabilities or witnesses;
- the parametric witness/capability transformation or simulation;
- promise/domain, solution and candidate coverage needed by the theorem family;
- semantic/contract preservation references where required;
- information/dependency/causal and contextual preservation where required;
- resource/performance overhead, domination, reflection or distortion where claimed.

Higher-order capabilities may require a constituted interaction contract covering role/input assumptions, allowed behavior/laws, history/state/consistency, visibility/causality, operational envelope and stochastic/liveness structure where theorem-bearing. Pointwise output validity alone is not a universal capability semantics.

Transport composition is partial and typed: a produced middle contract must satisfy/refine the contract consumed by the next transport. Syntactic function composition or a shared middle label is insufficient without the relevant semantic, admissibility, scope, dependency, behavior and quantitative compatibility.

A sound witness-preserving transport from `C1` to `C2` yields `Achievable(C1) -> Achievable(C2)` and, by contraposition over constituted scope-aligned claims, `Impossible(C2) -> Impossible(C1)`. Quantitative upper transport requires forward domination; quantitative lower transport requires suitable reverse candidate coverage/reflection.

Thus reduction existence is itself an achievability claim. Transformation soundness may depend on SCD/source-owned preservation facts, which are referenced rather than redefined by CP. Full derived laws are materialized in `DERIVED-TRANSPORT-CAPABILITY-CALCULUS.md`.

## 8. Comparative computational power

Computational power is always scoped to an explicit obligation universe `U` and the other controlled coordinates.

Define the achievability spectrum

`Power_U(R) = { O in U | O is achievable under R and the declared surrounding coordinates }`.

Then a comparative-power statement such as

`R1 <=_U R2`

means the relevant achievability spectrum of `R1` is included in that of `R2` under the declared scope.

There is no context-free universal computational-power ordering.

## 9. Hardness, completeness and degree structures

Given a declared transformation/reduction relation, hardness, completeness, equivalence classes, degrees and related orders are induced structures over obligations/regimes. They do not require additional primitive CP relations.

Lower-bound transfer is valid only when the transformer/coverage conditions support the required contrapositive reasoning; a proof barrier or restricted-model barrier alone is insufficient.

## 10. Higher-order, uniform, advice, preprocessing and dynamic forms

The current core admits these phenomena through typed structure rather than new Foundations:

- uniform/nonuniform distinctions through quantifier order and witness-family grammar;
- advice/preprocessing/training through explicit information/interface and indexing structure;
- online/causal computation through revelation/process/causal-availability constraints;
- distributed computation through roles, local information, interaction and family witnesses;
- sampling through output-law obligations, randomness/interface structure and sampler/trajectory witnesses;
- Type-2/infinite/limit computation through representation, oracle/information interfaces, higher-order names and limit/tower witness grammars;
- meta/self-modifying computation through explicit outer trajectory/admission semantics;
- witness discoverability through higher-order search witnesses rather than a new existence primitive.

## 11. Distinctions preserved by the theory

A unified existential engine does not identify computational situations that differ in load-bearing coordinates. The project explicitly preserves distinctions such as:

- `Decision != Semidecision` when output/evidence semantics differ;
- `WitnessExistence != WitnessDiscoverability`;
- `Randomized != Deterministic` when witness/interface/resource structure differs;
- `Offline != Online/Causal` when revelation/causal availability differs;
- exact represented output, effective arbitrary-precision approximation and convergence-only obligations when their representation/guarantees differ;
- formal achievability and actual realization;
- `QuantifierStructure != OpaqueSatisfactionPredicate`;
- `ComponentwiseAchievability != CompositionalAchievability`;
- `ValidOutputRelation != SelectionSemantics`;
- `PointwiseValidity != HistoryValidity`;
- `PerCallMarginals != JointLaw`;
- `AssumptionStrength != ObligationStrength`;
- `RegimePowerOrder != ContractDemandOrder`;
- `ContractDemandOrder != ComputationalHardnessOrder`.

The research task is to locate the responsible coordinate and derived transport/admissibility law, not to erase the distinction or invent a new existential primitive for every case.

## 12. Actual applicability

Formal `Achievable` / `Impossible` claims do not automatically apply to a concrete system.

The derived Applicability / Theorem-Transport bridge enforces:

- constructive/upper: `formal -> actual` implementation/realization;
- impossibility/lower: `actual -> formal` coverage/abstraction;
- quantitative upper: explicit domination mapping;
- quantitative lower: explicit reflection mapping.

External-owner premises remain authority/version/scope qualified. `SchemaValid`, `TheoremTrue`, `PremisesTrue` and `ActuallyRealized` are distinct claims.

## 13. Current theory standing

The completed whole-owner saturation programme found no deletion-essential ninth axis or numbered Foundation under current evidence.

Therefore:

- `NumberedFoundationCount = 0`;
- `Foundation0 = NOT_ADMITTED`;
- the eight-axis computational-situation schema is the current canonical architecture;
- the core remains a non-numbered Derived-Theory Basis;
- specialist mathematics remains open-ended;
- architecture reopens only on a concrete matched-world, theorem-independent structural, owner-boundary or equivalent falsifier.

This is **closed architecture, open derived theory**, not a claim that computation or theoretical computer science is exhausted.
