# Dirty State Provenance / Workspace Lifecycle Audit v0 — Result

Date: 2026-08-27

## Decision

```text
ADMIT bounded dirty-state preservation/disposition repair
REJECT dirty=active
REJECT age-only cleanup
REJECT automatic dirty deletion
REJECT new Dirty-State owner / ontology / registry
REJECT structured Host disposition field as correctness primitive
ADMIT Runtime operator dirty-checkpoint as physical recovery carrier
```

The historical conservative policy was correct for its original pressure: when semantic ownership and recoverability were weak, `dirty -> preserve / do not automatically delete` minimized false deletion. The current system has outgrown the *binary interpretation* of that policy, not its safety boundary.

The surviving distinction is:

```text
Preserve reachability != preserve live embodiment
```

with the stronger non-lifting boundary:

```text
Recoverable != Current != Claimed != Valuable != Admitted != SafeToDelete
```

## 1. Canonical-root provenance falsifier

Two shared canonical roots disproved `dirty == active concurrent work`.

### Media

Observed root state was 15 staged / 0 unstaged / 0 untracked. Blob lineage showed a cross-time staged mosaic: Chapter 2/3/4 blobs from one historical cut, Chapter 5/claims/cognition from another, later metadata from another, while already-admitted Chapters 6/7 were staged deleted. The index tree matched no single reachable or unreachable commit.

Exact preservation before remediation:

```text
refs/ordivon/quarantine/dirty-root-media-20260827
  -> 21e55b5273e58278ecad78368c1b467684777325
```

### Computing

Observed root state was 86 staged / 0 unstaged / 0 untracked with ~43,765 deleted lines. Several modified surfaces exactly reverted to older historical blobs while later research surfaces were staged deleted. Independent active Tasks observed this staged state but explicitly did not claim it.

Exact preservation before remediation:

```text
refs/ordivon/quarantine/dirty-root-computing-20260827
  -> 47246341683ff62c6305c8e1b0d7619cf29c064d
```

A complete current-Host checkpoint scan plus `/proc`, `fuser`, Git lock and Runtime-workspace evidence found no current canonical-root claimant. Both roots were therefore reset only after exact preconditions were rechecked: current HEAD/main, exact index tree, exact quarantine tree, no unstaged/untracked state, no physical claimant. Both canonical roots became clean while the exact staged candidates remained reachable through quarantine refs.

This establishes:

```text
Staged != CurrentIntent
ObservedByMany != ClaimedByAnyone
ContentRecoverability != ClaimantResolution
RootDirty != DetachedWorkspaceDirty
```

## 2. Runtime backlog evidence

Initial Runtime diagnose observed:

```text
open Workspaces  236
dirty            163
older than 24h   160
older than 72h   128
older than 7d     77
older than 14d    37
```

Only three dirty Workspaces were younger than 24 hours. Therefore stale dirty state cannot be interpreted primarily as current concurrent work.

A later live reachability census observed 166 dirty physical Workspaces while the system was concurrently evolving:

```text
UNIQUE_CONTENT_PRESENT 115
PARTIAL_UNIQUE          35
CONTENT_REACHABLE       10
UNKNOWN_CONTENT          6

HEAD_BEHIND_MAIN       121
DIVERGED_MAIN            37
HEAD_EQ_MAIN              7
HEAD_AHEAD_MAIN           1
```

Thus the opposite shortcut is also false:

```text
OldDirty != RedundantResidue
```

150/166 observed Workspaces contained all or some dirty blob content not reachable from existing refs. This makes age-only force-close unsafe.

## 3. Historical policy subtraction

Runtime already had an evidence-only `dirty-review` surface and deliberately excluded dirty / active / pinned / unknown / orphan-directory state from automatic lifecycle removal. `workspace.close` already had exact `expectedSourceStateDigest` compare-and-close.

The missing operation was visible in Runtime's own recommendation string:

```text
checkpoint_or_export
```

but there was no corresponding implementation. `dirty-review` persisted status/diff/untracked digests and sizes; it did not preserve tracked diff bytes, untracked bytes, or a reconstructable Git state carrier.

Therefore the old operational attractor was:

```text
Dirty
-> review
-> cannot prove independent content recovery
-> safest action remains keep live Workspace
```

The new pressure was not for weaker deletion safety. It was for a physical carrier between review and release.

## 4. Host/Runtime responsibility falsifier

A disposable Workspace tested whether a new structured Host disposition schema was correctness-required.

1. Host's existing revision-fenced WorkingCheckpoint recorded `DO NOT CLOSE` against exact Runtime `sourceStateDigest D`.
2. Dirty bytes were changed after the checkpoint.
3. `workspace.close(force=true, expectedSourceStateDigest=D)` failed `REVISION_MISMATCH`; the Workspace remained intact.
4. Unique bytes were committed into reachable Git state.
5. Host re-checkpointed against exact new digest `D'` with close-admissible disposition.
6. `workspace.close(force=false, expectedSourceStateDigest=D')` succeeded and the final commit remained recoverable.

Therefore:

```text
Current Host semantic checkpoint
+ Runtime exact sourceStateDigest fence
= sufficient correctness binding
```

A new structured Host dirty-disposition field may later be useful for queryability/scale, but is not a correctness primitive.

Responsibility remains:

```text
Runtime       = physical state, evidence, checkpoint carrier, compare-and-close
Host/Task/owner = semantic claimant + disposition
Git/artifact  = recoverability carrier
lifecycle     = execute an already-admitted physical action
```

## 5. Workspace-state carrier falsifiers

### F1 — pure unstaged unique state

`runtime-current-supply-chain-closeout-20260813` had two unstaged files with Index=HEAD. A zero-intrusion worktree carrier was written to:

```text
refs/ordivon/quarantine/workspace/runtime-current-supply-chain-closeout-20260813/worktree
  -> d671402e95ec78ec983cb2702eee10c1e242c6d6
```

The exact Runtime source-state digest did not drift; compare-and-close released the live Workspace. HEAD/index/worktree blobs remained reconstructable from source-repository refs.

### F2 — staged + unstaged + untracked

`harness-am2-am8-closeout-20260815` contained all three ordinary Git layers. Two carriers preserved the staging geometry:

```text
.../index    -> 243c3184a28ba4dc1a8a3e68cb9acfb7b043fd6b
.../worktree -> e4836c956ba28e86f1d91a6736e7ff7afb0cceb2
```

The worktree carrier was parented by the index carrier. Post-close reconstruction reproduced:

- staged-only transformation;
- unstaged-only transformations;
- untracked path presence.

### F3 — conflict boundary and correction

`final-closeout-runtime-stabilization-20260813` showed that a normal Git tree cannot represent an unmerged index. Exact raw index bytes plus stage 1/2/3 projections and a worktree tree preserved conflict *geometry*; immediate raw-index restoration was byte-exact, while the first `git status` refreshed index serialization without changing status/stage semantics.

Preserved evidence:

```text
.../bundle   -> 770238d771593f5ae392570a8e7e62ef6830d650
.../worktree -> 6e086576cb5021c885b72341ad34d725295330ab
```

However this experiment was closed before the later realization that merge/rebase/cherry-pick/sequencer continuation also depends on administrative metadata such as `MERGE_HEAD`. Therefore F3 supports **conflict-geometry preservation only**, not complete in-progress Git-operation recovery.

This correction directly narrowed production v1: it fails closed on unmerged index and in-progress Git operations rather than overclaiming recoverability.

## 6. Production capability: Runtime dirty-checkpoint v1

Canonical Runtime commit:

```text
f7600266c97aa9dd77dfb52873ad0c8f58f2f547
runtime: checkpoint dirty workspace state
```

The existing operator lifecycle now implements:

```text
dirty-review
-> dirty-checkpoint
-> owner disposition
-> workspace.get exact Runtime digest
-> workspace.close exact compare-and-close
```

`dirty-checkpoint`:

- is an operator physical-recovery command, not a new MCP authority;
- refuses active/held Jobs;
- requires the lifecycle candidate to remain `blocked_dirty`;
- creates immutable `refs/ordivon/checkpoints/<workspace>/<stateDigest>` in the source repository;
- preserves parent HEAD, raw index, stable stage/index projections, staged index tree, and complete tracked+nonignored-untracked worktree tree;
- leaves the live Workspace open and dirty;
- returns `automaticDeletionAllowed=false`;
- labels the manifest `physical-recovery-carrier-not-semantic-standing`;
- explicitly distinguishes its representation `stateDigest` from Runtime `sourceStateDigest`;
- is replay-convergent for the same logical Git state.

v1 fails closed on:

- sparse checkout;
- split index;
- submodule/gitlink state;
- unmerged index;
- in-progress merge/rebase/cherry-pick/revert/sequencer/bisect markers;
- non-file/non-symlink untracked path types.

## 7. Production dogfood

`security-pr27-operational-closeout-20260812` had no active Host claimant. `dirty-checkpoint` created:

```text
refs/ordivon/checkpoints/security-pr27-operational-closeout-20260812/
569eea5ec003faef2a533c79b8fa8b6c1658cd4f21a7b0ff39012c3697295ee2
  -> f9e8c8d4ff1ff3c181a4cec6b4782b2cf34759a4
```

The Runtime `sourceStateDigest` was identical before and after checkpoint. A replay returned the same stateDigest/ref/commit with `checkpointDisposition=existing`. After a fresh exact digest read, `workspace.close(force=true, expectedSourceStateDigest=...)` released the live Workspace. Post-close source-repo inspection confirmed `index.raw`, `index/`, `worktree/`, parent HEAD and manifest remained reachable.

This is a direct witness for:

```text
LiveDirtyWorkspace != OnlyCarrierOfUncommittedState
```

## 8. Current-pressure coverage

A post-deployment read-only applicability census observed 163 dirty Workspaces:

```text
SUPPORTED_V1   157
FAIL_CLOSED      6
```

Fail-closed reasons were:

```text
REBASE_HEAD                    1
CHERRY_PICK_HEAD + UNMERGED    1
SPECIAL_UNTRACKED              4
```

No current sample required sparse/split-index/gitlink handling. Thus v1 mechanically covers ~96% of the observed dirty population while preserving explicit failure for the remaining unsupported states.

This is not semantic cleanup coverage: a mechanically checkpointable Workspace still requires owner/currentness/disposition adjudication.

## 8A. Gate-discovered current-surface contraction

Computing T1 initially exposed two pre-existing canonical-base debts after the ambiguous staged root was resolved: one spelling-gate drift (`environmentalized`) and 17 executable experiment runners that were present in the current tree but bound to no `active`/`ready` research question. The runners were not registered as fake live work. Each had existing Git history/recoverability; they were removed from the current executable research surface under the existing C5 invariant. The wording was minimally repaired to `environment-shaping`.

This is a direct post-remediation witness that an ambiguous staged contraction can contain both unsafe rollback intent and valid contraction pressure. The original staged tree was therefore correct to quarantine rather than blindly commit, while later per-obligation adjudication could still recover and admit the earned deletions.

## 9. Validation and deployment

Runtime candidate validation:

```text
cargo build --workspace --all-features                  PASS
cargo test --workspace --all-targets --all-features     222 passed / 0 failed
python3 -m unittest discover -s scripts/tests -v         103 passed / 5 skipped
python3 scripts/check_docs.py                            PASS
scripts/local-acceptance check                           PASS
```

Canonical main and `origin/main` were guarded fast-forwarded to `f760026...`.

Receipted deployment:

```text
receipt: /var/lib/ordivon/deployments/20260826T191329Z-f7600266c97a
status: deployed
serviceActive: true
toolCount: 22
```

Post-deploy verification:

- installed lifecycle SHA-256 == canonical source lifecycle SHA-256 `df453a20...`;
- Runtime health = `healthy`;
- all 12 deployed artifacts match receipt digests/modes;
- installed `dirty-checkpoint --help` is live;
- canonical HEAD/main/origin all equal `f760026...`;
- stale dirty state remains maintenance `attention`, proving deployment did not add automatic deletion authority.

## 10. Method standing

The evidence earns a bounded extension of challengeable persistence:

```text
Preservation != unchanged survival
PreserveReachability != PreserveEmbodiment
```

A live environment, Workspace, branch, process, or representation can be retired while the load-bearing historical state remains reachable **if and only if** the relevant state has an adequate recovery carrier and current semantic authority is not inferred from that carrier.

Do not generalize this into a universal archival mechanism. Carrier adequacy is operation-relative: the ordinary Git-state bundle is sufficient for ordinary staged/unstaged/untracked state but not for every possible execution environment or in-progress protocol.

## 11. Rejected interpretations

- `dirty == active concurrent work`;
- `old dirty == redundant residue`;
- `checkpoint exists -> safe to delete`;
- `recoverable history -> current standing`;
- `sourceStateDigest -> content recovery`;
- age-only or automatic dirty force-close;
- Runtime inferring domain owner intent;
- a new Dirty-State ontology/owner/registry;
- a new Host schema field as a correctness prerequisite;
- claiming F3 proves full merge/rebase operation continuation;
- auto-checkpointing all dirty Workspaces merely because v1 coverage is high.

## 12. Remaining pressure

The major remaining problem is semantic-scale discoverability, not physical preservation: mapping a dirty Workspace to a current claimant/disposition is still awkward across many Host Tasks. Existing generic WorkingCheckpoint + Runtime exact fences are correct, but claimant lookup is not naturally bulk-queryable.

That should be reopened only as a discoverability/queryability pressure. It does not justify moving semantic disposition into Runtime.

Current backlog should therefore be reduced through bounded owner adjudication waves using `dirty-review -> dirty-checkpoint when required -> exact compare-and-close`, not by a blind global cleanup.
