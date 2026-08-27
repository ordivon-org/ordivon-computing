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
updated: 2026-08-25
summary: Canonical entry to the Agent-first research method, active questions, portfolio state, experiments, evidence, and construction rules.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-computing
related:
  - computing.authority
---
<!-- cspell:words COJC CECB -->
# Research

Research stores open questions, competing hypotheses, prototypes, experiments, immutable evidence manifests, and unresolved evidence.

## Owner-native research cores

SCD and Computational Possibility are independent semantic owners with standalone physical homes:

- [Semantics of Computational Descriptions / `ordivon-scd`](https://github.com/zycxfyh/ordivon-scd)
- [Computational Possibility / `ordivon-computational-possibility`](https://github.com/zycxfyh/ordivon-computational-possibility)
- [`core/shared-computing-history/`](core/shared-computing-history/) — Broad Computing / historical S-T / Algorithmics provenance and recovery navigation only; it is not a semantic owner.

The former `research/core/...` owner paths now contain only non-authoritative migration tombstones. Repository co-location no longer exists for these owners.

## Purpose

- [`world-model-loop-v2.json`](world-model-loop-v2.json) — current machine-readable closed loop with explicit historical-observation/currentness separation for project-evidence assimilation, cross-project comparison, shared world-model revision, and project re-test;
- [`world-model-frontier.json`](world-model-frontier.json) — historical Round-001 assimilation frontier; currentness is assessed separately by [`world-model-freshness-p2.json`](world-model-freshness-p2.json) and `scripts/assess_world_model_freshness.py`;
- [`WORLD-MODEL-LOOP.md`](WORLD-MODEL-LOOP.md) — human-readable projection of the world-model loop;
- [`world-model-assimilation-round-001.json`](world-model-assimilation-round-001.json) and [`WORLD-MODEL-ASSIMILATION-001.md`](WORLD-MODEL-ASSIMILATION-001.md) — first accepted return pass from current project practice into shared Core claims;
- [`COJC-SEDIMENTATION-CANON-20260825.md`](COJC-SEDIMENTATION-CANON-20260825.md) — canonical first-look for the completed initial Cross-Owner Joint Capability / Capability Ecology campaign: final result map, `DeletionEssential != JointIrreducible`, fair Generic Composition Subtraction, cross-world Representation moderator standing, recovery order and natural-pressure reopen gate; use [`JOINT-CAPABILITY-PROGRAMME-20260825.md`](JOINT-CAPABILITY-PROGRAMME-20260825.md) for the full historical charter;
- [`WORLD-MODEL-SEDIMENTATION-AUDIT-20260824.md`](WORLD-MODEL-SEDIMENTATION-AUDIT-20260824.md) — current cross-owner audit of `Research Result != World Model != Persistent Environment`, including responsibility-relative primacy, external-solution preservation, promotion/lineage/first-look debt, seven-standing S0–S6 diagnostics, and the bounded current method repair;
- [`S6-LONGITUDINAL-CONSEQUENCE-AUDIT-20260826.md`](S6-LONGITUDINAL-CONSEQUENCE-AUDIT-20260826.md) — pre-frozen one-to-two-week longitudinal process trace across ten environment-shaping/contraction candidates: establishes bounded local S6 consequence and challenge/rebind evidence, preserves `Survival != Benefit` and `MaterializedOnBranch != CurrentlyInhabited`, and explicitly withholds system-wide ratchet/month-year/external-benefit claims;
- [`COMPUTER-AGENT-NATIVE-LINEAGE-20260724-20260825.md`](COMPUTER-AGENT-NATIVE-LINEAGE-20260724-20260825.md) — historical causal lineage of the Ordivon Computer question from rebuild-the-stack through Semantic Core, classical substrate/overlay, removal-first contraction, Situation, First Interface, and the current Representation Environment frontier; it preserves ancestry and rejected alternatives without overriding current Core/owner authority;
- [`COMPUTER-TO-REALITY-WORLD-MODEL-REVISION-20260825.md`](COMPUTER-TO-REALITY-WORLD-MODEL-REVISION-20260825.md) — working world-model revision that reinterprets the historical Computer line under later Reality, representation, continuity, Workstation, Computational Possibility, and laboratory research: layer diagrams become projections rather than ontology; instrumentation/evidence production become capability variables; physical realized state remains distinct from software-reported state; no new Lab or hardware owner is admitted without owner-native pressure;
- [`CONSTRUCTIVE-CAPABILITY-ENVIRONMENT-CLOSEOUT-20260825.md`](CONSTRUCTIVE-CAPABILITY-ENVIRONMENT-CLOSEOUT-20260825.md) — completed PPD closeout on deliberate environment construction: separates frontier expansion from infrastructure capital, latent affordance from realized capability, active instances from reconfiguration/reconstruction capacity, and capability from authority/currentness; continuity uniqueness and institution novelty were strongly subtracted, while reconfigurable productive infrastructure survives as a bounded empirical Ordivon pattern;
- [`DISCOVERABILITY-CURRENTNESS-AUDIT-CLOSEOUT-20260827.md`](DISCOVERABILITY-CURRENTNESS-AUDIT-CLOSEOUT-20260827.md) — closed cross-owner audit of problem-to-result rediscovery and currentness recovery: owner-unknown retrieval remains representation-dependent, multi-lane union can improve reachability without monotone ranking improvement, and historical validity / semantic-successor recovery remain distinct from owner-native currentness proof.
- [`BOOK-V05-INTEGRATION-AUDIT-20260825.md`](BOOK-V05-INTEGRATION-AUDIT-20260825.md) — source-fenced coverage audit of the current five-chapter Ordivon Book against the wider research/domain portfolio; distinguishes functional decision coverage from textual/project-name coverage, and its post-audit update records that the Result/Value explicit map did not earn a core Book edit for fresh-Agent correctness;
- [`experiments/book-result-value-compression-v0/`](experiments/book-result-value-compression-v0/) — bounded Book A/B falsifier: 5×22 Book-only and Map+Book primary decisions both reached 110/110, rejecting a correctness-motivated Book expansion, while a post-primary multi-label challenge found narrower operation-specific reconstruction value for the compact Result/Achievement/Value map;
- [`experiments/book-representation-effect-v0/`](experiments/book-representation-effect-v0/) — historical consumer × operation × persistence representation-effect evidence: immediate effects were model/operation dependent and did not survive the required second natural workload as a reusable cross-artifact candidate; executable verifiers were removed from the active tree under the pre-run ANC-REPRESENTATION-001 deletion rule; Human effects remain transport-gated and unclaimed;
- [`experiments/representation-natural-n1-v0/`](experiments/representation-natural-n1-v0/) — closed second natural falsifier for ANC-REPRESENTATION-001: the Claim/Evidence/Challenge/Boundary projection cut payload bytes by 80.3% and prompt tokens by 67.6% but regressed protected ObjectiveAchievement, BoundedImprovement and CurrentConsumption families versus exact full source, yielding `MIXED_N1_NOT_REPRODUCED`; the question is now completed/reference and no shared representation mechanism is authorized;
- [`experiments/representation-cross-world-reconciliation-v0/`](experiments/representation-cross-world-reconciliation-v0/) — reconciles the canonical negative N1 with an independently frozen positive COJC relational-audit world (`93/120 -> 111/120`, prompt tokens `28,236 -> 7,253`): generic reusable CECB remains closed, while operation-local projection value is retained as conditional on support dispersion, local scoped-detail fidelity, finite-consumer fit and lifecycle debt; future reopen requires a pre-run workload-geometry prediction, not another formatting benchmark;
- [`experiments/world-model-a6-cross-domain-v0/`](experiments/world-model-a6-cross-domain-v0/) — first lower-half world-model re-test: Finance evidence tests Agent-owned source selection against full and caller-preselected views, including scale and campaign-recovery pressure;
- [`experiments/world-model-a10-time-scope-v0/`](experiments/world-model-a10-time-scope-v0/) — Security-grounded A10 re-test of historical/current truth admission; retains A10, rejects premature freshness standardization, and records evaluator-authority pressure;
- [`experiments/world-model-a10-world-presence-v0/`](experiments/world-model-a10-world-presence-v0/) — second-domain A10 re-test using World Presence; confirms the shared semantic distinction while rejecting a shared temporal relation-index mechanism in the bounded workload;
- [`experiments/structured-commitment-consistency-v0/`](experiments/structured-commitment-consistency-v0/) — conclusion-boundary falsifier separating schema validity, semantic consistency, owner truth admission, and downstream commitment authority while testing the existing Harness correction gate;
- [`experiments/finance-conclusion-admission-dogfood-v0/`](experiments/finance-conclusion-admission-dogfood-v0/) — real-domain Finance dogfood showing schema-valid execution intent can fail owner admission and that owner feedback can correct a live Agent; the two Harness correction-mechanics pressures and the later NO_PROGRESS conclusion-ownership pressure were returned to Harness, deterministically resolved, and retained as cross-project evidence rather than Finance semantics;
- [`experiment-contract-v1.json`](experiment-contract-v1.json) — compact reusable declaration template for bounded experiments; every experiment freezes its own evidence, baseline, oracle, authority, stop/deletion, and rollback rules;
- [`computer-responsibility-map-v2.json`](computer-responsibility-map-v2.json) — machine authority for the current contracted Computer responsibility prior;
- [`computer-product-boundary-review-v1.json`](computer-product-boundary-review-v1.json) — C3 closeout for Host, Harness, Runtime and Observation packaging against real consumers and recovery boundaries;
- [`COMPUTER-RESPONSIBILITY-REVIEW.md`](COMPUTER-RESPONSIBILITY-REVIEW.md) — human projection of the responsibility map;
- [`portfolio.json`](portfolio.json) — authoritative research status, maturity, blockers, next falsifiers, and WIP lines;
- [`P0-P1-CONSUMER-FALSIFICATION-DESIGN.md`](P0-P1-CONSUMER-FALSIFICATION-DESIGN.md) — P0 closeout plus remaining P1 and conditional owner-native follow-up boundaries for Harness retention, authority timing, ordinary Web production, and MCP contract freshness;
- [`experiments/p0-consumer-falsification-v0/`](experiments/p0-consumer-falsification-v0/) — deterministic apparatus plus retained live Provider evidence: five one-shot/Harness pairs and three ACT/HOLD authority-timing pairs per treatment under exact revision-bound contracts;
- [`experiments/experiment-loop-v0/`](experiments/experiment-loop-v0/) — P2 file/Git Continuous Experiment Loop closeout: two P1 self-changes plus a third cross-evidence-family world-model freshness change with frozen holdout and physical rollback; claim remains bounded recursive self-improvement with transfer, not open-ended RSI;
- [`RSI-PAL-REUNDERSTANDING-CLOSEOUT-20260819.md`](RSI-PAL-REUNDERSTANDING-CLOSEOUT-20260819.md) — deduplicated interpretive closeout over the later RSI/PAL re-reading: retains adaptive-ecology, trajectory-standing, invariant-bound-self, scoped-improvement, Adaptive-Attention-as-problem-structure, scarcity/bottleneck-migration and moving-constraint-reorientation syntheses while routing repeated R2E/Atlas/activation material back to its stronger empirical owners and admitting no new architecture/Foundation;
- [`experiments/skill-compilation-v0/`](experiments/skill-compilation-v0/) — P3 negative capability-compilation falsifier: a real repeated UNKNOWN-recovery burden produced one research Skill candidate, but the unchanged procedure Skill lost to explicit Tool-contract facts on the repaired live campaign and was not promoted; mechanical source landing was also rejected as a Skill;
- [`experiments/multi-participant-adaptation-v0/`](experiments/multi-participant-adaptation-v0/) — P4 bounded multi-participant falsifier: independent branches showed development-only gain and complementary holdout errors, so generic Multi superiority was rejected; current Host Goal/Task/object/Verification semantics were sufficient for the minimum branch/Join pattern;
- [`experiments/owner-pressure-discovery-v0/`](experiments/owner-pressure-discovery-v0/) — C6 negative owner-pressure selection falsifier: a repaired selective-inspection candidate could sometimes stop correctly on a null holdout but did not reliably respect its evidence ceiling or find the frozen Harness shared-method pressure; full-evidence one-shot also failed to earn itself, so no pressure-discovery layer or next architecture phase is authorized;
- [`experiments/computer-existence-gauntlet-v0/`](experiments/computer-existence-gauntlet-v0/) — full removal-first existence audit over 47 Computer features: control-plane semantic mutants, protocol molecular ablation, content-stack deletion, 54,979-line active-tree shadow contraction, global-method falsification, and exact verdicts (`retain/narrow/localize/archive/delete/inconclusive`) without granting any new infrastructure layer;
- [`experiments/crosscut-maintenance-p5-v0/`](experiments/crosscut-maintenance-p5-v0/) — crosscut survival/contraction closeout: every P0–P4 feature receives a current existence verdict, owner-native temporal contracts replace the generic freshness/event apparatus, and 87 historical experiment files leave the active tree while exact Git recovery and current gates remain intact;
- [`experiments/entity-gap-eg0-eg8-v0/`](experiments/entity-gap-eg0-eg8-v0/) — comparative-capability entity-gap audit over real Finance, Workstation, Computing, Security, Game, Studio/Web/Human pressures: exact verifier, optimizer, estimator, sensing, simulator, human-response and retrieval falsifiers retain several non-Agent roles while promoting zero new shared services/protocols and falsifying a dedicated generic Archivist/index layer;
- [`experiments/p1b-mcp-contract-freshness-v0/`](experiments/p1b-mcp-contract-freshness-v0/) — historical pre-refresh MCP catalog/snapshot drift evidence; refreshed Runtime/Host connector functionality is now closed and referenced by the P0 live closeout;
- [`PORTFOLIO.md`](PORTFOLIO.md) — generated human-readable portfolio and Ready Frontier;
- [`map.yaml`](map.yaml) — stable typed relations among construction tracks and research questions;
- [`questions/`](questions/) — one durable page per file-backed question, including historical questions;
- [`experiments/`](experiments/) — executable artifacts and experiment records;
- [`evidence/`](evidence/) — immutable cross-repository System Snapshots and their validator;
- [`charters/`](charters/) — durable missions and responsibility boundaries for cross-project research fabrics;
- [`capability-gaps/`](capability-gaps/) — evidence-oriented missing-capability registers, not implementation roadmaps;
- [GitHub Issues](https://github.com/zycxfyh/ordivon-computing/issues) — active construction tracks, dependencies, discussion, and Ready Frontier.

Durable question pages preserve hypotheses, baselines, falsifiers, and evidence criteria. `portfolio.json` owns current portfolio status and WIP. Its M0-M6 values are question-evidence maturity, not product maturity or value; P0-P3 are Computing-local allocation judgments. Externally owned P0-P3 rows require an exact same-cut owner observation and otherwise remain reference-only. GitHub Issues carry discussion, implementation history, and repository-local execution. Product repositories and `experiments/` carry executable artifacts. `evidence/` binds exact historical revisions, services, contracts, and Artifact digests; it is not a mutable deployment registry. Cross-repository current-state audits must distinguish the observed local `HEAD`, the upstream or published release revision, and the exact dependency revisions actually consumed; these are separate facts and must not be collapsed into one “current version.”

Research may contain alternatives, failed experiments, changing terminology, and incomplete models. Results move into [`../knowledge/`](../knowledge/) when they become reusable. Only compact, stable, cross-workload responsibilities that survive strong classical counterexamples may enter [`../core/`](../core/).

## Start here

- [`../knowledge/research-methods/ordivon-research-method-and-paradigm-canon.md`](../knowledge/research-methods/ordivon-research-method-and-paradigm-canon.md) is the reusable cross-owner research-method first look. In particular, recover the strongest applicable internal **and external** standing before opening/closing a route; keep novelty subtraction separate from usable solution-domain knowledge; and adjudicate the surviving result's destination before declaring a materially changed line closed.
- [`world-model-loop-v2.json`](world-model-loop-v2.json) defines how owner-native project evidence can challenge and revise the shared world model while separating historical observation validity from currentness.
- [`experiment-contract-v1.json`](experiment-contract-v1.json) defines only the declarations every bounded experiment must freeze. It does not choose the hypothesis, evaluator truth, or correct answer, and it carries no product authority.
- [`RSI-LAB.md`](RSI-LAB.md) defines the current thin scientific-instrument surface for owner evidence packing, mechanical matrices, DuckDB/Parquet analysis, and revision pressure without scientific or product authority.
- [`computer-responsibility-map-v2.json`](computer-responsibility-map-v2.json) is the current responsibility prior for Ordivon Computer; retired architecture categories live in historical evidence rather than permanent active slots.
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

- `ACR-C1` … `ACR-C6` — historical labels from the completed v1 Computer Responsibility reform; they remain Git-recoverable but do not form the current v2 phase ladder;
- `XINF-A0` … `XINF-A8` — the cross-cutting infrastructure audit sequence; `XINF-A0` and `XINF-A1` are closed reference work, while later labels remain plan-local until recorded by an owning artifact;
- `OCR-V0:A1` … `OCR-V0:D4` — work packages inside [`experiments/cognitive-reform-v0/program-v1.json`](experiments/cognitive-reform-v0/program-v1.json).

A shared suffix such as `A1` or `C4` implies no dependency, status, or shared authority across these scopes. New cross-program prose should use the qualified form.

## Historical comparisons

- `ANC-EDGE-001`, `ANC-LINK-001`, and `ANC-WORLD-001` are superseded by `ANC-WORLD-002`;
- `ANC-SECURITY-002` remains completed Phase 0 substrate evidence and is superseded by the unified World and strategic-Security programs;
- Semantic Core, Effect IR, Task continuation, Host boundary, and original Game/Host convergence are completed or frozen evidence, not open construction promises.

Experiment-contract and portfolio maintenance commands:

```bash
python3 scripts/check_world_model_loop.py
python3 scripts/ordivon_lab.py --help
python3 scripts/check_experiment_contract.py
python3 scripts/check_computer_responsibility_map.py
python3 scripts/check_historical_research_compression.py
python3 scripts/check_research_portfolio.py
python3 scripts/render_research_portfolio.py --check
```

Completed Computing derivations no longer remain in the active tree by default. Their reusable conclusions are compressed into [`../knowledge/agents/capability-externalization-and-responsibility-placement.md`](../knowledge/agents/capability-externalization-and-responsibility-placement.md); exact removed Git trees and dispositions are recorded in [`evidence/agent-first-historical-research-compression-f95d721.json`](evidence/agent-first-historical-research-compression-f95d721.json). Live conditional ideas such as `ANC-COMPILER-002` retain only the current question, stronger baseline, falsifier, and exact evidence pointer.

The strategic adversarial-systems reorientation, source comparison, insertion map, and research program live in [`../studies/2026-agent-native-adversarial-systems/`](../studies/2026-agent-native-adversarial-systems/).

The execution-entity, lineage, propagation, organization, control, resilience, and adversarial-ecology synthesis lives in [`../studies/2026-execution-entity-adversarial-ecology/`](../studies/2026-execution-entity-adversarial-ecology/). It is a completed reference study consumed through `ANC-SECURITY-007`; it does not activate implementation or promote a shared entity protocol.

The expanded Game thesis, comparative source set, experience/infrastructure admission split, and bounded post-alpha falsification program live in [`../studies/2026-agent-native-game-worlds/`](../studies/2026-agent-native-game-worlds/). `ANC-GAME-001` remains the completed Host/Game ownership question; `ANC-GAME-002` is the deferred product-and-world question and must not displace the current Ready Frontier.

- [`../studies/2026-cross-project-convergence/`](../studies/2026-cross-project-convergence/) — completed revision-bound comparison of Computing, Runtime, Host, Harness, World, Security, Finance, Studio, Web, Human, and Game; derives cross-owner convergence laws, a two-timescale self-loop, and a Game negative-knowledge lineage finding without promoting new shared infrastructure.

The one-time [`HISTORICAL-DOCUMENT-AUDIT.md`](HISTORICAL-DOCUMENT-AUDIT.md) records the retain, merge, historical, archive, delete, and rewrite-summary decisions applied to high-impact historical documents. It is audit evidence and does not own portfolio status or architecture.

## Retrospective research-taste evidence

[`experiments/tm0-research-taste-audit/`](experiments/tm0-research-taste-audit/) records retrospective candidate priors for high-information research selection. It does not create a scheduler, score, or active phase; the canonical portfolio remains the only admission surface, and prospective calibration is still required before any reusable selection mechanism can graduate.

## Computer contraction implementation

The removal-first implementation is closed in [`evidence/computer-contraction-implementation-closeout.json`](evidence/computer-contraction-implementation-closeout.json). The removal-first Computer contraction remains closed and current responsibility authority is still the ten-item [`computer-responsibility-map-v2.json`](computer-responsibility-map-v2.json). `ANC-JOINT-001` has completed its initial owner-preserving Cross-Owner Joint Capability screening campaign and is now reference/dormant. Future reopen is natural-pressure-first under the four canonical gates, with `MatureBaselineResidual` including fair Generic Composition Subtraction; J0/J1/N1/Continuity are historical evidence rather than an active experiment queue.
