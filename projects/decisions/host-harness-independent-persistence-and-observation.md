---
schema_version: 1
id: computing.projects.host-harness-observation
title: Independent Host and Harness Persistence with Automatic Observation
type: decision
profile: engineering
lifecycle: accepted
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-06
summary: Accepted boundary with independent Harness persistence implemented locally, production cutover still pending, and a reduced observation minimum core required before the first formal repeated Trials.
evidence_status: observed
readiness: not_applicable
applies_to:
  - ordivon-host
  - ordivon-harness
  - ordivon-runtime
  - ordivon-project-family
related:
  - computing.authority
  - computing.projects.decisions
  - computing.verify.agent-evaluation
---
# Independent Host and Harness Persistence with Automatic Observation

## Context

The current Host already owns an independent SQLite Journal, materialized Task projection, immutable CAS, recovery, backup, and Doctor surface. The current Harness repository owns Assignment, Run, Provider-call, Tool-step, Snapshot, Trace, recovery, and completion semantics, but its durable `HostHarnessRunStore` writes those objects into the Host CAS and advances them through Host extension events.

That arrangement proved one Host-backed native Agent path. It does not satisfy the required future composition:

```text
Host → Ordivon Harness
Host → Codex / Hermes / another Harness
Host → deterministic executor without a Harness

Game / Security / research runner → Ordivon Harness
Ordivon Harness → Runtime Tools
Ordivon Harness → domain-owned Tools without Runtime
```

The failure is not package location. It is durable dependency: a Harness Run cannot currently preserve its complete native continuity without a Host state root, while Host cannot observe all external Harnesses through one product-neutral binding.

A second pressure is automatic evidence collection. Runtime already retains large volumes of physical Job and Artifact evidence, and product repositories retain local receipts, but there is no reliable cross-project observation path. Formal Track R records are curated projections rather than automatic collection. Adding a collector before separating authority would copy the existing Host-bound Harness lifecycle into a global system and make later correction harder.

## Decision

Ordivon adopts two ordered phases.

### P0 — independent authority and composition

Host and Harness become independently durable products.

- Host retains Task, Task Attempt, commitment, verification, participant decision, and TaskOutcome authority in the Host Journal/CAS.
- Harness gains its own SQLite Journal/CAS and owns Run, Provider Call, Tool Step, Snapshot, Trace, stop, recovery, and completion-proposal history there.
- Runtime retains Workspace, Job, Attempt, physical Effect, process-tree, terminal-evidence, and Artifact authority.
- A caller-neutral Harness Run Contract replaces direct Host storage as the core Harness input.
- Host integrates Harnesses through a narrow external-executor adapter and stores only immutable foreign Run references, observations, proposals, and decisions required for Task continuity.
- Ordivon Harness provides an optional Host integration adapter but its core package and standalone Run path do not require `ordivon-host`.
- Existing Host-backed Harness history remains readable through a frozen compatibility reader. New Runs are never dual-written to both stores.

P0 adds no Collector, global observation database, dashboard, OTLP dependency, automatic Eval admission, or new repository.

### P1 — automatic observation without authority transfer

After P0, each authoritative component exposes its committed event stream for automatic export.

- Host and Harness use their existing ordered Journals as the durable outbox. Export cursors are derived consumer state; no duplicate observation event is written beside every authority event.
- Runtime exports from its Registry, Attempt bundles, terminal evidence, and trace stream through an owner-local adapter.
- Projects without an append-only event source use a transactional outbox in the same local transaction as their domain state change.
- A local observation gateway ingests at least once, deduplicates by stable event identity, preserves per-source order, stores a queryable non-authoritative copy, and emits OpenTelemetry-compatible traces, logs, and metrics.
- W3C Trace Context supplies cross-process correlation. Native Host, Harness, Runtime, and domain identities remain the only authority for recovery or adjudication.
- Large or sensitive payloads remain in owner-native CAS or Artifact stores. The observation copy records digests and references by default.
- Production observations may become candidate evaluation cases, but only versioned Task QA and explicit Dataset admission create formal Trials.

## Why Journal-as-Outbox is the default

Host and the planned Harness store are already event journals. Writing authority state and a second observation row would recreate the dual-write problem inside one process and increase storage without improving recoverability. An exporter can instead consume committed Journal sequence numbers and maintain an idempotent cursor.

For mutable domain stores without a durable event stream, the transactional outbox pattern remains necessary: domain state and the outbound event commit in one transaction, while a relay exports later. Consumers must tolerate duplicate delivery and preserve event order within an owner stream.

## Ownership matrix

| Fact | Authoritative owner | Observation-plane treatment |
| --- | --- | --- |
| Host Task, Attempt, commitment, verification, TaskOutcome | Host | immutable event reference and selected metadata |
| Harness Run, Provider Call, Tool Step, Snapshot, Trace, stop | Harness | immutable event reference, metrics, and Trace projection |
| Workspace, Job, Attempt, process tree, terminal evidence | Runtime | native reference and physical status projection |
| Game Session, Security Contest, Human Study, Studio Production | owning domain | domain result reference and bounded common metrics |
| trace, span, correlation, ingest status, query indexes | observation plane | derived copy only |
| evaluation Task, Trial, Result, Failure, Dataset admission | Track R or domain Eval owner | versioned research projection |

The observation database cannot complete a Task, resume a Run, reconcile a Job, authorize an Effect, determine a domain outcome, or repair an owner Journal.

## Core contracts

### Harness Run Contract

The core Harness accepts a caller-neutral immutable contract containing:

- Harness Run identity;
- caller identity and caller Run reference;
- objective and Context references;
- Provider/Adapter/model identity;
- Tool catalog and grant digests;
- complete budget;
- completion contract;
- System Manifest reference;
- correlation context;
- privacy policy.

Host Assignment is one adapter input, not the Harness persistence substrate. Domain projects may construct the same contract from their own durable Actor, Session, or Contest state.

### Host external-executor adapter

Host defines a structural adapter boundary:

```text
start(request) -> external run reference
observe(run reference) -> immutable observations
cancel(run reference) -> cancellation observation
recover(run reference) -> recovery observation
collect completion(run reference) -> completion proposal
```

The adapter may target Ordivon Harness, Codex, Hermes, another Agent framework, or a deterministic executor. It cannot commit Host Task state directly.

### Observation envelope

A versioned observation envelope carries:

- event, source stream, project, component, instance, and environment identity;
- source sequence and native event identity;
- trace/span context and links;
- caller, Task, Run, Workspace, Job, Provider Call, and Artifact references when present;
- source revision and System Manifest reference;
- bounded attributes, metrics, privacy class, payload reference, and digest.

The envelope does not define owner-native state machines.

## Migration rule

There is no production dual-write period.

1. Freeze and test the current Host-backed Harness reader.
2. Introduce the independent Harness store behind an internal Run-store protocol.
3. Refuse cutover while any legacy nonterminal Run requires Host-backed continuation.
4. Start every post-cutover Run in exactly one Harness store.
5. Host records the resulting foreign Run reference through idempotent correlation.
6. Preserve historical Host extension bytes and inspection tooling; do not bulk rewrite them into the new store merely to make the layout uniform.

A one-time migration may later import selected historical Runs into an archival Dataset, but imported bytes do not become current Harness recovery authority.

## Automatic collection guarantees

P1 provides:

- authority-first commit: product correctness never waits for the observation gateway;
- at-least-once export and idempotent ingest;
- stable event identity and ordered source sequence;
- explicit lag, failure, quarantine, and replay visibility;
- no secret collection and no raw private Chain-of-Thought requirement;
- metadata/digest collection by default, with bounded content capture only under an explicit policy;
- zero inference from process success to Task, Run, or domain success.

P1 does not promise globally exactly-once delivery. Exactly-once catalog rows are achieved by deduplication over at-least-once delivery.

## Implementation ownership

- `ordivon-host` implements its external-executor binding, independent state root, Journal exporter, and owner-native observation mapping.
- `ordivon-harness` implements `HarnessStore`, its state root, standalone Runner, Host adapter, Journal exporter, backup, Doctor, and compatibility reader.
- `ordivon-runtime` implements Registry/Attempt export and preserves existing physical authority.
- `ordivon-computing` owns the cross-project envelope, semantic conventions, prototype gateway, evaluation projection, and this decision during P0/P1.
- Domain repositories own domain events, privacy classification, result semantics, and eventual Eval adapters.

The prototype remains inside Computing until at least Host, Harness, and Runtime produce observations and at least operations and evaluation consume them. Only then may an `ordivon-observation` repository be admitted through a separate decision.

## Alternatives considered

### Keep Harness bytes in Host and add standalone trace export

Rejected. It would make exported traces independent while durable Run recovery remained Host-dependent. This solves browsing, not composition.

### Give Harness its own database but dual-write every Run to Host

Rejected. Cross-database atomicity is unavailable, disagreement would be inevitable, and both sides would appear authoritative for the same lifecycle.

### Move Assignment and Run authority into Host

Rejected. Host must support Harnesses with materially different internal lifecycles and must not become a universal Agent framework database.

### Store all Host and Harness state in the observation plane

Rejected. An observation backend may lag, sample, filter, restart, or change vendors. Recovery authority cannot depend on it.

### Use OpenTelemetry alone as the durable evidence contract

Rejected. OpenTelemetry supplies excellent trace, span, context, and export semantics, but it does not own Host Task transitions, Harness restart state, Runtime physical reconciliation, domain outcomes, Dataset admission, or immutable Artifact identity.

### Create Kafka, ClickHouse, or a cloud tracing platform immediately

Rejected for P1. A single-user local deployment first needs one collector, one SQLite ingest writer, owner-native storage, and measured volume. Larger infrastructure is admitted only after observed throughput or multi-node pressure.

## Consequences

Positive consequences:

- Host and Harness can evolve, deploy, recover, and back up independently;
- external Harness replacement no longer requires pretending every Harness has the Ordivon Run lifecycle;
- Ordivon Harness can serve Game, Security, and research paths without creating synthetic Host Tasks;
- automatic collection covers every supported composition rather than one Host-backed path;
- owner journals remain sufficient during collector failure;
- formal evaluation can reference full native histories instead of relying on one-off receipt curation.

Costs and risks:

- Harness must implement real storage, migrations, backup, Doctor, and operational hardening rather than delegating them to Host;
- cross-store workflows require idempotent correlation and reconciliation instead of one SQLite transaction;
- legacy Host-backed Runs require compatibility code until their retention horizon ends;
- observation mapping can drift from native schemas unless versioned and tested;
- local automatic collection will consume disk and requires explicit privacy and retention review.

## P0/P1 execution document

The executable design, table contracts, workstreams, gates, stop conditions, and repository sequence are in [`../../research/experiments/observation-plane-v0/P0-P1-DESIGN.md`](../../research/experiments/observation-plane-v0/P0-P1-DESIGN.md) and machine plan [`../../research/experiments/observation-plane-v0/plan-v1.json`](../../research/experiments/observation-plane-v0/plan-v1.json).

Formal Host–Harness–Runtime Trials remain designed but blocked until P0 and the Host/Harness/Runtime portion of P1 pass. This prevents collecting another curated local path that cannot represent the intended product composition.

## Status

Accepted as the cross-project design boundary. P0 independent Harness persistence, standalone execution, Host foreign-Run integration, response-loss recovery, and cutover control are implemented and locally tested; production state-root activation, exact release pins, scale acceptance, and final no-dual-write receipts remain open. P1 is split into a minimum experimental core and later production hardening. Only the minimum core blocks the first formal Trial. This decision does not register a new project or certify a production observation service.

## Reopen conditions

Reopen or supersede this decision if:

- a proven single durable owner can preserve independent Host and Harness replacement without lifecycle flattening;
- independent stores cause unrecoverable ambiguity that stable correlation and reconciliation cannot resolve;
- owner Journals cannot produce reliable observations without a second transactional write;
- OpenTelemetry or another standard acquires the exact authority and recovery semantics currently missing;
- automatic observation adds more permanent operational cost than the debugging, evaluation, and learning it enables.
