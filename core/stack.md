---
schema_version: 1
id: computing.stack
title: Classical Substrate, Durable Responsibility Boundaries, and Flexible Cognition
type: architecture
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - builder
  - researcher
  - agent
updated: 2026-08-07
summary: Canonical three-band architecture separating flexible cognition, future-model-robust responsibility boundaries, and mature classical substrate.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.foundations
  - computing.primitives
---
# Classical Substrate, Durable Responsibility Boundaries, and Flexible Cognition

## Purpose

Ordivon Computer does not define a permanent stack of Agent-specific subsystems. It identifies the smallest responsibilities that remain valuable when models, Providers, Context windows, and reasoning quality improve materially, then places each responsibility in the lowest owner that can preserve it.

## Contract

A subsystem name is not an architectural invariant. Host, Harness, Runtime, Observation, Memory, World, Prime, Graph, and similar names remain implementation or research choices unless deleting them leaves an unowned non-bypassable responsibility.

The current machine disposition is [`../research/computer-responsibility-map-v1.json`](../research/computer-responsibility-map-v1.json). This Core page preserves only the compact architecture that survived that review.

## Boundaries

Flexible cognition may propose, search, plan, delegate, or use Provider-native capabilities, but it does not become the owner of external facts or consequences merely by reasoning about them. Mature classical systems keep their mechanical authority. The middle band contains only responsibilities that remain unowned if both sides are composed directly.

## Components

The architecture has exactly three conceptual bands: replaceable cognition/product policy, thin durable responsibility boundaries, and classical substrate. Current repositories are implementations mapped onto those bands rather than permanent architectural layers.

## Data flow

Current work and source bindings compile one cognitive episode; cognition proposes; local adapters may lower semantic intent; the affected owner admits consequence; classical or domain backends execute; owner-native evidence returns; reconciliation and verification advance work state.

## Failure modes

The design fails when an attractive subsystem name becomes a permanent layer without an unowned invariant, when a derived projection becomes fact authority, when transcript or Provider Session becomes work truth, when response loss is guessed instead of reconciled, or when a current model limitation is frozen into shared infrastructure.

## Verification

The responsibility map, Agent-first research method, controlled fault experiments, real provider-replacement trials, cross-owner Observation evidence, product consumers, and deletion tests determine what remains in the middle band. Product state remains owned by product repositories; this Core page cannot promote implementation by itself.

## 1. Flexible cognition and product policy

The upper band contains replaceable intelligence and domain-specific judgment:

```text
participant or domain purpose
+ product policy
+ model / Provider-native Agent capability
+ optional Ordivon Harness or local planner
+ local Skills, search, specialists, and heuristics
```

This band may change rapidly. A stronger Provider may absorb Tool loops, subagents, memory, retrieval, code execution, or planning that today require an external Harness. Ordivon should exploit those capabilities rather than flattening them into a permanent lowest-common-denominator cognition runtime.

Model output remains a proposal. Flexible cognition does not own physical facts, external authority, or durable completion merely because it is capable of reasoning about them.

## 2. Durable responsibility boundaries

Only a small middle band currently survives the future-model test.

| Responsibility | Required invariant | Preferred lowest owner |
|---|---|---|
| Open-work identity and continuity | current semantic work and unresolved operation identity survive model, Provider, process, and Session replacement | work owner or mature durable workflow |
| Current Context binding | one cognitive episode is compiled from current, authorized, revision-valid sources rather than transcript authority | Context/retrieval adapter near the work owner |
| Consequence and authority | reversible private exploration stays cheap while shared, stale, revoked, costly, or irreversible consequence is admitted by the affected owner | resource or domain owner |
| Effect uncertainty and reconciliation | intended Effect and physical attempt remain distinct; `UNKNOWN` is explicit; response loss is reconciled before redispatch | effectful backend, durable workflow, Runtime, or narrow boundary contract |
| Evidence, verification, and completion | proposal, Observation, Artifact, Claim, independent verification, and accepted completion remain distinct where the domain requires it | domain authority and owner-native evidence |
| Tool contract identity and drift | pending work binds to the actual callable contract/revision rather than stale schema state | Tool provider or boundary adapter |
| Owner-native observation projection | Agents can inspect compact cross-owner state without creating a new fact authority | each fact owner plus disposable derived projection |

These are responsibilities, not mandatory repositories or universal schemas. If a database idempotency key, Temporal Activity, provider-native checkpoint, domain API, or other mature mechanism preserves the same invariant with lower recurring cost, Ordivon should use it.

## 3. Classical substrate

The lower band remains classical even when Agents use it intensively.

| Subject | Authoritative responsibility |
|---|---|
| hardware and compute | arithmetic, storage, acceleration, communication, device effects |
| operating system and isolation | processes, memory, files, scheduling, namespaces, devices, containment |
| deterministic software and data systems | databases, transactions, version control, networks, protocols, queues, durable workflows, compilers |
| model learning and serving | training, parameters, tokenization, batching, KV state, routing, quantization, inference serving |
| domain backends | cloud APIs, browsers, applications, exchanges, simulators, sensors, external services |

Agent pressure may motivate better interfaces to these systems. It does not transfer their mechanical authority into an Agent-native layer.

## 4. Current Ordivon packaging

Current repositories map onto the responsibility model, but the mapping is not a permanent hierarchy.

| Current component | Current role | Architectural status |
|---|---|---|
| Ordivon Host | durable Task/work ownership, assignment, semantic completion, consequence admission and foreign-executor binding | responsibility-oriented package root; proven repository read/mutation/code-change workloads are explicit local `engine` modules rather than Host primitives |
| Ordivon Harness | caller-neutral cognitive Run, Provider/Tool loop, durable Run continuity and Runtime bridging | recommended application API is Host-free; Host-backed `HarnessRunner` remains an explicit compatibility path, and Harness itself remains conditional product packaging rather than Core |
| Ordivon Runtime | Workspace/Job/Artifact execution facts, cancellation, recovery, durable request reconciliation | retained without C3 structural change; authoritative execution boundary whose mechanisms remain mostly classical |
| Observation experiment | owner-native run-once export, derived join/inspection and frozen selection | retain inspect/export + disposable projection pattern; no production Plane/daemon or new fact authority admitted |
| `ordivon-protocol` | consumed cross-repository Effect/ToolContract/Binding contracts | retain only contracts with real consumers |

An implementation may merge or split processes and repositories without changing this architecture, provided fact ownership, replacement, recovery, and consequence boundaries remain explicit.

## 5. Working trajectory

```text
purpose or assigned work
→ owner-native current work state
→ current-source Context compilation
→ replaceable cognition proposes
→ semantic intent may be lowered by a local adapter
→ consequence and authority admission
→ stable request / Effect identity
→ classical execution or domain API
→ owner-native Observation / Artifact / receipt
→ reconciliation and independent completion where required
→ current work state advances
```

No step requires a universal Memory database, cognition graph, World bus, or organization runtime.

## 6. What stays outside Core

The following remain product-local or Research until a stronger simpler baseline fails:

- a universal Ordivon Harness or Agent VM;
- a general Memory runtime;
- a universal internal Agent IR;
- a generic World layer beyond direct domain adapters and consumed boundary contracts;
- semantic Action lowering as a universal primitive;
- Prime-style programmable cognition or persistent Run Actor;
- Temporal Cognitive Graph or graph storage;
- generic multi-Agent branch/join infrastructure;
- universal Participant/Commitment organization objects;
- continual self-modification, self-training, or automatic product promotion.

Their absence from Core does not prohibit experiments. It prevents temporary model limitations or attractive abstractions from becoming permanent compatibility obligations.

## 7. Cross-cutting invariants

1. **Ownership** — every authoritative fact has an identifiable owner; derived projections do not silently become truth.
2. **Identity** — work, consequential requests, Artifacts, contracts, and relevant external objects keep stable identities across replacement where recovery requires them.
3. **Version binding** — Context sources, Tools, repositories, policies, authorities, and external objects bind to observable revisions when drift can invalidate work.
4. **Explicit uncertainty** — unknown outcome remains different from failure, success, or completion.
5. **Provenance** — durable evidence preserves enough source and causal binding to audit the claim it supports.
6. **Consequence and reversibility** — cheap private exploration is distinguished from shared, costly, privacy-sensitive, or irreversible commitment.
7. **Recovery** — current work and unresolved external effects can be reconstructed without requiring an old model Session or hidden reasoning state.
8. **Replacement** — models, Providers, Harnesses, adapters, and derived views may be replaced without changing the authoritative meaning of ongoing work.

## 7.1 Core authority boundary

Core is a **compressed prior and navigation surface**, not current-state authority. A direct 2026-08-10 ablation found that the compressed Core used about 48% of the Provider tokens of a larger raw control set, but scored 15/24 versus 18/24 on exact current responsibility decisions. Therefore current owner-native evidence, the canonical research portfolio, exact closeouts, and source revisions override Core whenever they differ. Core should remain small rather than absorb every current detail.

## 8. Admission and deletion test

A proposed durable structure must answer:

```text
What repeated Agent or human-runtime burden was observed?
Who carries the responsibility now?
Which mature lower mechanism is insufficient?
What exact invariant would remain unowned if the candidate is deleted?
Does a stronger and simpler baseline fail?
What permanent state, compatibility, latency, and maintenance cost is added?
Which second workload needs the same invariant?
What deletes or localizes the candidate later?
```

Unanswered proposals remain outside Core. Existing structures receive no presumption of retention from age, implementation effort, documentation volume, or test count.

## 9. Research path

The governing research method is [`../research/research-method-v1.json`](../research/research-method-v1.json). The evidence-backed Computer disposition is [`../research/computer-responsibility-map-v1.json`](../research/computer-responsibility-map-v1.json), with a human projection in [`../research/COMPUTER-RESPONSIBILITY-REVIEW.md`](../research/COMPUTER-RESPONSIBILITY-REVIEW.md).

Reusable reasoning lives in [`../knowledge/agents/capability-externalization-and-responsibility-placement.md`](../knowledge/agents/capability-externalization-and-responsibility-placement.md). Historical derivations remain recoverable from Git rather than occupying the active architecture path.
