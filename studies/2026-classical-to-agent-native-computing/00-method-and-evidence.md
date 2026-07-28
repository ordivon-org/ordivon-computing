# Method and Evidence

## 1. Responsibility, use, and proximity are different

A component owns a responsibility only when it provides the authoritative mechanism and accepts the corresponding failure burden.

```text
uses SQLite          ≠ owns a storage engine
runs a process       ≠ owns an operating-system scheduler
opens a worktree     ≠ owns a security sandbox
calls an LLM         ≠ owns a model runtime
exposes a Tool       ≠ owns task continuity or authorization
models a remote Node ≠ owns a distributed scheduler
```

For this study, a claimed implementation responsibility requires all of the following:

1. a runnable mechanism rather than only prose or types;
2. authoritative state or an explicit stateless contract;
3. a real invocation path;
4. defined failure and recovery behavior;
5. deterministic tests, live evidence, or both.

A repository name, roadmap, charter, interface sketch, or future provider adapter is not sufficient.

## 2. What counts as a layer

A stable layer should satisfy most of these conditions:

- **distinct subject** — it owns a kind of state or decision not already owned below;
- **stable contract** — callers can depend on a bounded interface or invariant;
- **independent failure** — the layer can fail while adjacent layers remain healthy;
- **non-bypassability** — bypassing it causes a real class of incorrect or unsafe trajectories;
- **cross-workload leverage** — the abstraction is useful in at least two materially different domains;
- **replacement boundary** — implementations can change without changing the layer's responsibility;
- **evidence path** — its guarantees can be tested or observed.

Importance alone does not create a layer. A frequently discussed concept may remain a policy, implementation detail, or research question. This is consistent with Anthropic's guidance to begin with simple composable patterns and add Agent complexity only when measurement justifies it [A07].

## 3. Five classes of change

### Unchanged

The existing deterministic mechanism still expresses and enforces the required contract. Example: SQLite atomic commit remains the byte-level durability mechanism beneath an Agent journal [C04].

### Amplified

Agent workloads create more events, longer execution, or greater risk, but the semantic object is unchanged. More log volume does not by itself create an Agent-native logging layer.

### Composed

An Agent product combines a model, tools, workflow engine, database, sandbox, and user interface. Composition may be valuable without creating a new universal primitive.

### Rewritten

An existing concept remains recognizable but its admission or completion contract changes. Authorization is an example: process credentials remain necessary, but an Agent effect may also need binding to a goal, object version, consequence envelope, and current approval.

### New responsibility

No lower layer owns the invariant. An example candidate is fact admission: a database can atomically store a model claim, but it does not decide whether the claim has sufficient independent evidence to become an accepted system fact.

## 4. Evidence levels

| Level | Evidence | Permitted claim |
|---|---|---|
| E0 | name, analogy, intention | research direction only |
| E1 | document, schema, or type | represented concept |
| E2 | executable local prototype | mechanism exists in one bounded environment |
| E3 | deterministic tests and fault cases | stated local invariants are enforced |
| E4 | real process, provider, restart, or deployment evidence | bounded vertical slice is operational |
| E5 | second materially different backend or project | candidate cross-system invariant |
| E6 | sustained real workloads and measured outcomes | mature operational responsibility |

Core inclusion normally requires E4 for a concrete failure class and E5 for a supposedly universal protocol or primitive. A compact principle can enter earlier only when primary-source reasoning is strong and its uncertainty remains explicit.

## 5. Source policy

Classical claims use standards or official implementation documentation. Agent-system claims prefer official engineering reports, product specifications, and original research from organizations that operate the systems. Ordivon claims use exact repository revisions, executable tests, and immutable receipts.

The source ledger records what each source can and cannot support. An official marketing statement is not treated as proof of an implementation invariant merely because it is first-party.

See [`REFERENCES.md`](REFERENCES.md).

## 6. Anti-confirmation procedure

Every proposed Agent-native responsibility is tested against the strongest classical alternative:

- process or Job semantics;
- database transaction and event log;
- Kubernetes controller reconciliation;
- Temporal durable workflows;
- capability, sandbox, and operating-system permissions;
- RPC, MCP, or A2A protocol state;
- ordinary tests, tracing, and observability.

The candidate survives only if these mechanisms still leave an unowned semantic invariant.

## 7. Temporary model limitations

Harnesses encode assumptions about what a model cannot currently do. Anthropic explicitly warns that those assumptions can become stale as models improve [A12]. The Core must therefore preserve stable system responsibility, not workarounds such as a particular prompt shape, fixed number of Agents, context-reset schedule, or provider-specific tool loop.

A responsibility is more likely to endure when it concerns:

- identity across replacement;
- current authority at a durable-effect boundary;
- external state and irreversible consequence;
- evidence provenance;
- explicit uncertainty;
- human responsibility for goals and consequences.

## 8. Writing rule

Each substantive chapter distinguishes:

```text
classical mechanism
→ exact guarantee
→ Agent-era pressure
→ semantic gap, if any
→ Ordivon evidence
→ counterexample
→ non-goal
```

This prevents the Ordivon implementation from becoming the premise of the Ordivon theory.
