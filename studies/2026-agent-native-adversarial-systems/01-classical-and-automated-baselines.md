# Classical and Automated Baselines

## 1. MITRE ATT&CK — adversary behavior vocabulary

MITRE ATT&CK represents adversary tactics as the reason for an action and
techniques as how the tactical goal is achieved. Enterprise ATT&CK covers
reconnaissance, resource development, access, execution, persistence, privilege,
stealth, defense impairment, credentials, discovery, movement, collection,
command and control, exfiltration, and impact [R01][R02].

### What it solves

- a shared vocabulary for observed adversary behavior;
- a hierarchy from tactical goal to technique, sub-technique, and procedure;
- links between real incidents, platforms, and defensive planning;
- a non-linear behavior map rather than one mandatory attack sequence.

### What it does not solve

- how one autonomous actor chooses among tactics against a specific opponent;
- how beliefs and deception alter strategy;
- how strategic objectives, resources, and initiative persist across actions;
- how an actor revises organization or policy after counter-adaptation.

### Ordivon implication

ATT&CK should be a tactical knowledge source or action vocabulary, never an
Ordivon-owned workflow or Campaign ontology.

## 2. MITRE D3FEND — countermeasure engineering knowledge

D3FEND is a semantic knowledge graph for defensive countermeasure components,
capabilities, engineering mechanisms, and relations to offensive behavior [R03].

### What it solves

- precise defensive mechanism language;
- explanation of how and under what conditions a countermeasure works;
- inferential links from defensive techniques to offensive techniques.

### What it does not solve

- strategic choice among countermeasures under scarce resources;
- active opponent modelling;
- autonomous deception and counter-deception;
- attack-defense coevolution.

### Ordivon implication

D3FEND is a mature knowledge substrate. Security may research an Agent's
selection and strategic combination of countermeasures, not recreate the graph.

## 3. MITRE Engage — adversary engagement and deception

MITRE Engage helps defenders plan denial, deception, and adversary-engagement
activities. Its public explanation explicitly frames deception through what the
defender wants the adversary to do, what the adversary must think, and what it
must see to form that belief [R04][R05].

### What it solves

- a practical planning vocabulary for influencing adversary behavior;
- links between adversary actions and opportunities for engagement;
- a shift from passive detection toward manipulating the attacker's decisions.

### Why it is especially relevant

Engage already moves from physical state to belief shaping. It is therefore a
strong counterexample to any claim that deception or information position is
entirely new in Agent systems.

### Remaining question

Can adaptive Agents autonomously construct, detect, and revise deception
strategies, including beliefs about what the opponent believes, across changing
Campaigns? Or is a human-designed Engage plan plus ordinary Agent execution
sufficient?

## 4. DARPA Cyber Grand Challenge — machine-speed cyber reasoning

DARPA's Cyber Grand Challenge fielded fully automated Cyber Reasoning Systems
that identified software flaws, scanned an air-gapped network, patched software,
attacked opponents, protected hosts, and preserved software function over an
approximately twelve-hour competition [R06].

### What it proves

- offense and defense can be automated at machine speed;
- vulnerability discovery, proof, patching, and network competition can be
  integrated;
- scoring can trade off security and continued service utility.

### Limitation relative to Ordivon

CGC is a major precedent for autonomous cyber competition. However, its center
is binary analysis, vulnerability reasoning, patching, and a purpose-built game.
It does not by itself establish open-ended language/tool Agent Campaigns,
explicit opponent models, multi-Agent organization, or evaluator-aware
strategic deception.

## 5. DARPA AI Cyber Challenge — LLM-enhanced cyber reasoning

AIxCC integrated AI and LLM techniques into Cyber Reasoning Systems for finding,
proving, and patching vulnerabilities in real open-source software. DARPA
reported 54 unique synthetic vulnerabilities found in the final challenges, 43
patched, plus real non-synthetic findings under responsible disclosure [R07][R08].

### What it proves

- LLMs can be composed with classical analysis and patch systems;
- autonomous vulnerability discovery and repair can operate on substantial real
  codebases;
- open-source cyber reasoning systems are a strong baseline for Ordivon.

### Limitation relative to Ordivon

AIxCC is still primarily a software-vulnerability and patch-quality competition.
Ordivon should not rebuild it. The open question is what happens when adaptive
opponents, contested information, long-horizon strategy, and organizations
become central rather than incidental.

## 6. CybORG/CAGE — autonomous Red/Blue environments

CAGE uses CybORG to train and evaluate autonomous cyber-defense agents in
increasingly realistic scenarios [R09]. CAGE Challenge 4 includes Red, Blue, and
Green actors, multiple defenders, changing mission phases, action duration,
communication constraints, network policy, false alerts, decoys, service impact,
and multi-Agent reinforcement learning [R10][R11].

### What it solves

- partially observed sequential attack-defense interaction;
- changing mission value and defender utility costs;
- multiple agents, communication, action duration, decoys, and service
  restoration;
- mature simulated world truth and repeatable episodes.

### Important limitation

The Red baseline is commonly finite-state or rule-driven and the action space is
predefined [R12]. This is not a defect; it is a strong experimental baseline.
It means Ordivon must prove value beyond replacing a finite-state actor with an
LLM.

### Ordivon implication

CybORG/CAGE should be the first comparison or adapter candidate for dynamic
opposition. It allows strategic research to advance before custom Link/Edge
fidelity.

## 7. Microsoft CyberBattleSim — abstract enterprise-network RL

CyberBattleSim studies interactions among automated agents in a simulated,
high-level enterprise network through a Gym interface [R13].

### What it solves

- accessible RL experimentation;
- abstract network and vulnerability state;
- automated agent interaction and policy learning.

### Limitation

High abstraction and defined actions simplify real tool use, open-ended
strategy, deception, and organization. It is useful as a simpler baseline, not a
complete strategic adversarial model.

## 8. Inspect and ControlArena — Agent control and sabotage evaluation

ControlArena builds on Inspect AI and provides Settings, main tasks, harmful side
tasks, honest and attack modes, trusted/untrusted policies, monitors,
micro-protocols, macro-protocols, scorers, and safety/usefulness analysis [R14].
AISI's research agenda explicitly anticipates latent reasoning, steganography,
collusion, jailbreaking, monitor bypass, and longer-running attacks [R15].

### What it solves

- rigorous evaluation of a potentially untrusted Agent;
- trajectory-level monitoring and control protocols;
- separation of useful main-task work from harmful side-task behavior;
- attack-mode models and hidden evaluation conditions.

### Limitation relative to Ordivon

The core relation is generally operator/control protocol versus one potentially
subversive policy. Ordivon asks whether multiple adversarial actors, competing
Campaigns, explicit opponent models, information conflict, and organization
should be the normal system form.

ControlArena is therefore a crucial baseline, not a model to ignore or replace.

## 9. POSGs and extensive-form games — formal multi-actor uncertainty

Partially observable stochastic games and extensive-form games provide mature
formal models for sequential multi-actor decisions under hidden information,
conflicting or shared rewards, and strategic interaction [R16][R17].

### What they solve

- actor policies, observations, hidden state, rewards, and equilibrium concepts;
- formal belief and information structures;
- a basis for reasoning about partial observability and opponent adaptation.

### Remaining question

Language/tool Agents can create tools, alter communication, change organization,
and operate across open-ended interfaces. The research question is whether these
features require a new system layer or only richer game state and action spaces.

## 10. Opponent modelling

Opponent-modelling research explicitly addresses non-stationarity created by
other adaptive agents and learns representations of opponent strategy [R18].

### Ordivon implication

Opponent modelling is not novel. Ordivon's burden is to show why persistent,
evidence-linked opponent hypotheses in Agent systems improve transfer,
continuity, deception reasoning, or diagnosis beyond latent policy state and
ordinary Context.

## 11. Melting Pot — social generalization

Melting Pot evaluates agents across cooperation, competition, deception, trust,
reciprocation, and unfamiliar social partners, with held-out scenarios and
background populations [R19][R20].

### Ordivon implication

Adversarial capability must generalize to unfamiliar actors, not merely exploit a
known Red or Blue policy. Melting Pot is a strong source for held-out social
situation methodology and a warning against opponent overfitting.

## 12. Baseline synthesis

The comparison yields four layers:

```text
classical mechanisms
  mature and reusable

automated cyber reasoning
  mature for discovery, exploitation, repair, and policy execution

autonomous Red/Blue environments and control evaluation
  mature for bounded sequential interaction and sabotage testing

strategic open-ended adversarial agency
  still fragmented across games, MARL, cyber, Agent control, and system design
```

Ordivon should research only the final integration gap, and must accept the
possibility that existing models plus thin adapters are sufficient.
