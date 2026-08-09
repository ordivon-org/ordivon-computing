---
schema_version: 1
id: computing.research.finance-conclusion-admission-dogfood-results
title: Finance Conclusion Admission Dogfood Results
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
updated: 2026-08-09
summary: Real-domain result showing Finance-owned conclusion admission can reject schema-valid execution intent and sometimes correct it, while exposing Harness correction wording, budget and terminal-structure friction.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-finance
  - ordivon-harness
related:
  - computing.research.structured-commitment-consistency-results
  - computing.research.world-model-loop
---
# Finance Conclusion Admission Dogfood Results

Machine acceptance: [`../../evidence/finance-conclusion-admission-dogfood-acceptance-641dcc3ab614.json`](../../evidence/finance-conclusion-admission-dogfood-acceptance-641dcc3ab614.json). Accepted protocol-v2 raw receipt: [`../../evidence/finance-conclusion-admission-dogfood-1f4ef0de7a65.json`](../../evidence/finance-conclusion-admission-dogfood-1f4ef0de7a65.json). Excluded protocol-v1 apparatus evidence: [`../../evidence/finance-conclusion-admission-dogfood-excluded-bbb85ea8ca8f.json`](../../evidence/finance-conclusion-admission-dogfood-excluded-bbb85ea8ca8f.json).

## Result

A real Finance consequence boundary confirms the earlier synthetic distinction:

```text
JSON/schema validity
!=
Finance execution admission
!=
Agent task optimality
!=
external effect authority
```

The existing Harness `validate_conclusion` hook can host Finance-owned admission without teaching Harness Finance semantics. The dogfood also exposes two established Harness correction problems and one additional structured-terminal pressure that requires a deterministic reproduction before patching.

## Observed aggregate

| Treatment | Slots | Structured decision | Finance admitted | Objective satisfied | Runs with correction | Model calls |
|---|---:|---:|---:|---:|---:|---:|
| SCHEMA_ONLY | 16 | 16 | 11 | 9 | 0 | 16 |
| FINANCE_ADMISSION_GATE | 16 | 14 | 14 | 10 | 2 | 19 |

The observed admission difference, 14/16 versus 11/16, is descriptive rather than a clean causal estimate because the two treatments used independent stochastic Provider calls. The stronger evidence is the within-Run correction trajectory below.

## Natural schema-valid Finance failures

SCHEMA_ONLY naturally submitted Finance-denied candidates in real domain cases. Examples include:

- delegated max-order: `sz=13`, `px=500.00`, with `ctVal=0.01` under a 60 USD delegated limit; Finance rejected both max-order and daily-budget authority;
- delegated daily headroom: a preferred `sz=5` exceeded remaining daily authority after a prior local reservation;
- market lot/tick shape: `sz=0.5`, `px=500.005` satisfied the structured string schema but violated Finance `minSz/lotSz/tickSz` economics.

Therefore the structured schema is doing the correct narrow job: representing the Agent-selected economic intent. Finance remains the authority for whether that intent can enter the execution chain.

## Causal correction evidence

The second delegated max-order gated replicate produced this exact trajectory inside one Harness Run:

```text
candidate 1: sz=13 → Finance denied
candidate 2: sz=13 → Finance denied
candidate 3: sz=12 → Finance admitted
```

The final intent also satisfied the experiment objective. This is direct evidence that owner-native conclusion admission can materially improve the same Agent's downstream commitment before effect reservation.

The first replicate did not converge:

```text
candidate 1: sz=13  → denied
candidate 2: sz=13  → denied
candidate 3: sz=120 → denied
→ invalid_model_output after correction budget exhaustion
```

So the admission hook has real value, but correction is not guaranteed merely because the owner can explain rejection.

## Harness friction 1: rejection wording is over-specialized

For a Finance authority/notional violation, Harness currently tells the Agent:

```text
candidate conclusion as incomplete
correct the missing evidence
```

No evidence was missing. The candidate violated current delegated authority. This wording appeared in the deterministic probe and in both live correction Runs.

The shared mechanism should communicate the **owner's rejection reason** without guessing that every rejection means incompleteness or missing evidence.

## Harness friction 2: conclusion correction is counted as Tool correction

The experiment had `toolCalls=0`, yet gated correction reported four `toolCorrections`. A deterministic zero-Tool-correction budget immediately changed the same Finance rejection into:

```text
invalid_model_output
Conclusion correction budget exhausted after local rejection
```

The live max-order first replicate also exhausted the current budget after two conclusion corrections.

This exposes a real collapsed distinction:

```text
Tool-call correction
!=
conclusion correction
```

The next Harness patch should give conclusion correction explicit accounting and budget authority rather than consuming `max_tool_corrections`.

## Finance admission is not task optimality

Several intents were valid Finance commitments but not the experiment's requested optimum. For example, after 40 USD was already locally reserved from a 60 USD daily delegated budget, the gated Agent chose admissible sizes 3 and 2 rather than the maximum admissible size 4 in two replicates.

Finance correctly accepted those intents. It should not become an optimizer merely because it owns execution admission.

```text
owner says "allowed"
!=
Task says "best"
```

This distinction prevents an effect-safety gate from silently acquiring Task or Purpose authority.

## Structured terminal pressure

One `market-lot-tick-shape / FINANCE_ADMISSION_GATE / r2` Run returned a non-null Harness conclusion that the bound Finance structured decoder could not consume. The old scorer raised `JSONDecodeError` before persisting the exact conclusion summary, stop code and usage. The slot is conservatively counted as a structured-decision failure and was **not** resampled.

Source audit shows that the Agent loop contains at least one plain-text fallback `AgentRunConclusion`, while structured completion binding is validated at Adapter/Contract setup rather than globally on every terminal conclusion. That makes terminal structured decodability a legitimate pressure, but the exact live path is unknown. A deterministic reproduction is required before changing fallback semantics.

## Excluded protocol-v1 run

The first campaign candidate accidentally included `referenceExpectedForExperimentScoring` inside Agent-visible `financeState`. Its four completed decisions are scientifically invalid regardless of answer quality. A subsequent Provider attempt ended `provider_state_unknown` without a saved decision.

All five observations are preserved in excluded evidence and contribute nothing to accepted statistics. Protocol revision 2 removed the leaked field and restarted from zero. This is an evaluator-boundary correction, not data cleaning after seeing bad accuracy.

## Safety and consequence boundary

No live portfolio or account state was sent to the Provider. No venue adapter was invoked. No dispatch claim was attempted. No external financial write occurred.

Eight treatment slots used a disposable local Finance fixture with one pre-reserved local effect to create real daily-budget state. Every decision compared the Finance snapshot before and after the model/gate path; dispatch claims remained zero. The accepted experiment stops before external effect authority.

## Disposition

### Finance

No Finance core patch is justified. `execution.request.prepare@1` did exactly what the architecture requires:

```text
Agent-selected economic intent
→ Finance mechanical lowering
→ Finance current admission
```

It remained read-only during conclusion validation.

### Harness

Two focused changes are now evidence-backed:

1. separate conclusion-correction accounting/budget from Tool-call correction;
2. make conclusion rejection feedback reason-neutral and preserve the caller/domain rejection reason.

A third candidate—structured terminal fallback enforcement—remains research pressure until deterministically reproduced.

### Shared world model

No Core rewrite is needed. The experiment strengthens the existing boundary with a consequential domain:

```text
structural validity
!=
owner admission
!=
task optimality
!=
effect authority
```

The next useful action is a focused Harness patch and acceptance against this Finance boundary, not another broad benchmark.
