# Ordivon Reform Sequence

> **Historical sequence:** this plan translated the audit into the P0/P1 reduction round. It is not the current roadmap; current status and implementation truth live in `research/portfolio.json` and the owning repositories.

This sequence converts the audit into deletion and localization. It deliberately avoids a new orchestration layer, global validation service, universal research-object schema, or mandatory governance ledger.

## 1. Decisions already earned

The source audit is sufficient to make the following architectural decisions without another exploratory round.

1. **Validation is subject to A11.** Tests, CI, receipts, evidence bundles, coverage thresholds, audits, generated mirrors, and release rituals are persistent constraints.
2. **Runtime remains the physical commitment kernel.** Its central verification is intrinsic to its product responsibility and is not a general formalism target.
3. **No independent World authority exists.** W1 and WCP-0 through WXP-2 both rejected it. World remains, at most, a temporary carrier and experiment boundary for owner-local adapters.
4. **Harness continuity semantics are not yet shared protocol.** They have one implementation consumer and return to Harness until another materially different consumer or transport boundary appears.
5. **Host remains a small continuity kernel.** Generic workload and extension semantics do not enter its stable public surface merely because Harness currently needs them.
6. **Game returns to product pressure.** Deterministic World integrity remains strict; generalized evaluation, evidence, and release machinery becomes secondary and mostly non-default.
7. **Security keeps the new adversarial experiment layer and retires the frozen Campaign substrate from active ownership.**
8. **Web is a projection and publication surface.** It does not own current architecture or repository state.
9. **Computer becomes less operationally central.** It preserves derivation and promotes only proven shared contracts.

## 2. P0 — stop formalism growth and restore coherent defaults

P0 is a coordinated reduction round. It changes default paths before deeper semantic redesign.

## P0-A — Core and audit method

### Change

Clarify A11 so that validation and audit machinery explicitly carry the same net-acceleration burden as ordinary abstractions.

### Required behavior

A future review must inspect:

- product code;
- test and CI code;
- generated artifacts;
- evidence and receipt machinery;
- compatibility and release paths;
- copied state and public projections.

### Non-goal

Do not add an A11 checker, constraint registry, or validation schema. Judgment and deletion remain the mechanism.

## P0-B — restore one coherent protocol state

The current Computer `origin/main` cannot pass its own conformance gate because package metadata is `0.5.0` while released and consumer conformance remains `0.3.0`.

The correct repair is not to promote every new Harness object into a `0.5.0` release merely to make the gate green.

### Coordinated migration

1. Move `HarnessToolStepIntent`, `HarnessToolStepReceipt`, `HarnessRunSnapshot`, `HarnessDispatchFence`, and related Harness-only enums into `ordivon-harness`.
2. Update Harness imports and tests to use the local module.
3. Remove the Harness-only module and exports from `ordivon-protocol`.
4. Remove Harness-only protocol tests from Computer.
5. Restore package metadata, release manifest, and conformance to one truthful version.
6. Keep shared canonical, Effect, Tool Contract, binding, and Host workload profiles only where current cross-boundary consumers remain.
7. Run one Computer protocol gate and one bounded consumer gate.

### Acceptance

- Computer's full conformance gate passes on the committed revision;
- Host and Harness install from exact commits;
- Harness durable recovery tests still pass;
- no second copy of the local Harness types remains in Computer;
- no release number is advanced without a release manifest and real consumer decision.

## P0-C — narrow the Host extension boundary

### Change

Keep a small extension append/storage port only if it reduces Harness use of Host internals.

Replace implicit object discovery through `*ObjectDigest` field naming with explicit referenced-object arguments or a Harness-local adapter.

### Acceptance

- Host does not parse Harness schemas;
- Harness can persist its objects without private Host access;
- the port does not advertise a plugin framework, scheduler, or generic extension ontology;
- one misspelled payload field cannot silently alter object retention;
- duplicated `HistoryValidation` and handoff models are reduced through composition or one generic base plus Harness projection.

## P0-D — reduce default CI to current responsibility

### Computer

Default documentation and study changes should run:

- basic syntax/JSON checks;
- relative-link checks where cheap;
- the specific generated view check only if that view remains.

Protocol gates should run only when protocol, release, conformance, or consumer-binding files change. Do not run full protocol and closed experiment conformance because prose changed.

### Game

Ordinary push/PR CI should protect:

- type correctness;
- deterministic World and persistence invariants;
- current Mission Control behavior;
- one first-playable browser trajectory.

Move to manual, release-triggered, nightly, or path-scoped execution:

- milestone receipt generation;
- general and replay measurements;
- release-input generation;
- control-boundary evaluation;
- self-download release re-verification.

Make coverage advisory or retain thresholds only for the small authoritative World reducer and storage boundary where an uncovered branch has a named failure.

### Harness

Default CI should protect:

- loop behavior;
- Provider adapter normalization;
- Tool dispatch/reconciliation;
- input wait and effect wait resume;
- cancellation truth;
- one complete repository-repair workload.

Historical H3/H4/H5 live receipt validators should be explicit reproduction scripts, not permanent package-quality indicators.

### Host

Default CI should protect the kernel and current real consumers. Experimental generic Effect lifecycle and dead state surfaces are deleted or placed under explicit experimental tests outside the stable public package.

### Runtime

Keep current Rust, script, and secret checks. Release acceptance remains manual/release-triggered. Remove only scripts with no observed operator or consumer use.

### World

Path-scope Cloudflare and network-observation jobs.

Move W1, WXP-1, WXP-2, capability-portfolio generation, and WCP closeout regeneration out of default every-push CI. They remain reproducible from their exact revisions.

### Security

Default CI should run small unit and current experiment-contract checks. Closed Round 1 families and frozen Campaign reproduction become path-scoped or manual.

### Web

One CI path should:

```text
read MDX/frontmatter
→ validate publication shape
→ typecheck/lint
→ build once
→ run one browser/accessibility smoke
```

Do not regenerate the same article metadata three times. The deploy workflow should reuse or repeat only the build required for trusted deployment, not the complete editorial audit unless the source changed after review.

## P0-E — archive or delete completed machinery

Git history and exact tagged revisions preserve closed work. The main branch should retain only what a current reader or reproducer needs.

### Computer

- remove completed experiments from default checks;
- compress old mutable portfolio machinery after active questions are reviewed;
- keep concise study conclusions rather than every generated control artifact in the active navigation path.

### Game

- retain one current release/evaluation summary;
- remove old milestone receipts from active documentation navigation;
- delete generalized replay/evidence modules not consumed by the player, current product API, or an active experiment;
- move Security-specific matrices to Security or freeze them at exact commits.

### Harness

- remove obsolete receipt checker scripts and duplicated evidence after one closeout summary points to immutable commits;
- keep only current provider adapters and active recovery fixtures.

### Host

- execute the prior audit's deletion decision for dead Task states, fields, and generic Effect lifecycle surfaces;
- reduce root exports to stable kernel and real extension boundaries.

### World

- retain the W1 and WCP result documents plus exact evidence;
- delete generated portfolio/closeout maintenance machinery if no current decision consumes it;
- do not rerun a negative architecture result indefinitely.

### Security

- search for external Campaign-v0 consumers;
- if none exist, remove Campaign Manifest, ledger, coordinator, process ports, and live composition from the active package;
- preserve the final revision and report as historical research;
- update all current ownership text from Link/Edge to World.

### Web

- stop committing generated article metadata when build-time generation is sufficient;
- delete stale curated system facts or replace them with dated interpretations and links;
- remove editorial policy documents that have not changed an actual article or publication decision.

## 3. P1 — simplify semantic ownership

P1 begins only after default verification cost is reduced.

## P1-A — minimal Harness durable state

Re-derive Harness continuity from actual recovery trajectories.

Candidate minimum:

```text
Task reference
Run identity
selected public Context/input digest
requested and effective model identity
cumulative budget
messages/observations needed for public resume
active external Tool operation reference, if any
pause reason
completion candidate and evidence reference
```

Every additional durable object must demonstrate an independent transition, consumer, or recovery decision.

Compare the reduced model against:

- input wait resume;
- response loss after Runtime dispatch;
- cancellation during Provider or Tool execution;
- Provider replacement;
- fresh-process completion.

The reduced model wins if it preserves outcomes with less durable state, fewer events, fewer schemas, and lower cognitive cost.

## P1-B — Host public-surface reduction

Classify every root-exported Host symbol as:

- stable kernel;
- current workload adapter;
- experimental;
- compatibility-only;
- delete.

Package-root exports retain only stable kernel and current extension seams. Workload engines can remain importable from explicit modules without being claimed as universal Host semantics.

## P1-C — Game product core

Use the current product-loop work as the main pressure.

Measure:

- time to first meaningful decision;
- number of interventions before the player understands the mission;
- whether failure can be explained in product language;
- whether a second run produces a deliberate strategy change;
- whether the Agent team creates surprise or attachment;
- whether replay is used by the player rather than only by tests.

Do not reopen generalized platform work until repeated play exposes a missing responsibility.

## P1-D — Security research core

After Campaign-v0 archival, Security should contain:

- experiments;
- actors and provider adapters;
- world adapters;
- scorer/evaluator logic;
- analysis;
- bounded evidence.

The next high-value work is held-out opponent and evaluator manipulation, not another control or evidence layer.

## P1-E — Web as generated projection only where generation is cheaper

The public site may derive article registries and route metadata during build. It should not attempt to synchronize live project maturity, architecture, and research status unless a reliable source can be consumed directly at acceptable cost.

When reliable generation is unavailable, prefer a dated editorial statement over a false current-state database.

## 4. P2 — reconsider repository boundaries only from operational evidence

Repository count is not itself a problem. A repository split or merge is justified when it reduces independent failure, release, dependency, authority, or recovery cost.

### World carrier decision

After CI is path-scoped, observe whether Cloudflare provider and network observation have:

- independent release cadence;
- independent consumers;
- conflicting dependency/toolchain needs;
- independent operational ownership;
- repeated cross-module change coupling.

Split only if those costs remain material. Do not create another generic `integrations` repository solely for naming cleanliness.

### Protocol location

Keep the shared protocol package in Computer while research-to-promotion iteration remains faster than independent release coordination. Extract it only when:

- release cadence is independent;
- multiple external consumers need package distribution;
- Computer research changes should not affect protocol delivery;
- extraction deletes more coordination than it creates.

### Computer portfolio

Replace the current portfolio/map machinery only if real work repeatedly loses active decisions. A single concise frontier document or GitHub Issues may be sufficient. Do not build a database or universal Research Object platform during this reform.

## 5. System-wide acceptance

The reform is complete when:

1. every repository's default CI protects its present responsibility rather than its complete history;
2. no current main revision has contradictory green subchecks and a red full state gate;
3. no single-consumer semantic model is labeled shared protocol;
4. World has no active shared-authority machinery after two negative architecture results;
5. frozen Security Campaign code is outside the active package or has a real current consumer;
6. Game's primary development metric is product experience, not coverage or receipt volume;
7. Web owns authored publication content but not copied live architecture truth;
8. Harness and Host preserve the tested recovery trajectories with fewer durable object types and public exports;
9. Runtime's physical commitment guarantees remain intact;
10. the reform deletes more active machinery than the audit added.

## 6. Explicit non-goals

This reform does not create:

- a central Ordivon daemon;
- a global validation service;
- a policy engine that decides which checks are allowed;
- a universal Research Object database;
- a mandatory graph store;
- a universal World schema;
- a new governance committee or approval path;
- an immediate monorepo;
- broad reduction of Runtime's execution guarantees;
- weaker evidence at real irreversible consequence boundaries.

The purpose is not to become less rigorous. It is to concentrate rigor where reality can still impose unrecoverable loss and remove rigor theater where recovery, local ownership, or direct evidence already solves the problem.
