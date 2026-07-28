# Testing policy

Tests protect explicit semantic and foundational invariants; they are not a mandatory precondition for every edit.

## Source layers

Production-candidate protocol code, normative Schemas, and canonical vectors live under `packages/ordivon-protocol/`. Executable experiments, fixtures, live evidence scripts, and conformance suites remain under `research/experiments/`. The independent `ordivon-host` repository owns product Host code; Computing does not carry a shadow Host tree.

Core, Knowledge, the classical-to-Agent transition Study, research map, and source ledger form a foundational architecture contract. They are checked mechanically for required files, relative links, reference identifiers, substrate/overlay structure, and obsolete layer terminology.

## T0 — surgical edit loop

Run the narrow checker or test that protects the touched boundary.

For foundational documents:

```bash
python3.12 scripts/check_foundational_docs.py
python3.12 -m unittest research.evidence.tests.test_foundational_docs
```

For protocol and experiments:

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

The repository root owns the canonical gate. It validates foundational documents, project and Protocol manifests, performs static checks, runs every deterministic Protocol, semantic, continuation, evidence, and conformance suite, and verifies the Rust canonical vectors.

```bash
python3.12 scripts/ordivon_conformance.py gate \
  --receipt /tmp/ordivon-conformance-receipt.json
```

The command uses the active Python interpreter and installed `ruff` and `rustc`; CI fixes these to Python 3.12, Ruff 0.15.14, and the stable Rust toolchain. Task-continuation subprocess fixtures receive an explicit `/tmp` boundary so Runtime-specific temporary directories do not change their isolation semantics.

## T2 — pull-request CI

`.github/workflows/deterministic-contracts.yml` invokes the same root gate when executable contracts or foundational architecture paths change. This includes root/Core/Knowledge/Studies, the research map and questions, evidence, Protocol, conformance, Schemas, fixtures, tests, and executable scripts.

Ordinary historical notes outside those paths may remain documentation-only. A document promoted into the foundational set inherits deterministic link and source-reference checks.

## T3 — cross-repository evidence

Revision-vector and System Snapshot capture are deterministic tools, but deciding which exact repositories, services, deployments, and live evidence belong to an experiment remains a bounded research decision.

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

Real Runtime execution, process restart, response-loss injection, benchmarks, service-binary binding, model-provider evidence, deployment observations, and sustained-workload measurements remain explicit T3 work. Their outputs belong in immutable machine receipts rather than mutable status prose.

## Deletion rule

Remove or merge a test only when it duplicates the same observable invariant, protects deleted behavior, or tests an implementation detail with no failure consequence. Remove a Core statement when deleting it creates no specific failure, a mature lower layer already owns the invariant, or the statement freezes a temporary model limitation.

Test count and document length are not value signals. Diagnostic power, falsifiability, execution cost, and downstream leverage decide the cost.
