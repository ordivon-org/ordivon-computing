---
schema_version: 1
id: computing.content-engineering.p0
title: Ordivon Content Engineering P0
type: architecture
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - contributor
  - agent
updated: 2026-08-04
summary: Shared content contracts, profiles, checks, templates, and migration boundaries for Ordivon repositories.
evidence_status: verified
readiness: DEGRADED
applies_to:
  - ordivon-project-family
related:
  - computing.content-engineering.baseline
  - computing.content-engineering.closeout-baseline
  - computing.content-engineering.closeout
---
# Ordivon managed-document metadata boundary

## Purpose

Computing retains one narrow documentation-specific invariant: a repository may explicitly mark a small set of documents as `managed_paths`, and those documents must carry stable identity, lifecycle, source-role, ownership, and canonical-role metadata. This exists because a real managed-frontmatter deletion was caught by the Ordivon validator while markdownlint-cli2, Vale, and CSpell all passed it.

The broader P0 Content Engineering apparatus is historical. Templates, fixtures, schema/profile packages, cross-repository baseline generation, word/link metrics, and phase-path warning counts did not earn current existence. Their exact history remains recoverable from Git and the retained content-engineering evidence.

## Boundaries

The current validator may:

- validate `.ordivon/project.yaml` documentation roots, managed paths, and enforcement mode;
- require metadata only for documents explicitly inside managed paths;
- validate document id, lifecycle, source role, owner/audience shape, and basic metadata fields;
- reject duplicate managed document identities and duplicate managed canonical identities;
- emit a deterministic receipt and fail closed in strict mode.

It may not:

- judge whether a claim is true, current, useful, or authorized;
- make unmanaged legacy documentation a governance backlog;
- replace Vale, markdownlint-cli2, CSpell, or Lychee;
- generate quality scores from word/link/warning counts;
- create templates or repository-wide migration pressure.

## Components

- `.ordivon/project.yaml` — owner-local declaration of documentation roots and managed paths.
- `packages/content-cli/` — compatibility package containing the small metadata validator.
- `scripts/ordivon_content.py` — stable source-tree entry used by Computing and optional external consumers such as Human.
- `.vale/styles/Ordivon/` — two bounded prose suggestions used by Vale; these are generic lint configuration, not a content contract package.
- Vale, markdownlint-cli2, CSpell, and Lychee — mature tooling for prose, Markdown, spelling, and links.

## Data flow

```text
.ordivon/project.yaml
+ Git-visible Markdown/MDX
→ select only managed paths
→ parse front matter
→ validate identity/lifecycle/source role
→ detect duplicate managed identities
→ BLOCKED | DEGRADED | READY
```

`READY` means only that this narrow metadata contract found no current violation. It does not prove document semantics.

## Failure modes

The validator should be deleted or narrowed again if generic tooling gains the same managed-metadata capability, if repositories stop consuming the shared source-tree entry, or if the metadata fields cease to protect a repeated failure. It must not regrow corpus inventory, template generation, semantic freshness checking, or baseline scoring without new evidence.

## Verification

```bash
PYTHONPATH=packages/content-cli/src python -m unittest discover -s packages/content-cli/tests
python scripts/ordivon_content.py project --root .
python scripts/ordivon_content.py check --root . --mode strict
```

General document checks remain separate:

```bash
vale <managed-docs>
markdownlint-cli2 <managed-docs>
cspell lint --no-progress --no-summary <managed-docs>
lychee --config lychee.toml <managed-docs>
```

## Historical evidence

The original inventory and closeout baselines remain under `research/evidence/` as historical diagnostic evidence. The Existence Gauntlet records why only the managed-metadata invariant survived the 2026-08-10 removal-first attack. Git preserves the removed Content packages exactly.
