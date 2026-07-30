# Host, Harness, Runtime, and Agent-System Concepts

Agent-system terms are easiest to understand when separated by **kind**, **authority**, and **lifetime** rather than arranged in one product stack.

## Three authoritative boundaries

```text
Host owns durable work.
Harness owns the cognitive episode.
Runtime owns physical execution facts.
```

### Ordivon Host

Host owns Goals, Tasks, Task Graphs, Ready Frontier, Assignments, Task Attempts, waits, budgets, leases, participant decisions, completion, and cross-session recovery.

### Harness

Harness compiles Context, invokes the Model, loads Skills, exposes Tools, runs the Agent loop, manages local plans and subagents, compacts working state, and produces progress or completion proposals.

### Ordivon Runtime

Runtime owns Workspaces, Jobs, processes, output, cancellation, Artifacts, physical receipts, execution observation, and response-loss recovery.

These may be deployed together, but an object has one authoritative owner.

## Work hierarchy

```text
Goal
→ Task
→ Assignment
→ Task Attempt
→ Harness Run
→ Turn
→ Step
→ Tool Call or ActionProposal
→ Effect / Dispatch where external commitment matters
→ Runtime Job or provider receipt
→ Runtime Attempt / process where applicable
→ Observation / Artifact / Evidence
```

A Task is not a Session or Job. A Plan is not yet a Task. A process exit is not Goal completion.

## Proposal and commitment

Probabilistic components propose; authoritative components commit.

```text
Harness proposes Task decomposition → Host commits Task Graph
Harness proposes completion → Host verifies and commits TaskCompleted
Harness requests execution → Runtime admits and records Job
Model proposes Claim → Verification may admit Fact
```

This prevents temporary cognition, stale workers, or optimistic Tool output from becoming system truth.

## Skill, Tool, Workflow, and Plugin

```text
Tool     executable capability
Skill    reusable procedure and knowledge
Workflow durable or reusable control structure
Plugin   distribution package for Skills, Tools, Hooks, Connectors, or UI
```

Harness understands and selects Skills. Tools execute through providers or Runtime. Host owns persistent Workflow or Task control only when the process must survive Session replacement or wait for external conditions.

## Hook, Event, Signal, and Policy

```text
Hook      deterministic lifecycle extension point
Event     immutable statement that something happened
Signal    asynchronous information to a running object
Command   request to perform an operation
Query     read-only state request
Update    accepted or rejected durable state change
Policy    allow/deny/limit/approval decision
Interrupt durable suspension awaiting input or condition
```

Before an operation, a Hook or Policy may block it. After an operation, an Event records the fact; the system reconciles or compensates rather than pretending it did not occur.

Hooks remain layer-local:

- Harness Hooks surround Context, Model, Tool, and compaction lifecycle;
- Host Hooks surround Goal, Task, Assignment, and completion commits;
- Runtime Hooks surround Workspace, execution, process, and Artifact lifecycle.

A global Hook engine would hide control flow and merge authorities.

## Graphs and Loops

A Graph is state structure. A Loop is the controller that advances it.

```text
Task Graph       Host
Planning Graph   Harness
Execution Graph  Runtime
Provenance Graph cross-layer
```

```text
Agent loop       Harness
Scheduling loop  Host
Execution loop   Runtime
Evaluation loop  Computing/Eval
```

One generic graph representation may store several graphs, but it must not erase their different semantics.

## Durability mechanisms

Checkpoints, journals, queues, leases, heartbeats, fencing tokens, idempotency keys, Sagas, backpressure, circuit breakers, and materialized views are mature classical mechanisms.

The Agent-specific question is where to apply them:

- Host checkpoint for durable open work;
- Harness checkpoint for provider-specific cognitive continuity;
- Runtime receipt and Job state for physical execution;
- fencing token for stale Assignment writers;
- idempotency and correlation for duplicate external requests;
- provenance links across Task, Run, Dispatch, Job, and Artifact.

## Agent worker

An Agent is not merely a Model.

```text
Agent worker
= Model
+ Harness instance
+ Context
+ assigned Task
+ Skills
+ Tool capability set
+ Runtime or World binding
```

Host creates and supervises durable workers. Harness may create local subagents whose lifetime remains inside one Run.

## Thin Harness hypothesis

Ordivon can research a thin Harness boundary because Host and Runtime already own most durable and physical responsibilities.

Candidate interface:

```text
start_assignment
resume_run
send_signal
interrupt
stream_events
checkpoint
finish
```

Candidate adapters include Codex, Claude Agent SDK, Hermes, and a minimal native loop. The boundary should preserve provider-specific capability through manifests rather than force a lowest common denominator.

`ordivon-harness` should not become a repository until at least two live adapters and two workloads demonstrate cross-Harness continuation, stable lifecycle contracts, independent release value, and measurable reduction in duplication.

## Decision test

When encountering a new Agent concept, ask:

```text
What kind of object or mechanism is it?
Who owns authoritative state?
Must it survive Session, process, Model, or machine replacement?
Does it create a real external effect?
How does it behave under retry, duplication, drift, and stale ownership?
Can a mature lower mechanism or local adapter solve it more cheaply?
```

The complete derivation, standards comparison, and research program are in [`../../studies/2026-agent-system-concept-system/`](../../studies/2026-agent-system-concept-system/).
