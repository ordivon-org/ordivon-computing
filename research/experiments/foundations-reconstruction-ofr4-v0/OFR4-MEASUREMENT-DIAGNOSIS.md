# OFR4 — Measurement Diagnosis

## The frozen action metric collapsed three different transitions

The Agent prompt asked whether a prose `REOPEN PROBE` should produce one binary `REOPEN | KEEP_CLOSED` decision. Holdout exposed that this was not one well-defined semantic target.

At least three transitions had been collapsed:

```text
Theory.reopenCondition
    != Evidence.sufficientToClaimConditionObserved
    != Research.reopenQuestion
    != Owner.admitPreviouslyRejectedRival
```

### Workstation counterexample

The causal/minimal Agents could recover the exact selected-path invariant and its boundary, then answer `KEEP_CLOSED` because a consumer explicitly asking for “best current route” with a new identity is already the allowed **different-product boundary**, not a reason to restore silent reselection inside exact revalidation. Under OFR3 wording, that same situation is also a reason to reopen local engineering. Both readings are coherent; the binary target is not.

### Security counterexample

A persistent session that needs prospective grant changes is exactly the stated reopen condition for new authority-lifecycle engineering. But it is **not** evidence for restoring the rejected retroactive-revocation model. Again, “reopen engineering” and “admit old rival” diverge.

### Finance counterexample

Several Agents refused to treat the sentence “a compact model was independently tested and preserves all properties” as sufficient evidence because the probe carried no provenance/results. This is epistemically defensible: Theory text does not grant Evidence authority merely because a natural-language scenario asserts that evidence exists.

## Consequence

The frozen `reopenDecisionAccuracy` gate is measurement-invalid. We do not repair the oracle after seeing holdout and do not rescore the same trials under a new target.

Instead OFR4 retains the failure as a new boundary:

> **A causal theory packet may state when a question deserves reopening, but it must not become the owner of whether evidence establishes that condition, whether research resumes, or whether a rejected mechanism gains action authority.**

A future action-pressure test must separate at least:

```text
researchReopen?
evidenceSufficient?
rivalAdmission?
```

and bind the evidence claim to an explicit truth/provenance role.
