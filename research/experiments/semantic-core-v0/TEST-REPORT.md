# Test Report

## Reference commands

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests scripts
```

## Reference result

```text
Python 3.12.13: 27 tests passed
Python 3.14.6:  27 tests passed
Bytecode compilation passed on both runtimes
git diff --check passed
```

## Covered semantic behaviours

- idempotent Effect admission and identity conflicts;
- independent Dispatch identity, optimistic revisions, and STARTED / ADMITTED / UNKNOWN / REJECTED lifecycle;
- non-regressing causal event time;
- unknown outcome and reconciliation without blind redispatch;
- retryable pre-admission rejection returns the Effect to prepared with a new future Dispatch;
- non-retryable rejection terminates the Effect; admitted/unknown Dispatches cannot be rewritten as rejected;
- immutable terminal outcomes;
- Observation/Artifact binding to Dispatch;
- equal content across distinct Dispatches retains distinct Observation identity;
- independent same-subject evidence may verify a Claim;
- different-subject, wrong-version, or future evidence is rejected;
- required evidence kinds and verification methods are enforced;
- rejected or missing Verification cannot create Fact;
- normal Ordivon running observation and scripted response-loss reconciliation;
- synchronous read and mutation payload projection;
- mutation response loss becomes unknown and is not repeated.

## Live Ordivon results

### Asynchronous execution

```text
initial state: running
terminal state: succeeded
correlated Jobs: 1
semantic Artifacts: 3
duplicate Dispatch blocked: true
stdout markers independently verified: true
Fact committed: true
```

### Versioned read and atomic mutation

```text
WRITE digest: sha256:9160d4be34c8695bd172a76c7c7966587ea5a4d991ad22c87b2b91af54aa9ebb
REPLACE_EXACT digest: sha256:7b9a72466d3960eb2aacccfc848939453490db0678bd4725def3f789b891c919
independently verified mutation Facts: 2
stale mutation state: failed
final content stable: true
final digest stable: true
```

The sanitized receipts are recorded in [`LIVE-REPORT.md`](LIVE-REPORT.md).

## Not yet proven

- deliberately injected live response loss;
- cancellation races against a real process;
- adapter or semantic-journal restart continuity;
- real Tool-schema drift;
- persistent journal reconstruction.
