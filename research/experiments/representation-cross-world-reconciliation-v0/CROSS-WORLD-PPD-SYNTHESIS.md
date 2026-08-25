# Representation Cross-World Reconciliation — Full PPD Synthesis v0

Status: **historical-evidence reconciliation / generic candidate remains closed / conditional moderator retained**, 2026-08-25.

This document reconciles two independently frozen natural Representation experiments that reached opposite local outcomes on the same day. It does **not** reopen `ANC-REPRESENTATION-001`, create a new Representation programme, or overwrite the canonical negative natural falsifier.

## 1. Currentness and independence

Canonical `ordivon-computing` currently contains commit `607d7de` (`research: close representation natural falsifier`) and its follow-up `e220468` archive contraction. The canonical N1 experiment used source cut `9cbbc217cc99c01acde42ef9fb0452000a416577` and returned `MIXED_N1_NOT_REPRODUCED`.

A parallel detached COJC lineage independently froze a different natural workload in commit `bab0395` at 2026-08-25 16:22 +08:00, before canonical `607d7de` was committed at 16:25 +08:00. Its semantic packet, projection, oracle, eligibility and primary scoring remained byte-identical through later carrier-only repairs. The final positive closeout is detached commit `5021e8f` at 16:44 +08:00.

The positive lineage is archived under `positive-lineage/` as non-executable historical evidence. Exact semantic SHA-256 values are retained. Its existence therefore does not depend on a temporary detached workspace remaining open.

This timing matters: the positive treatment semantics were frozen before the canonical negative result existed. The later v1/v2 work changed only experiment carrier/reliability handling, not source packet, projection, oracle, task or primary thresholds.

## 2. PPD — Problem reformulation

The question is no longer:

> Does operation-relative representation work?

Two natural workloads show that this question is too coarse.

The corrected problem is:

> **Which pre-treatment workload properties determine whether a source-bound projection removes more finite-consumer search/join burden than semantic/detail fidelity it destroys?**

Equivalent form:

```text
Representation useful here
!= Representation useful elsewhere
```

and:

```text
same broad CECB family
+ different support topology / judgement granularity
-> different outcome sign and failure morphology
```

The object of study is therefore a **conditional fit relation**, not a reusable Representation object.

## 3. Pressure

Any future theory must jointly survive these pressures:

- finite context/search/attention budgets;
- source truth and projection truth must remain distinct;
- exact facts may be present yet computationally hard for the consumer to join;
- compression may delete locally decisive distinctions;
- top-level claim polarity can differ from a scoped subclaim such as a bounded improvement;
- context length can hurt even when retrieval is nominally available;
- projection construction, refresh and recovery cost is real debt;
- owner-local earned surfaces may dominate a generic cross-artifact compiler;
- a compact representation can improve one relation family while regressing another;
- no amount of context saving compensates for violating a protected semantic family when that family is decision-critical;
- a successful local projection must not be promoted into shared infrastructure without a second distinct consumer and deletion-positive need.

## 4. External subtraction

The heterogeneity is not surprising relative to mature external work.

### Cognitive fit

Vessey (1991) argues that performance depends on a fit between task, representation and the problem-solving processes the representation supports. Same information does not imply same effective problem-solving performance.

### Computational advantage of representation

Larkin & Simon (1987) argue that diagrams can be computationally superior because indexing/grouping makes useful operations cheaper, not because the representation contains more information. They also stress that the solver must possess or discover the process that exploits the representation.

### Long-context finite-consumer limits

Liu et al. (TACL 2024, *Lost in the Middle*) show that long-context models do not robustly use all information present in context; position affects access. Du et al. (2025, *Context Length Alone Hurts LLM Performance Despite Perfect Retrieval*) further report degradation from sheer context length even when relevant information is perfectly retrievable.

These are mature reasons to reject:

`InformationPresent -> InformationEffectivelyUsable`.

### Compression and retrieval are task-dependent

A 2025 empirical prompt-compression study reports that compression effects vary by dataset/context regime and that moderate compression can sometimes improve long-context performance while more aggressive or poorly targeted compression loses information.

Han et al. (2025) systematically compare RAG and GraphRAG and find distinct strengths by task/evaluation perspective rather than a universal structured-retrieval winner. Gong et al. (2025) similarly report strong graph-free triplet retrieval against more complex graph/multi-round pipelines on their evaluated datasets.

### Strong simple baseline requirement

Laitenberger, Manning & Liu (EMNLP 2025) show that a simple DOS-RAG baseline preserving source fidelity and document structure can match or outperform more complicated multi-stage methods under controlled token budgets. This directly supports Ordivon's requirement that representation machinery beat exact/full or owner-local strong baselines rather than weak raw-search controls.

External subtraction therefore does not create a new theory. It makes the correct Ordivon contribution narrower: **source-fenced natural workload evidence about when task-relative projection helps or harms this finite Agent system.**

## 5. Two natural worlds

### World P — positive COJC relational-lineage audit

Scored families:

`J1 / J2 / W2 / ACT / D1 / D2 / D2A / FINREP`.

Pre-run geometry:

- 8 scored families;
- 11 frozen source files;
- every scored item points to multiple source files;
- source refs per item = `[3,3,2,2,3,3,4,3]`, mean `2.875`;
- all 8 `downstreamUse` oracle relations are positive and require later-consumer/programme lineage evidence;
- full frozen source bytes = `115686` before task/control wrapper;
- exact full-source Provider prompt = `28236` tokens per valid semantic slot;
- operation projection Provider prompt = `7253` tokens.

Primary result:

```text
FULL_SOURCE           93 / 120 = 77.5%
OPERATION_PROJECTION 111 / 120 = 92.5%
paired wins                 = 3 / 3
prompt-token reduction      = 74.31%
false broader promotion     = 0 vs 0
```

The dominant relation-level change is:

```text
downstreamUse
FULL 13/24
PROJ 24/24
```

Objective closure and broader-promotion boundaries are already `24/24` under both arms.

Interpretation: the projection mainly removes **cross-artifact relation-join burden**. The relevant facts existed in full source, but the finite consumer did not reliably reconnect later programme/synthesis consumption evidence to the earlier result family.

### World N — canonical PAL/ACS natural N1

Scored artifacts:

`F15 / F16 / F17 / F18 / F19 / ACS9`.

Pre-run geometry:

- 6 scored artifacts;
- 6 primary source files;
- one primary owner/source artifact per scored item;
- only `1/6` `CurrentConsumption` relations are positive;
- only `1/6` `RealizedBenefit` relations are positive;
- most protected positive burden lies in artifact-local `ObjectiveAchievement` and `BoundedImprovement` distinctions;
- full payload = `37065` bytes;
- CECB payload = `7310` bytes;
- full Provider prompt = `10952` tokens;
- CECB Provider prompt = `3546` tokens.

Primary result:

```text
FULL_SOURCE       79 / 90
SOURCE_BOUND_CECB 75 / 90
prompt-token reduction = 67.6%
false broader promotion = 0 vs 0
```

Protected-family regressions:

```text
ObjectiveAchievement 16 -> 15
BoundedImprovement   12 ->  9
CurrentConsumption   18 -> 17
RealizedBenefit      15 -> 16
BroaderPromotion     18 -> 18
```

Under its preregistered Pareto non-regression rule this is correctly `MIXED_N1_NOT_REPRODUCED`.

Interpretation: the source is already relatively local to the judgement object. Projection therefore acts more like **lossy local summarization** than like a materialized cross-source join. The saved search cost is smaller, while lost scope/detail can directly damage protected local judgments.

## 6. What the sign reversal already falsifies

The two worlds reject several tempting laws.

### Compression ratio is not the law

Both treatments compress heavily:

- positive workload prompt reduction: `74.31%`;
- negative workload prompt reduction: `67.6%`.

Yet the judgement outcome changes sign.

Therefore:

`MoreCompression != MoreCapability`.

### CECB form alone is not the law

Both treatments use source-bound Claim/Evidence/Challenge/Boundary-style representations. One succeeds strongly and one fails protected non-regression.

Therefore:

`CECBPresent != ProjectionBeneficial`.

### Full source is not universally safest for finite consumers

World P shows that exact source completeness can coexist with worse source-robust judgement because relation access itself is computational work.

Therefore:

`SourceComplete != ConsumerComplete`.

### Projection is not universally safer/cheaper

World N shows that compact task-fit prose can erase or blur a local distinction that the full source preserves.

Therefore:

`TaskRelevantSummary != SufficientStatistic`.

## 7. Candidate moderator map

The strongest current candidate is a competition between **support-dispersion burden** and **local-distinction fidelity**.

### M1 — Cross-source join demand

Question:

> How much of the target judgement requires joining evidence distributed across independently authored/current artifacts?

Pre-run observable candidates:

- authoritative sources required per scored item/relation;
- fraction of positive target relations whose support crosses source boundaries;
- lineage/path depth between result and named consumer/consequence;
- whether exact source requires manual Agent reconstruction of later-use relations.

Current evidence:

- World P: every item multi-source; mean `2.875` source refs; downstream relation recovery is the largest gain;
- World N: one primary source per item; almost all consumption relations are negative and already easy for full source.

Hypothesis:

`higher join demand -> larger potential benefit from operation-relative materialized relation projection`.

### M2 — Local distinction / scope density

Question:

> Does correct judgement depend on distinctions nested inside one source that a compact top-level representation can flatten?

Examples:

- global negative/non-admission standing while one bounded local improvement is still established;
- open experiment status while one specificity/efficiency signal is positive;
- implementation migration with several invariants/countermodels whose exact comparison matters.

World N regressions cluster in `BoundedImprovement` and one negative/objective-currentness boundary. This is consistent with local scope fidelity becoming load-bearing.

Hypothesis:

`higher local scope density -> larger risk from lossy projection unless the projection explicitly preserves the exact scoped discriminant`.

### M3 — Full-context load

World P full prompt (`28236`) is about 2.58× World N (`10952`). External long-context evidence makes context load a plausible amplifier.

But length is confounded with source topology here. It cannot yet be credited as the primary moderator.

Hypothesis:

`context load amplifies existing search/join burden but does not by itself determine treatment sign`.

### M4 — Projection fidelity to the scored relation

A representation can be compact but still omit the target distinction.

The old Book natural audit already showed evidence-only cards could lose declared target/claim for negative objective closure. The later positive COJC projection explicitly preserved target + targetClaim + sourceRefs + evidence + challenge + boundary, and achieved `24/24` objective closure. The canonical negative N1 preserved Claim/Evidence/Challenge/Boundary but still regressed on some local bounded distinctions.

Hypothesis:

`projection benefit requires not merely relevance but judgement-specific semantic sufficiency`.

### M5 — Consumer/operator fit

D2A already demonstrates:

`feasible procedure exists != finite consumer discovers it`.

Larkin/Simon and cognitive-fit work predict the same general shape externally. A projection may expose an efficient operation but fail if the current consumer does not discover or execute it.

No new shared operator is admitted from these two natural audits.

### M6 — Construction/currentness/recovery debt

Both natural experiments measured recurring prompt/context cost but not a mature production compiler's authoring, refresh, stale-view and recovery cost.

Therefore even a local positive does not establish net positive environmentalization.

## 8. Compact conditional model

Current working model:

```text
ExpectedProjectionValue(W, O, A)
    ~= Join/Search Burden Removed
       + Effective-Context Burden Removed
       + Useful Operator Salience
       - Lost Local Distinctions
       - Scope/Polarity Flattening
       - Construction Cost
       - Currentness/Recovery Debt
```

This is **not** a validated scalar score. It is a moderator decomposition used to generate falsifiable predictions.

The intended scientific move is to predict the sign before a future natural experiment, not fit coefficients retrospectively to these two worlds.

## 9. Strong nulls and external baselines

For future natural cases, retain these nulls:

1. **Exact full source / original structure** — source-fidelity baseline.
2. **Owner-local earned projection** — if an owner already exposes the relation cheaply, a cross-artifact compiler is redundant.
3. **Simple retrieval / source selection** — before adding ontology, graph or multi-stage machinery.
4. **No representation change** — if the real bottleneck is authority, observation, missing Reality information or Tool/action exposure.
5. **Mature external mechanism** — RAG/search/indexing/query plans may solve the burden without a new Ordivon layer.

This follows the same subtraction discipline as DOS-RAG style strong-baseline work: complexity is admitted only after simpler source-faithful alternatives fail.

## 10. Prospective reopen gate

`ANC-REPRESENTATION-001` remains completed/reference.

Do **not** reopen for another generic CECB formatting benchmark.

A future natural consumer may justify a new local experiment only if all of the following are frozen before treatment execution:

1. a materially different consumer/operation exists for owner-native reasons;
2. the exact source/currentness cut is known;
3. the target relation and consequence are named;
4. a **pre-treatment support-geometry prediction** is recorded;
5. at least one strong null/full-source/owner-local baseline exists;
6. projection construction/currentness cost is charged or explicitly bounded;
7. a contrary result would actually revise the moderator hypothesis.

Minimum predictive contrast:

```text
Regime J:
    high cross-source join demand
    + low/moderate local-detail dependency
    -> predict source-bound relation projection may help

Regime L:
    low cross-source join demand
    + high local scoped-detail dependency
    -> predict full source / owner-local projection should match or win
```

A natural result contrary to a frozen Regime J/L prediction is more scientifically valuable than another positive formatting result.

## 11. COJC implication

The positive detached workload came from COJC research, but it does not restore a COJC Representation candidate.

No deletion-essential owner coalition was isolated:

- source owners supplied truth;
- Computing compiled the research treatment;
- Harness carried zero-Tool Provider calls;
- no Media-specific or SCD-specific deletion-positive contribution was isolated;
- no new World/CP primitive is required.

Therefore:

```text
Representation workload heterogeneity = ESTABLISHED in two natural worlds
Generic reusable cross-artifact CECB = NOT REPRODUCED
Owner-local / operation-local projection value = CONDITIONAL
Shared Representation service/schema = NOT AUTHORIZED
Media × SCD × Harness JOINT_CAPABILITY = NOT ESTABLISHED
COJC emergence / phase transition = NOT ESTABLISHED
```

COJC should continue candidate selection outside this closed generic representation route.

## 12. Current standing

The strongest current statement is:

> **A source-bound projection is valuable when the operation requires a finite consumer to reconstruct relations whose support is dispersed across sources and the projection preserves the judgement-specific distinctions needed for commitment. The same style of projection can be harmful when the operation is already source-local and compacting the source removes scoped distinctions. Context length amplifies the pressure but does not determine the sign.**

Equivalent compression:

```text
Projection value
= task/consumer/support-topology conditional
```

not:

```text
Projection value
= intrinsic property of the projection format
```

This standing is sufficient to retain the two worlds as heterogeneous natural evidence and keep shared Representation infrastructure closed.

## 13. References used for external subtraction

- Iris Vessey (1991), *Cognitive Fit: A Theory-Based Analysis of the Graphs Versus Tables Literature*, Decision Sciences 22(2), 219–240.
- Iris Vessey & Dennis Galletta (1991), *Cognitive Fit: An Empirical Study of Information Acquisition*, Information Systems Research 2(1), 63–84.
- Jill H. Larkin & Herbert A. Simon (1987), *Why a Diagram Is (Sometimes) Worth Ten Thousand Words*, Cognitive Science 11, 65–99.
- Nelson F. Liu et al. (2024), *Lost in the Middle: How Language Models Use Long Contexts*, TACL 12, 157–173.
- Alex Laitenberger, Christopher D. Manning & Nelson F. Liu (2025), *Stronger Baselines for Retrieval-Augmented Generation with Long-Context Language Models*, EMNLP 2025.
- Haoyu Han et al. (2025), *RAG vs. GraphRAG: A Systematic Evaluation and Key Insights*.
- Zheng Zhang et al. (2025), *An Empirical Study on Prompt Compression for Large Language Models*.
- Yufeng Du et al. (2025), *Context Length Alone Hurts LLM Performance Despite Perfect Retrieval*.
- Shengbo Gong et al. (2025), *Beyond Chunks and Graphs: Retrieval-Augmented Generation through Triplet-Driven Thinking*.
