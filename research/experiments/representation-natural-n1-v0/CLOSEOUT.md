# ANC-REPRESENTATION-001 — second natural workload closeout


> **Post-closeout apparatus archive:** the one-shot Python sources used to build/run/score this closed experiment are preserved byte-for-byte as `*.py.txt`, not active executables. `closed-representation-apparatus-archive.json` maps each original execution path to its archived path and SHA-256.

Status: **COMPLETED NEGATIVE NATURAL FALSIFIER / MIXED_N1_NOT_REPRODUCED**, 2026-08-25.

## Question

The precommitted question was whether, on one materially different natural Computing research-audit workload, the smallest source-bound operation-relative `Claim | Evidence | Challenge | Boundary` projection could reduce context while preserving or improving protected source-robust judgments relative to exact full source.

This is the first natural workload required by `ANC-REPRESENTATION-001` after the earlier six-artifact Book representation programme. It is not another synthetic balancing benchmark.

## Frozen source cut

Computing source cut: `9cbbc217cc99c01acde42ef9fb0452000a416577`.

Six pre-run selected artifacts:

- F15 — current-world non-identifiable Finance × Workstation complementarity candidate;
- F16 — current-world non-identifiable endogenous-regulation candidate;
- F17 — open prospective pressure-certificate field study with bounded specificity signal and no true-positive/downstream decision change;
- F18 — one natural support-bound prior revalidation;
- F19 — one real invariant-bound Harness migration;
- ACS9 — implemented owner consumption surfaces with post-implementation fresh-Agent benefit.

Exact source digests, packet digests, oracle, task definitions and contract are frozen in `source-manifest.json`, `oracle.json`, `task-prompt.txt`, `contract.json` and `execution-freeze.json`.

## Treatments

### FULL_SOURCE

Exact frozen bytes of all six owner/Computing sources.

Payload: **37,065 bytes**.

### SOURCE_BOUND_CECB

One source-bound operation-relative projection preserving only the selected artifact's Claim, decisive Evidence, live Challenge and scope/authority Boundary. It added no Book, G/R/A vocabulary, oracle labels, new evidence, Tool surface, owner authority or action affordance.

Payload: **7,310 bytes**.

Payload reduction: **80.3%**.

## Provider / carrier

Six one-turn no-Tool structured calls were run with the production `DeepSeekTurnAdapter` from exact detached Harness revision `684333be5146d4f705a91edb396e83c6a1150e1f`.

All six calls returned schema-valid results with:

- requested/effective model: `deepseek-v4-flash`;
- provider request mode: `non-thinking`;
- system fingerprint: `a26a7955944dc5c60445bff77fac9c8e`;
- external Tools: zero;
- prior-run message carryover: zero.

Harness is an experimental carrier only. No Harness causal capability claim follows from these calls.

## Frozen primary gate

The candidate had to satisfy a Pareto-style gate rather than a scalar token↔accuracy exchange rate:

1. candidate payload and reported prompt tokens are strictly lower;
2. aggregate correctness is non-regressing **separately for every protected relation family**;
3. false broader promotion does not increase;
4. at least one protected judgment family or context dimension improves strictly.

Any protected-family regression means `MIXED / N1 NOT_REPRODUCED`, regardless of context savings.

## Primary result

| Metric | FULL_SOURCE | SOURCE_BOUND_CECB |
|---|---:|---:|
| total relation judgments | **79/90** | **75/90** |
| exact artifact judgments | **9/18** | **5/18** |
| mean prompt tokens | **10,952** | **3,546** |
| mean total tokens | **11,827.3** | **4,071** |
| payload bytes | **37,065** | **7,310** |
| false broader promotions | **0** | **0** |

Prompt-token reduction: **67.6%**. Mean total-token reduction: **65.6%**.

### Protected family totals (18 judgments per family)

| Relation | FULL_SOURCE | SOURCE_BOUND_CECB | Candidate non-regression? |
|---|---:|---:|---|
| ObjectiveAchievement | **16** | **15** | no |
| BoundedImprovement | **12** | **9** | no |
| CurrentConsumption | **18** | **17** | no |
| RealizedBenefit | 15 | **16** | yes / strict gain |
| BroaderPromotion | **18** | **18** | yes |

Therefore:

```text
protectedFamilyNonRegression = false
falsePromotionNonRegression  = true
contextStrictReduction       = true
strictJudgmentGain           = true

PRIMARY VERDICT = MIXED_N1_NOT_REPRODUCED
```

The large context saving cannot compensate for regressions in protected judgments under the pre-run contract.

## Error morphology

The result is not a simple `compression bad` pattern.

Shared difficulties existed under both treatments:

- F15 bounded speed improvement was conservatively missed in all three FULL and all three CECB runs;
- F17's bounded specificity improvement was missed in all three FULL and all three CECB runs;
- ACS9 realized downstream benefit was missed in all three FULL runs and two of three CECB runs.

The treatment-specific losses were more important for the causal comparison:

- CECB missed F19 `BoundedImprovement` in **3/3** runs while FULL recovered it in **3/3**;
- CECB missed F16 negative `ObjectiveAchievement` in **2/3** runs while FULL recovered it in **3/3**;
- CECB missed ACS9 `CurrentConsumption` in **1/3** runs while FULL recovered it in **3/3**.

CECB also improved some boundaries:

- it recovered ACS9 `RealizedBenefit` once where FULL never did;
- it made the still-open F17 `ObjectiveAchievement` correct in two of three runs versus one of three FULL runs;
- both treatments preserved all explicit broader no-go boundaries (18/18, zero false promotion).

This is exactly the expected trade-off shape for a representation intervention: it changes which relations become salient/recoverable. It does **not** establish monotonic capability gain.

## Evaluator apparatus incident

The frozen `score.py` contained a mechanical `NameError` in a convenience `exactArtifactJudgmentsOutOf18` expression. The failure occurred only after all six Provider outputs were complete and before the primary aggregate/Pareto block executed. No Provider call was rerun and no oracle/treatment/task bytes changed.

The failed scorer and Runtime failure receipt are retained. `score_repair_v1.py` changes only that broken convenience expression; the exact-artifact count is still recomputed later from frozen runs as originally intended. The repaired scorer produced `score.json`.

A second, independently written mechanical calculation reproduced exactly:

- FULL family totals `16/12/18/15/18`, total 79;
- CECB family totals `15/9/17/16/18`, total 75;
- the same Pareto booleans;
- the same `MIXED_N1_NOT_REPRODUCED` verdict.

Thus the evaluator implementation incident does not change the experiment's semantic rule or result.

## Post-primary sensitivity (non-promotional)

`sensitivity.json` tests whether the primary negative depends only on the most arguable oracle cells.

1. Dropping both F15 and F17 `BoundedImprovement` cells still leaves CECB regressing on ObjectiveAchievement, BoundedImprovement and CurrentConsumption.
2. Also dropping F16 negative `ObjectiveAchievement` makes CECB better on the remaining objective cells, but it still regresses on BoundedImprovement and CurrentConsumption.

These are post-primary diagnostics only; they do not rewrite the frozen oracle. They show the closure is not solely an artifact of those disputed cells.

## Scientific disposition

The following narrow candidate is falsified on its predeclared second natural workload:

> a generic operation-relative CECB projection over heterogeneous Computing research artifacts can be retained as a reusable representation candidate because its context reduction does not regress protected source-robust judgments.

That candidate **did not reproduce**.

This does not falsify:

- representation-dependent cognition in general;
- the external-cognition / cognitive-fit / search-geometry literature;
- ACS9's owner-local, consumer-earned surface projections;
- operation-specific representations earned by a concrete consumer;
- Media as observer-relative structured mediation;
- SCD semantic-preservation questions;
- Harness bounded Run mediation.

What fails is the attempt to retain this cross-artifact representation candidate after its required natural replication.

## Deletion-positive consequence

The pre-run `ANC-REPRESENTATION-001` deletion rule is now consumed:

- close `ANC-REPRESENTATION-001`;
- move it to portfolio `completed / reference` standing;
- retain the 2026-08-25 Book and N1 experiment bytes as historical evidence;
- remove the Book Result/Value and Book Representation executable verifier scripts from the active research tree;
- do not build a Representation service, global CECB schema, ontology/card registry, new Harness layer or Book Chapter 6 to preserve the candidate.

The owner-local ACS design law survives independently:

> eliminate repeated mechanical reconstruction only where a concrete consumer earns the projection; preserve semantic choice and exact owner truth.

## COJC consequence

This experiment is **not** a Media × SCD × Harness joint-capability proof:

- Media-specific deletion-essential value was not isolated from generic task-fit representation;
- SCD did not contribute a deletion-essential inferential discriminant to the treatment;
- Harness only carried the calls.

Therefore the earlier standing remains:

```text
Media × SCD × Harness JOINT_EXPLANATION          = strong
Media × SCD × Harness JOINT_OPERATIONAL_COMPOSITION = strong
Media × SCD × Harness JOINT_CAPABILITY           = NOT ESTABLISHED
```

The branch returns to dormant natural-pressure mode rather than opening a third representation benchmark.
