---
schema_version: 1
id: computing.research.start
title: Research
type: start
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-07
summary: Canonical entry to the Agent-first research method, active questions, portfolio state, experiments, evidence, and construction rules.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-computing
related:
  - computing.authority
---
# Research

Research stores open questions, competing hypotheses, prototypes, experiments, immutable evidence manifests, and unresolved evidence.

## Purpose

- [`world-model-loop-v1.json`](world-model-loop-v1.json) — machine-readable closed loop for project-evidence assimilation, cross-project comparison, shared world-model revision, and project re-test;
- [`world-model-frontier.json`](world-model-frontier.json) — Computing-owned assimilation state binding exact observed project revisions without copying product maturity or domain state;
- [`WORLD-MODEL-LOOP.md`](WORLD-MODEL-LOOP.md) — human-readable projection of the world-model loop;
- [`world-model-assimilation-round-001.json`](world-model-assimilation-round-001.json) and [`WORLD-MODEL-ASSIMILATION-001.md`](WORLD-MODEL-ASSIMILATION-001.md) — first accepted return pass from current project practice into shared Core claims;
- [`experiments/world-model-a6-cross-domain-v0/`](experiments/world-model-a6-cross-domain-v0/) — first lower-half world-model re-test: Finance evidence tests Agent-owned source selection against full and caller-preselected views, including scale and campaign-recovery pressure;
- [`experiments/world-model-a10-time-scope-v0/`](experiments/world-model-a10-time-scope-v0/) — Security-grounded A10 re-test of historical/current truth admission; retains A10, rejects premature freshness standardization, and records evaluator-authority pressure;
- [`experiments/world-model-a10-world-presence-v0/`](experiments/world-model-a10-world-presence-v0/) — second-domain A10 re-test using World Presence; confirms the shared semantic distinction while rejecting a shared temporal relation-index mechanism in the bounded workload;
- [`experiments/structured-commitment-consistency-v0/`](experiments/structured-commitment-consistency-v0/) — conclusion-boundary falsifier separating schema validity, semantic consistency, owner truth admission, and downstream commitment authority while testing the existing Harness correction gate;
- [`research-method-v1.json`](research-method-v1.json) — specialized Agent-first method for burden discovery, responsibility placement, externalization admission, and consequence-gated escalation;
- [`computer-responsibility-map-v1.json`](computer-responsibility-map-v1.json) — machine authority for the current future-model-robust Ordivon Computer re-derivation;
- [`computer-product-boundary-review-v1.json`](computer-product-boundary-review-v1.json) — C3 closeout for Host, Harness, Runtime and Observation packaging against real consumers and recovery boundaries;
- [`COMPUTER-RESPONSIBILITY-REVIEW.md`](COMPUTER-RESPONSIBILITY-REVIEW.md) — human projection of the responsibility map;
- [`AGENT-FIRST-RESEARCH-METHOD.md`](AGENT-FIRST-RESEARCH-METHOD.md) — human-readable projection of that method;
- [`portfolio.json`](portfolio.json) — authoritative research status, maturity, blockers, next falsifiers, and WIP lines;
- [`PORTFOLIO.md`](PORTFOLIO.md) — generated human-readable portfolio and Ready Frontier;
- [`map.yaml`](map.yaml) — stable typed relations among construction tracks and research questions;
- [`questions/`](questions/) — one durable page per file-backed question, including historical questions;
- [`experiments/`](experiments/) — executable artifacts and experiment records;
- [`evidence/`](evidence/) — immutable cross-repository System Snapshots and their validator;
- [`charters/`](charters/) — durable missions and responsibility boundaries for cross-project research fabrics;
- [`capability-gaps/`](capability-gaps/) — evidence-oriented missing-capability registers, not implementation roadmaps;
- [GitHub Issues](https://github.com/zycxfyh/ordivon-computing/issues) — active construction tracks, dependencies, discussion, and Ready Frontier.

Durable question pages preserve hypotheses, baselines, falsifiers, and evidence criteria. `portfolio.json` owns current portfolio status and WIP. GitHub Issues carry discussion, implementation history, and repository-local execution. Product repositories and `experiments/` carry executable artifacts. `evidence/` binds exact historical revisions, services, contracts, and Artifact digests; it is not a mutable deployment registry. Cross-repository current-state audits must distinguish the observed local `HEAD`, the upstream or published release revision, and the exact dependency revisions actually consumed; these are separate facts and must not be collapsed into one “current version.”

Research may contain alternatives, failed experiments, changing terminology, and incomplete models. Results move into [`../knowledge/`](../knowledge/) when they become reusable. Only compact, stable, cross-workload responsibilities that survive strong classical counterexamples may enter [`../core/`](../core/).

## Start here

- [`world-model-loop-v1.json`](world-model-loop-v1.json) defines how owner-native project evidence can challenge and revise the shared world model without centralizing project facts.
- [`research-method-v1.json`](research-method-v1.json) defines how an Agent turns one specific class of observed work burden into a falsifiable externalization experiment. It is a method consumed by the broader world-model loop, not the universal research method.
- [`computer-responsibility-map-v1.json`](computer-responsibility-map-v1.json) is the current reform input for Ordivon Computer; it classifies durable responsibilities, classical owners, product-specific packaging, and conditional cognition candidates without changing product authority.
- [`portfolio.json`](portfolio.json) is the mutable source of truth for line status, maturity, blockers, falsifiers, and disposition.
- [`PORTFOLIO.md`](PORTFOLIO.md) is its generated review projection.
- [`questions/`](questions/) owns durable question pages, including completed and superseded questions; only `portfolio.json` determines which are active.
- [`experiments/`](experiments/) owns executable investigations.
- [`evidence/`](evidence/) owns retained observations and immutable snapshots.

## Current boundary

Research importance does not imply active work, implementation commitment, or publication authority. A result can inform Core only after its evidence and limitations survive the relevant admission and deletion tests.

## Construction program

The cross-layer construction program is [#1 — Construct the Agent-Native Machine](https://github.com/zycxfyh/ordivon-computing/issues/1). Its tracks and typed relations are indexed in [`map.yaml`](map.yaml). The program is not a commitment to reimplement the whole computing stack: [`ANC-STACK-001`](questions/ANC-STACK-001-classical-to-agent-native-transition.md) determines which responsibilities should remain inherited, researched, or constructed.

## Current Ready Frontier

The canonical current view is [`PORTFOLIO.md`](PORTFOLIO.md), generated from [`portfolio.json`](portfolio.json). This overview intentionally does not repeat active line identifiers, question statuses, or next actions.

## Stage identifier scopes

Short stage labels are local to their program; they are not global Ordivon identifiers. Cross-program discussion should use qualified names:

- `ACR-C1` … `ACR-C5` — the Agent-first Computer Responsibility reform recorded in the responsibility map and review;
- `XINF-A0` … `XINF-A8` — the cross-cutting infrastructure audit sequence; `XINF-A0` and `XINF-A1` are closed reference work, while later labels remain plan-local until recorded by an owning artifact;
- `OCR-V0:A1` … `OCR-V0:D4` — work packages inside [`experiments/cognitive-reform-v0/program-v1.json`](experiments/cognitive-reform-v0/program-v1.json).

A shared suffix such as `A1` or `C4` implies no dependency, status, or shared authority across these scopes. New cross-program prose should use the qualified form.

## Historical comparisons

- `ANC-EDGE-001`, `ANC-LINK-001`, and `ANC-WORLD-001` are superseded by `ANC-WORLD-002`;
- `ANC-SECURITY-002` remains completed Phase 0 substrate evidence and is superseded by the unified World and strategic-Security programs;
- Semantic Core, Effect IR, Task continuation, Host boundary, and original Game/Host convergence are completed or frozen evidence, not open construction promises.

Research-method and portfolio maintenance commands:

```bash
python3 scripts/check_world_model_loop.py
python3 scripts/check_agent_research_method.py
python3 scripts/check_computer_responsibility_map.py
python3 scripts/check_historical_research_compression.py
python3 scripts/check_research_portfolio.py
python3 scripts/render_research_portfolio.py --check
```

Completed Computing derivations no longer remain in the active tree by default. Their reusable conclusions are compressed into [`../knowledge/agents/capability-externalization-and-responsibility-placement.md`](../knowledge/agents/capability-externalization-and-responsibility-placement.md); exact removed Git trees and dispositions are recorded in [`evidence/agent-first-historical-research-compression-f95d721.json`](evidence/agent-first-historical-research-compression-f95d721.json). Live conditional ideas such as `ANC-COMPILER-002` retain only the current question, stronger baseline, falsifier, and exact evidence pointer.

The strategic adversarial-systems reorientation, source comparison, insertion map, and research program live in [`../studies/2026-agent-native-adversarial-systems/`](../studies/2026-agent-native-adversarial-systems/).

The execution-entity, lineage, propagation, organization, control, resilience, and adversarial-ecology synthesis lives in [`../studies/2026-execution-entity-adversarial-ecology/`](../studies/2026-execution-entity-adversarial-ecology/). It is a completed reference study consumed through `ANC-SECURITY-007`; it does not activate implementation or promote a shared entity protocol.

The expanded Game thesis, comparative source set, experience/infrastructure admission split, and bounded post-alpha falsification program live in [`../studies/2026-agent-native-game-worlds/`](../studies/2026-agent-native-game-worlds/). `ANC-GAME-001` remains the completed Host/Game ownership question; `ANC-GAME-002` is the deferred product-and-world question and must not displace the current Ready Frontier.

The one-time [`HISTORICAL-DOCUMENT-AUDIT.md`](HISTORICAL-DOCUMENT-AUDIT.md) records the retain, merge, historical, archive, delete, and rewrite-summary decisions applied to high-impact historical documents. It is audit evidence and does not own portfolio status or architecture.
