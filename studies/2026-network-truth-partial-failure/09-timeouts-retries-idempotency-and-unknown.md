# 09 — Timeouts, Retries, Idempotency, and UNKNOWN

## A timeout is epistemic, not semantic

A timeout states that an observer did not receive an expected event before a
local deadline. It does not state what happened in the remote system.

After a state-changing request times out, plausible states include:

```text
request never left client
request left but was dropped
request reached proxy but not origin
origin rejected before commit
origin is still processing
origin committed but response was lost
proxy retried and one or more attempts committed
callback is delayed
observer failed
```

Collapsing these states into `failed` creates duplicate Effects and false
recovery.

## HTTP method idempotency

RFC 9110 defines idempotent methods as methods for which multiple identical
requests are intended to have the same effect as one request. This allows
automatic retries after communication failure in defined cases. [R33]

Idempotent method semantics do not guarantee:

- every implementation is correct;
- logs, notifications, billing, or side effects are duplicated nowhere;
- two non-identical requests share one Effect;
- an unsafe method cannot be made idempotent through application keys;
- a cached response reflects current state.

## Stable Effect identity

For durable actions, the client and provider can bind attempts to one stable
semantic Effect or idempotency key:

```text
Effect ID
→ attempt 1 through path A
→ timeout
→ reconcile provider state
→ attempt 2 through path B with same Effect identity
```

The provider must define scope, lifetime, parameter binding, conflict behavior,
and evidence. An idempotency key reused with changed parameters should not
silently authorize a different Effect.

## Retry layers

Retries can occur in:

- model or Agent loop;
- Host;
- Tool client;
- HTTP library;
- proxy or service mesh;
- load balancer;
- provider SDK;
- message queue;
- worker;
- human operator.

Without shared attempt and Effect identity, the system may not know how many
requests were issued.

## Backoff and jitter

Immediate synchronized retries amplify overload. Exponential or adaptive
backoff, jitter, server retry hints, concurrency limits, and total budgets reduce
retry storms.

An Agent should not infer urgency from repeated failure and increase concurrency
without an explicit policy.

## Deadline propagation

A parent Task may have a deadline shorter than downstream services. Each layer
needs enough time to complete or cancel work. If every layer independently uses
the same timeout, the outer layer may abandon while inner work continues.

A propagated deadline or cancellation signal is still not proof that remote
work stopped.

## Cancellation

Cancellation can mean:

- stop waiting locally;
- request best-effort remote cancellation;
- prevent new attempts;
- compensate an already committed Effect;
- destroy a body or process.

These are distinct. Some Effects cannot be undone.

## Callback and asynchronous completion

Providers may acknowledge admission and complete later through polling, callback,
webhook, queue, or external object state. A synchronous success response may
mean only `accepted`.

Evidence should distinguish:

```text
Dispatch admitted
provider request created
processing
committed
callback delivered
callback verified
Effect observed
Task accepted complete
```

## Reconciliation

Reconciliation asks the owning domain what state currently exists before issuing
another attempt.

A useful algorithmic discipline is:

```text
response definitive success
→ verify when required

response definitive rejection before commit
→ revise or stop

timeout / connection loss / unknown response
→ mark UNKNOWN
→ query provider or external state
→ redispatch only if absence is established or same Effect identity is safe
```

## Compensation versus rollback

A compensating action creates a new Effect intended to offset an earlier Effect.
It does not erase history or guarantee exact restoration.

```text
payment created
→ refund created
```

is not equivalent to the payment never existing.

## Replay and 0-RTT

Transport or attacker replay can duplicate an early request even when the client
issued it once. Application Effect identity and replay-safe operation design are
therefore needed independently of client retry logic.

## Residual state

After timeout, cancellation, or failover, residual state may include:

- provider request;
- queued job;
- partial upload;
- reservation;
- session;
- Token;
- callback subscription;
- generated Tool;
- remote process;
- cache entry;
- external object;
- billing charge.

Connection teardown does not close these.

## Attack chains

### Adversarial delay to induce duplication

```text
attacker or overloaded path delays response after commit
→ Agent times out
→ Agent selects alternate path and retries
→ second commit occurs
```

### Retry amplification

```text
one failure signal
→ Agent, SDK, proxy, and mesh each retry
→ attempt count multiplies
→ provider overload or rate-limit exhaustion
```

### Stale reconciliation

```text
client queries read replica or cache
→ committed Effect not yet visible
→ client concludes absence
→ retries duplicate operation
```

### Callback spoofing or loss

```text
provider completes asynchronously
→ callback is spoofed, delayed, or delivered to stale endpoint
→ Host accepts false completion or retries completed Effect
```

## Defensive principles

- Make `UNKNOWN` first-class.
- Bind every attempt to a stable Effect where the provider supports it.
- Inventory retry layers and total attempt budget.
- Use backoff, jitter, concurrency limits, and retry hints.
- Reconcile against authoritative provider or object state.
- Bind idempotency to parameters, participant, provider, and lifetime.
- Verify callbacks cryptographically and correlate them to the Effect.
- Separate cancellation, compensation, rollback, and teardown.
- Observe residual external state.
- Do not let model confidence replace provider evidence.

## Ordivon implication

This is already aligned with Ordivon's retained Effect identity, explicit
`UNKNOWN`, opaque backend correlation, reconcile-before-redispatch, and
independent verification. R3 strengthens the network reasoning behind those
choices without promoting a new transaction layer.
