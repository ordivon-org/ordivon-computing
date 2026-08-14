# Cross-project convergence: ownership, consequence, contraction, and the Ordivon self-loop

> **Status:** completed reference study. This study records cross-project evidence and does not itself authorize product or infrastructure changes.

## Purpose

This study interrupts a failure mode that can arise in a fast Agent-first project:

```text
local problem
→ local evaluator
→ local treatment
→ local interpretation
→ more local structure
→ another local problem
```

The loop is powerful. It is also an attractor. A project can become extremely good at optimizing the space it has already chosen while forgetting that sibling projects, prior contractions, mature external systems, or older negative evidence may already contain a better model of the problem.

The study therefore does **not** begin from one desired Game feature or one proposed shared layer. It reads the actual code and authority documents of the Ordivon project family, asks what each owner was forced to preserve, and compares the structures that survived repeated contraction.

The governing question is:

> Which ideas recur because they express a real responsibility, and which ideas recur only because Ordivon repeatedly invents similar scaffolding around local experiments?

The immediate trigger was Ordivon Game. After a productive G4 Product Value round, the project was ready to continue into bounded G5 Production. Instead of immediately expanding content, the development loop was stopped so that Game could be compared against the rest of Ordivon before another local optimization cycle began.

---

## Evidence boundary

This is a revision-bound comparative study. It does not copy owner truth into Computing.

The project revisions read were:

| Project | Revision read | Primary evidence |
| --- | --- | --- |
| Computing | `c96ba2cc73b651097443a38ff7a2431801efd217` | Core, promoted packages, research method, contraction evidence |
| Runtime | `761bfe8dd7ca7c5e3e514891657c986eecb204e5` | Rust execution model, SQLite state, MCP boundary, recovery tests |
| Host | `507589eb1ae602f788913c7a8fdfd7bad355fe6c` | Task/lease/checkpoint/Journal model, architecture and tests |
| Harness | `bb9f636cc4b533895254c0caf3e90eb083ca9e50` | Run/History/Cognition/Tool/Provider model, evals and contraction |
| World | `d36fa9e8764c89dd9c51dbef2727ebb13e7a9e27` | external trajectory bindings, provider adapters, UNKNOWN/reconciliation |
| Security | `2aba805e6ffe6c64ce0e0ebafce4240b61ef26a3` | law/profile/evaluator separation, CA0/CA5/CA6/CA7 evidence |
| Finance | `f3a3ff13077961620c8fb965506557e8947a6ecb` | capital semantics, execution/reconciliation kernels, compression work |
| Studio | `ad313efe289d36660e6643934ed5e3a586e5fab3` | production/media/review/perception model |
| Web | `c640e5af80727c7f7f35919257642776a8cdce10` | publication/editorial authority, public encounter, browser verification |
| Human | `f7725dfc9b391c3e9a0c509d49795994931c9d63` | Human-AI capability, evidence transport, contraction, task-search model |
| Game | `430ed2f77a18d925963de8a8cb1e6f32142655d7` | registered v2, unregistered v3, P0–P3, G4/Product Value, source/tests/Git history |

Where local, branch, and upstream revisions differed, they were treated as separate facts. This study does not infer that the newest checkout is automatically the strongest semantic authority.

---

# 1. Project-by-project irreducible cores

## Computing — responsibility admission before architecture

Computing has the largest research surface in the project family but a deliberately small promoted package surface.

Its most important distinction is:

```text
an abstraction can be useful
≠
an abstraction has earned shared infrastructure status
```

The promoted Observation Core exists only after materially different owners needed the same minimum contract. A broader Observation Plane was contracted away. `ordivon-protocol` preserves released compatibility while deleting a zero-current-consumer semantic-state candidate from the unreleased line.

Computing repeatedly asks:

```text
what recurring pressure exists?
who owns it today?
which simpler baseline fails?
what second materially different workload needs the same invariant?
what later condition deletes or localizes it?
```

**Irreducible core:** discover genuinely unowned responsibility and prevent local success from prematurely becoming global architecture.

**Contraction lesson:** research volume is not promotion evidence. Historical existence, elegant schema, test count, maturity, and hypothetical future use do not justify retention.

---

## Runtime — physical execution truth under uncertainty

Runtime does not own task meaning or domain completion. It owns the physical execution lifecycle once an operation has been admitted.

Its database treats uncertainty as state rather than an exception:

```text
succeeded
failed
timed_out
cancelled
lost
orphaned
```

The key separations are:

```text
Job ≠ Attempt
desired state ≠ observed resolution
dispatch issued ≠ result available
physical success ≠ semantic completion
```

Runtime also deliberately refuses to turn trusted-local execution into a universal security-policy platform. Stronger containment should be owned by a lower mechanism that actually provides it.

**Irreducible core:** preserve exact physical execution identity, evidence, cancellation, recovery, and uncertainty without overinterpreting process/transport events as semantic reality.

**Contraction lesson:** execution machinery should be deep where physical truth requires it, but it should not absorb domain semantics or duplicate mature isolation owners.

---

## Host — semantic work continuity across replaceable cognition

Host exists because semantic work must survive Agent, session, process, and Runtime replacement.

Its `WorkingCheckpoint` explicitly has truth role:

```text
semantic-working-claim
```

That wording matters. A checkpoint is not copied Git/Runtime/domain truth. It is a durable claim about the current frontier and where a future Agent must revalidate stronger owners.

Host keeps Task identity, revision, leases, commitments, uncertainty, verification references, and continuity. It does not become the owner of the external facts it references.

The Host kernel contracted away broader ambitions: generic scheduling, provider routing, workflow DSLs, and a generic Effect lifecycle were not retained without sufficient consumers.

**Irreducible core:** preserve semantic work identity and unresolved meaning across replaceable executors without becoming a second truth store.

**Contraction lesson:** persistence is justified when semantic continuity would otherwise be lost; persistence does not confer ownership.

---

## Harness — bounded cognition without a transcript machine

Harness preserves one bounded cognitive episode while resisting a very common collapse:

```text
History = current mind
```

Its durable distinctions include:

```text
Canonical History
Durable Cognition
Interaction Cognition
Attempt Cognition
Execution Control
Effects
```

and:

```text
History ≠ Cognition
Observation ≠ Retention
Storage ≠ Selection
Tool intent ≠ physical effect
physical effect ≠ semantic success
```

The model/Agent owns semantic selection. Harness owns structural identity, provenance, admission, replay, and recovery. It rejects generic automatic Memory/RAG, automatic relevance ranking, and other mechanisms that would silently choose the Agent's current world view for it.

`abstain` and no-change are first-class outcomes when no causal-red target is proven.

**Irreducible core:** preserve the structure and recoverability of bounded cognition while leaving semantic selection to the cognition owner.

**Contraction lesson:** more retained bytes and more automatic context are not necessarily more intelligence; evidence must earn decision value.

---

## World — durability begins at independently authoritative consequence

World is not a generic API aggregation layer. It owns the narrow boundary where another independent world can create a consequence that cannot safely be reconstructed from local intent alone.

Its recurring laws include:

```text
Provider success ≠ Task completion
Historical occurrence ≠ current Presence
Delivery ≠ cognition
Reconciliation precedes redispatch
```

The normal shape is:

```text
observe provider capability
→ bind exact request
→ persist before irreversible dispatch
→ deliver once
→ Receipt | UNKNOWN
→ reconcile by original identity
→ map provider evidence
→ domain owner interprets meaning
```

Pre-consequence `Observe → Query → Select` is intentionally disposable. World durability begins when consequence becomes non-recomputable.

**Irreducible core:** bind and reconcile cross-owner external trajectories without claiming provider or domain truth.

**Contraction lesson:** do not persist planning just because it can be represented; persist at the point where loss would make consequence ambiguous.

---

## Security — adversarial truth and evaluator humility

Security adds intelligent opposition and therefore exposes distinctions that non-adversarial systems can sometimes ignore.

Four rule classes are explicitly separate:

```text
Constitutional law
Authority/resource grant
Experiment profile/fixture
Evaluator judgment
```

A P0 no-network profile must not silently become a universal Security law. A score or finding interprets evidence; it does not become authority. The evaluator itself may be predictable, manipulated, corrupted, or lost.

CA5 formally concluded **not** to create a shared `RangeActionGateway`. CA7 formally concluded **not** to add Campaign, Organization, persistent OpponentModel, or Coevolution structures. CA6 showed that a thin deterministic adaptive policy matched the bounded outcome of a DeepSeek/Harness Agent in the tested arena.

**Irreducible core:** preserve causal, epistemic, and authority distinctions under active opposition while preventing experiment controls and evaluator judgments from becoming doctrine.

**Contraction lesson:** negative admission is a product of research. Model-backed success does not force model-native architecture.

---

## Finance — a semantic waist above irreversible capital machinery

Finance is structurally thick because money, fills, bills, venue state, and portfolio state are independently consequential and cannot be reconstructed from an Agent's story.

That thickness is split deliberately:

```text
below the waist
  exact effect identity
  venue-native observation
  order/fill/bill separation
  reconciliation completeness
  owner-capital attribution

above the waist
  observe
  research
  decide
  execute
  reconcile
  performance
  owner
```

The Primary Agent should reason in capital semantics, not protocol plumbing.

Finance also treats:

```text
wait
abstain
research
no-op
```

as complete decisions. Risk evidence normally changes judgment first; only true ownership or minimum-grounded-state failures should become hard authority blocks.

**Irreducible core:** connect owner-capital intent to independently reconciled financial consequence through a narrow semantic waist.

**Contraction lesson:** deep correctness machinery may be necessary below the waist; do not force the domain decision-maker to reason in that machinery's vocabulary.

---

## Studio — expression, perception, and transient critique

Studio owns expression production, not source-project facts.

The production path is:

```text
source owner fact
→ exact revision-bound Claim
→ editable expression
→ selected bytes
→ render / QC
→ craft judgment
→ human-response evidence only when the claim requires it
```

A polished or approved artifact does not grant Studio authority over its source claim.

Studio separates:

```text
mechanical/factual judgment
medium craft judgment
human experience judgment
```

and explicitly warns:

> machine-speed internal convergence is not human/culture/world truth.

Critique is transient by default. The durable consequence is normally the source diff, selected artifact, and scoped evidence—not every score, review turn, or hidden thought.

**Irreducible core:** preserve revision-bound expression and perception evidence without turning creative iteration into another truth store.

**Contraction lesson:** fast internal feedback should not create proportional persistent state; retain consequences, not every deliberative intermediate.

---

## Web — a public-consequence filter and encounter compiler

Web does not automatically mirror owner changes into public changes.

Its key law is:

```text
owner source changed
→ public review obligation
≠ automatic public mutation obligation
```

The publication loop is:

```text
bind owner revision
→ judge public consequence
→ no-op / correct / update / new argument / design experiment
→ preview
→ verify actual browser encounter
→ promote
```

Web also demonstrates:

```text
exposure ≠ comprehension
```

The same underlying facts can have different consequences when viewport order, reveal timing, or interaction path changes. The encounter is part of the artifact.

Feynman-style content work found that richer structural apparatus could consume more cognition without improving the next action. The default became the shortest causal path necessary for the next judgment.

**Irreducible core:** transform source-bound facts into deliberate public encounters while preserving owner authority and allowing no public change as a valid result.

**Contraction lesson:** downstream projection changes only when the downstream consumer's consequence changes; source mutation alone is insufficient.

---

## Human — external evidence first, residual local experiment second

Human resists the idea that more measurable human state implies a better Human model.

It separates:

```text
assisted output
joint human–AI capability
retained human capability
human agency / refusal / exit
```

An early large Human ontology was deleted in favor of a smaller question-driven dynamic model.

The most relevant contraction for this study is the corrected evidence order:

```text
credible external Human evidence
→ moderator / transport analysis
→ Ordivon-specific structural analysis
→ natural Human×Agent dogfood
→ direct residual experiment only if a real decision remains unresolved
```

A prepared experiment may be methodologically valid and still be the wrong next action. Existing evidence must be consumed before local retesting.

Human's Task-as-search model also makes the problem more durable than the current candidate solution:

```text
problem
constraints
established evidence
candidate solutions
frontier
rejected regions
unresolved regions
next information-gain actions
```

**Irreducible core:** maintain evidence-bounded claims about human capability, change, and agency with explicit transport/heterogeneity limits.

**Contraction lesson:** do not study the person because measurement is available; experiment locally only where external evidence stops and the residual changes action.

---

## Game — authoritative play, not an evaluation laboratory

Game's actual player-facing v3 waist is considerably narrower than its research and correctness surface.

The player loop is approximately:

```text
Commander intent
  objective / posture / formation / one remote capability / bounded contingencies
→ Generate Plan
→ inspect bounded specialist commitments and likely mission impact
→ Commit simultaneous Turn
→ authoritative consequence
→ Aftermath / plan review / debrief
→ next intent
```

The domain core beneath this waist is real and heavily consumed:

- authoritative World state and deterministic transition;
- faction-bounded Knowledge;
- legal Candidate/Intent admission;
- Commander intent;
- Plan/Preview/Commit separation;
- simultaneous Turn resolution;
- authoritative per-Intent feedback;
- bounded player projection;
- persistence/recovery needed for exact consequence and replay.

This resembles Finance: deep below-waist machinery can be justified because hidden information, simultaneous commitment, crash recovery, and replay correctness change the integrity of the actual game.

The research/development surface is different:

- P0/P1/P2/P3 phase contracts;
- G0–G8 lifecycle labels;
- fixture strategy matrix;
- live-Provider evaluator;
- G4 perception/calibration evaluator;
- Product Value evaluator;
- historical R/GX/AF/HP series.

These are useful construction and falsification tools. They are not additional gameplay layers.

**Irreducible core:** Game owns authoritative interactive world rules, player/Agent agency boundaries, content consequences, and the experienced play loop.

**Contraction lesson:** verification apparatus must remain below or outside the player semantic waist, and development/evaluation history must not become permanent product ontology merely because it is well tested.

---

# 2. Cross-project convergence laws

The following laws recur independently across multiple domains and are therefore stronger than any one project's local naming.

## Law A — structure must own a non-bypassable responsibility

A useful concept is not enough. A permanent shared structure must own a responsibility that existing owners cannot safely preserve locally.

Observed in:
- Computing promotion/deletion discipline;
- Host kernel contraction;
- Security CA5/CA7 negative admission;
- Game's own anti-platform rule;
- Finance semantic compression.

## Law B — persistence does not create authority

The fact that a repository or service retains bytes does not make it the owner of their meaning.

Observed in:
- Host checkpoints as semantic working claims;
- World provider receipts;
- Studio revision-bound claims;
- Web source bindings;
- Game replay/projections;
- Computing evidence snapshots.

## Law C — observation, proposal, action, consequence, and verification are different facts

Common collapse patterns are rejected repeatedly:

```text
observation ≠ truth
proposal ≠ authority
authority ≠ execution
execution ≠ consequence
consequence ≠ verification
verification in one scope ≠ completion in another
```

The exact intermediate objects differ by domain, but the separation is stable.

## Law D — uncertainty is a valid result

`UNKNOWN`, unresolved checkpoint state, pending review, abstention, or incomplete reconciliation should not be coerced into a confident binary result.

This recurs in Runtime, World, Security, Host, Finance, Harness, and Human research.

## Law E — no-op is a complete decision

Valid outcomes include:

```text
wait
abstain
research
no change
no public update
no new shared layer
no promotion
```

A system that structurally rewards only mutation will overbuild.

## Law F — durability begins at consequence or continuity loss

Do not persist every recomputable intermediate merely because it can be serialized.

World keeps pre-dispatch selection disposable. Studio keeps critique transient. Web keeps publication candidates in Git Workspace. Harness does not automatically promote attempt-local observations. Host persists semantic continuity because replacement would otherwise lose it. Runtime persists dispatch because physical ambiguity would otherwise become unrecoverable.

## Law G — evaluator judgment is not truth

Evaluators are scoped instruments. They can be underpowered, overfit, predictable, manipulated, or simply ask the wrong question.

Security makes this explicit, but the same issue appears in Game product evaluators, Studio visual review, Web browser checks, Finance simulation, and Human measurements.

## Law H — evidence should optimize decision value, not coverage

More observations, more retained context, more metrics, and more experiments can reduce clarity.

Harness rejects observation-count optimization. Human contracts experiments when external evidence already resolves the decision. Web prefers the shortest causal explanation. Computing deletes research apparatus after conclusions stabilize.

## Law I — promotion requires cross-pressure, not local success

A mechanism becomes reusable only after:

```text
one real pressure
+ failure of a simpler baseline
+ a second materially different consumer or condition
+ a clear owner
+ a deletion/localization rule
```

Game success alone cannot promote a Game mechanism into Ordivon infrastructure.

## Law J — fast internal convergence and slower world truth run on different clocks

Agent loops can iterate much faster than human learning, market response, public comprehension, adversarial adaptation, or cultural judgment.

The solution is not to slow the Agent to human speed. It is to separate timescales and require slower evidence only where the claim crosses into that slower world.

## Law K — a problem/search identity should outlive candidate solutions

Human Task-as-search, Host semantic checkpoints, Computing research questions, Security campaign questions, and Product development all benefit when the stable identity is the unresolved problem rather than the current implementation plan.

## Law L — negative knowledge needs durable representation

Deletion, non-admission, rejected regions, and failed baselines are not empty history. They prevent future work from re-entering already falsified space.

Git retains bytes, but merge ancestry alone is insufficient to preserve the *reason* a region was rejected. Cross-project continuity therefore needs explicit compact negative evidence, not only implementation diffs.

---

# 3. Deliberate divergences that should not be unified

Convergence does not imply one Ordivon framework.

## Runtime and Studio should have different durability profiles

Runtime must retain detailed attempt/dispatch/evidence state because physical effect ambiguity is expensive and sometimes irreversible.

Studio should not retain every critique turn because creative review is usually recomputable and persistence would create noise.

A shared “everything is an Event” architecture would destroy both owners' local optimum.

## Finance and Web should expose different semantic waists

Finance must preserve exact capital reconciliation below the waist but expose capital meaning above it.

Web normally has no reason to retain an execution ledger for every editorial consideration. Its public consequence filter can stay largely Workspace/Git based.

## Security needs stronger evaluator skepticism than ordinary product QA

An adversary can reason about and exploit the evaluator. A browser layout check normally does not face an adaptive opponent. The general law is scoped evaluator authority, not identical evaluator machinery.

## Host and World persist different kinds of continuity

Host persists semantic work because Agents/sessions are replaceable.

World intentionally leaves pre-consequence selection disposable and persists at external commitment.

One universal continuity store would conflate meaning with consequence.

## Human evidence cannot become the universal final gate

Human evidence is required for human claims, but it does not override physical truth, domain authority, or every product decision. Conversely, machine checks cannot establish human liking, learning, trust, or retention.

---

# 4. Game findings after the cross-project audit

## 4.1 The real Game semantic waist is healthy

The strongest surviving Game structures are not the research labels. They are the parts a player/Agent actually experiences through consequence:

```text
Authoritative World
Faction Knowledge
Commander Intent
Agent Candidate / legal Intent
Plan
Preview
Commit
simultaneous Turn consequence
owned feedback
Aftermath / later adaptation
```

The exact implementation may still contract, but these responsibilities have current consumers and direct gameplay meaning.

The Product Value round also demonstrated healthy subtraction: Loot policy was removed from the player surface after relevant-state tests found zero leverage, while protected-Actor semantics survived because targeted states showed real decision changes. That is the right pattern: a hypothesis can lose or regain admission based on current evidence.

## 4.2 P0–P3 are currently useful contracts, not permanent product ontology

The Game development model already says phase-coded files are historical work decomposition, not the player's loop or eternal architecture.

Today P0–P3 still serve a real purpose because v3 is an unregistered replacement path with exact contracts separate from registered v2. Once v3 is registered or otherwise stabilized, keeping phase identity in the normal product cognition path should be re-evaluated.

The correct long-term shape is likely:

```text
stable Product definition
+ stable World / persistence / planning contracts
+ historical P0–P3 derivation in Git/study evidence
```

not an ever-growing P4/P5/P6 architecture ladder.

## 4.3 Evaluators are instruments, not product authorities

The current v3 repository contains separate evaluators for:

- fixture strategic viability;
- live DeepSeek realization;
- G4 browser/perception calibration;
- Product Value/control/information/pressure analysis.

They have produced useful results. The cross-project lesson is that their outputs should change product decisions, not become another standing truth layer.

A healthy evaluator lifecycle is:

```text
question
→ scoped instrument
→ evidence
→ owner decision
→ retain instrument only if recurrence justifies its maintenance
```

not:

```text
every solved question
→ permanent evaluator suite
→ ever-growing required gate set
```

## 4.4 Game contains a concrete negative-knowledge lineage regression

This is the strongest code-level finding of the study.

At commit:

```text
22aa1ac  game: purge zero-causal Station Zero surface
```

Game deleted:

```text
src/station-zero-v3/resource-egress.ts
src/station-zero-v3/message-issuance.ts
src/station-zero-v3/entity-departure.ts
+ dedicated tests
```

The associated Existence Audit had already established:

```text
current production consumers = none
```

and explicitly classified the three modules as critical `DELETE / defer outside current product` candidates under a future-primitive law.

That commit is **not an ancestor** of current Game `430ed2f`.

During the later lineage reconciliation:

```text
b336f8d  merge: reconcile local and canonical main
```

nearly 4,000 lines were reconciled into that line, including these three cross-World modules. They currently have:

```text
public export through index.ts
+ dedicated tests
- no PlayService consumer
- no /v3 Server route
- no browser consumer
- no current product-document consumer
```

Current-vs-purge difference for just these modules/tests is roughly 1,435 lines.

This is not evidence that Git is wrong. It is evidence that **byte-level merge/reconciliation does not preserve negative semantic decisions unless the negative decision itself is carried as durable evidence/current admission state.**

The earlier `STATION_ZERO_V3_EXISTENCE_AUDIT.md` is also absent from current Game.

## 4.5 Several old zero/near-zero defendants remain visible today

The lost Existence Audit also named other defendants. Static inspection of `430ed2f` shows several remain materially similar:

- `mark-prize` still writes a marked status without a downstream deterministic consumer found in the current source scan;
- `signal-jam` still drives `uplinkSlots = 0`, and the slots are restored without a clear downstream gameplay consumer;
- `brood-awakening` still modifies biomass-nest severity without a clear later World-law consumer;
- `vent-spread` still creates/increments a hazard whose downstream gameplay use is not established by the current static graph;
- `alertLevel` is updated and projected into Context/UI, but current deterministic scoring/World law does not consume it;
- `reportIds` are retained/projected into Agent Context, while the DeepSeek adapter does not currently consume the field;
- `collateralPolicy` remains an internal Order/Provider field even though the later Product Value audit correctly stopped surfacing it as a current player control.

These are **contraction candidates**, not automatic deletions. A later consumer may now exist that a static scan misses, or a human/explanation use may justify one. The old audit's job is to restore burden of proof, not to become immutable law.

`protectedActorId` demonstrates why this distinction matters: it was an earlier suspect, but the later Product Value relevant-state audit found contextual decision leverage and therefore produced new evidence for retention.

## 4.6 Development metadata has leaked into runtime vocabulary

`StationZeroP0Contract` contains both runtime-relevant facts and design-history metadata such as:

```text
product form
player/Agent responsibility prose
roguelite / tactical-RPG / sandbox / systemic-sim / character-sim influences
retained/rejected mechanic lists
non-goals
```

In current runtime code, the main behaviorally consumed part is the encounter budget/contract facts; the design-influence metadata is primarily tested and retained as design evidence.

This is not a correctness bug, but it increases the product-core cognitive surface. The Finance/Web/Computing pattern suggests a future contraction should separate:

```text
runtime/content contract
from
design derivation / historical influence record
```

once the target stabilizes.

---

# 5. A corrected Ordivon self-loop

The old local loop remains useful:

```text
observe
→ hypothesize
→ smallest treatment
→ execute
→ observe consequence
→ retain / shrink / delete
```

The correction is not to replace it with a giant global process. The correction is to nest it inside a slower **cross-owner interruption loop**.

## Fast loop — owner-local consequence loop

Use for ordinary execution and bounded improvement:

```text
1. Frame one decision-relevant local problem.
2. Identify the owner of the relevant truth/consequence.
3. Search current local evidence and negative history.
4. Choose the smallest credible baseline/treatment.
5. Execute through owner-native authority.
6. Observe the consequence at the correct boundary.
7. Retain, contract, delete, abstain, or leave unchanged.
```

This loop should remain cheap and frequent.

## Slow loop — cross-project world-model interruption

Do not run this after every local edit. Trigger it when local optimization is at risk of becoming an attractor.

Suggested triggers:

- a new permanent type/service/table/protocol/evaluator is proposed;
- a local research series has produced several consecutive new structures without comparable deletion;
- a lifecycle stage changes, such as prototype → vertical slice or slice → production;
- an owner boundary changes;
- a merge/reconciliation crosses materially different research lineages;
- a local problem resembles a responsibility another project already owns;
- the same failure is being instrumented for a second or third time;
- a new shared abstraction is proposed;
- the expected information gain of another local experiment becomes low.

Then run:

```text
A. Restate the stable problem, not the current solution.
B. Query sibling projects and mature external mechanisms/evidence.
C. Recover rejected regions / deletion evidence / earlier baselines.
D. Compare responsibility and consequence boundaries.
E. Ask whether the current local abstraction is still the smallest owner-local answer.
F. Revise the world model or research frontier.
G. Return to the fast loop only for the residual uncertainty that still changes action.
```

This is an **open spiral**, not a closed local circle:

```text
local consequence
      ↑           ↓
cross-owner model ← external reality
```

The fast loop increases local resolution. The slow loop changes the coordinate system when evidence says the local search space itself is wrong.

---

# 6. Research-before-experiment order

Across Computing, Human, Security, Studio, Web, and Game history, a stronger order emerges:

```text
1. Existing owner truth and historical negative evidence
2. Mature external mechanism / research baseline
3. Cross-project analogous pressure
4. Static causal/consumer audit
5. Cheapest deterministic counterfactual
6. Real local dogfood
7. Live model / expensive provider test
8. Human/market test only for claims that actually cross into human/market truth
```

This ordering avoids two symmetric mistakes:

- **under-testing:** promoting a feature because it feels plausible;
- **over-testing:** building an elaborate local experiment for a question already answered by stronger existing evidence or a static zero-consumer fact.

---

# 7. Promotion and deletion contract

A local structure should graduate toward permanent/shared status only when it can answer all of:

```text
What exact responsibility does it own?
Which existing owner/simpler baseline fails?
What current consumer changes behavior because of it?
What independent second pressure confirms it is not local coincidence?
What consequence becomes ambiguous/wrong if it is removed?
What is the smallest semantic waist exposed to its user/Agent?
What evidence would contract or delete it later?
```

A deletion/negative decision should retain compact durable evidence:

```text
rejected region
reason
revision / experiment
reopen condition
```

The negative record should not become a universal constitutional ban. Its purpose is to prevent accidental rediscovery and lineage resurrection without renewed evidence.

---

# 8. Implications for Game — study conclusions, not implementation authorization

The cross-project study changes the likely next Game move.

The previous frontier was bounded G5 Production. The stronger current evidence says the next action should first be **a Game contraction/reconciliation pass**, because the current canonical line contains known historical negative-space drift.

A bounded follow-up should therefore begin with:

```text
Game canonical 430ed2f
vs
lost Existence Audit / contraction lineage
vs
current Product Value evidence
```

and classify each disputed structure as:

```text
KEEP
CONTRACT
DELETE
DEFER-OUTSIDE-CURRENT-PRODUCT
REOPEN-WITH-NEW-EVIDENCE
```

High-confidence first candidates for review:

1. the three no-current-consumer cross-World modules and their public exports/tests;
2. static zero/near-zero mechanics retained from the old Existence Audit;
3. design-history metadata currently mixed into runtime contracts;
4. evaluator scripts that no longer answer a recurring decision;
5. phase-coded documentation that should eventually collapse after v3 registration/stabilization.

This is **not** a command to delete all five categories immediately. The purpose of the study is to restore the correct burden of proof and negative history before G5 expands the tree further.

The core Game loop and its deep correctness machinery are not challenged by this result. The strongest Game structures are precisely those the other projects predict should survive:

```text
world authority
bounded knowledge
legal agency
explicit commitment
irreversible consequence
owned feedback
recoverable history where ambiguity would matter
narrow player semantic waist
```

---

# 9. Broader Ordivon consequence

The project family is converging on a general operating style without converging on one framework:

> **Keep owner-native mechanisms deep where reality forces them, expose the smallest domain-semantic waist, let local loops run quickly, but periodically interrupt them with cross-owner evidence, negative history, and external baselines before local success hardens into architecture.**

The resulting shape is not:

```text
one universal Ordivon stack
```

It is closer to:

```text
many strong owners
+ exact consequence boundaries
+ explicit evidence transport
+ sparse promoted cross-owner contracts
+ durable negative knowledge
+ fast local loops
+ slower world-model revision
```

That is a stronger interpretation of Agent-first development than simply making iteration faster.

Speed without interruption finds local optima quickly.

The Ordivon advantage should be:

> **fast local search plus the ability to change the search space before local success becomes dogma.**

---

## Status and next boundary

This study is complete as comparative evidence.

It does **not**:

- modify Game behavior;
- reactivate old Computing research lines;
- promote a new shared service/protocol;
- register Station Zero v3;
- revoke G5 as a lifecycle concept;
- claim every historical deletion remains correct forever.

It does establish a stronger next research boundary:

```text
before more Game production breadth,
reconcile current Game against its own lost contraction evidence
and the cross-project convergence laws above.
```

Only the residual structures that survive that pass should become inputs to the next Game production cycle.
