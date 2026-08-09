---
schema_version: 1
id: computing.authority
title: Computing Content Authority
type: decision
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-04
summary: Decision identifying the narrow set of documents and machine records allowed to define current shared Ordivon meaning.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-project-family
related:
  - computing.start
  - computing.research.start
---
# Computing Content Authority

## Context

The repository contains current theory, generated views, experiments, studies, audits, and historical phase records. File recency, size, or confident language cannot determine authority.

## Decision

The current canonical human-readable entry is [`../README.md`](../README.md). Shared purpose and model are defined by [`../core/intent.md`](../core/intent.md), [`../core/foundations.md`](../core/foundations.md), [`../core/stack.md`](../core/stack.md), and [`../core/primitives.md`](../core/primitives.md).

Research navigation is defined by [`../research/README.md`](../research/README.md). The shared world-model revision method is owned by `research/world-model-loop-v1.json`, while `research/world-model-frontier.json` owns only Computing's current project-assimilation state and never product maturity. Mutable research status is owned only by `research/portfolio.json`; `research/PORTFOLIO.md` is its generated projection. Stable project identity is owned by `projects/registry.yaml`. Cross-project ownership and project admission, extraction, merge, or retirement rationale is owned by [`../projects/decisions/README.md`](../projects/decisions/README.md) and its linked records; a record under review does not register a project. Promoted machine contracts and canonical vectors own cross-project protocol compatibility. [`content-engineering/README.md`](content-engineering/README.md) owns the shared document contract, maintenance rules, and concentrated-governance restart conditions.

Studies, experiments, audits, closeouts, baselines, and phase-named files are evidence, derivation, or history unless a canonical document explicitly incorporates their result. Ordivon Web publications are derived interpretations and cannot redefine these records.

Authority precedence is explicit: named canonical documents and machine registries override generated projections; generated projections override no source; historical documents remain scoped to their recorded revision. Words such as `current`, `active`, `next`, or `roadmap` inside a historical file do not reactivate it. Only `research/portfolio.json` may do that for research status.

## Consequences

Only the paths named above enter strict content management in this adoption step. Other documents remain discoverable and advisory; they are not bulk-rewritten or granted authority by default. A new canonical path must declare what it replaces and update this decision or the relevant machine registry.

## Status

Accepted and active. Reopen when a named source is removed, split, generated from a stronger owner, or shown to create conflicting current truth.
