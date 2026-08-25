# Semantic Preservation under Operational Reconfiguration — External/Internal Subtraction v0

Status: **research-only subtraction closeout**, 2026-08-25.

Question attacked:

> Is `SCD semantic preservation × Harness Context substitution/OPUR` a genuinely new theory seam, or mostly an owner-specific application of mature preservation/refinement/contract/reconfiguration theory?

Current answer:

> **Generic theory residual is not established. The seam is demoted to a natural owner-specific integration candidate.**

## 1. Mature external ancestors

### Refinement / data refinement

Classical refinement already asks when one representation/implementation may replace another while preserving externally relevant program behavior. Simulation obligations provide sufficient conditions; mutual refinement yields equivalence under the declared semantics.

This is structurally close to directional use-relative substitutability and directly subtracts generic novelty from `replacement that preserves obligations`.

### Behavioral subtyping

Liskov/Wing behavioral subtyping explicitly requires subtype objects to preserve behavioral properties of supertypes using specifications, invariants and constraints. Component replacement under a declared behavioral contract is mature theory.

### Verified compilation / transformation

CompCert proves semantic preservation pass-by-pass via forward/backward simulations: generated code preserves allowed source-program observable behavior/properties. Therefore `transformation changes representation but required observable semantics survive` is a canonical formal-methods problem, not a new SCD/Harness theory.

### Refactoring / behavior-preserving transformation

Refactoring theory centers behavior-preserving restructuring and has a large literature on what behavior means, preconditions, static/dynamic validation and formal proof. Again, representation/program structure may change while a declared observation contract survives.

### Bidirectional transformations / lenses

Lenses formalize source-view synchronization with laws such as GetPut and PutGet. Schema/view representations can evolve while consistency/round-trip properties constrain valid transformations. Database evolution work applies bidirectional transformations to co-existing schema versions and code/schema co-evolution.

### Dynamic Software Updating

DSU explicitly studies live code/data/type/state reconfiguration without stopping the running system. Correctness work uses client-oriented specifications to state which client-visible behaviors updated executions must preserve, and state-transfer systems explicitly transform old-version state into new-version representation.

### Contract-preserving runtime reconfiguration

Assume-guarantee/component-contract work explicitly treats replacement as safe when the new component satisfies the assigned contract; QoS/runtime adaptation work studies preserving contracts through dynamic reconfiguration. Thus `U-relative preservation across operational reconfiguration` is mature in generic form.

### Partial/unknown semantic preservation

Three-valued abstraction/model checking explicitly represents abstraction-induced information loss as `unknown`; definite results transport to the concrete system while unknown triggers refinement. Belnap–Dunn/four-valued logics explicitly distinguish true, false, both/conflict and neither/unknown across multisource information. Generic `do not collapse unknown/conflict` is mature.

## 2. Current Agent-era neighbors narrow TRAA novelty further

Current 2026 work also covers pieces that once looked unusually Agent-specific:

- evidence-force/warrant calibration: relevant evidence may under-warrant stronger relation/modality/scope/temporal/numeric claims;
- argument-level semantic roles + cross-step provenance + capability contracts for Agent authority;
- source-aware factuality verification for MCP traces;
- proof-carrying Agent actions with admissibility/approval/evidence checkpoints.

Therefore SCD must not claim novelty for generic provenance, role typing, warrant strength, proof obligations, source attribution, approval certificates or unknown preservation.

## 3. Harness already parameterizes the missing contract

Campaign 2 already states that Context substitution is relative to a bounded use contract U and that Harness must not invent arbitrary domain discriminants. If U cannot specify externally owned discriminants, an external decision contract is required.

Campaign 5 OPUR likewise preserves U-required obligations or explicitly rebinds/readmits them while keeping externally owned claims external.

This means:

`Harness needs an external semantic obligation`

is **not** sufficient evidence that SCD is a joint causal owner. The source/domain owner may directly supply the obligation.

## 4. Deterministic deletion probe

`scd_harness_deletion_probe.py` models an unsafe fluent fallback that drops required UNKNOWN standing and a safe fallback that preserves it.

When the source owner directly supplies U = `{current, preserves_unknown, authority_ok}`, a generic U-preservation checker rejects the unsafe fallback exactly as when the identical U is labeled SCD-provided.

Therefore:

`SemanticObligationPresent != SCDCausallyNecessary`.

SCD becomes deletion-essential only if it **derives/qualifies a semantic discriminant** that the source/use-contract owner cannot already supply at equivalent standing/cost and deleting that derivation changes the actual diagnosis/substitution/recovery decision.

## 5. What TRAA may still contribute

The strongest SCD-specific candidate remains narrower than generic semantic preservation:

- transformation/judgement-relative substitutability over heterogeneous owner-native descriptions;
- directional approximation rather than equality-only equivalence;
- strict separation of semantic adequacy from capability/permission/currentness/selection/execution;
- owner-qualified inferential standing/topology, including non-established bridges or undischarged obligations, when compressed Agent views otherwise invite illicit bridge completion;
- currentness/reopen implications when the authority/standing of the semantic bridge changes.

But every item has strong mature neighbors. The **combination** may be locally useful; literature novelty and cross-owner causal necessity remain open.

## 6. Strong external subtraction criterion

The seam should collapse to `ordinary owner-specific application of mature refinement/contracts` if a natural workload can be handled by:

1. source/domain owner supplies U/specification;
2. mature refinement/contract/preservation relation determines admissible replacement;
3. Harness performs bounded operational substitution/reconfiguration;
4. ordinary provenance/currentness references preserve owner evidence;
5. no SCD-specific semantic derivation changes the decision.

This is now the default null hypothesis.

## 7. SCD-positive promotion criterion

A natural case may promote SCD from adjudicative/supplier to causal only if all are true:

1. the target U contains a semantic distinction not directly available as a source-owner contract at equivalent standing/cost;
2. SCD qualification derives a directional preservation/non-entailment/support-closure fact needed by the decision;
3. deleting only that SCD fact causes an unsafe substitution, false promotion, missed recovery, or materially higher decision burden;
4. generic proof/warrant/provenance/task-fit controls do not match it;
5. result reproduces on at least one materially different owner/judgement morphology before any shared mechanism is proposed.

No natural case currently satisfies this gate.

## 8. Media status in this seam

Media is not automatically part of semantic reconfiguration. It becomes causal only if observer encounter/mediation after semantically valid reconfiguration changes the actual target relative to a generic task-fit representation baseline.

Thus the minimal plausible composition is not forced to be Media×SCD×Harness; it may be source×Harness, SCD×Harness, Media×Harness, or a larger source/Verify/World composition depending on the workload.

## 9. Current disposition

`GenericSemanticPreservationUnderTransformation = MATURE PRIOR`.

`GenericContractPreservationUnderReconfiguration = MATURE PRIOR`.

`UnknownConflictPreservation = MATURE PRIOR`.

`AgentProvenance/Warrant/AuthorityContracts = ACTIVE MATURE NEIGHBORHOOD`.

`SCD×Harness GenericTheoryNovelty = NOT ESTABLISHED`.

`SCD×Harness JointCapability = NOT ESTABLISHED`.

`SCD-as-provider-of-unique-semantic-discriminant = NATURAL CONSUMER HYPOTHESIS ONLY`.

The correct action is to wait for an owner-native natural case rather than construct a semantic-reconfiguration framework.
