# ANC-LINK-001 — Task Connectivity and Evidence Continuity

## Status

- Epistemic status: active foundational research question
- GitHub issue: #67
- Parent program: Agent-Native Responsibility Overlay
- Implementation owner: `ordivon-link`
- Semantic consumers: `ordivon-host`, semantic Kernel, `ordivon-edge`,
  `ordivon-security`
- Related questions: `ANC-MEMORY-001`, `ANC-EFFECT-001`, `ANC-WORLD-001`,
  `ANC-SECURITY-001`, `ANC-SECURITY-002`

## Question

Which semantics are required for an open Task to express, select, verify,
replace, and recover communication relationships while preserving identity,
path-conditioned evidence, uncertainty, authorization, and Task continuity
across mature network and messaging substrates?

## Why this is not ordinary networking

Classical systems already own packet transport, routing, DNS, VPNs, proxies,
CNI, service meshes, discovery, PKI, workload identity, retries, queues,
telemetry, failover, traffic shaping, and network simulation.

The unresolved candidate responsibility begins above those mechanisms:

```text
Task discovers a new service, data source, Agent, device, or human participant
→ logical relation and constraints are expressed
→ one path, endpoint, transport, and identity mechanism is selected
→ the realized relationship is verified
→ evidence is bound to the path and identity conditions that produced it
→ path, endpoint, identity, or participant changes
→ affected claims and pending work are reconciled or invalidated
→ the parent Task continues
```

## Objects under investigation

- Connectivity Requirement;
- Path/Identity Observation;
- Connectivity Candidate;
- Connectivity Binding;
- logical source and target identity references;
- path-conditioned Artifact/Claim provenance;
- invalidation conditions and dependency edges;
- communication delivery/reply uncertainty;
- relationship and participant continuation.

Each object is provisional. The research must find the minimum sufficient set,
not ratify all names.

## Classical baselines to defeat

1. Direct application use of DNS, HTTP clients, proxies, and VPN configuration.
2. CNI and SDN attachment/configuration lifecycles.
3. Service-mesh retry, failover, routing, identity, and telemetry.
4. SPIFFE/SPIRE or equivalent workload identity.
5. Message queues and durable workflow signals.
6. OpenTelemetry and packet/path observability.
7. Network emulation and traffic-control environments.
8. A2A/MCP request, Task, and Artifact transport semantics.

The Link layer is not justified unless realistic Task trajectories remain
ambiguous or repeatedly reimplemented above these systems.

## Required failure trajectories

### F1 — same target, different paths, different world

The same logical website is observed through direct, VPN, and remote Edge paths
and returns materially different content. Historical evidence must remain valid
as conditioned observation without becoming universal truth.

### F2 — transparent failover invalidates evidence

A service mesh or proxy silently changes endpoint or region. The application
call succeeds, but the Task's locality, identity, freshness, or reproducibility
claim may no longer hold.

### F3 — path loss with uncertain delivery

An Artifact or request may have been accepted before the connection failed.
Recovery must reconcile the original communication before retrying or switching
participants.

### F4 — identity rotation and endpoint replacement

A service or Agent participant changes process, address, certificate, or
identity generation. The Task must determine which permissions, commitments,
and pending work continue.

### F5 — relation changes transport form

A synchronous RPC becomes an asynchronous queue, Artifact handoff, or human
review. The logical work relation persists while transport and timing change.

### F6 — participant replacement

Agent B cannot continue and Agent C takes over. The Task must preserve explicit
handoff and responsibility rather than treating reachability as identity.

## Research tasks

1. Map classical packet, route, discovery, identity, mesh, queue, and
   observability layers and mark their authority boundaries.
2. Reclassify current `ordivon-link` components as observation producers,
   operator tools, reference transport, or network-condition laboratory.
3. Derive a schema-free Connectivity Requirement field inventory from public
   Web research and Agent-to-Agent Artifact review.
4. Publish versioned, expiring, method-bound Link Observations as Host Context
   sources and measure their value.
5. Run the same logical observation across direct, VPN, and remote Edge paths;
   define exact evidence invalidation behavior.
6. Inject endpoint replacement, identity rotation, response loss, and
   participant handoff into one Task.
7. Compare direct Host/network integration against a Link Binding layer for
   code volume, duplicated logic, recovery clarity, and evidence quality.
8. Attempt to delete Network World identity from ordinary production paths;
   retain it only where controlled-world experiments or replay demonstrably
   require it.
9. Use maintained CNI, namespace, service-mesh, or traffic-control mechanisms
   for any later data plane; do not build a new network stack.

## Evidence requirements

- exact Task, relation, identity, path, endpoint, policy, and observation
  revisions;
- method, timestamp, freshness, and uncertainty for every path claim;
- Artifact and Claim dependencies on network conditions;
- injected change and explicit invalidation results;
- delivery/reply reconciliation before retransmission;
- participant handoff evidence;
- comparison against strongest direct-network and service-mesh baselines;
- at least two materially different workloads.

## Decision outcomes

- **Promote:** a compact cross-workload relation/evidence continuity
  responsibility is proven and cannot be owned by Host or network adapters
  alone.
- **Keep in Research:** path-conditioned evidence is useful but relation or
  identity semantics remain domain-specific.
- **Absorb:** Host plus observation and provider adapters own the responsibility
  more cleanly.
- **Delete:** Network World or connectivity abstractions add no value beyond
  topology configuration and traces.
