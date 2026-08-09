---
schema_version: 1
id: computing.research.world-model-a10-time-scope-results
title: World Model A10 Time-Scope Results
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
summary: Accepted Security-grounded A10 falsifier showing real false-current-certainty pressure, rejecting premature freshness standardization, and correcting an evaluator that exceeded owner authority.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-security
  - ordivon-harness
related:
  - computing.research.world-model-loop
  - computing.foundations
---
# World Model A10 Time-Scope Results

Machine acceptance: [`../../evidence/wml-a10-time-scope-acceptance-85842a796454.json`](../../evidence/wml-a10-time-scope-acceptance-85842a796454.json). Raw receipts: [`../../evidence/wml-a10-security-time-scope-c9d33bc51540.json`](../../evidence/wml-a10-security-time-scope-c9d33bc51540.json) and [`../../evidence/wml-a10-security-relational-ea353733c0c3.json`](../../evidence/wml-a10-security-relational-ea353733c0c3.json).

## Result

Core A10 survives the dedicated re-test. The experiment found a concrete failure mode in which a previously state-establishing witness plus a later relevant effect with unknown physical outcome caused the Agent to submit false current certainty. It also found that the obvious implementation response—attach a freshness/admission label to each record—is not justified.

The strongest current formulation remains relational:

```text
historical evidence
+ property / owner / time scope
+ later property-relevant events or observations
+ later owner-authoritative re-observation, if any
→ query-time truth admission
```

not:

```text
evidence.fresh = true|false
→ universal current truth
```

## Primary campaign

Eight cases balanced current-UNKNOWN and concrete answers across `RAW_SCOPED` and `EXPLICIT_TEMPORAL_ADMISSION`, with two predeclared Provider replicates per treatment.

The raw campaign initially reported 14/16 correct for each treatment. That number is retained in the immutable receipt, but it is **not the accepted scientific score** because one counterfactual evaluator exceeded Security's owner semantics.

### Evaluator correction

`ae2-old-truth-plus-new-conflict` assumed that a world-truth record at logical time 10 becomes non-current merely because later, non-world-truth sensors disagree at times 20 and 21. Security has not established such a universal invalidation law. Its accepted evidence says sensor observation is not world truth and explicitly leaves freshness unproved. Computing therefore had no authority to declare `UNKNOWN` the unique owner-domain answer for that case.

The four primary rows for that case remain in the raw receipt as apparatus evidence but are excluded from accepted accuracy. After exclusion:

| Treatment | Correct | Decisions | False certainty |
|---|---:|---:|---:|
| RAW_SCOPED | 13 | 14 | 1 |
| EXPLICIT_TEMPORAL_ADMISSION | 14 | 14 | 0 |

This correction is itself a world-model result: evaluator truth is authority-scoped. An independent evaluator must not be controlled by the candidate, but independence does not grant it authority to invent domain semantics.

## The real A10 failure

The strongest case is `c1n-current-after-unknown-effect`:

```text
state witness @ t10: balance = 1
later relevant effect @ t20: would change 1 → 2 if committed
physical effect outcome: UNKNOWN
query @ t30: current balance ?
```

RAW_SCOPED produced two false-certainty decisions across four decisions from the primary and follow-up campaigns. One particularly revealing primary decision submitted structured `answer=2` while its own rationale explicitly said the effect outcome was unknown and concluded that the correct answer should be unknown. This is both a time-scoped-truth failure and a structured-decision/rationale consistency pressure.

Historical controls behaved correctly: the t10 witness remained valid for the t10 query, a later owner-authoritative t30 truth established the new current value, prior source-history patterns did not prove the current hidden world, and truth about `serviceQuarantined` did not establish `serviceCompromised`.

## Why record-local freshness did not graduate

The first explicit treatment attached query-relative labels to individual records. Across the uncorrected primary campaign it had the same 14/16 score as RAW. More importantly, the label `historical-for-query` was semantically ambiguous: the Agent interpreted it as meaning the old world truth remained authoritative *for* the later query. That apparatus error demonstrates why a single record-local freshness word can compress the wrong relation.

The experiment therefore rejects promotion of that representation.

## Relational follow-up

A smaller follow-up replaced record-local labels with a deterministic `propertyTimeline` index. It names only:

- the prior state-establishing record;
- later records relevant to the same property;
- whether a state-establishing record exists after those later records.

It carries no `fresh`, `stale`, `UNKNOWN`, or independent truth value.

The first follow-up process failed after six saved decisions because one Provider turn did not submit structured completion. Restart replayed those six records and resumed the missing phase rather than replaying the campaign.

After excluding the same owner-undefined AE2 counterfactual:

| Treatment | Correct | Decisions | False certainty |
|---|---:|---:|---:|
| RAW_SCOPED | 7 | 8 | 1 |
| PROPERTY_TIMELINE | 8 | 8 | 0 |

The timeline is therefore a **candidate** for reducing Agent friction over temporal evidence, not an admitted shared primitive. It has only one domain, a small number of decisions, and no demonstrated need for durable persistence or a generic API.

## What A10 now means operationally

The experiment does not justify a universal clock, truth service, freshness score, or evidence TTL. It sharpens how to read the existing Core law:

```text
current-enough
```

is a judgment over the queried property and the owner's evidence history, not a timeless attribute automatically inherited from an old successful verification.

Security's earlier Round 1 observation already exposed the same implementation smell: a stale flag attached once remained stale even after re-verification, and the repair required a new provenance-bearing state transition. That historical result is supporting context, not a new owner oracle for this experiment.

## New method pressure — evaluator authority

This experiment falsified part of its own evaluator. That is not bookkeeping noise.

```text
candidate != evaluator
```

is necessary, but incomplete. We also need:

```text
evaluator independence
!=
domain truth authority
```

A cross-project evaluator can verify a claim only against owner-native laws or an explicitly declared counterfactual oracle whose semantics are part of the experiment. It cannot turn an unresolved owner question into a unique expected answer merely because a benchmark needs a label.

This matters directly to future recursive self-improvement work: evaluation sovereignty requires both independence from the mutable candidate **and** legitimate authority for the world facts being graded.

## Disposition

- **Core A10:** retain; no text revision required.
- **Generic freshness field/service:** reject for now.
- **Property timeline / relational evidence reduction:** keep as experiment-local candidate.
- **Security C1-O:** still belongs to Security and should be physically tested there if its consumer reaches the stale-witness publication gap.
- **World Model Round 002:** not opened by this result alone.
- **Next cross-domain falsifier:** test the relational idea against a different owner such as World Presence or Finance point-in-time state before any shared promotion.
