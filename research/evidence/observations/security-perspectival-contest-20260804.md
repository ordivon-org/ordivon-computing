# Ordivon Security observation — perspectival Contest state — 2026-08-04

This is a bounded cross-project observation. Implementation authority remains in `ordivon-security`; Ordivon Computing consumes only the research implication.

## Owner binding

- repository: `https://github.com/zycxfyh/ordivon-security`
- revision: `334c4e7f69b2d3ff353580043229c259e79e77b9`
- product version: `0.2.0`
- relevant migration: `docs/MIGRATION-ROUND-2.md`
- observed capability: deterministic multi-Actor Contest plus pinned CAGE Challenge 4 Range

## Observed structure

The active Contest separates:

```text
Scenario identity
→ Actor-specific Observation
→ one ActionProposal per Actor
→ explicit admission
→ joint Range resolution
→ Actor result
→ sensor telemetry
→ independent world-truth snapshot
→ raw metrics and sealed evidence
```

In the CAGE Range:

- one Security Red Actor controls the CAGE Red team;
- one Security Blue Actor controls five CAGE Blue agents;
- Green agents remain native environmental actors;
- every Red and Blue CAGE action is explicitly submitted by Ordivon;
- Actor, management, sensor, and truth evidence are recorded separately;
- local source path is excluded from semantic Trial identity;
- exact CAGE revision and policy configuration are bound;
- action attempts are recorded as `resolved`, not falsely asserted as successful effects.

## Computing observation

The same world transition can support different participant conclusions because the participants do not receive the same view.

```text
CAGE management state
≠ Red observation
≠ Blue observation
≠ sensor event
≠ evaluator evidence
```

This difference is causal rather than merely presentational: changing which evidence an Actor receives can change its next proposal even when the underlying world is unchanged.

The observation also exposes several distinct causes of divergent conclusions:

1. **informational divergence** — Red and Blue receive different observations;
2. **interpretive divergence** — one signal can support natural-fault and adversarial explanations;
3. **commitment divergence** — Red and Blue pursue opposing objectives;
4. **strategic divergence** — one side may act to alter the other side's evidence or expectations.

These are not all captured by one generic Context or disagreement field.

## What this evidence proves

- one external simulation can support actor-specific bounded views;
- those views can be preserved separately from management truth and sensor telemetry;
- a Contest can collect simultaneous proposals without exposing one Actor's proposal to another;
- evidence can reconstruct which view preceded which action;
- shared world identity does not imply shared epistemic state.

## What this evidence does not prove

- the Actors are model-backed or strategically intelligent;
- explicit belief records improve objective performance;
- a shared `PerspectiveState` object is required;
- the four evidence channels are physically independent producers;
- CAGE ground truth generalizes to open physical or social worlds;
- non-adversarial participants need the same structure;
- different judgments remain after evidence and objectives are equalized.

Current CAGE Actors only select `native-policy` or `sleep`; the pinned native policy still selects concrete parameterized actions.

## Retained implication

Computing should investigate whether perspective is best represented by composition:

```text
participant or role
+ ContextSelection and omissions
+ Observation / Artifact references
+ commitments and Authority
+ Claims or hypotheses
+ time and uncertainty
```

rather than by a new state store.

## Required second evidence

Before Core or Protocol promotion, reproduce a materially similar responsibility in one non-adversarial workload:

- Game: two factions, player/Agent roles, or persistent actors receive different views or attach different value to shared facts; or
- Host: two participants share a Task but own different commitments, consequences, or verification authority.

The second workload must show that forced consensus or a universal Context loses capability, attribution, or responsibility compared with preserving bounded perspectives.

## Disposition

```text
new research question: ANC-EPISTEMIC-001
portfolio status: deferred M1
Ready Frontier effect: none
shared primitive admitted: none
first deletion test: existing Observation, Claim, Verification, Fact, ContextSelection, and domain-local Actor state are sufficient
```
