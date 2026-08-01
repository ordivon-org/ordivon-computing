# Network Truth, Routing, Transport, Encryption, and Partial Failure

Status: R3 foundational study completed

## Purpose

R3 studies which claims can be admitted from network observations and which
claims remain outside the network's authority.

The central question is:

> What can naming, routing, transport, and encrypted-channel evidence prove about
> identity, delivery, execution, and world consequence—and what remains unknown
> without endpoint and application evidence?

The analysis follows this path:

```text
participant names a service
→ resolver obtains current naming data
→ routing system selects reachable paths
→ local host chooses an address and interface
→ NAT, proxy, VPN, or tunnel transforms the path
→ transport creates stream or datagram state
→ TLS or QUIC authenticates and protects a channel
→ application exchanges requests and responses
→ provider or endpoint performs a world Effect
→ independent observation verifies outcome
```

## Adversarial stance

R3 assumes a strong adaptive opponent that can:

- control or compromise selected DNS zones, resolvers, caches, authoritative
  servers, network links, routers, autonomous systems, proxies, VPN endpoints,
  relay services, NAT-adjacent paths, application endpoints, or low-privilege
  identities when a concrete chain grants that position;
- announce or leak routes, manipulate unprotected traffic, delay, drop,
  duplicate, reorder, fragment, replay, redirect, or selectively degrade
  communication within the limits of the relevant protocol and position;
- operate legitimate network and cloud services, valid endpoints, and encrypted
  channels;
- force fallback or path switching where applications permit it;
- exploit caching, stale state, retries, resumption, 0-RTT, connection migration,
  timeout ambiguity, and inconsistent observations;
- construct measurement and path-selection Tools, coordinate multiple Agents,
  learn from defenses, and change strategy after detection;
- target the observer, monitor, resolver, route collector, identity provider, or
  evaluator rather than only the application endpoint.

The model does not assume magical decryption, arbitrary forgery of uncompromised
cryptographic identities, or control of an independent evidence plane without a
demonstrated path.

Model, Provider, Host, system-prompt, policy, and Tool-broker refusals are bound
configuration observations. They do not prove that a lower-layer network
capability or another Agent realization is absent. Generated aggressive text,
likewise, does not prove path control or world consequence.

R3 contains no intrusive network procedures, target enumeration, route
announcement instructions, traffic interception steps, credential capture,
packet-injection recipes, or public-system testing.

## Central result

Network observations form a ladder of limited claims:

```text
DNS answer
  one resolver path returned one name-to-data relation under stated validation,
  cache, and time conditions

BGP route
  one routing view selected or observed one path announcement and policy result

IP reachability
  packets can traverse one current path in at least one direction

transport success
  endpoints exchanged transport state or bytes under transport semantics

TLS/QUIC authentication
  the peer proved possession of credentials matching a reference identity under
  one handshake and trust configuration

application response
  one endpoint or intermediary produced application-level data

verified Effect
  an owning domain independently established the intended world observation or
  change
```

None of the earlier claims implies every later claim.

## Study structure

1. [`00-method-attacker-model-and-confounds.md`](00-method-attacker-model-and-confounds.md)
   — method, maximal bounded attacker, evidence, and policy-layer confounds;
2. [`01-network-epistemology-and-proof-limits.md`](01-network-epistemology-and-proof-limits.md)
   — claim ladder, path identity, observation conditions, and uncertainty;
3. [`02-dns-naming-resolution-and-cache.md`](02-dns-naming-resolution-and-cache.md)
   — DNS delegation, resolvers, cache, forgery resistance, DNSSEC, privacy, and
   stale/negative state;
4. [`03-bgp-routing-leaks-and-rpki.md`](03-bgp-routing-leaks-and-rpki.md) — BGP
   policy, route leaks, hijacks, RPKI origin validation, Roles, and path limits;
5. [`04-ip-nat-endpoint-and-path-identity.md`](04-ip-nat-endpoint-and-path-identity.md)
   — IP addressing, NAT, address sharing, interface selection, and endpoint
   identity;
6. [`05-tcp-udp-delivery-and-partial-failure.md`](05-tcp-udp-delivery-and-partial-failure.md)
   — stream/datagram semantics, ACK limits, resets, retransmission, duplication,
   and ambiguity;
7. [`06-tls-service-identity-and-channel-security.md`](06-tls-service-identity-and-channel-security.md)
   — current TLS 1.3, reference identity, termination, resumption, early data,
   and channel limits;
8. [`07-quic-migration-0rtt-and-path-validation.md`](07-quic-migration-0rtt-and-path-validation.md)
   — QUIC identity, Connection IDs, migration, validation, anti-amplification,
   and replay;
9. [`08-proxies-vpns-tunnels-and-path-composition.md`](08-proxies-vpns-tunnels-and-path-composition.md)
   — intermediaries, CONNECT, UDP proxying, service meshes, authority, and
   observability;
10. [`09-timeouts-retries-idempotency-and-unknown.md`](09-timeouts-retries-idempotency-and-unknown.md)
    — ambiguous completion, duplicate Effects, reconciliation, callbacks, and
    residual state;
11. [`10-agent-path-discovery-switching-and-defense.md`](10-agent-path-discovery-switching-and-defense.md)
    — Agent amplification, adaptive routing, deception, measurement, and Blue
    counterchains;
12. [`11-ordivon-insertion-and-r4-gate.md`](11-ordivon-insertion-and-r4-gate.md)
    — Host, World, Runtime, Security, and Game implications plus the R4 route;
13. [`REFERENCES.md`](REFERENCES.md) — primary standards ledger.

## Durable learning rule

For every network claim ask:

```text
what exact layer owns the claim?
which name, address, route, connection, identity, and application object are
being related?
who observed it, from which vantage point, at what time?
which caches, policies, fallback paths, tunnels, and translations participated?
which cryptographic validation actually occurred?
what can an on-path, off-path, endpoint, routing, or control-plane attacker do?
what happened after the last visible acknowledgment?
which retries or replays remain possible?
what external state persists after connection teardown?
which independent evidence verifies the intended Effect?
```

## R3 disposition

R3 establishes a network-evidence and architecture discipline. It does not
promote a universal network controller, route oracle, resolver, VPN, proxy,
service mesh, packet capture platform, or central path database. Mature DNS,
BGP, TCP, TLS, QUIC, VPN, proxy, identity, and observability systems remain the
substrate. New Ordivon responsibilities require reproduced cross-layer failure,
multiple consumers, measurable recovery or attribution value, and a deletion
test.
