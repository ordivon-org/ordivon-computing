# Initial Architecture Decisions

## D1 — Start with semantics, not serialization

JSON Schema, protobuf, dataclasses, and Rust structs are encodings. State, identity, causality, evidence, and forbidden transitions are defined before an Effect IR wire format is frozen.

## D2 — Use an independent reference implementation

The reference kernel is standard-library Python. Ordivon is Rust and Linux-specific. Agreement between independent implementations is stronger evidence of a universal contract than two implementations sharing one backend's assumptions.

Python is an executable semantic oracle and falsification surface, not the selected production kernel.

## D3 — Separate Effect from Dispatch

An Effect expresses intended world observation or change. A Dispatch is one concrete boundary attempt. `DispatchRecord` has independent identity, request digest, ownership, time, and a lifecycle: `STARTED`, `ADMITTED`, `UNKNOWN`, or `REJECTED`. Starting a boundary attempt does not claim backend admission.

## D4 — Separate pre-admission rejection from uncertain delivery

A structured rejection before backend admission may be retryable or terminal. Once a Dispatch is admitted or becomes unknown, it cannot be rewritten as a pre-admission rejection. This prevents a lost response from being normalized into a safe retry.

## D5 — Treat unknown as a first-class state

No response, lost process ownership, stale local state, or disconnected Host is not proof of failure. `unknown → reconciling → observed outcome` is a core path.

## D6 — Facts require evidence-bound verification

Model text, successful transport, process exit, and Artifact existence are not Facts. A Fact is admitted only when an explicit Claim receives an accepted Verification.

## D7 — Separate Claim origin from evidence origin

A Claim records the Effect that proposed it, but independent verification often requires a different Effect. Cross-Effect evidence is allowed only when its world-object identity and version match the Claim subject, its timestamp does not follow Verification, and it satisfies the originating Effect's VerificationPlan.

## D8 — Keep retries out of v0

Blind retry is unsafe after a Dispatch may have crossed the world boundary. Later work must distinguish new delivery, rebinding, retry, compensation, and a genuinely new Effect.

## D9 — Keep transport below adapters

The semantic core defines Tool-call uncertainty classes but does not implement MCP, HTTP, CLI, or RPC transports. Transport protocol correctness belongs to Tool ABI and adapter work.

## D10 — Keep Goal and Task above the kernel

Goal, Task, scheduling, memory, and model calls consume Effect and evidence state. They do not define the lower semantics.
