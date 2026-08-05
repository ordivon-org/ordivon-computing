# Host, Harness, and Observation Plane P0/P1 Design

Status: designed, not executed.

Plan: `HHO-P0-P1-001`.

## Purpose

Ordivon needs durable, automatically collected evidence across compositions in which:

- Host may use Ordivon Harness, Codex, Hermes, another Harness, or a deterministic executor;
- Ordivon Harness may serve Host, Game, Security, a research runner, or another durable caller;
- Runtime may execute work for any of those paths;
- domain projects retain their own authoritative outcomes;
- formal evaluation can select and replay useful work without becoming the source of product state.

The current implementation proves Host-backed Harness continuity but violates the first two requirements: Harness Run state is durable only because `HostHarnessRunStore` writes Harness objects into Host CAS and Host extension events. The current Track R system also curates selected evidence after execution rather than collecting all supported runs automatically.

This design resolves those pressures in order:

```text
P0: separate durable authority and composition
→ P1: automatic observation from committed owner-native events
→ R3: formal repeated Trials using the automatic evidence path
```

## Design bases

The plan was derived from clean local revisions:

| Component | Observed revision | Relevant current fact |
| --- | --- | --- |
| Computing | `b5bc1348f2a48c6319c9d4dfbe77add34b5dbfe3` | Track R contracts and formal Trial design |
| Host | `1a4027bb26d77a2e051ca933bf664578f071a5a9` | schema-v4 SQLite Journal/CAS and generic extension admission |
| Harness | `796e9f07899a250ea4d87ae3e96f38c7172ff674` | exact Host dependency and `HostHarnessRunStore` |
| Runtime | `ce061a5995d7a59246a103dcc51f0539245209a6` | authoritative Registry, Attempt bundles, Runtime trace, and Workspaces |
| Protocol | `420dc356cb664d75db0f34f356156baebe5843db` | current shared wire dependency |

These revisions are observations, not implementation pins. Each implementation phase records the exact tested revisions in its closeout.

External design bases:

- OpenTelemetry Collector receiver → processor → exporter pipelines and local agent/gateway deployment;
- W3C Trace Context, OpenTelemetry span links, and semantic conventions for cross-process correlation;
- transactional outbox or change-data-capture for reliable event publication without dual writes;
- tracing systems that automatically record model calls, Tool calls, handoffs, guards, and custom events while providing explicit sensitive-data controls.

Ordivon uses these patterns for transport and observation, not for owner-native recovery authority.

## Part I — invariants

## I1 — every owner remains recoverable alone

- Host opens, validates, backs up, restores, and reconstructs Task state without Harness or observation services.
- Harness opens, validates, backs up, restores, and reconstructs Run state without Host or observation services.
- Runtime preserves Job and Attempt truth without Host, Harness, or observation services.
- A domain project preserves its domain outcome without the observation gateway.

## I2 — no lifecycle has two writable authorities

A new Harness Run is written to exactly one Harness store. Host stores a foreign Run binding and observations, not a writable copy of Run state. The observation plane stores a query copy and cannot modify either owner.

## I3 — cross-owner atomicity is not invented

Host and Harness use independent local transactions. Their integration uses stable request identities, immutable contract digests, idempotent start/observe/complete operations, and reconciliation after process or response loss.

## I4 — native identities outrank trace identities

`traceId` and `spanId` correlate work. They do not identify the authoritative Task, Run, Job, Attempt, Artifact, completion decision, or domain outcome.

## I5 — automatic observation is eventually complete, not synchronously required

An owner first commits its authoritative event. Export may lag or retry. Collector failure cannot reinterpret or roll back committed product state.

## I6 — content capture is policy-controlled

Metadata, identities, status, counters, timings, digests, and references are automatic. Prompt text, Context contents, Tool arguments, model output, source bytes, media, and stdout/stderr are captured only as bounded private references or under an explicit content policy. Secrets and raw private Chain-of-Thought are forbidden.

## I7 — observation is not evaluation

All supported runs produce observations. Only an admitted Task, versioned environment, independent verifier, repeated Trial policy, and explicit Dataset admission produce formal evaluation evidence.

## Part II — P0 independent persistence and composition

## P0 objective

At P0 closeout:

1. Host has a production state root and no runtime dependency on `ordivon-harness`;
2. Harness has a production state root and its core runtime no longer depends on `ordivon-host`;
3. Host can use a fake or external Harness through a narrow adapter;
4. Harness can run through a fake/domain caller without Host;
5. Host + Ordivon Harness works through an integration adapter;
6. each side survives independent process replacement;
7. existing Host-backed Harness evidence remains inspectable;
8. no new Run is dual-written.

P0 deliberately does not deploy observation infrastructure.

## P0-A — freeze current semantics before storage movement

Before changing persistence, freeze the semantic inventory currently encoded in Host-backed Harness state.

### Required object inventory

- Task Contract and Task Attempt reference;
- Harness Assignment and generation;
- Tool Grant and catalog snapshot;
- native Run Contract;
- Run state and delta chain;
- Run Snapshot;
- Provider Call claim, dispatch, completion, failure, and UNKNOWN records;
- Tool Step Intent, Dispatch Fence, Receipt, previous Receipt, and Observation;
- canonical Harness Trace;
- Run Receipt;
- recovery assessment and abandonment;
- CompletionProposal, CompletionVerification, and completion decision receipt;
- caller, Runtime Workspace, Runtime Job, Artifact, source, and System Manifest references.

For every persisted type, record:

- current wire `kind` and `schemaVersion`;
- semantic identity and digest rules;
- owner and mutable lifecycle;
- current Host event kind and CAS reference role;
- required causal predecessors;
- current Doctor/history validation;
- legacy decode requirements;
- privacy class.

### P0-A gate

A generated inventory and compatibility test must prove that current accepted, rejected, paused, UNKNOWN, recovered, and superseded fixtures can be decoded without importing the new store implementation.

## P0-B — caller-neutral core contracts

### `HarnessRunContract`

The new immutable core contract contains:

```text
schemaVersion
harnessRunId
harnessImplementation
callerRef
callerRunRef
objectiveRef
contextRefs + contextDigest
provider / adapter / requested model
Tool catalog + Tool grant digests
budget
completionContract
sourceRefs
priorArtifactRefs
systemManifestRef
correlationContext
privacyPolicy
createdAt / optional deadline
integrity
```

It must not contain:

- Host `TaskProjection`;
- Host lease or stream revision;
- Host CAS object metadata;
- Host extension event kinds;
- Runtime credentials;
- Provider secrets;
- domain-specific success fields.

### `HarnessCallerPort`

The caller integration port is intentionally narrower than a Host:

```text
load_contract(caller_ref)
record_run_binding(caller_ref, harness_run_ref)
receive_progress(caller_ref, observation_ref)
receive_completion(caller_ref, completion_proposal_ref)
receive_failure(caller_ref, failure_ref)
```

The standalone runner may use a no-op or file-backed caller implementation. A domain project can bind these calls to its own Actor, Session, Contest, or Trial state.

### Host `ExternalExecutorAdapter`

Host defines a structural adapter interface around foreign execution:

```text
start(request_identity, task_attempt_ref, bounded_context, authority, completion_contract)
observe(external_run_ref)
cancel(external_run_ref)
recover(external_run_ref)
collect_completion(external_run_ref)
```

The Host stores an immutable `ExternalRunBinding` with:

- adapter implementation identity;
- request identity;
- foreign Run reference;
- contract digest;
- Task and Attempt references;
- correlation context;
- observed status and Evidence references;
- last reconciled foreign revision.

The adapter cannot commit Host Task transitions. It returns observations and proposals that Host admits through its existing revision, lease, verification, and TaskOutcome rules.

## P0-C — independent Harness store

### State root

Default production layout:

```text
/var/lib/ordivon/harness/
├── harness.sqlite3
├── objects/
├── receipts/
├── backups/
└── quarantine/
```

Permissions:

- state root and CAS directories: `0700`;
- database, WAL/SHM, objects, manifests, and receipts: `0600`;
- symlink roots, databases, objects, and credential files fail closed.

### Storage API

The core loop depends on a store protocol, not `HostHarnessRunStore`:

```text
HarnessStore
├── create_run(contract)
├── load_run(run_id)
├── append_event(expected_revision, event, object_refs)
├── acquire_run_lease(run_id, owner, ttl)
├── release_run_lease(...)
├── put_object(value, kind)
├── get_object(digest, expected_kind)
├── inspect_object(digest)
├── list_run_events(run_id, after_sequence)
├── current_snapshot(run_id)
├── provider_call(...)
├── tool_step(...)
└── terminal_record(run_id)
```

The public protocol is behavioral. SQLite table names are internal.

### SQLite schema v1

Minimum tables:

| Table | Purpose |
| --- | --- |
| `schema_info` | current schema version and creation identity |
| `schema_migrations` | ordered migration receipts |
| `runs` | materialized current Run projection and revision |
| `run_events` | append-only authoritative event stream |
| `object_refs` | CAS metadata and kind |
| `run_object_refs` | causal object retention by Run/event/role |
| `run_leases` | bounded single-writer Run admission |
| `provider_calls` | materialized Provider Call claim and terminal status |
| `tool_steps` | materialized Intent/Fence/Receipt/Observation status |
| `caller_bindings` | immutable caller and foreign correlation references |
| `object_validation` | trusted-local verified-object cache |

Provider Call and Tool Step tables are checked projections of `run_events`; they are not independent histories.

### Harness event families

The Journal includes owner-native events such as:

```text
harness.run-created
harness.run-started
harness.run-resumed
harness.snapshot-recorded
harness.provider-call-claimed
harness.provider-call-dispatching
harness.provider-call-completed
harness.provider-call-failed
harness.provider-call-unknown
harness.tool-step-prepared
harness.tool-step-dispatched
harness.tool-step-recorded
harness.tool-step-unknown
harness.tool-step-reconciled
harness.run-paused
harness.run-stopped
harness.completion-proposed
harness.run-failed
harness.run-completed
harness.run-abandoned
```

The current in-memory `HarnessRunEvent` Trace remains useful but is no longer the only ordered durable event history. Trace events may be projected from or bound to Journal events; the two sequences must have an explicit mapping and may not silently diverge.

### Operations

Required CLI surface:

```text
ordivon-harness init
ordivon-harness doctor [--history]
ordivon-harness inspect RUN_ID
ordivon-harness events RUN_ID
ordivon-harness backup DESTINATION
ordivon-harness verify-backup BACKUP
ordivon-harness restore BACKUP --destination ...
ordivon-harness run --contract ...
ordivon-harness resume RUN_ID
ordivon-harness recover RUN_ID
ordivon-harness cancel RUN_ID
```

Only `init` creates a missing state root. Normal reads and recovery reject an absent database.

## P0-D — remove the hard Host dependency from Harness core

The package becomes layered:

```text
ordivon_harness core
├── contracts
├── store protocol + SQLite/CAS implementation
├── Agent loop
├── Provider adapters
├── Tool protocols
├── Run recovery
└── standalone Runner

ordivon_harness.integrations.host
├── Host Assignment → HarnessRunContract adapter
├── Host caller port
├── Host external-executor adapter implementation
└── legacy Host-backed history reader
```

Acceptance rules:

- importing and installing core Harness does not import or install `ordivon-host`;
- Host integration may be an optional dependency extra or application composition package;
- `_host_compat` is reduced to the integration boundary and legacy reader;
- `DomainToolLoopRunner` can optionally persist through `HarnessStore` instead of remaining an in-memory-only loop;
- Host continues not to import `ordivon-harness` in core source.

The Protocol package may own only wire-stable cross-owner references after two independent implementations need them. P0 does not promote the internal Harness lifecycle into the shared Protocol.

## P0-E — no-dual-write cutover

### Legacy path

`HostHarnessRunStore` becomes a frozen compatibility implementation named and documented as legacy. It remains capable of:

- decoding retained Host-backed Harness objects;
- validating historical causal references;
- inspecting and exporting historical evidence;
- completing a specifically admitted pre-cutover recovery only if the cutover policy explicitly permits it.

Default cutover policy is stricter: no nonterminal legacy Run may exist at cutover.

### New path

Every post-cutover Run:

1. receives a stable caller request identity;
2. commits `HarnessRunContract` and `harness.run-created` in Harness;
3. returns the immutable Harness Run reference;
4. lets the caller record the foreign binding idempotently;
5. proceeds only through the Harness store;
6. returns progress and completion references to the caller;
7. never writes Run, Snapshot, Provider Call, Tool Step, or Trace bytes to Host.

### Cross-store crash matrix

| Crash or response loss | Reconciliation rule |
| --- | --- |
| Host request committed before Harness Run creation | repeat `start` with the same request identity; create at most one Run |
| Harness Run created before Host binding commit | discover by caller request identity and attach the existing Run |
| Provider Call admitted before response reaches caller | query Harness Call identity; never invoke again without recovery policy |
| Runtime Job admitted before Harness receipt | reconcile the original Runtime request identity |
| Harness completion committed before Host decision | replay the same immutable CompletionProposal reference |
| Host decision committed before caller receives response | return the existing decision and TaskOutcome idempotently |
| observation exporter unavailable | owner state continues; export later from Journal sequence |

## P0 acceptance matrix

### Independent package and process tests

- Host complete suite passes with `ordivon-harness` absent from the environment.
- Harness complete core suite passes with `ordivon-host` absent from the environment.
- Harness standalone scripted Run survives close/reopen and resumes from its own Snapshot.
- Host Task survives close/reopen while its selected executor is unavailable.

### Composition tests

- Host + fake external Harness produces one binding, observations, independent verification, and one TaskOutcome.
- Host + Ordivon Harness adapter produces separately valid Host and Harness histories.
- standalone Harness + fake caller produces a complete Run without Host objects.
- domain Harness + domain-owned Tool bridge persists the complete Run without synthetic Host Task state.

### Failure tests

- duplicate `start` request creates one Harness Run;
- stale caller proposal cannot advance Host;
- stale Run lease cannot append Harness state;
- cross-process Provider Call and Runtime response loss recover without redispatch;
- corrupt/missing Harness CAS fails Doctor and recovery closed;
- mismatched foreign Run reference fails Host reconciliation;
- terminal Harness Run cannot reopen;
- terminal Host Task cannot be changed by Harness.

### Migration tests

- every frozen Host-backed fixture remains inspectable;
- active legacy Run inventory is empty before default cutover;
- no test observes the same new Run written to both stores;
- historical bytes are not rewritten merely to match the new layout.

### Operational tests

- private modes and symlink rejection;
- schema migration backup and rollback test;
- online backup, independent restore, and full byte verification;
- 1,000 Runs and 100,000 Run events load test;
- current Run inspect and resume preparation remain under one second on the recorded target machine at that scale;
- full-history Doctor reports measured duration separately and may be slower.

## P0 stop conditions

Stop and redesign if:

- Run recovery still requires mutable Host projection fields;
- Host must decode Harness internal event schemas to remain correct;
- any new Run requires cross-database dual writes;
- caller-neutral contracts flatten Provider or domain lifecycles materially;
- legacy compatibility requires making Host the continuing Harness byte owner;
- independent storage introduces duplicate physical Effect dispatch that cannot be reconciled by stable identities;
- the store protocol becomes a universal workflow or domain state model.

## P0 closeout outputs

```text
host closeout + exact gate receipt
harness closeout + exact gate receipt
cross-composition receipt
legacy compatibility receipt
cutover inventory
state-root and backup receipts
fault matrix
performance receipt
P0 decision: proceed / narrow / revert
```

## Part III — P1 automatic observation

## P1 prerequisite

P1 begins only after P0 proves two independent Journals and a stable cross-owner correlation path. P1 may prototype its envelope earlier, but no production exporter is admitted against the Host-backed Harness layout.

## P1 objective

At P1 closeout:

- Host, Harness, and Runtime automatically export all admitted owner-native events;
- a standalone Harness Run and a Host using an external fake Harness both appear in one queryable observation store;
- Host → Ordivon Harness → Runtime work is linked across three independent authorities;
- collector or gateway outage loses no committed source event;
- duplicate delivery creates no duplicate catalog event;
- sensitive payload policy is enforced;
- Track R can project a Trial from observation references without copying owner databases;
- no dashboard or heavy analytical platform is required.

## P1-A — observation contract

### Envelope

`ordivon.observation-envelope.v1` contains:

```text
schemaVersion
kind
eventId
occurredAt
exportedAt
source
  projectId
  componentId
  instanceId
  streamId
  sequence
  nativeKind
  nativeId
  nativeRevision
correlation
  traceId
  spanId
  parentSpanId
  links[]
references
  callerRunId
  goalId
  taskId
  taskAttemptId
  assignmentId
  harnessRunId
  providerCallId
  toolStepId
  workspaceId
  runtimeJobId
  runtimeAttemptId
  artifactDigests[]
configuration
  sourceRevision
  systemManifestRef
  implementationId
attributes
metrics
outcome
privacy
payloadRef
integrity
```

Required properties:

- `eventId` is stable across retries;
- `streamId + sequence` is strictly ordered for one owner stream;
- absent measurements are absent or `null`, never invented zeroes;
- payload bytes are bounded and canonical;
- references may be unknown but must not be fabricated;
- all cross-owner links identify their relation type.

### Event identity

Owner event journals use the native event ID when globally stable. Other sources derive:

```text
sha256(projectId, componentId, instanceId, streamId, sequence, native event digest)
```

The gateway validates the supplied digest but does not generate replacement identities for malformed events.

### Trace context

- propagate W3C `traceparent` and `tracestate` across HTTP, MCP, subprocess environment carriers, and adapter calls where safe;
- use OpenTelemetry span links when work is asynchronous, recovered, joined, or correlated after creation rather than forcing a false parent;
- use baggage only for bounded non-secret correlation attributes;
- never use Trace Context as authorization or idempotency identity.

### Semantic attributes

Common resource attributes:

```text
service.name
service.version
service.instance.id
deployment.environment.name
ordivon.project.id
ordivon.component.id
ordivon.source.revision
ordivon.system_manifest.digest
```

Common Run attributes:

```text
ordivon.run.id
ordivon.native.kind
ordivon.native.id
ordivon.native.revision
ordivon.task.id
ordivon.task_attempt.id
ordivon.harness_run.id
ordivon.runtime.job.id
ordivon.outcome.class
ordivon.privacy.class
```

Use current OpenTelemetry GenAI semantic conventions for compatible model and Tool span attributes, but pin the mapping version. Ordivon native events remain valid if those conventions evolve.

## P1-B — source export patterns

### Host and Harness: Journal-as-Outbox

Each exporter reads only committed events:

```text
Journal event sequence N
→ map through versioned owner exporter
→ send observation envelope
→ receive gateway acknowledgement
→ advance consumer cursor to N
```

The cursor is consumer state, not authority state. Repeating an event is safe.

Required tables or files:

```text
observation_consumers
  consumer_id
  last_acknowledged_sequence
  exporter_version
  updated_at
```

A broken exporter mapping quarantines the event and reports lag. It cannot skip an event silently to advance the cursor.

### Runtime: Registry/Attempt exporter

Runtime maps:

- Workspace lifecycle;
- Job admission and state changes;
- Attempt creation and terminal evidence;
- Artifact metadata;
- cancellation, recovery, orphan, quarantine, and lifecycle receipts;
- request identity and foreign references.

Runtime exports physical status only. It never emits Host Task success or Harness completion.

### Domain projects: transactional outbox

A project without an append-only Journal writes domain state and `observation_outbox` in the same transaction. A generic relay exports rows at least once and advances a consumer checkpoint after gateway acknowledgement.

P1 provides a minimal Python SDK and JSON contract. Rust and TypeScript implementations may remain owner-local until repeated consumers justify shared code generation.

## P1-C — local observation gateway

### Prototype ownership

The prototype lives under Computing during P1. It is deployable but experimental. Repository extraction is deferred.

### State root

```text
/var/lib/ordivon/observation/
├── observation.sqlite3
├── receipts/
├── quarantine/
├── collector-state/
├── exports/
└── backups/
```

### Ingest boundary

- Unix socket by default for local native producers;
- optional loopback HTTP for OTLP or external-process adapters;
- no public network listener;
- peer identity and configured producer allowlist;
- bounded request size, batch size, and decompression ratio;
- one SQLite writer.

### Observation database

Minimum tables:

| Table | Purpose |
| --- | --- |
| `events` | exact canonical envelope bytes keyed by `event_id` |
| `source_streams` | last sequence, gap, duplicate, and producer metadata |
| `event_links` | indexed native and cross-owner references |
| `artifact_refs` | digest, owner, location class, and privacy metadata |
| `ingest_receipts` | accepted, duplicate, quarantined, and rejected batches |
| `producer_checkpoints` | optional gateway hints, not owner export authority |
| `schema_versions` | envelope and mapping support |
| `quarantine` | malformed, secret-bearing, gap, or unsupported events |

Ingest transaction:

1. validate schema, canonical digest, producer identity, privacy policy, and source sequence;
2. insert the exact envelope by `event_id` or recognize an exact duplicate;
3. index links and source progress;
4. persist an ingest receipt;
5. commit;
6. acknowledge the producer.

A same-ID/different-bytes event is corruption and is quarantined. A sequence gap is explicit and blocks a complete-stream claim but does not erase later data.

### Query CLI

```text
ordivon-observe status
ordivon-observe producers
ordivon-observe lag
ordivon-observe event EVENT_ID
ordivon-observe trace TRACE_ID
ordivon-observe run RUN_ID
ordivon-observe task TASK_ID
ordivon-observe failures
ordivon-observe missing-links
ordivon-observe export --format jsonl|parquet
ordivon-observe doctor
ordivon-observe backup / verify-backup
```

The default interface is structured JSON. No dashboard is required in P1.

## P1-D — OpenTelemetry bridge

OpenTelemetry is the interoperability and routing layer.

### Native Ordivon events

The gateway projects accepted envelopes into:

- spans for bounded operations with start/end;
- span events or logs for point facts;
- metrics for counters, durations, queue lag, token usage, cost, failure classes, and resource measurements.

The exact canonical envelope remains in the local observation database. OTel export is a derived projection.

### External frameworks

Frameworks with existing OpenTelemetry or custom trace processors may send OTLP to a loopback Collector. An adapter maps their spans into bounded external-Harness observations and preserves the original trace identity and backend reference. It does not invent Ordivon Harness Run semantics.

### Collector deployment

P1 uses one local Collector in agent/gateway form:

```text
receivers: OTLP loopback
processors: memory limit, batch, resource normalization, privacy filters
exporters: local gateway/derived backend, optional debug during acceptance
extensions: health check and file-backed persistent queue
```

Persistent queue and retry are enabled for downstream export. The owner Journal remains the stronger loss-prevention boundary; Collector persistence protects the derived telemetry path after ingest.

## P1-E — privacy and content policy

### Privacy classes

```text
public_metadata
private_metadata
private_content_ref
restricted_content_ref
secret_forbidden
```

Default by signal:

| Signal | Default capture |
| --- | --- |
| identities, times, status, counters, digests | inline private metadata |
| prompt and Context | digest + owner-native reference |
| model output | digest + private Harness object reference |
| Tool name and outcome | inline metadata |
| Tool arguments/results | policy-classified digest/reference |
| stdout/stderr | Runtime Artifact reference |
| source files and patches | Git/Runtime Artifact reference |
| video, image, audio | Studio/domain Artifact reference |
| credentials, tokens, cookies, private keys | reject and quarantine metadata only |
| raw private Chain-of-Thought | never required or captured |

### Redaction boundary

Emitters classify before export. The gateway independently rejects obvious secret-like keys and invalid privacy declarations. Observation does not promise semantic redaction of arbitrary user content; sensitive owner stores remain private.

## P1-F — retention and export

P1 performs no automatic deletion.

- owner-native retention remains defined by each product;
- observation events are retained until explicit operator policy exists;
- large payloads are not copied by default;
- JSONL.zst and Parquet are derived exports, not authority;
- DuckDB may query Parquet on demand;
- external SaaS export is optional and must respect privacy class and consent.

## P1 producer sequence

Mandatory P1 producers:

1. Host;
2. Harness;
3. Runtime.

Next producers after core closeout:

1. Game Session/Agent events;
2. Security Contest/Actor events;
3. Studio Production/Render/QC events;
4. World integration events;
5. Human study execution events;
6. Web build/publication operational events.

Each domain adds only:

- common Trace/Run correlation;
- a bounded set of domain event kinds;
- one domain result reference;
- privacy mapping;
- optional Eval adapter.

## P1 acceptance matrix

### Reliability

- stop the gateway while producers commit 10,000 events; after restart, ingest all events with zero missing source sequences;
- kill an exporter after gateway commit but before acknowledgement; retry produces one catalog row and one exact-duplicate receipt;
- restart Collector with queued telemetry; derived export resumes without affecting owner state;
- corrupt mapping or unsupported schema enters quarantine and does not advance the source cursor;
- sequence gaps are visible in `status`, `lag`, and Doctor.

### Correlation

- standalone Harness Run is queryable without Host IDs;
- Host + fake external Harness links Task/Attempt to a foreign Run without Ordivon Harness types;
- Host + Ordivon Harness + Runtime links Task, Harness Run, Provider Call, Tool Step, Workspace, Job, Attempt, Artifact, verifier, decision, and TaskOutcome;
- asynchronous response-loss recovery uses links and native request IDs without false parentage;
- one Trace may link multiple owner streams without becoming their authority.

### Privacy

- secret-like environment keys and bearer values never enter accepted events;
- default model and Tool spans contain digests/references rather than content;
- explicit bounded-content policy produces private content references and audit receipts;
- raw reasoning text is absent from schemas and test fixtures;
- external export rejects restricted classes unless an explicit policy permits them.

### Performance

On the recorded local target:

- ingest 100 events per second for ten minutes without sequence loss;
- P95 gateway acknowledgement under two seconds;
- owner operations never synchronously wait for the gateway;
- exporter lag and disk use remain queryable;
- common queries over one million metadata-only events complete within five seconds;
- measure CPU, memory, database size, WAL growth, and derived export cost before setting production retention.

### Evaluation integration

- select one complete Harness trajectory from observation queries;
- produce Track R native evidence references and digests without copying owner databases;
- demonstrate that process exit success alone cannot create an accepted Result;
- candidate extraction remains explicit and does not auto-admit a Dataset Task;
- formal R3 runner reads stable owner references rather than temporary receipt paths.

## P1 stop conditions

Stop and redesign if:

- observation loss can occur despite an intact owner Journal;
- exporters require modifying owner state outside normal owner transactions;
- gateway availability becomes necessary for Host, Harness, Runtime, or domain correctness;
- correlation requires copying entire owner databases;
- OTel mapping replaces native event identity or recovery state;
- sensitive content is accepted without explicit policy;
- query value does not justify the service and storage cost;
- the prototype grows into scheduling, routing, model selection, or Task authority.

## P1 closeout outputs

```text
observation envelope and mapping version
Host exporter receipt
Harness exporter receipt
Runtime exporter receipt
gateway deployment and Doctor receipt
10,000-event outage/recovery receipt
cross-owner correlation receipt
privacy acceptance receipt
one-million-event query benchmark
Track R projection receipt
P1 decision: retain in Computing / extract / narrow / delete
```

## Part IV — implementation sequence

## P0 implementation order

### P0.1 — contracts and inventory

Repositories: Computing, Harness.

- freeze persisted Harness object/event inventory;
- define caller-neutral Run Contract and store protocol;
- add compatibility tests around existing Host-backed fixtures;
- define cutover and active-legacy inventory commands.

No behavior cutover.

### P0.2 — Harness store and operations

Repository: Harness.

- SQLite/CAS schema v1;
- migrations, private modes, backup/restore, Doctor;
- store implementation behind the protocol;
- persist scripted standalone Run, Snapshot, Provider Call, Tool Step, Trace, and terminal record;
- load and resume after process replacement.

Host integration still uses legacy storage during this subphase.

### P0.3 — standalone core

Repository: Harness.

- remove hard Host dependency from core package;
- make Runner accept `HarnessStore`, caller port, Tool bridge, and adapter;
- persist DomainToolLoopRunner when a store is supplied;
- isolate Host integration and legacy reader.

### P0.4 — Host external executor boundary

Repository: Host plus Harness integration.

- define foreign Run binding and adapter interface;
- fake external Harness acceptance;
- Ordivon Harness adapter;
- idempotent start, observe, cancel, recover, and completion reconciliation.

### P0.5 — cutover and closeout

- verify no active legacy Run;
- default all new Ordivon Harness Runs to Harness store;
- retain legacy read-only inspection;
- deploy `/var/lib/ordivon/host` and `/var/lib/ordivon/harness`;
- execute full gates and fault matrix.

## P1 implementation order

### P1.1 — envelope and gateway skeleton

Repository: Computing experiment.

- schema, canonicalization, privacy classes, and query model;
- SQLite ingest store and Unix socket;
- exact duplicate and corruption behavior;
- CLI, Doctor, backup, and synthetic producer tests.

### P1.2 — Journal exporters

Repositories: Host, Harness.

- versioned native-event mapping;
- consumer cursor;
- lag and quarantine;
- outage/retry acceptance.

### P1.3 — Runtime exporter

Repository: Runtime.

- Registry and Attempt event mapping;
- Artifact and terminal-evidence references;
- physical-status-only invariant;
- correlation through existing foreign references.

### P1.4 — OpenTelemetry bridge

- local Collector configuration;
- trace/span/link projection;
- persistent queue and retry;
- external Harness OTLP intake;
- sensitive-data tests.

### P1.5 — Track R integration and closeout

- query one complete cross-owner trajectory;
- project formal Trial references;
- update R3 System Manifest and runner prerequisites;
- measure storage and query behavior;
- decide whether to extract `ordivon-observation`.

## Part V — repository admission gate

Do not create an Observation repository during P0.

At P1 closeout, extract only if all hold:

1. Host, Harness, and Runtime are active independent producers;
2. operations and Track R are independent recurring consumers;
3. the gateway has a deployment, migration, backup, privacy, and retention lifecycle distinct from Computing research;
4. keeping it in Computing creates release or authority distortion;
5. removing it would recreate duplicated exporters, incompatible correlation, or loss of automatic evidence;
6. the extracted role remains observation only and does not absorb Task, Run, Runtime, domain, evaluation, or media authority.

Candidate name: `ordivon-observation`. This design does not register or create it.

## Part VI — effect on formal Trials

The existing formal Trial plan `HHR-R3-001` remains valid as a workload and evidence design, but execution is blocked.

R3 resumes after:

- P0 independent Host/Harness persistence passes;
- P1 Host/Harness/Runtime automatic observation passes;
- one deterministic cross-owner trajectory is queryable from the observation store;
- System Manifest capture includes observation contract and mapping versions;
- the formal runner writes owner references rather than assuming Harness data lives in Host CAS.

The first formal Trial campaign then becomes the first repeated consumer of the automatic observation path rather than another isolated data-production script.
