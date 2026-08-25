# S5B-B v1 Apparatus Closeout

Status: **INVALID FOR FORMAL ARM COMPARISON — provider account balance exhausted mid-campaign**.

## Evidence

The Flash campaign mechanically completed all 54 planned schedule slots, but only 25 produced valid structured semantic outcomes.

- candidate_completed: 25
- invalid_model_output: 2
- provider_rejected: 27

The missingness is sharply time-clustered:

- slots 1–18: 16 valid, 0 provider_rejected;
- slots 19–36: 9 valid, 9 provider_rejected;
- slots 37–54: 0 valid, 18 provider_rejected.

Provider rejection affected all three arms:

- RAW_PARTIAL_ORDER invalid: 10
- FORCED_LINEARIZATION invalid: 10
- BINDING_SET_PROJECTION invalid: 9

An independent non-experimental provider-health probe using the same configured DeepSeek account returned:

`HTTP 402 {"error":{"message":"Insufficient Balance", ...}}`

DeepSeek's current API documentation classifies HTTP 402 as insufficient balance. Harness source maps 429 and 5xx to `provider_unavailable`, whereas the campaign recorded `provider_rejected`; the direct probe therefore resolves the previously unknown rejection cause.

## Disposition

- Do not calculate the registered S5B-B arm effect from the 25 observed semantic rows.
- Do not treat the 29 invalid rows as semantic failures.
- Do not use complete-case arm rates as a causal comparison: missingness is temporally clustered and therefore not plausibly MCAR.
- Do not retry recorded v1 invalid slots or start the Pro v1 campaign under the exhausted account.
- Retain v1 semantic rows as exploratory diagnostics only.
- The earlier first preflight with concurrency leakage remains apparatus-invalid; the corrected second preflight established packet mechanics but is not formal evidence.

## Experimental-design repair

A successor v2 is frozen as a **balanced randomized-block design**. Time/provider state is treated as a nuisance factor. Each completed block contains all three representation arms for one `(case, model, replicate)` stratum in randomized order. A block is semantically analyzable only if all three arm calls are provider-valid. If any call is rejected/unavailable/transport-failed, the entire block is excluded from arm comparison and no remaining arm in that block is used as treatment evidence.

This prevents provider/account changes from selectively changing arm denominators. It does not make provider failures random or recover missing outcomes; it makes the comparison boundary explicit and balanced.
