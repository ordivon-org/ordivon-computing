# Cognitive Reform Execution Program v0

This directory coordinates the bounded implementation program derived from `ANC-COMPILER-002` without turning the Temporal Cognitive Graph into a pre-approved product architecture.

Current execution has completed **A-Core** and now runs two bounded fronts:

- `A3` — make the exact Host/Harness/Computing/Runtime version vector remote-reachable and clean-install reproducible;
- `B1` — implement only the Observation Minimum Core contract, fixtures, in-process Gateway, and deterministic rebuild.

`A4` is a staging-only deployment rehearsal and remains blocked by `A3`. Production authority activation is not required for Level B.

The machine-readable authority for this execution program is [`program-v1.json`](program-v1.json). Product behavior remains owned by Host, Harness, and Runtime. Research status remains owned by [`../../portfolio.json`](../../portfolio.json).

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
