# Computational Possibility — Derived Transport & Capability Calculus v1

## 1. Status and purpose

This document materializes derived laws that survived the 2026-08-19 achievability / quantifier / transport / capability destructive audit.

It does **not** introduce a numbered Foundation, a ninth computational-situation axis, a universal capability datatype, a theorem engine, or a new specialist route. The eight canonical coordinates remain responsibility/coverage projections. The calculus below states how already constituted CP claims compose, transport, refine and preserve theorem meaning across deterministic, relational, interactive, promise-oracle, stateful and stochastic cases.

## 2. Claim formation precedes possibility truth

`Achievable` is a proposition over an already constituted computational situation, not a total Boolean predicate over arbitrary descriptions.

A useful formation judgment is:

`C : ConstitutedComputationalSituation`.

Only after this judgment is justified may CP form:

`Achievable(C)`

and

`Impossible(C) := not Achievable(C)`.

Constitution is load-bearing but not a requirement to fill eight fixed fields. The source meaning, obligation scope, witness grammar, information/process assumptions, quantifiers and resource structure must be explicit only where they affect the theorem.

Permanent controls:

- `Underconstituted != Impossible`.
- `NoWitnessFound != NoWitnessExists`.
- `NotEstablishedAchievable != Impossible`.
- `UndefinedOutsideDeclaredDomain != Failure`.

Research/evidence standing such as OPEN, UNKNOWN or PARTIAL is epistemic metadata about a well-formed proposition; it is not a third object-level computational truth value.

## 3. Guarded quantified achievability

For a constituted situation:

`Achievable(C) iff exists w in Adm(C) such that w satisfies the complete constituted obligation/resource contract.`

The outer existential is a **guarded strategy normal form**. It must not hide theorem-bearing quantifier/dependency structure inside an opaque satisfaction predicate.

For example:

`exists M forall x ...`

is not interchangeable with:

`forall x exists M_x ...`.

Likewise adversarial roles, chance scope, uniformity, revelation order, causal dependency, family quantification and interactive alternation must remain explicit/recoverable through `O`, `I`, `G`, `P` and related declared structure.

Strategy packaging may compress alternating choices into one strategy witness only when the strategy's dependency and information restrictions are preserved.

Permanent controls:

- `QuantifierStructure != OpaqueSatisfactionPredicate`.
- `GlobalPackaging != GlobalInformationAccess`.
- `WitnessExistence != WitnessDiscoverability`.

## 4. Joint and contextual admissibility

Separate component witnesses do not automatically form an admissible composite witness.

`Achievable(C1) and Achievable(C2)` does not by itself imply achievability of a declared composition.

A composition/wiring contract may constrain semantic interfaces, information visibility, causal dependency, synchronization, randomness, state, resource aggregation and contextual assumptions. These requirements are cross-coordinate admissibility conditions rather than a new CP axis.

Permanent controls:

- `ComponentwiseAchievability != CompositionalAchievability`.
- `StandaloneSatisfaction != ContextualSatisfaction`.
- `TypeCompatibility != DependencyCompatibility`.
- `PerComponentProbability != JointProbability`.
- `LocalStrategyTuple != UnrestrictedGlobalStrategy`.

## 5. Capability interaction contracts

A higher-order client/reduction may consume a capability rather than a single ordinary witness. Such a capability must be constituted by the interaction semantics that are theorem-bearing in that case.

The umbrella notion **Capability Interaction Contract** is derived and technology-neutral. It does not prescribe a universal schema. Depending on the theorem family, the load-bearing contract may include:

- client/environment assumptions and admitted operation/query scope;
- response/output obligations;
- role and choice authority;
- information, visibility and causal dependency;
- selection, consistency, state and history rules;
- operational totality/termination envelope;
- fairness/liveness or whole-history acceptance where relevant;
- stochastic law/correlation semantics;
- quantitative error/resource/performance structure.

Its `BehaviorSemantics` may be presented by a function, relation, selector class, realizer class, transition system, traces/fair traces, strategies, trajectories, stochastic kernels/laws, or another theorem-appropriate object. No one representation is canonical.

### Relational / multivalued providers

A relation `B(q)` states which outputs are valid, but does not determine who selects an output or how repeated calls are coordinated.

For a generic provider-parametric capability, a client/reduction must be correct for every complete provider behavior admitted by the declared contract, not merely for one favorable selector.

Permanent controls:

- `ValidOutputRelation != SelectionSemantics`.
- `OneSelectorReduction != ProblemLevelReduction`.
- `RelationalOutput != AdversarialChoice` — existential, universal/provider-parametric, stochastic and strategic selection roles must be constituted explicitly.

### Stateful providers

Pointwise response validity does not determine history validity. A sequence of locally valid responses may violate consistency, commitment, conservation, synchronization, state-transition or protocol-history constraints.

Permanent controls:

- `PointwiseValidity != HistoryValidity`.
- `FinitePrefixValidity != LivenessValidity`.

Hidden implementation state is not automatically CP-semantic. State-machine and extensional trace/behavior presentations may represent the same capability when qualified semantic/computational transport preserves all theorem-bearing distinctions.

### Stochastic providers

Per-call marginals and trace support do not determine interactive stochastic capability. Shared versus fresh randomness, correlation, adaptive conditioning and scheduler information may change computational truth.

For an adaptive client strategy `pi` and an admitted provider law/kernel `kappa`, their interaction induces a transcript law `P^(pi,kappa)`. A robust theorem has the general shape:

`exists pi; forall admitted provider laws kappa: declared probability/expectation/tail obligation holds under P^(pi,kappa)`.

The universal provider-law quantifier and the probability/expectation aggregation operator must not be conflated.

Permanent controls:

- `PerCallMarginals != JointLaw`.
- `SupportEquivalence != StochasticCapabilityEquivalence`.
- `StaticOutputDistribution != InteractiveStochasticCapability`.
- implicit fresh/independent randomness is forbidden when correlation is theorem-bearing.

## 6. Typed transport

A CP transport is a typed higher-order witness/transformer between constituted claim scopes. A useful transport claim exposes what is being translated.

For reductions this may include two opposed directions:

- an instance/obligation/query translation from source task toward target task;
- a witness/solver/capability lift from target capability back to a source witness/capability.

Thus a single unqualified `source -> target` arrow can be misleading.

A sound transport identifies, where load-bearing:

- source and target claim scopes;
- the translated object kind (instance, obligation, witness, capability, behavior contract, etc.);
- parametric witness/capability transformation;
- promise/domain and solution coverage;
- SCD/source semantic-preservation references;
- CP information/dependency/causal/quantifier preservation;
- optional contextual closure;
- optional quantitative overhead/distortion/domination/reflection.

Permanent controls:

- `NamedWitnessConstruction != ParametricReduction`.
- `OverlapCorrectness != PromiseCoverage`.
- `PromiseProblemSolver != OracleCapability`.
- `PromiseCorrectness != OracleSubstitutability`.

## 7. Promise-oracle and higher-order access

`oracle access to B` is underconstituted if the query/access semantics are theorem-bearing but unstated.

Relevant promise-oracle modes include, without making them exhaustive primitives:

- strict/validated access, where relied-on queries remain inside the promise;
- loose access, where outside-promise answers are unconstrained and the client must be robust to all admitted response behaviors;
- completion-consistent access, where an oracle supplies a total extension satisfying the promise commitments.

Equivalences between these modes are theorem- and regime-specific and must not be generalized by vocabulary alone.

For Turing-style composition, an inner reduction must often provide a substitutable **capability lift** rather than merely solve the intermediate problem once:

`Cap(C) -> Cap(B) -> Sol(A)`.

If the outer client can issue calls outside the intermediate correctness domain, the produced capability must still satisfy the required operational/access contract there.

## 8. Capability refinement and substitution

Raw behavior-set inclusion is a valid simplification only after client/environment assumptions and observation scopes are aligned.

In general, substitutability has assumption/guarantee polarity:

- a replacement provider must not require stronger client/environment assumptions than the required slot permits;
- under those admitted assumptions, it must not provide weaker guarantees than the required contract.

When assumptions and behavior types are aligned, a narrower admitted provider-behavior/law class represents a stronger provider guarantee and may safely fill a slot whose client was proved robust against a broader required class.

Permanent controls:

- `FewerBehaviors != StrongerProvider` unless assumptions/scopes are aligned.
- `ProviderGuaranteeStrength != ClientRobustnessStrength`.

Approximate provider substitution is quantitative theorem transport, not ordinary inclusion. A metric/divergence or other distortion relation must be paired with an explicit property-sensitivity theorem; CP assumes no universal stochastic or behavioral metric.

## 9. Contract-demand refinement

For two constituted claims with aligned witness meaning, define the derived successful-witness projection:

`Sol(C) = { w in Adm(C) | w satisfies C }`.

If `Sol(C1) subseteq Sol(C2)`, then `C1` is locally more demanding than `C2`. This yields:

`Achievable(C1) -> Achievable(C2)`

and

`Impossible(C2) -> Impossible(C1)`.

This local preorder explains monotonicity of broader committed domains, stricter output obligations, higher success thresholds, tighter resource/error bounds, weaker information access and larger adversary/context classes when other structure is fixed.

It must not be conflated with other orderings.

Permanent controls:

- `AssumptionStrength != ObligationStrength`.
- `RegimePowerOrder != ContractDemandOrder`.
- `ContractDemandOrder != ComputationalHardnessOrder`.

A narrower promise is usually a stronger input assumption but a weaker computational demand. A stronger regime allows more witnesses and therefore increases capability/power while making the fixed-obligation feasibility demand easier.

## 10. Theorem variance induced by transport

A sound witness-preserving transport `tau : C1 -> C2` induces multiple theorem actions rather than multiple primitive transport species.

### Qualitative

Forward witness preservation yields:

`Achievable(C1) -> Achievable(C2)`.

By contraposition over constituted, scope-aligned claims:

`Impossible(C2) -> Impossible(C1)`.

Thus positive achievability is covariant on the evidence arrow while impossibility is contravariant at theorem level.

### Quantitative

Upper-bound transport requires forward resource/performance domination.

Lower-bound transport requires the corresponding reverse candidate coverage/reflection sufficient to show that a hypothetical cheap target witness would induce a forbidden cheap source witness.

Permanent controls:

- `OneWaySimulation != ComputationalEquivalence`.
- `ComputabilityEquivalence != ComplexityEquivalence`.
- `SemanticEquivalence != ComputationalEquivalence`.

Bidirectional qualitative transport may induce achievability equivalence without making the transport artifacts literal inverses. Quantitative or contextual equivalence requires the corresponding stronger two-way burdens.

## 11. Transport composition

Transport composition is partial and typed, not an unconditional algebraic product.

For `tau12` followed by `tau23`, the produced middle contract must satisfy/refine the contract consumed by the second transport. Compatibility may require:

- SCD/source semantic/interface refinement;
- CP witness/capability admissibility;
- scope/promise coverage;
- quantifier/dependency/information/causal compatibility;
- behavior/assumption-guarantee substitutability;
- resource/error distortion composition;
- contextual closure where claimed.

Syntactic function composition alone does not establish theorem transport.

Permanent controls:

- `SyntacticComposition != SoundTransportComposition`.
- `SameMiddleLabel != ComposableMiddleContract`.

Identity-like and associative transport structure may exist within a fixed theorem family and equality/preservation notion, but current CP does not canonicalize a category, functor, naturality ontology or universal transport algebra.

## 12. Qualified presentation invariance

Absolute presentation invariance is false. Semantic correspondence alone does not force computational equivalence when representation translation, information topology, causal structure or resource scaling changes.

A claim family may be transported across two presentations only when the relevant bidirectional semantic/computational preservation burden is established.

Useful strength levels are:

1. semantic correspondence;
2. qualitative computational/achievability equivalence;
3. quantitative/resource equivalence under declared distortion;
4. contextual/compositional equivalence under admitted contexts.

`AxisPlacement != ComputationalTruth`: randomness, state or interface details may be factored differently across `I/G/P/Phi` provided a qualified structure-preserving transport shows the theorem-bearing contract is preserved.

## 13. Multi-order map

CP deliberately keeps several order-like structures distinct:

1. **Contract-demand refinement** — local entailment/successful-witness inclusion for aligned claims.
2. **Provider guarantee/refinement** — substitutability under assumption/guarantee and behavior/law semantics.
3. **Client robustness** — tolerance of broader admitted provider/environment behavior.
4. **Regime computational power** — inclusion of scoped achievability spectra `Power_U`.
5. **Reduction / hardness order** — induced by an explicitly declared reduction/transport family.
6. **Resource/performance preorder/frontier** — declared in `Phi`, possibly vectorial or only partially ordered.

No universal scalar 'hardness' or unqualified stronger/weaker relation merges these structures.

## 14. Owner boundaries

The calculus does not move truth between owners.

- SCD/source owners retain meaning, representation, semantic refinement/equivalence and preservation truth.
- CP owns formal, regime-relative witness/capability admissibility, achievability, reduction/transport burden and derived computational orders.
- Runtime owns actual execution, resource availability/consumption and attempt evidence.
- Interlocus owns actual reachability/topology/routing/communication capability.
- World owns physical/substrate realizability.
- Harness owns concrete agent/tool/run orchestration.
- Game/Mechanism/source owners retain strategic/payoff/environment semantics where applicable.

Shared transport grammar does not imply shared truth ownership.

## 15. Architectural standing

Rounds 1–11 found substantial new derived structure but no deletion-essential CP primitive outside the current architecture.

Therefore:

- `NumberedFoundationCount = 0` remains;
- `Foundation0 = NOT_ADMITTED` remains;
- no ninth computational-situation axis is admitted;
- the eight coordinates are best treated as current responsibility/coverage projections rather than proven orthogonal, minimal or uniquely factorized dimensions;
- the project remains `closed architecture -> open derived theory`.

A future architecture reopen still requires a concrete matched-world, theorem-independent structural/boundary falsifier rather than additional specialist richness.