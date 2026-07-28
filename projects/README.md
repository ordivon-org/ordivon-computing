# Projects

This directory maps real projects into the Agent-Native Computing research stack. Each implementation repository remains the source of truth for its code, tests, Issues, releases, runtime state, deployment revision, and current capabilities.

- [`registry.yaml`](registry.yaml) — stable project identities, roles, research branches, focus, and feedback sources;
- [`conformance.toml`](conformance.toml) — stable repository identities, Protocol relationship, and cross-project conformance profiles consumed by the executable base.

Neither file records mutable maturity, phase, deployment health, or a floating “latest revision.” Those facts belong to the implementation repository, live runtime, or an immutable observation captured at a specific time.

The root conformance tool validates that both project lists remain aligned, captures exact local Git revisions, verifies the independent Host's full Computing Protocol pin, and emits digest-bound revision vectors or System Snapshots:

```bash
python3.12 scripts/ordivon_conformance.py manifest
python3.12 scripts/ordivon_conformance.py vector --require-all --require-clean
```

Cross-repository experiments bind exact repository commits, service binaries, Tool-contract digests, and evidence Artifacts through [`../research/evidence/system-snapshot.schema.json`](../research/evidence/system-snapshot.schema.json). A snapshot is historical evidence, not a mutable declaration of current system state.
