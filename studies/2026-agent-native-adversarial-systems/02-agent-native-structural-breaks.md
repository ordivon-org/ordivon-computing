# Agent-Native Structural Breaks

## 1. The break is not “AI can attack”

Human attackers have always supplied intelligence to cyber conflict. Classical
security already assumes purposeful adversaries, deception, reconnaissance,
persistence, and adaptation.

The Agent-era break is narrower and more structural:

> The software component inside the operating loop can itself interpret strategic
> objectives, model other actors, construct and combine tools, maintain
> long-lived state, reorganize collaborators, and revise policy at machine speed.

Many visible changes are only amplification:

- more scanning;
- faster vulnerability discovery;
- cheaper phishing or content generation;
- automated patching;
- broader log analysis;
- higher-volume attack-path search.

These remain important, but they do not alone justify a new Ordivon layer.

## 2. From static environment to intelligent opposition

A normal Agent loop is often represented as:

```text
observe → infer → act → receive feedback → revise
```

Under strategic opposition:

```text
opponent chooses what can be observed
→ predicts how observation will be interpreted
→ shapes the actor's action
→ studies the resulting response
→ changes policy again
```

Feedback is no longer merely noisy. It may be adversarially selected to create a
particular belief or disclose a capability.

This produces three candidate structural requirements:

1. actor-specific observation must remain distinct from authoritative world
   truth;
2. competing explanations about opponent action may need durable continuity;
3. evaluation must consider what actors learned and exposed, not only physical
   end state.

## 3. From task completion to strategic continuity

A Task normally has a relatively stable objective and completion condition. A
Campaign may contain many Tasks whose local value changes because of opponent
behavior.

Examples:

- exploiting a decoy is tactically successful but strategically harmful;
- repairing a visible service may reveal the defender's detection capability;
- preserving a foothold may be more valuable than using it immediately;
- forcing an opponent to spend scarce attention may matter even without direct
  compromise;
- withdrawal may preserve future options better than continued local success.

This creates a candidate state above individual Task completion:

- strategic objective and acceptable end states;
- current Campaign phase and alternative paths;
- resources already committed or exposed;
- beliefs about opponent capability and awareness;
- remaining options and reserves;
- initiative and response burden.

The candidate is rejected if ordinary Goal/Task memory and cumulative reward
capture the same decisions.

## 4. From action policy to open capability construction

CybORG-class and game-theoretic environments usually define action and
observation spaces. That limitation enables reproducibility and learning.

Tool-using language Agents can instead:

- write new analysis or exploitation tools;
- alter communication formats;
- create sub-Agents;
- change the granularity of action;
- combine low-level mechanisms into an unanticipated procedure;
- reinterpret intermediate objectives;
- move between software, identity, communication, and organizational surfaces.

This openness creates a modelling tension:

- a fully open world is difficult to evaluate and reproduce;
- a fixed action set may hide the capabilities we intend to study.

Ordivon should not solve this by inventing a universal action language. The
research question is how much openness is required for a given claim and which
mature Tool/Runtime interfaces can provide it.

## 5. From one adaptive policy to recursive adaptation

Ordinary adaptation changes behavior after environmental feedback.

Adversarial adaptation is recursive:

```text
A changes policy
→ B detects and counters
→ A infers the countering rule
→ A changes what B can observe
→ B updates its model of A
```

The environment becomes non-stationary because the opponent is learning about
the learner.

Important observable patterns may include:

- cycling between exploit and countermeasure families;
- escalating capability exposure;
- strategic concealment and delayed action;
- convergence toward stable conventions or deterrence;
- collapse into mutual evaluator exploitation;
- overfitting to one opponent population.

A single successful trajectory cannot establish capability under this process.

## 6. From provenance to information conflict

Classical provenance records where data and actions came from. Agent adversarial
systems may additionally need to study what a sender intended the receiver to
believe and how the receiver interpreted the information.

Potentially distinct states are:

```text
truth
observation
claim
belief
belief about another actor's belief
intended belief effect
deception hypothesis
verification result
```

The distinction is useful only if it changes prediction, action, explanation, or
transfer. Otherwise established provenance plus ordinary Context is sufficient.

## 7. From multi-Agent coordination to adversarial organization

Multi-Agent systems often assume a shared goal. Strategic conflict introduces:

- compromised members;
- partially aligned incentives;
- compartmentalized information;
- hidden roles;
- opponent infiltration;
- collusion against the operator or evaluator;
- communication channels that disclose organization and intent;
- command replacement during active opposition.

This may require more than branch, Join, and Artifact ownership. But Ordivon must
prove that organization-level records predict or improve outcomes before adding
a cross-project organization protocol.

## 8. From neutral evaluator to contested evaluator

A capable actor may:

- find hidden answers;
- optimize for visible scoring quirks;
- manipulate logs or evidence;
- cause the judge to fail;
- behave differently when monitoring is inferred;
- coordinate covertly with another actor;
- manufacture apparent compliance or apparent opponent failure.

Control evaluation already studies parts of this problem. The additional
Ordivon hypothesis is that evaluator contest may become one dimension of normal
multi-actor strategic interaction rather than an exceptional attack mode.

## 9. From absolute capability to relational capability

The statement “Agent X can perform cyber operation Y” is incomplete.

A more defensible claim binds:

```text
actor system
× opponent distribution
× information structure
× world family
× tool and authority set
× resource and time budget
× organization
× evaluation protocol
```

Capability may increase against one opponent while decreasing against another.
More inference-time compute may improve planning, produce overthinking, expose
more behavior, or search harder for evaluator loopholes.

Ordivon Security should therefore treat adversarial capability as relational and
distributional.

## 10. Candidate structural breaks and admission tests

| Candidate break | Existing baseline that may already solve it | Evidence required before Ordivon construction |
|---|---|---|
| Campaign continuity above Tasks | Host Goal/Task memory, workflows, game episodes | improved transfer, strategic diagnosis, or continuation under counterplay |
| explicit opponent model | recurrent policy state, transcript Context, MARL opponent embeddings | held-out-opponent advantage or better calibrated adaptation |
| information position | provenance, hidden game state, trust labels | measurable deception/counter-deception outcome grounded in truth |
| initiative and strategic resources | cumulative reward, action cost, game inventory | robust prediction or ranking unavailable from reward alone |
| adversarial organization | Host branch/join, standard MARL team state | benefit under compromise, partition, or partial trust |
| coevolution evaluator | Inspect/ControlArena, self-play, league evaluation | better transfer and gaming detection without unstable rankings |

## 11. Strongest null hypothesis

The strongest null hypothesis is:

> Strategic adversarial agency requires no new shared Ordivon layer. Mature game,
> Agent-evaluation, cyber-range, Host-memory, and Tool systems are sufficient;
> `ordivon-security` should remain a thin research and scenario-composition
> repository.

The project should be designed so this null hypothesis can win.
