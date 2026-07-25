# Test Report

## Selected runtime

```text
Python 3.12.13
```


## Reference commands

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 -m compileall -q src tests scripts
```

## Reference result

```text
Python 3.12.13: 35 tests passed
Bytecode compilation passed
git diff --check passed
```

## Covered semantic behaviours

- idempotent Effect admission and identity conflicts;
- independent Dispatch identity, optimistic revisions, and STARTED / ADMITTED / UNKNOWN / REJECTED lifecycle;
- non-regressing causal event time;
- unknown outcome and reconciliation without blind redispatch;
- retryable pre-admission rejection returns the Effect to prepared with a new future Dispatch;
- non-retryable rejection terminates the Effect;
- admitted/unknown Dispatches cannot be rewritten as rejected;
- immutable terminal outcomes;
- Observation/Artifact binding to Dispatch;
- equal content across distinct Dispatches retains distinct Observation identity;
- independent same-subject evidence may verify a Claim;
- different-subject, wrong-version, or future evidence is rejected;
- required evidence kinds and verification methods are enforced;
- rejected or missing Verification cannot create Fact;
- versioned read, atomic mutation, receipt identity, and world-drift detection;
- real response loss becomes UNKNOWN and reconciles to the original Job;
- adapter-instance restart reconstructs pending identity from Effect and Dispatch records;
- `workspace.exec` is delivered exactly once during response-loss recovery;
- cancellation applied to a running Job reaches CANCELLED;
- natural completion may win the cancellation race and remain SUCCEEDED;
- a running observation does not erase CANCEL_REQUESTED intent.

## Live Ordivon results

### Response loss and adapter-instance restart

```text
initial state: unknown
terminal state: succeeded
workspace.exec deliveries: 1
correlated Jobs: 1
original Dispatch preserved: true
adapter instance restarted: true
semantic Artifacts: 3
```

### Cancellation race

```text
long-running Job: cancelled
short Job after delayed cancellation: succeeded
workspace.exec deliveries: 2
task.cancel calls: 2
invariant scan: passed
```

### Previously completed paths

```text
asynchronous execution: succeeded with one correlated Job
versioned read and atomic mutation: passed
independent digest Fact: committed
stale mutation: failed without changing final state
```

The sanitized receipts are recorded in [`LIVE-REPORT.md`](LIVE-REPORT.md) and [`FAILURE-REPORT.md`](FAILURE-REPORT.md).

## Not yet proven

- full semantic kernel/process restart continuity;
- persistent journal reconstruction;
- real pending/running Tool-schema drift;
- complete backend conformance.
