# S5A Closeout — Future Sufficiency / Transition Congruence

Status: **COMPLETE; registered dispositions = FRONTIER_IS_CURRENT_SUMMARY_NOT_STATE + CONTINUATION_KERNEL_SURVIVES_GENERATIVE_TEST + LATENT_OWNER_STATE_NEEDED**.

## Main result

Orthogonal Frontier v2 is a strong Agent-facing currentness representation, but it is not a transition-sufficient state abstraction.

A transition-sufficient abstraction F would require, over the admitted event language:

`F(h1) = F(h2)  =>  F(h1·f) = F(h2·f)` for every common future suffix f, relative to the institutional observables under test.

S5A found direct violations.

## Targeted future-distinguishability families

1. **Hidden compromised-root identity**
   - `compromise(R1)` and `compromise(R2)` expose the same Frontier: root standing is DEGRADED.
   - Common future `compromise(R1)` leaves the first state DEGRADED but makes the second THRESHOLD_COMPROMISED.
   - Therefore exact compromised-root identity is future-relevant Security state even when current consumer standing is identical.

2. **Hidden single current-support authority claim**
   - one live A-support claim and no claim both expose CURRENT / no conflictClaimants in Frontier v2.
   - Common future B-support claim produces CONTESTED in the first history and CURRENT in the second.
   - A claim can therefore be transition-relevant before it becomes a visible contest.

3. **Hidden sanction transition registry**
   - two histories were constructed with identical Frontier, identical current brute resources, identical remedy, and identical historical-invalidity presence, but with different live valid sanction IDs (S1 vs S2).
   - Common future `invalidate_sanction(S1)` creates remedy in only the S1 history.
   - Exact confirmation is retained in `evidence-s5a-t3-resource-preserving.json`.

The generic shrinker in the first S5A output did not preserve the extra same-resource constraint while minimizing T3; that minimized representation is presentation-invalid for the World-state guard. The original targeted pair was valid, and the separately frozen confirmation re-establishes the counterexample while preserving equal resources. The registered disposition does not depend on the invalid shrink.

## Generative result

- 120,000 random histories generated.
- 728 Orthogonal-Frontier equivalence classes had collisions.
- 149,943 common-future checks were exercised over equal-Frontier histories.
- A random Frontier counterexample was found and shrunk; it again exposed hidden authority-claim state.

A deliberately owner-side `ContinuationKernel v0` retained:

- source-valid Monitor;
- effective controller;
- normative/physical quota;
- lineage/identity relation;
- exact compromised-root set + active anchor;
- current-support claimant set;
- current remedy;
- sanction transition registry required by future review semantics.

Results:

- 3,850 equal-kernel collision classes;
- 149,781 common-future checks;
- **0 kernel divergence counterexamples found** under the frozen search budget.

This is bounded falsification evidence, not a proof of completeness/minimality.

## Architecture standing

The experiment rejects a category error:

`Agent-facing currentness projection == owner transition state`.

Instead:

`Owner-native continuation state -> derived Agent currentness projection`.

Fields enter owner transition state when removing them creates future distinguishability. They do not automatically enter the Agent-facing representation. This preserves the earlier `derive, don't duplicate` owner boundary.
