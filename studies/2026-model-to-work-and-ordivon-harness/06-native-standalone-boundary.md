# Native standalone Harness boundary

## Decision

The working Ordivon Harness implementation is now maintained in the standalone `ordivon-harness` repository. This supersedes only the physical-location decision in D12 and the old repository-promotion timing in the v0 gate. It does not supersede the responsibility boundaries established by D1–D11.

The dependency and ownership direction is:

```text
Ordivon Computer / ordivon-protocol
  normative Harness semantics and invariants

ordivon-harness
  Agent Loop, Provider adapters, Run-local state, Tool Step lifecycle,
  Runtime lowering, Run evidence, and the Host extension

ordivon-host
  durable Task truth, Journal, CAS, authority, completion admission

ordivon-runtime
  Workspace, Job, Attempt, process, Artifact, cancellation, and physical evidence
```

`ordivon-host` and `ordivon-runtime` must not import `ordivon-harness`. Harness may consume their stable ports without moving their state into Harness.

## Native protocol objects

Three Harness-local continuity objects are promoted into `ordivon-protocol` because removing them creates concrete failures across model adapters and Runtime-backed execution:

- `HarnessToolStepIntent`: durable identity before an effect-capable Runtime dispatch;
- `HarnessToolStepReceipt`: the observed, rejected, cancelled, or explicitly UNKNOWN result bound to that intent;
- `HarnessRunSnapshot`: a bounded pause/resume boundary for input, approval, or a prepared effect dispatch.

These objects do not own Task state, authority admission, Runtime Job state, Provider hidden state, or semantic completion. They bind identities across those owners.

## Thin-adapter rule

Host adaptation is limited to storing immutable Harness objects, validating current Assignment generation, and admitting completion. Runtime adaptation is limited to current Tool calls such as `workspace.exec`, `task.observe`, `task.cancel`, and Artifact reads.

No Harness table, daemon, scheduler, process registry, Runtime schema, or alternate Task state machine is admitted by this decision.

## Deletion test

A field remains only when deleting it permits one of these failures:

- dispatch occurs before its stable identity is durable;
- response loss permits blind redispatch;
- cancellation is reported as confirmed without Runtime evidence;
- a paused Run cannot bind its current Assignment and bounded Context;
- Provider replacement loses the identity needed to reconcile outstanding work.

Additional workflow, graph, routing, subagent, compaction, and persistent-Session objects remain deferred.
