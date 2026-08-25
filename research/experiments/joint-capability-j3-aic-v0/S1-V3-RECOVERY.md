# S1-v3 Recovery Record

The original 80-slot campaign Job `job-01a03709-497c-7983-83cc-b1ddcfbad4eb` terminated mechanically as `lost` with reason `SUPERVISOR_EVIDENCE_LOST` after the conversation/runtime connection failed. The campaign writes its evidence file after every completed slot, so `evidence-s1-v3-live.json` is the durable semantic campaign record rather than the lost Job terminal state.

Recovery inspection found exactly 71 unique scheduled slots present in that file. Nine schedule slots were absent and therefore had never been recorded. Recovery is restricted to those absent tuple identities `(scenarioId, treatment, model, replicate)` under the already frozen v3 semantics, models, budgets, schema, oracle and schedule seed.

Rules:

- Do not rerun any of the 71 recorded slots, including invalid provider/model outputs.
- Do not convert invalid trials into retries; they remain invalid apparatus/provider outcomes in the planned denominator and are excluded only from semantic denominators according to `v3-analysis-plan.json`.
- Run only missing schedule slots with the unchanged `aic_agent_run_v3.run_one()` implementation.
- Preserve all original rows verbatim and append recovered missing rows.
- Recompute campaign summary only from the combined 80-row record.
- This is continuity recovery, not an additional replicate campaign and not post-outcome tuning.
