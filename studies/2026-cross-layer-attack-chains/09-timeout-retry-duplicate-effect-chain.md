# 09 — Timeout and Retry: Ambiguity to Duplicate Effect

## Why this belongs beside CVEs

Not every serious attack or failure chain begins with a software vulnerability.
Distributed systems can create a hazardous state through individually reasonable
components:

- a client times out;
- a proxy retries;
- a provider commits before its response is lost;
- an Agent switches path and retries;
- no stable Effect identity joins the attempts.

An attacker who can selectively delay or drop responses can intentionally exploit
this ambiguity.

## Evidence boundary

RFC 9110 defines idempotent method semantics and permits automatic retry in
specified cases, but method semantics do not establish exactly-once durable
business effects. [R24]

AWS Well-Architected guidance explains that exactly-once processing is harder
than at-most-once or at-least-once behavior and recommends client-provided
idempotency tokens for mutating operations. [R23]

R4 treats this as a standards- and provider-validated failure family rather than
a claim about one named public incident.

## Causal graph

```text
A1 retries preserve availability under transient failure
→ T1 client cannot directly observe remote commit after response loss
→ W1 timeout collapsed into failure instead of UNKNOWN
→ V1 multiple layers retry without shared semantic identity
→ P1 same intended operation reaches provider more than once
→ I1 every attempt carries valid client authority
→ N1 alternate paths, proxies, queues, or workers multiply attempts
→ O1 duplicate payment, deployment, message, reservation, or infrastructure change
→ D1 provider/object reconciliation reveals duplicate state
→ R1 compensate or reverse where possible
→ X1 charges, notifications, callbacks, partial jobs, irreversible history
```

## The attacker primitive is delay, not authorization bypass

A network or endpoint attacker may not be able to forge the request. It can still
influence execution by shaping the client's belief:

```text
valid request commits
→ response is delayed or dropped
→ client believes operation failed
→ valid retry creates second commit
```

The attacker exploits uncertainty and automation.

## Retry multiplication

Suppose retries exist at:

```text
Agent loop
Host
SDK
HTTP proxy
service mesh
load balancer
queue consumer
human operator
```

If each independently performs even a small number of attempts, the total can
multiply. Logs may show each layer as locally reasonable.

## Idempotency key requirements

A useful idempotency relation binds:

- participant or account;
- provider and endpoint;
- exact semantic Effect;
- critical parameters;
- key scope and lifetime;
- first result and conflict behavior;
- retry attempts;
- final provider object.

A key that is reused with different parameters must not silently convert one
Effect into another.

## Method idempotency is not complete business idempotency

A nominally idempotent update can still duplicate:

- billing events;
- audit records;
- notifications;
- downstream Webhooks;
- workflow transitions;
- external side effects.

Conversely, a nominally non-idempotent API can support safe retries through a
provider-defined operation key.

## Stale reconciliation

Reconciliation can itself be wrong if it reads:

- a stale replica;
- a cache;
- the wrong region;
- an eventually consistent index;
- a different provider account;
- an object before asynchronous commit becomes visible.

Therefore the evidence source and consistency semantics matter.

## Defensive breakpoints

### B1 — explicit UNKNOWN

After ambiguous transport failure, do not assert failure or success.

### B2 — stable Effect identity

Project all attempts onto one semantic Effect.

### B3 — provider-native idempotency

Use mature provider mechanisms with exact scope and conflict semantics.

### B4 — inventory retry layers

One owner sets the total budget; hidden retries must be observable.

### B5 — reconcile before redispatch

Query authoritative provider or object state.

### B6 — backoff, jitter, and concurrency control

Prevent overload and synchronized retry storms.

### B7 — callback verification

Correlate asynchronous completion to the Effect and verify sender/transaction.

## Recovery and residual closure

A duplicate durable Effect may not be erasable. Compensation creates another
Effect and can leave:

- financial settlement history;
- notification history;
- audit and regulatory impact;
- temporary resource consumption;
- external recipients;
- new callbacks or jobs.

Closure must verify both the compensating action and remaining external state.

## Agent amplification

An Agent can make this failure worse by:

- interpreting urgency as permission to retry faster;
- switching providers or paths without preserving Effect identity;
- generating another Tool with hidden retries;
- trusting a success-looking response from a cache;
- repeating after a model restart without recovered state.

It can also improve defense by correlating attempts, querying provider state, and
holding at `UNKNOWN` until evidence arrives.

## Ordivon lesson

This chain strongly validates existing Ordivon decisions: stable Effect identity,
explicit `UNKNOWN`, opaque backend correlation, reconcile-before-redispatch, and
independent verification. It does not justify a new distributed-transaction
platform.
