# Agent Semantic Kernel Charter v0

## 1. Mission

The Agent Semantic Kernel is the smallest durable mechanism required when a probabilistic cognitive system can change an open external world.

It does not make an Agent intelligent and does not replace a classical operating system. It establishes a semantic admission boundary between cognition and execution:

```text
probabilistic cognition / dynamic planning
                 ↓ proposal
━━━━━━━━━━━━━━━━ semantic admission boundary ━━━━━━━━━━━━━━━━
Agent Semantic Kernel
                 ↓ admitted Dispatch
executor / Ordivon / classical OS / network / external system
```

The Kernel exists to preserve stable identity, legal state transitions, explicit uncertainty, evidence provenance, and recoverable history when ordinary process, request, and conversation identities are insufficient.

## 2. Classical mechanisms inherited, not reimplemented

The Kernel delegates the following responsibilities to mature lower layers:

- CPU scheduling, threads, processes, virtual memory, and privilege levels;
- files, sockets, devices, drivers, and network transport;
- local process isolation and resource enforcement;
- SQLite locking, WAL, atomic disk commit, and crash-safe storage mechanics;
- concrete execution, workspace isolation, Job ownership, and Artifact retention in Ordivon.

The Kernel may depend on these mechanisms but must not disguise them as Agent-native inventions.

## 3. Problems promoted into the Kernel

A problem belongs in this Kernel only when it is:

1. unavoidable for autonomous external action;
2. common across Agent frameworks and models;
3. unsafe to leave to probabilistic cognition or application convention;
4. impossible to reconstruct reliably after the boundary has been crossed;
5. stable enough to become a long-lived invariant;
6. mechanically falsifiable through tests and fault injection.

## 4. Hard guarantees

### K1 — Stable semantic identity

An Effect and its causal history retain the same identity across retries, reconnects, Adapter replacement, process restart, and replay. Process IDs, request IDs, conversations, and model calls are not semantic identity.

### K2 — Effect and Dispatch separation

An Effect is intended world observation or change. A Dispatch is one concrete boundary attempt. One Dispatch identity belongs to exactly one Effect, and reusing it for a different intent is forbidden.

### K3 — Unknown is not failure

Loss of response, ownership, transport, or current observability must not be rewritten as proven failure. The Kernel preserves `UNKNOWN` and requires reconciliation.

### K4 — Reconciliation precedes redispatch

An uncertain Dispatch is recovered by its stable identity. It cannot silently become a new delivery attempt. Blind redispatch from `UNKNOWN` is forbidden.

### K5 — Cancellation intent is not cancellation outcome

`CANCEL_REQUESTED` records intent. Only observed terminal evidence admits `CANCELLED`; natural success or failure may legitimately win the race.

### K6 — Observation is not accepted fact

A Tool response, Observation, Artifact, process exit, or model statement cannot directly become a Fact. Admission requires an explicit Claim and accepted Verification bound to permitted evidence.

### K7 — Semantic mutation is atomic

Every command and declared semantic transaction changes all affected projections or none. A reported failure must not leave partial Effect, Dispatch, Event, evidence, Claim, Verification, or Fact state.

### K8 — Durable history is replayable and fails closed

Committed semantic state survives process loss and is reconstructible from one ordered durable history. Unsupported schema, corruption, truncation, stale writers, or replay disagreement must be reported rather than normalized.

### K9 — Authority is separated by role

Proposing an Effect, admitting a Dispatch, attesting an Observation, evaluating a Verification, and accepting a Fact are distinct authorities. A normal caller must not obtain all powers merely by holding one Kernel object.

**Current status: OPEN P0.** The v0 Python API does not yet enforce this boundary and therefore is not a trusted reference monitor.

### K10 — Mechanical success is not goal completion

Exit code zero, HTTP success, Tool return, file existence, or an Agent statement may support evidence but cannot by itself establish goal satisfaction or an accepted Fact.

## 5. Guarantees deliberately not made

The Kernel does not claim:

- that every accepted proposition is objective truth;
- that arbitrary external effects occur exactly once;
- that all external systems support idempotency, status lookup, cancellation, or compensation;
- that all observations, Adapters, backends, or human approvals are honest;
- that an Agent will choose a correct goal, plan, or verification method;
- that every `UNKNOWN` state eventually resolves;
- distributed consensus, replication, remote failover, or Byzantine resistance;
- model scheduling, prompt construction, memory selection, or context compression;
- process, filesystem, network, sandbox, or device implementation.

A current `Fact` means a proposition accepted under recorded Kernel rules and evidence. It is not metaphysical or universally certified truth.

## 6. Cost budget

These guarantees intentionally cost:

- stable semantic IDs and Adapter correlation keys;
- one durable admission before an external boundary;
- one or more durable result/evidence commits afterward;
- storage for causal history and evidence references;
- reconciliation queries after uncertain delivery;
- explicit verification before accepted facts;
- schema, reducer, and Tool-contract version management;
- temporary unavailability when correctness requires waiting rather than guessing.

The strong path is required for external side effects, irreversible actions, cross-restart work, high-cost operations, or results that later decisions treat as facts. Pure reasoning, drafts, and harmless repeatable reads should remain outside or use a lighter path.

## 7. Admission rule for future Kernel features

No new primitive enters the Kernel because another Agent platform has it. A primitive is admitted only with:

1. a concrete failure that existing lower layers cannot express or prevent;
2. a proposed invariant;
3. an identified enforcement boundary;
4. a cost analysis;
5. a failing adversarial or crash test before implementation;
6. a passing conformance test after implementation.

Schedulers, memory systems, workflows, provider integrations, UI, channels, and product services remain above the Kernel unless this rule is satisfied.

## 8. Current maturity boundary

K1–K8 and K10 have executable local evidence in the reference implementation. K9 remains an explicit P0 gap. The current project is therefore a durable semantic consistency kernel prototype, not yet a trusted authority kernel.
