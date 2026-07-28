# Projects

This directory maps real projects into the Agent-Native Computing research stack. Each implementation repository remains the source of truth for its code, tests, Issues, releases, runtime state, deployment revision, and current capabilities.

## Truth hierarchy

When sources disagree about an implementation claim, use this order:

1. implementation code plus its tests, and exact-revision runtime or acceptance evidence;
2. contracts maintained in the implementation repository;
3. Issue and pull-request descriptions or discussion;
4. Ordivon Computing summaries, maps, and charters.

Evidence must remain bound to the revision and observation time that produced it. A lower source may summarize a higher source, but it cannot override it; stale Computing prose is corrected from implementation and runtime truth rather than treated as an independent maturity authority.

- [`registry.yaml`](registry.yaml) — stable project identities, roles, research branches, focus, and feedback sources;
- [`conformance.toml`](conformance.toml) — Protocol relationships and cross-project conformance profiles; repository URL and sibling path are derived from each stable project ID.

Neither file records mutable maturity, phase, deployment health, or a floating “latest revision.” In particular, the registry is not a maturity ledger. Those facts belong to the implementation repository, live runtime, or an immutable observation captured at a specific time.

The root conformance tool validates that both project lists remain aligned, captures exact local Git revisions, verifies the independent Host's full Computing Protocol pin, and emits digest-bound revision vectors or System Snapshots:

```bash
python3.12 scripts/ordivon_conformance.py manifest
python3.12 scripts/ordivon_conformance.py vector --require-all --require-clean
```

Cross-repository experiments bind exact repository commits, service binaries, Tool-contract digests, and evidence Artifacts through [`../research/evidence/system-snapshot.schema.json`](../research/evidence/system-snapshot.schema.json). A snapshot is historical evidence, not a mutable declaration of current system state.
