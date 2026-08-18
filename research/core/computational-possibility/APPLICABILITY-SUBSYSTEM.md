# Computational Possibility — Applicability / Theorem Transport Subsystem v1

## 1. Purpose

Applicability is the first-class project boundary between formal Computational Possibility claims and concrete targets owned elsewhere.

It answers one question:

> Given a scoped formal computational claim and a scoped actual target, what exact consequence may be transported, under which directional burden and owner-authoritative premises?

This subsystem does **not** make actual system facts into CP truth. It controls the conditions under which CP may consume external owner facts and emit a bounded transported consequence.

Applicability is a **derived cross-owner subsystem**, not a Foundation and not a second computational-possibility relation.

## 2. Truth-role map

The subsystem has four distinct truth roles.

### A. CP derived-theory authority

[APPLICABILITY-THEOREM-TRANSPORT-BRIDGE](APPLICABILITY-THEOREM-TRANSPORT-BRIDGE.md) is the owner-native statement of the transport structure:

- `ClaimScope`;
- `TargetScope`;
- `TransportBurden`;
- `PremiseEvidence`;
- `Verdict`;
- optional quantitative structure nested under `TransportBurden`.

The relevant project-level constitutional law is CP-C5 in [PROJECT-CONSTITUTION](PROJECT-CONSTITUTION.md).

### B. CP project navigation / recovery

This document explains how the bridge, artifact and external owner premises fit together. It is a project presentation/recovery surface. It does not supersede the bridge or create new semantic fields.

### C. Engineering-consumption artifact

The existing thin artifact lives at:

[`../../experiments/computational-applicability-transport-v0/`](../../experiments/computational-applicability-transport-v0/)

Its components are:

- [`SPEC.md`](../../experiments/computational-applicability-transport-v0/SPEC.md) — normative engineering specification derived from the bridge;
- [`computational-applicability-transport-v1.schema.json`](../../experiments/computational-applicability-transport-v0/computational-applicability-transport-v1.schema.json) — Draft 2020-12 structural schema;
- `fixtures/valid/` — five intended-valid conformance examples;
- `fixtures/invalid/` — seven intended-invalid deletion/direction/quantitative examples.

The artifact is derived instrumentation. It is not the semantic owner of theorem truth, premise truth, currentness or external authority.

### D. External owner authority

Actual facts remain with their owners. Applicability records may reference them with scope/currentness, but never convert them into timeless CP truth.

Examples:

- meaning/equivalence/preservation -> SCD/source owners;
- actual execution/resource availability -> Runtime;
- actual reachability/topology/bandwidth -> Network;
- physical realizability -> World;
- concrete orchestration/provisioning -> Harness;
- security/authority/adversarial truth -> Security;
- empirical/statistical validity -> Statistics/Epistemology;
- domain-specific target/value truth -> source-domain owner.

`Reference != Ownership`.

## 3. Canonical semantic blocks

An applicability claim is organized around five semantic blocks.

### `ClaimScope`

States exactly what formal claim is being consumed, including theorem kind, computational-regime reference, obligation, relevant constraint/resource functional, quantification domain and aggregation scope.

Its purpose is to prevent scope inflation such as:

- instance -> family;
- finite -> asymptotic;
- bounded -> unbounded;
- expected -> worst/tail;
- one aggregation semantics -> another.

### `TargetScope`

Identifies the actual owner-scoped target, revision/version and relevant configuration scope.

Its purpose is to prevent stale or timeless applicability claims.

### `TransportBurden`

States the directional witness relation required to carry the claim across the formal/actual boundary.

This is theorem-family-sensitive and must never be replaced by a generic `mapping=true` field.

### `PremiseEvidence`

References owner-authoritative premises with scope/currentness and a local applicability status. The applicability record does not overwrite those owner claims.

### `Verdict`

States the exact bounded consequence and one of:

- `APPLIES`;
- `DOES_NOT_APPLY`;
- `UNRESOLVED`;
- `EXPIRED`.

A verdict is about transport of the scoped computational claim only.

## 4. Directional transport law

The core law is asymmetric.

### Constructive / upper claims

To move from formal achievability to actual achievability, CP needs:

`formal witness -> actual witness`.

This is an implementation/realization burden.

For quantitative upper claims, the mapping must also support an explicit upper-domination relation connecting formal resource/performance claims to actual measurement semantics.

### Impossibility / lower claims

To move from formal impossibility to actual impossibility, CP needs:

`relevant actual candidate witness -> formal witness`.

This is an actual-to-formal coverage/abstraction burden.

For quantitative lower claims, the mapping must support an explicit lower-reflection relation such that a hypothetical too-cheap actual witness would induce a formal witness contradicting the formal lower bound.

Therefore:

`FormalToActualImplementability != ActualWitnessCoverage`.

A constructive implementation map alone can never establish a lower bound over all actual implementations.

## 5. Verdict semantics

### `APPLIES`

The scoped transport burden and required premises are discharged for the stated target/currentness fence. It authorizes only the exact transported consequence.

It does **not** mean:

- production-ready;
- authorized/permitted;
- secure;
- economically valuable;
- globally optimal;
- physically realized beyond the referenced premises.

### `DOES_NOT_APPLY`

The theorem/claim may remain true in its formal scope, but the target/scope/transport requirements do not support the requested consequence.

### `UNRESOLVED`

At least one required premise or transport obligation lacks sufficient current evidence. This is a valid fail-closed outcome, not falsity.

### `EXPIRED`

A previously usable applicability basis is stale relative to the current target/version/scope.

## 6. Currentness discipline

Applicability is inherently currentness-sensitive.

A record must not infer:

`HistoricalCapability -> CurrentCapability`.

A previous `APPLIES` verdict may become `EXPIRED` when the target or premise currentness fence changes.

Project formation, Host continuity, Git presence or a previously valid fixture does not refresh external owner premises automatically.

There is intentionally no automatic premise-refresh mechanism in v1.

## 7. Structural validation boundary

The machine-readable schema is deliberately narrow.

It may establish structural properties such as:

- required block presence;
- allowed theorem-kind/transport-direction combinations;
- presence of quantitative structure for upper/lower claims;
- verdict-shape consistency.

It cannot establish:

`SchemaValid == TheoremTrue`;

`SchemaValid == PremisesTrue`;

`SchemaValid == SemanticPreservationTrue`;

`SchemaValid == CurrentOwnerState`;

`SchemaValid == Authorized`.

The actual contract is therefore:

`normative bridge/spec + declarative structure + source-fenced evidence`,

not `schema -> automatic truth`.

## 8. Existing conformance set

The thin artifact currently preserves five intended-valid cases:

1. forward constructive / `APPLIES`;
2. backward lower-bound / `APPLIES`;
3. Runtime-resource / `UNRESOLVED`;
4. Windows-native stale target / `EXPIRED`;
5. finite-to-asymptotic mismatch / `DOES_NOT_APPLY`.

It also preserves seven intended-invalid structural cases:

- missing `ClaimScope`;
- missing `TargetScope`;
- missing `TransportBurden`;
- missing `PremiseEvidence`;
- missing `Verdict`;
- lower-bound wrong direction;
- upper-bound missing quantitative bridge.

These fixtures test structure and transport-family discipline. They do not prove real theorem applicability to any live owner target.

## 9. Anti-laws

Permanent subsystem controls include:

- `SchemaValid != TheoremTrue`;
- `SchemaValid != PremisesTrue`;
- `APPLIES != ProductionReady`;
- `APPLIES != Authorized`;
- `HistoricalCapability != CurrentCapability`;
- `OneSuccessfulRun != UniformFamilyAchievability`;
- `FiniteBenchmark != AsymptoticBound`;
- `SameTraceLanguage != StrategyPreservingTransport`;
- `FormalToActualImplementability != ActualWitnessCoverage`;
- `ExpectedBound != TailBound`;
- `AmortizedBound != PerOperationBound`.

These are guards against overclaim, not new CP primitives.

## 10. Engineering boundary

The current earned engineering level is exactly:

`normative spec + Draft 2020-12 schema + conformance fixtures`.

The following remain **NOT EARNED** without a concrete consumer falsifier:

- bespoke validator;
- service/API;
- database;
- MCP tool;
- global applicability registry;
- automatic theorem engine;
- automatic owner-state refresher;
- production admission/authority gate;
- first-class transport-composition graph.

A standard schema implementation may later be used for bounded structural validation if it becomes available through ordinary toolchain dependencies. No dependency or custom validator is justified merely to make the artifact self-validating.

## 11. Reopen conditions

Reopen this subsystem only if real dogfood identifies a concrete failure such as:

- a missing semantic role whose deletion causes an actual applicability overclaim;
- a theorem family whose sound transport direction cannot be represented by the existing directional variants;
- a quantitative application that cannot be expressed by current domination/reflection structure;
- an owner-currentness case that cannot be represented by scoped premise evidence;
- a Security/World/Agent/Runtime consumer case that falsifies a named existing bridge clause.

Convenience, desire for automation, more artifact instances, or availability of new tooling is not a semantic reopen condition.

## 12. First-reading usage

For a new applicability question:

1. read the formal claim from CP Core Theory / source theorem;
2. freeze `ClaimScope`;
3. identify the exact owner/version/configuration in `TargetScope`;
4. classify the theorem family as constructive/upper or impossibility/lower;
5. state the correct directional `TransportBurden`;
6. reference source-fenced `PremiseEvidence`;
7. add quantitative domination/reflection only when required;
8. return one bounded verdict;
9. never infer broader production/security/authority truth from that verdict.

This is the canonical project path from formal computational theory to actual-target applicability.
