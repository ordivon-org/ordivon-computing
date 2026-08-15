# OFR5 — Foundations Atlas / Progressive Causal Hydration Results

## Frozen verdict

`NO_ATLAS_PROMOTION`. The frozen holdout gate was not repaired after observing results.

| Treatment | Physical | Case localization | Requested-role fidelity | Refs | Epistemic boundary | Unsupported | Prompt/accepted |
|---|---:|---:|---:|---:|---:|---:|---:|
| FULL_EAGER | 0.917 | 1.000 | 1.000 | 1.000 | 0.636 | 0.273 | 8077.5 |
| ATLAS_PROGRESSIVE | 0.500 | 1.000 | 1.000 | 1.000 | 0.667 | 0.167 | 7680.5 |
| INDEX_ONLY | 0.917 | 1.000 | 0.500 | 0.091 | 0.636 | 0.364 | 2789.8 |
| CENTRALIZED_LAWS | 0.583 | 0.000 | 0.338 | 0.000 | 0.714 | 0.857 | 5453.7 |

The progressive candidate recovered every requested causal role in its six realized holdout answers, but only 6/12 trials realized and its failure-adjusted prompt cost was 95.1% of eager full context. That fails both the reliability and cost purpose of progressive disclosure.

## What survived the falsification

### 1. Compact index is an excellent locator, not a theory substitute

The 514-word index can identify the correct owner-local causal case. INDEX_ONLY shows the limit sharply: localization remained perfect while causal-role fidelity fell to 0.50 and exact-reference fidelity to 0.0909.

### 2. Cross-owner laws cannot replace local causal histories

CENTRALIZED_LAWS never identified the exact OFR3 owner-local case in accepted holdout answers. It often substituted a plausible C-family law for the concrete rival/falsifier/commit history, producing high unsupported inference and over-generalization. Shared invariant and owner-local causal archaeology are different knowledge products.

### 3. Field-level progressive hydration is too fine-grained for the current consumer

The Atlas navigator never missed a requested role when it realized, but role precision was only 0.724. The later one-loop Tool diagnostic over-fetched even more (precision 0.543). The model preferred safety through full-case hydration. OFR5 therefore does not earn a per-role public interface. The current smallest stable semantic hydration unit is one complete causal case.

### 4. Authority/currentness must be mechanical metadata

Even FULL_EAGER repeatedly called frozen reconstructions “current owner truth” or said they could establish evidence sufficiency/mechanism admission. More prose did not solve this. When the existing Harness DomainToolLoopRunner returned truthRole/currentness/authority flags mechanically, the post-holdout diagnostic reached 12/12 realization and 1.0 epistemic-boundary fidelity.

## Post-holdout mechanism diagnostics — not promotion evidence

Oracle-targeted minimal hydration: 10/12 realized, requested-role fidelity 1.000, ~2043.6 prompt tokens/accepted answer. This proves the frozen content can be compact when the correct case/roles are externally known; it does not prove an Agent can choose that subset cheaply.

Existing Harness single-loop read-only Tool hydration: 12/12 realized, requested-role fidelity 1.000, epistemic-boundary 1.000, ~6881.5 prompt tokens/accepted answer. It solves reliability/authority in this diagnostic but still costs too much because iterative context plus over-hydration remain.
