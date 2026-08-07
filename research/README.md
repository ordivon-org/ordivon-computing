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

- [`research-method-v1.json`](research-method-v1.json) — machine-readable Agent-first research method for burden discovery, responsibility placement, externalization admission, and consequence-gated escalation;
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

Durable question pages preserve hypotheses, baselines, falsifiers, and evidence criteria. `portfolio.json` owns current portfolio status and WIP. GitHub Issues carry discussion, implementation history, and repository-local execution. Product repositories and `experiments/` carry executable artifacts. `evidence/` binds exact historical revisions, services, contracts, and Artifact digests; it is not a mutable deployment registry.

Research may contain alternatives, failed experiments, changing terminology, and incomplete models. Results move into [`../knowledge/`](../knowledge/) when they become reusable. Only compact, stable, cross-workload responsibilities that survive strong classical counterexamples may enter [`../core/`](../core/).

## Start here

- [`research-method-v1.json`](research-method-v1.json) defines how an Agent turns observed work burden into a falsifiable externalization experiment. It does not own research status.
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

## Historical comparisons

- `ANC-EDGE-001`, `ANC-LINK-001`, and `ANC-WORLD-001` are superseded by `ANC-WORLD-002`;
- `ANC-SECURITY-002` remains completed Phase 0 substrate evidence and is superseded by the unified World and strategic-Security programs;
- Semantic Core, Effect IR, Task continuation, Host boundary, and original Game/Host convergence are completed or frozen evidence, not open construction promises.

Research-method and portfolio maintenance commands:

```bash
python3 scripts/check_agent_research_method.py
python3 scripts/check_research_portfolio.py
python3 scripts/render_research_portfolio.py --check
```

The primary-source derivation for `ANC-STACK-001` and the cross-paradigm validation program live in [`../studies/2026-classical-to-agent-native-computing/`](../studies/2026-classical-to-agent-native-computing/).

The first-principles derivation from transcript-centered Agent loops to a typed Temporal Cognitive Graph, including the pinned Host/Harness/Runtime audit, frontier evidence, candidate model, falsifiers, and reversible migration, lives in [`../studies/2026-linear-loop-to-temporal-cognitive-graph/`](../studies/2026-linear-loop-to-temporal-cognitive-graph/). It is consumed through deferred `ANC-COMPILER-002`; it does not activate a graph platform, Runtime Worker, multi-Agent layer, or third WIP line by itself.

The strategic adversarial-systems reorientation, source comparison, insertion map, and research program live in [`../studies/2026-agent-native-adversarial-systems/`](../studies/2026-agent-native-adversarial-systems/).

The execution-entity, lineage, propagation, organization, control, resilience, and adversarial-ecology synthesis lives in [`../studies/2026-execution-entity-adversarial-ecology/`](../studies/2026-execution-entity-adversarial-ecology/). It is a completed reference study consumed through `ANC-SECURITY-007`; it does not activate implementation or promote a shared entity protocol.

The expanded Game thesis, comparative source set, experience/infrastructure admission split, and bounded post-alpha falsification program live in [`../studies/2026-agent-native-game-worlds/`](../studies/2026-agent-native-game-worlds/). `ANC-GAME-001` remains the completed Host/Game ownership question; `ANC-GAME-002` is the deferred product-and-world question and must not displace the current Ready Frontier.

The scarcity, operability, and paradigm-change lens that guided the August 2026 Ordivon reform audit lives in [`../studies/2026-scarcity-operability-and-paradigm-change/`](../studies/2026-scarcity-operability-and-paradigm-change/). It is retained as a reference study; it does not alter the active Ready Frontier, admit a Core primitive, or authorize implementation changes by itself.

The dated Ordivon formalism and A11 reform audit is preserved in [`../studies/2026-ordivon-paradigm-reform/`](../studies/2026-ordivon-paradigm-reform/). It records the source-level deletion judgments that informed the August 2026 P0/P1 closeout; it is closed evidence, not a new active research line or mandatory governance process.

The one-time [`HISTORICAL-DOCUMENT-AUDIT.md`](HISTORICAL-DOCUMENT-AUDIT.md) records the retain, merge, historical, archive, delete, and rewrite-summary decisions applied to high-impact historical documents. It is audit evidence and does not own portfolio status or architecture.
