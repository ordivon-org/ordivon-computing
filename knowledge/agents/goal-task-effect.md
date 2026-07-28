# Goal, Task, Attempt, Context, and Effect

Agent systems often compress these objects into one prompt. They carry different identities, lifetimes, and authority.

## Goal

A Goal expresses a desired world condition and why it matters.

```text
Goal
= subject
+ desired condition
+ constraints and non-goals
+ completion evidence
+ consequence owner
```

A Goal can persist across models, sessions, tasks, and days. It does not need to contain the full execution plan.

## Task

A Task is one durable semantic unit that advances a Goal. Its dependencies and ready frontier can change as evidence reveals the problem.

```text
Goal
├── inspect the current system
├── reproduce the failure
├── construct candidates
└── validate the accepted result
```

A Task is not identical to a process, Kubernetes Job, Temporal Workflow, model session, or Tool call. Those can implement parts of it.

## Attempt

An Attempt is one exploration or execution path through a Task. It preserves a hypothesis, context binding, candidate actions, Effects, observations, Artifacts, cost, and end state.

The Task survives a failed Attempt. Failure can add evidence rather than erase the path.

## Context

Context is the bounded selected view supplied to one model invocation.

```text
durable Task, world, policy, Tool, and evidence state
→ selection and compression
→ Context
```

It should retain source and revision bindings sufficient to detect staleness. Context is not the authoritative store merely because the model can see it.

## Effect

An Effect is a stable semantic proposal to observe or change an external object. It minimally identifies:

- target and expected version;
- operation and input digest;
- preconditions;
- required authority or capability reference;
- declared idempotency behavior;
- completion semantics;
- verification and recovery path.

A stable Effect identifier supports correlation and reconciliation. It does not make an operation safe to repeat.

## Dispatch

A Dispatch is one concrete attempt to execute an Effect through a specific Tool or backend contract. A backend Job is an execution object owned by that backend.

```text
Effect
→ immutable Binding to Tool contract and request
→ Dispatch
→ Job or synchronous result
```

Response loss leaves the Dispatch outcome `UNKNOWN` until the world is re-observed.

## Progressive lowering

```text
human purpose
→ Goal
→ dynamic Task frontier
→ Attempt and Context
→ candidate Claim or Effect
→ authority admission
→ Tool-bound Dispatch
→ Observation and Artifact
→ Verification and Task update
```

Natural language preserves openness. Task state preserves continuity. Context scopes one cognitive episode. Effect and Dispatch identity bind cognition to external reality.

## Design rule

Do not promote a field to a shared primitive merely because one product needs it. The field must protect a specific failure across materially different workloads and remain stable across model and provider change.

See [`task-context-authority-effect-evidence.md`](task-context-authority-effect-evidence.md) and [`../../core/primitives.md`](../../core/primitives.md).
