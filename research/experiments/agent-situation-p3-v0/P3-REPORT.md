# P3 Agent Situation / Embodiment Surface — closeout

## Starting pressure

P0-P2 made Harness capabilities discoverable/composable, allowed exact cross-Run procedural capital, and moved mechanical Tool dataflow below repeated model turns. A remaining operational gap appeared above any single owner: a fresh Agent still had to reconstruct **where it is, which owner facts are current, what is actually admitted now, what occurred, and where UNKNOWN/recovery belongs** across Host, Harness, Runtime and World.

P3 asked whether this justified one global Agent state/registry or only a thinner read-only composition of existing owner truth.

Baseline revisions:

| owner | revision |
| --- | --- |
| Computing | `1ff3d8be4be464919a7ba33b9280799d1aaa35dc` |
| Host | `507589eb1ae602f788913c7a8fdfd7bad355fe6c` |
| Harness | `6639cf575eb006e8be2864037d9427b9913dd8a3` |
| Runtime | `761bfe8dd7ca7c5e3e514891657c986eecb204e5` |
| World | `da4eb2cafc7c33d0905140bceb7e7ceaef7330da` |

## P3-0 reality audit

The owners already have strong local projections:

- **Host** — Task/Goal/revision/frontier semantic continuity, handoff, verification/outcome; WorkingCheckpoint Runtime facts are explicitly navigation hints, not physical truth.
- **Harness** — Run/turn/WorkingSet/Provider/Tool/Snapshot continuity and exact request-bound action authority; workbench leaves process/external liveness unclaimed.
- **Runtime** — live Workspace source state, Job/Attempt identity, execution target/profile/provider, physical result/Artifact/recovery state; `semanticCompletionEvaluated=false` is explicit.
- **World** — provider/trajectory identity, admission/occurrence evidence, owner reconciliation hints and availability evidence; inspector grants no authority and claims no external currentness.

The common problem is therefore **distributed truth, repeated consumption joins**, not missing ownership.

## W5-B2 embodiment falsifier

World W5-B2 had already necessity-tested a research-only six-coordinate bounded occurrence proof:

```text
subjectRef / ownerId / bodyRef / scopeDigest / admissionDigest / occurrenceDigest
```

P3 supplies the previously missing third materially different consumer, but it **falsifies direct promotion**. A Host continuity Task can exist without a canonical global Agent `subjectRef`; a Runtime Workspace/Job is an execution locus rather than a domain Body; and continuation/recovery/current action admission are not represented by a bounded occurrence tuple.

What survives from W5-B2 is the deeper law: owner-qualified scope/admission/occurrence proof roles are useful and owner-native semantics must remain opaque.

## Observation Plane boundary

Computing already owns the earned minimum `ordivon-observation-core`: immutable owner metadata events, checkpointed export bundles, rebuildable Gateway and Selection manifests. It reconstructs historical cross-owner trajectories but deliberately does not infer Trial validity.

P3 therefore refuses to turn Observation into a currentness service. Historical relation closure cannot establish current Workspace existence, target availability, World reachability/presence or exact turn authority. Current facts still require current owner reads.

## P3-1 baselines

Three materially different current/replayed cases were frozen.

### A — stale continuity locus

The P3 Host checkpoint was current at Task revision 2 but its Runtime navigation hint named `harness-post-p2-retrospective-20260814`. A real Runtime `workspace.get` proved the workspace was already closed (`WORKSPACE_NOT_FOUND`, `retryClass=never`). The semantic Task remained valid while the physical locus did not.

### B — occurrence versus semantic completion and World UNKNOWN

Runtime Job `job-019ffe53-a9d0-7c11-8a91-5216ac546aed` physically succeeded and mechanically converged, but retained `semanticCompletionEvaluated=false`; the Host Task remained `ready`. Separately, the current World inspector contract represents unknown/pending provider outcome as an outstanding commitment with `nextOwnerOperation=reconcile-original-request-without-redispatch`, `actionAuthority=not-granted-by-inspection`, and `externalCurrentness=not-claimed`.

### C — installed versus admitted capability

Current Harness projects `compose_tool_program` as `stage=installed`, `visibility=advanced-opt-in`, with authority only from exact current `AgentTurnRequest.tools`. A current Runtime Workspace does not supply the missing Run/turn admission.

## P3-2 experiment

An experiment-local owner-qualified facet compiler was tested first. It uses explicit roles for continuity, locus, action/admission, occurrence, recovery and completion; currentness and authority remain proof metadata on each facet rather than separate objects. It performs only equality joins on explicit identities and fixed proof-boundary checks. It never queries an owner, chooses a locus, probes liveness, executes a recovery hint or validates domain completion.

The experiment passed seven focused falsifiers, including stale-locus, exact admission, physical-vs-semantic completion, UNKNOWN owner routing, order determinism and the W5-B2 shape rejection.

### Ablation

Across the three workloads:

| metric | baseline | treatment |
| --- | ---: | ---: |
| required owner reads | 8 | 8 |
| manual cross-owner joins | 10 | 0 |
| explicit unsafe implication opportunities | 10 | 0 |

The owner-read count intentionally does **not** improve. Currentness is owner truth; reducing reads by caching or centralizing them would weaken the model. The improvement is mechanical interpretation: repeated joins become deterministic while unresolved facts remain explicit.

## P3-3 promotion pressure

The treatment requires only dataclasses plus Observation Core canonical validation/digest helpers. Static audit proves it imports no Host/Harness/Runtime/World package, opens no DB/file/network process, probes no liveness, dispatches/reconciles nothing, and is absent from the stable package-root facade.

The retained implementation is therefore one advanced module:

```text
ordivon_observation_core.situation
```

It adds `SituationAnchor`, `SituationRelation`, `SituationFacet`, `SituationProjection`, and `compile_situation()`.

Observation Core full tests with the new module: **25/25 passed** before repository-wide acceptance.

## Acceptance and repository-gate boundary

P3-local and shared-package acceptance passed:

- experiment falsifiers before contraction: **7/7**;
- final `ordivon-observation-core` suite: **25/25**;
- static dependency/authority boundary audit: passed with zero Host/Harness/Runtime/World imports, owner calls, liveness probes or package-root exports;
- isolated `ordivon-observation-core 0.1.0` wheel: `situation.py` packaged, direct advanced import works, package-root Situation names remain absent;
- isolated `ordivon-protocol` Python 3.12 schema/protocol suite: **11/11**;
- Computing compile/Ruff/content-cli/RSI-lab/content strict/Vale/markdownlint/spelling/offline-link/foundational-doc/world-model/experiment-contract/computer-responsibility checks passed;
- research portfolio/view, project-family map, protocol release and protocol candidate checks passed;
- evidence/conformance suite passed **61/62**; its only failure is the same repository-wide research-compression condition described below.

Primary evidence Jobs include Observation Core `job-019ffe5c-f882-7d30-86b7-639cea079472`, ablation `job-019ffe5b-8b4d-74d3-90fc-cb54b46e5da4`, isolated protocol/evidence `job-019ffe62-4423-7063-97a6-8d772d7f7d6a`, and isolated wheel `job-019ffe62-ceed-71e1-86b5-b5fe58d445fb`.

The complete Computing conformance command is **not green at this concurrent repository state**. A clean baseline workspace reproduced a pre-P3 historical-research-compression failure. P3 contracted the already-closed ACS0–ACS9 executable apparatus and proved those five removed scripts remain Git-recoverable. The remaining blocker is `research/experiments/pal-foundations-v0/*.py`: PAL Foundations explicitly states it remains open after Wave 3, and Runtime currently has a separate `pal-foundations-wave4-research-20260814` workspace. P3 therefore does not delete that active apparatus or rewrite another research line's portfolio/status merely to make its own gate green. The current blocker is a cross-workstream policy/currentness conflict, not a P3 code regression.

## Retain / shrink / delete

### Retain

- owner-qualified Situation facets;
- caller-selected anchor instead of a global Agent identity authority;
- explicit currentness and authority status as proof metadata, never inferred from age/configuration;
- exact locus-hint versus owner-locus observation comparison;
- installed action versus exact admission distinction;
- physical occurrence versus semantic completion distinction;
- owner-routed recovery hint projection without execution authority;
- deterministic digest/order-independent read-only projection;
- existing Observation Core as the shared home for the pure metadata compiler.

### Shrink

- Situation is an **advanced direct module**, not package-root public facade;
- P3 adds no owner-specific mapper/API because existing public owner projections already carry the needed truth;
- historical Observation remains optional evidence, not required current Situation state;
- no automatic replacement-locus selection is attempted.

### Delete / reject

- global Agent database/registry;
- universal Agent identity owner;
- global Presence/reachability table;
- single authority object spanning Host/Harness/Runtime/World;
- direct promotion of W5-B2 six-coordinate occurrence proof into a Situation schema;
- `observedAt` age heuristics as currentness truth;
- Situation daemon/service;
- new standalone `ordivon-situation` repository/package;
- restoration of Host Observation exporter solely for P3;
- new Situation MCP tools on every owner;
- any inference that physical success, installed capability, historical occurrence or recovery hint equals semantic authority.

## Result

P3 changes the embodiment model from **“one Agent should have one global state”** to:

```text
owner-native current truth
        ↓ explicit owner reads
owner-qualified Situation facets
        ↓ deterministic composition
one Agent consumption view
```

The key law is:

> **Unified consumption does not require unified state, currentness, or authority.**

Operational embodiment is therefore a relation among continuity, locus, current action admission, occurrence evidence and owner-routed recovery—not a permanent global Presence record.
