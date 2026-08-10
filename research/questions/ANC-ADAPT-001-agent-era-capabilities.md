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

## P1 evidence update

The first admitted self-evolution evidence did not require waiting for Game/Security or constructing a shared adaptation platform. Computer P1 used current P0 evidence as its own bounded self-customer and changed two research-local policies under independent held-out evaluation and rollback:

1. `campaign_declared_evidence_v2` replaced the false universal requirement that every Trial must have Observation-plane completeness. On 20 development trajectories it removed 18 false exclusions with zero false inclusions, then passed all 5 frozen holdout trajectories. The promoted revision was independently reverted in a fresh Runtime Workspace and the preceding CEL test state passed.
2. The improved loop then selected `capability_evidence_v1` to replace historical phase-name readiness with exact capability evidence. It passed all 5 development cases and both frozen holdout cases, including leave-one-capability-out fail-closed controls. That second-generation revision was also independently reverted and the first-generation test state passed.

This satisfies the **self-evolution** slice of this question at bounded M4 evidence: Ordivon Computing changed its own research-selection and prerequisite policies through versioned evidence, isolated execution, independent evaluation, promotion, and rollback, then used the improved loop to drive another change to itself.

It does not satisfy the whole umbrella question. Skill compilation, multi-participant adaptation, materially different workload transfer, and open-ended recursive improvement remain unproven. The next falsifier should therefore come from a materially different self-change or owner-native workload, not from adding more infrastructure to the same P0 corpus.

The current machine closeout is [`../experiments/experiment-loop-v0/p1-bounded-rsi-closeout.json`](../experiments/experiment-loop-v0/p1-bounded-rsi-closeout.json), with current plan [`../experiments/experiment-loop-v0/plan-v5.json`](../experiments/experiment-loop-v0/plan-v5.json).

## P2 cross-evidence-family update

P2 tested whether the improved self-research loop transferred beyond the P0 Trial/Provider evidence family. The falsifier came from Computing's own world-model observation method: the retained Round 001 frontier still contained structurally valid Git revisions, but 9 of 10 owner repositories had advanced while the structural checker could still report `OK`.

`git_relation_freshness_v2` separates historical observation validity from currentness and classifies `exact`, `owner_advanced`, `checkout_behind_observation`, `diverged`, and `observed_unavailable`. Revision movement creates review pressure only; it does not automatically revise the shared world model. Against 7 development owners, the old syntax-only rule produced 6 false-current decisions while the new policy was 7/7 with no false-current or false-stale decisions. The frozen Harness/Studio/Web holdout was 3/3. The promotion was then reverted in an independent Runtime Workspace and the preceding 26 CEL tests plus the world-model checker passed.

This raises the self-evolution slice to **M5**: the improved loop survived a materially different cross-project evidence family and a third reversible self-change. It still does not complete `ANC-ADAPT-001`; Skill compilation, multi-participant adaptation, and open-ended recursive capability growth remain unproven.

## P3 Skill-compilation falsification

P3 tested the first natural dynamic-capability candidate rather than constructing a generic Skill system. Runtime history exposed repeated response-loss/`UNKNOWN` reconciliation across durable execution, Workspace open/patch/mutate, Host checkpoints, and external effects. A deterministic compiler therefore produced `skill:reconcile-before-redispatch:v1`, while a negative ownership control correctly rejected source landing/publication as Git/Runtime mechanics plus explicit consequence authority rather than a Skill.

The first 25 live DeepSeek trajectories suggested that the compiled procedure could alter behavior, but its evaluator contained synonymous action labels and an ambiguous redispatch boolean. That entire selection was invalidated and frozen rather than rescored. The Skill bytes were left unchanged. A second evaluator exposed the same operation-specific Tool contract facts to both treatments, removed the ambiguous boolean, froze five new holdout cases, and ran another 25 Provider trajectories. The strong baseline scored **8/10** development at 11,852 tokens; the Skill scored **6/10** at 14,618 tokens, about 23% more. Both had zero dangerous blind retries. Baseline then passed only **3/5** frozen holdout cases, so neither treatment established a stable recovery capability.

The Skill candidate is therefore **rejected, not promoted**. This does not show that capability compilation is generally useless. It falsifies a narrower and important hypothesis: repeated procedure text plus real incident provenance is not enough to become a Skill when current Tool contracts already expose the decisive facts. A useful Skill must add stable decision value beyond those contracts without duplicating Tool/Runtime/Host authority. No Skill repository, runtime, marketplace, registry, or new execution surface is authorized.

`ANC-ADAPT-001` remains at **M5** because P2's cross-evidence self-reform evidence still stands, but dynamic Skill compilation remains unproven. The next adaptation falsifier is `ANC-MULTI-001`.

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
- [`../experiments/experiment-loop-v0/`](../experiments/experiment-loop-v0/) — bounded file/Git CEL with P1 first- and second-generation self-change evidence; supports only the self-evolution slice and does not imply open-ended RSI.
- `ordivon-host`, `ordivon-runtime`, `ordivon-game`, `ordivon-security`, and `ordivon-world`
