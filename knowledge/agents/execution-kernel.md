# Open-Work Control and Effect Execution

The phrase “Agent execution kernel” can hide two different responsibilities. They should be separated.

## 1. Open-work control

Open-work control preserves the meaning and frontier of a Goal whose decomposition can change through model cognition and new evidence.

```text
Goal
→ dynamic Task frontier
→ Task Attempt or Branch
→ bounded Context
→ candidate Claim or Effect
→ revised Task state
```

It owns semantic continuity across:

- model and provider replacement;
- context reset or compaction;
- failed Attempts;
- Host and Runtime restart;
- changing repository or Tool revisions;
- human redirection;
- new evidence that invalidates the plan.

This is not generic durable workflow. Kubernetes Jobs and Temporal Workflows already preserve declared work across process and machine failure. The Agent-specific problem is preserving and revising work whose path is not completely encoded in advance.

## 2. Effect execution

Effect execution preserves the commitment boundary between a selected proposal and classical reality.

```text
Effect
→ authority and contract Binding
→ Dispatch
→ backend Job or synchronous operation
→ Observation / Artifact
→ reconciliation and verification
```

It owns:

- stable Effect identity;
- concrete Dispatch identity;
- Tool-contract binding;
- declared retry and idempotency semantics;
- explicit unknown outcome;
- physical execution evidence;
- cancellation and recovery.

The operating system, database, Tool, or remote service still owns the physical mechanism.

## 3. Why one monolithic kernel is undesirable

Collapsing both responsibilities creates several errors:

- a Runtime Job is mistaken for a Task;
- process completion is mistaken for Goal completion;
- a Task planner is forced into the trusted execution boundary;
- a model-generated plan can rewrite physical history;
- generic workflow durability is incorrectly claimed as Agent-native;
- every domain is pressured into one universal object model.

A thin commitment kernel can remain stable while Hosts, planners, memory systems, and products evolve more rapidly.

## 4. Recovery differs at each boundary

### Physical recovery

Re-observe process, Job, file, service, or remote object state. Reconcile a lost response without blind redispatch.

### Semantic recovery

Restore the current Goal, Task frontier, Attempts, world bindings, Claims, accepted Facts, and relevant Artifacts. Recompile context for a new cognitive episode.

### Human recovery

Present an unresolved decision, consequence, or ambiguity with evidence and alternatives.

No single conversation transcript is sufficient for all three.

## 5. Ordivon mapping

- `ordivon-runtime` implements a trusted-local Effect execution and recovery boundary;
- `ordivon-host` implements bounded open-work, context, admission, and verification slices;
- `ordivon-protocol` carries selected Effect, ToolContract, and Binding contracts;
- the Semantic Core experiment tests stable identity, uncertainty, authority, evidence, and replay across two backends.

The general Task runtime, cognitive scheduler, memory governance, and operator decision plane remain incomplete research areas.

See [`probabilistic-work-control-loop.md`](probabilistic-work-control-loop.md) and [`capability-externalization-and-responsibility-placement.md`](capability-externalization-and-responsibility-placement.md).
