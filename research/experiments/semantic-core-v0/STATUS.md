# Status

## Selected runtime

```text
Python 3.12.13
```

## Completed

### M0 — Semantic constitution v0

- typed identity for WorldObject, Effect, Dispatch, Event, Observation, Artifact, Claim, Verification, and Fact;
- Effect/Dispatch separation and explicit admission state;
- `UNKNOWN → RECONCILING` without blind redispatch;
- causal event ordering, optimistic revisions, evidence scope, and Fact admission;
- independent cross-Effect verification.

### M1 — Ordivon adapter and failure semantics v0

- versioned read and atomic mutation;
- asynchronous execution and observation;
- Artifact projection and digest Fact admission;
- response-loss recovery without duplicate execution;
- cancellation races;
- adapter-instance identity recovery.

### M1.5 — Kernel atomicity closure

- every mutating ReferenceKernel command is all-or-nothing;
- multi-command semantic transactions are supported;
- Adapter result projection and Claim/Verification/Fact admission use transactions;
- malformed result payloads roll back partial projection and become `UNKNOWN`;
- Dispatch/Event correspondence invariants were strengthened.

### M2 — Durable semantic journal v0

- append-only SQLite command journal using WAL and `synchronous=FULL`;
- internal schema-v1 allowlisted codec;
- hash-chained entries and durable head marker;
- corruption, tail truncation, and missing-head detection;
- semantic replay of all projections;
- separate-process reconstruction;
- journal-head compare-and-swap for stale writer rejection;
- pending Ordivon Job correlation after Kernel process restart;
- live process-restart recovery with exactly one `workspace.exec` delivery.

### M2.25 — Kernel Charter and falsification surface

- normative Kernel mission and classical-OS foundation boundary;
- K1–K8 proven hard guarantees with explicit costs;
- classical, distributed, and Agent-native failure model;
- canonical fault-injection tests for every current guarantee;
- document/test drift guard.

## Verification

```text
62 tests passed
Python bytecode compilation passed
ruff passed
real Ordivon process-restart recovery passed
```

## Current claim boundary

The current implementation is a durable local Agent Semantic consistency Kernel reference implementation. It provides atomic semantic commands, append-only persistence, deterministic replay, local multi-process writer conflict detection, real Ordivon recovery across a Python process restart, and executable K1–K8 Charter conformance.

It does not prove distributed consensus, replicated journals, long-journal snapshot/compaction performance, public Effect IR compatibility, pending/running Tool-contract drift, complete Ordivon conformance, or production Goal-level correctness.

## Next executable work

M2.5 is next: establish distinct authority and attestation surfaces with role-scoped APIs, evidence issuers, trust domains, and adversarial isolation tests. M3 Effect IR follows that authority boundary. The internal journal codec is not the public IR.
