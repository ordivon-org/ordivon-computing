# Task Continuation v0 evidence

Exact revisions, Capsule digests, process identities, baseline sizes, field ablations, model decisions, executed Effects, Facts, and failure outcomes belong in immutable JSON receipts under [`evidence/`](evidence/).

## Exact implementation evidence

Implementation revision:

```text
f0cc83f709ff85b1b6a85302562fe904727fbc8b
```

- [`fixtures/checkpoint-f0cc83f/`](fixtures/checkpoint-f0cc83f/) — frozen checkpoint with three baselines, complete signed Bindings, content-addressed semantic records, rubric, manifest, and world object;
- [`evidence/freeze-f0cc83f.json`](evidence/freeze-f0cc83f.json) — exact checkpoint and Capsule identity;
- [`evidence/continuation-f0cc83f.json`](evidence/continuation-f0cc83f.json) — scripted completion, drift blocking, and real Codex `gpt-5.5` fresh-process continuation;
- [`evidence/evaluation-f0cc83f.json`](evidence/evaluation-f0cc83f.json) — semantic baseline, ablation, continuation, and model-agreement report.

The frozen Capsule digest is:

```text
sha256:c5cceb3d1f57904851968f8685c73a0f138a9147d9c6dde22ca74862c318a956
```

## Evidence classes

- deterministic tests: schema, store, validation, drift, UNKNOWN, model failure, repeat prevention, terminal Capsule, and frozen-receipt integrity;
- scripted fresh-process evidence: one child Host process completes and a separate drifted child blocks;
- Codex fresh-process evidence: a real model receives only compiled context and selects one exact allowed action;
- field ablation: removes decision Artifact, checkpoint Fact, current Binding, or completed Effect references.

## Manual generation

```bash
python3.12 scripts/run_continuation_evidence.py \
  --source-revision <exact-commit> \
  --output evidence/continuation-<short-commit>.json
```

Real-model evidence remains manual and must not become a pull-request requirement.
