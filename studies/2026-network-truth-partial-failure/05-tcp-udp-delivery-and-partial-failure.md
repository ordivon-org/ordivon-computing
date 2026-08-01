# 05 — TCP, UDP, Delivery, and Partial Failure

## Transport is not application completion

Transport protocols provide communication semantics between endpoints. They do
not know the participant's Task, application transaction, durable storage,
downstream side effects, or business outcome.

```text
transport delivery evidence
≠ application consumption
≠ transaction commit
≠ durable Effect
≠ participant success
```

## TCP semantics

RFC 9293 is the current core TCP specification. TCP provides a reliable,
in-order byte stream between two transport endpoints, with connection state,
sequence numbers, acknowledgments, retransmission, flow control, and error
handling. [R26]

TCP does not preserve application message boundaries. Applications must define
framing above the stream.

## What a TCP acknowledgment proves

An ACK indicates that bytes have been received into the remote TCP sequence
space under that connection state. It does not prove:

- the application process read the bytes;
- the request parser accepted them;
- the operation was authorized;
- a database committed;
- a downstream service completed;
- the response was generated;
- the external Effect occurred exactly once.

## Half-open and half-closed states

One direction can close while the other remains usable. A host or NAT can lose
state while the peer retains it. Reset, timeout, crash, retransmission, and
reconnection can produce different beliefs about whether the connection or
request completed.

## Stream ambiguity at application boundaries

TCP can split or combine writes arbitrarily from the application's perspective.
A receiver must parse its own message boundaries. Security failures arise when
components assume one `send` maps to one application message or when a proxy and
origin disagree on framing.

R2 covers parser differentials; R3 adds that retransmission and connection reuse
can move ambiguity across time and requests.

## UDP semantics

UDP provides datagrams with source and destination ports and a checksum, but no
built-in reliability, ordering, duplicate suppression, congestion control,
connection establishment, or delivery acknowledgment. RFC 8085 gives usage
guidelines for applications built on UDP. [R27]

A successful local UDP send generally proves only that the local stack accepted
the datagram. The datagram may be dropped, duplicated, reordered, fragmented,
filtered, delivered to a different anycast instance, or processed without a
response.

## Application reliability over UDP

Applications may add:

- transaction IDs;
- acknowledgments;
- retries;
- congestion control;
- replay protection;
- path validation;
- fragmentation avoidance;
- session state.

QUIC is a prominent example. A custom UDP protocol that omits these properties
inherits the failure modes rather than avoiding them.

## Packet loss and retransmission

Loss can occur because of congestion, corruption, filtering, route changes,
receiver overload, NAT expiry, application rate limits, or deliberate attack.

Retransmission improves delivery probability but can amplify load and duplicate
application Effects when request identity and idempotency are not preserved.

## Reordering and duplication

IP networks may reorder packets. Redundant paths, retransmission, failover, and
application retries can duplicate data. Protocols need explicit sequence,
transaction, or Effect identity where duplicate processing matters.

## Fragmentation

Large IP packets can be fragmented or require path-MTU handling. Fragments may be
dropped or interpreted differently by middleboxes and endpoints. Modern
applications generally benefit from avoiding dependence on IP fragmentation and
using transport-level segmentation or protocol-defined limits.

## Congestion and resource attacks

A sender that transmits without congestion control can harm other traffic and
itself. Attackers can exploit retry storms, connection-state exhaustion,
reflection, amplification, and asymmetric resource costs.

The defense must consider:

```text
bytes attacker sends
versus
state, bandwidth, CPU, memory, or downstream work defender allocates
```

## Partial failure matrix

| Observation | Still unknown |
|---|---|
| DNS succeeded | route, endpoint, service, application |
| TCP connected | correct service, authorization, Effect |
| bytes ACKed | application read or commit |
| request sent | response and world outcome |
| response received | durable write or exactly-once execution |
| connection reset | whether server committed before reset |
| timeout | whether request never arrived, is still running, or completed |
| UDP response absent | loss, filtering, server failure, or silent success |

## Attack chains

### Timeout after commit

```text
client sends state-changing request
→ server commits Effect
→ response is lost or connection resets
→ client interprets timeout as failure
→ retry creates duplicate Effect
```

### Retry storm

```text
service latency rises
→ many clients time out and retry
→ load increases
→ latency and failure grow
→ defensive failover spreads load to additional regions
```

An adaptive Agent can accelerate this if it treats every timeout as permission
to retry immediately.

### UDP amplification

```text
small unauthenticated request
→ server emits much larger response toward spoofed source
→ victim receives amplified traffic
```

The exact feasibility depends on source-address validation, protocol behavior,
and server policy. R3 records the asymmetric principle without operational
instructions.

### Connection-state deception

```text
attacker selectively drops FIN, reset, ACK, or response traffic
→ peers retain different connection beliefs
→ one side retries or holds resources
→ monitor sees only one side and misclassifies outcome
```

## Defensive principles

- Define application messages above TCP explicitly.
- Give state-changing requests stable Effect or transaction identity.
- Distinguish transport receipt, application admission, commit, and verification.
- Use bounded retries with backoff, jitter, and total budgets.
- Reconcile before redispatch after ambiguous failure.
- Implement congestion control and amplification limits for UDP protocols.
- Make timeout states explicit rather than collapsing them into failure.
- Observe client and server sides where high-value ambiguity exists.
- Preserve request identity across reconnect and failover.
- Treat transport teardown as insufficient residual closure.

## Ordivon implication

Runtime owns local socket, process, stream, exit, and timeout facts. World or
providers own remote transaction and object observations. Host owns stable Effect
identity, retry policy, and completion criteria. Security evaluates deliberate
loss, resource asymmetry, and retry exploitation. No new transport is justified.
