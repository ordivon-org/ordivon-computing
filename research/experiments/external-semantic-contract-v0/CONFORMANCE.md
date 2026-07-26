# External Semantic Contract v0 conformance

## Local deterministic gate

```bash
PYTHONPATH=src:../semantic-core-v0/src:. python3.12 -m unittest discover -s tests
ruff check src integration tests scripts
rustc --edition=2021 rust/canonical-verifier/main.rs -o /tmp/anc-canonical-verifier
/tmp/anc-canonical-verifier fixtures/canonical/canonical-vectors.tsv
```

## Boundary matrix

| Boundary | Executable evidence |
|---|---|
| canonical bytes and digest | golden vectors; duplicate-key, float and nonfinite-number rejection |
| public `EffectEnvelope` | strict round trip, digest identity, backend-operation absence |
| Kernel-local projection | one-way Envelope projection; provider operation not stored in new Kernel state |
| live `ToolContract` | MCP `tools/list` normalization and checked-in catalog snapshot |
| complete signed Binding | Effect and Binding Authority verification plus content-addressed resolution |
| exact request binding | Adapter request digest must equal admitted complete Binding arguments |
| Kernel edge | revision history, exact Dispatch reference, Journal compatibility |
| dual Backend execution | exact request bindings for Ordivon and simulator trajectories |
| knowledge admission | bound mutation → independent read → Verification → Fact |
| response loss | original bound Dispatch recovered without redelivery |
| contract drift | pending rebind; active or UNKNOWN observe-original |
| dependency direction | Kernel source imports no external-contract package |

## Heavy evidence policy

Real Ordivon execution, process restart, benchmarks, catalog capture and receipt regeneration are manual T3 evidence. They are not ordinary pull-request CI. Commands and immutable receipts are indexed in [`EVIDENCE.md`](EVIDENCE.md).
