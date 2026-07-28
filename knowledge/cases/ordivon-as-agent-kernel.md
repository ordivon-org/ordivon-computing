# Case: Ordivon Runtime as an Effect Execution Kernel

Ordivon Runtime connects model-hosted or Host-managed work to a persistent Linux execution environment. Its importance is not command execution alone, but the durable commitment objects around physical execution.

## Current correspondence

| Commitment concept | Runtime object or Tool |
|---|---|
| version-bound operational address space | `workspace.open` and Workspace identity |
| bounded read and mutation | `workspace.read`, `workspace.mutate`, `workspace.patch` |
| candidate comparison | `workspace.diff` |
| physical execution | `workspace.exec`, `workspace.execPlan` |
| execution identity | Job ID and Attempt ID |
| progress and result observation | `task.observe`, `task.list` |
| cancellation | `task.cancel` |
| durable output | retained Artifact and `artifact.read` |
| lifecycle closure | `workspace.close` |

## More than a shell bridge

A shell accepts commands and returns process output. Runtime adds:

- service-owned semantic identities;
- exact source binding;
- atomic validated mutations;
- duplicate request admission control;
- asynchronous Jobs and Attempts;
- retained evidence and Artifacts;
- process-tree ownership;
- cancellation and closure semantics;
- startup reconciliation and orphan recovery.

These properties allow the physical execution history to survive a model session or network response.

## What Runtime does not own

Runtime is deliberately trusted-local. A Workspace or Git worktree separates candidate source state; it is not an untrusted-code security sandbox.

Runtime also does not own:

- human Goal meaning;
- task decomposition;
- long-term memory;
- model choice or context compilation;
- semantic approval of every Effect;
- domain Fact admission;
- operator interface.

Those responsibilities remain above or beside it.

## Workspace as versioned candidate state

A Workspace begins from an exact source revision and receives an independent candidate identity. Several Workspaces can explore alternatives without mutating one global checkout.

The analogy to copy-on-write memory is useful for reasoning about identity and branching, but it is not architectural equivalence: Git and the filesystem remain the actual mechanisms.

## Job, Attempt, and Effect

A Runtime Job is a concrete execution-control object. An Attempt records one physical execution path. A semantic Effect can bind to a Job or synchronous receipt through a concrete Dispatch.

```text
Effect intent
≠ Dispatch attempt
≠ Runtime Job
≠ process
```

The distinction matters when a response is lost. The system must inspect durable execution evidence rather than ask a new model episode to guess whether the operation happened.

## Current research leverage

Real dogfood has exposed:

- semantic progress for long-running work;
- active, stalled, terminal, orphaned, and unknown execution;
- at-most-once physical dispatch admission;
- Tool-contract revision and rebinding;
- minimum continuation state above Runtime;
- multi-Workspace candidate integration;
- boundaries between trusted execution and containment.

These observations feed Host, Protocol, and Computing research. They do not make Runtime a replacement operating system or complete Agent Host.
