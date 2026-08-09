# Ordivon Research Portfolio

> Generated from [`portfolio.json`](portfolio.json). Edit the JSON source, then rerun `python3 scripts/render_research_portfolio.py`.

- **As of:** `2026-08-10`
- **Active research-line limit:** `2`
- **Current active lines:** `2`

`portfolio.json` is the single source of truth for research status, maturity, blockers, next falsifier, and Ready Frontier. This generated document is a review projection; question pages preserve stable hypotheses and experiment contracts, while Issues preserve discussion and execution history.

## Active research lines

| Line | Priority | Question | Items | Implementation | Exit criterion |
|---|---|---|---|---|---|
| R-A-HARNESS-CONTROL | P0 | Calibrated non-action and recoverable continuation | ANC-VERIFY-002 | ordivon-computing#82, ordivon-game#58, ordivon-security#19 | Security IF0-IF3 counts as the first live authority-timing consumer. Close or narrow the line after one materially different act/hold comparison determines whether deliberation-before-authority improves intent convergence and authorized utility over direct Tool exposure without transaction ceremony or a new control platform. |
| R-C-HARNESS-EVALUATION | P0 | Harness evaluation, replay, and trajectory evidence | ANC-VERIFY-001 | ordivon-computing#9 | The former Harness acceptance-conflict blocker is retired. Run only the smallest frozen-workload comparison still needed to decide whether Ordivon Harness adds measurable recovery/evidence value over a strong simpler one-shot or Provider-native baseline; no Observation daemon or replica campaign is required. |

## Question and track portfolio

### Reference

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-STACK-001 | M5 | reference | ordivon-computing | — | — | — | Use as the admission test; reopen only on contradictory evidence. | A cross-workload failure reveals a necessary responsibility absent from the current substrate/overlay split. |

### Active

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-VERIFY-002 | M4 | P0 | ordivon-computing | R-A-HARNESS-CONTROL | — | — | Treat Security IF0-IF3 as one live-Provider positive consumer and as negative evidence against transaction-like readback/finalization ceremony. The next experiment should leave the AC2 Security world: use one materially different bounded act/hold workload or a Harness-native ablation, expose consequence authority only after a non-authoritative deliberation opportunity, and compare against direct Tool exposure. Do not build a generic abstention or approval platform. | A materially different second consumer or Harness-native ablation must show whether non-authoritative deliberation before consequence authority improves act/hold intent convergence and authorized utility versus direct Tool exposure; if the effect does not reproduce, keep the Security IF0-IF3 result local. |
| ANC-VERIFY-001 | M4 | P0 | ordivon-computing | R-C-HARNESS-EVALUATION | — | — | Retire the stale Harness acceptance-conflict blocker: current Harness 5a42afd includes the post-merge revision-fenced repair and H2 closeout. Run only the smallest comparative Trial still needed across an Ordivon Harness path and a strong simpler one-shot or Provider-native baseline on one frozen workload, preserving owner-native Runtime/Provider/verifier receipts. Do not build an Observation daemon or add replicas merely for volume. | The same frozen workload cannot be compared without copying Provider lifecycles or duplicating Host, Harness, Runtime, and verifier authority, or the common envelope adds no explanatory value over local receipts. |

### Ready

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-HARNESS-002 | M5 | P0 | ordivon-harness | — | 5a42afdf5e01 | — | Do not force Security or another domain to adopt advanced/internal H2 merely to manufacture a second consumer. Bind the current Harness public api/core boundary at 5a42afd, keep H2 internal, and let ANC-VERIFY-001 run the smallest comparative Trial still needed for the Harness retain/shrink/delete decision. Promote a new public lifecycle surface only when an independent consumer naturally requires the same invariant. | One-shot or mature Provider Harness paths match both the bounded repository-repair and Security CAGE workloads with equal correctness, recovery, portability, and lower permanent cost, eliminating the need for an Ordivon-owned bare-model Loop. |

### Blocked

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-ADAPT-001 | M1 | P3 | ordivon-computing | — | — | ANC-VERIFY-001, 20-50-homogeneous-task-trajectories | Remain blocked. First complete P1 Core and the R3 repeated native baseline; then use CEL-R4 E1 to prove a bounded self-customer experiment and collect 20–50 homogeneous trajectories before changing one Skill, Context policy, stopping policy, or system configuration through shadow, canary, and rollback. | A versioned Skill or Context-policy change fails held-out Tasks or cannot beat a fixed baseline after rollback costs. |
| ANC-SECURITY-005 | M0 | P3 | ordivon-security | — | — | ANC-SECURITY-003, ANC-SECURITY-004, ANC-MULTI-001 | No implementation until single-actor strategic and opponent-model hypotheses survive. | Ordinary Host delegation and branch/join plus domain-local trust fields explain the first compromise scenario. |
| ANC-SECURITY-006 | M0 | P3 | ordivon-security | — | — | ANC-SECURITY-003, ANC-SECURITY-004, ANC-SECURITY-005, ANC-VERIFY-001, ordivon-security#20 | No platform or training loop until the unit of strategic evaluation is proven. | Held-out static-opponent evaluation predicts the same architecture decisions as coevolution with lower cost. |

### Deferred

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-COMPILER-002 | M1 | P1 | ordivon-computing | — | — | ANC-HARNESS-002, ANC-VERIFY-001 | Retain only the live question, strong transcript/compaction/retrieval baseline, falsifiers, and exact source audit. Do not preserve the historical TCG architecture narrative in the active tree. After Harness and evaluation prerequisites pass, run only the minimum single-Actor comparison; Prime/RLM, Child Runs, graph storage, Runtime Worker, and continual Harness remain conditional. | A transcript-centered Harness with bounded compaction or retrieval, current Artifacts, and ordinary Host Task semantics matches or exceeds the Temporal Cognitive Graph on verified outcome, false completion, continuation, token cost, repeated reads, and operator review with fewer durable objects. |
| ANC-COMPILER-001 | M1 | P2 | ordivon-computing | — | — | — | Do not implement an Agent VM; revisit only after a minimal branch/join failure. | An ordinary Host Task Graph, queue, reducer, and workflow backend express the first branch/join workload without an Agent VM. |
| ANC-MULTI-001 | M1 | P2 | ordivon-computing | — | — | — | After R-A closes, run one Goal, two independent Tasks, two Artifacts, and one deterministic Join. | A single Agent plus independent verifier matches two-branch quality and cost, or ordinary Task Graph semantics are sufficient. |
| ANC-ORG-001 | M1 | P3 | ordivon-computing | — | — | ANC-MULTI-001, real-operator-attention-traces | Remain an umbrella; derive objects only from real operator and multi-Agent trajectories. | Host-local DecisionRequests and ordinary Task/participant relations explain observed coordination without a new organization layer. |
| ANC-GAME-002 | M1 | P1 | ordivon-game | — | — | — | Finish the Station Zero first playable, then run G-PLAY-001 with scripted, decorative-Agent, and consequential-Agent cells; do not build a general society or world platform. | One small non-mission Agent activity fails to produce greater return, surprise, attachment, expression, consequential history, or meaningful choice than a scripted baseline at comparable total cost. |
| ANC-SECURITY-001 | M1 | P2 | ordivon-security | — | — | — | Keep as a deferred umbrella. Round 1 completed the minimum dynamic-opponent method and rejected Campaign promotion; resume only through the narrower Security #10 and #20 experiments after current WIP frees. | Mature simulation, MARL, cyber evaluation, and thin adapters express the strategic distinctions without a new shared layer. |
| ANC-SECURITY-003 | M4 | P2 | ordivon-security | — | — | — | Round 1 completed the minimum local and CAGE dynamic-opponent method but did not earn Campaign state. Defer the next test to held-out policies and Host/Context replacement through Security #10. | A scripted or ordinary Goal/Task policy matches explicit Campaign state on policy-switch and held-out-opponent cases. |
| ANC-SECURITY-004 | M4 | P2 | ordivon-security | — | — | — | Round 1 found diagnostic and information-state value but no objective-success or transfer benefit. Defer the next transcript-versus-compiled-hypothesis test to Security #10 under held-out policies and deliberate Context loss. | A reactive policy without explicit opponent hypotheses matches held-out policy-switch performance and evidence quality. |
| ANC-SECURITY-007 | M1 | P2 | ordivon-computing | — | — | — | Retain the completed comparative study and Security e37cc70 observation as reference. Admit no implementation until a disposable dynamic-software backend or Agent-child lineage experiment exposes an authority, identity, revocation, residual, or propagation failure that existing owners cannot represent. | Artifact provenance, process trees, Host delegation, Harness/Runtime identity, Evaluation Trial evidence, Contest evidence, and classical epidemic or game models express software, Agent, descendant, population, organization, and Campaign claims without a shared Execution Entity relation. |

### Completed

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-IR-001 | M5 | reference | ordivon-computing | — | — | — | Use EffectEnvelope v1 as historical evidence; extend only when a new cross-backend failure cannot remain in Host, Runtime, or an adapter. | A second interface family cannot preserve Effect meaning with the current envelope and Binding projection. |
| ANC-MEMORY-001 | M4 | reference | ordivon-computing | — | — | — | Use TaskCapsule evidence; do not create a general memory runtime. | A materially different workload cannot continue from bounded semantic state without transcript or Provider Session state. |
| ANC-HOST-001 | M4 | reference | ordivon-host | — | — | — | Product evolution belongs to ordivon-host; shared changes require new cross-workload evidence. | A real workload requires durable cognition state that cannot remain a Provider Harness concern or Host application schema. |
| ANC-HARNESS-001 | M5 | reference | ordivon-host | — | — | — | Use the Host-local cross-Provider boundary and provider-specific direct drivers; use ANC-HARNESS-002 for the separate first-party bare-model Agent Loop. | A second independent consumer requires a stable shared Harness lifecycle and demonstrates measurable duplicate-code reduction without losing Provider capability. |
| ANC-WORLD-002 | M5 | reference | ordivon-world | — | — | — | Use the W1 direct-integration result. Keep W2 conditional and open a new narrow experiment only after a concrete capability mismatch, contract drift, callback, participant-handoff, or Effect-rebinding failure is reproduced. | A later materially different external trajectory fails under Host plus provider/observation adapters and requires one reusable cross-owner responsibility. |
| ANC-EFFECT-001 | M5 | reference | ordivon-computing | — | — | — | Retain stable semantic identity, explicit UNKNOWN, opaque backend correlation, reconcile-before-redispatch, and independent verification. Keep provider request schemas, digest algorithms, Receipt semantics, and contract adaptation inside each adapter; reopen only on a reproduced multi-Binding failure. | One live semantic Effect has multiple provider or Tool Binding candidates whose compatibility, selection, or migration cannot remain in Host and adapter-local contracts. |
| ANC-HUMAN-001 | M2 | reference | ordivon-human | — | aa5a7af51e36 | — | Consume the revised Human model as a reference: diagnose unsupported transitions, smallest binding sets, and the relevant engine while preserving life quality, recoverability, obligations, control, and maintenance. Reopen only on contradictory real evidence; do not create a person model, score, financial authority, or automatic successor. | A simpler model explains concrete Ordivon cases without separate terminal outcomes, three economic engines, cross-cutting rails, ownership and leverage quality, coupled constraints, attention cost, human–AI retained capability, or autonomy distinctions; or those distinctions do not change a design or evaluation. |
| ANC-GAME-001 | M4 | reference | ordivon-game | — | — | — | Host convergence and authority cutover are closed. Game #58 serves R-A as the deterministic paired laboratory; Game #59 preserves deferred Session/compaction ablations after Harness v0. | A second game family requires a generic responsibility absent from one Host plus Game-owned World and replay semantics. |

### Superseded

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-SECURITY-002 | M2 | reference | ordivon-computing | — | — | — | Use only as historical substrate evidence. | None; historical comparison is retained. |
| ANC-EDGE-001 | M2 | reference | ordivon-computing | — | — | — | Historical narrative is Git-only; successor and disposition remain in the portfolio. | None; the split was an intermediate derivation. |
| ANC-LINK-001 | M2 | reference | ordivon-computing | — | — | — | Historical narrative is Git-only; successor and disposition remain in the portfolio. | None; the split was an intermediate derivation. |
| ANC-WORLD-001 | M2 | reference | ordivon-computing | — | — | — | Historical narrative is Git-only; successor and disposition remain in the portfolio. | None; composition analysis produced the unified question. |

### Frozen

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-KERNEL-001 | M5 | reference | ordivon-computing | — | — | — | Accept only bug fixes, regression evidence, or newly demonstrated universal invariants. | A cross-framework failure requires a universal invariant that cannot remain in Host, Runtime, Tool contracts, or a domain World. |

## Programs

| Program | Issue | Kind | Status | Disposition | Next action |
|---|---|---|---|---|---|
| ANC-MACHINE-V0 | #1 | research_program | active | retain_as_parent | Use the generated portfolio as the Ready Frontier. |
| PERSONAL-DEVELOPER-RELIABILITY | #44 | operational_program | active | retain_as_operational_program | Continue only work that removes repeated operating friction. |
| STRATEGIC-ADVERSARIAL-SYSTEMS | #46 | research_program | deferred | retain_as_deferred_umbrella | Round 1 completed the minimal dynamic-opponent method and rejected Campaign promotion; defer Round 2 until held-out policy, Context-loss, and Host-replacement experiments are admitted. |
| EXTERNAL-BASELINE-VALIDATION | #56 | research_method_program | completed | absorb_into_research_method | Close after Round A; child Issues retain unfinished experiments. |
| PLURAL-INTELLIGENCE-ALIGNMENT | #63 | alignment_program | completed | absorb_into_core_registry_and_children | Close after Round A; remaining implementation stays in owning repositories. |

## Studies

| Study | Status | Role | Next action |
|---|---|---|---|
| 2026-adaptive-acceleration | reference | published normative position | Revise only after substantive evidence, critique, or position change. |
| 2026-agent-native-adversarial-systems | deferred | Round 1 evidence and deferred strategic Security research source | Consume the completed Round 1 method and negative abstraction result; resume only with held-out opponent policies, deliberate Context loss, and Host/Harness replacement. |
| 2026-execution-entity-adversarial-ecology | reference | cross-disciplinary foundation for software, Agent, lineage, population, organization, Campaign, control, resilience, and adversarial-ecology evaluation | Consume through ANC-SECURITY-007; do not create a shared Execution Entity protocol until a disposable-software or Agent-child workload exposes a reproduced cross-project failure. |
| 2026-agent-native-game-worlds | completed | bounded thesis and research program for intrinsic play, creation, persistent Agent participation, and plural Game verticals | Consume through ANC-GAME-002; finish the Station Zero alpha, then run G-PLAY-001 before constructing any generic social, habitat, or world platform. |

## Evidence maturity

- **M0** — Concept or intuition only.
- **M1** — Strong baseline and literature comparison.
- **M2** — Frozen workload, falsifier, and experiment contract.
- **M3** — Deterministic executable experiment.
- **M4** — Live Provider, Runtime, or World evidence.
- **M5** — Second materially different workload or backend.
- **M6** — Stable cross-project contract eligible for Core or Protocol promotion.

## Governance rules

- **Promotion:** No shared layer or repository without a reproduced failure, a second materially different consumer, explicit ownership, measured net benefit, and a deletion test.
- **Judgment:** The portfolio limits WIP and records reasons; it does not mechanically decide what matters. Identifiable participants remain responsible for priority, exception, revision, and deletion, and the portfolio itself must be narrowed or removed if its recurring cost exceeds the drift it prevents.
- **New question admission:** A new question must replace, block, or materially refine an existing item and name its first falsifier, minimum workload, deletion outcome, and consuming repository.
- **External observations:** An active or ready question owned outside ordivon-computing binds the exact observed repository revision and local immutable evidence. The binding records observation freshness; it does not override the product repository as implementation authority.
- **Source identity:** Cross-repository current-state audits must record local HEAD, upstream or published release revision, and consumed dependency pins as distinct facts. None may substitute for another, and historical receipts remain bound to their original revisions.
- Every completed experiment ends in one of: `retain`, `localize`, `shrink`, `defer`, or `delete`.
- `active` is a WIP state, not a statement of importance. `deferred` preserves a valid question without consuming current execution bandwidth.
- Historical evidence is retained through `completed`, `superseded`, or `frozen`; it does not remain in the Ready Frontier.
