# Durable Semantic Journal v0

## Purpose

The Journal makes Semantic Core state independent of one Python process while inheriting SQLite WAL, locking, atomic commit, and crash recovery.

```text
Attested semantic command
→ validate the affected identities and local invariants
→ apply through a command-local undo savepoint
→ append canonical command and durable head in SQLite
→ release the in-memory savepoint
```

The semantic layer owns identity, causality, evidence, authority, and replay rules. SQLite owns durable byte storage.

## Runtime boundary

```text
role-scoped AuthorizedKernel Views
→ ReferenceReducer local semantic admission
→ JournalReducer durable command append
→ SQLiteSemanticJournal
```

The internal codec is a storage encoding, not the public Effect IR. Only an explicit allowlist of semantic dataclasses and enums may be decoded.

## Command atomicity

### ReferenceReducer

Each mutation records undo actions only for the dictionary keys and event-list suffixes it touches. Validation is performed before or at the affected mutation boundary. If any later step in the command fails, the reducer rolls back to the command savepoint.

The hot path does not clone all projections, compare complete snapshots, or scan unrelated Effects. A full `validate_invariants()` remains available and runs during replay, explicit audit, tests, and `verify_from_genesis()`.

### JournalReducer

A durable command runs inside the same reducer transaction that holds its undo log. SQLite append occurs before that transaction is released. Therefore:

```text
semantic validation fails → no Journal append and no state change
Journal append fails       → in-memory state rolls back
stale writer head          → JournalConflict and in-memory state rolls back
append succeeds            → the command is durable before control returns
```

Multi-command View transactions accumulate commands and append them in one SQLite transaction. Read-own-writes uses the same live reducer projection; no transaction clone is created.

The Dispatch start remains a separate durable command before the external Tool call.

## SQLite mechanics

```text
journal_mode = WAL
synchronous = FULL
foreign_keys = ON
busy_timeout = 5000 ms
```

`journal_entries` is append-only through triggers. Each entry stores sequence, operation, canonical signed command payload, previous digest, entry digest, and commit time.

## Integrity model

```text
entry_digest = SHA-256(previous_digest || canonical_payload)
```

Startup verifies:

- SQLite `quick_check`;
- Journal, semantic-model, reducer, and Authority-policy versions;
- contiguous sequence and predecessor linkage;
- every entry digest and durable head;
- operation/payload agreement and allowlisted types;
- Authority grants, Attestation roles, exact semantic digests, contract versions, times, and signatures;
- deterministic replay and the complete Kernel invariant audit.

This detects accidental or partial corruption. It is not a signature against an administrator who rewrites the entire database coherently.

## Journal schema v4

Schema v4 adds signed `BindingAdmission` commands and optional Binding references on `DispatchRecord`. Known schema-v2 and schema-v3 Journals migrate in place only after their exact semantic-model version, reducer version, and Authority-policy fingerprint match. Existing legacy command payloads remain immutable; newly appended commands use schema v4. Legacy Dispatches decode with `binding_id = None` and `binding_digest = None`.

The following fields remain decode-only compatibility fields and are rejected for new Effects:

```text
free-text Precondition
parent_task_id
parent_attempt_id
idempotency_key / KEYED idempotency
CapabilityRef.valid_until_ms
```

Task lineage belongs above the Kernel. Keyed idempotency and expiry require real Tool Binding or policy enforcement before they re-enter the active model.

## Replay and audit

Normal open verifies and replays the complete command history into a fresh `ReferenceReducer`, then runs the full invariant audit. `verify_from_genesis()` independently repeats this reconstruction and compares the resulting projection with the live one.

Rebuilt projections include Effects, Dispatches, Events, Observations, Artifacts, Claims, Verifications, and Facts.

## Concurrent writers

Each `JournalReducer` records the head observed during open. Writes use that sequence/digest as a compare-and-swap precondition inside `BEGIN IMMEDIATE`. A stale process receives `JournalConflict`; no stale command is appended and its in-memory mutation is undone.

## Checkpoint experiment

Checkpoint/tail replay was implemented and benchmarked at exact prototype revision `23353fdd550badf090c404861755131a70b7807b`. At 1,000 Effects / 2,000 commands with a checkpoint after 900 Effects:

```text
checkpoint reopen: 359.628 ms
genesis verify:    332.942 ms
database size:     12,464,128 bytes
```

The snapshot duplicated state, increased storage, and was slower than the optimized genesis path. The runtime checkpoint implementation was therefore removed. Git history and `benchmark-results/prototype-23353fd.json` preserve the experiment. Checkpointing remains deferred until a different representation demonstrates positive net value.

## Live recovery

The signed restart scenario still requires exactly one external delivery:

```text
Dispatch intent persisted
→ successful response deliberately lost
→ Effect and Dispatch become UNKNOWN
→ Python process exits
→ Journal reopens and reauthenticates commands
→ original Job is correlated
→ original Dispatch reaches SUCCEEDED
```

Exact post-change live evidence is recorded in `CONFORMANCE.md`.
