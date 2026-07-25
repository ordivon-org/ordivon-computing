# Test Report

## Runtime

```text
Python 3.12.13
```

## Commands

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 -m compileall -q src tests scripts
ruff check src tests scripts
```

## Result

```text
53 tests passed
bytecode compilation passed
ruff passed
git diff --check passed
```

## M1.5 atomicity coverage

- Dispatch admission event conflict restores all projections;
- UNKNOWN time regression restores Effect and Dispatch;
- rejection event conflict restores Effect and Dispatch;
- an outer semantic transaction rolls back earlier successful commands;
- failed durable batches append zero journal rows;
- malformed Ordivon payloads leave no partial Job binding or admission Event and become UNKNOWN.

## M2 journal coverage

- reusable core conformance runs through JournalKernel;
- Effect and Event order survive reopen;
- every semantic projection rebuilds after reopen;
- separate Python processes write and reload the same journal;
- pending Job correlation survives Kernel reopen;
- normal successful Adapter projection commits transactionally through JournalKernel;
- transaction queries read staged state;
- idempotent no-op admission does not duplicate journal entries;
- hash-chain mutation, tail truncation, and missing durable-head metadata are detected;
- stale concurrent writers are rejected without publishing candidate state.

## Existing semantic and Adapter coverage

- Effect identity and revision conflicts;
- Dispatch STARTED / ADMITTED / UNKNOWN / REJECTED lifecycle;
- terminal immutability and event-time ordering;
- Observation and Artifact provenance;
- cross-Effect evidence scope and version checks;
- Claim → Verification → Fact admission;
- versioned read, atomic mutation, stale preconditions, and world drift;
- response loss, cancellation races, lost/orphaned uncertainty, and duplicate-dispatch prevention.

## Live Ordivon process-restart result

```text
initial state: unknown
terminal state: succeeded
kernel process restarted: true
workspace.exec deliveries: 1
correlated Jobs: 1
Dispatch identity preserved: true
semantic Artifacts: 3
journal entries before restart: 4
journal entries after recovery: 11
```

The detailed design and limits are recorded in [`JOURNAL.md`](JOURNAL.md).
