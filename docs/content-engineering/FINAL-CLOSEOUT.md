---
schema_version: 1
id: computing.content-engineering.closeout
title: Cross-Repository Documentation Governance Closeout
type: closeout
profile: research
lifecycle: accepted
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - editor
  - builder
  - agent
updated: 2026-08-04
summary: Final evidence and maintenance judgment for the nine-repository Ordivon documentation governance round.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.content-engineering
  - computing.content-engineering.baseline
  - computing.content-engineering.closeout-baseline
  - computing.authority
---
<!-- cspell:words Clippy -->
# Cross-Repository Documentation Governance Closeout

## Final judgment

The nine Ordivon repositories now form one navigable documentation system without becoming one shared truth store.

The governance round solved the highest-cost failures:

- every repository has a clear public entry and a route back to the complete project family;
- stable project roles are declared centrally while implementation, operations, research evidence, product registration, and public interpretation remain with their actual owners;
- Host, Harness, and Runtime no longer compete for the same durable facts;
- Game, Human, Security, World, and Web state current capability, experiment, candidate, or historical status without implying that every repository is a production layer;
- historical phase documents remain available as evidence but no longer define the default architecture;
- the public Web map and the repository authority model describe the same eight public projects plus the Web publication repository;
- a shared content contract, strict managed paths, and ordinary repository checks now catch new canonical drift before another concentrated rewrite is required.

This does not mean that every Markdown file is short, linked, metadata-managed, or current. It means that a reader and maintainer can determine which document owns a fact, where to begin, how to reach related projects, and when an older record is only historical evidence.

## Evidence

### Authority and boundary review

| Repository | Current owned role | Explicitly left elsewhere |
| --- | --- | --- |
| Computing | shared theory, research state, promoted contracts, project registry, conformance, and content-governance rules | product maturity, live operations, and domain truth |
| Host | durable Task continuity, Journal/CAS, commitments, verification records, participant decisions, and outcomes | Provider loops, Assignment/Run semantics, process truth, and domain truth |
| Harness | Assignment-scoped Agent Runs, Provider adapters, Tool steps, recovery, and completion proposals | generic Task persistence, Runtime supervision, and final domain authority |
| Runtime | Workspaces, Jobs, Runtime Attempts, process trees, Artifacts, cancellation, reconciliation, and physical recovery | Task meaning, Provider policy, and semantic completion |
| Game | Station Zero product registration, authoritative game World, rules, interventions, replay, and comparison | generic Host, Harness, and Runtime responsibilities |
| Human | admitted human questions, methods, practical paths, evidence limits, ethics, and privacy boundaries | cross-project contracts and individualized high-consequence advice |
| Security | bounded adversarial experiments, immutable traces, independent scoring, transfer, and evaluator-integrity research | production attack infrastructure, domain truth, and a general Campaign engine |
| World | retained Cloudflare adapter and private network operator tools | shared World service, database, router, workflow, or semantic authority |
| Web | public orientation, navigation, dated arguments, and maturity language | source, tests, releases, operations, research setup, and live state |

The central [`projects/README.md`](../../projects/README.md) links all nine repositories, their current authority entry points, and the public project directory. Every repository README links back to that map.

### Required checks

The closeout used each repository's existing contract rather than inventing one universal command.

| Repository | Required verification result |
| --- | --- |
| Computing | conformance gate, strict content check, and managed-document lint/link checks |
| Runtime | Rust formatting, Clippy, all-target/all-feature tests, transactional feature tests, Python operational tests, Ruff, generated-document contract, and local acceptance contract |
| Host | compileall, Ruff, 167 deterministic tests, and wheel build |
| Harness | compileall, Ruff, 256 deterministic tests against the current Host source graph, and wheel build |
| Game | TypeScript, browser-source syntax, 226 tests, and the registered product browser journey |
| Human | deterministic economic baseline reproduction, population-to-individual simulation reproduction, and compileall |
| Security | compileall and 29 active experiment/evaluation tests; one optional environment-dependent CAGE test remained skipped |
| World | Cloudflare provider CI and VPN controller checks |
| Web | publication contract, TypeScript, ESLint, 57-page production build, static budget, and 136 desktop/mobile browser tests |

The extra unregistered Station Zero v3 preview browser script was also exercised. It reported one console 404 and is retained as preview debt; it is not part of the registered Game product's required CI and was not converted into a documentation-governance code change.

### Baseline observation

The initial P0 inventory and the closeout inventory are linked from [`../../research/evidence/README.md`](../../research/evidence/README.md). The comparison is intentionally descriptive. More documents or metadata do not imply better quality, and warnings are not a backlog to clear mechanically.

The strongest structural signal from the governance round is the reduction in documents with no Markdown navigation while the long historical corpus was retained. The final counts and per-repository states are recorded in [`../../research/evidence/content-engineering-closeout-baseline.md`](../../research/evidence/content-engineering-closeout-baseline.md) and its JSON receipt.

## Retained

The following material remains because it carries evidence or necessary operational detail:

- source-grounded studies, experiments, reports, release records, migration notes, and failure analyses;
- long research reports whose length reflects evidence rather than a default entry-page design;
- historical Host and Harness phase documents with explicit banners and links to current authority;
- the initial P0 baseline as immutable pre-governance evidence;
- Game v3 design and implementation records as an implemented but unregistered preview;
- Security Round 1 traces and reports without promoting the deleted Campaign architecture;
- World negative results showing why the shared semantic layer did not survive;
- Web articles as dated arguments, including historical publications with visible later corrections.

Retaining these records does not restore them as canonical architecture, current product status, or default navigation.

## Removed

Across the completed documentation tasks, duplication and obsolete authority were reduced through targeted consolidation rather than corpus-wide rewriting:

- Host's root `CLOSURE.md` was merged into `docs/MIGRATION.md` and deleted;
- Harness's misplaced `H_SERIES_OPEN_PROPOSAL.md` was deleted;
- Host and Harness phase reports were marked historical or superseded where appropriate;
- stale Host ownership of Assignment and Agent Run semantics was removed after Harness extraction;
- Runtime language that described its Registry as a Task-fact database was replaced with physical execution ownership;
- the shared World service, database, router, workflow, and universal interaction-schema thesis was removed from active authority, leaving only retained owner-local capabilities;
- Security Campaign machinery and strategic ontology were not promoted after the experiment layer survived comparison;
- Game's registered v2 product, implemented v3 preview, and historical alpha were separated instead of presented as one current state;
- Web's obsolete four-project map, future-Harness claim, and World-as-execution-layer narrative were replaced with the current project family.

No bulk deletion was performed solely because a file lacked metadata, links, or a recent date.

## Open questions

### Historical corpus debt

Many historical and supporting documents still lack Ordivon metadata, explicit lifecycle fields, or Markdown links. This is acceptable while they remain outside strict managed paths and outside the default reading path. A local edit should reassess them; a bulk metadata migration is not justified by counts alone.

### Long documents

The number of documents at or above 2,000 words did not materially decline. Some are valuable complete reports. Future work should add summaries or navigation only when reader evidence shows retrieval friction, not split documents to improve a metric.

### Authored public status

Ordivon Web still uses an authored projection rather than automatic repository synchronization. That is deliberate, but it requires updating Web when a project's public role, maturity, registration, retirement, or next destination changes.

### Preview and optional-path debt

Station Zero v3 remains an implemented, unregistered preview. Its optional browser script currently observes a console 404 and should be repaired or deliberately removed before v3 becomes a registered product gate. Optional external environments, including Security CAGE paths and Runtime real-system acceptance, remain explicit rather than silently simulated on hosted CI.

### Advisory warning volume

Warnings remain concentrated in Computing's historical research corpus, Human's practical research collection, and Web's article corpus. They identify possible review pressure; they do not establish incorrectness. The project should prioritize warnings only when they affect a current entry, authority path, active operation, public claim, or repeated maintenance task.

### Maintenance and restart

The ordinary maintenance rules and concentrated-governance restart conditions are canonical in [`README.md`](README.md). Another cross-repository round is warranted only when ownership changes, duplicate canonical authority appears, Web and repository facts diverge materially, current documents become isolated, shared contracts change several repositories, or the same policy defect recurs across multiple projects.
