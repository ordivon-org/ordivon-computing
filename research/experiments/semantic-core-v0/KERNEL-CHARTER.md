# Agent Semantic Kernel Charter v0

## 1. Mission

The Agent Semantic Kernel is the smallest durable mechanism required when a probabilistic cognitive system can change an open external world.

It establishes a semantic admission boundary between cognition and execution:

```text
probabilistic cognition / dynamic planning
                 ↓ proposal
━━━━━━━━━━━━━━━━ semantic admission boundary ━━━━━━━━━━━━━━━━
Agent Semantic Kernel
                 ↓ admitted Dispatch
executor / Ordivon / classical OS / network / external system
```

Its value is to preserve stable identity, legal state transitions, explicit uncertainty, evidence provenance, and recoverable history across external action.

## 2. Classical foundation

The Kernel builds on mature lower-layer mechanisms:

- CPU scheduling, threads, processes, virtual memory, and privilege levels;
- files, sockets, devices, drivers, and network transport;
- local process isolation and resource enforcement;
- SQLite locking, WAL, atomic disk commit, and crash-safe storage mechanics;
- concrete execution, workspace isolation, Job ownership, and Artifact retention in Ordivon.

The Agent-native layer adds the semantic continuity that these mechanisms do not represent: intent identity, boundary-attempt identity, uncertainty, evidence, verification, and replayable causal history.

## 3. Kernel admission rule

A problem belongs in this Kernel when it is:

1. unavoidable for autonomous external action;
2. common across Agent frameworks and models;
3. unsafe to leave to probabilistic cognition or application convention;
4. impossible to reconstruct reliably after the boundary has been crossed;
5. stable enough to become a long-lived invariant;
6. mechanically falsifiable through tests and fault injection.

## 4. Hard guarantees

### K1 — Stable semantic identity

An Effect and its causal history retain the same identity across retries, reconnects, Adapter replacement, process restart, and replay. Semantic identity remains stable beyond any individual process, request, conversation, or model call.

### K2 — Effect and Dispatch separation

An Effect represents intended world observation or change. A Dispatch represents one concrete boundary attempt. Every Dispatch has exactly one owning Effect and an independent durable identity.

### K3 — Explicit uncertainty preservation

Loss of response, ownership, transport, or current observability is represented as `UNKNOWN`. The state machine preserves uncertainty as durable information and routes it into reconciliation.

### K4 — Identity-preserving reconciliation

An uncertain Dispatch is recovered through its original stable identity. Reconciliation correlates and observes the original boundary attempt before any additional delivery decision.

### K5 — Evidence-derived cancellation outcome

Cancellation intent and terminal outcome are recorded separately. `CANCEL_REQUESTED` preserves the request, while observed terminal evidence admits `CANCELLED`, `SUCCEEDED`, or `FAILED` according to actual completion order.

### K6 — Evidence-gated knowledge admission

Tool responses, Observations, Artifacts, and process results enter the Kernel as evidence. A Fact is admitted through an explicit Claim and an accepted Verification bound to the permitted evidence plan.

### K7 — Atomic semantic mutation

Every command and declared semantic transaction changes all affected projections together. Effect, Dispatch, Event, evidence, Claim, Verification, and Fact projections remain one coherent state.

### K8 — Durable deterministic replay

Committed semantic state survives process loss and is reconstructible from one ordered durable history. Schema validation, hash-chain validation, durable-head validation, writer conflict detection, semantic replay, and invariant validation protect the reconstructed state.

## 5. Value delivered

The Kernel provides a stable answer to the following questions across process and session boundaries:

```text
What was intended?
Which concrete attempt crossed the execution boundary?
What is known about external admission and completion?
Which uncertainty still requires reconciliation?
Which evidence was observed and retained?
Which Claim was evaluated?
Which Verification admitted the Fact?
How can the complete state be reconstructed after restart?
```

This creates a durable semantic substrate for future Goal, Task, authority, scheduling, and memory layers.

## 6. Cost budget

These guarantees intentionally cost:

- stable semantic IDs and Adapter correlation keys;
- one durable admission before an external boundary;
- one or more durable result/evidence commits afterward;
- storage for causal history and evidence references;
- reconciliation queries after uncertain delivery;
- explicit verification before Fact admission;
- schema, reducer, and Tool-contract version management;
- temporary waiting when the correct state requires additional evidence.

The strong path is used for external side effects, irreversible actions, cross-restart work, high-cost operations, and results consumed as durable facts. Pure reasoning, drafts, and harmless repeatable reads can use a lighter path.

## 7. Admission rule for future Kernel features

A new primitive enters the Kernel only with:

1. a concrete failure that existing lower layers cannot express or prevent;
2. a proposed invariant;
3. an identified enforcement boundary;
4. a cost analysis;
5. a failing adversarial or crash test before implementation;
6. a passing conformance test after implementation.

This keeps the Kernel centered on hard semantic guarantees while schedulers, memory systems, workflows, provider integrations, UI, channels, and product services remain composable upper layers.

## 8. Current conformance

K1–K8 have executable local evidence in the reference implementation. Together they establish a durable semantic consistency Kernel for external Agent action.
