# Test Report

## Reference commands

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests scripts
```

## Reference result

```text
Python 3.12.13: 31 tests passed
Python 3.14.6:  31 tests passed
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
before digest: sha256:8bf8ee1400851e9b01f687cac287cf26681d3b7ca49a345ce0efd1123d1573dd
after digest:  sha256:ae422cadc74a5b2f5c4eff147494edb0b68e0f83275c0d4874da986f060e2fb4
independent reread Fact: committed
stale mutation state: failed
stale mutation code: INVALID_REQUEST
```

The sanitized receipts are recorded in [`LIVE-REPORT.md`](LIVE-REPORT.md).

## Not yet proven

- deliberately injected live response loss;
- cancellation races against a real process;
- adapter or semantic-journal restart continuity;
- real Tool-schema drift;
- persistent journal reconstruction.
