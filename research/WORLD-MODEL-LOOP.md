---
schema_version: 1
id: computing.research.world-model-loop
title: World Model Loop
type: reference
profile: research
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-09
summary: Canonical human projection of how project evidence revises Ordivon's shared world model and returns falsifiable implications to independent project owners.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.research.start
  - computing.foundations
---
# World Model Loop

The machine authority is [`world-model-loop-v1.json`](world-model-loop-v1.json). The current assimilation state is [`world-model-frontier.json`](world-model-frontier.json).

## World model

Ordivon's **world model** is the current large set of claims used to describe what exists, what relations and causal boundaries matter, what can be observed or changed, which constraints remain real, and which structures are justified. It is distributed by responsibility rather than stored as one giant object:

```text
Core       compressed current shared claims
Knowledge  reusable explanations, limits, and cases
Research   live contradictions, alternatives, and falsifiers
Projects   owner-native facts, implementations, experiments, and world effects
```

Core is therefore a compression of the shared world model, not a copy of project state. A project can change rapidly without changing Core; a small project experiment can change Core when it falsifies a shared assumption.

## Closed loop

```text
current shared world model
        ↓
research questions / project structures
        ↓
project practice and external-world interaction
        ↓
owner-native evidence
        ↓
project delta + model pressure
        ↓
cross-project comparison
        ↓
retain / narrow / split / revise shared claims
        ↓
project-specific reform questions
        ↓
independent project re-test
        └────────────────────↺
```

The return edge is mandatory. A reform is incomplete when Computing sends a new principle into projects but never re-observes what the projects discovered after using it.

## What returns to Computing

Do not return every commit or local design decision. Return a candidate world-model pressure when evidence exposes at least one of these:

- a distinction the current shared model collapses but a project can now observe or act on;
- a current Core or Knowledge claim contradicted by owner-native evidence;
- the same relation appearing independently in materially different projects;
- a supposedly shared structure that a project deleted without losing its claimed invariant;
- a local mechanism that repeatedly solves a failure currently reconstructed elsewhere;
- a changed capability that makes an older scarcity assumption or constraint obsolete;
- a new consequence, authority, evidence, recovery, or value boundary that changes what counts as a correct system description.

Implementation churn, naming changes, local optimization, and maturity changes do not qualify by themselves.

## Assimilation is not central control

Projects remain free to develop local models and experiments under their own authority. Computing does not approve ordinary domain evolution. It only owns the shared comparison step: whether a local result should remain local, revise reusable Knowledge, challenge Core, or create a new cross-project Research question.

A `ReformImplication` is therefore a question such as:

> If Agent-selected Working Sets outperform externally assembled Context while preserving durable history, which other projects still assume that the caller should choose the complete model-visible view?

It is not an instruction to patch every repository in the same way.

## Method self-revision

The loop itself is part of the world model. If repeated assimilation shows that its selection rules miss important project discoveries, over-promote local claims, create excessive synchronization cost, or fail to propagate falsifiers, a new loop version must be tested. The method does not receive permanent authority from being written down once.

## First dogfood round

[`world-model-frontier.json`](world-model-frontier.json) records the first post-Agent-first assimilation frontier. It intentionally marks project revisions for review without asserting that every revision changed the shared world model. Finance and Studio also expose a simpler structural drift: both are real Ordivon projects while the previous stable registry still described a nine-project family. Fixing that drift is the first concrete demonstration that project reality must be able to revise Computing's own model of Ordivon.

## First lower-half re-test

[`experiments/world-model-a6-cross-domain-v0/`](experiments/world-model-a6-cross-domain-v0/) consumes the Round 001 A6 implication against exact Finance and Harness revisions. It demonstrates why the lower half of the loop is not a synchronized architecture rollout: the shared claim can survive while one implementation choice is rejected. Agent-owned selection transferred to the Finance workload; a static latest-only caller rule did not, and a separate selection-only Model call carried a measurable fixed cost.

The experiment also exposed a method pressure. A transient Provider disconnect after many completed observations initially erased the campaign-level receipt. The repaired campaign checkpoints completed steps independently and later resumed without dispatching them again. This is retained as evidence that experiment-step truth and terminal runner success are different facts; whether that becomes a machine-level world-model-loop rule remains an open method question rather than an automatic v1 mutation.
