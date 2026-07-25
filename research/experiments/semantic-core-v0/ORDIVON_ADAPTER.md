# Ordivon Adapter Design

## Current status

The adapter has passed live asynchronous execution, versioned read, and atomic mutation slices through Ordivon's public MCP contract. It is still an experiment rather than a production adapter.

Proven live:

```text
Effect preparation
→ stable Dispatch STARTED identity
→ workspace.exec
→ Dispatch ADMITTED only after Job identity exists
→ running Observation
→ task.observe
→ succeeded terminal Observation
→ Artifact projection
→ artifact.read verification
→ Claim → Verification → Fact
```

Proven live: response-loss recovery without redispatch, adapter-instance restart correlation, cancellation applied to a running Job, and natural completion winning a cancellation race. Full process restart and Tool-schema drift remain open.

## Boundary

The adapter must not leak systemd units, Git worktree paths, SQLite layouts, process IDs, or protocol envelopes into the semantic core.

```text
EffectSpec
→ Ordivon Tool arguments
→ stable clientRequestId and DispatchId
→ Job / Attempt correlation
→ TaskObservation and Artifact evidence
→ semantic state transition
```

## Identity binding

| Semantic identity | Initial Ordivon binding |
|---|---|
| EffectId | stable identity supplied above the adapter |
| DispatchId | stable boundary-attempt identity derived before invocation |
| WorldObjectId | normalized repository, Workspace, file, process, or Artifact identity |
| ObservationId | digest-bound reading from one public Tool payload |
| ArtifactId | namespaced Ordivon Artifact identity |
| EventId | semantic journal identity, not a protocol request ID |

`clientRequestId` is a backend idempotency and correlation key. It is not the universal Effect identity. A Tool request may begin while the semantic Dispatch remains STARTED; only a correlated Job or synchronous result admits it.

## Normal observation and reconciliation

These are separate semantic paths:

```text
DISPATCHED / RUNNING / CANCEL_REQUESTED
→ observe()
→ task.observe
→ current or terminal evidence
```

```text
UNKNOWN
→ reconcile()
→ task.list correlation
→ task.observe or continued UNKNOWN
```

A normal running Effect must not enter reconciliation merely because it still needs observation.

## Uncertainty handling

- transport or protocol loss after invocation begins → `unknown`;
- structured Tool rejection → search by `clientRequestId` before classifying;
- correlated Job found → observe the existing Job, never redispatch;
- no correlated Job after a structured rejection → semantic `failed` for this Effect;
- Ordivon `lost` or `orphaned` → semantic `unknown`.

## Evidence translation

### Workspace read

```text
workspace.read
→ Observation(payload digest, object version, slice identity)
→ Claim
→ Verification
→ Fact
```

### Atomic mutation

```text
precondition: expected revision or digest
workspace.mutate
→ Observation(new digest or revision)
→ independent read or diff
→ Verification
→ Fact
```

### Long command

```text
workspace.exec
→ DispatchRecord
→ Job / Attempt binding
→ running Observations
→ terminal Observation and Artifacts
→ semantic outcome
```

A zero exit code remains backend evidence; it is not sufficient proof of higher-level correctness. The live slice independently read stdout and verified expected markers before admitting Fact.

## Remaining focused tests

1. `Lost`/`Orphaned` live reconciliation;
2. Artifact digest or identity mismatch against a live backend;
3. Tool-schema change while an Effect is pending;
4. Tool-schema change while a Job is running;
5. invariant reconstruction after full process restart.
