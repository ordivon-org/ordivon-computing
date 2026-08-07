---
schema_version: 1
id: computing.stack
title: Classical Substrate and Agent-Native Responsibility Overlay
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
updated: 2026-08-03
summary: Canonical architecture boundary between inherited computing mechanisms and responsibilities introduced by persistent Agent participation.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.foundations
  - computing.primitives
---
# Classical Substrate and Agent-Native Responsibility Overlay

## Purpose

Locate Ordivon's irreducible responsibilities without rebuilding operating systems, databases, version control, workflow engines, model runtimes, or other mature substrate.

## Boundaries

Classical systems continue to own physical execution, storage, transport, isolation, and durable mechanics. Ordivon admits a new layer only where participant purpose, open work, commitment, evidence, or consequence would otherwise remain unowned and bypassable.

## Components

The architecture combines the inherited substrate, an Agent-native responsibility overlay, and a hybrid participation boundary that separates reversible exploration from durable consequence.

## Data flow

Participant purpose lowers into persistent work and version-bound context; cognition proposes; capability and consequence are bound; classical systems execute; observations and artifacts return for verification, revision, negotiation, or responsible decision.

## Failure modes

The architecture fails when it duplicates a mature lower owner, treats a proposal as commitment, hides uncertainty, promotes research vocabulary without a consumer, or retains a shared constraint whose friction exceeds its recurring value.

## Verification

Claims move toward Core only through primary-source comparison, executable evidence, cross-project consumers, counterexamples, cost measurement, and deletion tests. Current research state remains owned by the research portfolio rather than this architecture summary.

Ordivon studies the complete computing world but does not treat that world as an implementation roadmap. The current architecture separates the inherited execution substrate from responsibilities that are introduced or materially rewritten when probabilistic cognition participates in persistent work, commitments, and shared worlds.

## 1. Inherited substrate map

| Band | Subject | Authoritative responsibility |
|---|---|---|
| S0 | physical devices and compute primitives | energy, movement, storage, communication, arithmetic, acceleration |
| S1 | machine, operating system, and isolation | ISA, processes, memory, files, namespaces, devices, scheduling, containment |
| S2 | deterministic software and data systems | compilers, language runtimes, databases, version control, networks, protocols, durable workflows |
| S3 | model learning and inference | training, parameters, tokenization, batching, KV state, routing, quantization, serving |

These bands remain active research subjects. Ordivon normally composes their mature implementations rather than reimplementing them.

## 2. Agent-native responsibility overlay

| Responsibility | Subject | Central question |
|---|---|---|
| R0 | participant identity, purpose, and commitments | Who is participating, what do they seek or accept, which resources and consequences bind them, and what counts as completion or exit? |
| R1 | coordination, negotiation, and consequence allocation | Which commitments can proceed locally, which require another participant, verifier, resource owner, institution, or shared-world decision, and what evidence must be presented? |
| R2 | open-work continuity | What Goal, Task frontier, Attempts, waits, commitments, and uncertainty persist across model and process replacement? |
| R3 | context and memory compilation | Which versioned subset of durable state should influence one probabilistic cognitive episode, and what was omitted or invalidated? |
| R4 | cognition, proposal, and coordination | Which model, branch, verifier, Join, stopping rule, Action Proposal, or negotiation should be selected next? |
| R5 | capability, consequence, and Effect compilation | Can this proposal be lowered into an executable Effect against this world version under an applicable capability profile and consequence boundary? |
| R6 | Effect commitment and reconciliation | How does one stable Effect bind to a concrete Dispatch, survive response loss, and reconcile with reality without fabricated completion or blind repetition? |
| R7 | evidence, verification, and epistemic state | What was observed, what is claimed, how was it verified, and what can be accepted as current Fact? |
| R8 | evaluation, learning, and adaptation | Which trajectories improve capability, verification, recovery, distribution, or cooperation, and which constraints or abstractions should be revised or deleted? |

The overlay is a feedback graph, not a strict linear call stack and not a permanent hierarchy in which one intelligence form owns every other one.

## 3. Hybrid participation boundary

```text
participant purpose, commitments, or requests
→ persistent open work
→ version-bound context
→ probabilistic Action Proposal or Claim
→ capability and consequence resolution
→ deterministic Effect commitment
→ classical execution substrate
→ Observation and Artifact evidence
→ Verification and revised work
→ negotiation, responsible decision, refusal, or exit when required
```

The model supplies flexible search over possible next steps and may propose actions not pre-enumerated by the surrounding program. Deterministic state establishes what was proposed, compiled, admitted, dispatched, observed, verified, and accepted.

Current people and organizations usually retain legal and physical control over machines, credentials, money, and public commitments. The overlay must represent those owners exactly while remaining capable of supporting future artificial participants with stable identity, commitments, responsibilities, refusal, and exit if evidence and institutions warrant it.

## 4. Exploration and commitment are different paths

Low-consequence exploration should not inherit the complete friction of irreversible commitment.

```text
reversible / isolated / private
→ broad capability profile
→ parallel exploration
→ candidate Artifact or Claim
→ cheap deletion or rollback

shared / durable / costly / irreversible
→ explicit Effect
→ current world and contract binding
→ responsible participant or institution
→ evidence and recovery plan
```

The distinction is consequence-sensitive, not a simplistic read-versus-write split. A read can violate privacy; a local write in a disposable Workspace can be highly reversible.

## 5. What is not new

The following mechanisms remain classical even when Agents use them:

- processes, Jobs, retries, queues, and controllers;
- database transactions, event logs, and crash recovery;
- Git objects, branches, and content identity;
- containers, VMs, sandboxes, and network policy;
- RPC, MCP, A2A, and Tool schemas;
- compilers, tests, tracing, and metrics;
- model training and inference serving;
- replay of predeclared durable workflows.

Agent scale can amplify their importance. Composition can create a valuable product. Neither fact alone creates a new layer.

## 6. Cross-cutting invariants

1. **Identity** — participants, principals, Goals, Tasks, model invocations, Effects, Dispatches, Artifacts, authorities, commitments, and world objects retain stable identities across replacement.
2. **Version binding** — context, policies, Tools, repositories, models, authorities, and external objects bind to observable revisions.
3. **Explicit uncertainty** — unknown outcome and unsupported Claim remain distinct from failure, success, and Fact.
4. **Provenance** — durable outputs preserve their source, causal relation, and verification path.
5. **Consequence and reversibility** — reversible exploration is distinguished from shared, durable, or irreversible commitment.
6. **Recovery** — current work and Effect history can be reconstructed without relying on model memory.
7. **Negotiability** — commitments and authority can be proposed, delegated, revised, refused, revoked, or ended according to the domain contract.
8. **Non-domination** — current ownership and capability do not silently become unlimited authority over another participant.

## 7. Constraint test

Every durable gate, approval, policy object, compatibility path, schema version, containment mechanism, or shared abstraction must answer:

```text
What unrecoverable loss does it prevent?
What verification, recovery, coordination, or consequence boundary does it add?
What latency, interruption, cognitive compression, maintenance, and control concentration does it impose?
Can a narrower local mechanism provide the same benefit?
Who is the real current consumer?
What is the deletion trigger?
```

The audit begins with the mechanism outside the active path; existence does not count as evidence for retention. Only current consumers, concrete protected failures or capabilities, narrower-alternative analysis, and positive recurring net value rescue it. Otherwise the mechanism is removed, narrowed, archived, or kept outside the active path. Git history supplies recovery for cheap implementation; externally governed data and consequence remain subject to their domain authority.

## 8. Promotion rule

A proposed layer must answer:

```text
Which mature lower mechanism is insufficient?
What exact invariant remains unowned?
What realistic trajectory fails if the layer is bypassed?
Which second workload demonstrates the same responsibility?
Can the mechanism remain a policy or module instead of a new repository?
Does it increase verified improvement or reduce unrecoverable loss after its full cost is counted?
```

Unanswered proposals remain in Research.

## 9. Current derivation path

The compact Agent-first derivation is [`../knowledge/agents/capability-externalization-and-responsibility-placement.md`](../knowledge/agents/capability-externalization-and-responsibility-placement.md), and the executable research method is [`../research/research-method-v1.json`](../research/research-method-v1.json). Complete earlier Computing derivations remain recoverable from Git rather than staying in the active tree. The retained adaptive-acceleration study is a normative position, not an architecture dependency.
