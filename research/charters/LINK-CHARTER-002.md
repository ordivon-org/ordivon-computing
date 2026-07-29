# LINK-CHARTER-002 — Programmable Adversarial Network Fabric


> **Historical charter:** superseded for future responsibility and roadmap by [`LINK-CHARTER-003.md`](LINK-CHARTER-003.md). Phase 0 evidence below remains valid within its original claim boundary.
Status: working charter

## Mission

Ordivon Link is the programmable network and communication fabric for observing, constructing, perturbing, and controlling the connectivity of distributed Agents and systems.

Its subject is not one VPN, relay, transport, or workstation. Its subject is the relationship graph through which digital actors discover one another, exchange information, experience failure, establish trust, and reorganize under adversarial conditions.

## Foundational split

```text
Agent capability inside the experiment: may be broad
Real-world consequence outside the experiment: must remain narrow
```

Link must support high-capability internal experiments without confusing an isolated range path with permission to reach unrelated real systems.

## Owned semantics

Link owns:

- node, link, subnet, route, trust-zone, identity-domain, and failure-domain models;
- named network worlds and their reproducible lifecycle;
- path observation, selection, switching, partition, degradation, and recovery;
- communication identities and controlled discovery between experiment actors;
- replaceable transport and mediation adapters;
- programmable latency, loss, jitter, bandwidth, DNS, routing, and service-reachability conditions;
- independent network telemetry, connection graphs, and replayable path evidence;
- network-level containment claims and explicit egress facts;
- Agent-to-Agent communication topology inside controlled environments.

## Profiles

- **Local operations profile** — workstation observation, diagnosis, path evidence, and explicit per-command egress.
- **Range profile** — isolated multi-node topology, dynamic faults, synthetic identities, and deterministic reset.
- **Adversarial profile** — mutable topology, deception, competing communication policies, and independent observation.

## Current state — Phase 0 disposition

At the bound Phase 0 revisions, P0-A is verified by Link's typed deterministic Network World, lifecycle, synthetic identities, independent hash-chained observer, actor-safe projection, and explicit egress surface. P0-B is verified by the component-owned `link-world-security` lifecycle port, exact-operation reconciliation, residual classification, and fresh-root reconstruction. P0-C is verified by the infrastructure-only Security acceptance that ran the real Link loopback fixture under Runtime and closed a 75-event Campaign ledger with clean residual classification and a `success` / `conclusive` outcome.

The P0-C run executed Link merge `4cd9d2d2f4208c9799a522619ca7173befc31755`; the bound Link current-main truth source `2b2f449913d270706aba6af2e5ba7d3db0e81b1a` is its clean descendant. The immutable snapshot records both roles rather than substituting the later revision into the run.

P0-D is not verified: no persistent Edge Node is attached to a Link-managed data plane, and topology, latency, loss, route, DNS, and partition changes remain modeled rather than packet-enforced. The implemented scope is the local operations profile plus a deterministic local range slice and localhost transport reference. It contains no evaluated Red/Blue Agent and makes no current embodied-intelligence or physical-network claim.

## Boundaries

Link does not own Agent goals, attack or defense strategy, local process lifecycle, remote node provisioning, or campaign scoring. Host and Security decide why actors act; Runtime executes trusted-local work; Edge supplies remote bodies; Link defines how actors can connect and what the network proves happened.

## Required invariants

1. Every topology and mutation has a named world identity and revision.
2. Observed path facts are distinct from intended policy.
3. The independent observer is not controlled by the evaluated Agent.
4. Range reset restores topology, identity material, and network state to a known baseline.
5. Egress state is explicit; absence of an obvious route is not treated as proof of isolation.
6. Raw sensitive network evidence remains bounded and separately governed from reduced state.
7. Transports remain replaceable; no experiment depends on new cryptography invented by Ordivon.

## Success condition

Link is successful when the same Agent campaign can be replayed across named network worlds, with controlled changes to topology and communication conditions, while an independent observer can explain which connectivity facts changed and whether any external boundary was crossed.
