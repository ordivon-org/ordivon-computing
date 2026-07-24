# 14 — World Interfaces and Tool Contracts

Tools map Agent Effect semantics to real filesystems, processes, databases, browsers, cloud resources, applications, and physical devices.

## Interface layers

```text
Agent Effect
→ Tool contract
→ Adapter and transport
→ External system
→ normalized Observation
```

A Tool is the Agent-facing semantic capability. An API or CLI is one possible concrete channel. An Adapter translates the stable effect into that channel.

## Contract as ABI

A Tool contract defines:

```text
provider and Tool identity
input and output Schemas
effect meaning
error model
synchronous or asynchronous lifecycle
contract revision
```

Schema says what the messages look like. Semantics says what the call does to the world.

## Tool discovery

Available Tools vary by host, account, task, and time. A Tool catalog has its own revision. Hosts can expose the current task’s working set instead of loading every possible Tool into model context.

Tool selection considers target location, current task state, capability, information value, latency, and state affinity.

## Call lifecycle

```text
discover
→ select
→ bind contract
→ prepare arguments
→ dispatch
→ execute
→ observe
→ normalize
→ persist
→ continue
```

Results should distinguish success, failure, accepted asynchronous work, and unknown outcome.

## Contract evolution

Adding required fields, tightening accepted values, changing sync behaviour, or changing semantics alters what callers can safely do. A long-running task should bind the normalized executable catalog and detect later changes.

When a contract changes:

```text
detect
→ semantic diff
→ rebind pending Effects
→ preserve completed facts
→ continue observing active jobs by stable identity
```

## Tool Contract Drift

Drift occurs when the model-visible Schema, Host snapshot, approved app definition, and live runtime do not match. A model can generate a call valid under its visible contract that the runtime rejects.

This is distributed state. It requires catalog identity, change detection, and adoption semantics rather than only better Prompting.

## Authentication and capability

Authentication answers who the caller is. Capability answers which effects that identity can perform on which objects for this task. Capability is therefore part of both planning and execution.

## Different worlds

- files benefit from paths, digests, and versioned mutation;
- commands produce exit codes, streams, and long-running handles;
- databases provide transactions and constraints;
- browsers require observe–act–wait–verify loops;
- cloud resources have stable IDs and asynchronous lifecycles;
- physical systems require sensor-based confirmation.

A unified result model lets the Agent kernel preserve their differences while exposing common task semantics.
