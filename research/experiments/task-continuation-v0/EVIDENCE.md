# Task Continuation v0 evidence

Exact revisions, Capsule digests, process identities, baseline sizes, field ablations, model decisions, executed Effects, Facts, and failure outcomes belong in immutable JSON receipts under [`evidence/`](evidence/).

## Evidence classes

- deterministic tests: schema, store, validation, drift, UNKNOWN, model failure, repeat prevention, and terminal Capsule;
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
