# FD4 second-wave documentation preflight — initial treatment

The contract was preregistered at `53391ad` before any live Provider call. It compared eight frozen FD0 reader-consequence tasks across exact baseline/treatment revisions for World, Host, Runtime, and Computing.

## Execution

The initial parallel run accepted 47/48 trials. `FD0-COMP-01` baseline replicate 2 ended with HTTP `IncompleteRead(2094 bytes read)`. The incomplete run is retained verbatim in `evidence/preflight-v1-initial.json`. A repair script replayed only that missing frozen task/arm/replicate with the original deterministic credential slot assignment; no task, oracle, arm revision, judge rubric, or other trial was changed/replayed.

Final evidence contains **48/48 accepted reader trials**, 48 blind judge results, zero semantic publication blockers, and zero treatment critical over-inferences or unsupported-authority claims. Accepted calls consumed 97 recorded physical Provider calls; the failed initial HTTP call adds a lower bound of one additional physical call.

## World

Both frozen tasks remained 3/3 correct.

- WORLD-01: 16,349 → 11,444 input bytes (-30.0%), tokens 14,686 → 11,564 (-21.3%).
- WORLD-02: 33,366 → 28,461 bytes (-14.7%), tokens 24,547 → 21,297 (-13.2%).

World therefore passes both the primary causal gate and the secondary burden test.

## Host

Both frozen tasks remained 3/3 correct with zero over-inference.

- HOST-01: 10,268 → 11,053 bytes (+7.6%), tokens 12,484 → 12,373 (-0.9%).
- HOST-02: 39,037 → 39,822 bytes (+2.0%), tokens 28,380 → 28,523 (+0.5%).

This is essentially burden-neutral: the README is causally reorganized around session replacement/WorkingCheckpoint responsibility, while the architecture-containing task is dominated by unchanged Architecture bytes. No material token regression is established.

## Computing

Both frozen tasks remained 3/3 correct. The second local contraction performed before prereg materially reduced both tested bundles.

- COMP-01: 26,810 → 22,502 bytes (-16.1%), tokens 21,577 → 18,885 (-12.5%).
- COMP-02: 24,210 → 17,810 bytes (-26.4%), tokens 20,086 → 16,128 (-19.7%).

Computing passes primary and secondary tests.

## Runtime

Both Runtime tasks remained 3/3 correct with all required points covered and zero over-inference. However the first Runtime rewrite **fails the preregistered secondary contraction review**:

- RUNTIME-01: 11,202 → 12,632 bytes (+12.8%), tokens 12,270 → 12,972 (+5.7%).
- RUNTIME-02: 11,202 → 12,632 bytes (+12.8%), tokens 12,315 → 12,785 (+3.8%).

The treatment is causally safe but not yet an accepted Feynman contraction. The additional target-specific explanation is not buying a new decision on these ceiling-correct tasks. Runtime therefore requires a separate, preregistered follow-up contraction against the first treatment; this report and raw evidence are frozen before that follow-up begins.

## Interpretation boundary

These are fresh-Agent reconstruction results for the admitted DeepSeek family. They are not human-comprehension evidence. Exact correctness does not prove preferred style, delayed recall, or subjective clarity.
