# Cognitive Reform Execution Program v0

This directory coordinates the bounded implementation program derived from `ANC-COMPILER-002` without turning the Temporal Cognitive Graph into a pre-approved product architecture.

Current execution authority is [`program-v1.json`](program-v1.json). Its work-package identifiers are qualified as `OCR-V0:*` when referenced outside this directory.

The current state is:

- **Level A completed** — `OCR-V0:A1` through `OCR-V0:A4` closed the Harness engineering/evidence, release-vector, and staging-rehearsal prerequisites without activating production authority;
- **Level B reached B4** — the Observation Minimum Core, owner exporters, cross-owner Selection, and deterministic Formal Runner/fault cells are complete;
- **`OCR-V0:B5` is provider-blocked** — the frozen DeepSeek Flash/Pro attempts produced zero valid complete Trials under the required Patch contract, so the campaign does not continue with additional DeepSeek canaries;
- **`OCR-V0:B6` is blocked** behind the B5 provider-capability gate and explicit review;
- **Level C is blocked by Level B** and no TCG/graph/Prime/Child-Run implementation is authorized;
- **Level D remains not authorized**.

Product behavior remains owned by Host, Harness, and Runtime. Research status remains owned by [`../../portfolio.json`](../../portfolio.json). Production Harness authority activation is a separate product/operator decision and is not required to preserve these research results.

## Program rule

```text
close current authority and evidence gaps
→ build the strong sequential baseline
→ run a shadow cognitive-state experiment
→ promote only the smallest layer that beats the baseline
```

Run Actor scheduling, Child Runs, Prime/RLM Engine integration, Runtime Workers, Workspace fork/merge, graph databases, and continual Harness activation remain conditional. Production cutover is also separate from research progression: only a clean, remote-reachable version vector and stable owner-native evidence are prerequisites for formal baseline Trials.

## Validation

```bash
python3 -m unittest research/experiments/cognitive-reform-v0/tests/test_program.py
```

## A4 staging rehearsal

A4 proves deployment mechanics without activating production authority. The executable uses only ephemeral children of `/var/lib/ordivon/staging`, installs the exact remote Harness/Host release graph, rehearses backup/verify/restore, proves both safe rollback and post-activation rollback fencing, checks Doctors, and removes the complete staging tree.

```bash
uv run --python 3.12 \
  --with 'ordivon-harness[host] @ git+https://github.com/zycxfyh/ordivon-harness.git@f098f9492ab788068fd09da771bffc21e0fdc1b3' \
  python research/experiments/cognitive-reform-v0/staging_rehearsal.py \
  --output target/acceptance/a4-staging-rehearsal.json
```

The command must never target `/var/lib/ordivon/host` or `/var/lib/ordivon/harness`. Production activation remains a separate operator decision triggered by a real consumer.

### A4 result

The formal staging rehearsal passed on implementation `f6173b2c327c232a70b272cc947dc98bb857ae2a`. It installed remote Harness `f098f9492ab788068fd09da771bffc21e0fdc1b3`, used its exact Host pin `7b17807784cc52f0be4f1786719f6dc20deb92c8`, verified backup and restore, proved both rollback modes, removed the staging tree, and observed no production-root change. The retained receipt is [`evidence/a4-staging-rehearsal-f6173b2.json`](evidence/a4-staging-rehearsal-f6173b2.json).
