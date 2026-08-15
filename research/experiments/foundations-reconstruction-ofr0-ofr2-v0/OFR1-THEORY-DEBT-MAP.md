# OFR1 — Theory Debt Map

## Verdict

The dominant debt is not “missing documentation”. It is **recoverability of causation under high theory-to-code compression**.

Do **not** sum these debts into one score. Different debts demand opposite treatments: Distillation Debt may justify compression into Knowledge; Negative-Knowledge Debt may justify preserving one rejected path; Representation-Asymmetry Debt may require reverse engineering from code rather than more prose.

| ID | Debt | Main risk |
|---|---|---|
| D0 | Distillation Debt | Fresh Agents re-derive already-tested distinctions or over-read current Core as complete. |
| D1 | Causal-Recovery Debt | Future maintenance removes a necessary distinction or reintroduces a previously falsified mechanism. |
| D2 | Negative-Knowledge Debt | Attractive old ideas are repeatedly rediscovered and re-tested without new discriminating conditions. |
| D3 | Cross-Owner Convergence Debt | Stable structure remains fragmented, or later synthesis over-promotes superficial similarity. |
| D4 | Representation-Asymmetry Debt | Theory discovery becomes biased toward verbose owners; low-prose owners look conceptually shallow. |
| D5 | Vocabulary / Representation Drift | False unification or duplicate abstractions; Agents may transfer a rule across the wrong semantic boundary. |
| D6 | Currentness / Source-Relation Debt | A theory document silently substitutes historical evidence for current fact or rewrites history to match present state. |
| D7 | Promotion Debt | Either under-promotion causes repeated rediscovery or over-promotion turns local success into doctrine. |
| D8 | Theory-Use Validation Debt | Foundations become elegant documentation that does not improve reasoning. |
| D9 | Expression / Recoverability Debt | Causal understanding decays even though implementation survives. |

## Strongest observed debts

### D1 — Causal-Recovery Debt

The system often remembers *what must be true* after forgetting *which competing model failed and why*. This is the most dangerous debt because a future cleanup can delete an invariant that appears arbitrary once its failure history has vanished.

### D2 — Negative-Knowledge Debt

Ordivon already has unusually strong deletion culture, but rejected theory is less discoverable than surviving code. Negative results should remain compressed and dormant, not executable.

### D4 — Representation-Asymmetry Debt

The gap between Human/World/Finance/Security research prose and Workstation/Host/Game/Runtime compiled invariants can fool both Human and Agent reviewers into equating verbosity with theory maturity.

### D6 — Currentness / Source-Relation Debt

OFR itself reproduced this: semantic checkpoints, deployed revisions, historical experiment commits and current owner Git can all be different legitimate timeslices. A theory summary that writes “current” without the relation is already lossy.

### D8 — Theory-Use Validation Debt

Even a correct theory can be a useless default representation. OFR7 remains necessary: fresh Agents must actually make better owner-placement, deletion, action and UNKNOWN decisions under the compressed theory.

Machine authority: `theory-debt-map-v1.json`.
