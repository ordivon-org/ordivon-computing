# ANC-IR-001 — Minimum Useful Agent Effect IR

## Question

What is the smallest representation that can lower an open Goal into external Effects across models, runtimes, and Tool providers while preserving enough semantics for execution and continuation?

## Current hypothesis

A useful minimal Effect contains:

```text
identity
+ parent Task and Attempt
+ target identity
+ preconditions / guards
+ required capability
+ payload
+ idempotent identity
+ result semantics
+ verification path
```

The wider lowering chain is:

```text
Intent
→ Goal
→ Task Graph
→ Effect IR
→ Tool binding
→ Observation
→ Fact / Artifact
```

## First artifact

Construct a small machine-readable schema and interpreter capable of representing and executing several Ordivon operations:

- read a Workspace file;
- perform an atomic mutation against an expected version;
- launch and observe a long-running command;
- verify an output and record a Fact.

## Evidence

- successful representation of several heterogeneous Effects;
- clear handling of synchronous, asynchronous, failed, and unknown outcomes;
- continuation after a Tool contract or world-state change;
- comparison with direct ad hoc Tool calls.

## Related material

- [`../../core/primitives.md`](../../core/primitives.md)
- [`../../knowledge/agents/goal-task-effect.md`](../../knowledge/agents/goal-task-effect.md)
- [`../../studies/2026-computing-stack-walkthrough/12-agent-language.md`](../../studies/2026-computing-stack-walkthrough/12-agent-language.md)
- Ordivon
