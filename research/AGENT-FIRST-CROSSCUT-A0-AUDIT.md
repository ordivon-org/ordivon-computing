# Agent-first Cross-cutting Infrastructure A0 Audit

Status: A0 first closeout accepted; later promotion remains evidence-gated.

Baseline revisions inspected:

| Owner | Revision |
| --- | --- |
| Computing | `c239dff62f9f15baa4ee2056d2db9d7d1b3f12d6` |
| Host | `a76a620160b28d870670696e04c39e539296fe00` |
| Harness | `593a389d1b035ee46b91b374bf76f40ed2c697ef` |
| Runtime | `a455fd01ce0dea25684956e5e5da899d41832a1b` |
| Security | `3c605f2e341cf684ec499d5ea605cd7af40c4558` |
| Finance | `3387161260bbadc2418ed2861307319cf63334f4` |

This audit applies the Agent-first infrastructure-promotion rule to three cross-cutting candidates:

```text
A0-O  Observation Plane
A0-M  System / Environment identity
A0-U  Usage / Cost accounting
```

The audit asks whether each candidate is inherited infrastructure, an owner-local Agent-facing projection, or a genuinely shared Ordivon semantic responsibility. It does not assume a new service, database, daemon, or repository.

## Executive decision

| Candidate | Evidence today | A0 decision | Repository decision |
| --- | --- | --- | --- |
| Observation Plane | B3/B4 plus A0 O1 now reconstruct complete Host/Harness/Runtime trajectories from owner-native read-only exports; O1 passed against a >20k-Job live Runtime Registry | **Shared semantic responsibility earned; retain the minimum core** | **No extraction.** Keep shared contract/query implementation in Computing and exporters beside owners |
| System / Environment identity | Evaluation and Security expose materially different environment identity needs; M1 composed both without copying domain payloads, but the Security side is still a contract-shaped fixture | **Shared problem earned; shared contract still not earned** | **No extraction.** Retain the bounded composition experiment until a second real owner record passes |
| Usage / Cost accounting | U1 found and repaired Harness token normalization, then projected six terminal Run aggregates into Observation on a fresh O1 trajectory | **No new usage authority. Keep owner-native facts and bounded read-only measurements** | **No repository, service, or metrics database** |

The target composition is therefore:

```text
owner-native authority
        │
        ├── immutable configuration/environment references
        ├── owner-native usage/evidence
        │
        ▼
read-only Observation projection
        │
        ├── cross-owner trajectory
        ├── normalized measurements
        └── exact configuration identity refs
        │
        ▼
Evaluation / diagnosis / comparison / Agent inspection
```

Observation remains a rebuildable query copy. Configuration manifests remain immutable references. Usage remains owner-native fact plus non-authoritative normalization. None becomes product authority.

# A0-O — Observation Plane

## What exists

The current implementation has crossed the threshold from a logging convenience into a reusable responsibility.

- Host, Harness, and Runtime retain independent authoritative histories.
- Each owner has a run-once, read-only exporter with its own mapping version.
- Export checkpoints and outboxes live outside owner state roots.
- A durable export bundle is written before a checkpoint advances.
- The Gateway ingests at least once and deduplicates by stable owner-native identity.
- Payload bytes remain owner-native by default; observations carry metadata, digests, privacy class, and references.
- B3 selected twelve events from three source streams and reconstructed one Host → Harness → Runtime trajectory without inferring Trial validity.
- B4 froze an Observation Selection Manifest as part of a valid formal deterministic Trial.
- A0 O1 then ran a fresh current Host → independent Harness → real Runtime workload, selected 25 events from all three owners, retained no payload bytes, and kept Trial validity inference false.
- O1 used one exact Runtime Job while the long-lived Registry contained 20,399 Jobs, proving the same reconstruction path still works against accumulated production history.

This satisfies the core extraction-pressure test: deleting the shared observation contract would recreate cross-owner manual evidence joining for materially different owners and would break the current formal evaluation path.

## Why it still does not deserve a repository

The shared responsibility is the contract and reconstruction semantics, not an independently operated product.

There is currently no evidence for:

- an independently deployed observation service;
- a separate release cadence;
- multi-node throughput pressure;
- a public observation API with independent consumers;
- production correctness depending synchronously on the Gateway;
- a need for Kafka, ClickHouse, a tracing SaaS, or another permanent data platform.

Current default:

```text
Computing owns contract + reference Gateway + selection semantics
Owners own read-only mappings/exporters
Agent invokes export/query when useful
Owner state remains sufficient when observation is absent
```

A daemon is not admitted. If continuous telemetry becomes useful, OpenTelemetry Collector remains the inherited operational-telemetry baseline rather than an Ordivon reimplementation.

## A0-O dogfood findings and remaining gaps

O1 converted two paper risks into concrete engineering decisions.

1. The Observation README was stale after B3/B4 and was corrected; mutable status belongs in current evidence rather than copied old prose.
2. Runtime export was blocked by global Registry size: the old exporter rejected any Registry with more Jobs than `job_limit`, even for one known Job. Runtime now supports exact `job_ids`; the old whole-Registry bound remains the default when no explicit scope is supplied.
3. The final O1 run proved exact export with one selected Job while the live Registry contained 20,399 Jobs. This is an owner-local mechanical fix, not a reason to build an Observation service.
4. Harness now emits measurements only on the terminal `IndependentHarnessRunReceipt` Observation. Host and Runtime remain measurement-empty until their own real queries justify fields.
5. The Gateway still stores canonical envelopes without a dedicated measurement index. O1 did not need one, so none is admitted.
6. Runtime Artifact traversal remains owner-native; attaching later Artifact lists to historical Runtime events would mutate historical meaning.
7. Production Observation authority remains false. Owner recovery and correctness do not depend on export or Gateway availability.

## A0-O disposition

O1 is accepted. The current minimum is sufficient for fresh Agent dogfood without a daemon:

```text
owner truth → run-once read-only export → in-process Gateway → Selection/query
```

The next Observation change must come from another observed workload. Continuous collection should first inherit OpenTelemetry/Collector mechanisms if needed; an independent `ordivon-observation` repository is reconsidered only after independent deployment/versioning or materially different consumers make colocation more expensive.

# A0-M — System / Environment identity

## The actual responsibility

The shared problem is not “describe the whole computer.” It is narrower:

> Bind the material configuration facts required to decide whether two trajectories are the same configuration, comparable configurations, or incomparable environments.

This responsibility already appears in two materially different domains.

### Evaluation

`ordivon.evaluation-system-manifest` binds:

- source/System Snapshot;
- Provider, model, and Adapter identity;
- prompt, Context, Tool catalog, Tool grant, budget, and environment digests;
- evaluation schemas, Suite, grader set, and failure taxonomy;
- unavailable fields, limitations, privacy, and integrity.

Harness already accepts a generic immutable `systemManifestRef` in `HarnessRunContract`, so Harness does not require Evaluation to own the manifest schema.

### Security

Security independently defines `EnvironmentIdentity` with:

- environment identity;
- provider and provider revision;
- image digest;
- configuration digest;
- Guardian policy digest;
- Observation plan digest.

This is not an Evaluation System Manifest copy. It proves that exact environment identity is a real cross-domain need.

## Why the current Evaluation manifest cannot become the global contract

It hard-requires `evaluationContract`, including Task/Trial/Result/Failure schemas, Suite, grader set, and failure taxonomy. Those are Evaluation facts, not properties of every Agent run.

A0 also found a concrete admission inconsistency in frozen B4 evidence. The B4 System Manifest stores its grader path as an absolute `/root/projects/...` path, while the canonical System Manifest validator requires normalized relative paths. Direct validation returns:

```text
ValueError: evaluationContract.graderSet.path must be normalized and relative
```

B5 fixed this pattern and its retained System Manifest passes the canonical validator. The historical B4 evidence is not rewritten; its integrity remains historical evidence for the exact generator that produced it. The B4 generator is corrected so a future rerun uses a relative logical path and validates the manifest before returning it.

A second weakness is that Evaluation currently retains an `environment` digest without a standalone owner-neutral environment record. The digest is useful for equality but insufficient for an Agent that later needs to explain which environment dimensions differed.

## A0-M decision

Do not promote the Evaluation schema. A bounded **configuration-identity v0** experiment now exists inside Computing.

Its common layer should be composition, not a universal machine ontology. A candidate minimum is:

```text
manifest identity
captured time
material bindings grouped by role
  implementation
  execution environment
  cognition/provider
  authority/policy
  inputs/data
  verifier/domain, when present
unknown or unavailable material fields
privacy declaration
integrity
```

Each binding should be an immutable reference with identity, kind, and digest. Owner-specific payloads remain in Runtime, Harness, Security, Finance, Game, or another domain. Paths and host-local locators are never canonical identity.

M1 consumed a retained B5 Evaluation System Manifest and a metadata-only Security-shaped `EnvironmentIdentity`. It preserved the Security record as one opaque owner binding and marked Evaluation's environment `digest_only`; therefore it can say two configurations differ without pretending to explain an unavailable environment payload. The experiment is accepted as composition evidence, not as a shared schema release.

A shared configuration contract remains deferred until at least one real non-Evaluation owner record—preferably a Security KVM evaluation or another materially different domain—passes the same composition without domain leakage.

## A0-M falsifier

Do not create a shared contract if a B5 Harness Trial and a Security KVM Evaluation cannot both be expressed without either:

- copying domain-specific state into the common manifest;
- weakening their existing exact identity checks; or
- creating generic fields with no comparison or recovery consequence.

If that happens, retain only separate owner manifests plus opaque digest references.

# A0-U — Usage / Cost accounting

## Current ownership is already mostly correct

### Harness owns Agent Run usage

Current `AgentLoopResult.usage` already retains useful Run-local facts such as:

- model calls and Tool calls;
- observation bytes;
- total tokens and token limit;
- Provider attempts and replayed Provider results;
- model retries and Tool corrections;
- no-progress and observation-only turns;
- wall time and deadline overrun;
- requested/effective model identities;
- Provider-native usage records.

### Runtime owns physical execution measurements

Runtime already derives:

- Job/Attempt duration;
- admission → dispatch latency;
- dispatch → Runner-bound latency;
- Runner-bound → terminal latency;
- cancellation → terminal latency;
- reconciliation → convergence latency;
- Artifact counts and bytes;
- output retention/drop facts;
- physical budget commitments for memory, PIDs, and CPU quota.

Runtime intentionally does not claim semantic task quality. It also currently enforces cgroup resource ceilings without persisting a complete actual CPU-time/peak-memory/IO accounting stream.

### Domains own domain metrics

Security retains domain `rawMetrics` and separate operational evidence. Finance owns financial carrying costs and domain accounting. Those values must not be flattened into infrastructure usage merely because both happen to be numeric.

### Evaluation currently hand-assembles comparison metrics

B5 builds one `metrics` object from Harness usage, selected Runtime Job identities, trace analysis, wall time, and fixed human-intervention assumptions. A real B5 diagnostic recorded, for example, model calls, Tool calls, Runtime Jobs, observation bytes, cached/input/output/total tokens, invalid Tool calls, and wall time while leaving monetary cost explicitly unavailable.

That proves the useful metric set exists. It also proves the missing layer is **projection and provenance**, not collection.

## A0-U decision

Do not create `UsageRecord` as another writable authority and do not add a metrics database.

Use the already-existing `ObservationEnvelope.measurements` field as the normalization boundary:

```text
owner-native event / receipt
        ↓
owner-local read-only mapping
        ↓
Observation measurement { value, unit }
        + source identity
        + relations
        + payload/reference provenance
        ↓
query / Evaluation freeze / optional OTel export
```

The first mapping profile should cover only values with demonstrated cross-run comparison value:

| Measurement family | Native owner | Rule |
| --- | --- | --- |
| model/Provider call counts | Harness | project from retained Run/Provider evidence |
| Tool calls, correction counts | Harness | project from Run evidence |
| input/output/cached/reasoning/total tokens | Harness/Provider | preserve Provider semantics and expose unavailable values as absent, never fabricated |
| observation bytes | Harness | project exact retained count |
| Run wall time | Harness | retain as Run-local duration |
| Runtime Job count | derived selection | count exact linked Jobs, not guessed shell commands |
| Runtime physical latency and Artifact bytes | Runtime | project existing inspection/event facts |
| human intervention | Host/domain/human surface | only an owner that observed the intervention may emit it |
| monetary cost | Provider/billing/pricing projection | emit only with an explicit pricing/billing basis reference |
| domain score/cost | domain | keep namespaced/domain-owned; do not treat as infrastructure usage |

OpenTelemetry semantic conventions are useful export compatibility, especially for model/provider identity and GenAI token usage, but they are not Ordivon's durable authority. Their GenAI conventions are still evolving and have moved to a dedicated GenAI semantic-conventions repository. Ordivon should preserve owner-native facts and map outward rather than freezing a moving external vocabulary into recovery state.

### U1 live result

O1 exposed an owner-local accounting bug before measurement promotion: Harness retained Provider records using `inputTokens`/`outputTokens`, but `_usage_total_tokens()` did not recognize that naming pair, so the same Run reported aggregate `totalTokens=0`. Harness added the missing fallback and a hard-limit regression test; the repaired O1 Run reports `totalTokens=58`, exactly equal to the two scripted Provider calls.

Only after repairing the source did Harness project six terminal aggregates into `ObservationEnvelope.measurements`: model calls, Tool calls, observation bytes, total tokens, wall time, and Tool corrections. Per-call Provider usage remains owner-native and is absent from the retained Observation Bundle and O1 receipt. Monetary cost remains absent.

This is the desired A0 pattern: fix owner truth first, then project a small non-authoritative measurement view.

## What not to add yet

- no global cost service;
- no mandatory OpenTelemetry Collector;
- no Prometheus/ClickHouse deployment;
- no Runtime schema migration for CPU seconds or peak memory;
- no automatic USD estimate from a hard-coded model price;
- no unqualified aggregation across different System/Environment identities.

Actual cgroup CPU, memory, IO, and network consumption should be inherited from system/OpenTelemetry tooling if a real experiment proves those measurements change a decision.

# A0 combined acceptance target

The first useful cross-cutting Agent query is:

> Reconstruct this work from admitted Goal/Task through Agent Run, Tool/Runtime work, verification and outcome; identify the material configuration under which it ran; report the comparable resource/usage measurements and their evidence owners; preserve every unavailable or ambiguous field explicitly.

A0 does not require a single API that owns all of those facts. It requires that an Agent can compose them without manual archaeology or invented equivalence.

## A0 closeout and future gates

A0 O1/M1/U1 are closed for the first version. Their combined evidence is sufficient to answer the intended Agent query by composition: reconstruct one work trajectory, bind exact implementation/configuration references, surface comparable owned measurements, and preserve unknowns without inventing equivalence. No single authority owns the combined answer.

Retain now:

- Observation contract, owner-local read-only exporters, reference Gateway, and Selection semantics;
- exact Runtime Job export for bounded queries against a long-lived Registry;
- configuration-identity material bindings as a Computing experiment;
- terminal Harness measurement projection for already-owned Run aggregates.

Explicitly do not build now:

- an Observation repository/daemon;
- a universal System Manifest;
- a writable global UsageRecord or cost authority;
- a measurement index/database;
- hard-coded Provider price tables as evidence;
- Runtime CPU/peak-memory/IO accounting solely for completeness.

Reopen only through new evidence:

- **O2:** another materially different workload repeatedly pays manual export/query cost or needs continuous telemetry;
- **M2:** a real Security/Finance/Game/Studio owner manifest must compose without domain-field copying before a shared contract is considered;
- **U2:** another owner must need comparable measurements, or a decision must depend on physical CPU/memory/IO or monetary cost, before those fields/layers are added.

Repository extraction remains a later consequence of independent cadence/deployment/consumer pressure, never an A0 goal.

# Validation notes

The Observation Plane test set was run directly against the current Computing source with its implementation on `PYTHONPATH`: 59 tests passed; one schema test could not import because the system Python environment did not contain `jsonschema`. The failure was an execution-environment dependency, not an observed contract assertion failure. The schema contract remains covered by the repository's intended dependency environment.

The current B5 retained System Manifest passes the canonical System Manifest validator. The frozen B4 manifest fails only the normalized-relative-path admission rule described above; its historical bytes are intentionally left unchanged.
The final fresh O1 evidence is retained under `research/experiments/crosscut-a0-v0/evidence/o1-current-a0-o1-1786086849266-5a8cef08ce/`. It binds Computing `c772e93a9d102139842991c19922bed45e640211`, Host `a76a620160b28d870670696e04c39e539296fe00`, Harness `0d1e825e37b139d6b0b31a307fdc8bf904eeb722`, Runtime owner `a455fd01ce0dea25684956e5e5da899d41832a1b`, and Runtime exporter `4bc563e6da83af50679149002d31507cbd703305`. The retained Selection contains 25 events and all completeness claims pass while `trialValidityInferred=false`.

The final O1 Harness terminal measurements are six aggregate values; `ordivon.harness.total_tokens=58`. Cross-cutting retained evidence contains no Provider-call `providerUsage`, `inputTokens`, or `outputTokens` payload detail. The Runtime Workspace was closed and confirmed absent.
