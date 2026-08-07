# Experiment Loop v0

Status: designed, not executed.

Plan: `CEL-R4-001`.

This Track R experiment is the first consumer of [`../../research-method-v1.json`](../../research-method-v1.json). It tests the smallest bounded Agent-led loop that can turn validated Ordivon Trials and observed work burdens into another evidence-driven externalization experiment round without creating a second Host, scheduler, model router, deployment authority, or self-modification service.

- [`EXECUTION-PLAN.md`](EXECUTION-PLAN.md) — authority boundaries, records, roles, state machine, first campaigns, gates, and rollback;
- [`plan-v1.json`](plan-v1.json) — machine-readable execution plan;
- [`tests/test_plan.py`](tests/test_plan.py) — plan integrity and anti-expansion tests.

The dependency chain is strict:

```text
HHO-P1 Core observation
→ HHR-R3 formal repeated Trials
→ CEL-R4 bounded multi-round experiment loop
→ later ANC-ADAPT self-evolution evidence
```

P1 remains the sensing and evidence-query layer. R3 remains the Trial and validity layer. Experiment Loop v0 owns only research Campaign manifests, candidate lineage, round decisions, learning updates, and closeout receipts. Routine private and reversible research progression is Agent-led. Human attention is consequence-gated, and affected product/domain owners remain authoritative for product state, hidden graders, deployment, publication, and external commitments.
