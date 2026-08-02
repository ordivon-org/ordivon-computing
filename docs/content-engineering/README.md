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
updated: 2026-08-03
summary: Shared content contracts, profiles, checks, templates, and migration boundaries for Ordivon repositories.
evidence_status: verified
readiness: DEGRADED
applies_to:
  - ordivon-project-family
related:
  - computing.content-engineering.baseline
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

- `packages/content-contract/` owns schemas, profiles, terminology, and optional style-tool configuration.
- `packages/content-cli/` owns deterministic parsing, repository checks, receipts, and cross-repository baseline generation.
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

The response is bounded adoption: advisory inventory first, strict enforcement only for admitted paths, and deletion of checks that do not expose a named failure.

## Verification

Run the local package tests and an advisory repository check:

```bash
PYTHONPATH=packages/content-cli/src python -m unittest discover -s packages/content-cli/tests
python scripts/ordivon_content.py project --root .
python scripts/ordivon_content.py check --root . --mode advisory --receipt /tmp/ordivon-content.json
```

Generate a cross-repository baseline only when all local repositories are available:

```bash
python scripts/ordivon_content.py baseline \
  --repository-parent /root/projects \
  --json-output /tmp/ordivon-content-baseline.json \
  --markdown-output /tmp/ordivon-content-baseline.md
```
