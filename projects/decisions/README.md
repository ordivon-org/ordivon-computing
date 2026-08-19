---
schema_version: 1
id: computing.projects.decisions
title: Project-family Decision Records
type: start
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-07
summary: Canonical index and review procedure for cross-project ownership, admission, extraction, merge, retirement, and infrastructure-promotion decisions.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.authority
  - computing.projects.production-support
---
# Project-family Decision Records

## Purpose

This directory preserves the rationale for decisions that change responsibility across Ordivon repositories: project admission, extraction, merge, retirement, and ownership boundaries that cannot be decided correctly inside one implementation repository alone.

A decision record answers:

```text
what pressure was observed
→ which owners and alternatives were considered
→ what evidence was available
→ what was decided or left under review
→ what consequences and follow-up work result
→ what evidence would reopen or supersede the decision
```

## Start here

Read [`agent-first-infrastructure-promotion.md`](agent-first-infrastructure-promotion.md) for the default rule that mature infrastructure and thin Agent-facing adaptations precede any new Ordivon abstraction or repository. Read [`host-harness-independent-persistence-and-observation.md`](host-harness-independent-persistence-and-observation.md) for the accepted Host/Harness authority and automatic-observation boundary. [`product-and-production-support-boundary.md`](product-and-production-support-boundary.md) is preserved as the historical production-support / `ordivon-studio` admission review; it is not current Media owner authority. Use the rules below before adding another cross-project packaging decision.

## Current boundary

These records own cross-project decision rationale. They do not own implementation facts, product maturity, deployment state, or changing task progress.

- [`../registry.yaml`](../registry.yaml) is only Computing's bounded project-family packaging/compatibility roster; it is non-exhaustive and is not current semantic-owner identity/currentness authority.
- An implementation repository remains authoritative for its code, interfaces, tests, releases, and runtime state.
- GitHub Issues own changing work, dependencies, and execution status.
- A decision with `lifecycle: review` does not authorize a repository extraction or register a new project.

## Record rules

1. Connect a new record from this index and from the project-family map when it affects current navigation.
2. Use `review` while alternatives or admission evidence remain unresolved; use `accepted` only after the exact boundary and consequences are agreed.
3. Do not silently rewrite a materially changed rationale. Append review evidence, or create a superseding record and link it through metadata.
4. An accepted Computing packaging admission, merge, extraction, or retirement decision must update `projects/registry.yaml` and [`../README.md`](../README.md) when that packaging/navigation roster actually changes. A semantic owner admission, rename, or authority transition does **not** require a new Computing registry row unless a concrete Computing consumer needs that packaging identity; owner-native authority remains primary.
5. A rejected candidate remains as an archived record when its reasoning is likely to recur.
6. Record evidence and triggers, not meeting transcripts or exhaustive chronology.

## Current records

| Record | Lifecycle | Current result |
| --- | --- | --- |
| [`agent-first-infrastructure-promotion.md`](agent-first-infrastructure-promotion.md) | accepted | Agents first inherit mature mechanisms, then add only thin local Agent-facing adaptations; a new Ordivon abstraction or repository requires repeated evidence for an independent durable semantic responsibility. |
| [`host-harness-independent-persistence-and-observation.md`](host-harness-independent-persistence-and-observation.md) | accepted | Host and Harness become independently durable; committed owner events feed a non-authoritative automatic observation plane before formal repeated Trials. |
| [`media-owner-and-studio-packaging-transition.md`](media-owner-and-studio-packaging-transition.md) | accepted | Current Computing packaging/navigation follows Ordivon Media; Studio remains a Media-local capability and historical identity without transferring old world-model standing. |
| [`product-and-production-support-boundary.md`](product-and-production-support-boundary.md) | historical review | Historical Studio production-support admission reasoning is preserved; current semantic owner/navigation is Ordivon Media and must be resolved from Media authority rather than this review. |

## Reopen conditions

Revisit this procedure if decisions are repeatedly made outside the index, records duplicate mutable issue state, the registry can no longer express stable identity independently, or review records create more maintenance cost than they prevent.
