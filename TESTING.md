# Testing policy

Tests are protection for explicit semantic invariants, not a mandatory precondition for every edit.

## T0 — surgical edit loop

Run only the test file or named case that protects the code being changed, plus syntax or lint for the touched paths. This is the default while cutting or moving code.

Examples:

```bash
PYTHONPATH=research/experiments/semantic-core-v0/src \
  python3.12 research/experiments/semantic-core-v0/tests/test_binding_edge.py

cd research/experiments/external-semantic-contract-v0
PYTHONPATH=src:../semantic-core-v0/src:. \
  python3.12 tests/test_binding_authority.py
```

## T1 — deterministic component gate

Run the complete deterministic suites after a component reaches a coherent boundary. On the current repository they complete in a few seconds locally, so they remain cheap protection rather than a bottleneck.

```bash
cd research/experiments/external-semantic-contract-v0
PYTHONPATH=src:../semantic-core-v0/src:. python3.12 -m unittest discover -s tests

cd ../semantic-core-v0
PYTHONPATH=src python3.12 -m unittest discover -s tests
```

## T2 — pull-request CI

`.github/workflows/deterministic-contracts.yml` runs only when implementation, Schema, fixture, test, or executable script paths change. It performs static checks, both deterministic suites, and the Rust canonical-vector verifier.

Documentation-only changes and evidence receipts do not start the workflow.

## T3 — manual evidence

The following are deliberately excluded from ordinary CI:

- real Ordivon live execution;
- process-restart and response-loss injection;
- benchmarks;
- System Snapshot governance checks;
- exact-revision receipt regeneration;
- repository-wide Markdown audits.

Run them only when the corresponding boundary changes, before release, or during a stage closeout. Their outputs belong in immutable machine receipts, not in mutable status prose.

## Deletion rule

Remove or merge a test only when it duplicates the same observable invariant, protects deleted behavior, or tests an implementation detail with no failure consequence. Do not remove a deterministic test merely because the suite has many cases; duration and diagnostic value decide the cost.
