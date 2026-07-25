# Initial Architecture Decisions

## D1 — Start with semantics, not serialization

JSON Schema, protobuf, dataclasses, and Rust structs are encodings. State, identity, causality, evidence, and forbidden transitions are defined before an Effect IR wire format is frozen.

## D2 — Use an independent reference implementation

The reference kernel is standard-library Python. Ordivon is Rust and Linux-specific. Agreement between independent implementations is stronger evidence of a universal contract than two implementations sharing one backend's assumptions.

Python is an executable semantic oracle and falsification surface, not the selected production kernel.

## D3 — Separate Effect from Dispatch

An Effect expresses intended world observation or change. A Dispatch is one concrete boundary attempt. `DispatchRecord` has independent identity, request digest, ownership, and time.

## D4 — Treat unknown as a first-class state

No response, lost process ownership, stale local state, or disconnected Host is not proof of failure. `unknown → reconciling → observed outcome` is a core path.

## D5 — Facts require evidence-bound verification

Model text, successful transport, process exit, and Artifact existence are not Facts. A Fact is admitted only when an explicit Claim receives an accepted Verification.

## D6 — Bind Claims to Effects

A Verification cannot borrow convenient evidence from unrelated work. Each Claim identifies an owning Effect; accepted evidence must originate from that Effect and satisfy its VerificationPlan.

## D7 — Keep retries out of v0

Blind retry is unsafe after a Dispatch may have crossed the world boundary. Later work must distinguish new delivery, rebinding, retry, compensation, and a genuinely new Effect.

## D8 — Keep transport below adapters

The semantic core defines Tool-call uncertainty classes but does not implement MCP, HTTP, CLI, or RPC transports. Transport protocol correctness belongs to Tool ABI and adapter work.

## D9 — Keep Goal and Task above the kernel

Goal, Task, scheduling, memory, and model calls consume Effect and evidence state. They do not define the lower semantics.
