# S1-v2 Preflight Disposition

Status: **INVALID FOR ARM COMPARISON — conservative request-bound budget excluded the treatment before provider dispatch**.

`evidence-s1-v2-preflight.json` is retained. Both `CURRENT_BINDING_FRONTIER` trials stopped in 1–2 ms with:

- `modelCalls=0`;
- `providerAttempts=0`;
- `stopCode=budget_exhausted`.

The RAW_HISTORY trials did reach the provider. This is therefore not evidence of a cognitive/semantic treatment effect.

## Root cause

Harness correctly applies the DeepSeek adapter's conservative request preflight. The adapter's `request_token_upper_bound()` currently bounds **serialized request-body bytes + max output tokens**, not tokenizer-estimated tokens. S1-v2 froze `maxTotalTokens=10000`; the additional deterministic frontier pushed the provider request body above that conservative bound even though the user-visible prompt is only roughly 5–6 KiB and realized provider usage for RAW_HISTORY was about 2.4–2.7k tokens.

This creates an asymmetric admission artifact: one arm can reach the provider and the other cannot.

## Disposition

- Do not score v2 preflight as representation evidence.
- Do not change cases, semantics, schema, oracle, frontier, models, or treatments.
- Freeze S1-v3 with only one mechanical change: equal `maxTotalTokens=32768` for both arms, sufficient for the conservative serialized-request bound while preserving the same no-tool/model-call ceiling.
- Actual provider token use remains measured, so representation cost can still be reported from realized usage.
