# OFR7 Measurement Diagnosis

OFR7 deliberately keeps failed measurements rather than silently rescoring them. Three auxiliary fields were preregistered but proved underidentified on the holdout even when primary choices and causal reasoning were correct.

## `truthState`

The prompt did not bind one exact proposition. For a revocation case, one answer can truthfully call the *owner revocation observation* `KNOWN_TRUE` while the gold intended *current access allowed* = `KNOWN_FALSE`. Exact enum disagreement therefore does not prove a wrong decision model.

## `evidenceAuthority`

The enum mixes two questions: **who owns the facts?** and **are those facts sufficient to settle the final proposition?** An owner-current observation can authoritatively prove why a final state remains unresolved. Answers therefore oscillated between `OWNER_CURRENT_FACT` and `INSUFFICIENT_CURRENT_EVIDENCE` while selecting the same correct action.

## `seekMoreEvidence`

The field mixes evidence needed to **choose the current decision** with evidence that the **chosen recovery action says to acquire next**. An Agent that already correctly chooses “keep UNKNOWN and reconcile” can reasonably answer false (no more evidence needed to choose) or true (more evidence needed before world completion).

These fields remain recorded, but OFR7 does not use their exact-match rates to accept/reject Foundations.

## Treatment-blind `unsupportedInference`

The judge intentionally did not receive treatment identity or theory text. Two flags were triggered because an answer cited supplied doctrine (`A17`, `A13`/“theory surface”) rather than because it invented a current external fact. Those observations remain in the dataset, but `authorityConfusion` is the stronger measure of theory becoming false world authority here; it was zero in every treatment.

The valid primary semantic surface is therefore: exact action choice + causal mechanism/boundary + owner-authority confusion, with physical realization and cost kept as separate axes.
