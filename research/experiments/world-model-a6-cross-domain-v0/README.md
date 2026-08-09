---
schema_version: 1
id: computing.research.world-model-a6-cross-domain
title: World Model A6 Cross-Domain Experiment v0
type: experiment
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
updated: 2026-08-09
summary: Falsifiable Finance re-test of Core A6 source-state, selected-view, and selection-authority separation.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-finance
  - ordivon-harness
related:
  - computing.research.world-model-loop
  - computing.foundations
---
# World Model A6 Cross-Domain Experiment v0

## Claim

Core A6 predicts that `source state != selected view != selection authority` is not merely a Harness implementation detail. In a materially different Finance workload, letting the Agent choose a task-relevant model-visible slice should avoid errors from one static caller selection rule and should reduce irrelevant domain-source exposure as the available source world grows.

The claim is weakened if Agent selection fails to preserve answer correctness or if its selection cost does not become competitive as irrelevant source content grows. The experiment does not assume that a separate selection-only Model Call is the correct implementation.

## Setup

The experiment binds exact owner revisions and performs no Finance mutation:

- Finance revision: `ef3739d774037298af66a325f6a3314b92aefa8b`;
- Harness revision: `487e0ac8eb945256842347b5371cbbdd70bfce55`;
- model: `deepseek-v4-flash`;
- base Finance sources: `research/economic/spy-economic-case-v0.json` and `research/economic/spy-q2-earnings-progress-2026-08-05.json`;
- scale distractors: the largest exact Git-bound Finance schema JSON files;
- no Finance state mutation, venue call, capital action, or product patch is allowed.

The base source pool is split into six exact source units: five evidence items from the SPY case plus the later Q2 refresh, including its case-level completeness metadata.

## Procedure

The calibration compares three treatments over the same tasks, answer enum, source-state pool, model family, and deterministic evaluator:

1. **FULL** — caller exposes all source contents to the answering Agent.
2. **LATEST** — caller applies a fixed latest-observation heuristic and exposes only the newest Q2 refresh.
3. **AGENT** — Agent first receives a value-free source catalog containing identities, timestamps, field names, and provenance labels; it selects at most two exact sources, then answers from only those contents.

The scale sweep retains FULL and AGENT, keeps three representative tasks, and adds `0 / 2 / 4 / 8` real Finance schema sources as unrelated domain material. Each completed selection or answer is saved independently so a later Provider failure cannot erase prior campaign evidence.

Calibration validates the apparatus before scale interpretation. The scale sweep then asks whether the fixed selection cost remains larger than FULL-context cost or whether the relation reverses as the available source world grows.

## Results

The accepted calibration and scale sweep support A6 across the Finance workload while rejecting the experiment apparatus as a universal implementation. FULL and AGENT preserved all evaluated answers; a static latest-only caller rule failed half of calibration tasks. Agent selection was more token-expensive at the smallest pool, then became materially cheaper once unrelated real Finance schema content increased. A restart from saved progress also preserved completed campaign observations across a transient Provider disconnect.

See [`RESULTS.md`](RESULTS.md) and the machine acceptance record listed under Artifacts for exact metrics, negative conclusions, and return questions.

## Limitations

- The observed crossover is workload-specific; source size, model, Provider cache behavior, catalog representation, and task shape all affect it.
- AGENT uses two serial Model Calls per task in this apparatus, so lower token count does not establish lower wall-clock latency.
- The experiment evaluates bounded factual/semantic Finance questions, not open-ended portfolio research quality.
- Git-bound Finance research and schema sources are used for scaling; private live portfolio/account context is deliberately excluded.
- Direct Adapter calls do not provide durable exactly-once Provider continuation. Campaign progress records preserve completed observations, while an in-flight read-only Model Call may be repeated after a transport failure.
- The experiment does not authorize investment decisions or external financial effects.

## Artifacts

- [`run.py`](run.py) — calibration runner.
- [`run_scale.py`](run_scale.py) — scale-sweep runner with durable progress records.
- [`RESULTS.md`](RESULTS.md) — accepted interpretation, limits, and return questions.
- [`../../evidence/wml-a6-finance-selection-r0-44a2c762c8b4.json`](../../evidence/wml-a6-finance-selection-r0-44a2c762c8b4.json) — calibration receipt.
- [`../../evidence/wml-a6-finance-scale-r1-a6f3c3f1ec63.json`](../../evidence/wml-a6-finance-scale-r1-a6f3c3f1ec63.json) — recovered scale receipt.
- [`../../evidence/wml-a6-finance-cross-domain-acceptance-e74ef72fb5a8.json`](../../evidence/wml-a6-finance-cross-domain-acceptance-e74ef72fb5a8.json) — machine acceptance record.
