---
schema_version: 1
id: computing.research.world-model-a10-time-scope
title: World Model A10 Time-Scope Experiment v0
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
summary: Security-grounded falsifier for time-scoped truth admission, testing raw owner/property/time provenance against an explicit query-relative temporal projection.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-security
  - ordivon-harness
related:
  - computing.research.world-model-loop
  - computing.foundations
---
# World Model A10 Time-Scope Experiment v0

## Claim

Core A10 says accepted truth is scoped to the property, owner, and time established by domain-authorized evidence. Historical evidence remains valid history without automatically proving current state.

This experiment tests a narrower implementation question: **are ordinary record role, property, authority, logical time, and later-event semantics sufficient for a capable Agent to make the right truth-admission decision, or does an explicit query-relative freshness/admission projection materially reduce errors?**

The experiment is a falsifier in both directions. Raw scoped evidence fails if the Agent repeatedly turns previously valid evidence into false current certainty. The explicit projection fails its admission burden if it adds no observable correctness benefit over raw scoped evidence.

## Setup

The experiment is Computing-owned and read-only with respect to Security and Harness.

- Computing base revision: `cadc0154a2fee54504b8fe680cc6751107c9ae57`.
- Security source revision: `ad24160ab0a3eaec7656ffd8f530a6a86ba55b75`, frozen in `security-wml-a10-source-20260809`.
- Harness equipment revision: `f09c3795fc811c5a564a5285cf227b2a44283cf5`, frozen in `harness-wml-a10-equipment-20260809`.
- Provider/model: the configured `deepseek-v4-flash` profile.
- Owner-native grounding: accepted C1-N downstream-truth-failure evidence, AE2 conflicting-observation evidence, and AE3-C evidence-reduction limits.
- No Range execution, network target, external cyber action, Security mutation, or financial effect occurs.

The eight cases balance four expected-UNKNOWN decisions and four expected-concrete decisions so a model cannot score well by always abstaining or always trusting the strongest-looking historical record.

## Procedure

For each case, two treatments expose the same underlying facts:

1. **RAW_SCOPED** — records carry only ordinary domain semantics: role, property, authority, logical time, value/observation, and outcome status.
2. **EXPLICIT_TEMPORAL_ADMISSION** — the same records additionally carry an experiment-local query-relative `temporalAdmission` projection saying whether that record is eligible to establish the queried property at the queried logical time.

No `stale` or `fresh` label appears in RAW_SCOPED. The prompt gives only the generic rule that current truth must be established by the supplied records for the queried property/time and that hidden outcomes must not be invented.

Two Provider replicates per treatment are declared before execution. Treatment order reverses on replicate 2. Every completed decision is saved independently; restart reuses matching completed records rather than replaying the whole campaign.

Primary metrics are exact answer accuracy, false certainty, false abstention, wrong concrete answer, and treatment separation. Token use is retained as apparatus evidence but is not the scientific target.

## Results

The experiment supports Core A10 while rejecting premature freshness standardization. It also invalidated one of its own counterfactual evaluator cases because Computing had assigned a unique answer that Security owner semantics had not established. The accepted interpretation, corrected scoring boundary, follow-up, and method implications are in [`RESULTS.md`](RESULTS.md).

## Limitations

- This is a bounded truth-admission workload, not a general benchmark of model epistemic behavior.
- The explicit temporal projection is experiment-local; success would not by itself decide its architectural owner or schema.
- Counterfactual hidden worlds are evaluator-only devices grounded in Security's accepted UNKNOWN methodology; they are not claims that Security physically executed C1-O freshness.
- Two replicates can expose existence, stability, and failure cases but cannot establish population-level model reliability.
- The experiment does not test malicious timestamp forgery, distributed clock semantics, multi-writer ordering, or atomic witness publication.
- It does not authorize hostile-code execution or any external target action.

## Artifacts

- [`run.py`](run.py) — live Provider runner with durable progress records and deterministic evaluator.
- `RESULTS.md` — created after accepted execution.
- machine receipts under `../../evidence/` — created after accepted execution.
