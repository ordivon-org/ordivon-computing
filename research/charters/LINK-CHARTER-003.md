# LINK-CHARTER-003 — Task-to-Connectivity and Evidence Continuity Overlay


> **Historical intermediate charter:** superseded by [`WORLD-CHARTER-001`](WORLD-CHARTER-001.md) after external placement and connectivity were unified as one Task-to-World Interaction responsibility.
Status: historical intermediate charter — superseded by WORLD-CHARTER-001

Supersedes the long-term responsibility claim in
[`LINK-CHARTER-002`](LINK-CHARTER-002.md). Charter 002 remains a historical
record of the Phase 0 Network World hypothesis and its evidence.

## Mission

Ordivon Link studies and supplies the semantic boundary through which an open
Task expresses, selects, verifies, changes, and recovers communication
relationships without depending on one IP address, route, VPN, proxy,
transport, endpoint instance, network namespace, region, or temporary workload
identity.

Link is not a replacement network stack, VPN, proxy core, CNI implementation,
service mesh, SDN controller, DNS system, PKI, QUIC implementation, traffic
shaper, or observability platform. Those systems remain authoritative for byte
transport and network configuration. Link adds the Task-level relation,
binding, path-conditioned evidence, invalidation, and recovery semantics that
they do not own.

```text
Goal / Task / Task Attempt / Effect
              │ foreign semantic references
              ▼
      connectivity requirement
              ▼
 path, transport, endpoint, and identity observations
              ▼
       connectivity binding
              ▼
 mature DNS / CNI / VPN / proxy / mesh / transport / identity substrate
              ▼
 path-conditioned Observation, failure, identity and policy evidence
              ▼
       Host continues the Task
```

## Foundational split

```text
logical relationship
  who needs to interact with whom, why, and under which authority

communication identity
  which principal, workload, service, Agent participant, or device is present

physical path
  which endpoint, route, transport, tunnel, relay, region, or intermediary
  carried this interaction
```

Relation, identity, and path are not interchangeable. One relation may survive
path replacement. One logical identity may survive endpoint replacement. A
reachable endpoint is not necessarily the intended or authorized participant.

## Candidate owned semantics

Link may own the following semantics when experiments demonstrate that they are
shared and non-bypassable:

1. **Connectivity Requirement** — a bounded description of logical source,
   logical target, interaction kind, direction, identity assurance, trust and
   data boundaries, locality, latency, availability, evidence, and replacement
   requirements for one Task Attempt or Effect.
2. **Path and identity Observation** — versioned, expiring, method-bound facts
   about reachability, route class, egress, endpoint identity, protocol,
   application capability, and uncertainty.
3. **Connectivity Candidate** — one way to realize a relationship through
   mature mechanisms, including direct access, VPN, proxy, service mesh, Edge
   mediation, asynchronous Artifact handoff, or another participant.
4. **Connectivity Binding** — an immutable relation from Task, Task Attempt, and Effect
   references to logical source and target identities, selected path and
   transport, policy revision, identity generation, and the observations used
   to justify the selection.
5. **Path-conditioned provenance** — preservation of the network, identity,
   region, time, and observation conditions under which an Artifact or Claim was
   produced.
6. **Invalidation** — explicit classification of which Observations, Claims,
   pending communications, and permissions become stale when a path, endpoint,
   identity, policy, or observation revision changes.
7. **Communication recovery** — reconciliation of accepted, delivered,
   processing, replied, failed, and unknown work before retry, reroute, or
   participant replacement.
8. **Relationship continuity** — preservation of Task intent and accountable
   handoff across path, endpoint, transport, and participant replacement.

These objects are research candidates. Their exact schemas do not belong in
Core or Protocol until two materially different workloads prove them.

## Foreign semantics

Link references but does not redefine:

- Goal, Task, Task Attempt, Effect, Dispatch, Artifact, Claim, Verification, and Fact;
- participant responsibility, commitments, organizational membership, and
  campaign objectives;
- provider body, Sandbox, VM, browser, device, or process lifecycle;
- CNI, route, DNS, VPN, proxy, service mesh, PKI, transport, socket, and packet
  semantics;
- domain-level authorization and final evidence admission.

Host or the semantic Kernel owns open work and Effect history. Edge owns
Task-to-external-execution placement. Runtime owns trusted-local execution.
Security or the domain system owns consequence policy and final validity.
Classical network and identity systems remain authoritative for their native
mechanisms.

## Current repository interpretation

The current `ordivon-link` repository contains four distinct evidence classes:

1. **Useful observation producers** — local route, DNS, VPN, service, HTTP/TLS,
   HTTP/3/QUIC, transfer, and connection-lifetime probes plus reduced history.
2. **Private operator tooling** — explicit per-command WireGuard namespaces and
   provider-specific Surfshark measurement.
3. **Reference transport experiment** — bounded Baseline v0 framing and a
   Quinn/rustls localhost implementation.
4. **Network-condition research substrate** — deterministic Network World
   identity, modeled mutations, observer chain, actor view, lifecycle, and a
   narrow loopback fixture.

The fourth class is not promoted to a permanent Agent-native Network World core
by this charter. It remains a useful experiment laboratory for path, identity,
partition, and evidence hypotheses. Current code does not implement a
Task-level Connectivity Requirement, Connectivity Binding, path-conditioned
Artifact provenance, automatic selection, path-change invalidation, participant
continuity, or a real Host recovery benchmark.

## Research route

### L0 — Preserve operational truth

Keep network probes, reduced observations, explicit isolated egress, and bounded
reference experiments usable. Do not turn the repository into a generic network
platform.

### L1 — Publish Host-consumable path Observations

Expose versioned, expiring, secret-free observations with method, source,
target, path label, time, policy, uncertainty, and invalidation conditions. Prove
that Host Context can consume them without moving Context ownership into Link.

### L2 — Derive Connectivity Requirement from two real workloads

Use at least two materially different workloads, such as public Web research
and Agent-to-Agent Artifact review. Determine which logical relation, identity,
trust, data, locality, and evidence fields are truly required. Do not automate
host route or VPN changes.

### L3 — Prove path-conditioned evidence and invalidation

Run the same logical observation across direct, VPN, and remote Edge paths.
Prove that historical Artifacts remain attributable while stale path claims are
invalidated rather than silently generalized.

### L4 — Prove communication recovery

Inject response loss, endpoint replacement, identity rotation, and path failure.
Reconcile the original communication before retry, reroute, or participant
replacement, and preserve the parent Task.

### L5 — Revisit Network World and range data planes only under evidence

Use mature namespace, CNI, service-mesh, SDN, and traffic-control mechanisms
when a controlled world is required for Security or capability experiments. The
Network World becomes a durable Link abstraction only if multiple workloads
need the same Task-conditioned world identity, evidence, reset, and invalidation
semantics above those mechanisms.

## Admission tests

A proposed Link abstraction must answer:

1. Which mature network, identity, discovery, mesh, workflow, or messaging
   mechanism is insufficient?
2. Which exact Task-level relation or evidence invariant remains unowned?
3. What realistic failure occurs if the abstraction is deleted?
4. Which second workload demonstrates the same invariant?
5. Can the result remain a Host policy, observation schema, provider adapter, or
   domain-local relation instead of a new resident service?

## Falsifiers

Reduce or delete the independent Link semantic layer if:

- Host plus mature network and identity systems preserve the same relation,
  evidence, invalidation, and recovery semantics without duplicated application
  logic;
- Connectivity Requirement fields do not generalize beyond one workload;
- route and identity changes can remain fully transparent without altering Task
  evidence, authority, or recovery decisions;
- Network World identity adds no explanatory or experimental value beyond
  ordinary topology configuration and trace data;
- participant continuity cannot be separated from Host or organizational state.

## Success condition

Link succeeds when one open Task can express a logical communication need,
select and bind a mature path and identity mechanism, verify what relation was
actually realized, preserve path-conditioned evidence, invalidate only affected
claims after change, reconcile uncertain communication, and continue across
path or participant replacement without building a new network stack.
