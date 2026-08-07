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

## Content governance evidence

Cross-repository content baselines are diagnostic inventory evidence rather than mutable quality or maturity authorities:

- [`content-engineering-p0-baseline.md`](content-engineering-p0-baseline.md) and its [JSON receipt](content-engineering-p0-baseline.json) preserve the initial pre-governance inventory;
- [`content-engineering-closeout-baseline.md`](content-engineering-closeout-baseline.md) and its [JSON receipt](content-engineering-closeout-baseline.json) preserve the post-governance inventory and comparison;
- [`../../docs/content-engineering/FINAL-CLOSEOUT.md`](../../docs/content-engineering/FINAL-CLOSEOUT.md) records the resolved authority, navigation, lifecycle, and maintenance decisions.

Counts may expose review pressure, but they do not authorize deletion, rewriting, metadata promotion, or a claim that one repository is better documented than another.

## Agent-first historical compression

[`agent-first-historical-research-compression-f95d721.json`](agent-first-historical-research-compression-f95d721.json) records the one-time removal of completed, absorbed, superseded, or dated Computing studies from the current tree. Each removed study is bound to the exact pre-compression Git revision, path, tree object, and file count. [`../../scripts/check_historical_research_compression.py`](../../scripts/check_historical_research_compression.py) verifies that the current tree stays compressed while every recorded historical tree remains exactly recoverable from Git.

The receipt is not a substitute for live research evidence and does not make historical narrative authoritative. Current reusable conclusions live in Knowledge; live hypotheses retain only their question, baseline, falsifier, and exact evidence references.

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

The integrity digest is SHA-256 over canonical JSON with sorted keys and compact separators after removing the top-level `integrity` object. The validator recomputes this digest. For an Artifact with `path` and `repositoryId`, the validator reads that path from the exact repository commit recorded in the snapshot and verifies the content digest. The path does not need to remain in the current tree; validation requires the recorded Git commit to remain reachable, so CI checks out complete history.

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
