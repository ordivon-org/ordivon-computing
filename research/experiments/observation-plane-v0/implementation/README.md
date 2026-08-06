# Observation Minimum Core implementation

This directory is the executable M1 prototype for the non-authoritative Observation Plane. It remains in the Computing experiment until recurring producers and consumers justify extraction.

## Included

- strict metadata-only Envelope, Relation, Privacy, PayloadRef, Batch, and Acknowledgement contracts;
- deterministic native Event identity and canonical JSON digests;
- generated and frozen Draft 2020-12 JSON Schemas;
- an in-process SQLite Gateway with one-writer transactions, exact duplicate replay, corruption/gap/mapping/privacy quarantine, private modes, reopen, and full-history Doctor;
- a frozen synthetic Host/Harness/Runtime trajectory and deterministic catalog rebuild.

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
