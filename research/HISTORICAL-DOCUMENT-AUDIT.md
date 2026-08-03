# Computing Historical Document Governance Audit

> **Status:** one-time governance record for `ordivon-computing@faa957c`. This file records dispositions; it is not architecture or portfolio authority.

## Authority conflicts resolved

1. `research/portfolio.json` is the only mutable research-status source; `PORTFOLIO.md` is a generated projection.
2. Historical page-local words such as `active`, `current`, `next`, and `roadmap` cannot override `docs/authority.md` or the portfolio.
3. Edge, Link, and World 001 questions are superseded; Security 003–004 are deferred and 005–006 are blocked.
4. Published prose and historical audits cannot redefine Core, product ownership, or current implementation state.

## High-impact dispositions

| Path or group | Disposition | Governance result |
|---|---|---|
| `README.md`, `docs/authority.md`, `core/*` | retain | Remain the canonical human-readable architecture and authority entry. |
| `research/portfolio.json` | retain | Sole mutable source for status, maturity, blockers, and Ready Frontier. |
| `research/PORTFOLIO.md` | rewrite-summary | Generator now states that the JSON source, not the rendered page, owns truth. |
| `research/README.md`, `research/experiments/README.md`, `research/charters/README.md` | rewrite-summary | Navigation now distinguishes durable pages from mutable status and generated views. |
| Edge, Link, and World 001 question pages | historical | Page headers now match their superseded portfolio status. |
| Security 002–006 question pages | historical / rewrite-summary | Successor, deferred, and blocked status now matches the portfolio without rewriting research bodies. |
| `ANC-IR-001`, `ANC-MEMORY-001`, `ANC-GAME-001` | rewrite-summary | Added completed-reference boundaries; stale pre-closeout wording no longer appears current. |
| `ANC-GAME-002`, `ANC-HARNESS-002`, `ANC-VERIFY-001` | rewrite-summary | Page-local maturity and activation wording now matches the portfolio. |
| `harness-boundary-v0/README.md` | historical | H1–H5 rejection is explicitly scoped to a shared mature-Provider lifecycle, not the later bare-model Harness. |
| `harness-evaluation-v0/README.md` | rewrite-summary | R0–R2 and the curated evidence set are acknowledged; the obsolete disposable-runner next step was removed. |
| `core-work-system-v1/REPORT.md` | rewrite-summary | Long report points first to compact results and decisions and disclaims current product authority. |
| Adaptive Acceleration publication files | merge / archive / delete | `PUBLICATION.md` is the single publication copy; the long manifesto is archived; the edit record was merged and deleted. |
| Paradigm Reform study | rewrite-summary / archive / historical | A short README is now the entry; the 3,900-word audit moved to `AUDIT.md`; the reform sequence is explicitly historical. |
| Classical, concept-system, Task-to-World, adversarial, and Game study entries | rewrite-summary | Entry status now matches reference, completed, deferred, or conditional portfolio state. |
| Edge/Link charter 002 and 003 pairs | retain historical | They preserve materially different Phase 0 and continuity hypotheses; existing supersession banners are sufficient. |
| Dogfood evidence and Protocol normative artifacts | retain untouched | Governed by Task A and Protocol authority respectively; excluded from this audit. |

## Deletion rule applied

Only content with a stronger retained owner and no independent evidence role was deleted. Git history remains the recovery path. Long evidence reports were not shortened merely to reduce word count; they received a result or authority summary when search snippets could otherwise mislead.
