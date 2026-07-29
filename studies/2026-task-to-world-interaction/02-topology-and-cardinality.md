# 02 — Topology, Cardinality, and Data Movement

## Directions

### Local to remote

API calls, Browser execution, Sandbox work, cloud deployment, data query,
Agent delegation and device control.

### Remote to local

Webhook, callback, stream, notification, human approval, result delivery and
renewed credential request.

### Remote to remote

Sandbox to object store, storage to GPU provider, one Agent to another Agent,
provider chaining and external verification.

## Cardinality

- one Task → many interactions;
- one Effect → several reconciled Dispatches;
- one interaction → several communication sessions and provider operations;
- one provider execution → many external relations and Artifacts;
- one path → many interactions;
- one Artifact → many later consumers;
- many interactions → one Task join;
- many Tasks → shared provider account or transport pool without shared semantic
  identity.

## Control versus data

Ordivon should control and evidence the graph without carrying every byte:

```text
Host → intent and authority → provider A
provider A → Artifact bytes → object store / provider B
provider B → result bytes → retained external storage
Host ← Receipt, digest, provenance and verification references
```

Central proxying is justified only when the Task requires inspection,
transformation, policy enforcement, or local custody.

## Graph consequences

A linear `request → response` model cannot express callbacks, streaming,
fan-out, join, direct transfer, participant handoff, or delayed reconciliation.
The research should use explicit edges and independently revisioned bindings,
not one universal session or Node identity.
