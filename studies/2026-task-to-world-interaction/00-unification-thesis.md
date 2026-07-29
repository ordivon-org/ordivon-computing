# 00 — Why Edge and Link Converge

## Intermediate decomposition

The earlier model separated:

```text
Edge: where and through which external body does an Effect execute?
Link: which logical relation, identity, and path realize communication?
```

This was useful for preventing reimplementation of Sandboxes and network stacks.
It became harmful as a top-level repository boundary.

## Causal loop

```text
intended Effect or relation
↔ target, path, identity, transport, locality and session needs
↔ provider capability and execution position
↔ actual delivery and world change
↔ Receipt, Artifact and Observation
↔ uncertainty, invalidation and next Task action
```

Examples:

- Browser execution creates a second network path from provider to website.
- Creating a Sandbox returns a new endpoint and identity required for later work.
- A provider timeout may hide successful execution and committed Artifacts.
- Switching region or path may change the page that the browser observes.
- A callback is both an inbound relation and completion of remote work.
- Direct provider-to-storage transfer is both data movement and Effect evidence.

## Structural cost of separation

Separate top-level projects produced pressure for:

- Edge-to-Link attachments;
- shared Node/World identity;
- duplicate lease, generation, residual and reconciliation models;
- conflicting recovery when path and provider fail together;
- cross-repository protocols before a second consumer existed.

A unified repository removes the organizational source of those abstractions.
Connectivity and action remain separately observable and versioned, but their
Task-level correlation evolves inside one research object.

## New object

A **World Interaction** is one Task-conditioned external relation and/or action
with exact semantic, authority, target, path, identity, transport, provider,
execution, evidence, uncertainty, and continuity references.

It is not necessarily one stored object. The research must determine whether
ordinary foreign references and a correlated graph are sufficient.
