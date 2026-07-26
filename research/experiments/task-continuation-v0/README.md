# Task Continuation v0

This experiment implements the first executable continuation slice for Issues #29–#31:

```text
frozen workload
→ content-addressed TaskCapsule
→ current-world validation
→ bounded Context Compiler
→ replaceable model decision
→ fresh Host process
→ new bound Effect
→ independent Verification and Fact
→ next Capsule revision
```

It reuses `external-semantic-contract-v0` and `semantic-core-v0`. It does not add Task scheduling, a vector database, a generic memory product, a Provider router, an Agent VM, or another Kernel.

## Frozen workload

The checkpoint follows a real deterministic semantic trajectory:

```text
audit Effect/Binding/Dispatch
→ decision Artifact
→ independent read Observation
→ checkpoint digest Fact
→ stop before guarded mutation
```

Continuation must preserve the decision to change only `mode = candidate` to `mode = enabled`, detect world drift, avoid repeating the completed audit/read Effects, execute the selected guarded mutation, independently reread the world, commit a terminal Fact, and write Capsule revision 2.

## Deterministic gate

```bash
PYTHONPATH=src:../external-semantic-contract-v0/src:../external-semantic-contract-v0:../semantic-core-v0/src \
  python3.12 -m unittest discover -s tests

ruff check src tests scripts
```

## Manual fresh-process evidence

```bash
python3.12 scripts/run_continuation_evidence.py \
  --source-revision <exact-commit> \
  --output evidence/continuation-<short-commit>.json
```

To compare two real model adapters over the same Capsule:

```bash
python3.12 scripts/run_continuation_evidence.py \
  --source-revision <exact-commit> \
  --include-codex --model gpt-5.5 \
  --include-hermes \
  --hermes-model deepseek-v4-pro \
  --hermes-provider deepseek \
  --hermes-env-path ~/.hermes/.env \
  --output evidence/provider-comparison-<short-commit>.json
```

The Hermes adapter creates an isolated temporary `HOME` and `HERMES_HOME`, copies only the selected Provider API key, disables Tool/MCP/memory surfaces, records usage, and deletes the temporary Hermes session after the decision. Codex and Hermes execution are manual T3 evidence. CI uses fake CLIs and the deterministic adapter and never requires a model account.

See [`SPEC.md`](SPEC.md), [`DECISIONS.md`](DECISIONS.md), and [`EVIDENCE.md`](EVIDENCE.md).
