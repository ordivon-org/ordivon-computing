# 01 — Network Epistemology and Proof Limits

## The network carries evidence, not omniscience

Networking connects independently administered systems under partial
observation. Every layer exposes a different relation:

```text
DNS
  name → resource data

routing
  prefix → currently selected forwarding policy/path

IP
  source and destination addresses in one packet context

transport
  bytes or datagrams exchanged between transport endpoints

TLS
  protected channel + peer credential relation

application
  protocol message and response

World
  actual external object, observation, or durable Effect
```

The main architectural error is promoting one relation into another without
additional evidence.

## Claim ladder

### Naming claim

One resolver returned one RRset, negative answer, alias chain, or error under one
cache, validation, and time condition.

Does not prove:

- every resolver returns the same data;
- the route reaches the intended endpoint;
- the endpoint possesses the expected key;
- the service is healthy;
- the application completed an Effect.

### Routing claim

One route collector, router, or host selected or observed a path to a prefix.

Does not prove:

- packets follow that exact AS path in both directions;
- the path is policy-authorized by every participant;
- the final host or service identity is correct;
- traffic was delivered;
- encryption or application success occurred.

### Reachability claim

A packet exchange or active probe succeeded.

Does not prove:

- bidirectional application reachability for later flows;
- stable path or body identity;
- correct service;
- authorization;
- durable outcome.

### Transport claim

TCP acknowledgment or QUIC acknowledgment establishes transport receipt under
that protocol's state, not application consumption or durable commit.

A UDP send call generally establishes only local kernel acceptance, not remote
delivery.

### Cryptographic channel claim

A successful TLS handshake proves a peer possessed credentials accepted for the
client's reference identity under one trust configuration and that protected
traffic has channel properties. It does not prove the peer is uncompromised, the
application action is authorized, or the service state changed as intended.

### Application response claim

A response can come from origin, edge, proxy, cache, replica, failover service, or
application error handler. It does not prove the requested durable action was
committed exactly once.

### Effect claim

Only the owning domain or independent verifier can admit the intended external
observation or change.

## Path identity is conditional

A path can be identified by a tuple such as:

```text
source body and interface
destination name and resolved address
resolver and answer revision
routing observation
proxy, VPN, tunnel, or service-mesh chain
transport and connection identity
TLS reference identity and peer credential
application endpoint and provider object
observation time
```

Even this does not make the path permanent. DNS TTL, route updates, NAT rebinding,
QUIC migration, load balancing, certificate rotation, and provider deployment can
change individual relations.

## Symmetry cannot be assumed

Forward and reverse traffic can use different routes. DNS resolution and service
selection can differ across client and server. A successful outbound request
does not establish that callbacks or inbound connectivity will work.

## Identity and location differ

```text
IP address
≠ workload identity
≠ participant identity
≠ service identity
```

NAT, anycast, load balancing, containers, mobile interfaces, cloud replacement,
and QUIC migration make location especially unstable.

Service identity should be bound through the application protocol and TLS
reference-identifier process where applicable, not inferred from an observed IP
alone. [R34]

## Availability is not a Boolean property

A service can be:

- reachable only through one resolver or address family;
- reachable but slow enough to time out;
- reachable for handshake but not application traffic;
- reachable for reads but not durable writes;
- reachable through stale cache only;
- reachable from one region and blocked from another;
- reachable through fallback that weakens properties;
- intermittently available under congestion or rate limits.

Agent systems should treat reachability as conditioned evidence, not one durable
flag.

## Negative evidence

Failure can mean:

- name does not exist;
- resolver validation failed;
- route unavailable;
- packet filtered;
- NAT state expired;
- handshake failed;
- identity mismatch;
- endpoint overloaded;
- application rejected;
- response lost after commit;
- observer itself failed.

A timeout is a set of hypotheses, not a conclusion.

## Evidence conditioning

A useful network observation binds:

```text
observer and vantage
method and Tool revision
source interface/body
resolver and validation mode
name, answer, address, and TTL
route view and timestamp
proxy/VPN/tunnel state
transport and TLS parameters
request identity
response source and cache state
uncertainty and invalidation conditions
```

## Independent observers

A single Agent controlling measurement and interpretation can be deceived or
mistaken. High-value outcomes may require:

- endpoint-side logs or provider Receipts;
- a separate route or DNS vantage;
- signed or digest-bound observations;
- application object reads;
- callbacks or externally visible state;
- independent management-plane health.

## Security consequence

Attackers exploit proof inflation:

```text
DNS answer
→ treated as endpoint identity

successful TLS
→ treated as trusted application

TCP ACK
→ treated as durable commit

HTTP 200
→ treated as exactly-once Effect

VPN connected
→ treated as all traffic protected

Agent report
→ treated as world truth
```

The defense is not skepticism without action. It is precise authority and
reconciliation.

## Ordivon implication

World observations should remain conditioned and component-native. Host decides
which evidence is sufficient for one Task and Effect. Security evaluates
adversarial hypotheses. Runtime records local execution. No universal “network
truth” Boolean should enter Core.
