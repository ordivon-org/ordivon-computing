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

## Provider-comparison evidence

A #32 receipt must contain both `freshProcessCodex` and `freshProcessHermes`. The generated report requires identical Capsule and Context digests, identical exact decision identities and semantic execution results, distinct adapter identities, transcript-free processes, and successful completion. Hermes usage must report the requested model/Provider and at least one API call.

## Exact provider-replacement evidence

Implementation revision:

```text
1cdbbdc13514a3eb3663e2aa5bb66d077651c310
```

- [`evidence/provider-comparison-1cdbbdc.json`](evidence/provider-comparison-1cdbbdc.json) — Codex/GPT-5.5 and isolated Hermes/DeepSeek-V4-Pro fresh-process trajectories over the same Capsule and Context;
- [`evidence/provider-evaluation-1cdbbdc.json`](evidence/provider-evaluation-1cdbbdc.json) — exact provider-comparison acceptance report.

The exact comparison preserves Capsule identity, Context identity, decision identities, executed Effects, committed Facts, and transcript-free process boundaries. Hermes reports one real `deepseek-v4-pro` API call with zero Toolsets, no loaded memory, and no retained Provider session. Timing and token counts are single-run evidence, not general model-performance claims.
