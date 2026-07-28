# Publication Edit — Candidate 0.2

## Purpose

Convert the source-grounded research manifesto into an Ordivon Web article without weakening its accelerationist position.

## Editorial changes

### Preserve

- the strong historical claim that useful general-purpose capabilities continue to be rediscovered, copied, and expanded in a plural civilization;
- the rejection of global frontier slowdown as a durable civilizational strategy;
- the long horizon of AI, robotics, automated science, engineered biology, energy, and off-world industry;
- the distinction between governing consequences and owning the horizon of intelligence;
- the Ordivon objective of `verified improvement / unit time`;
- the non-domination framing for possible future intelligent participants.

### Remove or reduce

- repeated declarations of the same position;
- policy-paper tables and long lists;
- internal Ordivon primitive names that require repository context;
- claims that sound like smooth technological inevitability;
- false dichotomies between progress and immediate collapse;
- phrasing that treats every unresolved objection as already refuted;
- manifesto cadence in every paragraph, which reduces the force of the passages that should carry it.

### Reframe

- “technology always moves forward” becomes a conditional historical claim: if civilization survives and remains plural, useful general-purpose capabilities continue to be searched for and recombined;
- “pacing is impossible” becomes: pacing can interrupt specific trajectories but cannot credibly serve as the stable foundation of a plural technological civilization;
- “govern effects, not capability” becomes: govern consequences and observable high-risk bottlenecks without claiming permanent ownership of future intelligence;
- Ordivon moves from internal architecture exposition to an accessible example of infrastructure for fast, persistent, recoverable work.

## Publication structure

1. Opening tension: major revolutions rarely wait for readiness.
2. Long-run historical mechanism: cumulative knowledge and competitive adoption.
3. Organizational complementarity: electricity, computing, and AI absorption.
4. AI discontinuity: intelligence enters the production of knowledge.
5. Pacing critique: local controls versus global civilizational direction.
6. Positive program: whole-system acceleration.
7. Governance and non-domination.
8. Ordivon as a concrete response.
9. Strong but restrained conclusion.

## Web implementation

The publication candidate has been adapted in [Ordivon Web Draft PR #28](https://github.com/zycxfyh/ordivon-web/pull/28).

The Web version adds:

- canonical Article metadata, Open Graph, Twitter metadata, and JSON-LD;
- a visible seven-part table of contents;
- a central-thesis callout;
- a six-stage long-horizon technology path;
- a six-part civilizational-acceleration model;
- 13 grouped endnotes derived from 22 study reference identifiers;
- inline numbered citations with back-links;
- a direct route to this full research record;
- responsive desktop, tablet, and mobile layouts;
- Notes, homepage, Atom, and Sitemap integration.

The rendered copy makes a few publication-level refinements without changing the thesis. For example, “the demand is not foolish” becomes “the concern is not frivolous,” and the `Pacing the Frontier` trigger is introduced directly rather than left implicit.

The Web branch was rebased onto the latest `ordivon-web/main` after removal of the retired Finance and FinHarness surfaces. The publication does not restore those routes, assets, or narratives.

## Validation

- Computing conformance validates the research record and source identifiers;
- Web dependency-free contract passes across 19 HTML routes;
- Playwright passes 57 checks: 19 routes across desktop, tablet, and mobile;
- article-specific checks require a visible TOC, six future-path cards, six acceleration cards, and 13 source groups at every viewport;
- no horizontal overflow, serious or critical accessibility violations, console errors, or missing local assets were found;
- external-link sampling includes the full research branch and passed;
- `git diff --check` passed.

## Current assessment

- Research strength: high
- Position clarity: high
- Publication readability: ready for review
- Citation presentation: complete
- Responsive visual treatment: complete
- Web implementation: Draft PR prepared, not merged or live
- Remaining work: human editorial approval and merge decision
