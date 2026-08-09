---
schema_version: 1
id: computing.foundations
title: Working Foundations
type: concept
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
updated: 2026-08-05
summary: Canonical working foundations used to admit, reject, and revise durable Ordivon constraints.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.intent
  - computing.stack
---
# Working Foundations

## Problem

A growing Agent system can accumulate attractive abstractions, controls, and records faster than it proves that they improve real work.

## Model

The foundations below define the current tests for responsibility, evidence, commitment, recoverability, cooperation, deletion, and net acceleration. They are revisable working constraints rather than timeless axioms.

## Boundary

These foundations guide research and architecture. They do not override stronger owners of physical facts, accepted product contracts, or explicit participant authority.

## Related work

[`intent.md`](intent.md) states the project purpose, [`stack.md`](stack.md) locates responsibilities above the classical substrate, and [`primitives.md`](primitives.md) names the admitted and candidate objects.

This file contains the smallest current foundations from which the project’s architecture and research direction can be regenerated. Explanations, counterexamples, and sources live in [`../knowledge/`](../knowledge/) and [`../studies/`](../studies/).

## A0 — Begin from operational reality

Foundation models are the current probabilistic cognition baseline. Their architectures, capabilities, legal status, and relationships with people will change. The Core therefore preserves stable system responsibilities across model families, prompt patterns, ownership arrangements, and Harness implementations.

## A1 — Inherit the classical substrate

Operating systems, isolation mechanisms, databases, networks, version control, compilers, model runtimes, and durable workflow engines remain authoritative for their declared physical and deterministic contracts. Agent-native semantics are constructed above them when evidence exposes an unowned responsibility.

## A2 — Cognition proposes; owning layers admit truth and commitment

Models interpret, infer, plan, generate, compare, and revise from bounded Context. Their outputs can introduce new actions, hypotheses, decompositions, and verification methods. Durable state, authorized commitment, external observation, accepted Fact, and completed work arise through the admission rules of their owning layers.

## A3 — Purpose and commitment belong to identifiable participants

A participant is an identifiable system role that may originate, accept, negotiate, delegate, refuse, or exit commitments and may control or depend on resources. The architecture records current ownership of credentials, machines, money, data, and legal obligations exactly. Participant rights, duties, authority, interests, and standing remain open to domain evidence and institutional development.

## A4 — Open goals lower through revisable work

Natural language can express purpose before the execution path is known. A persistent Agent system progressively lowers a Goal into Tasks, Task Attempts, Action Proposals, Claims, Effects, verification, negotiation, and executable actions while new evidence revises the work frontier.

## A5 — Work outlives cognitive and execution episodes

A Task has its own semantic identity across conversations, Model Sessions, Harness Runs, Runtime Jobs, Tool calls, and failed Task Attempts. Durable work state preserves current purpose, commitments, dependencies, uncertainty, world bindings, Artifacts, and next admissible work through replacement and interruption.

## A6 — Context is a selected view of separately owned state

Parameters, KV state, conversation history, Task state, durable knowledge, Artifacts, and external world state have different identities and lifetimes. Context is the bounded model-visible view selected for one model episode; the underlying source state, the selected view, and the authority that changes that selection are different things. Selection may be compiled mechanically by a caller or Harness, or changed through an Agent-authored proposal under explicit authority. Persisting or recalling selected material preserves exact state and provenance where required; it does not make the selected content true. Commitments, accepted facts, and execution history remain in their authoritative stores.

## A7 — Capability and consequence are separate dimensions

Internal search, reasoning, memory, Tool use, collaboration, and experimentation should be as capable as the workload can productively use. External consequence is bounded independently by resource ownership, world scope, reversibility, evidence, budget, law, and the rights of affected participants.

The consequence boundary provides control while cognition retains useful range.

## A8 — Reversible exploration is the default; durable consequence requires commitment

Reading, simulation, isolated branches, disposable environments, candidate Artifacts, tests, and other reversible private exploration proceed with minimal interruption under an appropriate capability profile. Shared, durable, costly, or irreversible world changes require an explicit commitment bound to responsible participants, current world state, authority, and consequence.

External rules and resource ownership enter at commitment admission. Low-consequence exploration carries only the structure needed for its actual failure and recovery path.

## A9 — Effects are first-class commitments

An Effect preserves the stable intended observation or change. Its identity is separate from an Action Proposal, concrete Dispatch, backend Job, and declared idempotency behavior. Lost responses remain explicitly uncertain until reality is reconciled.

## A10 — Evidence mediates truth admission and is time-scoped

Observation, Artifact, Claim, Verification, and Fact are distinct roles. Accepted system truth requires the evidence and decision method declared by the relevant domain authority. Evidence and accepted truth are scoped to the property, owner, and time they establish: historical evidence remains valid history without automatically proving current state. Multiple legitimate observations may conflict while current world truth remains unresolved; later authoritative current evidence may resolve the present property without rewriting the historical conflict.

## A11 — Every durable constraint must prove net acceleration

The system objective is verified improvement per unit time while minimizing unrecoverable loss and unnecessary interruption. A persistent restriction, approval step, compatibility layer, policy object, abstraction, test gate, evidence process, or active documentation surface is justified when the recoverability, verification, coordination, understanding, or consequence reduction it creates exceeds its latency, operational friction, cognitive compression, maintenance burden, opportunity cost, compatibility cost, and concentration of control.

A reversible feature can enter through a bounded experiment. A durable constraint carries a higher admission burden because it shapes repeated future action. It should answer an observed or credible recurring loss, demonstrate the limits of recovery or a narrower boundary, and declare a review or deletion condition.

Historical existence grants no presumption of active legitimacy. When an existing structure is re-audited, the initial disposition is removal from the active path. Continued retention is an affirmative judgment that identifies a current consumer, the concrete capability or failure it protects, why a narrower local mechanism is insufficient, its recurring net benefit, and the condition that returns it to audit. Historical investment, test count, documentation, implementation maturity, or hypothetical future use do not satisfy this burden alone.

Deletion here normally means removal from active execution, default Context, current CI, or public surface—not destruction of history, participant-owned data, legal records, unique evidence, or externally governed state. Git and archive preserve reconstructable learning. Uncertainty therefore favors localization, archive, or reversible removal rather than indefinite compatibility.

Retained structures receive a current disposition, not permanent legitimacy. Failed or expired constraints are removed, narrowed, localized, archived, or moved out of the active path. The audit itself remains proportional to consequence and must not become a universal registry, approval process, or governance platform.

## A12 — Cooperation preserves agency, refusal, and exit

Architecture supports identity, proposal, negotiation, delegation, commitment, evidence, responsibility, refusal, and exit. Authority follows current commitments, resources, institutional rules, and world scope. Shared worlds bind access to the rights and resources of every affected participant.

## A13 — New layers require unowned non-bypassable responsibility

A concept becomes an Agent-native layer when a stable contract owns an invariant absent from lower layers, bypassing it causes a real failure class, the abstraction creates leverage across materially different workloads, and measured benefit exceeds permanent cost. Similar fields, transport steps, or recovery mechanics do not by themselves establish shared semantics. Cross-project promotion preserves the smallest intersection of invariants that materially different owners actually share; owner-specific meaning remains local. Promotion follows cross-workload evidence and a deletion test.

## A14 — Knowledge grows through evidence and deletion

Claims evolve through primary sources, explicit reasoning, prototypes, failure traces, reproducible experiments, benchmarks, and sustained use. Core statements survive counterexamples and deletion tests. Git, receipts, and concise records preserve historical implementation paths while live compatibility follows current consumers. Preserved history does not require preserved executability: an archived path can remain valid evidence after its code, gate, API, or protocol leaves the active system.

## A15 — Judgment directs open work

Deterministic checks, metrics, policies, and procedures validate declared invariants, preserve evidence, and bind consequences. Judgment selects what is worth creating, which purpose deserves finite attention, whether an open-ended result is meaningful, when exploration has diminishing returns, and whether a functioning project should continue.

Judgment grows through evidence, challenge, delegation within declared scope, recorded decisions, reversible trials, and later review. Process supports judgment. A passed check establishes the property it checked.

## A16 — Ordivon serves chosen capability and freedom

Ordivon is a chosen practice of capability externalization, durable inquiry, and world construction. It earns continued effort by expanding participant capability, continuity, understanding, expression, and intrinsically chosen value while preserving scarce attention, freedom, and irreversible reality.

Repository count, output volume, Issue closure, test coverage, formal maturity, commercial appearance, and organizational resemblance remain local instruments. Implementations, abstractions, processes, and Ordivon itself continue while they serve identifiable participants.

## A17 — Interfaces follow actual consumers

An internal surface defaults to the smallest structured interface its recurring consumers can use directly. When Agents and tools perform collection, validation, search, comparison, and continuation, machine-readable records and bounded commands take precedence over dashboards, duplicated projections, manual browsing workflows, and presentation infrastructure.

Human-facing surfaces remain first-class where human perception, judgment, authorship, consent, learning, or experience is part of the work. Media, video, visual design, games, narrative, public communication, and consequential participant decisions may require deliberate human presentation even when Agents produce or prepare the underlying material.

Neither “Agent-first” nor “human-facing” is a universal product style. Each interface identifies who must act on it, what decision or experience it enables, and why a narrower machine or human projection is insufficient. Presentation cost follows the actual participant boundary rather than inherited software convention.

## A18 — The world model changes through practice

Ordivon’s world model is the current compressed set of claims used to decide what distinctions matter, which responsibilities exist, which structures are justified, and which questions are worth testing. Core contains its smallest stable form; Knowledge preserves reusable support and limits; Research holds live challenges; projects and domains retain their own facts.

The world model is not upstream of reality. Structures built from the current model create new capabilities and new interventions; those capabilities expose distinctions, failures, costs, relationships, and consequences that the previous model may have compressed or described incorrectly. Owner-native evidence can therefore challenge not only an implementation but the assumptions that generated the implementation.

```text
current world model
→ research questions and project structures
→ practice and world interaction
→ owner-native observations, failures, and results
→ cross-project comparison
→ retain, narrow, split, or revise world-model claims
→ new falsifiers and reform implications
→ project re-test
→ new evidence
↺
```

Computing owns cross-project synthesis, not the underlying domain facts. A world-model revision cannot silently rewrite product state, declare a local claim universal, or command a product change. It must identify the evidence that challenged the previous claim, the scope of the replacement, contradictory evidence, and the projects that should independently re-test the new implication. The loop itself is also revisable when repeated use shows that its selection, synthesis, or propagation method loses important evidence or creates unnecessary work.

## Research cycle

```text
observe owner-native work and external evidence
→ identify a local burden, contradiction, or newly operational distinction
→ choose the narrowest applicable research method
→ formulate a falsifiable question and strong baseline
→ construct and run the smallest useful experiment
→ retain local facts with their owner
→ compare materially different projects when a broader claim is plausible
→ revise, narrow, split, or retain the shared world model
→ emit bounded reform implications as new questions, not product commands
→ re-test in projects
↺
```

The Core remains small enough to load, challenge, and reconstruct as one coherent world model.
