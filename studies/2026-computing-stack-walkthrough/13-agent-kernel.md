# 13 — Agent Execution Kernel

An Agent execution kernel gives a long-running Goal an identity and lifecycle independent of one model session.

## Kernel objects

```text
Goal
Task
Attempt
Effect
Workspace
Capability
Observation
Artifact
Checkpoint
Fact
```

Linux continues to manage processes, memory, files, and devices. The Agent kernel interprets those lower-level objects as task progress, attempts, effects, waits, artifacts, and verified facts.

## Task and Attempt

A Task is a semantic work unit. An Attempt is one concrete way of pursuing it. Failed Attempts remain valuable because they preserve hypotheses, actions, errors, and evidence for the next Attempt.

## State machines

Task state may move through:

```text
pending → ready → running → waiting → completed
                         ↘ failed / cancelled
```

Effect state may move through:

```text
proposed
→ prepared
→ dispatched
→ running
→ observed
→ verified
→ committed
```

A transport loss can create `unknown` rather than `failure`. The kernel then queries the target world and reconciles actual state.

## Async execution

Long work returns a stable execution handle:

```text
submit
→ accepted
→ observe semantic progress
→ complete
```

The model need not remain active while tests, builds, training, data analysis, or deployment continue.

## Checkpoints

A complete continuation point combines:

- execution state: Tasks, Attempts, Effects, process handles;
- cognitive state: current understanding and important findings;
- world bindings: repository revision, Workspace, Tool catalog, external resource identities.

Recovery loads the checkpoint, re-observes the world, reconciles unknown outcomes, and constructs the current ready queue.

## Idempotency and compensation

Stable Effect identities allow duplicate dispatches to return an existing result rather than repeat a world action. Some effects can be rolled back, some require a compensating effect, and some are best handled by accepting the current state and replanning forward.

## Concurrency

Versioned Workspaces let multiple Attempts branch from one base. A JOIN combines artifacts and facts into a new synthesis Task. This supports parallel exploration without forcing every worker to share one mutable state.

## Ordivon correspondence

Ordivon already exposes Workspaces, Jobs, Attempts, mutations, observations, artifacts, cancellation, and closure. Its real multi-hour tasks reveal where the semantic kernel still needs richer progress, continuity, and contract-rebinding objects.

## Anchor

The model can change; the connection can change; an Attempt can fail. The persistent Goal, world bindings, artifacts, and facts allow the work to continue.
