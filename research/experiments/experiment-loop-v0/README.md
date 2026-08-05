# Experiment Loop v0

Status: designed, not executed.

Plan: `CEL-R4-001`.

This Track R experiment tests the smallest bounded loop that can turn validated Ordivon Trials into another evidence-driven experiment round without creating a second Host, scheduler, model router, deployment authority, or self-modification service.

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

P1 remains the sensing and evidence-query layer. R3 remains the Trial and validity layer. Experiment Loop v0 owns only research Campaign manifests, candidate lineage, round decisions, learning updates, and closeout receipts. It cannot modify product authority, hidden graders, baseline evidence, or production deployments.
