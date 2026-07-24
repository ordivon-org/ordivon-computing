# Agent Execution Kernel

An Agent execution kernel makes work persist beyond a single model response or conversation.

## Kernel role

Linux manages processes, files, memory, devices, and networking. An Agent kernel manages higher-level semantic objects:

```text
Goal
Task
Attempt
Effect
Workspace
Observation
Artifact
Checkpoint
Fact
```

It connects model cognition to durable execution without replacing the operating system beneath it.

## Execution loop

```text
load persistent task state
→ find ready Tasks
→ create or resume an Attempt
→ request the next cognitive step
→ prepare Effects
→ execute through tools
→ preserve Observations and Artifacts
→ update the Task Graph
→ checkpoint at useful boundaries
```

The model is a replaceable cognitive component inside this loop. The Task and its world state remain stable.

## Asynchronous work

Long operations return an execution identity rather than holding one model call open:

```text
submit
→ accepted with execution_id
→ observe progress
→ completed / failed / unknown
```

Progress should expose semantic phases and recent activity, not merely “running.” This allows both users and later models to distinguish active work from a stalled process.

## Recovery

Recovery starts from persistent state and re-observes reality:

1. load the latest checkpoint;
2. verify workspace and repository bindings;
3. find active processes and completed effects;
4. reconcile effects with unknown outcomes;
5. rebuild the set of ready Tasks;
6. continue from the current world.

Recovery is not a replay of the entire conversation. It is a reconstruction of the minimum sufficient current state.

## Unknown outcome

A connection can disappear after an effect was dispatched. The action may have succeeded, failed, or remained in progress. The correct state is `unknown`, followed by a new observation of the target system.

```text
lost response
→ inspect world state
→ identify actual outcome
→ continue
```

## Versioned workspaces

A Workspace acts as a versioned logical address space. Multiple Attempts can branch from the same base, construct candidates independently, and later compare or integrate them. This reduces coordination through global mutable state.

## Event history and current state

A kernel can preserve both:

- an event history for explanation, learning, and reconstruction;
- materialized current state for fast scheduling and continuation.

The event history records what happened. The current state records what is true now.

## Design consequence

The central kernel property is continuity:

```text
models may change
connections may change
attempts may fail
but Goal, state, artifacts, and verified facts continue
```

See the [Agent kernel study](../../studies/2026-computing-stack-walkthrough/13-agent-kernel.md) and the [Ordivon case](../cases/ordivon-as-agent-kernel.md).
