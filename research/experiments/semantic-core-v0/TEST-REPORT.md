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
75 tests passed
bytecode compilation passed
ruff passed
git diff --check passed
```


## Kernel Charter conformance

- K1 stable identity survives durable restart;
- K2 one Dispatch identity retains one Effect owner;
- K3 transport loss is durably represented as UNKNOWN;
- K4 reconciliation reuses the original Dispatch identity;
- K5 cancellation intent and observed terminal outcome remain causally distinct;
- K6 Fact admission requires Claim, accepted Verification, and permitted evidence;
- K7 injected admission failure restores every projection;
- K8 corrupted durable history fails closed;
- a drift guard binds all eight Charter clauses to canonical test names.

Detailed mapping: [`CHARTER-CONFORMANCE.md`](CHARTER-CONFORMANCE.md).

## M2.5 Authority and Attestation coverage

- scoped bootstrap exposes Effect, execution, Verification, Fact, and read-only Views;
- `AuthorizedKernel` construction is rooted in `AuthorityRoot`;
- role-specific signers cannot escalate into another role;
- execution Views cannot attest Verification or Fact state;
- forged Authority grants are rejected;
- semantic content changes invalidate existing Attestations;
- invariant scanning detects altered stored evidence;
- caller-supplied evidence signatures are rejected;
- Adapter projections return the official attested records;
- Verification and Fact acceptance retain distinct Authority identities;
- Attestation provenance survives Journal replay;
- changed policy fingerprints and wrong authority secrets reject replay;
- Journal schema v2 binds semantic model, reducer, and authority-policy versions.

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

Implementation source revision: `efc5b2bd33f7c94ab28859a8872869e71aa42fd8`

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
