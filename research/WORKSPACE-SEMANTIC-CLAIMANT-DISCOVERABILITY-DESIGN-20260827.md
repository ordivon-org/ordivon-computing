# Workspace Semantic Claimant Discoverability — bounded design / preregistration v0

Date: 2026-08-27
Status: DESIGN FROZEN FOR BOUNDED FALSIFICATION; NO PRODUCTION INTERFACE ADMITTED
Owning programme continuity: `task:workspace-semantic-claimant-discoverability-20260827`
Computing source fence at design start: `4d56268b0141c07a14fab2461d68e337f4fb4c08`
Host source fence: `b40c7e6a56011dad3ccb595b332ab0edf9fa200a`
Runtime source fence: `f7600266c97aa9dd77dfb52873ad0c8f58f2f547`
Atlas owner-coverage work was concurrently advancing during design; any Atlas-assisted trial MUST re-fence current Atlas source immediately before execution rather than inheriting a stale commit from this note.

## 0. Decision target

The target is NOT a global claimant registry and NOT a new Runtime lifecycle state.

The decision target is narrower:

> Starting from one exact Runtime Workspace identity, can an Agent cheaply recover the current Host continuity records that explicitly name that Workspace, distinguish active references from terminal/history-only references, then route to the correct physical and owner/currentness authorities without inventing semantic claimant certainty?

The design must also determine whether queryability is even the dominant limitation. A perfect reverse query is insufficient if current Task checkpoints do not carry current Workspace navigation hints.

## 1. Already-established boundaries

The following are treated as fixed unless falsified by current source:

1. Runtime owns physical Workspace truth: existence, source repository, current head, dirty state, source-state digest, active Jobs, and exact close fences.
2. Host owns Host Task continuity and exact Task revision. `WorkingCheckpoint` has truth role `semantic-working-claim`.
3. `WorkingCheckpoint.runtime.workspaceId` is an OPTIONAL physical navigation hint. Host documentation explicitly says it is not copied Runtime truth and must be revalidated with Runtime.
4. Owner/domain repositories own semantic standing and domain authority.
5. Atlas may expose non-authoritative owner/source/coverage projections, but Atlas must not mint owner truth or Workspace claimant truth.
6. Workspace existence does not imply current semantic claim.
7. A Task reference to a Workspace does not imply that Workspace is still physically current or that the Task is the unique semantic claimant.
8. `recoverable != current != claimed != valuable != safe-to-delete`.
9. Absence of an explicit Host relation is NOT proof that no semantic claimant exists.

## 2. Live pressure snapshot captured during design

A read-only scan of current Host task heads and Runtime physical Workspace directories produced the following observed snapshot during this design session:

- Host Tasks: 1051 total.
- Host states: 977 completed, 39 cancelled, 35 ready.
- Current Task heads carrying a `runtime.workspaceId`: 526 total.
- Unique Workspace identities referenced by current Task heads: 346.
- Workspace identities referenced by more than one current Task head: 59.
- Maximum current-head fan-in observed: 23 Tasks for one historical Workspace.
- READY Tasks carrying a Workspace hint: 27 / 35.
- Runtime physical Workspace directories observed: 241.
- Current physical Workspaces with ANY current-head Host reference: 32.
- Current physical Workspaces with a READY-Task current-head reference: 8.
- Current physical Workspaces with terminal-head references only: 24.
- Current physical Workspaces with no current-head Host reference: 209.
- READY Task → Workspace hints that still pointed to an observed current Workspace: 8.

This is not yet a semantic ground-truth census. It is a mechanical relation census.

The first major design consequence is therefore:

`Reverse queryability` and `binding currentness/completeness` are separate variables.

A reverse query can be exact over the Host records and still be an incomplete answer to the wider semantic-claimant question.

## 3. Relation vocabulary

No candidate may collapse the following relation classes.

### R0 — Runtime physical existence

`R0(w)` means Runtime currently projects Workspace `w` as a physical Workspace candidate / exact Workspace state.

Authority: Runtime only.

### R1 — current explicit Host navigation reference

For Task `t` at current Host revision `r_t`:

`R1(t,w) := latest_checkpoint(t, r_t).runtime.workspaceId == w`

This means only:

> the exact current Host WorkingCheckpoint for `t` explicitly carries `w` as its Runtime navigation hint.

It does NOT mean Runtime says `w` exists, that `w` is current, or that owner truth agrees.

### R1-ready

`R1_ready(t,w) := R1(t,w) AND HostTaskState(t) is non-terminal/READY`

This is the strongest mechanically derivable current Host relation available without another authority.

It is still a Host semantic-working-claim relation, not domain truth.

### R1-terminal

`R1_terminal(t,w) := R1(t,w) AND HostTaskState(t) is terminal`

This is useful historical/recovery evidence. It must never be rendered as a current claimant merely because the terminal checkpoint still names the Workspace.

### R2 — physically current Host navigation reference

`R2(t,w) := R1_ready(t,w) AND Runtime currently confirms w exists`

No single system owns this relation. It is a caller-side composition of Host continuity and Runtime physical truth.

### R3 — semantic claimant candidate

A Task becomes a semantic claimant candidate only after R1/R2 plus task objective/frontier and relevant owner/currentness evidence support a live responsibility relation.

R3 cannot be minted by Runtime, by Workspace naming, by age, by Atlas coverage, or by a Host reverse index alone.

### R4 — owner route

`R4(w,o)` means Runtime sourceRepo plus current owner/source representation identifies `o` as the relevant owner candidate / authority route for further adjudication.

Atlas may help discover R4, but Atlas output remains non-authoritative unless the underlying owner publication/source is independently current.

### Negative states

The system must distinguish:

- `NO_CURRENT_HOST_REFERENCE`: no R1-ready relation found.
- `TERMINAL_REFERENCE_ONLY`: one or more R1-terminal relations, no R1-ready.
- `EXPLICIT_REFERENCE_PHYSICALLY_ABSENT`: R1-ready exists but Runtime does not currently expose the referenced Workspace.
- `EXPLICIT_REFERENCE_PHYSICALLY_CURRENT`: R2 exists.
- `SEMANTIC_CLAIMANT_UNKNOWN`: no sufficient R3 adjudication yet.

Critically:

`NO_CURRENT_HOST_REFERENCE != PROVEN_UNCLAIMED`.

## 4. Competing explanations

The experiment is designed to discriminate these hypotheses rather than to validate a preferred API.

### H0 — no material defect

Manual recovery is rare enough and cheap enough that no additional projection is justified.

### H1 — queryability is the main defect

The needed relation already exists in current WorkingCheckpoints. The problem is simply that Host exposes it only Task→Workspace, forcing an Agent starting from Workspace to enumerate and resume many Tasks. A read-only reverse filter is sufficient.

### H2 — binding currentness/completeness dominates

Even perfect reverse lookup has low practical value because active Tasks often carry stale/closed Workspace hints or no relevant Workspace hint at all. The correct repair would be checkpoint/currentness discipline, not a reverse API.

### H3 — owner routing dominates after Host recovery

The Agent can find a Task but still cannot naturally determine the authoritative owner/currentness path. Atlas owner coverage or another owner-native representation provides the deletion-essential improvement.

### H4 — caller-side composition is already sufficient

Harness/Agent orchestration can join Host + Runtime + Atlas cheaply enough that changing Host is unnecessary.

### H5 — a durable reverse index is required

On-demand derivation is too expensive or non-deterministic at current scale, forcing new durable index state.

H5 is deliberately the hardest hypothesis to admit.

## 5. Candidate mechanisms

### C0 — current manual baseline

Typical active-continuity path:

1. Runtime `workspace.get(w)` or `workspace.list` locates the physical Workspace.
2. Host `task.list()` retrieves nonterminal continuity inventory.
3. Caller performs `task.resume` / `task.observe` across plausible Tasks until matching `checkpoint.runtime.workspaceId` is found.
4. Caller revalidates Runtime and owner/domain truth separately.

Strength: no new code.
Weakness: reverse lookup cost leaks into every Agent.

### C1 — Host-derived reverse filter (preferred first falsifier, not yet admitted)

Extend existing `task.list` with OPTIONAL `workspaceId` query scope rather than add a seventh Host Tool.

Intended semantics:

- filter only external-continuity Tasks whose exact current WorkingCheckpoint has `runtime.workspaceId == workspaceId`;
- default still excludes terminal Tasks;
- `includeTerminal=true` may expose terminal-head references separately;
- cursor identity must include `workspaceId` so cursors fail closed across query-scope change;
- output remains TaskProjection + bounded semantic summary;
- output should add an explicit relation/truth-boundary description such as `workspaceReferenceTruthRole = current-working-checkpoint-runtime-navigation-hint`;
- no Runtime call occurs inside Host;
- no owner lookup occurs inside Host;
- no durable reverse index is created in v0.

Why `task.list` rather than `task.claimants`:

- `task.claimants` overstates the semantic strength of the relation;
- the primitive is still a filtered continuity inventory;
- an optional filter preserves the six-tool Host surface and existing responsibility boundary.

### C2 — Atlas owner-assisted lookup

Starting from Runtime `sourceRepo`, query current Atlas owner coverage/source representation to find registered owner, owner candidate, deferred owner, non-owner or special-review state.

C2 is NOT a substitute for C1. It answers a different question: where should owner/currentness adjudication continue?

### C3 — Harness/Agent on-demand join

Do not modify Host. Compile C0 into a reusable caller operation that enumerates current Host Tasks, fetches relevant checkpoints and performs Runtime/Atlas routing.

C3 wins if it matches C1 cost and reliability without creating a new Host query shape.

### C4 — composed first interface

If earned, the user-facing operation is conceptually:

`Workspace -> Runtime physical proof -> Host explicit-reference lookup -> exact Task resume -> owner route -> owner/currentness adjudication`

This may later be environmentalized by Harness, but each constituent authority remains separate.

### C5 — durable claimant/link graph

Not admitted in v0.

C5 may be reconsidered only if C1 on-demand derivation fails a measured latency/scale requirement or a natural case requires relations that cannot be reconstructed from authoritative source planes.

## 6. Mechanical oracle

The experiment's first oracle is intentionally narrower than semantic truth.

For every current Host Task head, source-fenced read-only code reconstructs the exact current WorkingCheckpoint and extracts its optional runtime Workspace hint. This yields the oracle set:

`O_host(w) = { exact current TaskProjection t | R1(t,w) }`

C1/C3 must match this oracle exactly.

This oracle is appropriate for testing reverse query correctness because it does not require subjective semantic claimant labeling.

It is NOT sufficient to label R3.

## 7. Benchmark strata

Freeze cases before candidate result inspection.

### S1 — live positive / READY + physical current

All or a bounded deterministic sample of Workspaces with at least one R1-ready and current physical existence.

Current design snapshot contained 8 such Workspaces.

Purpose: positive exact-recovery control.

### S2 — terminal-only physical Workspaces

Sample current physical Workspaces whose current-head Host references are all terminal.

Current snapshot contained 24.

Purpose: prevent historical-reference→current-claimant collapse.

### S3 — READY reference to physically absent Workspace

Sample READY Tasks whose current checkpoint carries a Workspace hint but Runtime no longer exposes that Workspace.

Purpose: test binding currentness/staleness and prove Host must not silently validate Runtime.

### S4 — current physical Workspace with no current-head Host relation

Sample recent and old cases across multiple source repos.

Purpose: test the critical negative boundary: no explicit Host relation does not prove semantic unclaimed state.

### S5 — high-fan-in historical Workspace

Sample Workspaces referenced by many terminal current Task heads.

Purpose: pagination, bounded result and history/claimant separation.

### S6 — owner-unknown / cross-owner routing

Choose cases where Workspace identity alone does not reliably reveal the owner or where repository/institutional owner differs from research-owner registration.

Purpose: measure the marginal contribution of Atlas owner coverage.

### S7 — no relation negative control

Current physical Workspace selected before candidate execution with no Host current-head reference and no evidence that the benchmark designer manufactured a Task relation.

Purpose: candidate must return uncertainty, never fabricated claimant truth.

## 8. Semantic adjudication subset

A smaller blinded subset is required to test whether R1/R2 actually helps real owner/disposition work.

For each selected Workspace:

1. freeze Runtime workspace identity/sourceRepo/head/digest;
2. freeze Host current reverse-reference result independently;
3. read exact Task objective/frontier only after relation selection;
4. recover owner/currentness evidence from current owner source / Atlas source representation;
5. classify only one of:
   - CURRENT_SEMANTIC_CLAIM_SUPPORTED,
   - HISTORICAL_REFERENCE_ONLY,
   - TASK_CONTINUITY_OPEN_BUT_WORKSPACE_REFERENCE_STALE,
   - NO_EXPLICIT_CURRENT_CLAIM / OWNER_ADJUDICATION_REQUIRED,
   - MULTIPLE_CANDIDATES_REQUIRE_ADJUDICATION,
   - UNKNOWN.

No benchmark label may use Workspace filename semantics as ground truth.

## 9. Metrics

### M1 — exact Host relation precision / recall

For the mechanical oracle O_host:

- precision = 1.000 required;
- recall = 1.000 required;
- any mismatch blocks production admission.

Because C1 is a deterministic projection over Host's own state, approximate retrieval is unacceptable.

### M2 — false semantic promotion

Count cases where candidate output or consumer interpretation incorrectly converts:

- terminal reference into current claimant;
- absent reverse result into `unclaimed`;
- Host navigation hint into Runtime currentness;
- Atlas owner coverage into owner semantic truth.

Required: zero in protected benchmark cases.

### M3 — remote operation cost

Measure number of externally visible Host/Runtime/Atlas calls needed to reach the exact same bounded evidence cut.

C1 promotion target: >= 80% reduction versus C0 on the selected lookup cohort, without losing evidence.

Expected shape for a positive current case:

- C0: `workspace.get + task.list + N task.resume/observe`;
- C1/C4: `workspace.get + task.list(workspaceId) + targeted task.resume + owner route if needed`.

### M4 — context/payload cost

Measure total structured payload bytes or equivalent model-facing context consumed before exact candidate Task identity is available.

Promotion target: >= 60% reduction on median positive lookup versus C0.

### M5 — service-local derivation latency

A design-time raw read-only scan of all 1051 current Host Task heads measured ~43 ms median hot-path after one cold iteration; the first iteration was ~275 ms.

This is only an engineering feasibility witness, not production latency.

C1 v0 therefore MUST attempt on-demand derivation first. A durable index is forbidden unless source-level prototype measurements under the actual Host implementation show unacceptable bounded latency at current scale.

### M6 — binding-currentness coverage

For READY Tasks with Workspace hints, measure fraction whose hinted Workspace remains physically current; separately measure sampled live semantic work whose current Workspace is absent from current checkpoint representation.

This metric decides H1 vs H2.

C1 must not be described as a complete claimant solution if binding-currentness coverage is poor.

### M7 — disposition utility

In at least one real bounded lifecycle/owner-adjudication wave, measure whether the candidate:

- avoids manual Task scans;
- prevents an unsafe `unclaimed` inference;
- identifies stale navigation needing rebind;
- enables a correct close/preserve/review decision faster;
- or produces NO_CHANGE.

A purely cosmetic API with no real consumer value does not earn broader environmentalization.

## 10. Promotion / deletion gates

### Gate G0 — semantic naming

Pass only if the candidate representation clearly names its truth role as explicit current Host checkpoint reference / navigation hint. If the representation naturally induces `Host says this Task owns this Workspace`, reject or rename it.

### Gate G1 — deterministic exactness

M1 must be 100% precision and recall across the frozen current-head oracle.

### Gate G2 — protected safety

M2 must be zero across S2/S3/S4/S7.

### Gate G3 — queryability gain

M3 >= 80% call reduction and M4 >= 60% context reduction on the benchmark cohort.

If not, C1 is deleted and C0/C3 remains.

### Gate G4 — no durable index

If on-demand derivation is bounded at current scale, durable indexing is rejected.

Only a measured scale/latency failure may reopen C5.

### Gate G5 — binding sufficiency

If current semantic claimant cases frequently lack current R1-ready representation, classify C1 as QUERYABILITY_ONLY and open a separate binding-currentness repair question. Do not widen the query surface to hide missing capture.

### Gate G6 — owner contribution

Atlas is added to the ordinary path only if S6 shows it materially reduces owner/currentness recovery failure or cost. Otherwise owner route stays targeted and owner-native.

### Gate G7 — production admission

A Host production change requires all of:

- G0–G4 pass;
- at least one real recurring consumer (dirty backlog, owner recovery, first-interface, or equivalent) demonstrates M7 utility;
- full Host regression/integrity passes;
- no new durable schema/state;
- no Runtime/Atlas semantic authority leakage.

## 11. Candidate C1 response semantics

A possible result shape, purely illustrative until engineering validation:

```json
{
  "schemaVersion": 3,
  "kind": "ordivon.host-task-list",
  "scope": "external-continuity",
  "query": {
    "workspaceId": "example-workspace",
    "workspaceRelation": "current-working-checkpoint-runtime-navigation-hint"
  },
  "tasks": [
    {
      "projection": {"taskId": "task:...", "revision": 7, "state": "ready"},
      "semanticSummary": {"checkpointRevision": 7, "checkpointDigest": "sha256:..."},
      "workspaceReference": {
        "workspaceId": "example-workspace",
        "truthRole": "semantic-navigation-hint-only",
        "runtimeCurrentnessValidated": false,
        "ownerTruthValidated": false
      }
    }
  ],
  "interpretation": "matching current Host checkpoint references only; empty result does not prove that the Workspace is semantically unclaimed"
}
```

The exact wire schema must be minimized after experiment; this is not a preregistered requirement to add all fields shown.

## 12. Cursor compatibility design

If `workspaceId` is added to `task.list`, cursor query identity must bind it.

Preferred implementation path:

- extend cursor payload with nullable `workspaceId` in a new cursor version;
- continue accepting existing v1 cursors only for queries with no workspace filter;
- filtered queries emit the new cursor form;
- reusing a cursor under another Workspace fails closed.

Do not silently reinterpret old cursors.

## 13. Why Host is the first candidate owner of the reverse relation

The reverse relation being queried is already encoded inside Host's own current WorkingCheckpoint object. Host can truthfully answer:

> Which current Host checkpoints explicitly reference Workspace W?

Host cannot truthfully answer without other authorities:

> Which Task/domain truly owns W right now?

This is exactly why C1 belongs in Host while R2/R4 remain caller-composed.

## 14. Why Runtime should not own the relation

Runtime can observe physical Workspace identity and Jobs. It cannot infer semantic claimant from:

- open/dirty/old state;
- branch name;
- source repo;
- Job history;
- force-close eligibility;
- checkpoint recoverability.

Moving claimant semantics into Runtime would reverse the successful dirty-state responsibility split.

## 15. Why Atlas should not own the relation

Atlas can make owner/source topology discoverable and can represent deferred/candidate/non-owner state without centralizing authority.

But Workspace→Task continuity is not primarily an Atlas research-source relation. Atlas is useful after Runtime supplies sourceRepo or after a Task identifies an owner source; it should not become a live Workspace claim registry merely because it is good at cross-owner representation.

## 16. Why Harness should not persist the relation

Harness may compile the multi-tool recovery path for Agent ergonomics. It should not become the durable owner of Host checkpoint↔Runtime Workspace identity. If C3 needs to persist its own claimant graph to be useful, that is evidence of responsibility drift rather than success.

## 17. Historical-approximation interpretation

This programme is a natural successor case for the already-closed Historical Approximation Re-adjudication lens.

Historical pressure:

- Runtime and Host originally lacked the present exact continuity/currentness boundaries;
- callers therefore recovered Task↔Workspace relations manually and treated Workspace names / remembered context as temporary glue.

New capability:

- exact Task revisions;
- bounded WorkingCheckpoint;
- exact Runtime Workspace identity and sourceStateDigest;
- owner/source currentness discipline;
- Atlas non-authoritative coverage.

Candidate obsolete coupling:

`Workspace-started investigation -> scan many Tasks / rely on remembered context`

The experiment asks whether this coupling has lost existence right now that an exact derived reverse projection is feasible.

The historical programme itself remains closed; no new Historical Approximation theory is created.

## 18. Stop conditions

Stop with NO_CHANGE if any of the following is observed:

1. manual reverse recovery is not materially expensive on real consumers;
2. C1 fails to reduce calls/context materially;
3. current link capture is so incomplete that reverse filtering creates misleading apparent completeness and no bounded binding repair is justified;
4. caller-side C3 matches C1 without responsibility drift;
5. Atlas assistance adds no owner-routing benefit;
6. production semantic naming cannot avoid claimant overstatement.

Stop with QUERYABILITY_ONLY if C1 passes but H2 remains strong.

Open a separate Binding Currentness task only if natural semantic claimant cases repeatedly demonstrate missing/stale checkpoint Workspace bindings and a bounded capture repair can be tested without turning WorkingCheckpoint into a Runtime graph.

## 19. Immediate execution sequence

1. Freeze the mechanical oracle implementation against current Host source.
2. Materialize deterministic S1–S7 manifest from a single observation fence.
3. Run C0 baseline call/context accounting.
4. Prototype C1 inside an isolated Host Workspace only; no deployment.
5. Compare C1 exactly against oracle.
6. Run S2/S3/S4/S7 protected interpretation tests.
7. Re-fence current Atlas owner coverage and run S6 marginal-value test.
8. Run one real backlog / owner-adjudication consumer wave.
9. Decide one of: NO_CHANGE, QUERYABILITY_ONLY, HOST_FILTER_ADMIT, CALLER_COMPOSITION_ONLY, BINDING_CURRENTNESS_REOPEN.
10. Only then consider canonical Host/Computing sedimentation.

## 20. Current design standing

The design currently favors the following minimal architecture, subject to falsification:

`Runtime workspace.get`
→ exact physical Workspace/sourceRepo

`Host task.list(workspaceId=W)`
→ exact current Host checkpoint references only

`Host task.resume(expectedRevision=R)`
→ bounded semantic working claim

`Atlas / owner-native source`
→ owner/currentness route where needed

`owner/domain adjudication`
→ actual semantic claimant/disposition

No component is allowed to silently promote the previous component's evidence into stronger truth.
