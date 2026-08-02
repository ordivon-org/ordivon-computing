---
schema_version: 1
id: computing.content-engineering.baseline
title: Ordivon content engineering baseline
type: report
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - agent
updated: 2026-08-02
summary: Advisory structural inventory of the current Ordivon documentation corpus.
evidence_status: observed
readiness: DEGRADED
applies_to:
  - ordivon-project-family
related:
  - computing.content-engineering.p0
---
# Ordivon content engineering baseline

## Executive judgment

Ordivon has crossed the threshold where documentation must be treated as shared engineering infrastructure. This inventory remains advisory: counts expose migration pressure but do not authorize rewriting, deletion, or promotion.

## Question

What structural documentation debt exists across the active Ordivon repositories before any large-scale text migration begins?

## Method

The dependency-free content checker scanned Git-tracked and unignored Markdown or MDX files under each repository's declared documentation roots. It counted metadata adoption, approximate words, Markdown links, long documents, and structural warnings. It did not judge claim truth or prose quality.

## Findings

### System summary

- Repositories: 9
- Markdown/MDX documents: 340
- Documents with Ordivon metadata: 1
- Approximate words: 301781
- Documents without Markdown links: 229
- Documents at or above 2,000 words: 24

### Repository inventory

| Project | Documents | Metadata | Words | No links | Long | Manifest | State |
|---|---:|---:|---:|---:|---:|---|---|
| ordivon-computing | 199 | 1 | 159080 | 120 | 10 | yes | DEGRADED |
| ordivon-game | 6 | 0 | 4990 | 5 | 0 | yes | DEGRADED |
| ordivon-harness | 11 | 0 | 16637 | 6 | 3 | yes | DEGRADED |
| ordivon-host | 13 | 0 | 10271 | 11 | 1 | yes | DEGRADED |
| ordivon-human | 40 | 0 | 30224 | 28 | 0 | yes | DEGRADED |
| ordivon-runtime | 12 | 0 | 11166 | 7 | 2 | yes | DEGRADED |
| ordivon-security | 14 | 0 | 15725 | 10 | 1 | yes | DEGRADED |
| ordivon-web | 32 | 0 | 48947 | 30 | 7 | yes | DEGRADED |
| ordivon-world | 13 | 0 | 4741 | 12 | 0 | yes | DEGRADED |

## Limitations

Word count, link count, paragraph length, and phase-code detection are diagnostic proxies. A long or link-free document may be correct and useful. The baseline does not establish factual accuracy, citation support, reader comprehension, or whether any specific document should survive.

## Evidence

The machine-readable sibling receipt records the same inventory at `2026-08-02T23:14:24Z`. Repository manifests were validated before inclusion.

## Next action

Admit only high-authority paths into strict management, starting with current architecture, active research questions, accepted decisions, operations, and flagship public reports. Do not bulk-convert the historical corpus.
