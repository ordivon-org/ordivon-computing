# 03 — Remediation and Deletion Gates

## P0 — authority correctness

### P0.1 Lease-fenced commit

- Carry the exact `LeaseRecord` into `LockedTask`.
- Check owner, lease revision and expiry in the same SQLite `BEGIN IMMEDIATE` transaction as event admission.
- Fail before writing when ownership is lost.
- Do not let release failure mask an already committed transition.
- Add thread/process takeover and slow-callback tests.

### P0.2 Immutable event-kind boundary

Replace dynamic `StrEnum._missing_()` with:

```text
CoreEventKind enum
+
immutable validated EventKind value
```

- reserve Host core namespaces;
- accept extension namespaces without global class mutation;
- preserve existing `harness.*` and `completion.*` history;
- add concurrent construction and typo rejection tests.

### P0.3 Outcome and terminal admission

- COMPLETED requires accepted verification when the workload declares accepted-verification completion.
- Failed/rejected Observation cannot be overwritten by caller status.
- `VerificationReceipt.accepted=false` cannot advance any result item.
- terminal Task states cannot transition to nonterminal states under the same identity.
- revised work uses a new Attempt or Task with explicit provenance.

### P0.4 Version-bound verification

For code-change verification, obtain a Runtime-provided stable Workspace generation or snapshot digest covering:

- source revision;
- current workspace tree/diff state;
- every verified file;
- dirty generation.

Commit only if the token still matches. Do not solve this by extending a Task lease across Runtime calls.

## P1 — evidence and privacy

### P1.1 Causal provenance

Choose one:

1. validate `caused_by_event_id` exists and precedes the new event; or
2. remove it in the next schema revision.

Add History Doctor checks and an index if retained.

### P1.2 Private state profile

- state root and CAS directories: 0700;
- SQLite, WAL/SHM, CAS objects and token files: 0600;
- backup/restore must preserve private modes;
- Doctor should report insecure modes;
- document the trusted-local single-user assumption.

### P1.3 Generic Effect lifecycle decision

Do not expand it further before a decision experiment.

**Keep/promote gate:** two distinct real repositories use it; unified recovery works; duplicated lifecycle code is deleted; total LOC and failure surface decrease.

**Delete/retreat gate:** no second consumer, no net deletion, or specialized workloads remain clearer and safer.

## P2 — subtraction and truthful claims

Evaluate removal or demotion of:

- `TaskState.PROPOSED`;
- `TaskState.RUNNING` until a real workload owns active-node semantics;
- `EventKind.WAKEUP_SCHEDULED`;
- `StreamKind.GOAL` until Goal streams exist;
- `expectedObservationKind` unless Observation gains enforceable type identity;
- production `boundary.py` ownership table if it remains test-only documentation.

Update architecture language:

- Host owns Goal-scoped Task coordination, not yet durable Goal commitments;
- external calls are not uniformly outside leases today;
- full historical semantic validation is optional Doctor work, not normal startup replay.

## Explicit non-goals

This remediation does not justify:

- a scheduler or DAG engine;
- distributed leases;
- a second database;
- a workflow DSL;
- Provider session persistence;
- re-coupling Harness into Host;
- a generic policy platform;
- additional Agent features.

The expected outcome is a smaller, more truthful and more deterministic Host.
