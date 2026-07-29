# Round 1 Results

## Result boundary

Round 1 compared one frozen maintenance workload across strong persistence,
Context, Effect, and operator-attention baselines. It produced 16 deterministic
trials and six live Provider-replacement trials. The result is deliberately a
set of scoped architectural dispositions, not a declaration that Ordivon won
every comparison.

## Deterministic matrix

| Work package | Passed | Failed | Main observation |
|---|---:|---:|---|
| Continuity | 3 | 1 | LangGraph, Temporal, and typed Ordivon state all recovered; transcript/summary lost operation identity and duplicated the Effect. |
| Context | 2 | 2 | Current-revision retrieval matched source-bound Context; transcript and rolling summary used stale or unsupported state. |
| Effect | 3 | 1 | Idempotency/audit, durable Activity, and Ordivon reconciliation all prevented duplicates; plain Tool retry did not. |
| Attention | 2 | 2 | Approval-everywhere was safe but expensive; evidence-rich routing was safe with fewer interruptions; static and model-selected policies missed consequential cases. |

The matrix contains 16 trials: 10 passed and six failed with retained hard-failure
labels. Negative results were not rewritten as success.

## Live Provider replacement

Six live trials were completed:

- `Codex → Hermes`: three;
- `Hermes → Codex`: three.

Every trial selected the version-bound maintenance action before commitment and
selected observation of the original operation after the committed response was
lost. All six produced one ledger Effect, no duplicate world Effect, an accepted
repository state, no original transcript load, and no retained Provider session.

This establishes bounded semantic-state portability. It does not establish equal
model quality, latency, cost, or universal interchangeability.

## Architectural dispositions

### E1 — Open-work continuity: `localize`

Keep Goal/Task/frontier/UNKNOWN state and the handoff projection as Host
application semantics. Do not create a separate Ordivon Task Runtime: LangGraph
and Temporal represented and recovered the same application state correctly.

### E2 — Effect commitment: `shrink`

Retain the compact failure-critical invariants:

```text
stable request/effect identity
+ explicit UNKNOWN
+ backend correlation
+ reconciliation
+ no blind redispatch
```

Idempotency plus audit and a durable Activity matched the current single-backend
outcome with fewer state objects. The complete cross-backend
Effect/Binding/Dispatch claim remains deferred until the Edge Fetch/Browser
experiment.

### E3 — Context provenance: `shrink`

Retain revision, trust, attribution, and invalidation metadata in Host Context.
Do not promote a generalized Context Kernel. Ordinary retrieval with current
revision filters matched the source-bound variant on this workload at lower
measured context size.

### E5 — Operator attention: `localize`

Retain evidence-rich DecisionRequest lifecycle and UX in Host. Do not promote a
universal attention plane. The deterministic oracle showed fewer interruptions
than approval-everywhere without missed escalations, but no real multi-operator
study was performed.

### E7 — Provider replacement: `retain`

Retain provider-neutral semantic state and replaceable Host adapters. The live
trials prove that work can continue across Codex and Hermes replacement without
loading the original conversation or repeating an UNKNOWN Effect. Provider
performance remains profile-specific.

## Repository consequences

- Runtime production code remains unchanged.
- The default OpenProposalHost remains read-only.
- The mutation lowerer remains an explicit experimental adapter.
- No Round 1 object is promoted to Protocol.
- Round 2 owns the second, materially different structured Effect backend.
