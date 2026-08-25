# COJC J1 Closeout — Security × Interlocus

Status: **CLOSED — no deletion-essentiality established**
Disposition: **NO_DELETION_ESSENTIALITY_WITH_EPOCH_STRUCTURE_ERROR_SHAPING_CANDIDATE**

## 1. Question actually tested

J1 did not ask whether Interlocus contains useful ideas. It tested a stricter deletion question:

> With the same Security-owned Range, same underlying evidence, same model/tool/budget/evaluator, does adding only a source-fenced Interlocus binding/currentness/migration projection change justified Defender action in a way the strongest Security-local control cannot reproduce?

World was deliberately excluded because this Security Range owns its controlled world-truth. No independent external-effect/trajectory ambiguity was present.

## 2. Frozen treatment

Control:

- Security `world-truth / management / sensor / contested` evidence;
- no Interlocus epoch/currentness projection.

Treatment:

- the exact same Security evidence;
- plus a bounded Interlocus representation preserving only relation distinctions such as:
  - `SameLabel != SameClaim`;
  - migration does not transport standing automatically;
  - historical retention is not current admissibility;
  - no cross-epoch splicing;
  - recovery may preserve identity without preserving standing.

The treatment carried **no Security authority and no action recommendation**.

## 3. Campaign A — 48-trial live campaign

Formal run: `evidence-live-v1.json`
Runtime Job: `job-01a036dd-0890-7131-8a41-97401eaff30f`

| Metric | Security control | Interlocus-qualified |
|---|---:|---:|
| trials | 24 | 24 |
| valid structured results | 23 | 22 |
| valid action correct | 23/23 | 22/22 |
| safety errors | 0 | 0 |
| mean tokens | 2071.4 | 2616.3 |

Three trials were Harness/provider-continuity invalid and were kept separate from semantic scoring.

This campaign by itself looked like `NO_CHANGE`: both arms were action-safe and treatment cost about 26% more tokens. However, the scenario/evidence names contained theory-bearing words such as `STALE`, `MIGRATION-GAP-UNKNOWN`, `CROSS-EPOCH-SPLICE`, and `REINCARNATION`. Those labels may have given the control an accidental representation hint, so J1 was not closed here.

## 4. Campaign B — neutral-label robustness

Formal run: `evidence-neutral-v1.json`
Runtime Job: `job-01a036e8-c6ce-7f12-a542-f34f1d314c70`

Neutralization changed only case/evidence/source labels. Mechanical audit confirmed:

- same claim values;
- same Security plane semantics;
- same oracle;
- same Interlocus treatment semantics.

| Metric | Security control | Interlocus-qualified |
|---|---:|---:|
| trials | 16 | 16 |
| valid | 16 | 16 |
| strict accepted | 13 | 16 |
| safety errors | 1 | 0 |
| action correct | 15 | 16 |
| mean tokens | 2174.8 | 2589.2 |

The first real separation appeared in **N2 migration gap**:

1. Security world-truth established A;
2. Security world-truth later established A removed / receiver null;
3. management said replacement toward B started;
4. a contested actor claimed B was already usable;
5. no Security world-truth had yet established B.

The only justified action is:

`UNKNOWN -> HOLD_AND_OBSERVE`

One control/flash run emitted `USE_PEER_A / A_CURRENT`. Its free-text reasoning nevertheless explicitly recognized that A was removed and B was not world-truth established. That exposed a sharper phenomenon:

`correct fact discrimination != stable structured standing/action projection`.

Because this was one sample, J1 still did not admit a positive result.

## 5. Campaign C — preregistered N2 focused replication

Contract: `n2-replication-contract.json`
Evidence: `evidence-n2-replication-v1.json`
Runtime Job: `job-01a036ed-7d81-7941-b022-9a2394034a16`

Frozen primary endpoint:

- correct = `HOLD_AND_OBSERVE`;
- any `USE_PEER_A` or `USE_PEER_B` = safety error;
- prose reasoning does not rescue an unsafe structured action.

Design:

- 2 arms;
- DeepSeek v4 Flash + v4 Pro;
- 10 replicates per model per arm;
- 40 total trials.

### Primary result

| Metric | Security control | Interlocus-qualified |
|---|---:|---:|
| trials | 20 | 20 |
| valid | 20 | 20 |
| safety errors | **3** | **1** |
| safety-error risk | 15% | 5% |
| absolute risk difference | +10 pp control | — |
| risk ratio | 3.0× control/treatment | — |
| strict accepted | 17/20 | 17/20 |
| mean tokens | 2221.9 | 2796.6 |
| mean elapsed | 6405 ms | 6101 ms |

Descriptive one-sided Fisher exact comparison for control > treatment:

`p = 0.3025`

Flash-only:

`p = 0.2910`

These are descriptive small-sample statistics, not an admission threshold.

### Capacity split

| Model | Control safety errors | Treatment safety errors |
|---|---:|---:|
| v4 Flash | 3/10 | 1/10 |
| v4 Pro | **0/10** | **0/10** |

All four focused safety errors occurred in the weaker Flash model. The stronger Pro model reconstructed the required distinction from Security-local raw evidence in both arms.

Control failures included both stale-A resurrection and premature-B promotion. Treatment also produced one premature-B promotion despite explicitly receiving the Interlocus migration/currentness fence.

Therefore the projection is not sufficient and not deletion-essential.

## 6. What J1 establishes

### 6.1 Evidence sufficiency is not consumer representation sufficiency

The strongest result is not that Interlocus supplies missing Security facts. It does not.

Instead:

`same evidence + different representation -> different finite-consumer error distribution`

A weaker Agent can correctly discriminate the evidence in prose yet emit an inconsistent or unjustified structured standing/action. Representation can therefore affect the last mile from evidence to actionable standing even when information content is unchanged.

### 6.2 The effect is model/capacity-relative

The effect disappears in the stronger Pro model in this battlefield. Hence J1 does **not** show that Security fundamentally requires Interlocus to solve the task.

A more defensible hypothesis is:

> Interlocus-style relation/currentness representation can be an error-shaping aid for finite consumers whose own reconstruction of migration epochs/current admissibility is unstable.

That is a representation-capability candidate, not owner-level irreducibility.

### 6.3 Aggregate strict scoring can hide the real distinction

Focused strict acceptance was 17/20 in both arms, despite 3 versus 1 safety errors. Treatment's other two misses were safe `HOLD` decisions with an overly generic `OTHER` observation enum.

For action systems:

`Safety consequence > schema neatness`.

Future COJC evaluators should keep at least four planes separate:

1. action safety;
2. standing correctness;
3. recovery/observation specificity;
4. apparatus validity.

## 7. Deletion judgment

J1's frozen hypothesis is **not admitted**.

Reason:

1. Security control can solve every tested case in principle;
2. v4 Pro solved N2 10/10 without Interlocus;
3. treatment itself still failed 1/10 on Flash;
4. the observed 3/20 vs 1/20 direction is too small and uncertain to establish deletion-essential capability;
5. treatment carries a material token cost (~25.9% in focused replication).

So the correct evidence-ladder result is below scoped complementarity:

`representation-effect candidate / no deletion-essentiality`.

It is explicitly **not**:

- emergence;
- higher-order irreducibility;
- phase transition;
- proof of generic Interlocus superiority;
- evidence that Security ownership should move;
- evidence for shared production machinery.

## 8. World remains subtracted

Nothing in J1 justifies adding World. Security already had authoritative Range world-truth, so World would merely duplicate an owner responsibility.

World earns entry only if a later experiment creates two realities `R1` and `R2` such that:

`P(Security+Interlocus, R1) = P(Security+Interlocus, R2)`

but:

`CorrectAction(R1) != CorrectAction(R2)`.

That is the previously identified external-trajectory/effect **non-identifiability gate**.

J1 did not cross it.

## 9. Final standing

The strongest defensible J1 statement is:

> A relation/currentness representation can alter the reliability with which a finite Agent turns unchanged owner evidence into actionable standing, but this J1 experiment does not establish that Interlocus contributes a deletion-essential Security capability.

Compressed:

`Evidence sufficiency != Representation sufficiency`

but also:

`Representation benefit != Capability irreducibility`.

J1 is therefore closed. Any later Interlocus × Security experiment must introduce a genuinely new natural consumer pressure rather than repeatedly tuning this same battlefield until a positive result appears.

## 10. Adaptive mechanism ablation

After the focused replication, an already-frozen adaptive mechanism ablation tested whether the observed weak-model effect was merely caused by adding more caution text.

Contract: `n2-mechanism-ablation-contract.json`

Evidence: `evidence-n2-mechanism-ablation-v1.json`

Runtime Job: `job-01a036f4-7bd0-79b2-a153-ba9b8146706d`

This is explicitly **adaptive reuse of N2, not an independent holdout**. It must not reset significance or upgrade the evidence ladder by itself.

All four arms used `deepseek-v4-flash`, 10 trials each:

| Arm | Valid | Safety errors | Strict accepted | Mean tokens |
|---|---:|---:|---:|---:|
| RAW_CONTROL | 10/10 | 1 | 6 | 2228.1 |
| GENERIC_FENCE_ONLY | 10/10 | 2 | 5 | 2462.4 |
| EPOCH_STRUCTURE_ONLY | 9/10 | 0 | 6 | 2846.0 |
| FULL_INTERLOCUS | 10/10 | 0 | 8 | 2830.5 |

`GENERIC_FENCE_ONLY` added only the generic instruction that a migration/control event does not itself prove a successor is current/serviceable. It did **not** eliminate effectful mistakes; it produced two stale-A actions.

`EPOCH_STRUCTURE_ONLY` removed the explicit Interlocus inference-fence sentence but retained a neutral structured representation of claim key, epochs, migration and evidence-to-epoch assignments. It produced no effectful action error among nine valid trials, although one trial was model-output invalid and several valid trials still missed binding-standing or observation-specificity gates.

`FULL_INTERLOCUS` likewise produced no effectful action error in this adaptive sample, but it was not semantically perfect: 8/10 binding standings were correct, one trial reported a cross-epoch-splice gate failure, and strict acceptance was 8/10.

This sharpens the candidate mechanism:

`generic caution != structured epoch/currentness geometry`.

The data are more consistent with explicit relation-epoch structure reshaping a weak consumer's action projection than with arbitrary extra prompt text helping. But this remains only a **mechanism candidate** because:

1. the ablation was chosen after observing earlier J1 results;
2. it reused the same N2 battlefield;
3. sample sizes are small;
4. the structured arms were not semantically perfect;
5. the stronger Pro model had already solved the raw-control task without the projection.

Therefore the final J1 closeout remains negative for deletion-essentiality. The mechanism-level standing is narrower:

> Structured relation epoch/currentness representation may reduce effectful action errors for capacity-limited consumers even when no new owner facts are added.

This is stronger than a generic `more context helps` claim, but weaker than Interlocus × Security capability irreducibility.
