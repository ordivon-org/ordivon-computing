# Research Evidence

This directory stores immutable, digest-bound evidence manifests for experiments that span repositories, services, Tool contracts, and generated Artifacts.

A System Snapshot answers:

```text
Which exact repository commits participated?
Which service binaries and configuration units were observed?
Which Tool-contract revisions or digests were bound?
Which evidence Artifacts were produced or consumed?
When was this combination observed?
```

It does not answer:

```text
What is the current deployment?
Which project is currently mature?
Which Issue is currently ready?
```

Those dynamic facts remain in the implementation repository, live service, or GitHub. A snapshot is historical evidence captured at one time.

## Files

- [`system-snapshot.schema.json`](system-snapshot.schema.json) — JSON Schema for the stable manifest shape;
- [`validate_system_snapshot.py`](validate_system_snapshot.py) — standard-library semantic and digest validator;
- [`snapshots/`](snapshots/) — append-only snapshot manifests.

## Immutability rule

A committed snapshot file is never edited. A correction or later observation creates a new snapshot with an optional `supersedes` reference.

Each manifest includes:

```text
schemaVersion
snapshotId
capturedAt
purpose
repository revisions
service binary and unit digests
Tool-contract digests, when available
evidence Artifact digests
payload integrity digest
```

The integrity digest is SHA-256 over canonical JSON with sorted keys and compact separators after removing the top-level `integrity` object. The validator recomputes this digest.

## Validate

```bash
python3 research/evidence/validate_system_snapshot.py \
  research/evidence/snapshots/*.json
```

Use `--write-digest` only before the first commit of a new snapshot:

```bash
python3 research/evidence/validate_system_snapshot.py \
  --write-digest research/evidence/snapshots/<new-snapshot>.json
```
