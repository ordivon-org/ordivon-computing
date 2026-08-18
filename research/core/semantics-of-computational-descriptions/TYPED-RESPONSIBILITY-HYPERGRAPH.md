# SCD Typed Responsibility Hypergraph

The canonical architectural model is a **typed responsibility hypergraph**.

It rejects a universal root Foundation and a universal linear prerequisite chain.

## Relation classes

- `conditionalDependency` — claim-local semantic reliance.
- `bridgeHyperedge` — relates multiple SCD and/or external responsibilities without merging owners.
- `reopenPropagation` — claim-scoped, asymmetric reopening triggered by a concrete invalidated dependency.

These relation classes are not interchangeable.

## Frozen boundary hyperedge

`SCDF2 ↔ SCDF5 ↔ SCDF10 Boundary Architecture v1`

This result must remain explicit as a hyperedge/boundary architecture rather than being hidden inside one Foundation or rewritten as a linear prerequisite chain.
