# Tool Contracts and World Interfaces

Tools connect Agent effects to filesystems, processes, databases, browsers, cloud services, enterprise applications, and physical devices.

## Four layers

```text
Effect semantics
→ Tool contract
→ Adapter and transport
→ External system
```

The Effect says what should be observed or changed. The Tool contract defines the callable interface. The Adapter maps that interface to HTTP, MCP, CLI, RPC, browser automation, or device protocols. The external system determines the actual world transition.

## Tool contract as ABI

A useful Tool contract contains more than an input JSON Schema:

```text
identity
+ input structure
+ output structure
+ effect semantics
+ error model
+ sync / async behaviour
+ contract revision
```

Schema describes the data shape. Semantics describe what the call means in the world.

## Result states

A call can produce:

- `success` — the operation completed and the result is known;
- `failure` — the operation is known not to have completed as intended;
- `accepted` — a long operation has a stable execution identity;
- `unknown` — the transport outcome is insufficient to infer world state.

Structured errors such as `revision_mismatch`, `capability_missing`, or `contract_mismatch` become direct inputs to the next planning step.

## Tool discovery and working set

The available Tool catalog changes across tasks, accounts, hosts, and time. A Host can expose a compact task-relevant working set rather than every possible Tool. Tool routing then considers target location, capability, state affinity, cost, latency, and contract revision.

## Contract evolution

Tools evolve by adding fields, changing accepted values, introducing async execution, or altering semantics. A durable task therefore binds to a normalized catalog and Tool contract revision.

```text
bind catalog revision
→ execute
→ detect normalized contract change
→ classify the difference
→ re-encode pending Effects
→ continue
```

## Contract drift

Drift occurs when the model-visible schema, Host snapshot, approved application definition, and live runtime contract differ. A model may generate a call that is valid according to its visible schema but rejected by the current runtime.

This is a distributed-state problem rather than a single component failure. Detection should operate on normalized executable contracts, not only human-readable version labels.

## Capability

Authentication establishes identity. Capability expresses the task-relevant action space:

```text
holder + action + object scope + lifetime
```

Capabilities inform planning before execution. A task can progress through construction and testing, then wait for a deployment capability rather than discovering that mismatch only at the final call.

See [`capability-externalization-and-responsibility-placement.md`](capability-externalization-and-responsibility-placement.md) and the [Tool Contract Drift case](../cases/tool-contract-drift.md).
