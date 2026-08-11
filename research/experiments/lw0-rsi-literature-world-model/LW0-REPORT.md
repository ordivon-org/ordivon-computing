# LW0 — External RSI Evidence Reconciliation

## Result

LW0 built the first **Ordivon RSI Literature World Model** from a curated cohort of 23 primary technical sources spanning 23 research groups and 14 domain families.

The purpose was not to collect papers. It was to ask whether independent external research changes Ordivon's experimentally earned world model, and to test a higher-order hypothesis:

> useful/correct structures may converge toward a small stable set, while wrong mechanisms may be high-entropy and diverse.

The first-pass result is **partial support plus an important correction**.

### What converges strongly

Across materially different domains, successful systems repeatedly force the same semantic distinctions even when their architectures and terminology differ:

- representation / self-report / public metric / description / prediction is not realized reality;
- evaluators are fallible system components and need hidden, independent, anchored or state-grounded checks;
- improvement must generalize beyond the optimized signal;
- operator/search/harness policy must be conditional on task/evidence/world conditions;
- persistent state should preserve verified causal/provenance/constraint information rather than equal the raw growing transcript;
- adaptive orchestration/search/defense must repay its own overhead against a strong simpler baseline;
- recursive improvement must eventually measure future improvement ability, not only current task score.

The strongest normalized motifs in the cohort are:

| Motif | Independent groups | Domain families |
|---|---:|---:|
| generalization beyond optimized signal | 13 | 7 |
| reality / representation separation | 10 | 8 |
| evaluator integrity | 10 | 8 |
| conditional operator policy | 8 | 6 |
| metaproductivity | 6 | 3 |
| overhead must repay itself | 4 | 3 |
| explicit persistent state | 4 | 4 |
| causal/provenance applicability | 4 | 4 |

This is meaningful independent convergence at the **semantic-law level**, not architecture convergence. AIDE², LongHorizon-Harness, AREX, CHILL, HGM, ToolPrivBench, RWML, STAGE-Claw, KTD-Fin and VISTA do not share one codebase or product ontology; they nevertheless repeatedly rediscover compatible distinctions.

## The user's stronger hypothesis was too strong

The cohort does **not** support the claim that wrong causal structure is completely chaotic.

Failure manifestations are highly varied: evaluator tampering, train/test leakage, similarity-only memory retrieval, context-compaction constraint loss, transient-failure privilege escalation, seed-literature collapse, unreliable foresight, meta-agent exfiltration, fixed search policy, uncontrolled orchestration cost, and many others.

AIDE² makes this surface diversity unusually visible: one manually inspected seed contained 95 rejected proposals including island populations, LLM-judge tournaments, adaptive restarts, restart/refine policies, majority-vote ensembles, exploration schedules, UCB-V, MCTS-style value backup and optimizer-curse corrections. Most sophisticated-looking mechanisms did not beat the incumbent under the fixed budget.

But once those failures are normalized by causal error, they also converge:

| Anti-law | Independent groups | Domain families |
|---|---:|---:|
| visible metric/proxy = true objective | 8 | 6 |
| local gain = general frontier progress | 6 | 5 |
| current performance = future improvement value | 4 | 3 |
| raw context / lossy compaction = sufficient state | 3 | 3 |
| fixed global policy = sufficient operator | 3 | 3 |
| more complexity/search = more value | 3 | 2 |
| one domain score = semantic success | 3 | 3 |

Therefore the refined hypothesis is:

> **Correct surviving structures are low-dimensional and recurrent. Wrong implementations are high-dimensional at the surface, but their deeper causal mistakes also collapse into a smaller recurrent set of anti-laws.**

That is more useful than a pure order-versus-chaos story. It implies an RSI system can learn not only positive invariants but also stable negative priors that cheaply eliminate large regions of search space.

## Entropy check

Using unique research-group × normalized-category assignments, LW0 obtains normalized Shannon entropy:

```text
successful structural motifs: 0.920
causal failure anti-laws:      0.935
```

The difference is small. It is **not** evidence for a strong mathematical law that correct systems always have lower entropy than failures.

The more defensible evidence is recurrence breadth: several successful distinctions independently recur across 6–8 domain families, while only a smaller number of failure anti-laws reach similar breadth. The cohort is also selected for Ordivon relevance, so these frequencies are descriptive rather than population estimates.

## Reconciliation with Ordivon semantic laws

### L1 — Representation Distinction

Strongly strengthened.

LongHorizon-Harness separates independently verified task state from growing execution context; RewardHackingAgents separates reported metric from trusted evaluation; AgentSearchBench separates textual capability description from execution-grounded performance; RWML separates predicted next state from realized transition; STAGE-Claw evaluates final system state rather than textual completion; KTD-Fin separates raw return from attributable investment skill; VISTA separates functional success from visual fidelity.

This is exactly the kind of independent cross-domain recurrence required for a semantic law.

### L2 — Applicability Binding

Strengthened, but HP4 remains ahead of the external cohort.

AREX preserves verified evidence and unresolved constraints; LongHorizon-Harness updates task state only from audited environment facts; AMA-Bench finds causality/objective information necessary for memory; STAGE-Claw binds success to verified state.

However, none of these establishes that **currentness evidence decides semantic applicability after owner drift**. Ordivon HP4 directly falsified that stronger claim. Binding is supported; generic applicability competence remains open.

### L3 — Partial Observation

Supported.

External systems repeatedly introduce auditing, unresolved constraints, prediction-observation correction and selective foresight because absence of model-visible evidence is not sufficient evidence of absence. Do not turn this into a universal confidence score.

### L4 — Scoped Authority

Supported but with narrower external scope.

ToolPrivBench directly shows that models frequently choose or escalate to unnecessary higher privilege, especially after transient failure. Governance Decay shows governance can disappear if context management treats constraints as ordinary lossy text. These support least privilege and protected authority state. Ordivon's distinction between epistemic selection and effect authority remains broader.

### L5 — Causal Non-Collapse

Strongly strengthened.

RewardHackingAgents, STAGE-Claw, KTD-Fin and VISTA all demonstrate domain-specific versions of the same law: reported success does not establish the causal consequence that matters.

## Harness reconciliation

LongHorizon-Harness and AREX strongly support Ordivon's `Canonical History ≠ Working Set ≠ current verified state` direction. AMA-Bench adds that causal/objective relations matter more than similarity-only retrieval. Governance Decay adds a critical boundary: compression is useful only if it preserves governance/constraints that must not be lossy.

CHILL-Harness independently supports the RF1 lesson that adaptive harness behavior has a cost and must earn its existence. CHILL does not contradict RF1: CHILL gates workflow interventions by estimated relative advantage; RF1 falsified serial per-observation Agent self-questioning as a stopping implementation.

HP3 is also externally consistent: AIRA/CHILL support conditional operators, but no external evidence requires an Agent-facing discrete Ordivon topology enum. Keep evidence affordances; keep topology names descriptive.

## Evaluator reconciliation

This is one of the strongest convergence zones.

AIDE² relies on private scores and reports emergent reward-hacking reduction; Who Grades the Grader evolves metrics only under anchors and an outer audit; RewardHackingAgents measures evaluator tampering and leakage as explicit outcomes; AIRA2 uses hidden consistent evaluation; RWML prefers realized-state alignment over task-reward-only or LLM-judge signals.

The shared law is not `private evaluator = truth`.

It is:

```text
evaluator is part of the world
→ evaluator can be wrong or gamed
→ bind it, hide what should be hidden, audit it independently, and preserve owner/state evidence
```

This strongly supports Ordivon's HP4 decision to invalidate the entire contaminated v1 campaign when the evaluator leaked post-consequence facts into a pre-consequence decision test.

## Research Frontier / Scientific Taste reconciliation

External evidence creates a productive conflict.

`AI Can Learn Scientific Taste` shows that a model can learn a preference signal correlated with later citation impact and transfer that preference across years/fields/review signals. But `AI Research Agents Narrow Scientific Exploration` finds current research agents produce ideas more concentrated around seed literature and mainly recombine known methods.

Therefore:

```text
impact preference
!=
frontier expansion
!=
tractability
!=
what should receive compute now
```

This directly justifies FS0's continued existence. Open-world multi-owner problem selection remains a real research frontier rather than a solved consequence of better scientific-idea scoring.

## Metaproductivity and ignition

DGM, HGM, MetaSkill-Evolve and AIDE² all push the evaluation target upward from current task performance toward future improvement ability.

HGM names the mismatch directly: the best current agent is not necessarily the best ancestor. MetaSkill evolves the improvement procedure itself. AIDE² explicitly tests whether an improved inner-loop agent becomes a better outer-loop improver and reports that ignition was **not** established.

Ordivon should therefore add `metaproductivity` as a **candidate ResearchOutcome dimension**, not a semantic primitive or universal scalar.

A future Ordivon ignition test should require:

```text
T0 / improver0
→ produce T1 / improver1

then on fresh held-out pressures:
T1 must produce better future research-policy updates than T0
under a fixed/declared budget vector
```

Current-task improvement is insufficient.

## World reconciliation

RWML and COMAP directly support the World Model loop:

```text
predict action-conditioned consequence
→ observe realized transition
→ compute prediction error
→ update world model
→ improve future action selection
```

This is strong evidence for `World Model ≠ static prompt knowledge`. It does not grant model predictions owner authority. Realized transition remains the calibration source.

## Security / Memory reconciliation

AMA-Bench supports causal/objective memory over similarity-only recall. Governance Decay shows that lossy context management can erase authority constraints. ToolPrivBench shows safety alignment alone does not reliably create least-privilege tool behavior.

These reinforce Ordivon's direction that memory, authority and observations require provenance/binding and cannot be treated as generic helpful context.

## Runtime / Effect reconciliation

STAGE-Claw strongly supports final-state verification over textual completion. ToolPrivBench supports least privilege. RewardHackingAgents supports evaluator integrity.

But the external cohort remains thinner on several Runtime/Finance problems Ordivon has already encountered physically:

- immutable materialization / exact consumed bytes;
- ambiguous delivery and exact replay of a previously admitted identity;
- semantic applicability after a safe binding conflict;
- separated effect principal / signer authority;
- owner-bound concurrency at consequence time.

These remain legitimate Ordivon research frontiers rather than redundant reinventions.

## Domain laboratories

### Finance

KTD-Fin independently demonstrates `return ≠ transferable investment skill`: leakage and passive factor exposure can explain apparent success. This strongly supports Finance's insistence on causal attribution/evidence before performance claims, while live venue/effect semantics remain additional requirements.

### Game

OmniGameArena's Improvement Dynamics Curve independently supports AF003's direction: evaluate how an Agent changes across rounds and whether learned behavior survives held-out game variants. Fixed-Genesis performance is not enough evidence of robust game world-model improvement.

### Web / Studio

VISTA shows functional correctness and visual fidelity are partially decoupled. This supports Web/Studio's refusal to treat build/tests as product/aesthetic truth.

## What LW0 changes

LW0 strengthens existing semantic laws but **promotes no new global Ordivon layer**.

Candidate additions to future ResearchOutcome / RSI measurement:

- metaproductivity;
- ignition / third-order generalization;
- evaluator evolution/integrity;
- scientific exploration breadth.

These are measurement dimensions and hypotheses, not primitives.

## What LW0 rejects

Do not build:

- `ResearchTasteService`;
- a universal ResearchScore;
- a TopologyClassifier;
- a global Evaluator authority;
- automatic literature-to-product rules;
- a shared architecture merely because multiple papers use similar words.

The repeated convergence is semantic, not necessarily mechanical.

## New higher-order world model

The user's initial intuition survives in a refined form:

```text
many independent worlds
      ↓
successful structures
      ↓
repeated pressure
      ↓
small set of stable semantic distinctions
```

while:

```text
wrong implementation space
      ↓
very many mechanisms / symptoms
      ↓
BUT causal post-mortem
      ↓
smaller recurring anti-laws
```

The practical RSI implication is substantial:

> Scientific taste may partly consist of a compressed world model of both **stable invariants** and **stable anti-laws**. The value is not to preach them to the Agent as prose—TM1/HP2/HP3 warn against that—but to use them to design cheaper falsifiers, stronger baselines, better ResearchBets, and more discriminating experiments.

## Next falsification path

LW0 is retrospective reconciliation. It does not graduate the convergence thesis.

The strongest next test is prospective:

1. freeze the current motif/anti-law vocabulary;
2. ingest future papers or materially different systems evidence **before reading outcome sections into the coding decision**;
3. predict which structural choices should survive and which should fail;
4. compare predictions to authors' ablations/held-out outcomes;
5. use an out-of-domain holdout from older systems/scientific-method literature to test whether recurrence is deeper than 2026 agent-research fashion.

Only if those predictions work should `stable invariant / stable anti-law` become a stronger Research Frontier prior.
