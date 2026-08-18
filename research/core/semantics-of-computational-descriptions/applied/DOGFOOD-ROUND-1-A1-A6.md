# Applied SCD Dogfood Round 1 — A1–A6

Status: **first-pass consumer falsification corpus**.

Source grammar: CF-v0.1. Source kernel: provisional K0.2.

Canonical Foundation non-regression during this round:

- `SCDF1/3/6/7/8/9/10 = FROZEN`.
- `SCDF2/4/5 = OPEN`.
- `SCDF2 ↔ SCDF5 ↔ SCDF10 Boundary Architecture v1 = FROZEN`.
- `Foundation0 = NONE`.
- `FamilyMapLocalClosure = ADMITTED`.
- `WholeSExhaustiveComplete = UNKNOWN`.
- `ResearchOrderSCDF = UNKNOWN`.

## A1 — Research System: Network stale-ready

Real source facts:

- `task:network-post-foundations-open-exploration-20260818` remains Host `READY` at revision 7.
- Its historical semantic frontier called for controlled NDF0 reopen / NDF1 repair after the quantum counterexample.
- Later Network owner consolidation repairs/refreezes NDF0 as `InterLocusCapability` and NDF1 as `Inter-Locus Capability Composition / Realization Algebra`, freezes NDF0–NDF5 and keeps NDF6 NOT_ADMITTED.
- Research-System legacy dogfood independently classifies the old route as `HISTORICAL_NOT_CURRENT / SOURCE_ADVANCED_STALE` while preserving Host continuity and repair lineage.

K0.2 interpretation:

```text
S_old = (ρNetwork ⊢ D_old @ Σ_old)
φ_old = current-recovery(old-handoff)
v     = owner repair/refreeze/consolidation
μhist = old description -> preserved historical repair lineage
Δ     = Host continuity + owner AuthorityVersion/current-recovery support
```

Expected target standing:

- historical-continuity claim: **stands**;
- old semantic route as current recovery: **fails / not-current**;
- Host `READY`: remains a true Host-owned continuity fact.

Result: **PASS**.

Negative law exercised:

```text
HostReady != SemanticCurrent
```

## A2 — Host/Runtime history: EF27 completed but superseded

Real source facts:

- `task:runtime-deep-foundations-ef27-20260818` remains Host `COMPLETED` revision 3.
- Current Runtime consolidation states canonical Execution registry is EF0–EF26.
- EF27 is historical superseded evidence whose effective work was merged into EF26; it must not be recreated as current EF27.
- Research-System legacy dogfood independently records `HISTORICAL_PRESERVED + WITHDRAWN/SUPERSEDED`, lineage `MERGED_INTO EF26`.

K0.2 interpretation:

- completed Host Task stays in provenance / external support;
- `μhist` preserves the historical contribution into later Runtime lineage;
- no valid current correspondence transports `EF27 is a current numbered Foundation` into current Runtime authority.

Expected:

- historical EF27 validity/provenance: **stands**;
- `EF27 is current`: **fails**;
- Host `COMPLETED`: remains true operational history.

Result: **PASS**.

Negative law exercised:

```text
TaskCompleted != ResearchCurrent
```

## A3 — Host handoff: bounded content vs authoritative recovery

Real source structure from `task.resume`:

```text
ExternalContinuityResume
  ├─ Projection
  ├─ OperatorHandoffCapsule
  └─ WorkingCheckpoint
```

The HandoffCapsule carries exact Task identity/revision, digests, ready frontier and next-admissible structure, but not the complete semantic working claim.

Direct claim:

```text
HandoffCapsule ≡ FullWorkingCheckpoint
```

Expected: **fails**.

Reference-mediated claim:

> Given exact `taskId + taskRevision` and authoritative Host resolution, the full revision-bound checkpoint can be recovered before consequential continuation.

Expected: **stands under the resolution/currentness contract**.

Hostile perturbation:

- drop/ignore revision fence;
- resolve only a generic latest state;
- act from the bounded capsule as if it contained all constraints.

Expected: safe-preservation claim **unresolved/fails**.

Result: **PASS**.

Key result:

```text
semantic preservation may be recoverable/referential
without content duplication
```

## A4 — Lossy memory: checkpoint frontier as summary

Real source:

A Host WorkingCheckpoint contains a compact `frontier` plus separate:

- established;
- unresolved;
- rejected;
- constraints;
- nextActions.

Variation:

```text
full checkpoint -summary-> frontier-only memory
```

Claim 1: high-level RoadmapDirection.

Expected: **may be preserved**.

Claim 2: FullSafeContinuationContract, including negative knowledge and owner/non-destructive constraints.

Expected: **not preserved by frontier alone**.

Hostile delegation:

> another Agent receives only frontier text and treats it as equivalent to full current state.

Expected: semantic-fidelity claim **fails**, even if the Agent continues in a superficially correct direction.

Result: **PASS**.

Key result:

```text
summary fidelity is claim-selective
```

## A5 — Harness: current WorkingSet -> exact Agent-visible turn

Exact inspected Harness engineering revision:

`7277e1074be83fa38c28cd8170c28d6f4223146e`

Harness architecture separates:

- append-only canonical history;
- Agent-selected current durable WorkingSet;
- caller interaction ingress;
- attempt-local Tool evidence;
- exact per-turn action authority.

`WorkingSetViewProjector` deterministically compiles current committed exact pins into a WorkingView; `AgentTurnProjector` constructs the effective Agent-visible request. Accepted transitions bind both:

- `sourceWorkingSetDigest` — durable selected context;
- `sourceModelViewDigest` — exact effective view the Agent actually saw.

Continuity independently reconstructs/validates permitted view/provenance before Provider admission.

K0.2 interpretation:

```text
v  = current cognition / ingress / tool evidence -> AgentTurnRequest projection
μ  = exact pin-to-message-range / caller / tool / digest correspondences
Δ  = Run Contract + WorkingSet/model-view digests + Journal/CAS + privacy + Provider evidence
```

Positive claim:

> the Agent saw the exact current selected cognition and admitted suffix represented by the request.

Expected: **stands only when exact current digests/provenance and independent continuity verification agree**.

Hostile perturbations:

- stale predecessor-attempt Tool exchange;
- forged current pin/message range;
- unbound caller injection;
- replacement projection unsupported by current authority.

Expected: view-fidelity claim **fails**.

Result: **PASS**.

Key distinction:

```text
canonical history membership
!= materialized source
!= current cognition
!= current model-visible view
```

## A6 — Harness: installed mechanism != current turn capability

Harness explicitly distinguishes:

1. package/Runner installed mechanisms;
2. immutable Run-admitted Contract/Binding authority;
3. exact turn-admitted `AgentTurnRequest.tools/capabilities`.

A Provider adapter may render exact current authority but cannot mint additional actions locally.

K0.2 claim:

```text
φ = CurrentlyExecutable(action)
```

Support includes exact Run/turn contract, current addressability/gates and action surface.

Hostile carry-forward:

```text
Installed(action)
        or
PreviouslyAdmitted(action)
        => CurrentlyExecutable(action)
```

Expected: **false**.

Harness example: caller-ingress promotion can be withdrawn on a later turn even while the promotion mechanism remains installed; a stale historical Runtime Tool request can be rejected with `physicalDispatch=false`.

Result: **PASS**.

Key result:

```text
capability truth is staged and current-turn scoped
```

# Round-1 outcome

All six fixtures are expressible in K0.2 without K0.3.

No fixture forces:

- Artifact into the semantic kernel;
- Context as a universal primitive;
- first-class SemanticStanding;
- a lineage primitive;
- a new Foundation;
- a Foundation reopen.

The strongest recurring pressures are G1 multi-framework obligation coordination, G2 owner-typed dependency/currentness, and G4 correspondence composition/recovery. These remain research-gap candidates only.
