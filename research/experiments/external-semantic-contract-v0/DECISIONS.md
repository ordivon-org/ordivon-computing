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
