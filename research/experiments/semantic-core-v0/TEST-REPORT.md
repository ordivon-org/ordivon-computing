# Test Report

## Reference commands

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```

## Reference result

```text
Python 3.12.13: 17 tests passed
Python 3.14.6:  17 tests passed
Bytecode compilation passed on both runtimes
git diff --check passed
```

## Covered behaviours

- reusable reference conformance scenarios;
- idempotent Effect admission and identity-conflict rejection;
- optimistic revision conflicts;
- independent DispatchRecord identity and ownership;
- non-regressing causal event time;
- unknown outcome cannot blindly redispatch;
- unknown outcome can reconcile to a correlated terminal result;
- immutable terminal outcomes;
- Observation must match the bound Dispatch;
- accepted Verification must satisfy required evidence kinds;
- Verification cannot borrow another Effect's evidence;
- rejected Verification cannot create Fact;
- missing Claim or Verification cannot create Fact;
- Fact cannot predate Verification;
- Ordivon public status preserves uncertainty;
- scripted normal observation from `running` to terminal;
- scripted response-loss reconciliation without duplicate `workspace.exec`;
- structured Tool rejection is distinguished from unknown delivery;
- Ordivon Artifact projection preserves provenance.

## Live Ordivon result

A reproducible local run used the public MCP endpoint and these Tool operations:

```text
workspace.open
workspace.exec
task.observe
task.list
artifact.read
workspace.close
```

Observed result:

```text
initial semantic state: running
terminal semantic state: succeeded
semantic Artifact count: 3
correlated Job count: 1
duplicate Dispatch blocked: true
stdout markers verified: true
Fact committed: true
Workspace closed: true
```

The exact sanitized receipt is recorded in [`LIVE-REPORT.md`](LIVE-REPORT.md).

## Not yet proven

- versioned read and atomic mutation through semantic adapters;
- deliberately injected response loss against the live backend;
- process-restart semantic durability;
- real Tool-schema drift;
- cancellation races against a real process;
- persistent journal reconstruction.
