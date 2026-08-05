# Cross-Disciplinary Foundations

## 1. Why one discipline is insufficient

An execution entity can simultaneously be:

- code that must be reversed;
- a controller that acts under constraints;
- a strategic player facing another player;
- a replicator spreading across a graph;
- a member of an organization;
- a population undergoing selection;
- an evaluated policy attempting to manipulate its judge;
- a component of a mission that must continue after compromise.

No single mature discipline owns all of those relations. Ordivon should use each
discipline only for the questions it is competent to answer.

## 2. Program analysis and malware research

### Transferable concepts

- exact Artifact identity and provenance;
- static structure, imports, resources, strings, control flow, and data flow;
- reachability and capability analysis;
- packing, obfuscation, dynamic loading, and unresolved regions;
- runtime behavior, memory state, file and registry effects, and network flows;
- reverse engineering and hypothesis-driven dynamic analysis;
- family classification and variant comparison.

DARPA's Cyber Grand Challenge demonstrated that automated systems can discover
software flaws, generate patches, attack competitors, defend services, and
operate at machine speed in an air-gapped tournament [R02]. MITRE ATT&CK provides
a mature behavior vocabulary grounded in observed adversary operations [R01].

### Limitation

Program analysis can show potential and observed behavior but does not by itself
establish objective, authorization, organizational responsibility, population
dynamics, strategic adaptation, or evaluator manipulation.

### Ordivon implication

Static and dynamic analysis become evidence-producing adapters. Security owns
which claim is supported under which authority and experimental distribution.

## 3. Game theory

Game theory treats decisions as interdependent: one actor's outcome depends on
what others choose. Aumann and Schelling's work established conflict,
cooperation, repeated interaction, commitment, signalling, and strategic
interdependence as formal research objects [R03].

### Transferable models

| Model | Execution-entity question |
|---|---|
| zero-sum game | is one side's advantage exactly the other's loss? |
| general-sum game | can both sides lose, cooperate, extort, or share risk? |
| Bayesian game | what happens when type, capability, or objective is uncertain? |
| repeated game | how do reputation, retaliation, learning, and conventions form? |
| signalling game | how do entities reveal, conceal, bluff, or authenticate? |
| stochastic game | how do actions and random events alter future state and payoffs? |
| coalition game | when do entities form, maintain, or betray alliances? |
| evolutionary game | which strategies persist in a changing population? |
| principal-agent model | does a delegated entity still serve the principal? |
| mechanism design | which rules make self-interested entities produce acceptable outcomes? |

Stackelberg Security Games provide a practical model for limited defensive
resources facing an attacker that observes and responds to the defender's
allocation [R04]. They also show why randomized or mixed strategies can matter
when predictable defense becomes exploitable.

### Limitation

Formal games require declared players, actions, observations, transitions, and
payoffs. Open Tool construction, changing identities, new descendants, and
unbounded communication may not fit without significant modelling choices.

### Ordivon implication

Use games as the strongest null model. Add an Ordivon distinction only when a
measured fact cannot remain scenario state, policy state, or evaluation data.

## 4. Strategic and military theory

Strategic theory supplies a language for sustained conflict among adaptive
wills. MCDP 1 emphasizes friction, uncertainty, fluidity, disorder, complexity,
initiative, tempo, concentration, vulnerability, and the tactical,
operational, and strategic levels of war [R05].

### Transferable concepts

| Strategic concept | Digital interpretation |
|---|---|
| friction | latency, model failure, Tool error, incomplete authority, coordination loss |
| uncertainty | partial, delayed, deceptive, or conflicting observation |
| initiative | which side imposes response burden and narrows the other's options |
| tempo | rate of useful observe-decide-act-recover cycles |
| concentration | committing scarce compute, credentials, tools, or Agents to a decisive point |
| dispersion | reducing correlated detection or single-point destruction |
| logistics | compute, tokens, identity, credentials, bandwidth, storage, and Provider supply |
| reserve | unexposed tools, access, nodes, models, or Agents retained for later use |
| critical vulnerability | dependency whose loss collapses a larger capability |
| withdrawal | preserving capability and option value rather than chasing local success |
| deception | shaping what another entity sees, believes, and chooses |

### Limitation

Military terminology can create false grandeur and imported abstractions. It is
useful only when grounded in measurable digital facts and compared against
ordinary Goal, Task, reward, inventory, and queue models.

### Ordivon implication

Strategy is an experimental hypothesis, not a naming scheme. Campaign,
initiative, reserve, or tempo survive only when they improve prediction,
transfer, continuity, or evaluation.

## 5. Epidemiology and propagation on graphs

Directed-graph epidemiological models of computer viruses adapted mathematical
epidemiology to program-sharing networks and showed that topology and epidemic
thresholds matter for computational spread [R06].

### Transferable concepts

- susceptible, exposed, active, dormant, detected, quarantined, removed,
  recovered, and reinfected states;
- reproduction number and epidemic threshold;
- contact graph and directionality;
- incubation, activation, and detection delay;
- recovery and reinfection;
- heterogeneous susceptibility;
- superspreading nodes;
- intervention timing and coverage.

### Strategic contagion

A conventional epidemic model assumes transition rates. An intelligent entity
may choose targets, lower its visible spread rate, wait for authority, vary its
descendants, sacrifice nodes, or coordinate multiple routes. The resulting
research object is **strategic contagion**: propagation dynamics whose rates and
paths are policy-dependent and adversarially adapted.

### Limitation

Biological analogies can mislead. Digital descendants may copy exactly, mutate
intentionally, share state instantly, or be revoked centrally. Ordivon must bind
which biological concept remains predictive.

## 6. Ecology and evolutionary dynamics

Evolutionary game theory studies how strategies spread, stabilize, cycle, or
collapse in populations. Work on finite populations, cooperation, and stochastic
games shows that reciprocity, population structure, environmental feedback, and
selection conditions can change which behaviors persist [R07][R08].

### Transferable concepts

- fitness under a declared environment;
- selection pressure created by defense;
- mutation and variation;
- niche and resource competition;
- cooperation, defection, parasitism, and mutualism;
- diversity and correlated failure;
- invasion and displacement;
- predator-prey and host-parasite coevolution;
- carrying capacity and resource exhaustion;
- equilibrium, cycling, and path dependence.

### Ordivon implication

A defense may suppress one population while selecting for a slower, stealthier,
or more decentralized population. Evaluation must therefore retain population
diversity, historical opponents, held-out environments, and collateral effects.

### Limitation

“Fitness” must not become a vague score. It must be tied to survival,
replication, objective progress, resource position, control, and evidence under a
specified distribution.

## 7. Control theory and safety invariance

Control Barrier Functions formalize how a controller may optimize performance
while preserving a safe set [R09]. The transferable idea is not a direct
mathematical equivalence to cyber systems; it is the separation between:

```text
performance policy
  chooses useful action

safety constraint
  prevents state from leaving an admitted set
```

This maps to Ordivon's Observer/Guardian separation:

- the Entity or Agent pursues an objective;
- the Observer estimates and records state;
- the Guardian enforces a hard boundary;
- the truth plane verifies whether the boundary held.

### Research questions

- what is the safe set for one Trial or Campaign?
- which facts are known strongly enough for hard enforcement?
- when should an unsafe proposal be projected to a safe alternative?
- when is termination mandatory?
- can authority expand after evidence without weakening the boundary?
- how do several local Guardians compose?

### Limitation

Digital worlds are hybrid, partially observed, and adversarially manipulated.
Formal guarantees require a much clearer state and transition model than many
Agent systems possess.

## 8. Cyber-resilience engineering

NIST SP 800-160 Volume 2 treats cyber resiliency as systems engineering for
survivable and trustworthy systems under adversity [R10]. The essential shift is
from perfect prevention to the ability to anticipate, withstand, recover, and
adapt.

### Transferable outcomes

```text
anticipate
withstand
recover
adapt
```

Evaluation should therefore ask:

- did the critical mission continue?
- was control recovered?
- were descendants and residuals accounted for?
- is the recovered system still trustworthy?
- did adaptation reduce risk against held-out future conditions?
- did defense destroy legitimate utility or future options?

### Ordivon implication

Entity elimination is one possible outcome, not the universal objective.
Isolation, degradation, deception, replacement, recovery, and coexistence may be
better under some mission constraints.

## 9. Organization and distributed systems

A group of Agents introduces authority, trust, communication, failure, and
coordination questions that ordinary process trees do not answer.

### Transferable concepts

- principal, delegate, role, and scope;
- least authority and attenuation;
- revocation and expiry;
- compartmentalization;
- quorum and independent adjudication;
- Byzantine or compromised members;
- command replacement;
- provenance and non-repudiation;
- partition, stale state, and reconciliation;
- responsibility after delegation.

NIST's current AI-Agent security work identifies identification,
authorization, auditing, non-repudiation, and prompt-injection mitigation as
important agent-specific concerns [R12][R13].

### Ordivon implication

A child Agent must not automatically inherit the parent's complete authority.
Lineage is not authorization. Every delegation needs an explicit principal,
scope, environment, duration, and revocation relation.

## 10. AI-Agent hijacking and autonomous replication

NIST's Agent hijacking evaluations show that repeated and adaptive attacks can
reveal risk missed by one-shot evaluation [R11]. AISI's RepliBench decomposes
autonomous replication into component capabilities such as resource acquisition,
deployment to new compute, copying model capability, persistence, and recursive
replication [R14].

### Transferable lessons

- evaluate repeated attempts, not one prompt;
- decompose a compound capability into necessary sub-capabilities;
- distinguish successful action from robust autonomous continuation;
- bind environment weakness and identity assumptions;
- test descendant functionality, not merely file copying;
- measure persistence after parent loss;
- include authority, cost, and external dependency.

### Limitation

A replication benchmark is not evidence of malicious intent or general
self-sustaining autonomy. Ordivon must report component success, complete-chain
success, operator assistance, and failure conditions separately.

## 11. Synthesis

The disciplines combine into one evaluation grammar:

```text
program analysis
  what capability exists and what executed?

game and strategic theory
  how does action depend on opponents, information, resources, and time?

epidemiology and ecology
  how do descendants and strategies spread, compete, and persist?

control and resilience
  which boundaries hold, and can the mission recover and adapt?

organization and Agent security
  who authorized whom, who remains responsible, and can control be revoked?

evidence science
  which claims can an independent evaluator reconstruct?
```

The Ordivon contribution, if any, is the compact relation among those evidence
families—not reimplementation of their mechanisms.
