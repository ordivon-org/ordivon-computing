# Ordivon Research Portfolio

> Generated from [`portfolio.json`](portfolio.json). Edit the JSON source, then rerun `python3 scripts/render_research_portfolio.py`.

- **As of:** `2026-07-30`
- **Active research-line limit:** `2`
- **Current active lines:** `2`

The portfolio is the single source of truth for research status, maturity, blockers, next falsifier, and Ready Frontier. Question pages preserve stable hypotheses and experiment contracts; Issues preserve discussion and execution history.

## Active research lines

| Line | Priority | Question | Items | Implementation | Exit criterion |
|---|---|---|---|---|---|
| R-A-HARNESS-CONTROL | P0 | Harness composition, completion, and calibrated non-action | ANC-HARNESS-001, ANC-VERIFY-002 | ordivon-computing#83, ordivon-host#14, ordivon-runtime#64, ordivon-game#58, ordivon-security#19 | Two live Harnesses, one mid-Task replacement, CompletionProposal validation, stale-worker fencing, and paired act/abstain trajectories produce a retain/localize/shrink/delete decision. |
| R-B-WORLD-EFFECT | P1 | Task-to-World continuity and Effect-contract decision | ANC-WORLD-002, ANC-EFFECT-001 | ordivon-computing#78, ordivon-computing#6, ordivon-world#1, ordivon-world#2 | A structurally different external Provider path competes with direct Host integration under ambiguous delivery and rebinding, then World and Effect fields are retained, absorbed, shrunk, or deleted. |

## Question and track portfolio

### Reference

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-STACK-001 | M5 | reference | ordivon-computing | — | — | Use as the admission test; reopen only on contradictory evidence. | A cross-workload failure reveals a necessary responsibility absent from the current substrate/overlay split. |

### Active

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-HARNESS-001 | M2 | P0 | ordivon-computing | R-A-HARNESS-CONTROL | — | Execute two-Harness, replacement, CompletionProposal, Hook/Event, lease, and fencing experiments. | Direct Provider integration remains simpler and equally correct, or a common interface destroys material Provider capability. |
| ANC-VERIFY-002 | M2 | P0 | ordivon-computing | R-A-HARNESS-CONTROL | ANC-HARNESS-001 | Run as a fault family inside R-A instead of building a separate control platform. | A simpler paired act/abstain or static policy achieves equal authorized utility, timing, and recovery with fewer states. |
| ANC-WORLD-002 | M2 | P1 | ordivon-world | R-B-WORLD-EFFECT | — | Run W1/W2 against direct integration and force a retain, absorb, shrink, or delete decision. | Direct Host/Provider integration preserves uncertainty, provenance, rebinding, and recovery with less permanent machinery. |
| ANC-EFFECT-001 | M4 | P1 | ordivon-computing | R-B-WORLD-EFFECT | ordivon-world#1 | Do not generalize Tool ABI until World supplies a structurally different real backend. | Stable request identity, Provider receipts, and durable Activities match the second-backend outcome with fewer semantic objects. |

### Blocked

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-ADAPT-001 | M1 | P3 | ordivon-computing | — | ANC-VERIFY-001, 20-50-homogeneous-task-trajectories | Collect comparable trajectories first; later change only one Skill, Context policy, or stopping policy through replay, shadow, canary, and rollback. | A versioned Skill or Context-policy change fails held-out Tasks or cannot beat a fixed baseline after rollback costs. |
| ANC-SECURITY-005 | M0 | P3 | ordivon-security | — | ANC-SECURITY-003, ANC-SECURITY-004, ANC-MULTI-001 | No implementation until single-actor strategic and opponent-model hypotheses survive. | Ordinary Host delegation and branch/join plus domain-local trust fields explain the first compromise scenario. |
| ANC-SECURITY-006 | M0 | P3 | ordivon-security | — | ANC-SECURITY-003, ANC-SECURITY-004, ANC-SECURITY-005, ANC-VERIFY-001 | No platform or training loop until the unit of strategic evaluation is proven. | Held-out static-opponent evaluation predicts the same architecture decisions as coevolution with lower cost. |

### Deferred

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-COMPILER-001 | M1 | P2 | ordivon-computing | — | — | Do not implement an Agent VM; revisit only after a minimal branch/join failure. | An ordinary Host Task Graph, queue, reducer, and workflow backend express the first branch/join workload without an Agent VM. |
| ANC-MULTI-001 | M1 | P2 | ordivon-computing | — | — | After R-A/R-B, run one Goal, two independent Tasks, two Artifacts, and one deterministic Join. | A single Agent plus independent verifier matches two-branch quality and cost, or ordinary Task Graph semantics are sufficient. |
| ANC-VERIFY-001 | M1 | P2 | ordivon-computing | — | — | Use local receipts; extract a shared Eval Envelope only after R-A, R-B, and one branch/join experiment. | Three real experiments do not share enough stable evidence fields to justify common Eval infrastructure. |
| ANC-ORG-001 | M1 | P3 | ordivon-computing | — | ANC-MULTI-001, real-operator-attention-traces | Remain an umbrella; derive objects only from real operator and multi-Agent trajectories. | Host-local DecisionRequests and ordinary Task/participant relations explain observed coordination without a new organization layer. |
| ANC-SECURITY-001 | M1 | P2 | ordivon-security | — | — | Keep as umbrella; activate only the minimal Campaign/opponent experiment after WIP capacity frees. | Mature simulation, MARL, cyber evaluation, and thin adapters express the strategic distinctions without a new shared layer. |
| ANC-SECURITY-003 | M1 | P2 | ordivon-security | — | — | Prepare one minimal dynamic-opponent experiment only after R-A/R-B free capacity. | A scripted or ordinary Goal/Task policy matches explicit Campaign state on policy-switch and held-out-opponent cases. |
| ANC-SECURITY-004 | M1 | P2 | ordivon-security | — | — | Pair with ANC-SECURITY-003 in one minimal experiment; do not build a general epistemic system. | A reactive policy without explicit opponent hypotheses matches held-out policy-switch performance and evidence quality. |

### Completed

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-IR-001 | M5 | reference | ordivon-computing | — | — | Consume EffectEnvelope v1; extend only through ANC-EFFECT-001 evidence. | A second interface family cannot preserve Effect meaning with the current envelope and Binding projection. |
| ANC-MEMORY-001 | M4 | reference | ordivon-computing | — | — | Consume TaskCapsule evidence; do not create a general memory runtime. | A materially different workload cannot continue from bounded semantic state without transcript or Provider Session state. |
| ANC-HOST-001 | M4 | reference | ordivon-host | — | — | Product evolution belongs to ordivon-host; shared changes require new cross-workload evidence. | A real workload requires durable cognition state that cannot remain a Provider Harness concern or Host application schema. |
| ANC-GAME-001 | M4 | reference | ordivon-game | — | — | Original boundary is closed; Game #58 now serves R-A as a deterministic laboratory. | A second game family requires a generic responsibility absent from one Host plus Game-owned World and replay semantics. |

### Superseded

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-SECURITY-002 | M2 | reference | ordivon-computing | — | — | Use only as historical substrate evidence. | None; historical comparison is retained. |
| ANC-EDGE-001 | M2 | reference | ordivon-computing | — | — | Historical only. | None; the split was an intermediate derivation. |
| ANC-LINK-001 | M2 | reference | ordivon-computing | — | — | Historical only. | None; the split was an intermediate derivation. |
| ANC-WORLD-001 | M2 | reference | ordivon-computing | — | — | Historical only. | None; composition analysis produced the unified question. |

### Frozen

| ID | Maturity | Priority | Owner | Active line | Blocked by | Next action | Next falsifier |
|---|---|---|---|---|---|---|---|
| ANC-KERNEL-001 | M5 | reference | ordivon-computing | — | — | Accept only bug fixes, regression evidence, or newly demonstrated universal invariants. | A cross-framework failure requires a universal invariant that cannot remain in Host, Runtime, Tool contracts, or a domain World. |

## Programs

| Program | Issue | Kind | Status | Disposition | Next action |
|---|---|---|---|---|---|
| ANC-MACHINE-V0 | #1 | research_program | active | retain_as_parent | Use the generated portfolio as the Ready Frontier. |
| PERSONAL-DEVELOPER-RELIABILITY | #44 | operational_program | active | retain_as_operational_program | Continue only work that removes repeated operating friction. |
| STRATEGIC-ADVERSARIAL-SYSTEMS | #46 | research_program | deferred | retain_as_deferred_umbrella | Do not activate organization or coevolution before a minimal dynamic-opponent experiment. |
| EXTERNAL-BASELINE-VALIDATION | #56 | research_method_program | completed | absorb_into_research_method | Close after Round A; child Issues retain unfinished experiments. |
| PLURAL-INTELLIGENCE-ALIGNMENT | #63 | alignment_program | completed | absorb_into_core_registry_and_children | Close after Round A; remaining implementation stays in owning repositories. |

## Studies

| Study | Status | Role | Next action |
|---|---|---|---|
| 2026-computing-stack-walkthrough | reference | physical-to-institutional learning map | Revise only after a material computing-paradigm change. |
| 2026-classical-to-agent-native-computing | reference | layer-admission and deletion framework | Use as the default admission test. |
| 2026-adaptive-acceleration | reference | published normative position | Revise only after substantive evidence, critique, or position change. |
| 2026-agent-system-concept-system | active | canonical terminology and Harness-boundary source | Consume through R-A; do not create a Harness repository before its promotion gate. |
| 2026-task-to-world-interaction | active | canonical World and Effect research source | Consume through R-B and force an architecture disposition after the second backend. |
| 2026-agent-world-interface-overlay | superseded | historical Edge and Link derivation | Preserve as history; active work belongs to Task-to-World Interaction. |
| 2026-agent-native-adversarial-systems | deferred | strategic Security research source | Start only the minimal Campaign/opponent experiment after active-line capacity is free. |

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
- Every completed experiment ends in one of: `retain`, `localize`, `shrink`, `defer`, or `delete`.
- `active` is a WIP state, not a statement of importance. `deferred` preserves a valid question without consuming current execution bandwidth.
- Historical evidence is retained through `completed`, `superseded`, or `frozen`; it does not remain in the Ready Frontier.
