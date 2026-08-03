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
# Ordivon Content Engineering P0

## Purpose

Content Engineering gives Ordivon repositories a shared way to identify, validate, navigate, and project research and engineering documents. It does not become a second owner of project facts.

The P0 contract separates four concerns:

```text
project repository owns facts and evidence
→ content metadata declares document identity and lifecycle
→ deterministic checks expose structural failure and migration debt
→ Web, Agents, and tools consume bounded projections
```

## Boundaries

P0 does not require immediate metadata migration for the existing document corpus. Each repository declares `managed_paths`; strict requirements apply only after a path is explicitly admitted.

The content layer may validate:

- document identity, type, lifecycle, source role, and visibility;
- required sections for an admitted document type;
- relative links, duplicate identifiers, navigation signals, and oversized paragraphs;
- project manifests and machine-readable check receipts.

It may not decide whether a research claim is true, whether a project is authorized to act, whether a prototype is production-ready, or whether an old document should be deleted.

## Components

- `packages/content-contract/` owns schemas, profiles, terminology, and shared tool configuration.
- `packages/content-cli/` owns only Ordivon-specific metadata, lifecycle, source-role, relationship, receipt, and baseline checks.
- Vale, markdownlint-cli2, CSpell, and Lychee own prose rules, Markdown structure, spelling, and link integrity. Their versions are pinned in `mise.toml`, and the Computing gate derives their document inputs from `.ordivon/project.yaml` `managed_paths` rather than a duplicated path list.
- `packages/content-templates/` provides starting structures; templates are not canonical facts.
- `packages/content-fixtures/` provides valid and invalid cases for regression tests.
- `.ordivon/project.yaml` declares one repository's content boundary and adoption mode.

## Data flow

```text
Markdown or MDX + .ordivon/project.yaml
→ front-matter and project-manifest parsing
→ contract and relationship checks
→ issue set
→ BLOCKED | DEGRADED | READY
→ JSON receipt and optional baseline report
```

`READY` means that the configured content checks found no current issue. It does not grant authority, prove claims, or authorize publication.

## Failure modes

The principal P0 failure modes are:

- treating warning counts as quality targets;
- enabling strict mode over a legacy corpus before ownership and source roles are known;
- using automatic prose revision to change claims, numbers, limitations, or authorization;
- creating duplicated canonical facts in Web or generated indexes;
- adding metadata that merely restates filenames without improving lifecycle or navigation.

The response is bounded adoption: advisory inventory first, strict enforcement only for admitted paths, and deletion of checks that do not expose a named failure. The current Computing authority set is recorded in [`../authority.md`](../authority.md); shared schemas and profiles are documented in [`../../packages/content-contract/README.md`](../../packages/content-contract/README.md).

## Verification

Install the pinned external tools, then run the local package tests and repository checks:

```bash
mise install
PYTHONPATH=packages/content-cli/src python -m unittest discover -s packages/content-cli/tests
python scripts/ordivon_content.py project --root .
python scripts/ordivon_content.py check --root . --mode advisory --receipt /tmp/ordivon-content.json
vale docs/content-engineering/README.md
markdownlint-cli2 docs/content-engineering/README.md
cspell lint --no-progress --no-summary docs/content-engineering/README.md
lychee --config lychee.toml docs/content-engineering/README.md
```

Generate a cross-repository baseline only when all local repositories are available:

```bash
python scripts/ordivon_content.py baseline \
  --repository-parent /root/projects \
  --json-output /tmp/ordivon-content-baseline.json \
  --markdown-output /tmp/ordivon-content-baseline.md
```

## Maintenance rules

The documentation system stays lightweight when ordinary changes follow six rules:

1. **Declare the role of a new core document.** A new entry, architecture, operations, current-answer, or authority document declares metadata, names the fact it owns, links from the existing entry path, and identifies any source it replaces.
2. **Update the owning summary when a boundary changes.** A change to architecture or operations updates the canonical owner, the repository README summary, and Ordivon Web only when the public role, maturity, or next destination changes.
3. **Reassess old documents when editing them materially.** A substantive change to a phase report, closeout, proposal, or historical design requires an explicit lifecycle and source-role decision; editing does not silently make it current.
4. **Keep history out of the default path.** Historical material may remain valuable evidence, but confident language, a recent edit date, or a broken old link cannot restore it as a default entry or alternate architecture.
5. **Connect before creating.** A new document should extend the existing README, authority map, research registry, operations route, or evidence index. If no existing route should link it, the document is probably not yet admitted.
6. **Use baselines diagnostically.** Document, word, link, length, metadata, and warning counts reveal review pressure. They are not quality scores and are never targets to drive to zero without a named reader or maintenance failure.

## When to reopen concentrated governance

Start another cross-repository documentation round only when at least one system-level condition appears:

- two canonical sources claim the same current fact or responsibility;
- a repository extraction, merge, retirement, or product registration changes project ownership;
- the public Web map materially disagrees with repository authority;
- repeated changes create unlinked current documents or ambiguous default entry paths;
- required checks cannot determine which documents are authoritative inputs;
- a promoted shared contract changes the responsibility boundary of multiple repositories; or
- accumulated local fixes require the same policy decision in several repositories.

Ordinary stale links, isolated wording defects, one new research report, or advisory warning growth should be handled locally rather than triggering a governance program.

## Governance record

The initial inventory is preserved in [`../../research/evidence/content-engineering-p0-baseline.md`](../../research/evidence/content-engineering-p0-baseline.md). The post-governance comparison is [`../../research/evidence/content-engineering-closeout-baseline.md`](../../research/evidence/content-engineering-closeout-baseline.md), and [`FINAL-CLOSEOUT.md`](FINAL-CLOSEOUT.md) records the completed cross-repository review, remaining debt, and restart conditions.
