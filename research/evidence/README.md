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

Changing deployment, project, and Issue state remains in the implementation repository, live service, or GitHub. A snapshot binds one historical observation to exact revisions and digests.

## Files

- [`system-snapshot.schema.json`](system-snapshot.schema.json) — JSON Schema for the stable manifest shape;
- [`validate_system_snapshot.py`](validate_system_snapshot.py) — standard-library semantic and digest validator;
- [`snapshots/`](snapshots/) — append-only snapshot manifests;
- [`../../projects/conformance.toml`](../../projects/conformance.toml) — stable project and Protocol conformance declarations;
- [`../../scripts/ordivon_conformance.py`](../../scripts/ordivon_conformance.py) — deterministic gate, revision-vector, Host-pin, and snapshot capture entry point.

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
evidence Artifact digests and source repository binding
payload integrity digest
```

The integrity digest is SHA-256 over canonical JSON with sorted keys and compact separators after removing the top-level `integrity` object. The validator recomputes this digest. For an Artifact with `path` and `repositoryId`, the validator reads that path from the exact repository commit recorded in the snapshot and verifies the content digest.

## Capture repository state

From the ordinary `/root/projects/ordivon-computing` checkout, sibling Ordivon repositories are discovered from `projects/conformance.toml`. Explicit `--repository-root ID=PATH` bindings can select isolated Workspaces or historical checkouts instead.

```bash
python3.12 scripts/ordivon_conformance.py vector \
  --require-all --require-clean \
  --output /tmp/ordivon-revision-vector.json

python3.12 scripts/ordivon_conformance.py snapshot \
  --require-all \
  --snapshot-id ordivon-system-<timestamp> \
  --purpose "<bounded experiment or closeout>" \
  --output research/evidence/snapshots/<snapshot>.json
```

The vector is an operational inspection receipt and may be replaced. A committed System Snapshot is immutable.

## Validate

```bash
python3.12 research/evidence/validate_system_snapshot.py \
  research/evidence/snapshots/*.json
```

Use `--write-digest` only before the first commit of a manually constructed snapshot. The automated snapshot command writes and validates its digest directly.
