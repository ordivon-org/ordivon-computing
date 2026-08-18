# Computing Research Git Durability

## Current committed base

`main = origin/main = 1a9cc7b3a9144751b6f3d38650f42f0ea7340148` at repair inspection time.

## Preserved historical Broad Computing lineage

Detached Broad Computing campaign final head:

`4c70e7f90b12c204509536f7b11246969c6b2b0a` — `research: close broad Computing umbrella campaign`

Durable local historical ref created by this repair:

`refs/heads/research/history/computing-umbrella-closeout-20260818`

This final head contains, by ancestry, `4d4d5919e45b115f3baaf0594f1da06fa2a311ba` (`research: reconcile broad Computing owner decomposition`) and the earlier A–K / saturation campaign lineage.

The historical ref is provenance only. It is intentionally not merged, replayed, or fast-forwarded into current `main` by this repair.

## Dirty source safety

At repair start, the live source worktree had staged deletions under `research/experiments/computational-applicability-transport-v0/`. Their intent was not inferred and the repair did not reset, restore, stash, clean, or overwrite them. Materialization was performed in an isolated detached worktree from the committed base.
