---
schema_version: 1
id: computing.primitives
title: Minimal Shared Vocabulary and Responsibility Boundaries
type: reference
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
updated: 2026-08-16
summary: Minimal shared vocabulary for future-model-robust work, consequence, Effect, evidence, Tool-drift, and observation responsibilities.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.stack
  - computing.foundations
---
# Minimal Shared Vocabulary and Responsibility Boundaries

## Scope

Core vocabulary exists to distinguish responsibilities that cannot safely collapse into one model Context or one backend call. It is not an ontology of everything an Agent system may contain.

Production compatibility remains defined by versioned protocol artifacts and product repositories. Research and experiment-local objects do not become Core primitives merely because Ordivon once implemented them.

## Contract

A shared term exists only to preserve a durable responsibility boundary. The exact storage object, schema, API, Provider representation, or repository is replaceable unless a real consumer depends on that representation.

Identity follows the owner-named invariants that make an object, commitment, or observation the same thing for the responsibility being protected. Label, byte, ticker/name, or implementation-revision equality alone is neither necessary nor sufficient. No universal identity tuple follows; each owner names the invariants whose change would alter meaning, authority, replay, or continuity.

## Errors

Invalid interpretations include treating product-local vocabulary as universal protocol, treating an experiment object as Core because it was implemented, treating model confidence as owner-native evidence, treating a projection as authority, or treating a stronger interface abstraction as proof that a new shared layer is required.

## Compatibility

Current cross-project compatibility is defined only by consumed versioned contracts such as those in [`../packages/ordivon-protocol/`](../packages/ordivon-protocol/), plus each product repository's own state and tests. This vocabulary can shrink without breaking compatibility when no current consumer requires the removed term.

## Admission rule

A shared term survives here only when it clarifies one of the durable boundaries in [`stack.md`](stack.md), has a current consumer or failure consequence, and cannot be replaced by a lower classical mechanism or local adapter without losing that distinction.

## 1. Inherited classical objects

These remain important but are not Agent-native primitives.

### Workspace, process, and Job

A Workspace is an operational address space. A process is an operating-system execution object. A Job is a backend-owned durable execution/control object. They can implement work without owning the semantic purpose of that work.

### Transaction and durable workflow

Databases own atomic state changes. Durable workflow systems own replay and continuation of declared workflow logic. Ordivon should reuse those mechanics whenever they preserve the required invariant.

### Tool

A Tool is an executable interface. Tool availability or credentials establish possible reach, not semantic permission to create every consequence the Tool can produce.

## 2. Work identity and Context binding

### Goal or purpose

A Goal or equivalent domain purpose expresses why work exists and what outcome matters. It may be represented differently by each product or domain; no universal Goal schema is required by Core.

### Task or work identity

A Task is the current Ordivon Host representation of durable semantic work. The lasting primitive is the **work identity and unresolved state**, not the specific Task database schema. Work may outlive model calls, Provider Sessions, Harness Runs, processes, Jobs, and failed attempts.

### Context

Context is the bounded selected view supplied to one cognitive episode. It is not an authoritative store. The durable requirement is **Context binding** to current sources, revisions, capability/authority state, and relevant work state when drift can change the correct action.

Transcript, provider memory, vector retrieval, summary, cache, and Working Set are replaceable ways to help compile Context.

## 3. Consequence and authority

### Authority or grant

Authority is a scoped external relation describing who or what may commit a consequence against a resource or domain. Credentials may implement reach but do not automatically establish semantic authority.

### Consequence boundary

The consequence boundary separates low-cost reversible exploration from shared, privacy-sensitive, costly, revoked, stale, or irreversible commitment. The exact policy object is domain-specific unless multiple consumers prove a shared contract.

Human approval is not a primitive. The responsible owner may be a person, service, organization, domain authority, or another participant according to the actual resource and consequence.

## 4. Effect and Dispatch

### Effect

An Effect is the stable intended external observation or change when that identity must survive recovery, rebinding, or response loss. It preserves selected intent; it does not make execution idempotent.

### Dispatch or request attempt

A Dispatch is one physical attempt to realize an Effect through a concrete Tool or backend. Some backends already provide the necessary request identity, Activity identity, transaction key, or audit record. In those cases Ordivon should bind to the existing identity rather than reproduce the mechanism.

```text
selected semantic intent
→ stable Effect / request identity
→ one or more observable physical attempts
→ UNKNOWN when acknowledgement is lost
→ reconcile original identity before redispatch
```

The durable primitive is the distinction between intended Effect and physical attempt plus explicit uncertainty and reconciliation.

## 5. Tool contract and Binding

### ToolContract

A ToolContract identifies the callable interface revision needed to detect material drift for pending work. Discovery and caching may be local; Core does not require a global Tool registry.

### Binding

A Binding ties selected Effect semantics to the exact Tool contract/request representation used for execution where replay, comparison, or drift recovery requires that relation.

`ordivon-protocol` currently carries consumed Effect/ToolContract/Binding schemas. Only real cross-repository consumers justify their continued shared compatibility.

## 6. Observation, Artifact, verification, and completion

### Observation

An Observation is an owner-native recorded reading or result about external or execution state. The producing owner remains authoritative for what was actually observed.

### Artifact

An Artifact is a durable content-bearing output with identity and provenance sufficient for its consumer: patch, dataset, report, binary, log, result, or other retained output.

### Claim and verification

A Claim is an assertion that may require evidence. Verification is an independently declared method/decision that evaluates evidence when a domain needs stronger acceptance than model confidence or process exit.

A separate universal `Fact` object is not required by Core. Domains may promote verified Claims to their own accepted state.

### Completion

Completion is owned by the work/domain authority under declared criteria. Runtime success, Tool success, model self-report, or Artifact existence alone does not universally imply semantic completion.

## 7. Owner-native projection

An inspect/export/query surface may project Host, Harness, Runtime, Tool, or domain state for an Agent. The projection is derived and replaceable.

```text
owner-native facts
→ bounded projection / selection
→ Agent inspection or research view
```

A projection does not become a second owner merely because it joins several sources.

## 8. Product-local vocabulary

The following names can be useful in products without becoming shared Core objects:

- Task Attempt, Assignment, lease, wait, budget, completion candidate;
- ActionProposal or semantic Action request;
- CapabilityProfile;
- DecisionRequest;
- ParticipantRef and Commitment;
- local Branch, Join, checkpoint, plan, scratchpad, summary, or Working Set;
- provider-native Session, subagent, memory, Tool search, or code-execution object.

Products should use the smallest representation that serves their actual consumer. Promote a cross-project schema only after multiple materially different consumers need the same invariant.

## 9. Experiment-local and conditional vocabulary

The closed Semantic Core experiment used `WorldObjectRef`, `EffectEvent`, `Fact`, `Attestation`, and `Semantic Journal` to test identity, evidence, replay, and authority. Those objects remain valid historical evidence but are not permanent Core commitments unless a current consumer rescues them.

The following remain Research candidates rather than Core primitives:

- general Memory runtime;
- universal Agent IR or bytecode;
- generic World layer;
- semantic Action lowering as a universal primitive;
- Prime-style programmable cognition or persistent Run Actor;
- RunFrame or typed Working Set beyond the minimum current work state;
- Temporal Cognitive Graph or graph storage;
- generic multi-Agent organization, Branch/Join runtime, or Agent society;
- universal organization/governance object model;
- continual self-modification or automatic training/promotion loop.

Their next admission conditions live in [`../research/computer-responsibility-map-v2.json`](../research/computer-responsibility-map-v2.json).

## 10. Current repository mapping

- `ordivon-host` owns its current durable Goal/Task/Assignment/completion product facts;
- `ordivon-harness` owns its current cognitive Run and Provider/Tool-loop facts;
- `ordivon-runtime` owns Workspace, Job, process, output, cancellation, Artifact, and execution-recovery facts;
- Observation research owns no product facts and only reconstructs owner-native evidence;
- `ordivon-protocol` owns versioned shared contract artifacts, not the runtime truth of any consumer.

These mappings describe current ownership. They do not require the same repository topology for future implementations.

## 11. Structural rule

Use intelligence for novel, unstable judgment. Externalize only repeated structure that is cheaper, safer, more durable, or more shareable outside token space.

```text
novel cognition
→ repeated burden
→ measurable candidate externalization
→ strong simpler baseline
→ local Tool / adapter / owner state when sufficient
→ shared protocol only after multiple consumers
→ Core only for the surviving responsibility
```

A durable primitive survives because deleting its responsibility causes a concrete failure, not because its name appears in an earlier architecture diagram.
