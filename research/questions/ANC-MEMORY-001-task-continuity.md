# ANC-MEMORY-001 — Minimum Durable State for Task Continuity

> **Status:** completed at M4 and localized to Host/application continuity. The experiment sections below are historical construction records; no general memory runtime is active.

## Question

What is the minimum durable state that allows a different model instance, process, session, or machine to understand and continue a long-running task?

## Current hypothesis

A continuation state requires three connected layers:

```text
execution state
+ cognitive state
+ world bindings
```

A minimal Task Capsule may include:

- Goal identity and desired state;
- active Tasks and Attempts;
- current Workspace and exact base revision;
- verified Facts and unresolved outcomes;
- relevant Artifacts rather than full message history;
- available capabilities and Tool catalog identity;
- next ready work.

## First experiment

Run a real multi-stage Ordivon engineering task, stop the original model session after a checkpoint, and continue with a fresh model instance using only the candidate capsule and world observations.

Compare capsules of different sizes to find information that is necessary, redundant, stale, or harmful.

## Evidence

- continuation without rereading the full conversation;
- no repetition of already committed Effects;
- correct detection of changed world state;
- time and context required to regain an accurate task model;
- quality of the first useful next action.

## Related material

- [`../../knowledge/computing/state-computation-and-memory.md`](../../knowledge/computing/state-computation-and-memory.md)
- [`../../knowledge/agents/execution-kernel.md`](../../knowledge/agents/execution-kernel.md)
- [`../../studies/2026-computing-stack-walkthrough/13-agent-kernel.md`](../../studies/2026-computing-stack-walkthrough/13-agent-kernel.md)
- `ordivon-host` and `ordivon-runtime`
