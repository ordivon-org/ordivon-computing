# Durable Semantic Journal v0

## Purpose

M2 makes Semantic Core state independent of one Python process while deliberately inheriting mature classical mechanisms instead of rebuilding storage from first principles.

```text
Attested semantic command
→ verify Authority role and exact-content signature
→ validate against a candidate ReferenceKernel
→ SQLite transaction
→ append command entries and durable head
→ commit
→ publish the candidate projection
```

The semantic layer owns identity, causality, evidence, and replay rules. SQLite owns file locking, WAL, atomic commit, durability mechanics, and crash-safe storage.

## Runtime boundary

`ReferenceKernel` remains the executable semantic reducer. `JournalKernel` composes the reducer with durable storage, while public runtime access is issued through role-scoped `AuthorizedKernel` Views:

```text
ReferenceKernel
SQLiteSemanticJournal
internal journal codec v2
AuthorityPolicy verification
```

The internal codec is a storage encoding, not the public Effect IR planned for M3. Only an allowlist of current semantic dataclasses and enums may be decoded, including `AuthorityRef`, `Attestation`, `AuthorityRole`, and `AttestationKind`.

## M1.5 atomicity

### Single semantic command

Every mutating `ReferenceKernel` operation snapshots all projections, performs the operation, validates invariants, and restores the complete snapshot on any exception.

An invalid event identity, stale revision, backward time, or cross-object invariant can no longer leave a partial Dispatch, Event, Observation, Claim, or Fact update.

### Multi-command semantic transaction

`SemanticKernel.transaction()` groups related operations. Successful groups commit together; an exception restores the state that existed before the outer transaction.

The Ordivon adapters use this boundary for:

- Dispatch admission + Observation + Artifact projection + terminal Effect state;
- synchronous receipt + Observation + terminal read/mutation state;
- Claim + Verification + optional Fact admission.

The Dispatch start is intentionally committed before the external Tool call. This preserves the real boundary order and makes response loss recoverable.

### Malformed backend results

If a backend result cannot be translated consistently, the result projection is rolled back and the original Dispatch becomes `UNKNOWN`. No partial Job binding or evidence remains, and reconciliation is required.

## SQLite storage mechanics

The journal uses Python's standard-library `sqlite3` with:

```text
journal_mode = WAL
synchronous = FULL
foreign_keys = ON
busy_timeout = 5000 ms
```

`journal_entries` is append-only through SQLite triggers that reject UPDATE and DELETE. Each row stores sequence, operation, canonical signed command payload, previous digest, entry digest, and commit time. Commands in one semantic transaction are appended inside one SQLite transaction.

## Integrity model

Each entry digest binds the previous digest and canonical payload:

```text
entry_digest = SHA-256(previous_digest || canonical_payload)
```

The journal also stores a durable head sequence and digest. Startup verifies:

- SQLite `quick_check`;
- supported Journal schema version;
- semantic model version;
- reducer version;
- authority-policy fingerprint;
- contiguous sequence numbers;
- predecessor linkage and every entry digest;
- operation column/payload agreement;
- command schema and type allowlist;
- reconstructed tail against the durable head;
- Authority grant signatures and required roles;
- Attestation kind, exact semantic digest, contract version, record time, and signature;
- semantic replay and all Kernel invariants.

Missing head metadata on a non-empty journal, middle-entry mutation, sequence gaps, and tail truncation are reported as corruption rather than normalized.

This is integrity checking, not a cryptographic signature against an administrator who can rewrite the entire database and metadata coherently.

## Replay

Opening the Journal with its `AuthorityPolicy` creates a fresh `ReferenceKernel`, verifies every journal entry and Attestation, decodes each command, applies it in sequence, and validates the resulting projection. The standard bootstrap returns scoped Authority Views over the reconstructed Kernel.

The following projections are rebuilt:

```text
effects
dispatches
effect events
observations
artifacts
claims
verifications
facts
```

Typed getters expose each rebuilt object.

## Concurrent writers

Every `JournalKernel` records the journal head observed during replay. A write uses that sequence/digest as a compare-and-swap precondition inside `BEGIN IMMEDIATE`.

If another process has committed first, the stale process receives `JournalConflict`; its candidate projection is not published and no stale command is appended.

This provides one durable SQLite writer order. It is not distributed consensus or multi-host replication.

## Proven live recovery

A real `workspace.exec` call was delivered to Ordivon and its successful response was deliberately discarded. The first Python process persisted Effect preparation, Dispatch start, and an unknown outcome, then exited.

A second process reopened the journal, rebuilt the Effect and Dispatch, found the original Job by stable identity, observed terminal success, and appended admission, Observation, Artifact, and terminal commands. A third open independently replayed the final state.

Latest signed result, executed from implementation commit `88678a3c06f406c41eadb0ded484d09aa656ae43`:

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
Authority policy reauthenticated: true
all stored Attestations replayed: true
```

The first process generated one ephemeral 32-byte root secret and used scoped Effect and execution Views. The child process received the same secret through its environment, reconstructed the Authority policy, verified Journal schema v2 metadata, reauthenticated every signed command, and continued the original Dispatch. The secret was not printed or stored in the Journal.

## Production extensions

The next storage-engineering layers are snapshots, compaction, archival, encryption policy, online schema migration, replicated deployment, and long-Journal performance work. The next semantic vertical slice develops the public Effect IR and evolving Tool contracts together. These extensions build on the signed local semantic history established by Journal schema v2.
