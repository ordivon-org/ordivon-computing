# Cross-cut maintenance P1 v0

P1 reduces iteration drag without promoting another central authority.

The work has five empirical outcomes:

1. **Compiler-cache equipment was falsified as a default Runtime answer.** `sccache` is useful for rebuilding the same Rust target path, but current Runtime correctness intentionally isolates `CARGO_TARGET_DIR` per Workspace and the tested cross-target variants produced zero Rust cache hits. The equipment remains available; Runtime does not pretend the RSI build-churn problem is solved.
2. **Dirty aging now has an owner-local evidence action.** Runtime `dirty-review` revalidates one explicit dirty Workspace, records exact record/HEAD/status/diff/untracked identities and recommends an aging action while authorizing no deletion or content mutation.
3. **Fast lifecycle observation is cheap enough to use when demanded, not enough to justify another timer by itself.** Ten scans had a 1.754 s median after a 4.37 s cold first scan and observed real state transitions. P1 keeps the existing production cadence and prefers on-demand/event-driven reconciliation until a recurring consumer is demonstrated.
4. **Cross-owner conflicts are classified rather than centrally resolved.** A contained Runtime PATH mismatch is observer-context drift, user-local Ruff was provider-placement drift and was converged to pacman, forbidden `msitools` is owner-policy drift requiring owner review, and ambient Windows administrator state remains a warning because execution authority is explicitly limited/elevated elsewhere.
5. **Computing conformance now owns its execution semantics.** A repo launcher provides supported Python 3.12.13 with pinned Ruff/jsonschema while Computing's mise environment owns Vale, markdownlint, CSpell and Lychee. A small `ruff.toml` fixes the intended correctness rule set instead of inheriting provider-default rule expansion. CI and local/Runtime execution use the same launcher.

P1-F deliberately does **not** promote the eight-class P0 lifecycle vocabulary into a production shared package. Computing is currently the only materially different consumer requiring that exact vocabulary; Runtime and World retain owner-native lifecycle semantics. One useful projection is not enough evidence for another shared package, much less another repository.
