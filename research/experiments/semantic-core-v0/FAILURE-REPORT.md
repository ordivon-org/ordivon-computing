# Failure Semantics v0 Report

## Scope

The normative failure taxonomy and required response classes are defined in [`FAILURE-MODEL.md`](FAILURE-MODEL.md). This report records the failure-continuity slice executed against the local Ordivon public MCP endpoint on July 26, 2026.

Selected runtime:

```text
Python 3.12.13
```

## A. Lost response after successful delivery

The harness delivered a real `workspace.exec` call to Ordivon, allowed the backend to create the Job, then deliberately discarded the successful response and raised a transport error to the adapter.

Expected semantic path:

```text
Dispatch STARTED
→ successful backend delivery, response discarded
→ Dispatch UNKNOWN
→ old adapter instance discarded
→ new adapter reconstructs pending identity
→ task.list by stable clientRequestId
→ original Job found
→ task.observe
→ Dispatch ADMITTED
→ Effect SUCCEEDED
```

Sanitized receipt:

```json
{
  "adapterInstanceRestarted": true,
  "attemptId": "attempt-019f9a73-e6bd-7d50-9d52-0da25121a0d2",
  "correlatedJobCount": 1,
  "dispatchIdPreserved": true,
  "initialState": "unknown",
  "jobId": "job-019f9a73-e6bd-7d50-9d52-0d9ea6ce1277",
  "responseDroppedAfterSuccessfulDelivery": true,
  "semanticArtifactCount": 3,
  "sourceRevision": "d45ba1b1165e0fa863810c2e23f0086d0fedb3d6",
  "terminalState": "succeeded",
  "workspaceExecDeliveries": 1,
  "workspaceId": "anc-live-response-loss-1785002714647"
}
```

Supported conclusions:

- response loss is not backend failure;
- UNKNOWN prevented blind redispatch;
- a new adapter instance reconstructed `_PendingDispatch` from durable Effect and Dispatch records;
- stable `clientRequestId(effect_id)` found exactly one original Job;
- original Dispatch identity was preserved;
- `workspace.exec` crossed the boundary exactly once.

Boundary:

That earlier run kept the reducer in memory and proved adapter-instance restart. M2 added full local Python-process reconstruction. M2.5 now replays the same recovery path through Journal schema v2, scoped execution Authority, and content-bound Attestations; see `JOURNAL.md`, `AUTHORITY.md`, and `LIVE-REPORT.md`.

## B. Cancellation race

Two real Jobs were used.

### Cancellation applied first

```text
long command
→ running
→ CANCEL_REQUESTED
→ task.cancel
→ cancelled
```

### Natural completion wins

```text
short command
→ running
→ process completes
→ cancellation attempted later
→ task.observe original Job
→ succeeded
```

Sanitized receipt:

```json
{
  "cancelApplied": {
    "attemptId": "attempt-019f9a74-da3c-7273-8541-337e3e89cb1c",
    "jobId": "job-019f9a74-da3c-7273-8541-336850d1bb02",
    "state": "cancelled"
  },
  "invariantsValid": true,
  "naturalCompletionWon": {
    "attemptId": "attempt-019f9a74-dbd4-7693-b111-3a3bab6eb510",
    "jobId": "job-019f9a74-dbd4-7693-b111-3a2ccd9daba8",
    "state": "succeeded"
  },
  "sourceRevision": "d45ba1b1165e0fa863810c2e23f0086d0fedb3d6",
  "taskCancelCalls": 2,
  "workspaceExecDeliveries": 2,
  "workspaceId": "anc-live-cancel-race-1785002776989"
}
```

Supported conclusions:

- cancellation request and cancellation completion are different facts;
- `CANCEL_REQUESTED` does not overwrite a natural terminal result;
- cancellation can legitimately terminate as either CANCELLED or SUCCEEDED depending on observed world order;
- both terminal results retain their original Job and Dispatch identity;
- no duplicate execution was created.

## Remaining failure boundary

Not proven in this slice:

- replicated or multi-host journal recovery;
- server restart while a Job is running;
- Tool-schema drift while pending or running;
- network partitions longer than Job retention;
- complete Ordivon failure-state coverage.
