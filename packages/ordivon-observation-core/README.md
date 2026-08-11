# Ordivon Observation Core

`ordivon-observation-core` is the promoted minimum implementation behind the
shared owner-native Observation responsibility.

It is deliberately **not** an Observation service or source of product truth.
Host, Harness, Runtime, World, and domain owners remain authoritative for their
own state. This package only supplies deterministic metadata contracts,
checkpointed export bundles, a rebuildable SQLite query projection, and
selection manifests that bind exact owner-native identities.

The package exists because three materially different current owner exporters
(`ordivon-host`, `ordivon-harness`, and `ordivon-runtime`) consume the same
contract. The earlier implementation lived under the Observation Plane
experiment and was contracted with the rest of that apparatus; P0 RSI-lab
dogfood showed the current exporters then failed with
`ModuleNotFoundError: ordivon_observation_core`. Promotion restores the earned
shared mechanism without restoring a daemon, writable authority plane, or
continuous collection policy.

## Boundary

- owner state is never written;
- raw private payload bytes are not required by the metadata contract;
- Gateway state is disposable and rebuildable from export bundles;
- Selection is evidence binding, not Trial validity or semantic completion;
- no importance, priority, topology, or research-policy classification is
  produced;
- continuous telemetry should inherit mature OpenTelemetry/system tooling when
  a real workload requires it.

## Promotion contraction

The historical experiment also generated standalone JSON Schema builders and
schema copies. P0 did not promote those files because the current owner
exporters, Gateway, Selection, and EvidencePack do not consume them. Historical
schema evidence remains in the contracted Observation Plane record. A schema
surface can return only after a current package/API consumer proves it reduces
real contract friction.
