# Ordivon Adapter Design

## Current status

A scripted adapter prototype exists. It translates Ordivon's public Tool payloads into the reference semantic model, but it has not yet passed a live backend conformance run. No production MCP client is included in this experiment.

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
| WorldObjectId | normalized repository, workspace, file, process, or artifact identity |
| ObservationId | digest-bound reading from one public Tool payload |
| ArtifactId | namespaced Ordivon Artifact identity |
| EventId | semantic journal identity, not a protocol request ID |

`clientRequestId` is a backend idempotency and correlation key. It is not the universal Effect identity.

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

A zero exit code remains backend evidence; it is not sufficient proof of higher-level correctness.

## Required live tests

1. successful Job and Artifact projection;
2. duplicate delivery without duplicate Job;
3. response loss after durable admission;
4. structured rejection before admission;
5. `Lost`/`Orphaned` reconciliation;
6. cancellation racing with natural completion;
7. Artifact digest or identity mismatch;
8. stale Workspace revision;
9. Tool-schema change while an Effect is pending;
10. Tool-schema change while a Job is running;
11. invariant scan after adapter restart.
