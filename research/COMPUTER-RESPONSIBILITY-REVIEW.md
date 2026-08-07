---
schema_version: 1
id: computing.research.computer-responsibility-review
title: Ordivon Computer Responsibility Review
type: reference
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-07
summary: Human-readable projection of the Agent-first responsibility map used to re-derive Ordivon Computer for stronger future Agents.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
related:
  - computing.research.agent-first-method
---
# Ordivon Computer Responsibility Review

The machine authority for this review is [`computer-responsibility-map-v1.json`](computer-responsibility-map-v1.json). This page explains the current disposition; it does not own product state or authorize implementation changes in Host, Harness, Runtime, World, or other repositories.

## Result

The durable center of Ordivon Computer is smaller than the historical architecture vocabulary.

A materially stronger future Agent still needs external structure when the responsibility concerns reality rather than temporary model weakness:

1. **open-work identity and continuity** — current work and unresolved operation state survive model, Provider, process, and Session replacement;
2. **current Context binding** — one cognitive episode sees current, authorized, revision-valid sources rather than treating transcript as truth;
3. **consequence and authority** — reversible private exploration stays cheap while shared, revoked, stale, costly, or irreversible consequence is admitted externally;
4. **Effect uncertainty and reconciliation** — intended Effect and physical attempt stay distinct, `UNKNOWN` remains explicit, and response loss is reconciled before redispatch;
5. **evidence, verification, and completion** — model proposal, Tool output, Artifact, Claim, independent verification, and accepted completion are not silently collapsed where consequence or evaluation requires separation;
6. **Tool contract identity and drift** — pending work binds to the actual callable contract rather than stale model-visible schema;
7. **owner-native observation projection** — Agents can inspect cross-owner state without creating a new shadow authority.

These are responsibilities, not promises that today's Ordivon object names, repositories, or storage layouts are permanent.

## What shrinks

Several earlier ideas remain useful only in narrower form:

- **Task / Host state** retains the minimum semantic work identity, but storage may be supplied by a mature durable workflow or domain owner;
- **Context** retains current-source and revision binding, while the experiment already showed that current-revision retrieval can match a richer source-bound representation; a general Context Kernel is not justified;
- **Effect machinery** retains identity, uncertainty, and reconciliation, but ordinary idempotency keys, audit records, or durable Activities should own the mechanism when they are sufficient;
- **Verification** remains at declared consequence and evaluation boundaries rather than becoming a universal Fact database;
- **Observation** remains an owner-native export and derived projection; daemon, multi-node, and central shadow-database infrastructure stay unproven;
- **Agent IR** shrinks to consumed boundary contracts such as Effect, ToolContract, and Binding. Internal cognition, plans, and provider-native representations stay local.

## What is not Core

The following are explicitly model- or workload-contingent:

- Ordivon Harness as a universal cognition runtime;
- a general Agent Memory runtime;
- a generic World layer;
- semantic Action lowering as a universal primitive;
- Prime-style programmable cognition and persistent Run Actor;
- Temporal Cognitive Graph / graph storage;
- generic multi-Agent branch/join infrastructure;
- universal Participant/Commitment organization objects;
- continual self-modification or training infrastructure.

They remain legitimate experiments only when a stronger simpler baseline exposes the corresponding burden.

## Evidence that changed the architecture

The most important existing results are already sufficient to remove several assumptions:

- transcript-summary continuity duplicated a world Effect and lost unresolved operation identity, while LangGraph SQLite, Temporal Workflow, and Ordivon typed state recovered it;
- six live Codex/Hermes replacement trials continued after response loss without the original transcript or persistent Provider Session;
- full-transcript and rolling-summary Context used stale or unsupported state, while current-revision retrieval matched the source-bound variant at lower representation cost;
- plain Tool retry duplicated an Effect after response loss, while idempotency/audit, durable Activity, and Ordivon Effect variants reconciled without redispatch;
- approval-everywhere created unnecessary interruption while static/model-only selection missed consequential or revoked cases; evidence-rich consequence selection passed;
- B5 DeepSeek Trials exposed model/tool-interface friction, but the separate V2 semantic edit surface has only scripted-Provider + real-Runtime acceptance, so semantic lowering is an experiment rather than a Core claim;
- Observation B3 proved cross-owner reconstruction while preserving owner-native truth.

## New Computer shape

The emerging architecture is therefore not a ladder of Agent-specific subsystems. It is three bands:

```text
Flexible cognition and product policy
  model / Provider-native Harness / Ordivon Harness / local planner / optional specialists

Durable responsibility boundaries
  work identity
  current-source Context binding
  consequence and authority
  Effect identity + uncertainty + reconciliation
  evidence / verification / completion
  Tool-contract drift
  owner-native inspect projections

Classical substrate
  OS / Git / database / network / VM / workflow / queue / compiler / model serving / domain APIs
```

The middle band should remain thin. Each responsibility chooses the lowest existing owner that can preserve its invariant. A named Ordivon layer is admitted only when no mature lower owner can do so and multiple workloads demonstrate recurring value.

## Reform frontier

`C1` is now the next step: rewrite Core architecture around this three-band model and remove wording that accidentally makes R0–R8 look like permanent subsystem layers.

Then:

- `C2` compresses completed research questions that no longer own a live falsifier;
- `C3` re-audits Host, Harness, Runtime, and Observation packaging against current consumers;
- `C4` tests Agent-facing semantic actions, inspect projections, and operational working state before Prime/TCG/multi-Agent construction;
- `C5` applies the method to the rest of Ordivon under each domain's own authority.

No step is authorized merely by appearing in this sequence. Each still passes the Agent-first research admission gates.
