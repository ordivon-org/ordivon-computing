# Harness Evaluation v0

Status: R0–R2 evidence contract and curated dogfood set implemented; Track R remains active at M3 for the bounded R3 comparison owned by `research/portfolio.json`.

## Question

Can a thin research envelope describe materially different Agent Harness experiments, support exact comparison and failure attribution, and preserve existing Host, Harness, Runtime, and Provider-native semantics?

## Hypothesis

Four append-only research records are sufficient for the first comparison:

```text
Task Definition
Trial Manifest
Trial Result
Failure Record
```

They reference component-native receipts and Artifacts rather than normalizing Provider lifecycles or creating a second execution plane.

## Contents

- [`schemas/task.schema.json`](schemas/task.schema.json) — formal Task and Task-QA metadata;
- [`schemas/trial.schema.json`](schemas/trial.schema.json) — one exact evaluation configuration;
- [`schemas/result.schema.json`](schemas/result.schema.json) — outcome, verifier, actions, cost, and evidence;
- [`schemas/failure-record.schema.json`](schemas/failure-record.schema.json) — first observable failure and recovery attribution;
- [`failure-taxonomy.yaml`](failure-taxonomy.yaml) — bounded v0 classes derived from observed Ordivon failures;
- [`validate_evaluation_evidence.py`](validate_evaluation_evidence.py) — standard-library semantic and integrity validator;
- [`examples/`](examples/) — historical projections from H3, H4, and the Codex→Hermes H5 trajectory;
- [`tests/`](tests/) — contract, tamper, relation, and semantic tests;
- [`dogfood-20260802/INDEX.md`](dogfood-20260802/INDEX.md) — curated real-run evidence index; diagnostic failures remain separate from accepted evidence.

## Historical admission

The H3–H5 examples are projections, not rewritten source receipts. Each retains the source repository path, exact SHA-256 file digest, and the limitations of the historical observation. Fields absent from the original evidence are `null`; they are not inferred.

The examples establish that the common envelope can represent:

- one Codex App Server Run that leaves the Host Task waiting;
- one Hermes ACP Run with a different Session/Prompt lifecycle and no retained thought text;
- one two-Harness replacement trajectory with stale-completion rejection, response-loss recovery, verified Artifacts, and accepted TaskOutcome.

They do not establish comparative model quality because task, model, budget, and Harness conditions differ.

## Validate

```bash
python3 research/experiments/harness-evaluation-v0/validate_evaluation_evidence.py \
  research/experiments/harness-evaluation-v0/examples/**/*.json

python3 -m unittest discover \
  -s research/experiments/harness-evaluation-v0/tests \
  -p 'test_*.py'
```

Use `--write-digests` only while authoring a new record before its first commit. A committed record is immutable; corrections create a new version or superseding record.

## Boundaries

This experiment does not:

- execute an Agent;
- dispatch Runtime work;
- alter Host completion state;
- require Provider reasoning text;
- provide a model leaderboard;
- define a universal trace format;
- authorize a standalone Eval service or repository.

## Current activation gate

R3 compares the same frozen repository-repair Task under one-shot execution, Ordivon Harness, and a mature Provider Harness after the product-owned QA gate passes. Computing retains only the evaluation envelope and curated projections; workload execution and temporary projection scripts remain product-owned or disposable.

## Canonicalization domain

Track R records use `ordivon-evidence-json-v1`: sorted-key compact JSON over the finite JSON number domain admitted by the evaluation schemas. This label is intentionally distinct from the integer-only strict `anc_canonical` protocol domain. The two profiles may share byte ordering without claiming the same accepted value set.
