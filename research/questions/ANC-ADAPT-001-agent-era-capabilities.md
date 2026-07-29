# ANC-ADAPT-001 — Agent-Era Adaptation and Self-Evolution

## Question

How can an Agent system learn across Tasks, compile new capabilities, coordinate multiple cognitive participants, improve cognition quality, and evolve its own operating structure while increasing verified improvement per unit time and minimizing unrecoverable loss, unnecessary interruption, and permanent concentration of capability?

## Why this belongs in Ordivon Computing

Ordivon Runtime, Host, Protocol, Edge, Link, Game, and Security already explore durable execution, Effect semantics, world interfaces, recovery, multi-Agent workloads, and adversarial evaluation. The next missing capabilities are not owned by one product repository. They cut across the Agent-native computing model:

```text
past trajectories
→ reusable evidence
→ revised cognition and capability
→ reversible or isolated experiment
→ independent verification
→ promotion, negotiation, or rollback
→ broader and faster participation
```

This is therefore a Computing research question. Product repositories should provide workloads and evidence, not each invent an incompatible learning, Skill, coordination, or self-modification substrate.

## Triggering observation

The current Ordivon stack can preserve Tasks, bind Effects, execute Jobs, recover unknown outcomes, and verify world changes. It does not yet provide a shared answer to five higher-order Agent-era problems:

1. **Cross-task learning** — determining which decisions, Tools, providers, Task decompositions, and recovery strategies repeatedly succeed or fail.
2. **Dynamic capability compilation** — discovering Tool contracts, proposing new operations, composing them, validating them, and promoting verified compositions into reusable Skills.
3. **Multi-participant collaboration** — assigning Task and Effect responsibility, transferring work, joining independent branches, negotiating commitments, resolving conflicts, and verifying another participant’s Claims.
4. **Cognitive quality improvement** — detecting weak plans, unsupported conclusions, loops, stale world models, insufficient evidence, and situations requiring another model, verifier, resource owner, or institution.
5. **Self-evolution** — allowing Ordivon to use its own execution and evidence stack to propose, test, canary, observe, promote, or roll back changes to itself.

These are not requests for a monolithic autonomous super-Agent or a permanent governance bureaucracy. They are missing system semantics around adaptation, coordination, evaluation, and recoverable change.

## Current hypothesis

The minimum useful architecture is an evidence-driven acceleration pipeline:

```text
Task trajectories and world outcomes
→ typed Evidence and failure classification
→ evaluation against explicit objectives
→ candidate policy / Skill / architecture change
→ broad reversible exploration or isolated execution
→ independent Verification
→ bounded real-world commitment
→ continued observation
→ promotion, revision, negotiation, or rollback
```

The system should distinguish at least:

- **Fact learning** — admitting verified world knowledge;
- **strategy learning** — updating Task decomposition, provider choice, or recovery policy;
- **capability compilation** — turning verified Tool compositions into reusable Skills;
- **coordination learning** — revising responsibility, branch, handoff, negotiation, and Join rules;
- **system evolution** — changing Ordivon code, contracts, configuration, or deployment through the same Effect and Evidence discipline applied to external work.

No learning result becomes authority merely because a model proposed it, a person asserted it, an institution published it, or a correlation appeared in historical traces.

## Constraint principle

Adaptation is not improved by unrestricted irreversible mutation, but neither is it improved by making cognition weak or placing every reversible experiment behind approval.

```text
maximize internal capability and search
+ isolate or version reversible experiments
+ bind shared consequences explicitly
+ preserve evidence and rollback
```

Every persistent guard, approval, compatibility path, or promotion object must report its protected failure, measured cost, and deletion trigger.

## Required dependencies

This question depends on evidence from existing branches rather than replacing them:

- `ANC-MEMORY` must determine which durable trajectories and continuation records are sufficient for learning without replaying entire conversations;
- `ANC-EFFECT` and `ANC-IR` must preserve stable capability, Effect, result, and verification semantics;
- `ANC-HOST` must expose open Action Proposals, cognition decisions, and uncertainty without treating hidden model reasoning as authoritative state;
- `ANC-MULTI` and `ANC-ORG` must define responsibility, handoff, negotiation, review, refusal, and Join;
- `ANC-VERIFY` must provide evaluation, replay, counterfactual comparison, and promotion evidence.

## First evidence program

Use Ordivon Game and Ordivon Security as two deliberately different workload families.

1. Record normalized Task, Decision, ActionProposal, Effect, Observation, Verification, Outcome, cost, and failure trajectories.
2. Compare providers and policies on repeatable workloads without putting full conversations into long-term memory.
3. Identify one repeated Tool composition and compile it into a candidate Skill with an explicit contract and verification path.
4. Run independent Agent branches with explicit responsibility and Artifact-based Joins.
5. Detect one deliberately injected cognition failure such as unsupported completion, stale evidence, repeated non-progress, or contradictory plans.
6. Let Ordivon propose a small change to its own code or configuration, execute it in an isolated Workspace, run gates, deploy to a canary when consequence requires it, and either promote or roll back from observed evidence.
7. Measure whether each guard and approval step improves accepted outcomes or merely adds latency and interruption.

The program may be split into smaller experiments. The capabilities should remain connected by shared identities and evidence rather than becoming unrelated frameworks.

## Evidence required for progress

- learning improves a repeated workload without merely adding more context or model budget;
- the system can explain which prior Evidence changed a policy or Skill;
- a compiled Skill has a stable contract, capability profile, tests, and rollback path;
- multiple Agents make useful independent progress without duplicate Effects or ambiguous responsibility;
- cognition-quality controls detect known injected failures with acceptable false-positive and latency cost;
- a self-change follows proposal, reversible or isolated execution, Verification, observation, and promotion or rollback;
- replacing the model or Host session does not erase learned state or invalidate execution identity;
- negative results and regressions remain preserved rather than rewritten as success;
- useful capability becomes easier to access rather than more concentrated in one central gatekeeper.

## Non-goals

This question does not justify:

- silently increasing a participant’s authority over another participant’s resources;
- irreversible recursive self-modification without versioning, evidence, or recovery;
- treating all historical messages as memory;
- building a generic Skill marketplace before repeated local compositions exist;
- creating a second Runtime, Host, or evaluation framework inside each application;
- allowing model confidence, human status, or institutional authority to substitute for world evidence;
- optimizing for autonomous activity when stopping, negotiating, refusing, or requesting a responsible decision is the correct action;
- preserving compatibility, approval, or governance mechanisms that have no real consumer or measured net benefit.

## Related material

- [`ANC-MEMORY-001`](ANC-MEMORY-001-task-continuity.md)
- [`ANC-IR-001`](ANC-IR-001-agent-effect-ir.md)
- [`ANC-EFFECT-001`](ANC-EFFECT-001-tool-contract-evolution.md)
- [`ANC-ORG-001`](ANC-ORG-001-agent-native-organization.md)
- [`../../core/stack.md`](../../core/stack.md)
- [`../../knowledge/agents/goal-task-effect.md`](../../knowledge/agents/goal-task-effect.md)
- [`../../knowledge/institutions/plural-intelligence-organization.md`](../../knowledge/institutions/plural-intelligence-organization.md)
- [`../../studies/2026-adaptive-acceleration/README.md`](../../studies/2026-adaptive-acceleration/README.md)
- `ordivon-host`, `ordivon-runtime`, `ordivon-game`, `ordivon-security`, `ordivon-edge`, and `ordivon-link`
