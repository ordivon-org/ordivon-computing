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
- internal schema-v2 allowlisted codec with signed Authority and Attestation types;
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

### M2.5 — Authority and attestation boundary

- signed Authority grants for EFFECT, DISPATCH, OBSERVATION, VERIFICATION, and FACT roles;
- one derived HMAC signer per Authority;
- content-, contract-, and time-bound Attestations on every mutation and evidence record;
- scoped production Views with no public full-authority bootstrap;
- Ordivon Adapters restricted to DISPATCH + OBSERVATION;
- separate Verification and Fact acceptance handles;
- invariant scanning and Journal replay re-authenticate stored history;
- Journal metadata binds semantic model, reducer, and authority-policy versions.

## Verification

```text
75 tests passed
Python bytecode compilation passed
ruff passed
real Ordivon process-restart recovery passed
```

## Current claim boundary

The current implementation is a durable local Agent Semantic Kernel reference implementation. It provides atomic semantic commands, role-scoped signed admission, attested evidence, append-only persistence, deterministic authenticated replay, local multi-process writer conflict detection, real Ordivon recovery across a Python process restart, and executable K1–K10 Charter conformance.

It does not prove distributed consensus, replicated journals, long-journal snapshot/compaction performance, public Effect IR compatibility, pending/running Tool-contract drift, complete Ordivon conformance, or production Goal-level correctness.

## Next executable work

M3 is next: define the external Effect IR on top of the now-stable semantic, durability, Authority, and Attestation boundaries. The internal Journal codec remains a replaceable storage format.
