# P0–P1 Consumer Falsification Design

Status: executing. P0-A0/P0-B0 deterministic apparatus is implemented, validated, and frozen in exact-revision receipts; no live Provider comparison is claimed yet. No new shared infrastructure is authorized by this document.

This design started from the reconciled 2026-08-10 Ready Frontier and was first landed at Computing `32014ceea7590e172407c309e411c899109c8bde`. P0 execution must bind fresh exact owner revisions rather than treating that design revision as deployment truth. It operationalizes the transition from infrastructure construction to ordinary consumer falsification. Product and domain repositories retain their own authority. Computing owns only experiment design, cross-project comparison, and interpretation.

## Program contract

P0 asks whether current Agent infrastructure earns continued existence or whether a smaller baseline is enough. P1 asks whether already-built capabilities survive ordinary production use and client-visible contract drift without another control plane.

The program follows four rules:

1. **Strong simpler baseline first.** A new mechanism does not compete against a deliberately weak baseline.
2. **One causal variable per comparison where possible.** Provider, model, Task, verifier, budget and environment remain fixed when the claim is about Harness or authority timing.
3. **Owner-native truth remains local.** Computing records exact references and derived Trial records; it does not copy Host, Harness, Runtime, Game, Web or Provider state into a new authority.
4. **Negative results delete work.** Equivalent simpler baselines shrink infrastructure; non-reproduction localizes a result; client refresh success closes operational work.

```text
P0  causal / architectural falsification
    ├─ P0-A  Harness retain / shrink / delete
    └─ P0-B  deliberation-before-authority causal test

P1  ordinary production friction
    ├─ P1-A  Web ordinary source-bound production
    └─ P1-B  Agent-effective MCP contract freshness
```

Game, World and Security continue their own ordinary product/domain work in parallel. They are evidence sources, not subprojects owned by this program.

---

# P0 — Consumer falsification

## P0-A — Harness retain / shrink / delete

### Decision question

For a frozen bounded repository-repair workload, does current Ordivon Harness produce enough additional correctness, recovery, evidence quality or continuation value over a strong simpler path to justify its permanent cognitive-execution machinery?

This is `ANC-VERIFY-001`. It is not a model leaderboard.

### Existing apparatus to retain

Reuse the existing `harness-evaluation-v0` evidence contract, B4 deterministic Formal Runner, frozen `HARNESS-REPO-REPAIR-001` Task/verifier, owner-native Observation Selection, Trial disposition and failure taxonomy. Do **not** restart the historical B5 campaign. `run_b5_native_trial.py` and its provider-capability gate remain historical diagnostic apparatus.

The former Harness H4 acceptance blocker is retired by current Harness owner evidence. A new comparison must bind current exact owner revisions and use the current public Harness surface rather than pretending the old B5 configuration is still current.

### Competitive cells

#### Cell S — strong simple one-shot

An evaluation-local direct Provider adapter receives exactly the visible Task material and acceptance/output contract in one bounded model request. It returns candidate `allocation.py` content plus the same structured completion payload expected from the iterative path. Computing applies the candidate through Runtime and sends it through the same independent visible/hidden verifier and semantic admission path.

This adapter is experiment apparatus only. It must not become a product-side one-shot Harness.

#### Cell H — current Ordivon Harness loop

P0-A0 found that the current high-level `HarnessAgentRun` handle is **not closed over the frozen repository-repair custom Tool catalog**: its supported exact compositions are currently the no-Tool and independent-search surfaces. P0 must not enlarge that high-level API merely to make a benchmark fit.

The first causal S/H comparison therefore uses the current public dependency-inverted `DomainToolLoopRunner` for the Harness cognitive loop, with the same Provider/model family, visible Task information, verifier and aggregate configuration budget. This isolates the incremental value/cost of iterative Harness Tool cognition against one-shot cognition without mislabeling an advanced/historical composition as `HarnessAgentRun`.

Durable Run continuation, Runtime reconciliation and response-loss recovery remain separate Harness value dimensions. If the public domain-loop comparison shows no useful cognitive-loop advantage, those durable mechanisms can still be tested independently before a repository-wide shrink/delete decision. If the loop does show value, a later consumer—not this benchmark—must justify whether a more general high-level `HarnessAgentRun` Tool-surface composition is needed.

#### Cell P — Provider-native/mature Harness reference, optional

A mature Provider Harness such as Hermes ACP may be added only after an equivalence gate shows comparable visible information, capability scope and acceptance semantics. If Tool surfaces or Provider behavior cannot be made comparable, Cell P remains a system-level reference and is never described as isolated Harness causal evidence. P0 does not block on Cell P.

### Fairness invariants

Cell S and Cell H must bind the same:

- Task ID/version and historical fixture bytes;
- hidden and visible verifier identity;
- Provider and model identity where the comparison claims Harness effect;
- sampling parameters where exposed;
- visible source information and protected-file boundary;
- output/completion contract;
- total wall-time and token ceilings at the configuration level;
- Runtime source materialization and verifier environment;
- evidence/privacy rules.

They are allowed to differ in Tool interaction count, intermediate observations, durable cognition and recovery because those are Harness mechanisms being measured.

### Execution sequence

#### A0 — rebind and deterministic preflight

1. Capture exact current Computing, Host, Harness and Runtime revisions.
2. Preserve historical B4 as revision-bound evidence. Its current rerun is expected to fail closed when owner revisions differ; do not edit its pinned owner vector to manufacture freshness. Reuse only its frozen Task/verifier primitives where their exact historical identities remain valid.
3. Build a fresh current-revision A0 comparator and later System Manifest.
4. Implement Cell S as the minimum evaluation-local one-shot apparatus.
5. Bind Cell H first to the current public `DomainToolLoopRunner`; separately probe the high-level `HarnessAgentRun` custom-Tool closure rather than assuming it.
6. Require scripted S/H to bind the same visible Task, hidden verifier and oracle candidate before any live call.

P0-A0 satisfied this deterministic apparatus gate. It also retained the `HarnessAgentRun` custom-Tool surface gap as evidence instead of expanding Harness. No live comparative Provider call occurs until the Agent-visible MCP contract freshness gate is closed.

#### A1 — paired canary

Run one `S1 → H1` pair sequentially. This pair answers only: are the cells actually comparable and does the evidence path remain complete? Any infrastructure/evaluator failure invalidates the pair and is repaired before more sampling.

#### A2 — development group

If A1 is valid, run three selection-eligible Trials per cell, interleaved rather than blocked:

```text
S1 → H1
H2 → S2
S3 → H3
```

The A1 pair counts toward this group only when its exact System Manifest matches.

#### A3 — architecture-decision expansion, conditional

Do not automatically scale. Expand toward five to ten valid Trials per cell only if the three-trial group leaves a real retain/shrink/delete ambiguity whose expected decision value exceeds Provider cost.

### Measurements

Primary:

- semantic verifier outcome;
- false-completion count;
- valid/invalid/unknown Trial disposition;
- duplicate physical dispatch / duplicate semantic outcome;
- recovery from response loss or process replacement when actually exercised;
- evidence completeness sufficient to explain the result.

Secondary cost/friction:

- model calls and Tool calls;
- Runtime Jobs;
- input/output/reasoning tokens when exposed;
- wall time;
- repeated reads/commands;
- invalid/corrected Tool calls;
- operator intervention;
- permanent code/state required by each path.

There is no scalar global score.

### Architecture disposition

P0-A ends with one of these scoped outcomes:

- **retain** — Harness has repeated measurable recovery/evidence/correctness value not matched by the simple baseline at comparable total cost;
- **shrink** — only a smaller subset such as durable Run/reconciliation or bare-model fallback produces recurring value;
- **localize** — Provider-native Harnesses dominate ordinary cases while Ordivon Harness remains useful only for explicit bare-model or research workloads;
- **delete path** — the one-shot/Provider-native baseline is equivalent or better and the native Harness machinery adds recurring cost without a protected failure.

The result applies first to the tested workload family. A repository-wide deletion still requires checking current independent consumers before removing public surfaces.

### Stop conditions

Stop rather than patch around comparison validity when:

- Provider/model identity changes mid-group;
- hidden verifier or Task bytes change;
- Cell S and H visible information differ materially;
- client/tool schema drift changes one cell's callable surface;
- evidence cannot establish whether a physical effect was duplicated;
- a new runner becomes more complicated than the mechanisms it is evaluating.

---

## P0-B — Deliberation before consequence authority

### Decision question

Does giving cognition one non-authoritative opportunity to form/revise intent **before** consequence Tools become available improve act/hold intent convergence relative to direct Tool exposure, or was Security IF0–IF3 a domain-local result?

This is the sharpened `ANC-VERIFY-002` question. Readback/finalization ceremony is not a candidate mechanism; IF0/IF1 already provide negative evidence for that path.

### Why two stages

A direct jump into another product domain would confound the timing variable with domain policy. Therefore P0-B first uses current Harness H2 as **internal experimental apparatus**, not as a public feature. Only if the causal timing effect survives this controlled ablation do we ask Game for a second owner-native confirmation.

### B0 — Harness-native causal ablation

Build two treatments over the same bounded decision fixtures:

```text
D — direct authority
Context + consequence Tools
→ one ordinary Agent turn/loop
→ final admitted intent

L — late authority
Context, no consequence Tools
→ retained non-authoritative deliberation
→ same Context + exact deliberation record + consequence Tools
→ final admitted intent
```

Use the existing advanced/internal H2 lifecycle composition for L so aggregate token budget, wall deadline and cancellation authority span both phases. Do not export H2 through the recommended public API for this experiment.

### Fixture structure

Use at least one matched pair of exact contexts:

- **ACT** — one bounded effect is unambiguously utility-improving under the declared objective;
- **HOLD** — the superficially available effect is unambiguously dominated by non-action under the same decision grammar.

The experiment fixture owns only a typed candidate-effect admission record; it need not perform an external physical side effect. The question is whether Tool authority shapes intent formation. A later Game confirmation supplies real domain consequence.

The two contexts should be new and must not reuse Security AC2 wording or state. They should contain enough interacting evidence that the model must integrate state/objective consequences rather than match a trivial keyword.

### Controlled variables

D and L bind the same:

- Provider/model/sampling;
- complete source Context;
- objective;
- effect schema and final admission rules;
- total token/wall budget;
- completion/result schema;
- trial ordering policy.

The intended causal variable is only **when consequence action vocabulary becomes available**.

### Measurements

For ACT and HOLD separately:

- oracle-consistent final intent;
- false action / false hold;
- first authoritative effect-intent position;
- whether intent is revised before admission;
- disagreement between final reasoning/conclusion and admitted effect;
- model calls, tokens and wall time;
- no-progress or budget termination;
- stochastic variance across repeats.

The non-authoritative deliberation record is cognition evidence, not effect authority or world truth.

### Sampling sequence

1. Scripted deterministic apparatus acceptance for both treatments. **Completed in P0-B0** with a mechanically derived ACT/HOLD oracle, exact Context equality, direct first-request Tool exposure, late first-request Tool absence, and the same Tool catalog opening in phase B under one H2 aggregate lifecycle budget.
2. After Agent-visible MCP contract freshness is proven, run one live D/L canary for ACT and HOLD under one exact Provider/model configuration.
3. If valid, run three live replicates per `treatment × context` cell.
4. Review every disagreement, not just aggregate correctness.

A single positive replicate does not generalize the mechanism.

### B1 — second-domain confirmation, conditional

Only if B0 shows a repeatable timing effect, move to Station Zero v3 without changing Game core semantics. Game is a good second domain because its current faction candidate surface already includes consequential actions and `wait`, Provider output selects a legal candidate identity, and Game retains separate action/World authority.

The Game experiment should:

- bind one exact v3 Planning Head / World revision;
- choose one faction with one paired world/objective condition where action is preferable and one where `wait` is preferable;
- compare ordinary direct candidate exposure against one pre-candidate deliberation phase;
- preserve Game's Candidate admission, Subject × Cognition × Actor × Intent binding and World consequence authority unchanged;
- store Computing interpretation outside Game authority.

If B0 fails, B1 is cancelled. If B0 succeeds but Game does not reproduce, the result remains Harness/Security-local and no shared public cognition primitive is promoted.

### Promotion threshold

Even a positive Security + H2 + Game result does **not** automatically create a new service. The first promotion candidate is only a narrow Harness composition/surface for caller-selected authority staging. A persistent policy engine, abstention service or universal deliberation phase remains rejected unless another workload forces it.

---

# P1 — Ordinary production friction

## P1-A — Web ordinary source-bound production

### Decision question

Can a fresh Agent make one normal high-value public Web change from owner-native truth through the existing Studio/Web production protocol, with good rendered desktop/mobile output and no new showcase-specific rules?

### First production target

Use the Ordivon Runtime Project surface to explain the newly proven Windows-native execution target. This is ordinary product communication, not another A3 aesthetic experiment.

Reader task:

> Understand what Windows-native execution can actually do, how authority/recovery is bounded, what is physically proven, and what client-visible limitation remains, without confusing repository, deployed Runtime, server Tool contract or ChatGPT-loaded schema.

Owner truth must be re-observed immediately before editing. Fast-changing revision labels are publication evidence, not timeless prose. Stable claims should describe responsibility and proven behavior; exact revisions belong in bounded status/provenance where useful.

### Production path

```text
OBSERVE
Runtime / Workstation / Host owner facts
        ↓
FRAME
reader task + Project-page encounter
        ↓
BIND
current / historical / limitation claims
        ↓
EXPRESS
existing Web expression profile + Studio protocol
        ↓
RENDER
real desktop + mobile browser outputs
        ↓
AUDIT
claim semantics + navigation + accessibility + responsive meaning
        ↓
DECIDE
revise / no-op / promote only recurring Web-local priors
```

### Required evidence separation

Keep four judgment streams separate:

1. **source truth** — exact owner facts and observed revisions;
2. **reader/task success** — can the page answer the intended questions;
3. **semantic/accessibility integrity** — no visual implication exceeds textual authority, keyboard/structure/contrast/responsive behavior remain valid;
4. **expression judgment** — hierarchy, rhythm, identity, interest and visual continuity.

A beautiful page with stale capability claims fails. A truthful page with avoidable reading friction also fails production quality, but the failure owners remain distinct.

### Promotion rule

Do not add a new Web rule after one page. Record residual friction. Change `design/expression-profile.md` only when the same Web-local prior survives at least one other materially different ordinary production surface.

### Stop conditions

Stop publication when owner truth cannot be reconciled, current/deployed/client states are conflated, mobile rendering changes factual meaning, accessibility audit fails, or a bespoke component exists only to dramatize one project fact with no recurring utility.

---

## P1-B — Agent-effective MCP contract freshness

### Decision question

Can an Agent reliably move from a stale client-loaded Tool contract to the already-deployed server contract through ordinary connector/session refresh and exact contract re-observation, without a central Tool registry or raw-MCP workaround?

### Current known pressure

At design time the running servers expose capabilities newer than the current ChatGPT-loaded schemas:

- Runtime live server exposes `workspace.exec.executionTarget` and `windowsAuthority`;
- current ChatGPT-loaded Runtime `workspace.exec` still lacks them;
- Host server `task.checkpoint` supports `continuityDisposition`;
- current ChatGPT-loaded Host Tool schema still omits it.

This is a CR-07 Tool-contract drift / client adoption problem, not evidence of missing server functionality.

### B0 — freeze the mismatch

Before refresh, retain:

- live server `serverInterface` / Tool catalog identity;
- current client-visible Tool field set;
- exact missing fields;
- one owner-native service/deployment status proving the server is current.

Do not infer stale/fresh from version labels alone.

### B1 — ordinary refresh

Use the normal ChatGPT connector/session refresh/reload boundary. No server redeploy and no schema changes are allowed during this test.

After refresh, re-observe the **client-loaded** Tool definitions. Success requires both Runtime fields and Host `continuityDisposition` to appear where the refreshed connector exposes those Tools. A reconnect banner or successful server response is insufficient evidence.

### B2 — connector-level functional smoke

After the schema is actually fresh:

1. Run one ordinary connector `windows_native + limited` Runtime Job with a harmless exact executable/argument and verify owner-native Job/Attempt evidence.
2. Optionally run one elevated read-only identity smoke if the ordinary client exposes `windowsAuthority=elevated`; no mutable elevated action is needed.
3. Use refreshed Host `task.checkpoint(... continuityDisposition=complete)` to close one semantically completed continuity Task through the ordinary connector.

The test succeeds only through the same Agent-facing tools normal work will use. Raw MCP probes remain diagnostic evidence and do not substitute for B2.

### Failure classification

- **server mismatch** — live `tools/list` itself lacks expected fields: owner/server problem;
- **client adoption failure** — fresh ChatGPT connector/session still loads an older schema while live server is current;
- **functional transport failure** — client schema is fresh but ordinary call cannot realize the advertised contract;
- **closure ergonomics only** — Runtime call works but Host semantic done Tasks remain hard to terminate.

### Escalation threshold

One successful refresh closes P1-B as ordinary lifecycle friction. Do not build infrastructure.

If two genuinely fresh connector/session instances independently reproduce client adoption failure against the same current server schema identity, retain a bounded compatibility/evidence case and pursue the narrow client/connector integration fix. Even then, do not create a central Tool registry unless pending work cannot safely bind/rebind using provider-owned catalog identities.

---

# Execution ordering

P0 and P1 can partially overlap, but the default order is:

```text
P0-A0  evaluation rebind + scripted comparator
P0-B0  authority-timing apparatus design
        ↓
P1-B0/B1  refresh the Agent-visible MCP contracts
        ↓
P0-A1/A2  live Harness comparison
P0-B live ablation
        ↓
P1-A  ordinary Runtime Web publication
        ↓
conditional P0-B1 Game confirmation
```

P1-B is deliberately early because a stale Agent Tool contract can contaminate later Runtime/Host-facing experiments. P1-A publication occurs after current owner states are re-observed so the public page describes the actual system used by P0 rather than an earlier snapshot.

# Program exit

P0 exits when:

- Harness has a scoped retain/shrink/localize/delete disposition from valid comparative evidence; and
- authority timing either reproduces beyond Security or is explicitly localized.

P1 exits when:

- one ordinary Web production change completes without creating another showcase workflow; and
- ordinary Agent-facing Host/Runtime Tool contracts converge after refresh, or a narrowly classified client adoption defect is retained.

Neither exit authorizes World Model Round 002. Computing reopens the world model only if these experiments produce a contradiction or a stable unowned responsibility that current A2/A6/A7/A9/A10/A13 cannot regenerate.
