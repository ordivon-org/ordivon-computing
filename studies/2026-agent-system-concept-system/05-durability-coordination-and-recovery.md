# Durability, Coordination, and Recovery

These mechanisms are mostly inherited from durable workflows, databases, and distributed systems. Their value in Agent systems comes from applying them at correct semantic boundaries.

## 1. Checkpoint, Snapshot, Journal, and Replay

### Checkpoint

A Checkpoint is the minimum state required to continue a Run or Task after interruption.

Host continuation may require:

```text
Goal and Task identities and revisions
active Assignment and generation
current Task Attempt
ready and waiting work
relevant Facts, Claims, Artifacts, and unresolved outcomes
world, source, policy, Tool, and capability revisions
next admissible action or decision boundary
```

Harness continuation may additionally require provider-specific Session state, compaction summary, Tool-call state, or reasoning-retention reference.

### Snapshot

A Snapshot is a point-in-time state view. It supports inspection, comparison, forking, rollback analysis, and materialized views. It need not be sufficient for execution continuation.

### Journal

A Journal is an append-only sequence of state-changing records. It preserves causality and can rebuild projections.

### Replay

Agent systems require three distinct replay modes:

1. **Exact replay** — reuse recorded Model and Tool outputs to reconstruct state and UI.
2. **Semantic replay** — re-run the same Task under a new Model or Harness for regression comparison.
3. **Counterfactual replay** — fork at a checkpoint and deliberately alter Model, Skill, Tool, policy, or world condition.

Re-executing model or external calls is not exact replay.

## 2. Interrupt and Resume

An Interrupt durably records:

- why execution cannot continue;
- which object is waiting;
- what input, evidence, commitment, or condition is required;
- current revisions and lease state;
- which side effects have already occurred;
- which operations must not be repeated;
- the checkpoint and allowed resume actions.

Resume must revalidate current state. It must not blindly continue a stale local stack frame.

```text
load authoritative Task
→ reconcile prior external effects
→ verify current Assignment generation
→ recompile Context
→ continue or replan
```

Any side effect before an interrupt or checkpoint boundary must be idempotent, correlated, or explicitly reconciled.

## 3. Lease, Heartbeat, and Fencing

### Lease

A Lease grants a worker temporary right to advance an Assignment.

```text
assignment_id
worker_id
lease_until
generation
```

Lease expiry allows Host to recover work without declaring the old worker malicious or failed.

### Heartbeat

A useful heartbeat reports more than process liveness:

```text
current Run and Job
last model or Tool activity
last new Evidence or Artifact
semantic progress marker
checkpoint age
known blocker
budget consumption
```

A worker that emits heartbeats while repeating the same failed step is alive but not healthy.

### Fencing token

Every Assignment generation increases monotonically. Completion, state updates, or external commitment requests carry the generation. Host rejects stale generations.

```text
Agent A generation 17 lease expires
Agent B receives generation 18
Agent A reconnects and submits completion with 17
→ rejected as stale, evidence retained for review
```

Without fencing, lease-based recovery can create concurrent owners.

## 4. Idempotency and reconciliation

An idempotency key supports deduplication. It does not prove that the first request completed successfully.

For external effects:

```text
stable Effect identity
+ immutable request binding
+ Dispatch identity
+ provider correlation or receipt
+ observation path
```

Response loss produces `UNKNOWN`, not automatic failure or success. The system first observes the world or provider before redispatch.

Runtime should own physical correlation where it controls the backend. Host owns Task-level decision to retry, rebind, compensate, or wait.

## 5. Compensation and Saga

Many real effects cannot be rolled back. Compensation creates a new effect that counteracts the old one.

Examples:

```text
create preview deployment  ↔ delete preview deployment
publish broken release     ↔ publish rollback release
send incorrect message     ↔ send correction
create branch              ↔ delete or supersede branch
```

A Saga coordinates a long sequence of effects and compensations. Host or a mature workflow system owns the durable coordination. Runtime or provider implements each concrete operation.

Compensation is not equivalent to erasing history.

## 6. Queue, Mailbox, Channel, and Blackboard

### Queue

Competitive work distribution:

- Ready Tasks;
- pending Runtime Jobs;
- pending evaluations;
- dead-letter items.

### Mailbox

Directed messages to an Agent, Assignment, Task, or participant:

- user instruction;
- cancellation request;
- dependency completion;
- delegated result;
- approval decision.

### Channel

A typed stream with potentially many subscribers:

- progress;
- Artifact production;
- control events;
- trace or telemetry.

### Blackboard

A shared collaboration surface for facts, hypotheses, questions, and candidate results. A Blackboard is dangerous unless every entry carries:

```text
author and source
claim versus fact status
confidence or verification
validity scope and revision
created time
supersedes relation
evidence references
```

A shared Markdown file is not an authoritative multi-Agent Blackboard.

## 7. Reducers and concurrent state

Parallel workers should not replace complete Task state. They submit typed updates that Host reduces.

Examples:

```text
Artifacts       set union with identity checks
Evidence        append with provenance
Risk severity   domain-specific maximum or set
Task completion explicit proposal and validator
Claims          preserve conflicts; do not last-write-wins
Budget          monotonic consumption
```

Reducer semantics must be versioned and deterministic when they affect durable state.

## 8. Backpressure, circuit breaker, and bulkhead

### Backpressure

When Runtime, provider, or evaluator capacity is saturated, upstream Harnesses and Host scheduling must slow down. Queuing unlimited Tool calls creates stale work and Context noise.

### Circuit breaker

Repeated failures against one provider temporarily stop new calls while preserving a probe or recovery path.

### Bulkhead

Resources are isolated by consequence or workload:

```text
reversible research
production deployment
adversarial simulation
external provider calls
```

Failure or overload in one pool should not consume the entire system.

## 9. Timeout, deadline, timer, and watchdog

- **Timeout** bounds one operation.
- **Deadline** specifies when a Task or commitment is no longer useful.
- **Timer** generates an event at a time.
- **Watchdog** observes whether progress and invariants remain healthy.

An Agent watchdog should inspect:

- repeated identical Tool calls;
- token consumption without new evidence;
- old checkpoint or heartbeat;
- unobserved long-running Job;
- unresolved `UNKNOWN` outcome;
- cyclic replanning;
- stale Context or Tool revision;
- repeated CompletionProposal rejection.

## 10. Dead letter, quarantine, tombstone, and supersession

### Dead-letter queue

Stores repeatedly unprocessable work or messages for diagnosis and possible replay.

### Quarantine

Prevents suspicious or invalid Artifacts, Skills, memories, Tool results, or updates from entering trusted state.

### Tombstone

Records that an object existed and was deleted or retired.

### Supersession

Explicitly links old and new objects:

```text
Task T1 superseded_by T2
Skill v2 supersedes v1
ToolContract r4 supersedes r3
Fact F2 invalidates F1 for world revision W7
```

Deletion without a marker damages provenance and can cause resurrection by stale workers.

## 11. Capability and schema drift

Long-running Tasks bind to observable revisions of:

- repository and files;
- model and Harness;
- Skill and instructions;
- Tool Contract and provider;
- policy and authority;
- world target and path;
- Context selection method.

A change may be:

```text
compatible
requires Context refresh
requires rebind
requires new Effect or Task revision
invalidates evidence
unsupported
```

Compatibility must be classified rather than inferred from successful parsing.

## 12. Recovery matrix

| Failure | Authority that detects | First response |
|---|---|---|
| Harness process exits | Host | expire/revoke lease, load checkpoint, reassign |
| Model Session lost | Harness/Host | preserve declared state, start replacement Session, no hidden-state continuity claim |
| Runtime response lost | Runtime/Host | correlate original Job or external receipt before redispatch |
| Runtime Job orphaned | Runtime | observe, reconcile, cancel, or mark indeterminate |
| Task worker duplicated | Host | fencing generation rejects stale commits |
| Tool Contract changes | Harness/Host | invalidate Context and Effect Binding as required |
| World target changes | Host/World | re-observe and re-lower proposal |
| Completion accepted on stale evidence | Host/Verifier | invalidate completion and reopen/supersede Task |
| Hook fails | owning layer | apply declared fail-open/closed policy and record event |
| Event consumer fails | consumer | retry from durable offset; producer fact remains unchanged |

## 13. What not to build yet

Defer until a real consumer exists:

- global event sourcing for every byte and token;
- general distributed transaction protocol;
- universal Saga DSL;
- cross-repository consensus service;
- market-based task scheduling;
- automatic global Skill mutation;
- one Blackboard for all projects;
- a plugin marketplace;
- mandatory checkpoint after every Agent step.

Use mature local mechanisms and preserve clear adapters first.
