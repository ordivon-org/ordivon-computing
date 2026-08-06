# HHO-P1 Execution Plan

Status: Level A complete; Minimum Core M1 contract, in-process Gateway, schemas, privacy rejection, and synthetic rebuild fixture implemented; run-once owner exporters pending.

Plan: `HHO-P0-P1-001`, phase `HHO-P1`.

Architecture authority remains [`P0-P1-DESIGN.md`](P0-P1-DESIGN.md). This document converts its P1 boundary into repository work packages, dependency gates, concrete storage and exporter contracts, acceptance receipts, rollback conditions, and the handoff into formal Trials.

## 1. Decision

P1 builds a local, non-authoritative observation path over committed Host, Harness, and Runtime facts.

It does **not** create another Task, Run, Job, completion, recovery, or domain authority. It does not place the gateway on an owner write path. It does not require Kafka, ClickHouse, a dashboard, a global scheduler, or a new repository.

The execution strategy is split into two gates:

- **P1 Core** — canonical observation envelope, local gateway, three read-only owner exporters, cross-owner trajectory queries, privacy enforcement, and Track R projection. P1 Core unblocks formal Trials.
- **P1 Interop** — OpenTelemetry projection and loopback Collector integration. This is an interoperability layer and does not block formal Trials once P1 Core has passed.

## 1.1 Level A execution correction

The full P1 design remains the long-term hardening envelope, but it no longer blocks the first formal Trial as one indivisible production project. Execution is split into:

- **P1 Minimum Experimental Core** — canonical contract, in-process SQLite ingest, run-once read-only Host/Harness/Runtime exporters, cross-owner trajectory query, privacy rejection, rebuild determinism, and one stable `ObservationSelectionManifest`. This is the only Observation prerequisite for the first R3 deterministic smoke and sequential baseline.
- **P1 Production Hardening** — Unix-socket daemon, follow services, systemd packaging, long outage/load gates, million-event query benchmark, operational backup/restore, OpenTelemetry bridge, Collector, and repository extraction. These require a recurring consumer and do not block the first R3 campaign.

Level A is complete. Harness `f098f9492ab788068fd09da771bffc21e0fdc1b3` is remote-reachable, pins Host `7b17807784cc52f0be4f1786719f6dc20deb92c8`, and carries current live and 1,000-Run/100,000-Event receipts for implementation `f7e03aa78fec63237df6690c0c8f85e4a2ef76c1`. Computing retains the exact release vector and a staging-only backup/restore/cutover rehearsal at `a10c10f23215f02e1bddd2c567377193c0a144f8`. Production authority remains inactive by design and does not block P1.

Run Actor scheduling, Child Runs, Prime/RLM Engine integration, Runtime Workers, graph storage, and continual Harness are outside P1 and are not prerequisites for TCG-P0 or the first single-Actor comparison.

## 2. Current baseline

The execution plan was prepared against these local revisions:

| Repository | Revision | Relevant fact |
| --- | --- | --- |
| `ordivon-computing` | `a10c10f23215f02e1bddd2c567377193c0a144f8` | Level A closeout, release vector, and staging rehearsal baseline consumed by M1 |
| `ordivon-host` | `7b17807784cc52f0be4f1786719f6dc20deb92c8` | remote-reachable schema-v4 Journal/CAS and external executor boundary |
| `ordivon-harness` | `f098f9492ab788068fd09da771bffc21e0fdc1b3` | remote-reachable exact Host pin, independent Store, live H2 and scale evidence |
| `ordivon-runtime` | `ce061a5995d7a59246a103dcc51f0539245209a6` | remote-reachable append-only Job streams and real system acceptance |
| `ordivon-protocol` package | `420dc356cb664d75db0f34f356156baebe5843db` | current pinned cross-repository wire package |

P0 is accepted for research and release progression. Atomic bounded Harness admission, the 1,000-Run/100,000-Event gate, exact remote Host pin, clean wheel installation, live H2 journey, Runtime system acceptance, and staging backup/restore/cutover/rollback receipts all pass. Production Host/Harness roots remain absent and production authority is not activated.

Run-once exporters may now be developed and accepted against exact owner revisions and temporary or read-only owner stores. No exporter service is enabled on a production path in the Minimum Core.

## 3. Non-negotiable execution invariants

### 3.1 Owner databases are read-only to P1

Host, Harness, and Runtime exporters open their owner stores read-only. P1 adds no observation cursor, trigger, outbox row, or schema migration to an existing authority database.

Exporter checkpoints, mapping failures, retry receipts, and lag state live in observation-owned sidecar state. Removing P1 must leave all owner databases byte-compatible with their original schemas.

### 3.2 Commit first, export later

An owner transaction commits before an exporter can observe it. Gateway, exporter, or Collector failure cannot fail or reinterpret the owner operation.

### 3.3 Delivery is at least once

Exporter acknowledgement is recorded only after gateway commit. A crash after gateway commit but before checkpoint commit resends the same native event. Exact duplicates are accepted; same identity with different bytes is corruption.

### 3.4 Native identity and sequence remain primary

Trace IDs help navigate work but do not identify Task, Harness Run, Runtime Job, Artifact, verification, or completion. Native owner IDs and sequence rules remain the source of completeness and replay.

### 3.5 Mapping is allowlisted

Exporters construct a bounded envelope from explicitly mapped fields. They never serialize an owner event payload wholesale. Prompt text, model output, Tool arguments/results, source bytes, patches, and stdout/stderr default to owner-native digest or Artifact references.

### 3.6 OpenTelemetry is downstream

OTel consumes accepted observation envelopes. It does not read owner stores directly and is never required for P1 Core correctness.

### 3.7 Observation is sensing, not experiment control

P1 must be useful to a later continuous experiment loop without acquiring its authority.

- P1 reports committed events, typed relations, evidence references, lag, and completeness per native stream.
- P1 does not decide whether a Trial is valid, improved, regressed, selection-eligible, or worth another round.
- Track R freezes the exact event selection used by a Trial through an `ObservationSelectionManifest`; the Gateway does not create Trial or Campaign state.
- External experiment identities may appear as namespaced relation targets, but remain owned by the experiment system that created them.
- Negative, invalid, unknown, and incomplete experiment outcomes must remain distinguishable above P1 rather than being flattened into an Observation outcome.

The post-P1 design is [`../experiment-loop-v0/EXECUTION-PLAN.md`](../experiment-loop-v0/EXECUTION-PLAN.md). Its existence does not expand the P1 closeout gate beyond evidence needed by the first formal Trial campaign.

## 4. Target topology

```text
Host Journal/CAS  ── read-only Host exporter ─────┐
Harness Journal/CAS ─ read-only Harness exporter ─┼─ Unix socket ─ Observation Gateway
Runtime Registry ─── read-only Runtime exporter ──┘                  │
                                                                      ├─ SQLite catalog
                                                                      ├─ JSON queries
                                                                      ├─ Track R projection
                                                                      └─ derived OTel bridge

Exporter checkpoint/receipts:
/var/lib/ordivon/observation/exporters/<producer>/

Gateway state:
/var/lib/ordivon/observation/gateway/
```

There is no cross-owner transaction. Correlation is reconstructed from committed native references.

## 5. Observation contract v1

### 5.1 Canonical envelope

The implementation freezes a smaller envelope than the earlier wide reference draft. Cross-owner identities use typed relations rather than a permanently expanding nullable reference object.

```text
schemaVersion: 1
kind: ordivon.observation-envelope
eventId
occurredAtMs
source:
  projectId
  componentId
  instanceId
  streamId
  sequence
  nativeKind
  nativeId
  nativeRevision?
  nativeDigest
  mappingVersion
relations[]:
  relationType
  targetKind
  targetId
  targetDigest?
trace?:
  traceId?
  spanId?
  parentSpanId?
  links[]
attributes
measurements
outcome?
privacy:
  class
  policyId
  containsInlineContent
payloadRef?:
  owner
  kind
  nativeId?
  digest
  locatorClass
integrity:
  algorithm
  canonicalization
  payloadDigest
```

Rules:

- `occurredAtMs` is owner-native event time and participates in canonical bytes;
- dynamic exporter and gateway times do **not** participate in canonical Envelope bytes; they live in exporter and ingest receipts so rebuilding the same native event cannot create false corruption;
- `eventId` is stable for one native event across retries and mapping re-execution;
- `nativeDigest` binds the source record used by the mapping;
- `source.streamId + source.sequence` defines completeness only inside that native stream;
- `attributes` contains allowlisted JSON scalars or bounded scalar arrays, not arbitrary native payloads;
- `measurements` contains numeric values with explicit units in the key or value object;
- absent facts are absent, never converted to zero or an invented status;
- `payloadRef` identifies owner-native evidence without granting access or copying content;
- a mapping version change does not silently rewrite accepted envelopes.

### 5.2 Event identity

The canonical event identity is derived from stable source identity, not from mapped bytes:

```text
sha256(projectId, componentId, instanceId, streamId, nativeId)
```

The gateway separately compares the complete canonical envelope digest. Therefore:

- same event ID + same canonical bytes = exact duplicate;
- same event ID + different canonical bytes = corruption;
- a corrected mapping requires a new mapping version and an explicit remap procedure, not silent replacement.

### 5.3 Relation vocabulary

P1 Core freezes only the relations required for the three-owner trajectory:

```text
belongs_to
requested_by
executes
observes
produced
references
proposes_for
verifies
accepted_by
reconciles
caused_by
derived_from
evaluates
linked_to
```

A relation is navigational evidence, not authority transfer. Unknown relation kinds are rejected until the contract version changes. `targetKind` is a bounded namespaced owner-native type rather than a fixed union of nullable Envelope fields; examples include `ordivon.eval.campaign`, `ordivon.eval.configuration`, `ordivon.eval.trial`, and `ordivon.eval.grader-result`. Accepting such a target does not make P1 its semantic owner.

### 5.4 Native stream mapping

| Producer | Stream | Sequence | Native identity |
| --- | --- | --- | --- |
| Host | one stream per Host Journal instance | global `events.sequence` | Host `event_id` |
| Harness | one stream per Harness Journal instance | global `run_events.sequence` | Harness `event_id` |
| Runtime | one stream per Runtime Job | `job_events.event_sequence` | Runtime `event_id` |

Runtime deliberately uses per-Job streams because the Registry has an append-only per-Job sequence but no durable global event sequence. P1 does not add a global observation column to Runtime.

### 5.5 Ingest batch protocol

A native batch contains one producer instance and one source stream:

```text
schemaVersion
requestId
producerIdentity
streamId
firstSequence
lastSequence
events[]
batchDigest
```

Gateway rules:

1. verify producer allowlist, batch digest, envelope schema, mapping version, privacy policy, and canonical event digests;
2. require a contiguous source sequence range;
3. accept new events and exact duplicates in one transaction;
4. reject a sequence gap, unsupported mapping, privacy violation, or same-ID/different-bytes corruption without advancing completeness;
5. commit an ingest receipt;
6. acknowledge only after commit.

The acknowledgement includes accepted, duplicate, and rejected counts; source range; gateway receipt digest; and the exact contiguous sequence committed.

## 6. Observation-owned state

### 6.1 State layout

```text
/var/lib/ordivon/observation/
├── gateway/
│   ├── observation.sqlite3
│   ├── receipts/
│   ├── quarantine/
│   ├── backups/
│   └── exports/
├── exporters/
│   ├── host/
│   │   ├── checkpoint.sqlite3
│   │   ├── receipts/
│   │   └── quarantine/
│   ├── harness/
│   └── runtime/
└── collector/
```

All roots and files use private modes and reject symlink substitution. Gateway and exporter backups are observation backups; they are not substitutes for owner backups.

### 6.2 Gateway database

Minimum tables:

| Table | Purpose |
| --- | --- |
| `schema_info` | gateway schema and instance identity |
| `schema_migrations` | migration receipts |
| `producer_instances` | allowlisted producer and last heartbeat |
| `events` | exact canonical envelope and common indexed source columns |
| `source_streams` | last contiguous sequence, highest seen sequence, completeness state |
| `relations` | indexed typed links from event to native entities |
| `ingest_receipts` | accepted, duplicate, rejected, and corruption batch outcomes |
| `quarantine` | malformed, unsupported, privacy-rejected, or corrupt bytes |
| `mapping_versions` | accepted envelope and producer mapping identities |

`events` retains the canonical JSON bytes and digest. Common source fields are duplicated only as checked indexes over those bytes. `relations` is a checked projection of envelope relations, not another fact source.

### 6.3 Exporter sidecar database

Minimum tables:

| Table | Purpose |
| --- | --- |
| `exporter_identity` | exporter instance, owner store identity, mapping version |
| `stream_checkpoints` | last acknowledged sequence and event identity per source stream |
| `batch_receipts` | source range, gateway receipt, retry count, elapsed time |
| `mapping_quarantine` | source record and mapping error without cursor advancement |
| `runtime_job_heads` | Runtime Job discovery and last observed event head |

The exporter refuses to reuse a checkpoint against a different owner store identity or lower mapping version without an explicit reset/migration receipt.

## 7. Exporter execution model

Every exporter follows the same state machine:

```text
open owner store read-only
→ identify owner instance and source head
→ load observation-owned checkpoint
→ read a bounded committed batch
→ map through a versioned allowlist
→ send exact batch
→ receive committed gateway acknowledgement
→ atomically advance sidecar checkpoint
→ emit exporter receipt and lag status
```

Crash behavior:

| Failure point | Recovery |
| --- | --- |
| before gateway request | reread and resend source batch |
| during request / response unknown | resend identical request and batch |
| after gateway commit before sidecar checkpoint | gateway returns exact duplicates; then checkpoint advances |
| mapping failure | quarantine source record; do not advance stream |
| owner database unavailable | report lag; never substitute cached state as current owner truth |
| gateway unavailable | retain checkpoint; retry with bounded backoff |

### 7.1 Host exporter

Host already has a global append-only Journal sequence. The exporter reads event rows in sequence order and maps only committed event metadata, referenced CAS object identities, Task/Attempt IDs, external request/binding IDs, verification IDs, and TaskOutcome references.

It does not decode Harness internal objects retained in historical Host CAS. Legacy Host-backed Harness evidence remains a compatibility source, not a new Harness observation producer.

### 7.2 Harness exporter

Harness exports independent `run_events` after P0 cutover. It maps Run, Provider Call, Tool Step, Snapshot, Trace, recovery, stop, receipt, and CompletionProposal identities. Provider/model usage measurements may be inline metadata; prompts and outputs remain private owner references.

The exporter can be tested against temporary independent Harness stores before production cutover, but production enablement requires the no-dual-write receipt.

### 7.3 Runtime exporter

Runtime has per-Job append-only event sequences rather than one global sequence. The exporter therefore:

1. scans read-only Job heads as `(job_id, max(event_sequence))`;
2. compares them with `runtime_job_heads` in the sidecar;
3. reads only Jobs whose native head exceeds the acknowledged sidecar head;
4. emits one source stream per Job;
5. keeps terminal Jobs eligible for later administrative repair or reconciliation events;
6. enriches Job events with immutable Execution Plan, Attempt, Artifact, terminal-evidence, Workspace, request, and foreign-reference links where available.

P1 does not synthesize a false global Runtime order and does not turn mutable Workspace snapshots into authoritative lifecycle events. A future Runtime-global sequence is admitted only if measured full-head scanning becomes materially expensive.

## 8. Work packages and gates

## P1.0 — preflight and P0 closeout alignment

Repositories: Computing, Harness, Host.

Deliverables:

- update machine plan from `not_started` to `closeout_pending` for P0 and `execution_designed_waiting_for_p0_closeout` for P1;
- retain the completed request-only Harness recovery acceptance as a prerequisite receipt;
- complete Harness batch-admission performance work and scale receipt;
- produce production state-root, backup/restore, cutover, and no-dual-write receipts;
- freeze exact source revisions used by the first exporter fixtures.

Gate:

- P1 contract/gateway work may proceed;
- no production exporter service may be enabled until all P0 closeout receipts pass.

Rollback:

- P1 remains fixture-only and no owner schema is changed.

## P1.1 — contract and deterministic fixture corpus

Repository: Computing experiment.

Deliverables:

- Python dataclasses and strict decoder for envelope, relation, privacy, source, batch, acknowledgement, and receipt;
- canonical JSON and digest implementation;
- JSON Schemas generated or checked from the same contract;
- frozen Host, Harness, and Runtime native fixture records;
- versioned mapping manifests declaring accepted native kinds and emitted attributes/relations;
- contract documentation and compatibility policy.

Tests:

- canonical order and digest stability;
- unknown fields rejected where strictness is required;
- same native identity maps to the same `eventId`;
- same ID / different bytes classified as corruption;
- relation and privacy vocabularies are closed;
- no raw prompt, model output, Tool payload, stdout/stderr, credential, or private reasoning fixture is admitted.

Gate:

- one synthetic three-owner trajectory can be represented without querying owner databases.

Rollback:

- delete the experiment package; no producer or production state changed.

## P1.2 — local gateway and query core

Repository: Computing experiment.

Deliverables:

- SQLite schema, migrations, private modes, symlink rejection, Doctor, backup/verify/restore;
- one-writer ingest service over a Unix domain socket;
- atomic single-stream batch ingest;
- duplicate, corruption, gap, mapping-version, and privacy handling;
- CLI commands:

```text
ordivon-observe init
ordivon-observe serve
ordivon-observe status
ordivon-observe producers
ordivon-observe lag
ordivon-observe event EVENT_ID
ordivon-observe entity KIND ID
ordivon-observe trajectory --task|--harness-run|--runtime-job ID
ordivon-observe failures
ordivon-observe doctor [--history]
ordivon-observe backup / verify-backup / restore
ordivon-observe export --format jsonl
```

Tests:

- commit-before-ack response loss;
- exact duplicate batch replay;
- batch atomicity;
- sequence gap refusal;
- same ID / different bytes quarantine;
- gateway restart and database reopen;
- backup verification and independent restore;
- bounded connected-trajectory query over cyclic relations;
- one synthetic million-event query benchmark.

Gate:

- gateway passes all tests with synthetic producers and no owner imports.

Rollback:

- stop service and remove only the observation state root after an explicit export/backup decision.

## P1.3 — Harness exporter

Repository: Harness.

Deliverables:

- read-only independent Harness event reader with global sequence batches;
- `harness-observation-mapping.v1`;
- observation-owned checkpoint and receipt store;
- run-once and bounded-follow CLI modes;
- lag, mapping failure, owner identity mismatch, and gateway-unavailable diagnostics;
- temporary-store and restored-store acceptance.

Tests:

- source database schema and event bytes unchanged by export;
- Run creation through terminal completion exports a contiguous stream;
- pause/resume and recovery preserve native sequence and relations;
- Provider and Tool content defaults to digest/reference;
- gateway-down backlog catches up exactly once by catalog identity;
- crash after gateway commit before checkpoint produces duplicates, not new catalog events.

Gate:

- standalone Harness Run is queryable with no Host identity;
- exporter is production-disabled until P0 cutover receipt exists.

Rollback:

- disable exporter and retain owner state untouched; sidecar state may be removed after receipt export.

## P1.4 — Host exporter

Repository: Host.

Deliverables:

- read-only Host Journal event reader with global sequence batches;
- `host-observation-mapping.v1`;
- mappings for Task, Attempt, Context reference, Effect/Dispatch, external executor request/binding/observation, Verification, CompletionDecision, and TaskOutcome;
- sidecar checkpoint, receipt, and lag handling;
- legacy Harness objects excluded from native Harness semantics.

Tests:

- Host source database remains byte/schema compatible;
- fake external executor trajectory exports without importing Ordivon Harness types;
- external CompletionProposal remains distinct from accepted TaskOutcome;
- stale revision, rejected verification, and UNKNOWN states remain visible;
- exact replay and response loss do not create duplicate catalog events.

Gate:

- Host + fake external Harness Task/Attempt/foreign Run trajectory is queryable and does not imply completion from executor status.

Rollback:

- disable exporter; Host Task correctness and recovery remain unchanged.

## P1.5 — Runtime exporter

Repository: Runtime.

Deliverables:

- read-only Registry exporter binary or subcommand;
- `runtime-observation-mapping.v1`;
- per-Job stream discovery and sidecar head tracking;
- mappings for Job events, Attempt identity, Execution Plan, Artifact references, terminal evidence, cancellation, reconciliation, orphan/lost/repair outcomes, request identity, and foreign references;
- no Host or Harness semantic status in Runtime mapping.

Tests:

- source Registry unchanged by export;
- multiple Jobs advance independently;
- a later repair event on a terminal Job is discovered and exported;
- exporter restart from sidecar checkpoint emits no missing native event;
- duplicate dispatch and reconciliation events remain mechanically distinguishable;
- Runtime success cannot emit `task_completed` or `harness_completed`.

Gate:

- one Runtime Job is queryable by Job, Attempt, Workspace, Artifact, `clientRequestId`, and foreign reference.

Rollback:

- disable exporter binary/service; Runtime service and Registry remain untouched.

## P1.6 — cross-owner correlation and privacy acceptance

Repositories: Computing plus three producer fixtures.

Deliverables:

- relation mappings for the deterministic path:

```text
Host Task
→ Task Attempt
→ external executor request
→ Harness Run Contract / Run
→ Provider Call / Tool Step
→ Runtime request / Job / Attempt / Artifact
→ Harness CompletionProposal
→ Host Verification / CompletionDecision / TaskOutcome
```

- trajectory query that returns owner-grouped events, relation edges, missing-link findings, completeness per stream, and evidence references;
- generic namespaced relation targets for externally owned Campaign, Configuration, Trial, and Grader Result identities;
- synthetic repeated-Trial grouping containing one valid positive, one valid negative, one invalid, and one incomplete trajectory while P1 reports only evidence completeness;
- privacy policy receipt for each mapping version;
- deterministic fake-provider cross-owner fixture;
- real bounded local composition smoke after P0 production cutover.

Tests:

- process exit success without Host verification is not an accepted outcome;
- asynchronous response-loss recovery uses native links and optional span links, never a false parent;
- missing Harness, Host, or Runtime events produce an explicit incomplete trajectory;
- P1 does not convert complete evidence into Trial validity or improvement;
- repeated Trial identities group correctly without pooling materially different Configuration Cells;
- secret-like keys and forbidden content are rejected before gateway acceptance;
- owner references remain sufficient to retrieve evidence through owner tools without copying it into the gateway.

P1 Core gate:

- the complete deterministic three-owner trajectory is queryable after service restarts;
- one Observation Selection Manifest remains digest-stable after Gateway rebuild from intact owner stores;
- gateway outage during 10,000 committed source events recovers with zero missing native sequence;
- owner operations never wait for gateway acknowledgement;
- P1 Core reliability, privacy, and performance receipts pass.

## P1.7 — Track R projection and formal Trial handoff

Repository: Computing.

Deliverables:

- query adapter that selects one complete trajectory by native owner references;
- immutable `ObservationSelectionManifest` containing query identity, selected event IDs and canonical digests, source-stream heads, mapping versions, completeness claims, and selection digest;
- Trial projection containing System Manifest, Configuration Cell, owner refs, Observation Selection reference, observation contract version, producer mapping versions, completeness statement, and privacy statement;
- explicit candidate extraction; no automatic Dataset admission;
- update `HHR-R3-001` runner assumptions so Harness evidence is not read from Host CAS;
- deterministic R3 smoke using the automatic observation path.

Tests:

- deleting the observation database does not delete or reinterpret owner evidence;
- rebuilding observation from intact owners reproduces the same native event identities and relation graph; ingest timestamps and receipts may differ;
- the same frozen Observation Selection produces the same selection digest after rebuild;
- an incomplete stream cannot be promoted as a complete Trial;
- a complete stream is not automatically a valid Trial;
- a Runtime terminal success cannot bypass Host/domain grading;
- Trial projection contains no copied private payload bytes.

Gate:

- formal repeated Trials become unblocked for the first deterministic and Native DeepSeek campaigns.

## P1.8 — OpenTelemetry interoperability

Repository: Computing experiment.

This work may begin after the envelope is frozen, but it is not a P1 Core prerequisite.

Deliverables:

- envelope-to-span/log/metric mapper with pinned mapping identity;
- span links for asynchronous, recovered, and joined work;
- loopback OTLP Collector configuration with memory limit, batching, health check, and file-backed retry queue;
- external OTel trace intake mapped as bounded external observations without inventing Harness Run semantics;
- local-only default and privacy filtering before any external exporter.

Tests:

- disabling Collector does not affect gateway or owner correctness;
- Collector queue survives restart;
- restricted content is not exported;
- native IDs and event digests remain present as OTel attributes/links;
- OTel mapping changes cannot rewrite canonical observation events.

P1 Interop gate:

- one complete native trajectory has a consistent derived OTel trace without using OTel as completeness or recovery proof.

## P1.9 — scale, operations, and disposition

Repositories: Computing and owning repositories for exact exporter receipts.

Hard acceptance gates:

- 10,000 owner events committed while gateway is unavailable, then zero missing source sequence after recovery;
- exporter crash after gateway commit and before checkpoint produces one catalog event per native event;
- 100 metadata events/second for ten minutes without owner-path blocking or sequence loss;
- gateway acknowledgement P95 below two seconds, with a diagnostic target below 250 ms for local batches;
- common indexed entity/trajectory queries over one million metadata events complete within five seconds on the recorded machine;
- exporter lag, checkpoint, source head, disk use, WAL growth, CPU, and memory are queryable;
- backup/restore and rebuild-from-owner proofs pass;
- source databases are unchanged by observation enablement except for ordinary owner work.

Closeout disposition:

- retain prototype in Computing;
- narrow or delete it if query value does not justify cost;
- extract `ordivon-observation` only after recurring production and Track R consumers prove an independent release and operations lifecycle.

## 9. Dependency DAG and repository order

```text
P0 recovery/performance/deployment closeout ───────────────┐
                                                           ├─ enable production exporters
P1.1 contract ─→ P1.2 gateway ─→ P1.3 Harness exporter ───┤
                              ├→ P1.4 Host exporter ──────┤─→ P1.6 correlation/privacy
                              └→ P1.5 Runtime exporter ───┘          │
                                                                     ├→ P1.7 Track R / R3 unblock
                                                                     └→ P1.8 OTel interoperability
                                                                            │
                                                                            └→ P1.9 closeout
```

Recommended commit batches:

1. **Computing C1** — contract, schemas, fixtures, canonicalization tests;
2. **Computing C2** — gateway SQLite core, CLI, Doctor, backup/restore, synthetic reliability tests;
3. **Harness H1** — read-only exporter and sidecar checkpoint, disabled-by-default service packaging;
4. **Host O1** — read-only exporter and mapping;
5. **Runtime R1** — per-Job stream exporter and mapping;
6. **Computing C3** — cross-owner relation vocabulary, trajectory query, privacy and outage acceptance;
7. **Computing C4** — Track R adapter and deterministic formal smoke;
8. **Computing C5** — OTel mapper and Collector acceptance;
9. **Cross-project closeout** — exact revision manifest and all receipts.

Each repository commits independently. A cross-project manifest records tested revisions; no repository waits for an uncommitted sibling checkout as a runtime dependency.

## 10. Required closeout evidence

```text
p0-closeout-prerequisite.json
observation-contract-v1.json
observation-gateway-schema-v1.json
gateway-doctor-and-backup-receipt.json
host-exporter-receipt.json
harness-exporter-receipt.json
runtime-exporter-receipt.json
owner-read-only-proof.json
ten-thousand-event-outage-recovery.json
cross-owner-trajectory.json
privacy-acceptance.json
million-event-query-benchmark.json
track-r-projection.json
observation-selection-manifest-fixture.json
otel-interop-receipt.json          # P1 Interop, not P1 Core
p1-closeout.json
```

Every receipt binds source revision, mapping version, envelope version, gateway schema version, source instance identity, test configuration, timestamps, asserted checks, and integrity digest.

## 11. Stop and rollback conditions

Stop P1 Core and redesign if any of these occurs:

- an exporter requires a write, migration, trigger, or lock in an owner database;
- intact owner history cannot rebuild the same native event catalog;
- gateway availability becomes necessary for owner progress or recovery;
- one source event can be silently skipped to advance a checkpoint;
- Runtime requires a fabricated global order for correctness;
- cross-owner correlation requires copying owner databases or content payloads;
- the envelope grows into a universal Task, workflow, model, or domain schema;
- privacy can only be enforced by storing then redacting forbidden content;
- Track R cannot distinguish complete, incomplete, invalid, and non-admitted trajectories;
- operational cost materially exceeds the value of automatic evidence at current scale.

Rollback is deletion-safe by construction:

1. stop exporter services;
2. stop gateway and Collector;
3. export or retain observation receipts according to operator policy;
4. remove observation-owned state only;
5. continue operating Host, Harness, and Runtime from their owner-native stores.

## 12. Immediate Ready Frontier

M1 is implemented and tested:

- reduced Envelope, relation vocabulary, privacy classes, and native stream rules;
- canonicalization, strict decoding, native event identity, Batch and Acknowledgement contracts;
- in-process SQLite Gateway with atomic ingest, exact replay, corruption/gap/mapping/privacy quarantine, private modes, reopen and full-history Doctor;
- generated/frozen JSON Schemas;
- deterministic metadata-only Host/Harness/Runtime fixture with 13 Events, three complete streams, and catalog digest `sha256:c71a5af70734d6a1f41167141affc9f6482194895cb3ab843bd6d5c6bd093f15`.

The shared exporter contract is frozen at Computing `ad1d0240966441e783c1ce9ef0f79f710580ba70`. It provides an installable wheel, exact owner/exporter revision binding, dynamic export receipt time, and digest-CAS multi-stream checkpoints. Host and Harness use global Journal streams; Runtime uses one stream per Job and no fabricated global order.

The immediate frontier is now:

1. add bounded run-once Harness, Host, and Runtime exporters with observation-owned sidecars and read-only owner access;
3. reconstruct one real deterministic cross-owner trajectory and freeze an `ObservationSelectionManifest`;
4. hand that selection to the R3 deterministic smoke before authorizing daemon, follow-service, OTel, Collector, backup operations, or million-event hardening.

Production hardening requires measured recurring use by R3, TCG, or operations.
