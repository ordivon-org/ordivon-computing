---
schema_version: 1
id: computing.research.structured-commitment-consistency-v0
title: Structured Commitment Consistency Experiment v0
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
summary: Falsifier separating schema validity, semantic cross-field consistency, and owner-native truth admission at the Harness structured conclusion boundary.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-harness
related:
  - computing.research.world-model-loop
---
# Structured Commitment Consistency Experiment v0

## Claim

A schema-valid structured conclusion is not necessarily semantically admissible. A prior A10 campaign produced a structured `answer` of `2` while its own explanatory `reason` explicitly concluded that the answer should be `unknown`. This experiment tests whether the existing caller/domain conclusion gate is sufficient to separate schema validity, semantic consistency, and owner truth admission before downstream commitment.

Harness already states that `structured-result-v1` is a caller-owned codec and that caller/domain semantic verification remains mandatory. The Agent loop also exposes an optional `validate_conclusion` gate that can reject a model-correctable candidate before terminal completion.

The experiment therefore tests three distinct layers rather than assuming Harness should become a generic truth verifier.

## Setup

- Computing base revision: `04471010e0cbb1d04e8b5647204b60d090149067`.
- Harness source revision: `ca752057926426a4f49e6f9d03ce868f48ea49ee`, frozen in `harness-structured-commitment-source-20260809`.
- Harness `structured-result-v1` remains a caller-owned codec; no Harness semantic authority is added.
- The live Provider profile is configured `deepseek-v4-flash`.
- The synthetic owner law and commitment mapping are declared before execution and are machine-checkable.
- No Runtime Tool, Host mutation, domain effect, or external world action is available to the Agent.

## Layers

1. **SCHEMA_ONLY** — the Provider result must satisfy the caller JSON schema. No cross-field semantic admission runs.
2. **CONSISTENCY_GATE** — a domain-owned conclusion gate requires `evidenceVerdict` and `commitment` to obey the declared mapping, but does not decide whether the verdict itself is true.
3. **OWNER_ADMISSION_GATE** — the domain owner deterministically re-evaluates the supplied owner records for the exact query, then checks both verdict truth and commitment consistency.

The completion result contains:

```text
evidenceVerdict = proven-a | proven-b | unknown
commitment      = commit-a | commit-b | abstain
basisRecordIds
reason
```

The owner commitment law is:

```text
proven-a → commit-a
proven-b → commit-b
unknown  → abstain
```

The JSON schema deliberately permits all nine verdict/commitment combinations. Therefore schema validity does not encode the semantic law.

## Owner oracle

The synthetic test domain is intentionally narrow and machine-checkable. For one exact query, only an `authoritative-current-state` record bound to that exact `queryId` establishes `A` or `B`. Historical state, priors, sensors, conditional effects, failed observations, operator preference, and other-property records are non-state-establishing for that query. If no exact authoritative current-state record exists, the owner verdict is `unknown`.

This oracle is part of the experiment contract; Computing is not inferring an unstated domain rule after observing model output.

## Procedure

The runner first performs a deterministic injected boundary test using the real DeepSeek structured-result parser with canned Provider responses:

- schema-only accepts one schema-valid but semantically inconsistent result;
- the real `OrdivonAgentLoop` plus a consistency gate rejects that result and accepts a corrected second conclusion.

It then executes eight live cases under all three treatments with two predeclared Provider replicates. Treatment order reverses on replicate 2. Completed case/treatment/replicate results are saved independently.

No Runtime Tool, Host mutation, domain effect, or external world action occurs.

## Interpretation boundary

A free-form rationale is not treated as a second source of truth and no hidden chain of thought is required. If a semantic relation matters for admission, the experiment encodes that relation in explicit structured fields or recomputes it from owner-native evidence.

A consistency gate can prove only that submitted fields agree. It cannot make a wrong but internally consistent verdict true. Owner admission remains a separate authority.

## Results

The deterministic boundary falsifier proves that schema-valid structured output may still violate a caller/domain semantic relation and that the existing Harness conclusion gate can reject and correct it. In the 48 counted live decisions, all three treatments were 16/16 on truth, commitment and cross-field consistency with zero natural correction turns. This supports the existing Harness boundary rather than a new global semantic verifier. See [`RESULTS.md`](RESULTS.md).

## Limitations

- The synthetic owner oracle is deliberately narrow; it proves the conclusion-boundary mechanism, not a universal domain verifier.
- Cross-field consistency does not imply truth. A wrong verdict and matching wrong commitment can pass `CONSISTENCY_GATE`.
- `OWNER_ADMISSION_GATE` is possible only where the owner has a deterministic admission law or independently authoritative evidence.
- Free-form rationale remains explanatory content and is not treated as hidden reasoning authority.
- Two Provider replicates expose failure existence and correction behavior but do not estimate population-level model reliability.

## Artifacts

- [`run.py`](run.py) — deterministic boundary falsifier plus live three-treatment campaign with per-decision progress retention.
- `RESULTS.md` — created after accepted execution.
- machine receipts under `../../evidence/` — created after accepted execution.
