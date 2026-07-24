# Case: Ordivon as an Agent Execution Microkernel

Ordivon connects a model-hosted conversation to a persistent Linux execution environment. Its importance is not the presence of command execution alone, but the semantic objects exposed around execution.

## Current correspondence

| Agent-kernel concept | Ordivon object or Tool |
|---|---|
| Workspace | `workspace.open` and a version-bound isolated worktree |
| Read | `workspace.read` |
| Candidate state | `workspace.mutate` |
| Difference from base | `workspace.diff` |
| Compute or command Effect | `workspace.exec` |
| Long-running execution identity | Job ID and Attempt ID |
| Observation | `task.observe` |
| Active execution discovery | `task.list` |
| Cancellation | `task.cancel` |
| Durable output | Job Artifact and `artifact.read` |
| Workspace lifecycle | `workspace.close` |

## Why this is more than a shell bridge

A shell primarily accepts a command string and returns process output. Ordivon adds:

- server-owned semantic identities;
- version-bound workspaces;
- atomic mutations;
- idempotent client request identities;
- asynchronous jobs;
- retained artifacts;
- cancellation and closure semantics;
- recovery through later observation.

These objects allow a model session to leave while the task state continues.

## Workspace as logical address space

A Workspace begins at an exact repository revision and contains an isolated candidate state. Multiple workspaces can branch from the same revision, explore different changes, and later be compared or integrated.

This resembles copy-on-write memory and register renaming: shared base state remains stable while candidate versions receive independent identities.

## Jobs and attempts

A long command returns a Job identity. Observers can reconnect, read progress, inspect retained stdout and stderr, and obtain result artifacts. A failed execution becomes an Attempt with durable evidence rather than an erased conversational moment.

## Current research leverage

Real dogfood has exposed questions about:

- progress semantics for multi-hour work;
- distinguishing active, stalled, failed, and unknown execution;
- retaining the minimum sufficient continuation state;
- Tool catalog revision and contract drift;
- joining multiple workspace branches;
- exposing task-level objects above raw command execution.

These are direct inputs to [`../../research/questions/`](../../research/questions/) and make Ordivon an experimental branch of the wider Agent-native stack.
