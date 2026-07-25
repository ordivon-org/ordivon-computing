# Status

## Completed

- Python 3.12.13 is the single reference and acceptance runtime.
- M0 semantic reference kernel implemented.
- 35 unit and conformance tests pass on Python 3.12.13.
- Effect, Dispatch, backend admission, Observation content identity, and causal observation identity are distinct.
- VerificationPlan, subject/version scope, and evidence-time ordering are enforced.
- Independent read Effects can verify mutation Claims without permitting unrelated evidence.
- Live asynchronous execution, versioned read, atomic mutation, Artifact projection, and digest Fact admission passed through the public Ordivon MCP contract.
- Retryable and non-retryable pre-admission rejections preserve distinct semantics.
- Deliberately lost `workspace.exec` responses recover by stable identity without redispatch.
- A new adapter instance can reconstruct the pending binding from persistent Effect and Dispatch records and recover the same Job.
- Live cancellation reaches `cancelled` when applied; natural completion may legitimately win the race and remain `succeeded`.
- Two concurrent Semantic Core implementations and the dedicated I/O subsystem were semantically integrated rather than overwritten.

## Current live coverage

```text
workspace.open
workspace.read
workspace.mutate
workspace.exec
task.observe
task.list
task.cancel
artifact.read
workspace.close
```

## Current claim boundary

The experiment proves the semantic reference model, the four required operation classes, response-loss recovery, adapter-instance restart correlation, and cancellation races against one real Ordivon backend.

It does **not** yet prove:

- persistence across a full kernel/process restart;
- durable journal reconstruction;
- pending or running Tool-contract drift;
- complete Ordivon conformance;
- production readiness or Goal-level correctness.

## Next executable work

1. build the durable semantic journal;
2. reconstruct kernel projections after process restart;
3. test pending/running Tool-contract drift;
4. only then consider Effect IR serialization and Task runtime work.
