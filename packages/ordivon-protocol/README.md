# Ordivon Protocol

This distribution contains the smallest production-candidate primitives promoted from the executable experiments in `ordivon-computing`.

It owns:

- strict canonical JSON and content digests;
- public Effect envelopes;
- Tool contracts and change classification;
- immutable Effect bindings;
- pure Effect and Dispatch state algebra;
- typed semantic identities.

It does **not** own a journal, Host loop, Runtime client, provider adapter, simulator, authority root, task scheduler, or verification policy.

The existing `anc_*` Python import names and `anc.*` serialized identities are preserved in v0 because they are already covered by cross-language conformance vectors. Renaming them would be a protocol migration, not a source-layout cleanup.

Research fixtures, live scripts, benchmarks, and conformance tests remain under `research/experiments/`; production candidates live here and those experiments test this source directly.
