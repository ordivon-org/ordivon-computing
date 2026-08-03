---
schema_version: 1
id: computing.content-engineering.baseline
title: Ordivon content engineering P0 baseline
type: report
profile: research
lifecycle: accepted
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - agent
updated: 2026-08-03
summary: Initial advisory structural inventory captured before the cross-repository documentation governance round.
evidence_status: observed
readiness: DEGRADED
applies_to:
  - ordivon-project-family
related:
  - computing.content-engineering.p0
---
# Ordivon content engineering P0 baseline

## Executive judgment

This initial inventory established that Ordivon had crossed the threshold where documentation must be treated as shared engineering infrastructure. This inventory remains advisory: counts expose migration pressure but do not authorize rewriting, deletion, or promotion.

## Question

What structural documentation debt exists across the active Ordivon repositories before any large-scale text migration begins?

## Method

The dependency-free content checker scanned Git-tracked and unignored Markdown or MDX files under each repository's declared documentation roots. It counted metadata adoption, approximate words, Markdown links, long documents, and structural warnings. It did not judge claim truth or prose quality.

## Findings

### System summary

- Repositories: 9
- Markdown/MDX documents: 366
- Documents with Ordivon metadata: 59
- Approximate words: 338691
- Documents without Markdown links: 215
- Documents at or above 2,000 words: 26

### Repository inventory

| Project | Documents | Metadata | Words | No links | Long | Manifest | State |
|---|---:|---:|---:|---:|---:|---|---|
| ordivon-game | 11 | 8 | 13044 | 3 | 1 | yes | DEGRADED |
| ordivon-harness | 12 | 3 | 17238 | 4 | 3 | yes | DEGRADED |
| ordivon-host | 14 | 4 | 10935 | 9 | 1 | yes | DEGRADED |
| ordivon-runtime | 13 | 5 | 11828 | 5 | 2 | yes | DEGRADED |
| ordivon-security | 16 | 8 | 17622 | 6 | 1 | yes | DEGRADED |
| ordivon-web | 33 | 4 | 49401 | 30 | 7 | yes | DEGRADED |
| ordivon-world | 14 | 10 | 6797 | 6 | 0 | yes | DEGRADED |
| ordivon-computing | 201 | 9 | 160754 | 118 | 10 | yes | DEGRADED |
| ordivon-human | 52 | 8 | 51072 | 34 | 1 | yes | DEGRADED |

## Limitations

Word count, link count, and phase-code detection are diagnostic proxies. A long or link-free document may be correct and useful. The baseline does not establish factual accuracy, citation support, reader comprehension, or whether any specific document should survive.

## Evidence

The machine-readable sibling receipt records the same inventory at `2026-08-03T09:17:41Z`. Repository manifests were validated before inclusion.

## Next action

Admit only high-authority paths into strict management, starting with current architecture, active research questions, accepted decisions, operations, and flagship public reports. Do not bulk-convert the historical corpus.
