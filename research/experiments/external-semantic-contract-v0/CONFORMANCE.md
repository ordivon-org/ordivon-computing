# External Semantic Contract v0 Conformance

## Local gates

```bash
PYTHONPATH=src:../semantic-core-v0/src:. python3.12 -m unittest discover -s tests -v
ruff check src integration tests scripts
rustc --edition=2021 rust/canonical-verifier/main.rs -o /tmp/anc-canonical-verifier
/tmp/anc-canonical-verifier fixtures/canonical/canonical-vectors.tsv
```

## Evidence matrix

| Boundary | Executable evidence |
|---|---|
| canonical bytes/digest | golden vectors, duplicate-key and number rejection |
| EffectEnvelope | strict round trip, digest identity, forbidden Backend names |
| ToolContract | presentation stripping, schema tightening, semantic break and unknown keyword |
| EffectBinding | same Effect across two contracts, immutable revisions, digest separation |
| dependency direction | AST import guard and Kernel no-import guard |
| Kernel edge | Binding Authority, revision history, exact Dispatch reference, Journal v2/v3 migration |
| dual Backend lowering | one mutation Envelope succeeds through Ordivon and simulator |
| knowledge admission | bound mutation → independent read → Verification → Fact |
| response loss | one launch Envelope recovers original bound Dispatch through both Backends |
| contract drift | pending rebind; UNKNOWN observe-original; no new delivery |

Exact implementation and live evidence are recorded under `evidence/` after the implementation revision is frozen.
