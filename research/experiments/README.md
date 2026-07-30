# Research Experiments

Experiments connect open Agent-Native Computing questions to executable artifacts and observable results. They are not production components by default.

## Active experiments

- [`core-work-system-v1/`](core-work-system-v1/) — Round 1 strong-baseline comparison across open-work continuity, Context invalidation, Effect ambiguity, operator attention, and live Codex/Hermes Provider replacement. Its [full report](core-work-system-v1/REPORT.md) documents the principles, implementation, complete data, engineering problems, limitations, and the localization or reduction of every shared-layer claim except bounded Provider-neutral state.
- [`task-continuation-v0/`](task-continuation-v0/) — frozen continuation workload, content-addressed TaskCapsule, field ablations, bounded Context Compiler, and fresh-process Host continuation.
- [`external-semantic-contract-v0/`](external-semantic-contract-v0/) — backend-neutral canonical encoding, public Effect IR, ToolContract normalization and diff, immutable Effect Binding, the minimal signed Kernel admission edge, dual-backend integration, and exact evidence.

## Closed reference experiments

- [`semantic-core-v0/`](semantic-core-v0/) — completed Agent Semantic Kernel v0 reference experiment. It established K1–K11, durable replay, role-scoped Authority, incremental command cost, Ordivon recovery, and structurally distinct second-backend portability. It now accepts only bug fixes, regression evidence, and genuinely universal Kernel invariants.

## Planned experiment families

- dynamic Task dataflow and Agent VM control;
- multi-Workspace branch and Artifact join;
- second-backend Effect comparison through Edge Fetch/Browser.

Each experiment should record:

```text
question
→ hypothesis
→ smallest constructed artifact
→ workload
→ observations
→ interpretation or falsification
→ next revision
```

Failed hypotheses remain useful when they preserve the exact boundary exposed by reality.
