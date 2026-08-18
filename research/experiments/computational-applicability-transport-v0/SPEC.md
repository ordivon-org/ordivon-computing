# Computational Applicability / Transport Artifact v1

## Status and ownership

This artifact is **derived Computational Possibility instrumentation**. It is not a Foundation, theorem prover, configuration registry, or authority gate.

Computational Possibility owns only the formal computational projection and the derived transport consequence. Other owners retain their truth:

| Concern | Owner |
|---|---|
| meaning, equivalence, refinement, preservation | Semantics of Computational Descriptions (SCD) |
| actual execution, lifecycle, resource availability/consumption | Runtime |
| actual reachability, topology, routing, communication capability | Network |
| physical realizability and physical-resource truth | World |
| concrete Agent/tool provisioning and orchestration | Harness |
| security/authority/adversarial truth | Security |
| empirical workload/distribution validity | Statistics / Epistemology |
| source problem/value/authority | source-domain owner |

The artifact **references** those claims. It does not copy them into timeless Computational Possibility truth.

Schema validity proves only structural completeness and variant consistency. It does not prove theorem truth, semantic preservation, owner-premise truth, measurement validity, currentness, or operational authority.

## Envelope

A record has non-semantic envelope fields:

- `schemaVersion = 1`
- `kind = "ordivon.computing.computational-applicability-transport"`
- `recordId`

The semantic payload has five top-level blocks:

1. `claimScope`
2. `targetScope`
3. `transportBurden`
4. `premiseEvidence`
5. `verdict`

`quantitative` is optional and lives inside `transportBurden`.

## ClaimScope

`claimScope` identifies the formal Computational Possibility claim being transported. It preserves enough scope to prevent instance-to-family, bounded-to-unbounded, finite-to-asymptotic, and aggregation drift.

It names the formal claim, theorem kind, typed computational-regime reference, constituted obligation reference, optional performance/constraint functional, quantification scope/domain, and aggregation semantics.

Supported theorem kinds in v1 are deliberately narrow:

- `constructive-achievability`
- `upper-bound`
- `impossibility`
- `lower-bound`

The schema does not encode theorem truth.

## TargetScope

`targetScope` identifies the concrete owner-scoped target against which applicability is being tested. It carries owner, target identity, target revision/version, and optional configuration reference. It does **not** embed a Runtime/Network/Security/Finance snapshot.

## TransportBurden

Transport is directional.

For `constructive-achievability` and `upper-bound`:

```text
formal witness -> actual witness
```

The burden is an implementation/embedding claim plus referenced semantic preservation. For an upper bound, `quantitative` is mandatory and uses `upper-domination`.

For `impossibility` and `lower-bound`:

```text
relevant actual candidate witness -> formal witness
```

The burden is coverage/abstraction of the target witness space plus referenced semantic preservation/contract translation. For a lower bound, `quantitative` is mandatory and uses `lower-reflection`.

A formal-to-actual implementation alone never establishes a lower bound over all actual implementations.

### Quantitative substructure

`quantitative` is present only for `upper-bound` or `lower-bound`. It names the formal resource functional, aggregation semantics, upper-domination or lower-reflection relation, and measurement/interpretation dependencies. No universal scalar `cost` is admitted.

## PremiseEvidence

`premiseEvidence` is a non-empty list of references to owner-authoritative claims/evidence. Each item names owner, claim identity, evidence identity, scope/currentness identity, and local status:

- `discharged`
- `unresolved`
- `stale`
- `falsified`

These statuses are local to this applicability record. They do not overwrite the source owner's claim.

## Verdict

`verdict.status` is one of:

- `APPLIES`
- `DOES_NOT_APPLY`
- `UNRESOLVED`
- `EXPIRED`

Every verdict states the **exact transported consequence**. `APPLIES` means only that this bounded computational consequence transports under the referenced premises. It does not imply production readiness, security, economic value, physical optimality, permission, or source-domain authority.

`UNRESOLVED` is a successful fail-closed result when a required premise has not been discharged. `EXPIRED` is used when a formerly usable premise is stale for the current target/version scope.

## Anti-laws

```text
SchemaValid != TheoremTrue
SchemaValid != PremisesTrue
APPLIES != ProductionReady
APPLIES != Authorized
HistoricalCapability != CurrentCapability
OneSuccessfulRun != UniformFamilyAchievability
FiniteBenchmark != AsymptoticBound
SameTraceLanguage != StrategyPreservingTransport
FormalToActualImplementability != ActualWitnessCoverage
ExpectedBound != TailBound
AmortizedBound != PerOperationBound
```

## Conformance fixtures

`fixtures/valid/` contains records that must validate structurally.

`fixtures/invalid/` contains records that must fail structural validation. The negative fixtures cover deletion of each semantic top-level block plus wrong-direction and missing-quantitative cases.

No bespoke validator is part of v1. A standard JSON Schema Draft 2020-12 implementation is sufficient for structural conformance. Semantic and source-owner truth remain outside local schema validation.
