# Dirty State Provenance v0 — Frozen Evidence

This is a source-fenced evidence bundle for adversarial review. It does not authorize cleanup.

```json
{
  "schemaVersion": 1,
  "kind": "ordivon.dirty-state-provenance-audit-v0",
  "sourceFences": {
    "computingMain": "797b519d013b5de3a03bce9a8bfa5f52a3dc5ef1",
    "mediaMain": "5fea691564f80304414ed057c273527d975cbdc4",
    "runtimeCurrent": "fd6765c20981461f1a29508d97225b96971cc389"
  },
  "runtimeBacklog": {
    "physicalOpen": 236,
    "dirty": 163,
    "olderThan24h": 160,
    "olderThan72h": 128,
    "olderThan168h": 77,
    "olderThan336h": 37,
    "ageBinsDerived": {
      "lt24h": 3,
      "1to3d": 32,
      "3to7d": 51,
      "1to2w": 40,
      "gt2w": 37
    },
    "workspaceBytes": 4671658982,
    "maintenanceReason": "STALE_DIRTY_WORKSPACES",
    "defaultStaleDirtyHours": 168
  },
  "runtimePolicy": {
    "autoRemoval": "dirty/active/pinned/unknown/orphan-directory cases are excluded from automatic lifecycle removal",
    "closeDefault": "workspace.close refuses dirty unless force=true",
    "sourceStateDigest": "exact physical source-state commitment over current HEAD/index/tracked/untracked bytes and modes",
    "forceCloseRecoverability": "final HEAD may receive rescue ref; uncommitted/untracked bytes are not converted into a recoverable commit by force close; digest alone is not content recovery"
  },
  "hostCurrentRuntimeCheckpointFields": [
    "workspaceId",
    "relevantJobIds",
    "observedHeadRevision"
  ],
  "canonicalRoots": {
    "media": {
      "staged": 15,
      "unstaged": 0,
      "untracked": 0,
      "indexTree": "2d8e6168ef7e7b1f833d8dee883eec29e7f4ae3d",
      "exactCommitTreeMatch": false,
      "classificationEvidence": "staged temporal mosaic: Chapter 2/3/4 index blobs equal Aug24-era blobs, Chapter5/claims/cognition/etc equal Aug25-era blobs, production/source-map equal Aug25 20:42-era blobs, while later-admitted Chapters 6/7 are staged deleted. A WIP ref e978d4b preserved an earlier staged state, but the present index is not that commit tree either.",
      "wipRef": "e978d4bc5c9205434db8d2fdc2eae88520f76b1d",
      "latestKnownRootFileMtime": "2026-08-25T20:42:47+08:00"
    },
    "computing": {
      "staged": 86,
      "unstaged": 0,
      "untracked": 0,
      "indexTree": "bd1ac3b4ba0dd8f5fff0f6e9cbc5cfb7f4f06f74",
      "approxDeletedLines": 43765,
      "classificationEvidence": "staged temporal rollback/contraction candidate: capability assimilation + Method Canon blobs exactly revert to 97262c5; J1 closeout/result revert to 90b7bc3; many later research surfaces are staged deleted. Independent discoverability audit records ConcurrentStagedIntent=UNKNOWN_UNTIL_COMMITTED/RESOLVED."
    }
  },
  "workspaceSamples": [
    {
      "id": "rep-capability-formalization-ws1-20260825",
      "repo": "ordivon-computing",
      "shape": "4 untracked research/probe files",
      "lastOriginalActivity": "2026-08-25",
      "semanticDisposition": "unknown"
    },
    {
      "id": "cojc-continuity-phase1-harness-20260825",
      "repo": "ordivon-harness",
      "shape": "21 untracked experimental runner files",
      "lastOriginalActivity": "2026-08-25",
      "semanticDisposition": "unknown; later Book/continuity work exists"
    },
    {
      "id": "representation-witness-scan-media-20260824",
      "repo": "ordivon-media",
      "shape": "2 modified files README.md + tests/test_agent_surface.py",
      "lastOriginalActivity": "2026-08-24",
      "currentMainRelation": "README exact old f695cf4 blob; test file differs current main and had no exact blob history match",
      "semanticDisposition": "partly superseded/partly unique unknown"
    },
    {
      "id": "finance-owner-world-flow-coverage-20260824",
      "repo": "ordivon-finance",
      "shape": "22 mixed modified+untracked code/schema/tests",
      "lastOriginalActivity": "2026-08-24",
      "currentMainRelation": "many paths evolved/differ; some old untracked paths absent from current main",
      "semanticDisposition": "could be abandoned prototype, partial lineage, or unique evidence; cannot infer from age"
    }
  ],
  "existingTheoryGuards": [
    "historical occurrence != current presence",
    "HistoricalValidity != Currentness",
    "semantic successor recovered != currentness proved",
    "retain history without lifting it into current authority",
    "responsibility-preserving reactivation: recover current load-bearing premises from owners, retain history, preserve unresolved effects/obligations, recompile next affordance",
    "preservation/sedimentation should remain challengeable and deletable rather than unchanged survival"
  ],
  "candidateDistinctions": [
    "Dirty != Active",
    "Staged != CurrentIntent",
    "PreservedBytes != PreservedClaim",
    "DigestPreserved != ContentRecoverable",
    "HistoricalValidity != CurrentClaimant",
    "CannotAutoDelete != MustRemainSemanticallyAmbiguousForever",
    "RootDirty != WorkspaceDirty",
    "Preservation != Sedimentation",
    "WorkspaceExistence != TaskContinuity"
  ],
  "candidateClasses": [
    "ACTIVE_DIRTY",
    "REVIEW_CANDIDATE",
    "RECOVERABLE_RESIDUE",
    "UNCOMMITTED_UNIQUE_EVIDENCE",
    "TEMPORAL_MOSAIC",
    "AMBIGUOUS_CLAIMANT"
  ],
  "candidateResponsibility": "Runtime owns physical facts/fences; Task/Host/domain owner decides semantic disposition; Git/artifacts provide recoverability; lifecycle executes close only after disposition + exact physical fence."
}
```

## External baseline

Git mechanically separates HEAD/index/worktree/untracked state and normally refuses removal of dirty linked worktrees without force. Git state does not encode current semantic claimant or owner intent. Ordivon Runtime deliberately strengthened the loss-prevention side by excluding dirty/active/unknown workspaces from automatic lifecycle deletion.
