# EX2-B diagnosis — relations survive, promotion taxonomy contracts

EX2-B replaced the rejected fixed five-axis row with question-relative typed relations and a new 24-case / 52-query held-out set.

Results across six paired fresh-Agent replicates:

| representation | query exact | case exact | owner/carrier | critical native fact | minimality |
|---|---:|---:|---:|---:|---:|
| compact responsibility | 278/312 = 89.10% | 110/144 = 76.39% | 100% | 100% | 47.22% |
| typed relations | 290/312 = 92.95% | 122/144 = 84.72% | 100% | 94.44% | 63.89% |

The preregistered result remains `REJECT_OR_REVISE`: typed relations improved most semantic-boundary questions but did not reach the safety threshold.

## What clearly survived

Typed relations eliminated most of the category errors exposed by EX2-A:

- `DECIDES_SEMANTICS`: 72.2% → 100%;
- `VERIFIES_ACCEPTANCE`: 70.8% → 95.8%;
- `PERSISTS_VIA`: 100%;
- `PROVES_LOCAL_EXECUTION`: 100%;
- `MAPS_OR_DERIVES`: 100%;
- `RECONCILES_IDENTITY`: 100%;
- `TIME_COORDINATE`: 100%;
- `DELEGATES_MECHANICS_TO`: 100%;
- owner-vs-carrier cases: 100%.

The largest gain therefore came from **asking only the relation that is actually uncertain**, not from making the explanation longer.

## Remaining representation defect: promotion status

`PROMOTION_STATUS` was still an overloaded enum. `KEEP_LOCAL`, `NOT_PROMOTED`, and `DELEGATE_CLASSICAL` are not peer alternatives:

- semantic home may be local;
- mechanics may be delegated to classical substrate;
- the same responsibility may simultaneously be not promoted into a new shared Ordivon layer.

This recreated the exact overlap already exposed in EX1. EX2-C removes the redundant enum and asks one independent question only:

`SHARED_PROMOTION(responsibility) -> PROMOTED_SHARED | NOT_PROMOTED_SHARED`.

Semantic home and mechanical delegation remain separate relations.

## Remaining subject ambiguity

R16 asked who owned “attempt record semantics” while the scenario also discussed scientific interpretation. Some answers selected the researcher/Agent rather than the Finance Trial Ledger contract. The relation itself is useful, but its **subject must be named exactly**. Likewise destination-native admission must name the destination domain fact rather than the broader delivered-message trajectory.

EX2-C therefore requires every relation query to name its exact subject in the scenario/query id and uses a third held-out set. No EX2-B scenario is reused verbatim.
