# Testing policy

Tests are protection for explicit semantic invariants, not a mandatory precondition for every edit.

## Source layers

Production-candidate protocol code lives under `packages/ordivon-protocol/`. Executable experiments, fixtures, live evidence scripts, and conformance suites remain under `research/experiments/`. `incubation/host-v0/` now records the closed H2-H6 Host proof and its extraction source; after the history-preserving split, active Host product development belongs in `ordivon-host`.

Experiments import the promoted package directly. They must not retain shadow copies of promoted source.

## T0 — surgical edit loop

Run only the test file or named case that protects the code being changed, plus syntax or lint for the touched paths. This is the default while cutting or moving code.

Examples:

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

## T1 — deterministic component gate

Run the complete deterministic suites after a component reaches a coherent boundary. On the current repository they complete in a few seconds locally, so they remain cheap protection rather than a bottleneck.

```bash
cd packages/ordivon-protocol
PYTHONPATH=src python3.12 -m unittest discover -s tests

cd ../../research/experiments/external-semantic-contract-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:../semantic-core-v0/src:. \
  python3.12 -m unittest discover -s tests

cd ../semantic-core-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:src \
  python3.12 -m unittest discover -s tests

cd ../task-continuation-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:src:../external-semantic-contract-v0:../semantic-core-v0/src \
  python3.12 -m unittest discover -s tests

cd ../../../incubation/host-v0
PYTHONPATH=src:../../packages/ordivon-protocol/src \
  python3.12 -m unittest discover -s tests
```

## T2 — pull-request CI

`.github/workflows/deterministic-contracts.yml` runs only when implementation, Schema, fixture, test, or executable script paths change. It performs static checks, promoted-package tests, all deterministic experiment suites, Host boundary tests, and the Rust canonical-vector verifier.

Documentation-only changes and evidence receipts do not start the workflow.

## T3 — manual evidence

The following are deliberately excluded from ordinary CI:

- real Ordivon live execution;
- process-restart and response-loss injection;
- benchmarks;
- System Snapshot governance checks;
- exact-revision receipt regeneration;
- real Codex or other model continuation evidence;
- repository-wide Markdown audits.

Run them only when the corresponding boundary changes, before release, or during a stage closeout. Their outputs belong in immutable machine receipts, not in mutable status prose.

## Deletion rule

Remove or merge a test only when it duplicates the same observable invariant, protects deleted behavior, or tests an implementation detail with no failure consequence. Do not remove a deterministic test merely because the suite has many cases; duration and diagnostic value decide the cost.
