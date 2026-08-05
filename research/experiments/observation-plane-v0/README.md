# Observation Plane v0

Status: P0 implementation present with closeout pending; P1 execution designed and waiting for the P0 production gate.

This experiment turns Host, Harness, Runtime, and future domain runs into automatically linkable evidence without creating a second authority plane.

- [`P0-P1-DESIGN.md`](P0-P1-DESIGN.md) — accepted architecture and authority boundary;
- [`P1-EXECUTION-PLAN.md`](P1-EXECUTION-PLAN.md) — executable P1 work packages, dependencies, gates, receipts, and rollback conditions;
- [`plan-v1.json`](plan-v1.json) — machine-readable plan `HHO-P0-P1-001`;
- [`tests/test_plan.py`](tests/test_plan.py) — plan integrity and boundary tests.

P0 has landed the independent Harness store, standalone core, Host external-executor boundary, and cutover controls, but performance, recovery-gap, production state-root, and cutover receipts remain open. P1 contract and gateway work may proceed against fixtures; production exporters remain disabled until P0 closeout. Formal repeated Harness Trials remain blocked until P1 Core can reconstruct one complete deterministic Host–Harness–Runtime trajectory from owner-native references.
