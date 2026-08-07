---
schema_version: 1
id: computing.projects.agent-first-infrastructure-promotion
title: Agent-first Infrastructure Promotion Rule
type: decision
profile: engineering
lifecycle: accepted
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-07
summary: Mature host capabilities and thin Agent-facing adapters are the default; Ordivon owns a new durable abstraction or repository only after repeated evidence proves a distinct semantic responsibility.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.projects.decisions
  - computing.projects.host-harness-observation
---
# Agent-first Infrastructure Promotion Rule

## Decision

Cross-cutting infrastructure follows a three-layer promotion rule:

```text
missing capability
→ mature host / OSS capability exists?
  → yes: Agent discovers and uses it directly
  → no or repeated use remains mechanically unsafe:
      add the smallest Agent-facing adapter, manifest, schema, or projection
      → repeated real workloads still expose an unowned durable semantic responsibility?
          → yes: propose an Ordivon-owned abstraction
          → only after extraction evidence: consider an independent repository
```

The first two layers are normal Agent work. They do not require a new Ordivon project decision merely because the capability is useful across repositories.

## Layer 1 — inherit mature mechanisms

Agents should prefer mature tools and classical infrastructure when they already own the operation semantics well enough. Examples include Git, SQLite, DuckDB, Parquet, OpenTelemetry, KVM, FFmpeg, rsync, rclone, restic, hyperfine, jq, ripgrep, and provider-native APIs.

The default action is to discover the live executable or endpoint, inspect the relevant version or capability when needed, and use it through the existing Runtime or domain boundary. Do not create an Ordivon wrapper merely to rename a command or hide ordinary arguments.

## Layer 2 — add only Agent-facing friction reduction

When direct use repeatedly creates avoidable mechanical work, the Agent may add the smallest local layer that makes the mature mechanism machine-friendly. Suitable forms include:

- capability inventory or discovery metadata;
- exact System or Environment Manifest projection;
- narrow adapter around unsafe or ambiguous invocation semantics;
- schema, query projection, or immutable reference form;
- bounded exporter or importer;
- local policy or capability grant;
- deterministic conversion between an owner-native format and a shared observation format.

This layer should remain colocated with the current owner or in Computing research while its semantics are still being discovered. It must not become a new authority merely because several callers can technically reuse it.

## Layer 3 — Ordivon-owned semantic responsibility

A new durable Ordivon abstraction is justified only when real workloads demonstrate a responsibility that mature infrastructure plus thin adapters do not own. The evidence should show most of the following:

1. at least two materially different consumers encounter the same failure class;
2. deleting the proposed abstraction would predictably recreate a material correctness, continuity, evidence, authority, recovery, or lineage failure;
3. the responsibility has a stable identity and lifecycle independent of one current implementation;
4. owner boundaries cannot express the responsibility cleanly by references or projections alone;
5. the abstraction reduces total system complexity rather than centralizing convenient but unrelated functions;
6. recovery, migration, deletion, and authority consequences can be stated explicitly;
7. a stronger future Agent would still need the responsibility rather than merely a more convenient interface.

Useful cross-project code is not sufficient evidence. Repeated semantic responsibility is the threshold.

## Independent-repository gate

Even when Layer 3 is earned, an independent repository is a second decision. Extraction should be proposed only when independent versioning, release, persistence, deployment, security boundary, or materially different consumers make repository independence cheaper than continued colocation.

Until that threshold is met:

- keep experimental shared contracts in the owning repository or `ordivon-computing`;
- keep thin adapters beside their truth owner;
- reuse mature external infrastructure directly;
- do not create `ordivon-*` projects for capability collection, naming symmetry, or architectural completeness.

When the threshold appears to be met, the Agent should present the evidence, proposed responsibility, alternatives, and extraction cost for human review before creating or admitting the independent Ordivon repository.

## Current application

The next cross-cutting audit will examine the existing A0 candidates without assuming they deserve new projects:

- Observation Plane;
- System / Environment Manifest;
- Usage / Cost Accounting.

The audit should first ask what can remain inherited infrastructure or owner-local Agent-facing projection. It should recommend Ordivon ownership only where a durable semantic responsibility has already emerged from real Host, Harness, Runtime, Finance, Security, or other domain work.

## Reopen conditions

Revisit this rule if mature tools repeatedly prevent Agent autonomy despite thin adapters, cross-project local adapters create incompatible semantic copies, a shared responsibility repeatedly causes correctness or recovery failures, or independent deployment/versioning becomes materially cheaper than colocation.
