# SCD Gap Investigations G2/G4 — Negative Closeout v0.1

Status: **negative research result / integration-profile closeout**, not Foundation truth.

This artifact records two targeted post-dogfood gap investigations that were deliberately attacked against mature external theories.

## G2 — Owner-Typed Dependency Currentness

Initial question:

> Does SCD require a new formal theory for semantic claims whose standing depends on externally owned, versioned/current authority?

### Result

**Independent formal gap rejected.**

Applied cases A1/A2/A6 can be decomposed using established supplier roles:

1. **Authority / trust / authorization** resolves whose credential, policy, version or delegated authority is currently usable.
2. **Provenance / versioning** preserves derivation, revision, specialization, invalidation and historical lineage.
3. **Truth maintenance / assumption maintenance** recomputes which claims stand under the current support environment while retaining alternative/historical contexts when desired.
4. **Incremental dependency machinery** propagates changed support only to affected computations/claims.
5. **Domain/SCD semantic evaluation** supplies the actual typed semantic relation such as `HISTORICAL_NOT_CURRENT`, `MERGED_INTO`, `superseded`, or `CurrentlyExecutable`.

No new Currentness primitive or logic is justified.

### AFCM integration profile

Provisional descriptive name: **Authority-Fenced Claim Maintenance (AFCM)**.

```text
resolve owner-native authority/version/currentness
        ↓
retain provenance / repair / revision lineage
        ↓
expose current owner statement as typed support reference
        ↓
maintain/recompute dependent semantic claim standing
        ↓
interpret exact semantic relation in the owning/domain framework
```

Non-inferences:

- authority resolution does not manufacture arbitrary semantic truth;
- provenance does not select current semantic standing;
- truth maintenance does not mint external authority;
- incremental recomputation does not define semantic meaning;
- a downstream consumer cannot become the owner by caching a statement.

G2 therefore survives only as an **Applied/Integration profile under G1**, not as a distinct formal research continent.

## G4 — Correspondence Composition

Initial question:

> If `μ1` and `μ2` are individually valid semantic correspondences, does SCD need new machinery for `μ2 ∘ μ1`?

### Result

**Independent universal composition gap rejected.**

Mature suppliers already provide composition where their typed correspondence notion is closed under composition: compiler simulations, refinement relations, institution morphisms/comorphisms, Galois-style abstraction machinery and ordinary typed/partial mappings.

The important negative rule is:

```text
Valid(μ1) ∧ Valid(μ2)
    !=>
CompositePreservesStanding(μ2 ∘ μ1)
```

A composite is admissible only when the intermediate semantic surfaces align or are bridged explicitly, all local proof assumptions hold, authority/dependency/currentness support remains valid, and any partial resolver is defined for the exact fenced input.

### TCC integration profile

Provisional descriptive name: **Typed Correspondence Chain (TCC)**.

For:

```text
S0 -μ1-> S1
S1' -μ2-> S2
```

composition requires at least:

1. framework-supplied composition closure **or** explicit bridge `β : S1 ↔ S1'`;
2. compatible observation/property/satisfaction interfaces;
3. preserved local assumptions and scope;
4. current dependency/authority support;
5. defined partial resolution for exact references/fences;
6. a framework/domain proof that the final claim transport is valid.

SCD does **not** gain a universal `compose(μ1, μ2)` operator.

## Applied reconstruction

### A3 Host handoff

```text
bounded handoff
  -> exact revision-fenced reference
  -> authoritative Host resolution
  -> WorkingCheckpoint
  -> safe continuation claim
```

This chain is valid only while the resolver is defined for the exact revision/currentness contract. A task-id-only or stale/latest lookup changes the intermediate and breaks the preservation claim.

### A5 Harness projection

```text
exact selected pins / WorkingSet
  -> WorkingView
  -> AgentTurnRequest / model-visible view
  -> independent Continuity reconstruction
```

`sourceWorkingSetDigest`, `sourceModelViewDigest`, exact message ranges, privacy/caller/tool provenance and current action authority are intermediate witnesses. A plausible final prompt does not repair a broken chain.

## K0.2 consequence

K0.2 remains unchanged:

```text
Situation S = (ρ ⊢ D @ Σ)
Claim     φ
Change    χ = (v, μ)
Support   Δ
Standing  Stand(φ | S, Δ)
```

`μ` remains a **framework-supplied correspondence interface slot**. Its composition law, if any, belongs to the supplying framework or an explicit bridge theorem.

No K0.3 is justified by G2/G4.

## Research disposition

- G2: rejected as independent formal gap; retained as AFCM integration profile.
- G4: rejected as independent universal formal gap; retained as TCC integration discipline.
- G1: must now be reassessed after subtracting G2/G4.
- G3 Description Identity remains unresolved and lower-pressure.

No result here changes SCDF standing, Foundation0, Boundary Architecture, closure or research order.
