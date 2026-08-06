# Observation Minimum Core implementation

This directory is the executable M1 prototype for the non-authoritative Observation Plane. It remains in the Computing experiment until recurring producers and consumers justify extraction.

## Included

- strict metadata-only Envelope, Relation, Privacy, PayloadRef, Batch, and Acknowledgement contracts;
- deterministic native Event identity and canonical JSON digests;
- generated and frozen Draft 2020-12 JSON Schemas;
- an in-process SQLite Gateway with one-writer transactions, exact duplicate replay, corruption/gap/mapping/privacy quarantine, private modes, reopen, and full-history Doctor;
- a frozen synthetic Host/Harness/Runtime trajectory and deterministic catalog rebuild;
- installable `ObservationExportCheckpoint` and `ObservationExportBundle` contracts with digest-CAS sidecar writes and multi-stream support.

## Excluded

M1 does not import owner packages, read owner databases, implement exporter checkpoints, expose a daemon/socket/CLI, perform operational backup/restore, emit OpenTelemetry, decide Trial validity, or own Task/Run/Job/domain outcomes. Dynamic export and ingest times are receipt fields, not canonical Envelope fields.

## Verification

```bash
python3.12 -m unittest \
  research/experiments/observation-plane-v0/tests/test_contract.py \
  research/experiments/observation-plane-v0/tests/test_gateway.py \
  research/experiments/observation-plane-v0/tests/test_schema.py \
  research/experiments/observation-plane-v0/tests/test_fixture.py -v
ruff check \
  research/experiments/observation-plane-v0/implementation \
  research/experiments/observation-plane-v0/tests/test_contract.py \
  research/experiments/observation-plane-v0/tests/test_gateway.py \
  research/experiments/observation-plane-v0/tests/test_schema.py \
  research/experiments/observation-plane-v0/tests/test_fixture.py
```

## Exact owner dependency

Owner exporters must pin the shared package by exact Computing revision:

```text
ordivon-observation-core @ git+https://github.com/zycxfyh/ordivon-computing.git@b0973311d84b0debe30ca002e15e02401e16ee36#subdirectory=research/experiments/observation-plane-v0/implementation
```

Host and Harness use one global Journal stream. Runtime uses one stream per Job because Runtime has no durable global Event sequence. The checkpoint contract therefore stores a map of stream heads and never fabricates a Runtime-global order.

## M2 owner exporters

The shared package revision used by all three owner exporters is `b0973311d84b0debe30ca002e15e02401e16ee36`. The owner implementations are Host `e1c134f330a90c15495126a67021b06c56245156`, Harness `e3cb34b4991b5f52e1c0ed0151ea17b067e88e16`, and Runtime `8c22c2b409e99a0fd07fd72a9029ef8c74c6cb47`. They are run-once adapters, not product daemons or owner write paths.

Runtime exports one stream per Job from append-only `job_events`. Artifact lists are not attached to existing Job Events because later Artifacts would change historical Event digests. B3 must choose an independent append-only Artifact mapping or explicitly exclude Artifact traversal from its first trajectory.


## B3 cross-owner selection

B3 adds a narrow `cross-owner-task-trajectory-v1` query and an immutable `ObservationSelectionManifest`. The query is anchored by one Host Task and follows only the closed relation vocabulary needed to select the matching Harness Run and Runtime Job. The manifest freezes selected Event IDs and envelope digests, source-stream heads, mapping versions, completeness claims, privacy claims, a catalog digest, and a selection digest. It explicitly fixes `trialValidityInferred` to `false`.

The first trajectory uses `artifactCoverage=owner_native_only`. Runtime Artifact bytes and mutable Artifact lists are not copied into Observation or attached to historical Runtime Job Events. Owner-native Artifact evidence remains available to the formal runner and Host verifier.

Run the disposable real-owner acceptance without touching production roots:

```bash
python3.12 research/experiments/observation-plane-v0/scripts/run_b3_owner_native_acceptance.py
```

The acceptance constructs private one-trajectory Host, Harness, and Runtime stores using their real schemas, runs the three exact owner exporters, rebuilds two Gateways with different owner ingest order, and proves a stable catalog and selection digest. Removing the Runtime Bundle must produce an explicit incomplete selection rather than an inferred Trial verdict.
