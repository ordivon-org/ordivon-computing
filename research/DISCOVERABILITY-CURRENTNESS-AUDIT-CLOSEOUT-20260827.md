# Discoverability / Currentness Audit Closeout — 2026-08-27

Status: **bounded cross-owner research-capability closeout**. This document summarizes a preregistered 15-owner retrieval/currentness pressure test. It is not Atlas owner truth, not a global search architecture, and not evidence that all Ordivon research has equal retrieval importance.

## 1. Question

Can a finite successor Agent begin from a problem expression, without already knowing the historical owner/repository/canonical vocabulary, recover an already-established research standing, distinguish history from present standing, and lawfully re-enter current owner-native authority without re-researching the problem?

The tested capability is therefore larger than search:

```text
problem expression
→ query representation
→ bounded candidate formation
→ query-relative inspection
→ semantic discrimination
→ owner/successor resolution
→ currentness re-entry
→ authority escape
```

## 2. Frozen target universe and apparatus

- 15 current semantic/research owners were sampled; one current-source-supported target was frozen per owner before Atlas retrieval.
- Three initial query conditions were frozen: owner-known lexical-rich QK, owner-unknown English QU-E, owner-unknown Chinese QU-ZH.
- Atlas committed main was tested with curated synthesis alone and with the exact existing generated projection snapshot.
- Retrieval used Atlas first-look / first-look-many and then official bounded inspect-candidate; semantic recall was not inferred from a non-empty result list.
- Model evaluators were bounded judgment instruments only. Owner-native source anchors remained the truth oracle, and evaluator self-contradictions were explicitly normalized rather than promoted.

## 3. Final recall after evaluator-consistency repair

| Condition | synthesis only | synthesis + existing generated |
|---|---:|---:|
| owner-known QK | **6/15** | **9/15** |
| owner-unknown English raw | **2/15** | **2/15** |
| owner-unknown Chinese raw | **0/15** | **0/15** |

Existing generated projections improve owner-known exact recovery, but did not improve owner-unknown raw English/Chinese recall in this sample.

```text
OwnerProjection != OwnerUnknownDiscoveryRepresentation
```

## 4. Query-authoring and raw-preserving ablations

| Owner-unknown view | English | Chinese | worst top-k candidate budget |
|---|---:|---:|---:|
| T0 raw | 2/15 | 0/15 | 8 |
| T1 authored variants only | **4/15** | **4/15** | 8 |
| T2 raw + authored variants merged | 3/15 | 3/15 | 8 |
| representation-portfolio union, all three lanes | **6/15** | **4/15** | up to 24 |

T1 demonstrates that query formation/translation is a real capability variable, especially for Chinese. T2 falsifies the simple repair that preserving the raw query inside one merged top-k ranking makes query expansion monotone. Different query representations expose different target-bearing candidate/section geometries.

```text
MoreQueryVariants != MoreRecall@k
CandidateIdentitySame != InspectionRepresentationSame
RepresentationPortfolio != OneMergedRepresentation
```

The English three-lane union reaches 6 owners although the best single lane reaches 4. This is a real representation-portfolio effect, but it costs additional finite attention and does not justify permanent multi-pass search by default.

## 5. Owner-level reachability map

| Owner | QK | T0 EN | T1 EN | T2 EN | T1 ZH | T2 ZH | classification |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| computing | — | — | ✓ | ✓ | ✓ | ✓ | `ALTERNATIVE_REPRESENTATION_ONLY` |
| runtime | ✓ | — | — | — | — | — | `OWNER_KNOWN_ONLY` |
| host | ✓ | — | ✓ | — | ✓ | ✓ | `REPRESENTATION_SENSITIVE` |
| harness | ✓ | — | ✓ | — | ✓ | — | `REPRESENTATION_SENSITIVE` |
| world | — | — | — | — | — | — | `UNREACHED_UNDER_FROZEN_VIEWS` |
| game | — | — | — | — | — | — | `UNREACHED_UNDER_FROZEN_VIEWS` |
| security | — | — | — | — | — | — | `UNREACHED_UNDER_FROZEN_VIEWS` |
| finance | — | — | — | ✓ | — | — | `ALTERNATIVE_REPRESENTATION_ONLY` |
| human | ✓ | — | — | — | — | — | `OWNER_KNOWN_ONLY` |
| media | ✓ | — | — | — | — | — | `OWNER_KNOWN_ONLY` |
| web | — | — | — | — | — | — | `UNREACHED_UNDER_FROZEN_VIEWS` |
| scd | ✓ | — | — | — | — | — | `OWNER_KNOWN_ONLY` |
| computational-possibility | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | `MULTI_REPRESENTATION_REACHABLE` |
| interlocus | ✓ | ✓ | — | — | — | — | `REPRESENTATION_SENSITIVE` |
| normative | ✓ | — | — | — | — | — | `OWNER_KNOWN_ONLY` |

Across every frozen query representation, **11/15** target standings were recovered at least once. The four not recovered under any frozen view were: **game, security, web, world**.

This is evidence of a residual coverage/representation ceiling, not proof that those owners are intrinsically undiscoverable. In particular, configured-owner membership was not sufficient: Game and World were configured yet their sampled current targets remained unrecovered; conversely Computing and Finance were not configured Atlas owner sources yet some target semantics were reachable through curated cross-owner synthesis.

```text
ConfiguredOwner != CurrentTargetCoverage
CorpusPresence != QueryReachability
InformationPresent != ComputationallyReachableForThisQuery
```

## 6. Currentness and successor controls

| Control | existing generated + synthesis | interpretation |
|---|---|---|
| C1 Network→Interlocus | `MIXED_REQUIRES_REENTRY` | semantic successor/stable owner identity recovered; fresh currentness still requires owner re-entry |
| C2 Normative physical migration | `NOT_RECOVERED` | generic migration concepts do not recover the specific current standalone cutover |
| C3 Post-Host PHR lineage | `MIXED_REQUIRES_REENTRY` | generated projection recovers PHR1→Normative and PHR2–4 sibling history; stale fence prevents currentness proof |
| C4 Workstation rehome | `HISTORICAL_ONLY` | historical Workstation material is dense; current no-standalone-owner/public-MCP-retired rehome is absent |
| C5 GoalCoordinatorHost removal | `NOT_RECOVERED` | neither the historical mechanism nor its current removal/contraction is adequately recovered |

No tested successor control earns `CURRENT_RESOLVED` from Atlas alone. A semantically correct successor description plus an owner-native escape route is still only a recovery candidate until present owner currentness is actually re-entered.

```text
HistoricalValidity != Currentness
SemanticSuccessorRecovered != CurrentnessProved
ProjectionHealthAt(t0) != ProjectionCurrentAt(t1)
```

## 7. Mechanical currentness evidence

The existing generated projection snapshot labels all 10 configured owners `CURRENT_TO_SOURCE`, yet exact revision comparison found **0/10** snapshot source fences equal to the present committed owner mains; all **10** differed.

A fresh committed-Atlas `check → refresh` attempt then timed out after **120,075 ms** without establishing semantic completion. This does not prove refresh is generally unusable, but it shows that fresh currentness re-entry was not an ordinary cheap path in this bounded trial.

## 8. Revised capability decomposition

The evidence supports separating discoverability/currentness into at least these operation-relative relations:

```text
D(W,t) = Qf ∘ Rc ∘ Iq ∘ Sd ∘ Or ∘ Kr ∘ Ae

Qf = query formation / translation
Rc = corpus + candidate formation
Iq = query-relative inspection representation
Sd = semantic discrimination
Or = owner / successor resolution
Kr = currentness re-entry
Ae = authority escape
```

None of these terms is a mandatory global service. They are an audit decomposition of the capability path.

## 9. Current standing

| Capability | Standing |
|---|---|
| owner-known prior-result recovery | **REAL_BUT_COVERAGE_BOUNDED** |
| owner-unknown research re-entry | **PARTIAL_REPRESENTATION_SENSITIVE** |
| cross-language query formation | **DEMONSTRATED_NOT_SUFFICIENT** |
| multi-representation portfolio | **REAL_NON_MONOTONE_TRADEOFF** |
| semantic successor recovery | **REAL_SPARSE_REQUIRES_CURRENTNESS_REENTRY** |
| negative-history current re-entry | **WEAK** |
| fresh currentness revalidation | **SEMANTICALLY_SOUND_OPERATIONALLY_FRAGILE_IN_THIS_TRIAL** |
| whole-Ordivon discoverability | **NOT_ESTABLISHED** |

A compact ordering of the present capability is:

```text
Preservation
  > owner-known recovery
  > owner-unknown semantic re-entry
  > successor/currentness re-entry
```

## 10. Minimal repair direction

The current evidence does **not** justify immediately introducing vector search, an LLM query router, a global owner registry, a universal Research Search service, or automatic successor/currentness authority. The smallest next repairs are responsibility-specific:

1. **Coverage before mechanism** — for target families unreached under every frozen view, determine whether an operation-relevant current representation should exist at all; do not add owners merely for symmetry.
2. **Representation portfolios without forced merge** — where multiple views are justified, preserve native/raw query and derived views as independent bounded lanes or fallbacks rather than assuming one globally scored merge is monotone.
3. **Inspection is part of retrieval** — test query-relative section projection separately from candidate ranking; a correct file can be selected while the useful section remains computationally unreachable.
4. **Successor/currentness re-entry** — current use of historical/synthesis/generated material should end in an explicit owner-native revalidation step when the retained source fence is not proven current.
5. **Evaluator challenge remains mandatory** — structured model judgments are inspectable evidence, not epistemic oracle; contradictions between label, reason, candidate content and source anchor must fail closed.

## 11. Non-admissions

- no vector/embedding search architecture admitted;
- no permanent LLM query router admitted;
- no global owner/relevance registry admitted;
- no universal Research Search service/daemon admitted;
- no automatic successor/currentness oracle admitted;
- no requirement to add all current owners to Atlas `sources.json` merely for symmetry;
- no claim that multi-pass representation portfolios are worth their attention/latency cost for ordinary use yet.

## 12. Durable evidence

- `research/experiments/discoverability-currentness-v0/prefrozen-targets-v2.json`
- `research/experiments/discoverability-currentness-v0/inspection-semantic-evaluations-normalized-v2.json`
- `research/experiments/discoverability-currentness-v0/authored-query-semantic-evaluations-v2.json`
- `research/experiments/discoverability-currentness-v0/raw-preserving-query-semantic-evaluations-normalized-v2.json`
- `research/experiments/discoverability-currentness-v0/discoverability-currentness-capability-map-v1.json`

Successor/currentness controls were first run in a sibling isolated audit workspace and then consolidated into this experiment directory. Durable local evidence includes `successor-negative-history-contract.md`, `successor-negative-history-raw-controls-v1.json`, `successor-negative-history-evaluations-normalized-v3.json`, `existing-projection-drift-v1.json`, and `atlas-refresh-attempt-v1.json`.

## 13. Positive capability statement

> Ordivon already possesses real bounded research-recovery components: curated synthesis, owner projections, query-authorable retrieval, query-relative inspection, semantic discrimination, owner-native escape and explicit currentness semantics. The residual challenge is to compose them so a finite successor can re-enter prior research from its own problem representation without already knowing where the answer lives, while preserving history/currentness/authority boundaries.
