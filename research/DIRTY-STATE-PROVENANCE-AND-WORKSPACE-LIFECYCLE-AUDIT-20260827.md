# Dirty State Provenance and Workspace Lifecycle Audit — 2026-08-27

## Current standing

Ordivon's historical `dirty -> preserve / do not touch` discipline was a rational loss-prevention approximation, not a design mistake. It becomes insufficient when `dirty` is treated as a semantic claimant or when preservation of unique bytes is coupled indefinitely to preservation of the live environment that happens to contain them.

The current evidence-backed refinement is:

```text
Dirty != Active
Staged != CurrentIntent
OldDirty != RedundantResidue
DigestPreserved != ContentRecoverable
Recoverable != Current/Claimed/Valuable/SafeToDelete
PreserveReachability != PreserveEmbodiment
```

Runtime retains physical truth and exact compare-and-close; Host/Task/domain owners retain semantic disposition. The new Runtime `dirty-checkpoint` operator fills the previously missing `checkpoint_or_export` step without creating deletion authority.

Canonical Runtime implementation: `ordivon-runtime@f7600266c97aa9dd77dfb52873ad0c8f58f2f547`.

Full evidence and falsifiers: `research/experiments/dirty-state-provenance-v0/RESULT.md`.

## Canonical-root remediation

Media and Computing staged-only canonical roots were proven to contain ambiguous historical mixtures/rollback candidates rather than active canonical-root work. Their exact index trees were first retained under source-repository quarantine refs, current Host and physical claimant evidence was checked, and only then were the shared roots restored to committed main. No candidate bytes were deleted.

## Workspace lifecycle implication

Do not replace the old rule with `stale -> delete`. Replace the coupling:

```text
uncertain dirty state -> keep live Workspace forever
```

with:

```text
observe physical state
-> recover claimant/currentness
-> preserve unique state into an adequate immutable carrier when needed
-> bind semantic disposition to exact Runtime sourceStateDigest
-> compare-and-close only after owner admission
```

The carrier is history/evidence, never current authority.
