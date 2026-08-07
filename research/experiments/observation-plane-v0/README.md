# Observation Plane v0

Status: Level A and P0 are closed. P1 Minimum Core, the three run-once owner exporters, deterministic cross-owner selection, B4 formal deterministic use, and fresh A0 O1 dogfood are complete. The B5 native Provider campaign is blocked by Provider/tool-call fidelity rather than Observation infrastructure. Production Observation authority remains intentionally inactive.

This experiment turns Host, Harness, Runtime, and future domain runs into automatically linkable evidence without creating a second authority plane.

- [`P0-P1-DESIGN.md`](P0-P1-DESIGN.md) — accepted architecture and authority boundary;
- [`P1-EXECUTION-PLAN.md`](P1-EXECUTION-PLAN.md) — executable P1 work packages, dependencies, gates, receipts, and rollback conditions;
- [`plan-v1.json`](plan-v1.json) — machine-readable plan `HHO-P0-P1-001` and current execution status;
- [`implementation/`](implementation/) — executable Minimum Core contract, Gateway, exporter support, and selection logic;
- [`schemas/`](schemas/) — Observation Envelope, export/checkpoint, ingest, and Selection schemas;
- [`owner-exporter-closeout-v1.json`](owner-exporter-closeout-v1.json) — exact Host/Harness/Runtime exporter closeout;
- [`evidence/b3-owner-native-e9bc8b4/`](evidence/b3-owner-native-e9bc8b4/) — owner-native three-stream reconstruction acceptance;
- [`../harness-evaluation-v0/evidence/b4-smoke-78de3a6/`](../harness-evaluation-v0/evidence/b4-smoke-78de3a6/) — first formal deterministic Trial consuming a frozen Observation Selection;
- [`../crosscut-a0-v0/`](../crosscut-a0-v0/) — fresh current three-owner dogfood plus bounded configuration/measurement cross-cutting acceptance;
- [`tests/`](tests/) — contract, privacy, Gateway, exporter, selection, and closeout tests.

The current Minimum Core is deliberately non-authoritative. Host, Harness, Runtime, and domains remain independently recoverable; exporters read committed owner-native state and may lag or fail without changing product truth. B3 proved a metadata-only twelve-event selection across three owner streams, B4 used the same boundary inside a valid formal Trial, and A0 O1 rebuilt a fresh 25-event Host/Harness/Runtime trajectory against a long-lived Runtime Registry with more than 20,000 Jobs. Observation completeness still does not imply Trial validity, Candidate quality, semantic completion, or domain truth.

O1 also established the correct growth pattern: dogfood first, then fix owner-local friction. Runtime gained exact Job selection because the previous global Job-count bound blocked a real bounded export; Harness gained terminal Run measurements only after its owner-native token aggregate was repaired. Neither finding justified continuous collection or another authority layer.

Further Observation work is evidence-gated. Reopen expansion only when another materially different workload repeatedly pays manual export/query cost or needs continuous telemetry. OpenTelemetry/Collector remains the inherited first baseline for continuous operational telemetry; a measurement index, dedicated daemon, or independent `ordivon-observation` repository remains unearned. See [`../../AGENT-FIRST-CROSSCUT-A0-AUDIT.md`](../../AGENT-FIRST-CROSSCUT-A0-AUDIT.md) for the A0 closeout.
