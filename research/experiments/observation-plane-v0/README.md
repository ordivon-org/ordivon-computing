# Observation Plane v0

Status: Level A and P0 are closed. P1 Minimum Core, the three run-once owner exporters, deterministic cross-owner selection, and the B4 formal deterministic smoke are complete. The B5 native Provider campaign is blocked by Provider/tool-call fidelity rather than Observation infrastructure. Production observation authority remains intentionally inactive.

This experiment turns Host, Harness, Runtime, and future domain runs into automatically linkable evidence without creating a second authority plane.

- [`P0-P1-DESIGN.md`](P0-P1-DESIGN.md) — accepted architecture and authority boundary;
- [`P1-EXECUTION-PLAN.md`](P1-EXECUTION-PLAN.md) — executable P1 work packages, dependencies, gates, receipts, and rollback conditions;
- [`plan-v1.json`](plan-v1.json) — machine-readable plan `HHO-P0-P1-001` and current execution status;
- [`implementation/`](implementation/) — executable Minimum Core contract, Gateway, exporter support, and selection logic;
- [`schemas/`](schemas/) — Observation Envelope, export/checkpoint, ingest, and Selection schemas;
- [`owner-exporter-closeout-v1.json`](owner-exporter-closeout-v1.json) — exact Host/Harness/Runtime exporter closeout;
- [`evidence/b3-owner-native-e9bc8b4/`](evidence/b3-owner-native-e9bc8b4/) — owner-native three-stream reconstruction acceptance;
- [`../harness-evaluation-v0/evidence/b4-smoke-78de3a6/`](../harness-evaluation-v0/evidence/b4-smoke-78de3a6/) — first formal deterministic Trial consuming a frozen Observation Selection;
- [`tests/`](tests/) — contract, privacy, Gateway, exporter, selection, and closeout tests.

The current Minimum Core is deliberately non-authoritative. Host, Harness, Runtime, and domains remain independently recoverable; exporters read committed owner-native state and may lag or fail without changing product truth. B3 proved a metadata-only twelve-event selection across three owner streams, and B4 used the same selection boundary inside a valid formal Trial. Observation completeness still does not imply Trial validity, Candidate quality, semantic completion, or domain truth.

The next Observation work is dogfood, not platform expansion: reconstruct fresh current workloads, measure export/query friction, and add only operations that repeated Agent use proves missing. Continuous collection, an OpenTelemetry deployment, a measurement index, or an independent `ordivon-observation` repository remain evidence-gated rather than assumed next steps. See [`../../AGENT-FIRST-CROSSCUT-A0-AUDIT.md`](../../AGENT-FIRST-CROSSCUT-A0-AUDIT.md) for the current cross-cutting A0 decision.
