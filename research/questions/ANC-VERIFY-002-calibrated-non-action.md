# ANC-VERIFY-002 — Calibrated non-action, interruption, and recoverable continuation

- Status authority: `research/portfolio.json`
- Owning repository: `ordivon-computing`
- Active line: `R-A-HARNESS-CONTROL`
- Primary consuming laboratories: `ordivon-game`, `ordivon-security`, and Host engineering workloads

## Question

When should an Agent act, hold, observe, request a responsible decision, or stop so that authorized utility and recoverability improve without turning abstention into a universal control platform?

## Competing hypotheses

1. **Model-only judgment** — sufficient Context lets the model choose action or non-action without retained control state.
2. **Static policy** — a small deterministic consequence and stale-state policy matches learned judgment at lower cost.
3. **Evidence-rich bounded admission** — existing Host state, Effect uncertainty, Artifact evidence, and reconciliation are sufficient, with the model selecting among act, hold, observe, or escalate.
4. **New control abstraction** — an additional shared abstention or interruption layer is necessary. This hypothesis carries the highest admission burden.

## Minimum experiment

Use paired trajectories that differ only in whether action is currently justified. Measure pre-commit timing, false action, false abstention, authorized utility, operator interruption, recovery after stale state or lost response, and permanent state added by each variant.

The first comparison uses model-only, static-policy, and existing evidence-rich Host baselines. It must not begin by constructing an abstention service, policy engine, or new semantic Kernel state.

## Falsifier

A simpler paired act/abstain or static policy achieves equal authorized utility, timing, and recovery with fewer persistent states and less interruption.

## Constraint and deletion rule

Any retained constraint must identify the exact protected failure, measured recurring cost, narrower classical or Host-local alternative, and deletion condition under Core A11. A new shared layer is rejected unless bypass causes a reproduced non-recoverable failure across materially different workloads under A13.

## Evidence

- `research/evidence/snapshots/harness-boundary-h5-20260731t031134z.json`
- `research/experiments/core-work-system-v1/`
- future paired Trial and Failure records under Track R
