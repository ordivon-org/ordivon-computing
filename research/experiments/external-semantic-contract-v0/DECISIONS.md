# Decisions

## E1 — One workspace, four logical packages

The components evolve together during research but retain import-level boundaries. Separate Git repositories are deferred until independent consumers or release cycles exist.

## E2 — Public canonical encoding is not the Journal codec

`anc-canonical-json-v1` has its own version, vectors, and implementation. Journal serialization remains an internal Kernel storage format.

## E3 — Effect identity is independent of Binding identity

Contract or argument changes create a new immutable Binding revision. They do not rewrite the Effect identity or any active Dispatch.

## E4 — Backend operation names belong to ToolContract

`workspace.exec` and `simulator.job.launch` may implement the same semantic action but never appear in `EffectEnvelope`.

## E5 — Unknown compatibility fails closed

The differ classifies only proven cases. Unsupported JSON Schema keywords or unproven semantic equivalence produce `UNKNOWN`.


## E6 — Public Effect and Kernel projection are not peers

`EffectEnvelope` is the public backend-neutral semantic record. `KernelEffectProjection` is a one-way internal projection used by Kernel v0. Historical `EffectSpec` records remain decodable through a non-exported compatibility alias; new Kernel state does not store a Provider operation.

## E7 — Complete Bindings remain outside Kernel state

Binding Authority verifies the signed Effect, ToolContract revision, arguments and digests, then stores the complete signed Binding by content address. Kernel state retains only `BindingAdmission`; the Binding digest is also the external resolution key. Missing, corrupt or forged Binding artifacts fail closed.

## E8 — A bound Dispatch must match the actual request

The Adapter request digest must equal the canonical digest of the resolved complete Binding arguments before `begin_dispatch`. Illustrative lowerers may demonstrate semantic portability, but only exact request Bindings may cross a real execution boundary.

## E9 — Live catalog capture, not a catalog service

The first Tool ABI slice reads the current MCP `tools/list`, normalizes execution-relevant schemas, and retains a reproducible snapshot. A long-running catalog service, automatic Provider selection and generalized interface registry remain deferred until a real consumer requires them.

## E10 — Defer Binding alternatives

Revision and supersedes continue to describe one selected Binding lineage. A separate candidate/alternative model is not implemented because there is no current workload selecting among multiple live Backend candidates for one Effect. The selected Binding alone crosses the Kernel edge.
