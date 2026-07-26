# Task Continuation v0 specification

## Ownership

| Object | Owner |
|---|---|
| Effect, Binding, Dispatch, Observation, Artifact, Fact | existing semantic experiments |
| frozen continuation workload and rubric | this experiment |
| `TaskCapsule` and content-addressed continuation store | this experiment |
| context compilation and fresh Host process | this experiment |
| model-specific CLI/prompt/response adaptation | model adapter |

The Host does not own Kernel transitions, Tool schemas, complete Binding semantics, or domain workflow scheduling.

## TaskCapsule v0

A Capsule contains:

```text
task identity, revision, supersedes digest
goal digest and bounded success condition
checkpoint world binding
completed Effect references
current Binding references
UNKNOWN/reconciling Dispatch references
Fact references
decision Artifact references
open questions and blockers
next-ready actions
```

All semantic records are content-addressed references. A Capsule does not contain the full transcript, raw Tool history, hidden model reasoning, complete Kernel state, or provider-specific prompt fields.

## Validation order

Before model invocation or execution, a fresh Host must:

1. decode the Capsule from its content address;
2. reread the current world object;
3. resolve every required semantic reference;
4. verify Effect and Binding Authority signatures and digests;
5. require an accepted Fact for the checkpoint world digest;
6. verify the retained decision Artifact content;
7. verify the selected Binding belongs to the pending Effect and frozen ToolContract;
8. compare current world digest with the checkpoint digest.

Missing, corrupt, forged, mismatched, or stale required references fail closed.

## Context Compiler

The compiled context contains current semantic state, not conversation replay. It exposes exactly one action class:

```text
current world + no unresolved Dispatch → selected guarded mutation
world drift                            → refresh-world
UNKNOWN/reconciling Dispatch           → observe-dispatch
```

Completed Effects are emitted as forbidden Effects. The model may choose only an exact item from `allowedActions`; the Host rejects invented or repeated actions.

## Completion

The reference Host executes a new bound guarded mutation, independently rereads the world, commits a digest Fact, and creates an immutable Capsule revision whose `supersedesDigest` points to the checkpoint Capsule. A complete Capsule has no ready actions or blockers and binds the terminal world digest.
