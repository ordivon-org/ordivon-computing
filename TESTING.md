# Testing policy

Tests protect explicit semantic invariants; they are not a mandatory precondition for every edit.

## Source layers

Production-candidate protocol code, normative Schemas, and canonical vectors live under `packages/ordivon-protocol/`. Executable experiments, workload fixtures, live evidence scripts, and conformance suites remain under `research/experiments/`. The closed H2-H6 Host incubator remains recoverable from Git history and the independent `ordivon-host` repository; Computing no longer tests or carries a second Host product tree.

Experiments import the promoted package directly. They must not retain shadow copies of promoted source.

## T0 — surgical edit loop

Run only the test file or named case that protects the touched boundary, plus syntax or lint for the changed paths.

```bash
cd packages/ordivon-protocol
PYTHONPATH=src python3.12 -m unittest tests.test_promoted_boundaries

cd research/experiments/semantic-core-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:src \
  python3.12 tests/test_binding_edge.py

cd ../external-semantic-contract-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:../semantic-core-v0/src:. \
  python3.12 tests/test_binding_authority.py
```

## T1 — complete deterministic gate

The repository root owns the canonical gate. It validates the project and Protocol manifest, performs static checks, runs every deterministic Protocol, semantic, continuation, evidence, and conformance suite, and verifies the Rust canonical vectors.

```bash
python3.12 scripts/ordivon_conformance.py gate \
  --receipt /tmp/ordivon-conformance-receipt.json
```

The command deliberately uses the active Python interpreter and installed `ruff` and `rustc`; CI fixes these to Python 3.12, Ruff 0.15.14, and the stable Rust toolchain. Task-continuation subprocess fixtures receive an explicit `/tmp` boundary so Runtime-specific temporary directories do not change their isolation semantics.

Component commands remain available for T0 debugging, but they are no longer duplicated as a manually maintained repository-wide checklist.

## T2 — pull-request CI

`.github/workflows/deterministic-contracts.yml` invokes the same root gate when implementation, Protocol, conformance, Schema, fixture, test, or executable-script paths change. Documentation-only changes and immutable evidence receipts outside executable evidence paths do not need a second testing policy.

## T3 — cross-repository evidence

Revision-vector and System Snapshot capture are deterministic tools, but deciding which exact repositories, services, deployments, and live evidence belong to an experiment remains a manual research decision.

```bash
python3.12 scripts/ordivon_conformance.py vector \
  --require-all --require-clean \
  --output /tmp/ordivon-revision-vector.json

python3.12 scripts/ordivon_conformance.py snapshot \
  --require-all \
  --snapshot-id ordivon-system-<timestamp> \
  --purpose "<bounded experiment or closeout>" \
  --output research/evidence/snapshots/<snapshot>.json
```

Real Runtime execution, process restart, response-loss injection, benchmarks, service-binary binding, model-provider evidence, and deployment observations remain explicit T3 work. Their outputs belong in immutable machine receipts rather than mutable status prose.

## Deletion rule

Remove or merge a test only when it duplicates the same observable invariant, protects deleted behavior, or tests an implementation detail with no failure consequence. Test count alone is not a cost signal; duration and diagnostic value decide the cost.
