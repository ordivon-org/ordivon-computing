# Projects

This directory maps real projects into the Agent-Native Computing research stack. Each implementation repository remains the source of truth for its code, tests, Issues, releases, runtime state, deployment revision, and current capabilities.

- [`registry.yaml`](registry.yaml) — stable project identities, roles, research branches, focus, and feedback sources.

The registry deliberately excludes dynamic labels such as current maturity, active phase, deployment health, or latest revision. Those facts belong to the implementation repository, live runtime, or an immutable experiment snapshot captured at a specific time.

Cross-repository experiments record exact repository commits, service binaries, Tool-contract digests, and evidence Artifacts through [`../research/evidence/system-snapshot.schema.json`](../research/evidence/system-snapshot.schema.json). A snapshot is historical evidence, not a mutable declaration of current system state.
