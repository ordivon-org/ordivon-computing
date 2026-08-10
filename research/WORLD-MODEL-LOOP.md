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
updated: 2026-08-10
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

The current machine authority is [`world-model-loop-v2.json`](world-model-loop-v2.json). [`world-model-frontier.json`](world-model-frontier.json) remains the accepted Round-001 historical observation frontier; [`world-model-freshness-p2.json`](world-model-freshness-p2.json) is a later freshness assessment, not a replacement owner-state registry.

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


## Historical observation is not currentness

P2 exposed a method failure: an exact observed Git revision can remain valid historical evidence after its owner repository has advanced. A structural checker that only validates SHA syntax can therefore produce a false sense of currentness. WML v2 requires current cross-project claims to classify the relation between the retained observation and the selected owner source: `exact`, `owner_advanced`, `checkout_behind_observation`, `diverged`, or `observed_unavailable`.

This classification is sensing only. `owner_advanced` means Computing should review new owner evidence before asserting current state; it does **not** mean the shared world model changed, and it does not authorize copying owner-native mutable facts.

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

## Evaluator authority pressure

[`experiments/world-model-a10-time-scope-v0/`](experiments/world-model-a10-time-scope-v0/) exposed a second lower-half failure: Computing initially assigned a unique expected answer to one Security counterfactual even though Security had not defined the relevant current-truth invalidation law. The raw model observations remain evidence, but that case is excluded from accepted scientific accuracy.

This sharpens the return-loop discipline:

```text
candidate != evaluator
evaluator independence != domain truth authority
```

Cross-project evaluation must bind its oracle to owner-native semantics or to an explicit counterfactual law declared as part of the experiment. Computing may compare and falsify shared claims, but it cannot make an unresolved project-local truth rule become true by placing a label in a benchmark. This is retained as method pressure; it does not yet justify a new machine loop version.

## Second-domain A10 re-test

[`experiments/world-model-a10-world-presence-v0/`](experiments/world-model-a10-world-presence-v0/) tests the same A10 distinction against committed World Presence semantics rather than Security predicate truth. World independently requires current relation evidence to remain bound to exact Subject, Body, owner scope and query coordinates: historical occurrence or materialization does not become current Presence, observation failure remains `UNKNOWN`, and absence through one Body does not imply global Subject absence.

The cross-domain relation survived, but the Security experiment's candidate temporal reduction did not generalize into a shared mechanism. Raw World owner records already produced the correct relation in every evaluated decision; an added query-relation index changed no answer and increased Provider token use. The shared model therefore retains the semantic/authority distinction while leaving temporal evidence representation owner-native.

## Structured commitment boundary

[`experiments/structured-commitment-consistency-v0/`](experiments/structured-commitment-consistency-v0/) tests a failure first exposed by the Security A10 campaign: one schema-valid structured answer disagreed with the semantic conclusion stated in the same model output. The follow-up does not promote free-form rationale into authority. Instead it separates four boundaries:

```text
structural validity
!=
semantic consistency
!=
owner truth admission
!=
downstream effect authority
```

A deterministic falsifier proves that the existing Harness structured codec can correctly accept a schema-valid but cross-field-inconsistent candidate, while the existing caller/domain `validate_conclusion` hook can reject that candidate and drive a correction turn before terminal completion. A 48-decision live campaign produced no naturally occurring inconsistency or truth error under an explicit owner law, so the result supports the current responsibility split rather than a new global Harness semantic verifier. Domain semantic admission remains conditional on an actual owner invariant and consequence boundary.

## Finance consequence-boundary dogfood

[`experiments/finance-conclusion-admission-dogfood-v0/`](experiments/finance-conclusion-admission-dogfood-v0/) takes the next return edge into a real owner domain. The Agent submits only Finance `ExecutionOrderIntent v0`; Finance itself deterministically lowers the intent through `execution.request.prepare@1` and applies current C2 Proposal, authority, market-basis, notional, lot/tick and risk semantics without reserving or dispatching an external effect.

The dogfood naturally produced schema-valid but Finance-denied intents. In one gated Run, the same Agent moved from delegated size 13, to 13 again, to admitted size 12 after Finance rejection; in another replicate, rejection failed to converge before the current correction budget was exhausted. This establishes both the value and the limit of owner-native conclusion admission.

It also exposes a Harness-local collapse that does **not** justify moving Finance semantics into Harness:

```text
Tool-call correction
!=
conclusion correction
```

The dogfood exposed two focused Harness mechanics pressures: model-correctable conclusion rejection consumed `toolCorrections` / `max_tool_corrections` despite zero Tool calls, and the correction message incorrectly assumed every domain rejection meant incompleteness or missing evidence. Harness later resolved both without importing Finance semantics. Implementation `9e47ee615b2db77e274921ef5a043e429ba04c56` separates conclusion correction from Tool correction; acceptance `a38f4cfde3b20c64219ab00d911cac738da8961e` verifies the boundary, and both revisions remain ancestors of the currently observed clean Harness main `49a388238ed5df9d50be182f06bb86e3e2ff2e5b`.

The remaining live non-decodable structured-conclusion pressure was then reproduced deterministically in Harness. The exact path was not a Finance semantic error: a Harness-owned external-observation `NO_PROGRESS` disposition synthesized a plain-text `needs_input` `AgentRunConclusion`, so a valid `structured-result-v1` caller received a non-null conclusion that could not satisfy its caller-owned result representation. Harness implementation `8170e65778ba40a1e6cdc2b526b2b753f7387317` removes that synthesized conclusion while retaining the stop reason in Run detail/Trace; acceptance `a4b28963ee7a0196df961a7409c599da90d26ec0` verifies the result and also remains an ancestor of current Harness main.

The returned relation is therefore broader than the original Finance failure but still narrower than a Core revision:

```text
Tool-call correction != conclusion correction
Harness execution disposition != Agent semantic conclusion
```

These are candidate shared ownership relations. They do not justify a global semantic verifier, a generic correction service, or a new Round 002 by themselves. The next Computing assimilation review should compare them with independent Runtime, Host, World and domain evidence before deciding whether they remain reusable Knowledge or pressure an existing Core claim.

The experiment also caught and excluded its own first runner revision after the evaluator target accidentally entered Agent-visible context. This reinforces the same authority discipline at the method layer: evaluator answers are not ordinary Agent input merely because the evaluator owns scoring.
