# Ordivon Research Portfolio

> Generated from [`portfolio.json`](portfolio.json). Edit the JSON source, then rerun `python3 scripts/render_research_portfolio.py`.

- **As of:** `2026-08-02`
- **Active research-line limit:** `2`
- **Current active lines:** `2`

The portfolio is the single source of truth for research status, maturity, blockers, next falsifier, and Ready Frontier. Question pages preserve stable hypotheses and experiment contracts; Issues preserve discussion and execution history.

## Active research lines

| Line | Priority | Question | Items | Implementation | Exit criterion |
|---|---|---|---|---|---|
| R-A-HARNESS-CONTROL | P0 | Calibrated non-action and recoverable continuation | ANC-VERIFY-002 | ordivon-computing#82, ordivon-game#58, ordivon-security#19 | Paired should-act and should-hold trajectories measure pre-commit timing, false abstention, authorized utility, recovery, and whether existing Host facts suffice without a new control platform. |
| R-C-HARNESS-EVALUATION | P0 | Harness evaluation, replay, and trajectory evidence | ANC-VERIFY-001 | ordivon-computing#9 | One frozen Task runs under one-shot, Ordivon Harness, and a mature Provider Harness with the same verifier, repeated Trials, exact cost/action evidence, and a decision to retain, shrink, or delete the common evaluation envelope. |

## Question and track portfolio

### Reference

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-STACK-001 | M5 | reference | ordivon-computing | — | — | — | Use as the admission test; reopen only on contradictory evidence. | A cross-workload failure reveals a necessary responsibility absent from the current substrate/overlay split. |

### Active

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-VERIFY-002 | M2 | P0 | ordivon-computing | R-A-HARNESS-CONTROL | — | — | Run the paired non-action suite against model-only, static-policy, and existing Host evidence-rich baselines; use H5 retained generation, Artifact, and reconciliation mechanisms without building a Harness or abstention platform. | A simpler paired act/abstain or static policy achieves equal authorized utility, timing, and recovery with fewer states. |
| ANC-VERIFY-001 | M3 | P0 | ordivon-computing | R-C-HARNESS-EVALUATION | — | — | Use the R0-R2 contract and HARNESS-REPO-REPAIR-001 QA gate for R3: project one-shot, Ordivon Harness, and mature Harness runs into the same Trial and Result records, then review every failure and anomalous success. | The same frozen workload cannot be compared without copying Provider lifecycles or duplicating Host, Harness, Runtime, and verifier authority, or the common envelope adds no explanatory value over local receipts. |

### Ready

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-HARNESS-002 | M4 | P0 | ordivon-host | — | 264d96cb2325 | — | OH4 now provides a native Host Run Contract, Assignment-scoped ToolGrant, persisted evidence, independent verification, and fresh-process Outcome recovery. Use Track R R3 to compare the same frozen repository-repair Task under one-shot, Ordivon Harness, and a mature Provider Harness; retain, shrink, or delete the first-party Loop from measured value rather than implementation existence. | One-shot or mature Provider Harness paths match the same bounded workloads with equal correctness, recovery, portability, and lower permanent cost, while no bare-model use case requires a first-party Loop. |
| ANC-HUMAN-001 | M2 | P1 | ordivon-human | — | ec8142020f20 | — | After lawful approved CHFS/CFPS access, execute the owner-side E2 aggregate pipeline privately, validate weights and panel links, estimate current poor/wealthy constrained states and recovery outcomes, and return disclosure-reviewed aggregate findings. Computing should consume implications only. | Recent approved CHFS/CFPS analysis shows that liquidity, commitment timing, housing/debt state, control, quality-of-life, and option-set variables add no explanatory value beyond conventional income and net worth, or wealthy-constrained prevalence disappears under defensible alternative definitions. |

### Blocked

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-ADAPT-001 | M1 | P3 | ordivon-computing | — | — | ANC-VERIFY-001, 20-50-homogeneous-task-trajectories | Collect comparable trajectories first; later change only one Skill, Context policy, or stopping policy through replay, shadow, canary, and rollback. | A versioned Skill or Context-policy change fails held-out Tasks or cannot beat a fixed baseline after rollback costs. |
| ANC-SECURITY-005 | M0 | P3 | ordivon-security | — | — | ANC-SECURITY-003, ANC-SECURITY-004, ANC-MULTI-001 | No implementation until single-actor strategic and opponent-model hypotheses survive. | Ordinary Host delegation and branch/join plus domain-local trust fields explain the first compromise scenario. |
| ANC-SECURITY-006 | M0 | P3 | ordivon-security | — | — | ANC-SECURITY-003, ANC-SECURITY-004, ANC-SECURITY-005, ANC-VERIFY-001, ordivon-security#20 | No platform or training loop until the unit of strategic evaluation is proven. | Held-out static-opponent evaluation predicts the same architecture decisions as coevolution with lower cost. |

### Deferred

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-COMPILER-001 | M1 | P2 | ordivon-computing | — | — | — | Do not implement an Agent VM; revisit only after a minimal branch/join failure. | An ordinary Host Task Graph, queue, reducer, and workflow backend express the first branch/join workload without an Agent VM. |
| ANC-MULTI-001 | M1 | P2 | ordivon-computing | — | — | — | After R-A closes, run one Goal, two independent Tasks, two Artifacts, and one deterministic Join. | A single Agent plus independent verifier matches two-branch quality and cost, or ordinary Task Graph semantics are sufficient. |
| ANC-ORG-001 | M1 | P3 | ordivon-computing | — | — | ANC-MULTI-001, real-operator-attention-traces | Remain an umbrella; derive objects only from real operator and multi-Agent trajectories. | Host-local DecisionRequests and ordinary Task/participant relations explain observed coordination without a new organization layer. |
| ANC-GAME-002 | M1 | P1 | ordivon-game | — | — | — | Finish the Station Zero first playable, then run G-PLAY-001 with scripted, decorative-Agent, and consequential-Agent cells; do not build a general society or world platform. | One small non-mission Agent activity fails to produce greater return, surprise, attachment, expression, consequential history, or meaningful choice than a scripted baseline at comparable total cost. |
| ANC-SECURITY-001 | M1 | P2 | ordivon-security | — | — | — | Keep as a deferred umbrella. Round 1 completed the minimum dynamic-opponent method and rejected Campaign promotion; resume only through the narrower Security #10 and #20 experiments after current WIP frees. | Mature simulation, MARL, cyber evaluation, and thin adapters express the strategic distinctions without a new shared layer. |
| ANC-SECURITY-003 | M4 | P2 | ordivon-security | — | — | — | Round 1 completed the minimum local and CAGE dynamic-opponent method but did not earn Campaign state. Defer the next test to held-out policies and Host/Context replacement through Security #10. | A scripted or ordinary Goal/Task policy matches explicit Campaign state on policy-switch and held-out-opponent cases. |
| ANC-SECURITY-004 | M4 | P2 | ordivon-security | — | — | — | Round 1 found diagnostic and information-state value but no objective-success or transfer benefit. Defer the next transcript-versus-compiled-hypothesis test to Security #10 under held-out policies and deliberate Context loss. | A reactive policy without explicit opponent hypotheses matches held-out policy-switch performance and evidence quality. |

### Completed

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-IR-001 | M5 | reference | ordivon-computing | — | — | — | Consume EffectEnvelope v1 as historical evidence; extend only when a new cross-backend failure cannot remain in Host, Runtime, or an adapter. | A second interface family cannot preserve Effect meaning with the current envelope and Binding projection. |
| ANC-MEMORY-001 | M4 | reference | ordivon-computing | — | — | — | Consume TaskCapsule evidence; do not create a general memory runtime. | A materially different workload cannot continue from bounded semantic state without transcript or Provider Session state. |
| ANC-HOST-001 | M4 | reference | ordivon-host | — | — | — | Product evolution belongs to ordivon-host; shared changes require new cross-workload evidence. | A real workload requires durable cognition state that cannot remain a Provider Harness concern or Host application schema. |
| ANC-HARNESS-001 | M5 | reference | ordivon-host | — | — | — | Consume the Host-local cross-Provider boundary and provider-specific direct drivers; use ANC-HARNESS-002 for the separate first-party bare-model Agent Loop. | A second independent consumer requires a stable shared Harness lifecycle and demonstrates measurable duplicate-code reduction without losing Provider capability. |
| ANC-WORLD-002 | M5 | reference | ordivon-world | — | — | — | Consume the W1 direct-integration result. Keep W2 conditional and open a new narrow experiment only after a concrete capability mismatch, contract drift, callback, participant-handoff, or Effect-rebinding failure is reproduced. | A later materially different external trajectory fails under Host plus provider/observation adapters and requires one reusable cross-owner responsibility. |
| ANC-EFFECT-001 | M5 | reference | ordivon-computing | — | — | — | Retain stable semantic identity, explicit UNKNOWN, opaque backend correlation, reconcile-before-redispatch, and independent verification. Keep provider request schemas, digest algorithms, Receipt semantics, and contract adaptation inside each adapter; reopen only on a reproduced multi-Binding failure. | One live semantic Effect has multiple provider or Tool Binding candidates whose compatibility, selection, or migration cannot remain in Host and adapter-local contracts. |
| ANC-GAME-001 | M4 | reference | ordivon-game | — | — | — | Host convergence and authority cutover are closed. Game #58 serves R-A as the deterministic paired laboratory; Game #59 preserves deferred Session/compaction ablations after Harness v0. | A second game family requires a generic responsibility absent from one Host plus Game-owned World and replay semantics. |

### Superseded

| ID | Maturity | Priority | Owner | Active line | Observed revision | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|---|
| ANC-SECURITY-002 | M2 | reference | ordivon-computing | — | — | — | Use only as historical substrate evidence. | None; historical comparison is retained. |
| ANC-EDGE-001 | M2 | reference | ordivon-computing | — | — | — | Historical only. | None; the split was an intermediate derivation. |
| ANC-LINK-001 | M2 | reference | ordivon-computing | — | — | — | Historical only. | None; the split was an intermediate derivation. |
| ANC-WORLD-001 | M2 | reference | ordivon-computing | — | — | — | Historical only. | None; composition analysis produced the unified question. |

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
| 2026-computing-stack-walkthrough | reference | physical-to-institutional learning map | Revise only after a material computing-paradigm change. |
| 2026-classical-to-agent-native-computing | reference | layer-admission and deletion framework | Use as the default admission test. |
| 2026-scarcity-operability-and-paradigm-change | reference | first-principles lens for scarcity migration, operational resolution, conceptual decoupling, and Ordivon pre-reform audit | Use as a reference when a capability or cost shift invalidates an inherited coupling; do not change the Ready Frontier or architecture from the study alone. |
| 2026-retention-default-inversion | reference | default active-removal and audited-retention framework derived from the Station Zero anti-formalism audit | Apply during repository audits; do not create a retention registry or mandatory governance workflow. |
| 2026-adaptive-acceleration | reference | published normative position | Revise only after substantive evidence, critique, or position change. |
| 2026-agent-system-concept-system | completed | canonical terminology and closed cross-Provider Harness-boundary source | Preserve as reference; use ANC-HARNESS-002 for the separate first-party bare-model Agent Loop. |
| 2026-model-to-work-and-ordivon-harness | completed | canonical model-to-work stack, H1-H5 evidence ledger, and Ordivon Harness admission source | Consume through ANC-HARNESS-002; revise only if the v0 experiment contradicts the ownership or scope decision. |
| 2026-task-to-world-interaction | completed | canonical closed World and Effect boundary decision source | Preserve the W0/W1 direct-integration result as reference. Activate only a narrow W2 or new trajectory after a concrete external mismatch, callback, handoff, or rebinding failure. |
| 2026-agent-world-interface-overlay | superseded | historical Edge and Link derivation | Preserve as history; active work belongs to Task-to-World Interaction. |
| 2026-agent-native-adversarial-systems | deferred | Round 1 evidence and deferred strategic Security research source | Consume the completed Round 1 method and negative abstraction result; resume only with held-out opponent policies, deliberate Context loss, and Host/Harness replacement. |
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
- Every completed experiment ends in one of: `retain`, `localize`, `shrink`, `defer`, or `delete`.
- `active` is a WIP state, not a statement of importance. `deferred` preserves a valid question without consuming current execution bandwidth.
- Historical evidence is retained through `completed`, `superseded`, or `frozen`; it does not remain in the Ready Frontier.
