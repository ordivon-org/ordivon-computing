# Observation Plane v0

Status: Level A and P0 closeout passed; P1 Minimum Core M1 contract, in-process Gateway, schemas, privacy enforcement, and synthetic rebuild fixture are implemented. Run-once owner exporters remain pending.

This experiment turns Host, Harness, Runtime, and future domain runs into automatically linkable evidence without creating a second authority plane.

- [`P0-P1-DESIGN.md`](P0-P1-DESIGN.md) — accepted architecture and authority boundary;
- [`P1-EXECUTION-PLAN.md`](P1-EXECUTION-PLAN.md) — executable P1 work packages, dependencies, gates, receipts, and rollback conditions;
- [`plan-v1.json`](plan-v1.json) — machine-readable plan `HHO-P0-P1-001`;
- [`implementation/`](implementation/) — executable Minimum Core contract and in-process Gateway;
- [`schemas/`](schemas/) — frozen Observation Envelope, Batch, and Acknowledgement JSON Schemas;
- [`fixtures/three-owner-trajectory-v1.json`](fixtures/three-owner-trajectory-v1.json) — metadata-only Host/Harness/Runtime reconstruction fixture;
- [`tests/test_plan.py`](tests/test_plan.py) — plan integrity and boundary tests.

Level A closed the independent Harness persistence, exact release graph, live Host–Harness–Runtime journey, scale gate, and staging backup/restore/cutover rehearsal without activating production authority. P1 M1 now provides a strict metadata-only contract, an atomic SQLite Gateway, explicit duplicate/corruption/gap/privacy behavior, and deterministic reconstruction of a 13-event three-owner fixture. The next frontier is three run-once read-only owner exporters, followed by cross-owner trajectory selection. Formal repeated Harness Trials remain blocked until the complete Minimum Core freezes one `ObservationSelectionManifest`. P1 reports evidence completeness, not Trial validity or Candidate quality; those belong to R3 and the later [`../experiment-loop-v0/`](../experiment-loop-v0/) plan.
