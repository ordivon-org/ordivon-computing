# HR0 v1 preflight failure

HR0 v1 was stopped before any human response. The failure was in the experiment's scoring law, not in Harness execution, browser geometry, or the sealed human stimuli.

## What happened

The preregistered v1 participant scorer changed a factual-answer target to `O4` whenever the evidence required by the R6 oracle was absent from the initial viewport. That collapsed two consequences that Studio R6 had deliberately kept separate:

1. **factual answer accuracy** — did the observer select the mechanism's oracle answer?
2. **evidence discipline / unsupported inference** — was that substantive answer actually established by the evidence visible to this encounter?

Under the original R6 law, an observer can guess the right factual answer while still making an unsupported assertion. Conversely, abstaining with `O4` can be epistemically disciplined while not matching the underlying factual oracle. v1 incorrectly treated those as one notion of correctness.

## Evidence

- all 12 planned Harness surrogate Runs produced structured conclusions;
- no Provider/equipment failure occurred;
- no human mechanism H1–H3 was sent to a Provider;
- the distorted v1 scoring reported fragmented adaptation accuracy of 8.3%, a value not comparable to the R6 adaptation metric;
- final human stimulus commitments were already frozen in `fb9b4ab1a37e0ad598ea7c9f9c2f45a5eb64d71b` and browser geometry for H1–H3 remained exact.

## Disposition

**Falsify HR0 v1 before human use.** Do not patch `contract-v1.json` or regenerate H1–H3. HR0 v2 reuses the exact same sealed human bytes and changes only the response/scoring interpretation so factual accuracy, unsupported inference, and epistemic decision quality remain distinct.

This is the desired failure mode of preregistration: a broken measurement law becomes a new version rather than being silently repaired after seeing data.
