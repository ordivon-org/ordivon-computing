# ANC-WORLD-002 — Task-to-World Interaction Continuity

## Status

- Epistemic status: active foundational research question
- GitHub issue: #78
- Parent program: Agent-Native Responsibility Overlay
- Implementation carrier: `ordivon-world`
- Product experiment: `ordivon-world` #1
- Semantic consumers: `ordivon-host`, semantic Kernel, `ordivon-runtime`,
  `ordivon-security`, and future domain systems
- Supersedes: `ANC-EDGE-001`, `ANC-LINK-001`, and `ANC-WORLD-001`

## Question

Which minimum semantics allow an open Task to discover, bind, execute, observe,
reconcile, and rebind one external-world interaction across changing target,
path, identity, transport, provider, body, participant, and result conditions?

## Structural claim under test

```text
Task / Attempt / Effect
→ interaction intent
→ target, identity, path, transport, provider and capability observations
→ exact Interaction Binding
→ communication and provider execution
→ Receipt / Artifact / Observation / callback / residual state
→ reconcile, invalidate, rebind, verify, continue
```

The research does not assume this chain requires a standalone service or stable
universal object. It may collapse into Host-local composition plus provider and
observation adapters.

## Why the earlier split is insufficient

- action requirements determine connection requirements;
- connection/provider conditions alter evidence and consequence;
- delivery ambiguity and execution ambiguity must be reconciled together;
- provider replacement usually changes connectivity and execution at once;
- callback and remote-to-remote flows are not owned by a local-to-remote split;
- separate project boundaries generated artificial attachment contracts.

## Classical baselines to defeat

1. Direct Host use of provider SDKs, HTTP clients, DNS, proxy, VPN, and network
   observations.
2. Durable workflow engines with activity retry, operation IDs, polling,
   callbacks, and signals.
3. Cloud control planes, Browser/Sandbox APIs, queues, object stores, and native
   provider reconciliation.
4. CNI, Service Mesh, workload identity, discovery, failover, and telemetry.
5. A2A/MCP Task and Artifact transport semantics.
6. OpenTelemetry and W3C-PROV-style tracing and provenance.
7. Host-local foreign references with no independent World object.

## Required trajectories

### F1 — complete local-to-remote interaction

A Host Task obtains current path/target evidence, invokes an existing external
Fetch or Browser provider, receives Artifacts, and verifies the result.

### F2 — remote commit with lost response

The provider commits work and Artifacts but the response is lost or Host
restarts. Recovery queries the original interaction and avoids duplicate Effect.

### F3 — conditioned observation drift

Path, endpoint, region, identity, provider, policy, or build changes. Historical
evidence remains attributable while unsupported current Claims become stale.

### F4 — remote-to-local callback

External work continues asynchronously and delivers a callback or result to a
changed endpoint or Host generation. Acceptance and responsibility are
reconciled before replacement.

### F5 — remote-to-remote transfer

Provider A writes an Artifact directly to storage or Provider B. Host receives a
reference, digest, Receipt, and provenance rather than proxying the bytes.

### F6 — fan-out and join

One Task creates multiple interactions across heterogeneous providers or
participants, then joins their independently conditioned Artifacts.

### F7 — participant or provider handoff

Path, endpoint, identity, transport, provider, body, or participant is replaced
without inventing a new Task or silently inheriting authority.

## Research tasks

1. Build one authority map spanning networking, identity, provider operations,
   workflow durability, messaging, callbacks, tracing, and provenance.
2. Run `ordivon-world#1` with direct-integration controls.
3. Record a broad field inventory, then perform field-deletion experiments.
4. Separate semantic Effect, Dispatch, delivery, session, provider execution,
   Receipt, Observation, and Artifact identities.
5. Inject response loss, Host restart, stale path evidence, endpoint/identity
   rotation, policy drift, and provider uncertainty.
6. Test a second materially different workload.
7. Test local→remote, remote→local, remote→remote, one→many, and many→one.
8. Compare independent and combined rebinding of path/provider/participant.
9. Measure whether Security or another domain is a genuine second consumer.
10. Decide retain, absorb, freeze, or delete.

## Evidence requirements

- exact Task/Attempt/Effect/Dispatch references;
- exact target, participant, endpoint, path, transport, identity, provider,
  execution, policy, build, Observation, Receipt, and Artifact revisions;
- method, time, freshness, uncertainty, and invalidation dependencies;
- injected failure point and observed world result;
- duplicated/lost work, recovery time, operator intervention, and state volume;
- direct-integration code and complexity comparison;
- at least two materially different workloads;
- retained negative and null results.

## Decision outcomes

- **Promote:** a compact cross-workload World responsibility prevents real
  failures and has multiple consumers.
- **Absorb:** Host plus provider/observation adapters own the semantics more
  cleanly.
- **Keep modules:** Cloudflare and network tools remain useful without a shared
  World layer.
- **Delete:** candidate interaction fields or abstractions add no value beyond
  mature systems and ordinary foreign references.
