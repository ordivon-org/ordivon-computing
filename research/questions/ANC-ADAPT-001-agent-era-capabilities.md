# ANC-ADAPT-001 — Agent-Era Adaptation and Self-Evolution

## Question

How can an Agent system learn across tasks, compile new capabilities, coordinate multiple cognitive actors, regulate cognition quality, and improve its own operating structure without surrendering evidence, authority boundaries, reversibility, or human control?

## Why this belongs in Ordivon Computing

Ordivon Runtime, Host, Protocol, Edge, Link, Game, and Finance already explore durable execution, Effect semantics, world interfaces, recovery, and domain workloads. The next missing capabilities are not owned by one product repository. They cut across the Agent-native computing model:

```text
past trajectories
→ reusable evidence
→ revised cognition and capability
→ bounded experiment
→ independent verification
→ controlled promotion or rollback
```

This is therefore a Computing research question. Product repositories should provide workloads and evidence, not each invent an incompatible learning, Skill, coordination, or self-modification substrate.

## Triggering observation

The current Ordivon stack can preserve Tasks, bind Effects, execute Jobs, recover unknown outcomes, and verify world changes. It does not yet provide a shared answer to five higher-order Agent-era problems:

1. **Cross-task learning** — determining which decisions, tools, providers, task decompositions, and recovery strategies repeatedly succeed or fail.
2. **Dynamic capability compilation** — discovering Tool contracts, composing Operations, validating them, and promoting verified compositions into reusable Skills.
3. **Multi-Agent ownership and collaboration** — assigning Task and Effect ownership, transferring work, joining independent branches, resolving conflicts, and verifying another Agent's claims.
4. **Cognitive quality control** — detecting weak plans, unsupported conclusions, loops, stale world models, insufficient evidence, and situations requiring another model or human judgment.
5. **Self-evolution** — allowing Ordivon to use its own execution and evidence stack to propose, test, canary, observe, promote, or roll back changes to itself.

These are not requests for a monolithic autonomous super-Agent. They are missing system semantics around adaptation, coordination, evaluation, and controlled change.

## Current hypothesis

The minimum safe architecture is not an unrestricted memory or self-modifying loop. It is an evidence-governed adaptation pipeline:

```text
Task trajectories and world outcomes
→ typed Evidence and failure classification
→ evaluation against explicit objectives
→ candidate policy / Skill / architecture change
→ isolated execution and fault injection
→ independent Verification
→ bounded promotion
→ continued observation
→ rollback when evidence degrades
```

The system should distinguish at least:

- **Fact learning** — admitting verified world knowledge;
- **strategy learning** — updating task decomposition, provider choice, or recovery policy;
- **capability compilation** — turning verified Tool compositions into reusable Skills;
- **coordination learning** — revising ownership, branch, handoff, and join rules;
- **system evolution** — changing Ordivon code, contracts, configuration, or deployment through the same Effect and Evidence discipline applied to external work.

No learning result becomes authority merely because a model proposed it or because a correlation appeared in historical traces.

## Required dependencies

This question depends on evidence from existing branches rather than replacing them:

- `ANC-MEMORY` must determine which durable trajectories and Task Capsules are sufficient for learning without replaying entire conversations;
- `ANC-EFFECT` and `ANC-IR` must preserve stable capability, Effect, result, and verification semantics;
- `ANC-HOST` must expose cognition decisions and uncertainty without treating hidden model reasoning as authoritative state;
- `ANC-MULTI` and `ANC-ORG` must define ownership, handoff, review, and responsibility;
- `ANC-VERIFY` must provide evaluation, replay, counterfactual comparison, and promotion evidence.

## First evidence program

Use Ordivon Game and Ordivon Finance as two deliberately different workload families.

1. Record normalized Task, Decision, Effect, Observation, Verification, Outcome, cost, and failure trajectories.
2. Compare providers and policies on repeatable workloads without putting full conversations into long-term memory.
3. Identify one repeated Tool composition and compile it into a candidate Skill with an explicit contract and verification path.
4. Run independent Agent branches with explicit ownership and Artifact-based joins.
5. Detect one deliberately injected cognition failure such as unsupported completion, stale evidence, repeated non-progress, or contradictory plans.
6. Let Ordivon propose a small change to its own code or configuration, execute it in an isolated Workspace, run gates, deploy only to a canary, and either promote or roll back from observed evidence.

The program may be split into smaller experiments. The five capabilities should remain connected by shared identities and evidence rather than becoming five unrelated frameworks.

## Evidence required for progress

- learning improves a repeated workload without merely adding more context;
- the system can explain which prior Evidence changed a policy or Skill;
- a compiled Skill has a stable contract, bounded authority, tests, and a rollback path;
- multiple Agents make useful independent progress without duplicate Effects or ambiguous ownership;
- cognition-quality controls detect known injected failures with acceptable false-positive cost;
- a self-change follows proposal, isolated execution, Verification, canary, observation, and promotion or rollback;
- replacing the model or Host session does not erase learned state or invalidate execution identity;
- negative results and regressions remain preserved rather than being rewritten as success.

## Non-goals

This question does not justify:

- unrestricted recursive self-modification;
- silently increasing an Agent's authority;
- treating all historical messages as memory;
- building a generic Skill marketplace before repeated local compositions exist;
- creating a second Runtime, Host, or evaluation framework inside each application;
- allowing model confidence or eloquence to substitute for world evidence;
- optimizing for autonomous activity when stopping, escalating, or asking for judgment is the correct action.

## Related material

- [`ANC-MEMORY-001`](ANC-MEMORY-001-task-continuity.md)
- [`ANC-IR-001`](ANC-IR-001-agent-effect-ir.md)
- [`ANC-EFFECT-001`](ANC-EFFECT-001-tool-contract-evolution.md)
- [`ANC-ORG-001`](ANC-ORG-001-agent-native-organization.md)
- [`../../core/stack.md`](../../core/stack.md)
- [`../../knowledge/agents/goal-task-effect.md`](../../knowledge/agents/goal-task-effect.md)
- [`../../knowledge/institutions/human-agent-organization.md`](../../knowledge/institutions/human-agent-organization.md)
- Ordivon Host, Runtime, Game, Finance, Edge, and Link
