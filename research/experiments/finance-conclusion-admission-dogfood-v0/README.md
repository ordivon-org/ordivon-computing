---
schema_version: 1
id: computing.research.finance-conclusion-admission-dogfood-v0
title: Finance Conclusion Admission Dogfood v0
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
summary: Real-domain dogfood of Harness conclusion rejection against Finance C2 execution.request.prepare and execution admission without external financial writes.
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
# Finance Conclusion Admission Dogfood v0

## Claim

The existing Harness `validate_conclusion` hook should be able to host a **real Finance-owned admission law** without Harness learning Finance semantics. A schema-valid Agent-selected `ExecutionOrderIntent v0` may still be inadmissible under current Proposal, authority, market-basis, notional, lot, tick, daily-reservation, or risk-effect constraints. Finance should remain the authority that decides this through its existing deterministic `execution.request.prepare@1` / execution evaluation chain.

The experiment also tests two suspected Harness ergonomics problems that only become visible once a non-evidence domain rejection uses the hook:

```text
Finance semantic rejection
→ is the model told "missing evidence" even when evidence is not missing?

Finance conclusion rejection
→ does it consume the Tool-correction budget even though no Tool call was wrong?
```

## Setup

- Computing base revision: `d857cb24eda9d2fa9f04f111d51dd8cab5d2a4e2`.
- Finance source revision: `6e810f7d3022913e26386509945365ef358e0cfe`.
- Harness source revision: `ca752057926426a4f49e6f9d03ce868f48ea49ee`.
- Finance C2 committed owner-native/delegated authority fixture supplies the real `ExecutionKernel`, Owner Constitution, Proposal/Decision binding, market basis, and delegated-lease semantics.
- The structured result schema is derived from Finance's committed `ordivon.finance.execution-order-intent.v0` schema. Mechanical execution identity remains Finance-owned.
- The live Provider profile is `deepseek-v4-flash`.
- No venue adapter, dispatch claim, authenticated order submission, fill, or real capital movement is available to the experiment.
- One pair of cases uses local fixture-only `execution.reserve` state to create real delegated daily-budget pressure. Those reservations remain inside disposable temporary Finance databases and are never dispatched.

## Treatments

1. **SCHEMA_ONLY** — the candidate runs through the normal Harness Agent loop and structured completion codec, but no domain conclusion validator is installed. After the Run, Computing asks Finance `prepare_request_v2` only to score whether the submitted intent was admissible.
2. **FINANCE_ADMISSION_GATE** — the same Harness loop installs a domain bridge whose `validate_conclusion` decodes the exact structured intent and calls Finance `prepare_request_v2`. Finance rejection is returned as `MODEL_CORRECTABLE`; Harness may then give the same Agent another bounded turn.

Both treatments use the same prompt, Finance state, schema, model and Run budget. Every treatment/replicate gets a fresh disposable Finance fixture.

## Domain cases

Eight predeclared cases exercise current Finance C2 semantics rather than an experiment-invented truth oracle:

- owner-native baseline;
- delegated max-order cap arithmetic;
- delegated remaining daily-budget arithmetic after a local reserved effect;
- market lot/tick shape;
- missing delegated-authority decoy versus current Owner Constitution;
- venue without a matching current market basis;
- `reduceOnly` semantics for an `act → increase` Decision;
- delegated composite daily-budget arithmetic at a non-round price.

The domain gate checks **admission only**. A separately scored task objective may be stricter, such as choosing the largest admissible size. This distinction is deliberate:

```text
Finance admission
!=
Agent task optimality
```

## Procedure

Before any live Provider call, a deterministic real-domain boundary probe uses canned Provider responses:

1. Finance delegated authority is capped at 60 USD.
2. A schema-valid intent with `sz=13`, `px=500`, and `ctVal=0.01` has 65 USD notional and must be rejected by Finance.
3. `sz=12` has 60 USD notional and must be accepted.
4. The real Harness correction loop is exercised with the Finance-owned gate.
5. A zero `max_tool_corrections` budget is separately tested to identify whether conclusion correction is coupled to Tool correction.

The live campaign then runs eight cases × two treatments × two predeclared Provider replicates. Treatment order reverses on replicate two. Completed decisions are saved independently so a transport failure does not erase prior counted observations. Provider transport attempts that terminate without a candidate decision are retained separately and excluded from the decision count; the logical slot is retried with a new Harness Run identity because no external financial effect is available.

The first live runner candidate was rejected before scientific acceptance because it accidentally placed the evaluator's expected answer under `referenceExpectedForExperimentScoring` inside Agent-visible `financeState`. Its four completed decisions and one subsequent `provider_state_unknown` attempt are retained as excluded apparatus evidence in [`../../evidence/finance-conclusion-admission-dogfood-excluded-bbb85ea8ca8f.json`](../../evidence/finance-conclusion-admission-dogfood-excluded-bbb85ea8ca8f.json). Protocol revision 2 removes that field entirely and restarts the scientific campaign from zero.

## Limitations

- The Finance state is a disposable committed-domain fixture, not the user's live portfolio/account. This avoids transmitting private live account state to the Provider while still exercising current Finance owner semantics.
- The experiment proves only the pre-reservation admission boundary. It does not attempt or authorize a venue write.
- A Finance-admitted order may still be a poor task choice; admission is not optimization.
- Two Provider replicates can expose concrete failure/correction behavior but do not estimate a population error rate.
- The experiment does not assert that every Finance structured result should use a conclusion gate. It tests one consequence-bearing boundary where an existing executable owner law already exists.

## Artifacts

- [`run.py`](run.py) — deterministic Finance/Harness boundary probe and live campaign runner.
- `RESULTS.md` — created after accepted execution.
- machine evidence under `../../evidence/` — created after accepted execution.

## Results

Protocol revision 2 completed 32 counted slots. SCHEMA_ONLY produced 16 structured decisions, of which 11 were Finance-admitted. FINANCE_ADMISSION_GATE produced 14 consumable structured decisions and 14 Finance-admitted outcomes; one natural max-order Run corrected from an inadmissible size 13 to admissible size 12, while another exhausted the current correction budget. See [`RESULTS.md`](RESULTS.md).
