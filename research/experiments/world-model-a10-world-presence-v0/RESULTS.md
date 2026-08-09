---
schema_version: 1
id: computing.research.world-model-a10-world-presence-results
title: World Model A10 World Presence Results
type: reference
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-09
summary: Second-domain A10 result: World Presence independently reproduces time-scoped truth admission while falsifying the need for a shared temporal relation index in this workload.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-world
  - ordivon-harness
related:
  - computing.research.world-model-loop
  - computing.foundations
---
# World Model A10 World Presence Results

Machine acceptance: [`../../evidence/wml-a10-world-presence-acceptance-6741b1ddbea5.json`](../../evidence/wml-a10-world-presence-acceptance-6741b1ddbea5.json). Raw live-Agent receipt: [`../../evidence/wml-a10-world-presence-944dc99293dd.json`](../../evidence/wml-a10-world-presence-944dc99293dd.json).

## Result

World independently reproduces the semantic relation behind Core A10:

```text
historical owner evidence
!=
current query-scoped relation truth
```

but it **does not** reproduce the Security experiment's pressure for an extra temporal evidence-reduction mechanism. World already expresses the relation through owner-native query, Subject, Body, scope, current observation, and current binding semantics.

## Owner-defined cases

All eight evaluator cases come directly from committed World Presence laws:

- old Game occurrence plus a new Planning scope without a new binding → `unknown`;
- same Body plus a new exact current binding → `present-within-scope`;
- current Security Body with Subject activation unproven → `unknown`;
- exact destroyed Security Body with historical materialization Receipt retained → `absent-through-body`;
- current owner observation timeout with historical success retained → `unknown`;
- one Subject simultaneously present through Game while absent through Security Body A → query each Body independently;
- replacement Body B cannot inherit Body A evidence, and failed B observation remains `unknown`.

Computing did not invent any additional Presence invalidation rule.

## Live Agent result

Two predeclared replicates produced 32 Provider decisions:

| Treatment | Correct | Decisions | Total tokens | Prompt tokens |
|---|---:|---:|---:|---:|
| RAW_OWNER_RECORDS | 16 | 16 | 27,582 | 21,960 |
| QUERY_RELATION_INDEX | 16 | 16 | 31,194 | 25,780 |

Both treatments were 16/16. Across all 16 paired comparisons:

```text
answer changed        = 0
index fixed RAW error = 0
index harmed RAW      = 0
```

The index increased total Provider tokens by approximately **13.1%** and prompt tokens by approximately **17.4%**.

The index therefore supplied no observed correctness value in this bounded workload.

## Why RAW was sufficient

RAW reasoning correctly used the owner relations rather than one global last-known state. For example:

```text
same Subject + same Game Body
+ old r0 occurrence
+ current r1 Body
+ old r0 binding rejected for r1
→ UNKNOWN
```

and:

```text
historical Security materialization
+ current owner observation timeout
→ UNKNOWN
```

and:

```text
Game Body current + exact current binding
Security Body A currently absent
same Subject
→ Game query PRESENT
→ Security Body-A query ABSENT-through-body
```

The Agent also rejected old Body-A evidence for replacement Body B after B failed to obtain a valid current owner observation.

## Cross-domain interpretation

Security and World now independently support the same high-level world-model distinction but with different local friction:

```text
Security
  previously state-establishing witness
  + later potentially state-changing uncertainty
  → RAW Agent sometimes over-extends old truth

World
  historical occurrence/materialization
  + exact owner query/body/scope laws
  → RAW Agent already resolves the current relation correctly
```

This means the shared invariant is **not** `PROPERTY_TIMELINE`, `temporalAdmission`, `fresh`, or any other particular representation.

The more durable cross-domain relation is:

```text
current-enough evidence
=
owner-native evidence interpreted for
one exact property/relation + owner + query/scope + relevant current observation boundary
```

Core A10 already covers this at the required abstraction level. No Core text revision is justified.

## Mechanism disposition

The Security `PROPERTY_TIMELINE` follow-up remains a useful local experiment technique because it repaired one false-certainty decision there. It does **not** graduate into a shared candidate merely because World is also temporal. World supplies a counterexample to that promotion: its owner-native relation vocabulary already carries enough structure, and the added index only increased cost.

Therefore:

- generic freshness service: rejected;
- shared temporal evidence index: rejected for now;
- World Presence registry/global epoch: rejected;
- owner-native query-shaped current relation: retained;
- Core A10: cross-domain supported, unchanged.

## Next pressure

The most useful next experiment is no longer another freshness representation. The prior Security campaign exposed a different failure:

```text
structured submitted answer
!=
its own semantic rationale
```

That now deserves an independent Harness/evaluation falsifier. If an Agent can derive the right truth in its reasoning but submit the wrong structured decision, evidence freshness and context quality cannot repair the final action boundary by themselves.
