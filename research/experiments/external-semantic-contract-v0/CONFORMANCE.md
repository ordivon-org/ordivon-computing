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

Exact implementation revision: `2f4d7ca8db6756b8add3356db52dcd237ed7a256`

Evidence:

- [`evidence/external-contract-2f4d7ca.json`](evidence/external-contract-2f4d7ca.json) — 29-test report, canonical and schema metrics, Effect/Contract/Binding digests, drift decisions, and direct-call comparison;
- [`evidence/live-ordivon-2f4d7ca.json`](evidence/live-ordivon-2f4d7ca.json) — exact live Journal restart and versioned file paths;
- [`../semantic-core-v0/benchmark-results/binding-edge-2f4d7ca.json`](../semantic-core-v0/benchmark-results/binding-edge-2f4d7ca.json) — exact post-Binding-edge performance.

Key deterministic values:

```text
external tests: 29 / 29
canonical vectors: 5, Python = Rust
Effect canonical bytes: 854
Ordivon mutation contract bytes: 1,149
simulator mutation contract bytes: 921
Backend operation names in EffectEnvelope: false
same Effect digest across two Bindings: true
distinct contract and argument digests: true
schemaVersion tightening: CALLER_ADAPTATION
PREPARED decision: REBIND
RUNNING / UNKNOWN decision: OBSERVE_ORIGINAL
SUCCEEDED decision: KEEP
```

The direct-call comparison records that an ad hoc Tool call has none of stable Effect identity, explicit contract digest, immutable Binding revision, UNKNOWN reconciliation identity, or Fact admission by itself; the external contract path provides all five through composition with the Kernel.
