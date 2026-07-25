# Test Report

## Commands

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```

## Current result

```text
Python 3.12.13: 16 tests passed
Python 3.14.6:  16 tests passed
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
- scripted response-loss reconciliation without duplicate `workspace.exec`;
- structured Tool rejection is distinguished from unknown delivery;
- Ordivon Artifact projection preserves provenance.

## Not yet proven

- live Ordivon backend conformance;
- process-restart durability;
- real Tool-schema drift;
- cancellation races against a real process;
- persistent journal reconstruction.
