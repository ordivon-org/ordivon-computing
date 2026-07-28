# Ordivon Protocol

This distribution contains the smallest production-candidate primitives promoted from the executable experiments in `ordivon-computing`.

It owns:

- strict canonical JSON, content digests, and normative canonical vectors;
- public Effect envelopes, including repository-bound source changes;
- Tool contracts and change classification;
- immutable Effect bindings;
- normative JSON Schemas for those public wire objects;
- pure reference Effect/Dispatch state algebra and typed semantic identities.

It does **not** own a journal, Host loop, Runtime client, provider adapter, simulator, authority root, task scheduler, or verification policy.

## Stability boundary

| Module | Status | Rule |
|---|---|---|
| `anc_canonical` | normative core | canonical bytes, digest format, and vectors are protocol truth |
| `anc_protocol_types` | normative core | shared execution/completion enums; public modules re-export them |
| `anc_effect_ir` | normative core | backend-neutral Effect wire object |
| `anc_tool_contract` | normative core | normalized executable interface identity |
| `anc_effect_binding` | normative core | immutable Effect-to-contract binding |
| `ordivon_semantics` | reference candidate | retained for experiments; do not expand without a second production consumer |

The existing `anc_*` Python import names and `anc.*` serialized identities are preserved in v0 because they are already covered by cross-language conformance vectors. Renaming them would be a protocol migration, not a source-layout cleanup.

Normative Schemas and vectors ship inside the distribution under `ordivon_protocol`. Research fixtures, live scripts, benchmarks, and conformance campaigns remain under `research/experiments/` and consume those packaged resources rather than maintaining shadow copies.
