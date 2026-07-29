# 05 — Edge/Link Boundary and Composition

## Independent responsibilities

```text
Edge: which body or external provider executes the work?
Link: which logical relation, path, endpoint, and identity realize communication?
```

Changing one does not necessarily change the other.

- A local Runtime may change from direct access to VPN without body replacement.
- A Task may move from local Runtime to remote Browser using ordinary provider
  networking without Link-owned path selection.
- One Edge body may use several paths and target identities.
- One path may connect several bodies, services, and participants.

## Replacement alternatives

When a local path fails, Host may:

1. keep the body and select a new path through Link;
2. keep the logical relation and move the execution through Edge;
3. change communication form to an asynchronous Artifact handoff;
4. replace the participant with an explicit handoff.

Host owns the Task-level choice. Edge and Link provide candidates, bindings,
and evidence.

## Minimal composition hypothesis

The first useful composition should be references, not shared lifecycle:

- Placement Binding reference;
- zero or more Connectivity Binding references;
- exact independent revisions;
- shared Task/Attempt/Effect references;
- evidence dependency and invalidation edges;
- separate residual closure.

A Link attachment must not create or destroy an Edge body. An Edge placement
must not own routes or communication identity.

## Repository decision

Conceptual grouping as World Interfaces is useful. Physical repository merger
is unjustified until real consumers show synchronized state, release, privilege,
and failure domains. Security composition alone is insufficient because the
current acceptance explicitly lacks a persistent Edge-to-Link data plane.
