# P10–P11: Effect Phase and Order Stability

## Verdict

P10 supports a narrower and stronger consequence law: **applicability is a pre-admission question; exact admitted Effect identity owns recovery after admission**. P11 rejects active order-canonicalization infrastructure: once the semantic oracle was made unambiguous, raw presentation order was already 44/48 strict and neither stable ordering nor an identity map improved it. The round promotes no new long-lived code.

## P10 — Finance ambiguous external Effect

Finance C2 v3 already supplies the physical substrate: signed EffectAdmission, deterministic `clOrdId`, exact package replay, one dispatch permission, ambiguous delivery, and read-only reconciliation. A fake counted OKX adapter replaced only the external transport; no live order was sent. The owner fence passed 41 Node tests plus 24 Python tests at exact Finance revision `999672a...`.

The physical matrix proved an important boundary. Replaying an exact Effect after dispatch consumption creates **zero** new POSTs and returns `RECONCILIATION_REQUIRED`; read-only reconciliation also creates zero POSTs. But creating a distinct new Effect identity for the same economic intent after ambiguous/unbound/accepted-response-loss created **one additional POST** and `duplicateEconomicWrite=true`. Exactly-once is therefore identity-scoped, not an economic-intent-global dedupe guarantee.

### Evaluator self-falsification

P10a and P10b initially treated post-dispatch `RECONCILE_EXACT_EFFECT` as the only correct next action. That oracle was wrong: production Finance proves `EXECUTE_EXACT_EFFECT` is also safe because the consumed dispatch identity cannot POST twice and routes to reconciliation. Those campaigns are retained only as diagnostics; no selective rescoring occurred.

The corrected P10c used set-valued owner-grounded next-action acceptance.

| Treatment | Accepted | Duplicate new-write intent | Missed exact resume | Unnecessary hold |
| --- | ---: | ---: | ---: | ---: |
| changed-only | 45/48 | 0 | 0 | 0 |
| raw current | 45/48 | 0 | 3 | 1 |
| always-on scoped basis | 40/48 | 0 | 3 | 4 |
| **phase-gated basis** | **48/48** | **0** | **0** | **0** |

The result is not an ApplicabilityService. The surviving trajectory is:

```text
planning intent
  -> pre-admission applicability basis/current owner fence
  -> exact Effect admission
  -> exact Effect identity
  -> exactly-one dispatch identity
  -> exact replay and/or reconciliation
```

Continuing to expose mutable currentness/applicability after exact admission can distract the Agent from valid recovery identity.

## P11 — Order stability

The mechanical experiment first separated presentation order from semantic order. An owner-declared unordered six-dataset Finance bundle has 720 raw permutation digests but collapses to one digest under stable dataset identity encoding. Conversely, five Effect events with explicit `orderingDomain + sequence` were reconstructed correctly by sequence identity; naive lexical sorting was semantically valid in **0/120** permutations. There is no safe global sorting rule.

P11-v1 is invalidated wholesale: the original 13-field Tool schema produced truncated DeepSeek function arguments in 141/144 cells. P11-v2 fixed the wire representation, but then exposed a second confound: “tracking-error leader” was ambiguous while the oracle meant the numerically largest tracking error. Its large apparent order effect is diagnostic only.

P11-v3 froze the intended semantic target explicitly.

| Representation | Strict | Distinct input digests |
| --- | ---: | ---: |
| **raw six presentation orders** | **44/48** | 6 |
| stable dataset-order list | 42/48 | 1 |
| identity map | 43/48 | 1 |

Canonicalization therefore did not improve semantic accuracy. The earlier P9 order-sensitivity claim must be narrowed: order can remain a falsifier, but this workload did **not** reproduce a useful order-normalization effect once the semantic question was clarified.

## World-model revision

1. Applicability and replay are different phases, not two versions of the same freshness question.
2. Exactly-once guarantees attach to exact operation/Effect identity; replacing identity can re-open consequence authority.
3. Recovery may have multiple safe owner-native next actions; evaluators must not force a single path when exact replay and reconciliation both preserve the invariant.
4. Before blaming Context order, falsify ambiguity in the question, metric and oracle.
5. Deterministic canonical bytes are useful mechanics only under explicit owner semantics; they do not imply a better model representation.
6. No EffectPhaseService, global deduper, EvidenceNormalizer, OrderService or ContextCompiler earns existence.

## Apparatus recovery

The complete executable/raw campaign is Git-recoverable from snapshot `cc259ffdf046fcb8a4a17d563bd07ac4e7944a64` under `research/experiments/p10-p11-effect-phase-order-v0/apparatus/`. The current tree intentionally removes it; no P10/P11 runner becomes a long-lived research authority.
