# Decisions

## D1 — One fixture, separate causal work packages

The same world is reused, but E1/E7, E3, E2, and E5 are first evaluated in
isolation. The combined gauntlet runs only after isolated faults pass.

## D2 — Strong baselines receive the same semantic fields

Goal revision, frontier, evidence, pending operation, source revisions, catalog
digest, uncertainty, and next work may be ordinary LangGraph or Temporal state.
The experiment tests ownership and failure semantics, not field-name exclusivity.

## D3 — Fault injection lives outside production Runtime

Response loss, process termination, stale summaries, catalog drift, and poisoned
sources are controlled by this experiment. Runtime production code is not given
a random-failure switch.

## D4 — Single-backend Effect evidence cannot promote a universal layer

Round 1 may retain or shrink the Runtime-backed Effect path. A universal or
Protocol claim requires the materially different Edge backend from Round 2.

## D5 — Human-attention evidence remains product-local by default

A single-operator study can justify Host UX changes but cannot establish a
universal organization or attention plane.

## D6 — Open-work continuity remains Host-local

LangGraph SQLite, Temporal Workflow state, and Ordivon typed state all recovered
the same pending operation. Round 1 therefore rejects a new standalone Ordivon
Task Runtime and keeps Goal/Task/frontier semantics as a Host application schema.

## D7 — Context provenance shrinks to enforceable metadata

Current-revision retrieval matched the source-bound variant. Keep revision,
trust, attribution, and invalidation metadata where Host can enforce it; reject a
generalized Context Kernel and Protocol promotion.

## D8 — Effect commitment shrinks pending a second backend

Keep stable identity, explicit UNKNOWN, backend correlation, reconciliation, and
no-blind-redispatch. Idempotency/audit and durable Activity matched the current
single-backend result with fewer state objects. Full Effect/Binding/Dispatch
universality remains unproven.

## D9 — DecisionRequest remains Host product code

Evidence-rich routing passed the deterministic oracle with seven interruptions
versus twelve for approval-everywhere, while static and model-selected policies
missed consequential cases. The lifecycle remains Host-local until real operator
evidence exists.

## D10 — Provider-neutral state is retained without interchangeability claims

Six live Codex/Hermes trials completed in both replacement orders without the
original transcript, retained Provider session, blind redispatch, or duplicate
world Effect. This retains the adapter/state boundary but does not claim equal
Provider performance.
