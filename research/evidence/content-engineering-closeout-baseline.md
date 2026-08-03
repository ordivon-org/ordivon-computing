---
schema_version: 1
id: computing.content-engineering.closeout-baseline
title: Ordivon Content Engineering Closeout Baseline
type: report
profile: research
lifecycle: accepted
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - editor
  - agent
updated: 2026-08-04
summary: Advisory post-governance inventory and comparison for the nine-repository Ordivon documentation system.
evidence_status: observed
readiness: DEGRADED
applies_to:
  - ordivon-project-family
related:
  - computing.content-engineering.baseline
  - computing.content-engineering.closeout
  - computing.content-engineering
---
# Ordivon Content Engineering Closeout Baseline

## Executive judgment

The documentation system grew because the project family gained independent Harness authority, complete public project pages, retained research paths, operational Runtime documents, and governance evidence. At the same time, navigation improved: documents without Markdown links fell from **215** to **179** even though the corpus expanded from **366** to **379** documents.

Warnings declined from **575** to **547**, but the closeout does not interpret that reduction as a quality score. Long documents remained at **26**, reflecting the deliberate retention of complete research reports, experiment records, and historical analyses. All nine repositories have valid manifests and zero strict managed-content blockers; every repository remains `DEGRADED` because advisory historical or supporting debt is still present.

## Question

How did the nine-repository documentation corpus change during the governance round, and which structural pressures remain without treating the metrics as quality targets?

## Method

The dependency-free content checker scanned Git-tracked and unignored Markdown or MDX files under each repository's declared documentation roots. It validated project manifests, counted metadata adoption, approximate words, Markdown links, long documents, and structural warnings, and recorded each repository's strict-content state. The initial comparison source is the accepted P0 baseline. The checker does not judge claim truth, reader comprehension, or whether a particular historical document should be removed.

Both snapshots cover the same nine repositories. The closeout scan includes the final governance record, the closeout baseline itself, the current Web information architecture, and Runtime's expanded public documentation set. Counts therefore describe the resulting system rather than a fixed-file migration cohort.

## Findings

### System comparison

| Metric | P0 | Closeout | Change |
| --- | ---: | ---: | ---: |
| Repositories | 9 | 9 | 0 |
| Markdown/MDX documents | 366 | 379 | +13 |
| Documents with Ordivon metadata | 59 | 68 | +9 |
| Approximate words | 338,691 | 351,198 | +12507 |
| Documents without Markdown links | 215 | 179 | -36 |
| Documents at or above 2,000 words | 26 | 26 | 0 |
| Structural warnings | 575 | 547 | -28 |

### Repository comparison

| Project | Documents | Metadata | Words | No links | Long | Warnings | Final state |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Computing | 201→206 | 9→11 | 160,754→165,018 | 118→115 | 10→10 | 368→366 | DEGRADED |
| Runtime | 13→19 | 5→10 | 11,828→17,725 | 5→7 | 2→2 | 11→14 | DEGRADED |
| Host | 14→13 | 4→4 | 10,935→11,553 | 9→0 | 1→1 | 16→11 | DEGRADED |
| Harness | 12→12 | 3→4 | 17,238→17,456 | 4→0 | 3→3 | 12→8 | DEGRADED |
| Game | 11→11 | 8→8 | 13,044→13,132 | 3→3 | 1→1 | 6→6 | DEGRADED |
| Human | 52→54 | 8→8 | 51,072→51,465 | 34→12 | 1→1 | 86→66 | DEGRADED |
| Security | 16→16 | 8→8 | 17,622→17,710 | 6→6 | 1→1 | 12→12 | DEGRADED |
| World | 14→14 | 10→10 | 6,797→6,876 | 6→6 | 0→0 | 4→4 | DEGRADED |
| Web | 33→34 | 4→5 | 49,401→50,263 | 30→30 | 7→7 | 60→60 | DEGRADED |

### Interpretation

- **Navigation improved more than corpus size changed.** The system added documents and words while reducing link-free pages by **36**. Repository README family links, central authority navigation, historical banners, and Web project routing explain most of the structural gain.
- **Metadata was concentrated, not universalized.** Metadata adoption rose by **9** documents because new or promoted canonical surfaces declared roles. Historical corpora were not bulk-converted.
- **Long-form evidence was retained.** The long-document count remained **26**. This is consistent with preserving full experiment reports, practical research paths, and historical derivations while improving their entry points.
- **Warning pressure remains uneven.** Computing, Human, and Web retain the largest advisory corpora. World, Game, Host, Harness, Runtime, and Security have smaller but non-zero historical or supporting debt. These differences reflect repository purpose and corpus shape rather than a documentation ranking.
- **No repository is structurally blocked.** Strict managed paths validate, while `DEGRADED` records the continuing advisory corpus outside those paths.

## Limitations

The baseline is a structural snapshot, not a quality score. A link-free article may have complete navigation through the Web interface; a long report may be the correct evidence unit; a warning may describe intentionally retained history. Counts also change when new products, research cycles, canonical operating documents, or closeout evidence are added. No deletion, rewrite, metadata promotion, or governance restart is authorized by a number alone.

The checker does not test whether two prose claims are semantically equivalent, whether a reader can understand a page, whether external evidence supports a conclusion, or whether a public deployment currently contains the latest source commit. Those questions require authority review, browser tests, repository checks, or explicit research evidence.

## Evidence

The machine-readable sibling receipt records the exact per-repository inventory. The initial reference is [`content-engineering-p0-baseline.json`](content-engineering-p0-baseline.json); the final receipt is [`content-engineering-closeout-baseline.json`](content-engineering-closeout-baseline.json). Boundary and maintenance interpretation is recorded in [`../../docs/content-engineering/FINAL-CLOSEOUT.md`](../../docs/content-engineering/FINAL-CLOSEOUT.md).

The closeout inventory was generated after all nine repository navigation changes were integrated and after Runtime's new canonical public documents were restored to the shared content contract. Required functional checks are recorded in the closeout rather than inferred from these counts.

## Next action

Use the baseline only when a concrete maintenance question appears: duplicate authority, a broken default path, a new unlinked current document, public/repository status disagreement, or repeated warning patterns on active surfaces. Ordinary historical warning volume should remain advisory and be handled locally when the material is substantively edited.
