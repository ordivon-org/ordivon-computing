# Method and Admission Standard

## 1. Research object, not vocabulary collection

A term enters this study only when it identifies one of the following:

1. an object with identity and lifecycle;
2. a container that owns other running objects;
3. a control mechanism that changes state;
4. a record that describes what happened;
5. a distribution or integration unit;
6. a cross-cutting invariant such as identity, provenance, authority, or version binding.

Synonyms are collapsed unless their failure semantics differ. Similar names remain separate when they have different owners or lifetimes.

## 2. Six classification questions

Every candidate concept must answer:

```text
What kind of thing is it?
Which responsibility does it express?
Who owns its authoritative state?
Must it survive Session, process, model, or machine replacement?
Can it produce an external side effect?
What happens under retry, duplication, delay, drift, or partial failure?
```

A concept without clear answers remains descriptive vocabulary rather than protocol.

## 3. Evidence classes

| Class | Meaning | Example |
|---|---|---|
| Classical mechanism | Mature mechanism whose semantics predate Agent systems | process, queue, transaction, lease, trace |
| Product packaging | Multiple responsibilities combined for product simplicity | Codex CLI, Claude Code CLI |
| Proven Ordivon object | Implemented and exercised in a real Ordivon path | Host Task, Runtime Job, Effect Binding |
| Research candidate | Plausible shared object lacking cross-workload evidence | generic Harness checkpoint, ConsequenceEnvelope |
| Domain-local object | Valuable but owned by one world or product | Game TickBatch, Security Campaign |
| Deferred mechanism | Known useful pattern without a current consumer | global plugin registry, distributed consensus |
| Rejected generalization | A local mechanism that should not become shared infrastructure | universal approval engine, one graph for all semantics |

## 4. Mature-standard comparison

A new Ordivon mechanism must be compared against the strongest simpler baseline from its native discipline:

- operating systems for process, files, scheduling, signals, and isolation;
- databases for transactions, journals, snapshots, projections, and conflict control;
- durable workflows for timers, retries, signals, queries, updates, and continuation;
- distributed systems for leases, heartbeats, fencing, idempotency, backpressure, and circuit breaking;
- observability for traces, spans, metrics, logs, and semantic conventions;
- Agent frameworks for model loops, context, handoffs, lifecycle hooks, and checkpoints;
- MCP or provider protocols for capability negotiation and Tool contracts.

Agent scale or fashionable terminology does not make a classical mechanism Agent-native.

## 5. Promotion gates

A research object may enter shared Protocol or Core only when:

1. a realistic failure occurs without it;
2. a second materially different workload needs the same semantics;
3. the authoritative owner is unambiguous;
4. restart and replacement behavior is specified;
5. the object has a deletion or localization falsifier;
6. the measured benefit exceeds implementation and governance cost;
7. it cannot remain a local module, adapter, policy, Skill, or documentation convention.

A repository has an additional gate:

```text
independent release or deployment need
+ at least two real consumers or implementations
+ stable ownership boundary
+ measurable reduction in coupling
> permanent repository and compatibility cost
```

## 6. Design discipline

### 6.1 Separate proposal from commitment

Models and Harnesses may propose:

- plans;
- Task decompositions;
- Action Proposals;
- Tool calls;
- completion;
- memory consolidation;
- Skill changes.

The authoritative component commits only after its own invariants are satisfied.

```text
Harness proposes Task split → Host commits Task graph
Harness proposes completion → Host commits TaskCompleted
Harness requests execution → Runtime admits and records Job
Model claims success → Verification may admit Fact
```

### 6.2 Separate before and after

Before an operation, a mechanism may gate, mutate, route, or require approval. After an operation, the system should record an Event rather than pretend the past can be blocked.

```text
BeforeToolCall → Hook / Policy / Approval
ToolExecuted    → immutable Event / Observation
```

### 6.3 Prefer operations over whole-object replacement

Concurrent components should submit typed operations:

```text
AddEvidence
ReportBlocker
ProposeCompletion
SupersedeAssumption
RenewLease
```

They should not overwrite complete shared Task objects.

## 7. Cost model

For every persistent abstraction measure:

- latency and additional round trips;
- token and context cost;
- serialization and storage cost;
- implementation and migration burden;
- debugging and observability burden;
- provider feature loss;
- interruption and operator-attention cost;
- long-term compatibility surface;
- authority concentration and failure blast radius.

The default disposition is local, thin, and deletable.

## 8. Research output standard

Each retained research question should contain:

- exact question;
- ownership hypothesis;
- mature baselines;
- candidate object model;
- failure matrix;
- minimum experiment;
- measurements;
- evidence required;
- falsifiers and deletion tests;
- explicit non-goals;
- repository consumers.
