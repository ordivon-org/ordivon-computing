# Initial Architecture Decisions

## D1 — Start with semantics, not serialization

JSON Schema, protobuf, dataclasses, and Rust structs are encodings. The first artifact defines state, identity, causality, evidence, and forbidden transitions before freezing an Effect IR wire format.

## D2 — Use an independent reference implementation

The reference kernel is Python and standard-library only. Ordivon is Rust and Linux-specific. Agreement between them is stronger evidence of a universal contract than two implementations sharing the same storage and process assumptions.

Python is not selected as the production kernel. It is selected as an executable semantic oracle and a rapid falsification surface.

## D3 — Separate Effect from Dispatch

An Effect expresses the intended observation or change. A Dispatch is one concrete crossing into a Tool or external system. This separation is required for response loss, rebinding, correlation, and no-duplicate guarantees.

## D4 — Treat unknown as a first-class state

No response, lost process ownership, stale local state, or disconnected Host is not proof of failure. `unknown → reconciling → observed outcome` is a core path.

## D5 — Facts require evidence-bound verification

Model text, successful transport, process exit, and Artifact existence are not Facts. A Fact is admitted only when an explicit Claim receives an accepted Verification that references immutable evidence.

## D6 — Keep retries out of v0

Generic retry semantics are deferred. Blind retry is unsafe once a Dispatch may have crossed the world boundary. A proven retryable pre-admission rejection is different: the rejected Dispatch remains immutable while the Effect returns to prepared and may create a new Dispatch identity. Rebinding, compensation, and retry after unknown outcome remain deferred.

## D7 — Keep Goal and Task above the kernel

Goal, Task, scheduling, memory, and model calls depend on lower semantics. They must consume Effect and evidence state, not define it.

## D8 — Bind semantic objects before binding Tools

A Tool argument such as `workspaceId` is not enough to prove that the Effect targets the intended world object. The adapter must validate a canonical WorldObject identity against the concrete backend object before a Dispatch begins.

## D9 — Separate transport uncertainty from explicit rejection

Transport loss or malformed protocol state may leave the world outcome unknown. A structured Tool rejection is different, but the adapter first confirms whether a durable backend Job exists. With no Job, a retryable rejection preserves the Effect as prepared; a non-retryable rejection fails it.

## D10 — Keep concrete protocols below a provider-neutral Tool port

The semantic adapter depends on a minimal `ToolCaller` protocol and generic Tool errors. Streamable HTTP MCP is one concrete transport implementation, not part of Agent semantic truth.

## D11 — Effect and Dispatch have different lifecycles

An Effect is durable intent; a Dispatch is one concrete delivery attempt. Dispatch rejection does not necessarily invalidate the Effect. This distinction is required for capacity pressure, temporary unavailability, schema adaptation, and future backend rebinding.

## D12 — Do not add a packaging substrate before reuse requires one

Semantic Core v0 runs directly from `src/` with no runtime dependency. The local environment has no Python build backend, and packaging is not part of the current research question. A build backend, distribution format, or registry publication will be introduced only when a second consumer requires an installable artifact.
