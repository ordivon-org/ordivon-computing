# Semantic Core Backend Adapters

## Purpose

Adapters translate backend-specific Tool contracts into stable Semantic Core objects without leaking Git worktrees, systemd units, SQLite layouts, process IDs, or protocol envelopes into Kernel semantics.

```text
EffectSpec
→ stable Dispatch identity before invocation
→ backend Tool request
→ backend Job or synchronous receipt
→ Observation / Artifact evidence
→ semantic state transition
```

The standard runtime supplies `views.execution`, containing DISPATCH and OBSERVATION authority. Effect proposal, Verification, and Fact acceptance remain outside adapters. Returned projections are the official attested records read back from the Kernel after admission.

## Shared identity rules

| Semantic identity | Backend binding |
|---|---|
| EffectId | stable identity supplied above the adapter |
| DispatchId | one concrete boundary attempt, allocated before invocation |
| WorldObjectId | normalized repository, Workspace, file, process, or Artifact identity |
| ObservationId | digest-bound reading with Effect and Dispatch causality |
| ArtifactId | namespaced backend Artifact identity |
| EventId | semantic Journal identity, not a protocol request ID |

`clientRequestId` is a backend idempotency and correlation key. It is not the universal Effect identity. Beginning a request does not prove backend admission.

## Asynchronous Ordivon execution

```text
prepared Effect
→ Dispatch STARTED persisted
→ workspace.exec
→ correlated Job identity admits Dispatch
→ task.observe
→ running or terminal Observation
→ Artifact projection
→ semantic outcome
```

Normal observation and reconciliation are different paths:

```text
DISPATCHED / RUNNING / CANCEL_REQUESTED
→ task.observe
→ current or terminal evidence
```

```text
UNKNOWN
→ task.list correlation by stable clientRequestId
→ task.observe original Job or remain UNKNOWN
```

Transport or protocol loss after invocation begins becomes `UNKNOWN`. A correlated Job is observed and never redispatched. Structured rejection is classified only after correlation checks. Ordivon `lost` and `orphaned` project to semantic `UNKNOWN`.

Cancellation request and cancellation completion remain distinct. A natural terminal result may legitimately win a cancellation race.

## Versioned read

A file target is a versioned `WorldObjectRef`. `workspace.read` returns content and a digest; the adapter independently hashes UTF-8 content and rejects a malformed receipt whose digest differs.

```text
prepared read Effect
→ Dispatch STARTED
→ workspace.read
→ synchronous receipt admitted
→ Observation(target.version = digest)
→ Effect succeeds or records VERSION_MISMATCH
```

World drift is preserved as evidence. A version mismatch does not erase the admitted receipt or Observation.

## Atomic mutation

The current slice supports an existing file with compare-and-swap protection:

```text
workspace.mutate
mode = WRITE | APPEND | REPLACE_EXACT
expectedDigest = current version
```

A stale digest produces structured `INVALID_REQUEST`; the Dispatch is rejected and the Effect fails without changing the file. Transport uncertainty after invocation remains `UNKNOWN`, because the mutation may have crossed the world boundary.

Synchronous success is bound as a receipt identity:

```text
ordivon-receipt:<tool>:<dispatch-id>:<response-digest>
```

Dispatch identity keeps two content-identical reads causally distinct.

## Evidence and knowledge admission

Backend success enters the evidence path but does not directly create Fact.

```text
Mutation Effect succeeds
→ Claim(object version = expected digest)
→ separate Read Effect
→ Observation of the same WorldObject and version
→ Verification accepted or rejected
→ Fact accepted only by Fact authority
```

A zero process exit code is also backend evidence, not higher-level correctness. Output markers or other declared evidence must satisfy the originating Effect's Verification plan.

## Two-backend portability result

The Ordivon Adapter and deterministic simulator now run one shared semantic conformance suite despite using different operation names, status words, correlation keys, receipt structures, and backend identities. Their normalized semantic reports are exactly equal.

The comparison separates the boundary as follows:

| Universal semantic record | Backend-local mechanism |
|---|---|
| `EffectId` | proposal identity supplied above either Adapter |
| `DispatchId` | one boundary attempt allocated before either call |
| opaque backend operation binding | Ordivon Job ID or simulator operation ID |
| `UNKNOWN` | response loss, orphaned Job, or indeterminate inspection |
| `RECONCILING` | Job lookup/observe or correlation lookup/inspect |
| cancellation intent and outcome | `task.cancel` or simulator cancellation flag |
| Observation / Artifact | backend-specific payload and retained bytes |
| Authority / Attestation | the same scoped Kernel Views for both Adapters |

Backend implementation objects are scanned out of Kernel snapshots, and neither simulator nor portability driver is exported from the package root.

## Remaining Adapter questions

- Tool-contract identity and schema drift while an Effect is pending or a Job is running;
- reconciliation of uncertain synchronous mutation when no durable receipt is available;
- new-file and multi-file atomic mutation semantics;
- Artifact digest or identity mismatch against a live backend.

Executable and live evidence is indexed in [`CONFORMANCE.md`](CONFORMANCE.md).
