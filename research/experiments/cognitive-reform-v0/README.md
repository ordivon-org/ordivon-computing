# Cognitive Reform Execution Program v0

This directory coordinates the bounded implementation program derived from `ANC-COMPILER-002` without turning the Temporal Cognitive Graph into a pre-approved product architecture.

Current execution is limited to **Level A**:

- `A1` — Ordivon Harness P0 final closeout in `ordivon-harness`;
- `A2` — correct the Computing plan, remove stale blockers, freeze work packages and gates.

The machine-readable authority for this execution program is [`program-v1.json`](program-v1.json). Product behavior remains owned by Host, Harness, and Runtime. Research status remains owned by [`../../portfolio.json`](../../portfolio.json).

## Program rule

```text
close current authority and evidence gaps
→ build the strong sequential baseline
→ run a shadow cognitive-state experiment
→ promote only the smallest layer that beats the baseline
```

Run Actor scheduling, Child Runs, Prime/RLM Engine integration, Runtime Workers, Workspace fork/merge, graph databases, and continual Harness activation remain conditional. They are not Level A deliverables and are not prerequisites for the first TCG ablation.

## Validation

```bash
python3 -m unittest research/experiments/cognitive-reform-v0/tests/test_program.py
```
