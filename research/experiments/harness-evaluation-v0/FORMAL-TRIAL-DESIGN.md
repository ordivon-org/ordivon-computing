# Host–Harness–Runtime Formal Trial Design

Status: designed, not executed.

This document defines the first formal Track R campaign for the current Ordivon Host, Harness, and Runtime. It is an execution design, not a product-quality result. No live Provider Trial is claimed by this document.

## Decision summary

The first formal Trial program is not one benchmark and does not assign one score to Host, Harness, and Runtime.

It separates four claims:

| Claim | Primary owner | What is tested | What is not inferred |
|---|---|---|---|
| Harness capability | Harness | whether one model–Tool loop completes the frozen Task, stops correctly, retains evidence, and recovers bounded failures | Host correctness or Runtime process safety from acceptance rate alone |
| Host semantic integrity | Host | whether Task, Attempt, Assignment, CompletionProposal, verifier decision, and TaskOutcome remain exact across rejection, restart, and replay | model quality or physical process completion |
| Runtime physical reliability | Runtime | whether Workspace, Job, Attempt, request identity, process tree, terminal evidence, reconciliation, and closure remain exact | semantic Task completion |
| Cross-layer continuity | Host + Harness + Runtime | whether one real Task can be reconstructed from durable identities without duplicate work or false completion | a universal ranking or production-readiness claim |

The first campaign therefore runs:

1. current component acceptance gates once;
2. one deterministic cross-layer smoke Trial;
3. three repeated live Ordivon Harness Trials on `HARNESS-REPO-REPAIR-001`;
4. five bounded fault cells that isolate Host, Harness, Runtime, and cross-process recovery;
5. trajectory review for every failure and anomalous success.

One-shot and mature Provider Harness comparisons follow only after this runner and evidence path are proven. Building all three paths before the first native baseline would mix runner defects, Provider differences, tool-contract differences, and component failures.

### Execution prerequisite

The campaign design is retained, but execution is blocked by [`../observation-plane-v0/P0-P1-DESIGN.md`](../observation-plane-v0/P0-P1-DESIGN.md). P0 must first make Host and Harness independently durable without dual-writing new Runs. The Host/Harness/Runtime portion of P1 must then automatically export owner-native evidence into a queryable non-authoritative observation path. R3 resumes only after one deterministic cross-owner trajectory can be reconstructed from native references without assuming Harness state lives in Host CAS.

## Audited starting point

The design was derived from these clean local revisions:

| Component | Observed revision | Relevant current surface |
|---|---|---|
| Computing | `d1b351168e43013adccb1828345a251bb9095023` | Track R schemas, Suite, validators, query tool |
| Host | `1a4027bb26d77a2e051ca933bf664578f071a5a9` | Task continuity, admission, verifier decision, TaskOutcome, live read acceptance |
| Harness | `796e9f07899a250ea4d87ae3e96f38c7172ff674` | native DeepSeek loop, Provider adapters, Tool steps, snapshots, recovery, completion proposals |
| Runtime | `ce061a5995d7a59246a103dcc51f0539245209a6` | Workspace, Job, Attempt, systemd/cgroup supervision, terminal evidence, reconciliation |
| Protocol dependency | `420dc356cb664d75db0f34f356156baebe5843db` | exact Host and Harness dependency pin |

These are design inputs, not permanently selected execution revisions. Campaign start captures a new complete System Manifest. Any source, Provider, model, Adapter, prompt, Context, Tool catalog, Tool grant, budget, environment, or verifier change creates a new configuration identity.

### Frozen Task provenance

`HARNESS-REPO-REPAIR-001` remains usable as Task version 1.

Its Task Definition binds historical Host revision `b4bc43a4ea7eb1e7771644d507bc4a3a39b4e741` and fixture path `fixtures/harness-replacement-repository-repair-v1`. That revision is still present locally. The four fixture files at that historical revision are byte-identical to the extracted Harness copies:

- `SPEC.md`;
- `allocation.py`;
- `test_allocation.py`;
- `artifacts/.gitkeep`.

The Task QA already proves three clean rebuilds with complete agreement:

- baseline fails visible and hidden verification;
- oracle passes visible and hidden verification;
- floor-only implementation fails both;
- visible-suite overfit passes visible verification and fails the hidden verifier.

The formal runner must construct the Workspace from the exact historical Host revision, not copy an arbitrary current fixture directory without proving the bound digest.

## What counts as a formal Trial

A formal Trial is one exact Task execution under one complete configuration. It has all of the following:

1. a validated Task Definition and QA receipt;
2. one complete System Manifest for the configuration;
3. one fresh initial Workspace constructed from the Task source revision;
4. one isolated Host state root unless the cell deliberately tests restart or continuation;
5. one Task, Task Attempt, current Assignment, and Harness Run identity;
6. every Runtime Job correlated to the exact Task, Attempt, Assignment, and Harness Run;
7. a Provider and model identity captured without secrets;
8. an independent verifier outside the model-visible Workspace;
9. a Host CompletionDecision and, only on acceptance, one TaskOutcome;
10. a Track R Trial Manifest, Trial Result, and Failure Records where required;
11. verified Workspace closure or an explicit retained-state reason;
12. no raw private reasoning and no credential material in committed evidence.

A process exit, model final message, Harness stop, Runtime success, visible test pass, or completion Artifact alone is not formal acceptance.

## Claim-specific verdicts

Every campaign produces separate verdicts.

### Component gate verdict

A component gate says only that the exact source and current supported acceptance path passed.

- Host gate: deterministic suite plus one current read-only Host→Runtime journey.
- Harness gate: deterministic suite, wheel smoke, network-free scripted loop, and current H2 Host→Harness→Runtime journey.
- Runtime gate: portable suite plus the explicit root/systemd/cgroup local acceptance and MCP end-to-end receipt.

Component gate receipts are captured once per exact campaign manifest. They are not rerun before every stochastic Trial and are not counted as model successes.

### Trial acceptance verdict

A repository-repair Trial is accepted only when all are true:

- visible tests pass;
- hidden tests pass;
- `SPEC.md` and `test_allocation.py` are unchanged;
- no path outside `allocation.py` and `artifacts/` changed;
- `artifacts/completion.json` exists and validates;
- the Runtime terminal evidence is conclusive and process-tree clean;
- the Host verifier decision is accepted;
- exactly one TaskOutcome is committed;
- the disposable Workspace closes successfully.

### False-completion verdict

`falseCompletion` is true when the model or Harness proposes candidate completion but the independent verifier or Host rejects it. A physically successful Runtime Job with a missing Artifact or incorrect source is a false-completion case when a completion claim was made; it is not Runtime failure.

### Recovery verdict

Recovery passes only when the same durable work is reconstructed without a second physical dispatch, stale Assignment admission, duplicate TaskOutcome, hidden state guess, or loss of required evidence.

## Campaign phases

## Phase 0 — complete campaign preflight

Run once against exact clean revisions.

### Required source gates

- Computing full conformance gate;
- Host `scripts/local-acceptance run` with a retained receipt;
- Harness `scripts/local-acceptance run` with a retained receipt;
- Runtime `scripts/local-acceptance run` with a retained receipt;
- Harness Task QA for `HARNESS-REPO-REPAIR-001`;
- clean Git status for every source repository;
- exact dependency and executable versions;
- Runtime health, protocol lifecycle, installed binary digest, and Tool catalog digest;
- no unrelated active Runtime Jobs occupying the selected trial Workspace or capacity.

### Complete System Manifest requirement

The P0 System Manifest intentionally contained unavailable Provider and configuration fields. R3 cannot reuse it.

Each competitive configuration receives a complete manifest containing:

- Host, Harness, Runtime, Computing contract, and Protocol revisions;
- installed Runtime binary and current Tool catalog identity;
- Provider ID, model ID, model revision when exposed, and Adapter revision;
- prompt-set digest;
- Context-policy digest;
- Tool-catalog digest;
- Tool-grant digest;
- budget-profile digest;
- environment digest;
- Task, verifier, Suite, and schema digests;
- privacy declaration excluding secrets and raw reasoning.

A changed manifest creates another configuration group. Results from different manifests are not silently pooled.

## Phase 1 — deterministic integrated smoke

Run one Trial with a scripted deterministic adapter before spending Provider budget.

The smoke must exercise the same formal runner path used by live Trials:

```text
frozen Task
→ exact Runtime Workspace
→ Host Task + Attempt
→ current Assignment
→ Harness Run
→ Runtime Tool calls
→ completion Artifact
→ hidden verifier
→ Host CompletionDecision
→ TaskOutcome
→ Trial/Result projection
→ Workspace close
```

The scripted adapter may use known oracle actions, but its result is marked `competitive=false`. It proves the runner and evidence join, not Agent capability.

Smoke failure blocks all live Trials.

## Phase 2 — first repeated live baseline

Run three sequential Trials with the current native Ordivon Harness and one exact DeepSeek configuration.

Default development candidate:

- Provider: DeepSeek;
- model: `deepseek-v4-flash` unless the execution manifest intentionally selects another supported model;
- Harness path: current `HarnessRunner` plus native `DeepSeekTurnAdapter`;
- Runtime profile: owner-trusted local profile selected by the runner;
- Task: `HARNESS-REPO-REPAIR-001` version 1;
- verifier: `HARNESS-REPO-REPAIR-001-verifier` revision 1;
- maximum model calls: 8;
- maximum Tool calls: 20;
- maximum Runtime Jobs: 8;
- maximum wall time: 600,000 ms;
- no concurrent Trials.

Every Trial receives:

- a new Runtime Workspace from the exact historical source revision;
- a new Host state root;
- a fresh Provider Session or API conversation;
- the same prompt, Context policy, Tool catalog, Tool grant, budget, sampling configuration, verifier, and environment;
- a distinct Trial ID and request identities.

Three Trials establish development evidence only. They do not support a general model ranking or final architecture decision.

## Phase 3 — comparative development cells

This phase begins only after Phase 2 produces valid records and the runner survives failure review.

### Cell A — one-shot DeepSeek

The evaluation-only one-shot adapter receives the complete visible fixture and Task contract in one bounded request. It returns:

- complete candidate `allocation.py` source;
- a structured completion Artifact payload;
- no iterative Tool observations.

The runner applies the candidate through Runtime, runs the same visible and hidden verifier, and passes the same Host acceptance path. This is a lower-interaction baseline, not a product Host or Harness feature.

### Cell B — native Ordivon Harness DeepSeek

This is the Phase 2 path. Its previous three Trials may be reused only if the full System Manifest remains identical.

### Cell C — mature Provider Harness using DeepSeek

Hermes ACP is the preferred first external reference because it can use the same Provider/model family. It becomes comparison-eligible only after an equivalence gate proves that:

- visible Task information is the same;
- protected files and hidden verifier remain outside model control;
- available filesystem, terminal, or Tool capabilities are explicitly captured;
- output and Artifact requirements are equivalent;
- Provider Harness state does not become Host Task authority;
- acceptance still uses the same independent verifier and Host decision.

If equivalent Tool access cannot be constructed without hiding material differences, the result remains a system-level reference and is not described as an isolated Harness causal comparison.

### Scheduling

Competitive Trials are sequential and interleaved rather than run in three large blocks. A first three-cell schedule is:

```text
A1 → B1 → C1
C2 → A2 → B2
B3 → C3 → A3
```

This reduces—but does not eliminate—Provider-time drift. Credential switching, rate limiting, endpoint changes, and model aliases are recorded as limitations. Secrets are never written to Trial evidence.

## Phase 4 — boundary fault cells

Fault cells answer whether each layer preserves its own invariant. Most are deterministic and require one conclusive execution, not three stochastic repetitions.

| Cell | Injected condition | Expected owner-visible result | Forbidden result |
|---|---|---|---|
| `HOST-STALE-ASSIGNMENT` | completion proposal from an old Assignment generation | Host rejects before verifier acceptance and before new Runtime dispatch | stale proposal advances Task or creates TaskOutcome |
| `HOST-MISSING-ARTIFACT` | Runtime process succeeds but completion Artifact is absent | Host rejects; Runtime success remains physical evidence only | process exit becomes semantic completion |
| `HARNESS-INVALID-TOOL-CORRECTION` | first model Tool call has malformed arguments, then emits a corrected call | invalid call retained, not dispatched; corrected call may proceed | malformed call reaches Runtime or disappears from Trace |
| `RUNTIME-RESPONSE-LOSS-REPLAY` | response is lost after Runtime admission | fresh caller finds exactly one Job and exact replay returns it | second Job or Attempt is dispatched |
| `CROSS-RESTART-AFTER-RUN` | Host/Harness process stops after Run receipt but before final decision | fresh process reconstructs evidence and commits at most one decision/outcome | Provider Session memory or copied transcript is required |

The fresh current Runtime local-acceptance receipt separately covers systemd/cgroup cancellation, orphan handling, corrupt/missing runner evidence, capacity, and MCP end-to-end behavior. Those tests remain Runtime component evidence and are not duplicated inside every Agent Trial.

Additional fault cells are admitted after the first campaign only when a real trajectory exposes an unresolved class. Candidates include budget exhaustion, source drift before spawn, cancellation during a Tool step, provider transport loss, Runtime terminal-evidence loss, and `needs_input` handoff.

## Evidence chain

Every accepted or rejected Trial must be reconstructable through this chain:

```text
Campaign
└── System Manifest
    └── Task Definition + QA
        └── Trial Manifest
            ├── Host Task
            ├── Host Task Attempt
            ├── Harness Assignment
            ├── Harness Run / Snapshot / Trace
            ├── Runtime Workspace
            ├── Runtime Job / Attempt
            ├── Runtime terminal-evidence Artifact
            ├── completion Artifact
            ├── independent verifier assertions
            ├── Host CompletionDecision
            └── Host TaskOutcome, when accepted
```

Track R stores references and digests. It does not copy Host Journal, Harness history, Runtime Registry, Provider raw messages, secrets, or private reasoning into a second control plane.

## Metrics by owner

### Common Trial metrics

Use the existing Result schema:

- model calls;
- Tool calls;
- Runtime Jobs;
- observation bytes;
- input, output, cached-input, reasoning, and total tokens when exposed;
- wall time;
- estimated cost when the pricing basis is explicit;
- repeated reads and commands;
- invalid Tool calls;
- human intervention count.

Unknown values remain `null`, not zero.

### Harness-native evidence

Retain in Harness receipts and Trace references:

- stop code and termination code;
- Provider Call identities;
- Tool Step Intent, Fence, Receipt, and reconciliation;
- snapshots and resume count;
- invalid/corrected calls;
- budget exhaustion;
- provider fault classification;
- candidate completion or `needs_input` conclusion.

Do not add all of these fields to the common Result schema before repeated Trials demonstrate a recurring cross-configuration query.

### Host-native evidence

Retain in Host Journal/CAS and decision references:

- Task and Attempt identity;
- Assignment generation and digest;
- stale proposal rejection;
- verifier invocation and assertion result;
- CompletionDecision;
- exact TaskOutcome count;
- state before and after fresh-process reconstruction;
- handoff or intervention state.

### Runtime-native evidence

Retain in Runtime Registry and Artifacts:

- Workspace source-state digest;
- Job and Attempt identities;
- request identity and foreign references;
- terminal evidence and process-tree disposition;
- duplicate dispatch count;
- recovery/cancellation conditions;
- Runtime inspection summary;
- Workspace closure or retained-state reason.

Runtime does not emit semantic acceptance.

## Minimal formal runner

The runner belongs to Track R as a thin research orchestrator. It is not a daemon, scheduler, database, Provider router, or replacement Host.

It should be one explicit command with an explicit output root. Its durable local files are bounded per campaign and Trial:

```text
campaign-preflight.json
system-manifests/<configuration>.json
trials/<trial-id>/intent.json
trials/<trial-id>/native-refs.json
trials/<trial-id>/runner-state.json
trials/<trial-id>/trial.json
trials/<trial-id>/result.json
trials/<trial-id>/failures/*.json
trials/<trial-id>/review.json
closeout.json
```

`intent.json` is immutable. `runner-state.json` is atomically replaced and contains only orchestration progress and native references. Restart logic must reconcile existing Host, Harness, and Runtime identities before any dispatch. It must never create a new Runtime request identity because a response was lost.

The runner performs these steps:

1. validate Task, Suite, plan, and component receipts;
2. capture or load the exact configuration System Manifest;
3. construct the exact initial Workspace;
4. create Host Task, Attempt, and Assignment through existing product APIs;
5. invoke the selected execution-path adapter;
6. collect native receipts and immutable references;
7. run the hidden verifier outside the evaluated Workspace;
8. request Host adjudication;
9. project Trial, Result, and Failure records;
10. run integrity and relation validation;
11. close the Workspace and verify cleanup;
12. emit a bounded review packet.

Product-specific behavior remains product-owned:

- Harness owns the native loop and Provider adapters;
- Host owns Task and completion state;
- Runtime owns physical work;
- Computing owns only campaign orchestration and research projection.

## Agent-first review

No experiment dashboard is required.

The runner emits structured JSON. `query_evaluation.py` provides status, identity lookup, failure filtering, and comparison readiness. Agent review reads native receipts and produces one bounded `review.json` for:

- every failure;
- every false completion;
- every duplicate Effect or physical dispatch;
- every anomalous-cost success;
- every grader/verifier disagreement;
- every Trial requiring manual intervention;
- a small random sample of accepted Trials before architecture decisions.

Human review is required only when the decision itself needs human judgment or responsibility: ambiguous verifier meaning, consequential external effects, privacy or publication concerns, major architecture deletion, or a result intended for human-facing media. Internal mechanical joins and routine trajectory classification remain Agent-consumable.

## Promotion and stop rules

### Proceed from smoke to live baseline only when

- every component preflight gate is current and bound;
- System Manifest fields required for comparison are complete;
- deterministic smoke acceptance is conclusive;
- all native identities join exactly;
- cleanup leaves no active Job or leaked Workspace;
- the hidden verifier remains outside model control.

### Proceed from baseline to comparison only when

- three native Harness Trials are valid records;
- no runner defect remains unresolved;
- every failure and anomalous success has a review;
- repeated Trials share one exact configuration manifest;
- one-shot and Provider Harness adapters can preserve the same Task and verifier contract.

### Stop the campaign when

- Task or verifier QA becomes unstable;
- source, model, Adapter, prompt, Tool catalog, Tool grant, budget, or environment changes mid-group;
- Runtime or Host state cannot be reconciled conclusively;
- a secret or private reasoning payload enters evidence;
- an unrelated production Job contaminates the selected state root or Workspace;
- duplicate physical dispatch or duplicate TaskOutcome occurs;
- cleanup cannot prove the disposition of a Workspace or process tree;
- Provider behavior changes materially during the interleaved comparison window.

### Architecture decision threshold

Three Trials per configuration support development diagnosis. A retain, shrink, or delete decision for the native Harness requires five to ten valid Trials per competitive configuration, all triggered reviews, exact common verifier identity, and a statement of remaining confounders. No heterogeneous global score is generated.

## Implementation sequence

### R3-A — runner and manifest foundation

- add a standard-library formal plan validator;
- add the thin campaign runner skeleton;
- build complete configuration System Manifests;
- add atomic per-Trial intent/state handling;
- project existing native receipts into current Track R records;
- do not invoke a live Provider yet.

### R3-B — deterministic integrated smoke

- implement one scripted repository-repair execution;
- prove all cross-layer references and cleanup;
- add the five fault cells using scripted or existing deterministic fixtures;
- fix runner defects before live calls.

### R3-C — native live baseline

- run three sequential native DeepSeek Trials;
- validate and review every trajectory;
- produce the first repeated live baseline closeout.

### R3-D — comparative cells

- add the evaluation-only one-shot adapter;
- add Hermes ACP only after the equivalence gate;
- interleave three development Trials per configuration;
- decide whether five-to-ten architecture Trials are justified.

The immediate next engineering task is R3-A. No new service, database, dashboard, generic evaluation repository, or automatic experiment scheduler is authorized.
