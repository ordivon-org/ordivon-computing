# Observation Plane v0

Status: P0/P1 designed, not executed.

This experiment turns Host, Harness, Runtime, and future domain runs into automatically linkable evidence without creating a second authority plane.

- [`P0-P1-DESIGN.md`](P0-P1-DESIGN.md) — accepted architecture and implementation sequence;
- [`plan-v1.json`](plan-v1.json) — machine-readable plan `HHO-P0-P1-001`;
- [`tests/test_plan.py`](tests/test_plan.py) — plan integrity and boundary tests.

P0 makes Host and Harness independently durable. P1 exports committed owner-native events into a local non-authoritative observation gateway and OpenTelemetry-compatible projections. Formal repeated Harness Trials remain blocked until both phases close.
