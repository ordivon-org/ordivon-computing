# Runtime documentation contraction follow-up

The FD4 primary preflight found the first Runtime rewrite causally safe but unnecessarily expensive: both frozen Runtime decisions stayed perfect while the entry bundle and Provider burden increased. Per the preregistered secondary rule, that treatment was not accepted as the final Feynman entry.

A compact v2 README was therefore created and committed at `853858e941061468c011dca33fcc71e54f90306f`. It retains the physical-proof boundary, response-loss identity rule, owner split, one Runtime workflow, target/profile summary, effect-opaque distinction, and reader routes while moving target-specific Windows/structured-effect detail back behind technical documentation links.

The follow-up was preregistered at `8dd1c1d4e5eb30afa31838ce99a1f3c8774bf331` before live calls. It compared the first treatment `a09ccd2c0647a0b276920b4f3e95227340b056cc` against compact v2 on the same two frozen Runtime tasks, three fresh readers per arm, with separate arm-blind judges.

## Result

- 12/12 accepted trials;
- 24 physical Provider calls;
- zero failures;
- both arms 3/3 correct on both tasks;
- zero critical over-inference;
- zero unsupported-authority claims;
- no publication blockers.

### RUNTIME-01

- input: 12,632 → 8,194 bytes (**−35.1%**);
- subject+judge Provider tokens: 12,970 → 10,186 (**−21.5%**);
- required-point coverage: 9/9 in both arms.

### RUNTIME-02

- input: 12,632 → 8,194 bytes (**−35.1%**);
- tokens: 12,778 → 10,177 (**−20.4%**);
- required-point coverage: 6/6 in both arms.

Against the original pre-FD4 Runtime README (`a62d0b9`), compact v2 is also smaller: 11,202 → 8,194 tested bytes (**−26.9%**). The initial rewrite's additional prose therefore failed the deletion test and was removed from the default entry.

## Publication boundary

Passing this follow-up does not remove the Runtime currentness fence. The owner root worktree is concurrently changing the engine and every technical document linked by the README (`status`, `runtime`, `operations`, `compatibility`, `effect-kernel`, `data-and-privacy`, `releases`). Compact v2 remains revision-bound under `refs/heads/docs/feynman-runtime-entry-v1` until that owner contraction lands and the entry is revalidated against it.

This is Agent reconstruction evidence, not human-comprehension evidence.
