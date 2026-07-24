# Goal, Task, Attempt, and Effect

Agent-native execution benefits from separating four concepts that are often compressed into one Prompt.

## Goal

A Goal expresses a desired world state and the context that gives it meaning.

```text
Goal = subject + desired state + context + completion evidence
```

A Goal may persist across many models, sessions, tasks, and days.

## Task

A Task is a schedulable semantic unit that advances a Goal. Tasks form a dependency graph and can be created dynamically as new observations reveal the structure of the problem.

```text
Goal
├── inspect current system
├── reproduce friction
├── construct a candidate
└── validate in a real workload
```

A Plan explains a strategy. A Task Graph gives that strategy stable identities, dependencies, and runtime state.

## Attempt

An Attempt is one concrete path through a Task. It carries a hypothesis, world binding, Effects, observations, artifacts, and an end state.

```text
Task: improve recovery
├── Attempt 1: memory-only progress
├── Attempt 2: synchronous event persistence
└── Attempt 3: staged checkpoints
```

The Task survives individual failed Attempts. Each Attempt adds information to the next.

## Effect

An Effect is an external observation or change prepared for execution. It minimally identifies:

- the target object;
- the expected world state;
- the required capability;
- the payload;
- a stable identity for retry and reconciliation;
- the expected result and verification path.

A Task can contain many Effects. “Verify the implementation” may lower into reading configuration, starting tests, observing a long-running process, reading a log artifact, and recording the exact result.

## Progressive lowering

```text
Intent
→ structured Goal
→ candidate Plan
→ dynamic Task Graph
→ Effect IR
→ concrete Tool Call
→ Observation
→ Fact and Artifact
```

Each layer preserves a different kind of meaning. Natural language preserves openness; Task structure preserves continuity; Effect IR binds cognition to a specific reality.

## Pure computation and effects

Pure computation transforms values without changing external state and is easy to cache or repeat. Effects observe or change files, processes, databases, services, people, or devices. Mixing the two hides recovery and retry semantics.

## Why this matters

A long task should not be represented only by the latest model message. Stable Goal, Task, Attempt, and Effect identities let the system know what persists, what may be revised, what has actually run, and what remains to be verified.

See [`../../core/primitives.md`](../../core/primitives.md) and the [Agent language study](../../studies/2026-computing-stack-walkthrough/12-agent-language.md).
