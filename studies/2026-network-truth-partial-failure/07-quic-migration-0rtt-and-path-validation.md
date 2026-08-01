# 07 — QUIC, Migration, 0-RTT, and Path Validation

## QUIC combines transport and cryptographic setup

RFC 9000 defines QUIC version 1; RFC 9001 defines its use of TLS. QUIC runs over
UDP, provides reliable streams, loss recovery, congestion control, connection
establishment, and cryptographic protection of payload and most control
information. [R29][R30]

QUIC changes transport assumptions:

- multiple independent streams avoid TCP connection-level head-of-line blocking;
- connection identity can survive IP and port changes;
- transport is largely encrypted and implemented in user space;
- 0-RTT can carry application data during resumption;
- endpoints validate new paths and limit amplification.

## Connection ID versus network address

A QUIC Connection ID allows packets arriving from a new address to be associated
with an existing connection. RFC 9308 explains how this supports NAT rebinding,
interface changes, temporary-address rotation, and intentional migration. [R31]

Therefore:

```text
same QUIC connection
≠ same IP address or path
```

and:

```text
same IP address
≠ same QUIC connection or workload
```

## Migration

A client can migrate a connection to another path where supported. The peer
validates reachability of the new address before fully using it.

Migration preserves application connection continuity while changing:

- source address and port;
- interface;
- NAT mapping;
- route;
- latency and congestion state;
- VPN or local-network exposure;
- observer visibility.

Host and World evidence must not assume one connection has one immutable path.

## Path validation limits

QUIC path validation demonstrates that the peer can receive and return
path-validation data at an address. It does not establish:

- participant identity;
- authorization of the new network;
- confidentiality from local observers;
- equivalence of policy between old and new paths;
- correct application endpoint beyond the authenticated connection;
- final Effect.

## Anti-amplification

Before validating a client's address, a QUIC server limits bytes sent relative
to bytes received. This reduces reflection and amplification against spoofed
addresses. [R29]

The limit controls network consequence, not application CPU, memory, certificate,
or downstream work by itself. Implementations still need resource controls.

## 0-RTT

QUIC uses TLS early data to reduce latency for resumed connections. RFC 9308
states that application protocols must deliberately define which data can safely
be sent in 0-RTT because replay is possible. [R31]

0-RTT can also carry assumptions from the previous connection about:

- transport parameters;
- application protocol;
- server deployment;
- resource and authorization state.

A server can reject early data, but the client and application need defined retry
behavior.

## Version negotiation and fallback

QUIC supports version negotiation. UDP blocking or middlebox behavior can cause
applications to fall back to TCP-based alternatives. A fallback path can have:

- different resolver behavior;
- different proxy or VPN routing;
- different TLS termination;
- different cache;
- different observability;
- different retry semantics.

Success through fallback must be reported as fallback, not as QUIC success.

## Stateless reset and observer ambiguity

A stateless reset allows an endpoint that lost connection state to signal that
the peer should abandon the connection without maintaining full state. From an
application perspective, reset can leave requests in an ambiguous state:

```text
transport state lost
→ application does not know whether peer processed prior request
```

Reconciliation remains necessary for durable Effects.

## Connection IDs and privacy

Connection IDs allow routing and continuity but can create linkability if reused
across paths. QUIC provides mechanisms to issue new Connection IDs and retire old
ones. Path migration should consider both routing requirements and observer
correlation.

## Multipath and alternate paths

Even without standardized multipath application semantics, QUIC can encounter
path changes, preferred server addresses, load balancer routing, retries, and
connection replacement. A provider may map Connection IDs to backend state.

Compromise or drift in that mapping can route an authenticated connection to an
unexpected body or fail continuity.

## Attack chains

### Replay of early application action

```text
client sends operation in 0-RTT
→ attacker or infrastructure causes replay
→ application lacks stable Effect identity or anti-replay rule
→ duplicate world change
```

### Forced fallback

```text
QUIC traffic selectively blocked
→ application retries TCP path
→ alternate path uses weaker proxy, resolver, or monitoring
→ attacker gains visibility or policy advantage
```

### Path-migration policy drift

```text
authenticated connection migrates from VPN interface to local interface
→ transport continuity succeeds
→ organizational path requirement is no longer satisfied
→ application continues high-value Task
```

### Connection-routing state loss

```text
load balancer or endpoint loses QUIC state
→ peer receives reset or timeout
→ client retries request on new connection
→ original application action may already have committed
```

## Defensive principles

- Track connection identity separately from path and body identity.
- Apply path policy after migration, not only at connection creation.
- Use QUIC address validation and anti-amplification mechanisms.
- Restrict 0-RTT to replay-safe operations or use stable Effect identity and
  application anti-replay.
- Make fallback explicit and preserve security invariants.
- Reconcile application state after reset or ambiguous connection loss.
- Observe Connection ID issuance, retirement, migration, and backend mapping
  without exposing sensitive correlation broadly.
- Reassess VPN, interface, region, and egress requirements after migration.
- Test held-out path changes and state loss.
- Verify final Effects independently of QUIC acknowledgment.

## Ordivon implication

World may expose QUIC connection, path, interface, migration, fallback, and
provider-body observations. Host owns Task path requirements, Effect identity,
and replay policy. Runtime owns local client process and socket evidence.
Security evaluates forced fallback, replay, migration abuse, and observer gaps.
No QUIC implementation belongs in Ordivon Core.
