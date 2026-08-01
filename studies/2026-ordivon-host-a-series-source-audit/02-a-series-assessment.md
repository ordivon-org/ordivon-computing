# 02 — A0–A16 Assessment

## A0 — stable responsibilities across model and Harness change

**Assessment: substantially passes.**

The Harness extraction removed Provider and Agent-loop implementation from Host without replacing Task/Journal/CAS continuity. Preserve this boundary.

## A1 — inherit the classical substrate

**Assessment: passes with one regression.**

SQLite, filesystem CAS, Git and Runtime remain authoritative. Dynamic Enum mutation is unnecessary custom machinery and should be replaced by an immutable value type.

## A2 — cognition proposes; owning layers admit truth and commitment

**Assessment: fails in generic Effect completion and Goal result application.**

Caller-supplied outcome status and result-item status can override retained failure or rejected verification.

## A3 — purpose and commitment belong to identifiable participants

**Assessment: partial.**

TaskDescriptor binds assignee/provider/domain references. Host does not yet own durable Goal purpose or commitment despite architecture and ownership-table language.

## A4 — open Goals lower through revisable work

**Assessment: partial.**

Open proposal lowering exists. Task revision exists. Terminal Task reopening currently mutates the same Task identity rather than expressing revised work through a new Attempt/Task.

## A5 — work outlives cognition and execution episodes

**Assessment: strong substrate, failed concurrency edge.**

Fresh-process reconstruction and durable Dispatch identity are proven. Lease admission and generic recovery integration are incomplete.

## A6 — Context is a compiled view

**Assessment: passes.**

CompiledContext is separate from Task truth, bounded, persisted before invocation and reloaded across processes.

## A7 — capability and consequence remain separate

**Assessment: mostly passes.**

Capability profiles and consequence lowering are separate. Default state/token permissions do not protect the resulting private evidence boundary.

## A8 — reversible exploration by default; durable consequence explicit

**Assessment: passes structurally, partial operationally.**

Runtime Workspaces and explicit Dispatch preparation are sound. Evidence and state files need an explicit privacy profile.

## A9 — Effects are first-class commitments

**Assessment: strong identities, failed outcome admission.**

Effect/Binding/Dispatch/UNKNOWN separation is a major strength. Generic completion and reversible terminal state undermine the final commitment boundary.

## A10 — evidence mediates knowledge admission

**Assessment: fails in four places.**

- code-change evidence is not bound to commit-time Workspace state;
- rejected joint verification can advance a Task;
- failed generic delivery can become completed;
- causal provenance can dangle.

## A11 — every durable constraint proves net acceleration and deletion condition

**Assessment: fails for several surfaces.**

PROPOSED, WAKEUP, Goal Stream, expectedObservationKind and ownership-table entries lack production consumers or executable semantics.

## A12 — cooperation preserves agency, refusal and exit

**Assessment: not yet proven.**

CANCELLED exists but no cross-participant refusal/exit protocol is implemented. This is acceptable if not claimed as complete.

## A13 — new layers require an unowned non-bypassable responsibility

**Assessment: fails for the current generic EffectLifecycleHost promotion.**

It has no external consumer, no unified recovery integration and does not replace the three existing lifecycle implementations.

## A14 — knowledge advances through evidence and deletion

**Assessment: partial.**

The repository has strong immutable evidence. Dangling causal links and dead ownership surfaces should be enforced or deleted.

## A15 — judgment directs open work; a passed check proves only its property

**Assessment: violated by prior confidence, not by the basic design.**

154 passing tests did not cover failed generic completion, concurrent EventKind construction, lease takeover, terminal reopening or verification TOCTOU. The test suite must add adversarial trajectory tests rather than only more happy-path cases.

## A16 — chosen capability and freedom are the final constraint

**Assessment: directionally passes.**

Thin Host/Harness/Runtime separation supports replaceability. Correctness faults at commitment boundaries must be removed before adding more Host features.
