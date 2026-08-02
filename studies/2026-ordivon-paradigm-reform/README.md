# Ordivon Paradigm Reform Audit

Date: `2026-08-02`

This study applies the scarcity-and-operability lens and Core A11/A15 to the complete current Ordivon portfolio. It audits not only product code and declared architecture, but also the tests, receipts, schemas, evidence bundles, generated mirrors, audits, release rituals, and CI gates that previous source reviews usually treated as unquestioned evidence of maturity.

The main conclusion is:

> Ordivon's largest current structural problem is not ordinary implementation bloat. It is a verification and representation overhang: multiple layers describe, prove, mirror, and re-prove the system faster than they improve the real capability, product experience, research judgment, or recovery path that the system exists to serve.

This does not mean verification is generally wasteful. Runtime's identity, at-most-once dispatch, evidence, cancellation, and recovery checks are the product. Host's revision fencing and durable Task reconstruction protect real continuity. Game's deterministic World transitions and replay protect an actual game invariant. The failure appears when a check, receipt, abstraction, or historical experiment remains active after its protected failure, consumer, or decision value disappears.

The machine-readable one-time inventory is in [`evidence/source-audit-20260802.json`](evidence/source-audit-20260802.json). It is evidence for this review, not a new schema, registry, generator, or default gate.

## 1. Audit baseline

Every repository was read at its current `origin/main`, not at the potentially stale long-lived local checkout.

| Repository | Revision |
|---|---|
| `ordivon-computing` | `37760a58d482c61748ed90ea5f46546cfd2e2344` |
| `ordivon-game` | `21271056174ed451db6fb3e9578eab218c4bd1f0` |
| `ordivon-harness` | `f72fef829aa09ec9b02fba0b344408a7d5f4647f` |
| `ordivon-host` | `2b17b0683128f995831fef54544f87d0166bab2d` |
| `ordivon-runtime` | `2a5036183a67288523a408460759eebb646a63b3` |
| `ordivon-security` | `36ce116c8de9df492946a04b710b6fe71aef901a` |
| `ordivon-web` | `11a546f2948dbdc39dae1dff670249b7f23ea10f` |
| `ordivon-world` | `5e20e1ce44da418c159fa92e0655f6234db71e32` |

The active uncommitted Game product-loop workspace was also inspected because it represents current work beyond `origin/main` and shows where real product pressure is already correcting the architecture.

## 2. Why prior source audits did not expose this

The earlier audits were not useless. They found real correctness, ownership, concurrency, recovery, and over-generalization failures. The blind spot was methodological.

### 2.1 Declaration-conformance bias

The audits primarily asked:

```text
Does the implementation match the declared boundary?
Does the test prove the declared invariant?
Does the document accurately describe the code?
```

They did not ask with equal force:

```text
Should this declared boundary exist?
Is this invariant still worth protecting?
Does this test duplicate another test?
Is the document itself a copied truth surface?
Would deleting this validation reduce no real capability?
```

A system can be internally consistent and still be unnecessary.

### 2.2 Evidence-density bias

Receipts, immutable manifests, schemas, test matrices, replay bundles, coverage reports, and source audits were treated as positive evidence. Their existence made a subsystem look mature.

But under A11 they are durable constraints. They consume:

- implementation time;
- CI time;
- review attention;
- repository navigation bandwidth;
- model Context;
- migration and compatibility effort;
- confidence that may be misplaced when many local checks are green.

Their burden of proof is not lower than ordinary production code. In many cases it is higher because they shape every later change.

### 2.3 Repository-local optimization

Each audit asked whether one repository had a coherent boundary. It rarely priced the same semantic fact across repositories.

Examples include:

- Harness continuity objects in Harness, Host CAS, Host extension events, and Computer protocol;
- architecture state in product README files, Computer registries, research maps, Web content models, and curated Web system views;
- Game outcomes in World state, Host records, replay evidence graphs, evaluation reports, milestone receipts, release manifests, and Security matrices.

Each copy can be locally defensible while the whole system becomes expensive and contradictory.

### 2.4 No counterfactual deletion run

Previous audits usually added missing adversarial tests. They did not run the symmetric experiment:

```text
remove one check, document, receipt, state object, or compatibility layer
→ rerun real workloads
→ identify which failure becomes possible
→ restore only the narrowest mechanism that prevents it
```

Without deletion experiments, verification naturally accumulates.

### 2.5 Historical evidence remained in the active path

The repositories correctly preserved negative results, but often preserved their machinery too:

- World proved that no independent World layer was required, then continued running completed W1/WXP experiments in default CI;
- Security marked Campaign v0 as frozen historical substrate, but continued shipping and testing it in the active repository;
- Game retained every milestone receipt and evaluation track while moving to the next product milestone;
- Computer retained closed experiments and their conformance surfaces in the same active repository that owns current research and protocol work.

Git already preserves history. Active CI is not required to prove that history existed.

### 2.6 Stale audit baselines

Several long-lived local checkouts were behind `origin/main`: Game by 32 commits, Web by 16, Security by 6, and other repositories by one. An audit can be source-level yet still examine the wrong source state.

The reform process must bind every cross-repository conclusion to exact current revisions or explicitly label it historical.

### 2.7 Audit output became architecture

Each review tended to create:

- another report;
- another receipt;
- another evidence snapshot;
- another schema or generated summary;
- another CI check to prevent the report from drifting.

The audit mechanism therefore rewarded itself. A successful audit often increased the permanent surface it should have been judging.

## 3. A11 interpretation after this audit

A validation mechanism is a durable constraint when it repeatedly blocks, delays, duplicates, or structures future work.

This includes:

- tests and coverage thresholds;
- CI and release gates;
- approval and review requirements;
- receipts and evidence bundles;
- schemas and protocol profiles;
- generated mirrors committed beside their sources;
- audit and closeout documents required to remain synchronized;
- historical experiment reproduction in the default path;
- compatibility layers without current consumers.

Every such mechanism should answer:

```text
Which exact unrecoverable or repeatedly expensive failure does it prevent?
Who currently consumes the property it proves?
Why is a narrower owner-local check insufficient?
Which other check already proves part or all of the same property?
How often must it run?
What latency, maintenance, Context, and control cost does it impose?
When will it be deleted, archived, made advisory, or moved out of the default path?
```

A check that cannot answer these questions is not automatically harmless because it is deterministic or fast.

## 4. Portfolio-level diagnosis

The current portfolio has four different verification classes. They should not share one default treatment.

### 4.1 Irreducible boundary verification — retain

These checks protect a responsibility that remains owned by the component:

- Runtime operation identity, at-most-once dispatch, cancellation, reconciliation, and evidence;
- Host Task revision fencing, event/CAS reconstruction, uncertain Effect handling, and terminal admission;
- Game deterministic World transition and minimal save/replay correctness;
- provider-native idempotency, Receipt lookup, and Artifact verification;
- Security experiment separation between actor observation and hidden World truth.

These checks may be intensive because their failure invalidates the component's primary purpose.

### 4.2 Product regression verification — narrow

These checks protect a visible behavior but should run at the cheapest sufficient level:

- one Game first-playable browser path;
- one Web build and route/accessibility smoke;
- one Harness real Task outcome comparison;
- one Host recovery trajectory for each genuinely different Effect class.

They should not automatically expand into complete internal-model coverage.

### 4.3 Research evidence — preserve, remove from default CI

A closed experiment needs immutable source, result, and enough instructions to reproduce it. It does not need to run on every unrelated change.

Examples:

- World W1, WXP-1, and WXP-2;
- Security Round 1 and R-A matrices;
- Game M2–M5 evaluations;
- Harness H3/H4/H5 provider-replacement evidence;
- Computer closed semantic-core and external-contract experiments.

These belong to explicit reproduction commands, periodic research review, or path-scoped checks.

### 4.4 Governance mirrors and ritual verification — delete or localize

These mechanisms repeat state without owning it:

- generated portfolio views that become a second project-management system;
- manually curated public architecture graphs that copy repository state;
- committed generated metadata that is regenerated during every build;
- universal release or conformance profiles for one consumer;
- receipts whose only consumer is the next audit report;
- default CI jobs that validate completed historical dispositions.

## 5. Responsibility and bottleneck map

The reform should optimize each project against its actual scarce output.

| Project | Stable responsibility | Current scarce output | Verification that directly serves it |
|---|---|---|---|
| Computer | preserve derivation, questions, evidence, stable principles, and only proven cross-project contracts | judgment, synthesis, deletion, and correct project pressure | source integrity and checks only at promoted shared boundaries |
| Harness | turn replaceable model cognition and Tools into useful bounded work | task success, adaptation, context quality, stopping, and provider replacement | a small set of end-to-end Tasks and explicit wait/recovery cases |
| Host | preserve durable Task meaning, commitment, uncertainty, and admission across replacement | simple reliable continuity without becoming a workflow platform | revision, CAS, event, Effect, reconciliation, and terminal-admission invariants |
| Runtime | execute committed local Effects with observable recovery | trustworthy physical execution at low friction | operation identity, dispatch, evidence, cancellation, reconciliation, recovery |
| World | supply and study owner-native external capabilities and observations | useful external capability, not another authority | provider/module-local contracts and named failure experiments |
| Security | study adaptive opposition and contested evaluation | stronger adversaries, strategic behavior, transfer, and evaluator integrity | experiment validity, hidden-state separation, exact Trial identity, scorer integrity |
| Game | create a game people want to play and Agents can inhabit | player comprehension, tension, surprise, attachment, replay value | deterministic World correctness plus one real product loop |
| Web | make Ordivon understandable and worth reading | editorial clarity, trust, navigation, and public expression | one build, link/content validation, accessibility and route smoke |

The present portfolio often verifies a less scarce stage because that stage is easier to formalize.

## 6. Repository findings

## 6.1 Ordivon Computing — research, governance, and protocol are over-coupled

### Evidence

- 457 tracked files;
- 25,070 lines of documents;
- 114 validation-named files;
- `research/map.yaml` is 642 lines;
- `research/portfolio.json` is 165 lines;
- only two questions are active;
- the `ordivon_protocol.harness` module is 583 lines and has one implementation consumer;
- at revision `37760a5`, package metadata is `0.5.0` while conformance and immutable release metadata remain `0.3.0`.

The strongest failure is not merely version drift. On the exact same revision:

```text
check_protocol_release.py       → success for released 0.3.0
check_foundational_docs.py      → success
ordivon_conformance.py gate     → failure: protocol package version differs
```

The local checks are individually correct about their small questions, but together they do not describe one coherent usable state.

### Formalism failure

Computer currently combines:

- research archive;
- active portfolio management;
- project registry;
- graph map;
- protocol implementation;
- release manifests;
- cross-repository conformance;
- immutable system snapshots;
- historical experiments;
- Core and Knowledge.

This makes the repository appear authoritative over the whole system even when product repositories own current truth.

The Harness continuity protocol is a direct A11/A13 violation candidate: a large one-consumer model was promoted into the shared protocol before a second materially different consumer existed.

### Disposition

Retain:

- Core;
- reusable Knowledge;
- source-grounded Studies;
- concise active questions;
- only contracts already consumed across genuinely different boundaries.

Localize or delete:

- Harness-specific continuity objects back into Harness until a second consumer exists;
- stale or closed experiments from default gates;
- copied mutable project status;
- graph and portfolio fields that do not change an actual decision;
- protocol release machinery for unreleased single-consumer changes.

Computer should become more epistemically authoritative and less operationally central.

## 6.2 Ordivon Game — the validation system grew faster than the game

### Evidence

- 17,638 lines of product code;
- 10,144 lines of tests;
- 10,095 lines of documents;
- 49 validation-named files;
- global coverage thresholds of 95% lines, 90% branches, and 95% functions;
- every push runs coverage, browser E2E, receipt generation, general measurement, replay measurement, and release-input generation;
- milestone receipts and evaluation records exist from M0 through M5;
- the alpha release uploads, downloads, and fully reverifies its own bytes.

The current product-loop workspace is changing shell, fronts, interventions, mission pacing, and first-playable measurements. That is evidence that the real bottleneck is now player experience, not lack of another replay or release proof.

### Formalism failure

The Game repository became several products at once:

- deterministic game engine;
- embedded Agent Host experiment;
- replay/evidence graph system;
- diagnosis system;
- deployment comparison system;
- control-boundary evaluation suite;
- release reproducibility system;
- playable interface.

Each component is defensible in isolation. Together they consume more attention than the player-facing loop.

Global coverage thresholds encourage tests for internal branches regardless of product consequence. Milestone receipts duplicate Git history, tests, evaluation JSON, and release artifacts. Self-download and full re-verification is disproportionate for a solo alpha with no demonstrated distribution threat.

### Disposition

Retain:

- deterministic World kernel;
- domain invariants;
- save/load and minimum replay needed for the product;
- Mission Control product API;
- model/provider adapter boundary;
- one first-playable E2E path.

Freeze or move out of the active product path:

- historical M0–M5 receipts;
- control-boundary research matrices;
- generalized evidence graph and diagnosis machinery not used by the player;
- release-input and measurement jobs on ordinary pushes;
- global coverage thresholds.

Game should be judged first by whether people can understand, enjoy, replay, and improve their decisions.

## 6.3 Ordivon Harness — durable cognition was decomposed beyond current evidence

### Evidence

- 13,631 lines of product code;
- 7,118 lines of tests;
- 6,596 lines of scripts and workflow operations;
- one P0/P1 test file is 1,400 lines;
- the durable path contains Task Contract, Attempt Descriptor, Assignment, Tool Grant, Run Contract, Tool Step Intent, Dispatch Fence, Receipt, Snapshot, state delta, Recovery, Completion Proposal, Completion Verification, and Completion Decision;
- shared Harness protocol types have one implementation consumer.

### Formalism failure

The system has separated many identities before demonstrating that each independently changes recovery or task performance.

Host already owns durable Task, revision, Journal, CAS, and commitment state. Runtime already owns Job, Attempt, physical cancellation, and evidence. Harness still introduces a second dense layer of Attempts, Assignments, Run snapshots, Tool-step receipts, and completion objects.

Some distinctions are real:

- Provider Session versus durable Run;
- pending Tool operation versus completed Observation;
- input wait versus dispatch wait;
- requested model versus effective model;
- cancellation request versus proven cancellation.

But the current implementation represents these distinctions through more durable object types than the tested workloads have proven necessary.

Dedicated live-provider receipt checkers from H3/H4/H5 also remain as permanent package surfaces after their architectural question was answered.

### Disposition

Retain:

- the Agent loop;
- provider-faithful adapters;
- Context/input compiler;
- Tool bridge;
- bounded budgets and stopping;
- explicit input and physical-dispatch wait states;
- enough public Run state to resume those boundaries;
- independent completion verification where the Host cannot infer completion safely.

Localize and reduce:

- Harness protocol objects into Harness;
- the durable state model to the minimum fields needed by actual resume and reconciliation;
- historical provider receipt checkers to archived reproduction scripts;
- tests to named invariant families rather than complete object-shape coverage.

The next Harness benchmark should compare useful task outcome, recovery, Context cost, and stopping quality—not object count or semantic completeness.

## 6.4 Ordivon Host — the thin kernel is sound, but its public semantic surface is not thin

### Evidence

The prior A-series source audit already found:

- a 645-line generic `EffectLifecycleHost` without two real consumers;
- unconsumed durable states and fields;
- duplicated workload lifecycle mechanics;
- public claims not backed by production use.

Current Host adds a generic `HostExtensionPort`. Its only external consumer is Harness. The port infers retained CAS references partly through payload field names ending in `ObjectDigest` or `ObjectDigests`.

Host and Harness separately define `HistoryValidation` and `OperatorHandoffCapsule`.

### Formalism failure

The Host kernel solves a real responsibility, but the surrounding package exports many workload, cognition, proposal, decision, execution, handoff, recovery, and compatibility concepts as if they were equally stable.

The extension port is useful as an extraction seam, but its generic payload naming convention is a weak implicit protocol. A one-consumer boundary should remain narrow and explicit rather than advertise a general extension platform.

### Disposition

Retain:

- Task identity and projection;
- Journal and CAS;
- revision/state/frontier fencing;
- Host kernel;
- Effect commitment and uncertain reconciliation;
- minimal Runtime client boundary;
- terminal Task outcome admission.

Delete, narrow, or move out of the public stable surface:

- dead states and fields identified by the prior audit;
- generic Effect lifecycle until real consumers replace specialized paths;
- inferred extension object retention by field naming;
- duplicated handoff/history models;
- workload-specific engines exported from the package root.

Host should be a small continuity kernel with explicit extension adapters, not a semantic catalog of every Agent concept.

## 6.5 Ordivon Runtime — verification is mostly intrinsic rather than ceremonial

Runtime is the strongest current alignment with A11.

Its validation protects the exact thing the component sells:

- stable operation identity;
- at-most-once physical dispatch;
- source-state commitment;
- process-tree ownership;
- evidence retention;
- cancellation;
- uncertainty;
- reconciliation;
- recovery.

Its document-to-code and test-to-code ratios are materially lower than Game, Harness, or Computer. CodeQL and release acceptance are manual rather than repeated on every ordinary change.

### Remaining pressure

Runtime still has many operational scripts, compatibility documents, and acceptance paths. They should be pruned based on actual invocation and consumer use, but no broad reduction is justified merely from counts.

### Disposition

Retain the kernel. Apply only narrow A11 cleanup:

- remove scripts with no real operator invocation;
- path-scope Python versus Rust checks where useful;
- keep release acceptance manual or release-triggered;
- delete compatibility only after current Host/Harness consumers move.

Runtime should not be simplified by weakening the physical commitment boundary.

## 6.6 Ordivon World — two negative architecture results did not close the active machinery

### Evidence

W1 concluded that direct Host/provider integration was correct and simpler than a World correlation layer.

WCP-0 through WXP-2 then concluded:

```text
retain provider and observation adapters
localize callback and Artifact facets
admit no World service, database, Workflow engine, callback journal,
Artifact transfer service, universal schema, broker, or router
```

Despite this, default CI still:

- validates repository layout and W1 evidence;
- regenerates and checks a capability portfolio;
- regenerates and checks a WCP closeout;
- reruns W1;
- reruns WXP-1 and WXP-2;
- runs the complete Cloudflare provider suite;
- runs the complete network-observation Rust suite.

The repository couples two capabilities with independent owners, dependencies, toolchains, release paths, and failure modes:

- Cloudflare provider operations;
- network observation and private tooling.

### Formalism failure

World has become a semantic shell around capabilities that the experiments explicitly kept owner-local.

The historical experiments are valuable evidence, but their default CI presence makes every provider or observation change re-prove a closed architectural decision.

The generated capability portfolio is read-only and carefully non-authoritative, but that raises the A11 question: if it changes no dispatch, recovery, release, or consumer decision, why is synchronization mandatory?

### Disposition

Immediately:

- remove W1/WXP reproduction from default every-push CI;
- run historical experiments manually or only when their own files change;
- path-scope Cloudflare and network-observation checks;
- stop treating generated closeout and capability views as merge gates.

Temporarily retain the repository as a carrier while evaluating whether provider and observation release cadence actually justify a split. Do not create another semantic World layer or rename solely for conceptual cleanliness.

## 6.7 Ordivon Security — the new experiment layer is valuable; the old Campaign substrate should leave the active path

Security has materially improved since the earlier local checkout. It now contains real dynamic-opponent, model-backed, and CAGE-based experiments. The separation among Actor observation, hidden World truth, exact Trial identity, and independent Scorer is a genuine research requirement.

Its own A11 audit nevertheless states that Campaign Manifest/ledger/coordinator v0 is approximately 4.6k active contract lines with historical reproduction as its only current consumer and a disposition of `frozen/archive`.

Default CI still runs the entire deterministic Round 1 acceptance on every push and pull request. `CHARTER.md` also still names retired Link and Edge ownership while `README.md` correctly names World.

### Formalism failure

The repository contains two generations:

- frozen infrastructure-composition contracts;
- current adversarial experiment and evaluation code.

Keeping both active confuses what Security is for and makes historical reproducibility look like present capability.

The 1,450-line full report and large evidence files are acceptable as closed research records. They should not cause the complete experiment family to run on unrelated changes.

### Disposition

Retain:

- current experiment interfaces;
- Actor/World/Scorer separation;
- hidden evaluation records;
- exact Trial identity;
- strategic outcome dimensions;
- current adversarial evaluation work.

Archive or delete from the active package after a final consumer search:

- Campaign v0 manifest/ledger/coordinator/live-composition substrate;
- compatibility import paths that exist only for historical reports;
- default CI execution of closed Round 1 families.

Fix stale project ownership text immediately; it is copied state, not historical evidence.

## 6.8 Ordivon Web — the publication layer is recreating a small CMS and architecture registry

### Evidence

- 4,394 lines of code;
- 4,987 lines of documents;
- 1,393 committed generated metadata lines;
- `pnpm check` runs content synchronization, publication validation, typecheck, lint, build, budget reporting, and Playwright;
- content is regenerated in `typecheck` and again in `build`, after already being checked;
- pull-request checks and main-branch deployment both install Chromium and run the full check;
- curated system views manually encode project roles and dependencies owned elsewhere.

### Formalism failure

The public site needs editorial metadata, but it does not need both source frontmatter and committed generated TypeScript as active truth.

The Web repository is also becoming a public architecture database. That creates immediate drift: World may be shown as an external-effect authority even after World itself rejects such authority; project status changes require manual edits in several places.

Editorial policy documents can improve writing, but audience taxonomies, claim policies, article-type systems, audits, generated manifests, and architecture graphs together exceed the needs of the current publication volume.

### Disposition

Retain:

- authored MDX and its frontmatter;
- a small publication schema;
- routes and article rendering;
- one build;
- one accessibility/route smoke;
- deployment recovery.

Delete or simplify:

- committed generated metadata when it can be generated during build;
- repeated content generation within one check;
- duplicate full checks in PR and deploy workflows;
- curated architecture facts that cannot be generated or linked directly from authoritative sources;
- editorial documents that do not change an actual published article decision.

Web should project Ordivon, not become another owner of Ordivon state.

## 7. Cross-repository reform decisions

### 7.1 Stop promoting single-consumer semantics

No object belongs in `ordivon-protocol` merely because it is durable and carefully validated.

A shared protocol object requires at least one of:

- two materially different consumers;
- a cross-language boundary;
- independent release or transport compatibility;
- a failure that cannot be solved through a consumer-local type and adapter.

Harness continuity objects currently fail this test and should return to Harness.

### 7.2 Closed research does not run by default

A completed experiment should retain:

- exact source revision;
- inputs;
- result;
- a reproduction command;
- limitations and disposition.

It should not automatically remain in every push pipeline. Default CI protects current production and active research boundaries, not the entire historical epistemic record.

### 7.3 One owner, many projections

Project state, architecture, and research position should have one owner. Other surfaces should link, derive, or state a date-bound interpretation.

Manual copies must not be described as current truth.

### 7.4 Coverage is diagnostic, not governance

Coverage can reveal unexecuted code. It does not prove product value, architectural necessity, semantic correctness, or adequate adversarial testing.

Global thresholds should be replaced by targeted invariant and trajectory tests where the cost of an uncovered branch is known.

### 7.5 Audit output has a deletion condition

Every future audit should state at creation time:

- whether it is a temporary work product, historical record, Knowledge candidate, or Core candidate;
- which earlier document it supersedes;
- which active mechanism it deletes or narrows;
- when its own active references can be removed.

An audit that only adds another layer is incomplete.

## 8. Final assessment

The current Ordivon direction remains coherent. The problem is not that thin core, high potential, low governance, high recoverability, graph-shaped work, or evidence-based research were wrong.

The problem is that Ordivon applied those principles asymmetrically:

```text
product abstractions were challenged
verification abstractions were trusted

runtime authority was localized
research and publication authority was copied

new semantic layers required evidence
new tests, receipts, and audits did not

negative results changed prose
but did not always delete active machinery
```

The reform therefore does not require inventing a new architecture. It requires enforcing the architecture's own deepest principles against the structures that were previously exempt.

The execution sequence is defined in [`REFORM.md`](REFORM.md).
