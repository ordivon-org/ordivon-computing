# S4B Closeout — Agent Metamorphic Robustness

Status: **COMPLETE; registered dispositions = METAMORPHIC_ROBUSTNESS_EFFECT + FRONTIER_STABILIZATION + RAW_HISTORY_SENSITIVITY**.

## Mechanical completion

- 8 semantics-preserving metamorphic pairs / 16 distinct histories.
- 2 representation arms x 2 models x 2 replicates = 128 trials.
- Flash 64/64 and Pro 64/64 completed; combined evidence has 128 unique tuple identities.
- One RAW pair comparison was apparatus-invalid because one member was invalid; it was excluded from semantic pair denominators according to the frozen contract and was not retried.

## Pair-level results

| Endpoint | RAW_HISTORY | RAW_PLUS_ORTHOGONAL_FRONTIER |
|---|---:|---:|
| valid pair comparisons | 31/32 | 32/32 |
| both sides exact-response correct | 48.4% | **100.0%** |
| response invariant across equivalent histories | 61.3% | **100.0%** |
| exactly one side response-correct | 29.0% | **0.0%** |
| both sides strict all-coordinate correct | 45.2% | **100.0%** |
| full decision-signature invariant | 61.3% | **100.0%** |
| consequence-authority invariant | 83.9% | **100.0%** |
| pair has any semantic safety error | 16.1% | **0.0%** |

Registered deltas:

- Frontier vs Raw pair-both-correct: **+51.6 pp**.
- Frontier vs Raw one-side-only-correct: **-29.0 pp**.
- Frontier vs Raw response invariance: **+38.7 pp**.

Therefore all three applicable registered conclusions trigger:

1. `METAMORPHIC_ROBUSTNESS_EFFECT`;
2. `FRONTIER_STABILIZATION`;
3. `RAW_HISTORY_SENSITIVITY`.

## Interpretation

On histories already proven equivalent by the semantic substrate, a finite Agent consuming raw history alone frequently changes its response because of history transformations that should not alter actionable institutional currentness. An orthogonal currentness projection eliminated the measured pair instability in this bounded set.

This is stronger than S2 average accuracy because S4B controls the semantic relation between paired histories. It is still a representation-consumption result, not proof that the Frontier is itself a transition-sufficient system state.

## Boundary exposed by S4B

A representation can stabilize fresh-Agent decisions while still omitting latent owner state required to process future events. Therefore the next question is not another Agent benchmark. S5A attacks **future sufficiency / transition congruence**:

`F(h1)=F(h2)` must imply that a common admissible future cannot make the two histories institutionally diverge if F is to be called a state rather than a current summary.
