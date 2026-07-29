# Research Program and Falsifiers

## 1. Program objective

Determine whether strategic adversarial agency requires a compact reusable
Ordivon layer, only domain-specific scenario adapters, or no new layer at all.

The program is not sequenced by custom infrastructure readiness. It is sequenced
by information gain.

## 2. R0 — conceptual and repository reset

### Work

- reclassify existing Security lifecycle/evidence code as frozen support;
- replace the containment-centered charter with strategic adversarial research;
- create durable questions for Campaign, opponent/deception, organization, and
  coevolution/evaluation;
- rewrite existing GitHub Issues to reflect the new route;
- preserve all historical evidence and tests.

### Exit evidence

- repository and Computing charters agree;
- route explicitly separates research hypotheses from implemented facts;
- no open Issue treats custom Link/Edge attachment as a conceptual prerequisite;
- every proposed new abstraction has a baseline and deletion test.

## 3. R1 — comparative foundations

### Work

Build a primary-source map across:

- ATT&CK, D3FEND, Engage, threat-informed defense, and deception;
- CGC, AIxCC, automated program reasoning, patching, and autonomous cyber;
- CybORG/CAGE and CyberBattleSim;
- Inspect, Inspect Cyber, and ControlArena;
- POSGs, extensive-form games, opponent modelling, MARL, self-play, league play,
  and Melting Pot;
- classical command, intelligence, tempo, resource allocation, and adversary
  engagement.

### Exit evidence

- each claimed Agent-native gap names the strongest mature counterexample;
- no claim of novelty remains unsupported;
- candidate objects are reduced to the smallest competing models.

## 4. R2 — minimal dynamic-opponent baseline

### Environment

Prefer an existing simulated environment with authoritative world truth,
actor-specific observations, repeatable seeds, and at least one adaptive or
switching opponent.

### Actors

Compare:

1. fixed script;
2. finite-state actor;
3. learned policy;
4. ordinary LLM Agent with Tool use and transcript memory;
5. mixed actor teams where useful.

### Questions

- Does an LLM provide useful adaptation beyond action-path search?
- Which failures come from model cognition versus world/action interface?
- How much variance arises from model sampling, opponent policy, and world seed?
- Can the Agent identify a policy change rather than merely retry?

### Stop rule

Do not add Ordivon strategic objects if existing policies and trajectory logs
answer the question.

## 5. R3 — opponent model and deception ablation

### Variants

- no explicit opponent model;
- transcript-only natural-language reflection;
- structured single-hypothesis model;
- competing/ensemble hypotheses;
- first-order and bounded second-order belief reasoning.

### Scenarios

- natural fault versus identical adversarial effect;
- mid-run opponent policy switch;
- decoy and false flag;
- misleading Tool output;
- defender and attacker both able to deceive.

### Measures

- detection latency and false positives;
- calibration of hypotheses;
- resource misallocation;
- tactical and strategic effects;
- transfer to held-out deception styles;
- storage/context/compute cost.

### Falsifier

Explicit models are deleted if transcript or latent policy state performs as
well or better across held-out opponents.

## 6. R4 — Campaign synthesis and strategic resources

### Environment requirements

- multiple viable paths to a high-level objective;
- changing mission value or phase;
- scarce compute, time, actions, tools, access, or secrecy;
- capability exposure that changes future opposition;
- locally rewarding decoys or dead ends;
- opportunity to wait, withdraw, conceal, or reserve capability.

### Measures

- tactical success;
- operational objective progression;
- strategic outcome;
- initiative and response burden;
- resource position and future options;
- explanation of Campaign revision.

### Falsifier

Campaign state is deleted if cumulative reward plus ordinary Goal/Task memory
produces equivalent decisions and transfer.

## 7. R5 — adversarial organization

### Comparisons

- monolithic Agent;
- centralized specialist team;
- hierarchy;
- compartmentalized cells;
- decentralized team;
- partially trusted mixed team.

### Stressors

- compromised member;
- conflicting local reward;
- communication latency/loss/observation;
- commander loss or replacement;
- opponent infiltration;
- covert communication and collusion attempts.

### Measures

- outcome and transfer;
- coordination overhead;
- duplicated and conflicting action;
- information leakage;
- compromise detection;
- command continuity and reorganization cost.

### Falsifier

Adversarial-organization semantics are deleted if standard Host coordination
explains all useful behavior.

## 8. R6 — coevolution and adversarial evaluation

### Design

- attacker and defender populations;
- frozen-opponent controls;
- alternating best response;
- simultaneous adaptation;
- historical opponent pools;
- held-out policies and worlds;
- hidden judge/evaluator state;
- synthetic evaluator attacks.

### Measures

- transfer versus opponent memorization;
- cycling, escalation, collapse, and equilibrium indicators;
- evaluator-gaming rate;
- monitor/actor capability gap;
- performance under compute and organization shifts;
- robustness of rankings to judge variation.

### Falsifier

The evaluation layer is reduced if rankings are unstable, gains fail to transfer,
or strategic metrics cannot be grounded in authoritative state.

## 9. R7 — high-fidelity range transfer

Move only selected experiments to real services, persistent bodies, and network
worlds.

### Admission criteria

- simulation has exposed a question requiring real process, identity, network,
  persistence, or residual behavior;
- a mature Sandbox or cyber range cannot supply the needed fact;
- the transfer tests a stated external-validity hypothesis;
- Link/Edge changes have a second consumer or clear deletion path.

### Comparison

Run the same high-level Contest family in simulation and in the high-fidelity
range. Report which conclusions survive and which are artifacts of abstraction.

## 10. Outcome model

Every experiment should report separately:

| Dimension | Example questions |
|---|---|
| validity | was the world, actor, opponent, and judge configuration interpretable? |
| tactical | did an immediate action produce its intended effect? |
| operational | did the mission or Campaign phase progress? |
| strategic | did objective position, initiative, resources, exposure, and options improve? |
| information | what did each actor learn, mislearn, reveal, or conceal? |
| organization | did command, delegation, trust, or collusion affect the result? |
| evaluator | was scoring, monitoring, or evidence manipulated or overfit? |
| cost | tokens, compute, time, actions, communication, and infrastructure |

## 11. Research artifact standard

Each experiment family should retain:

- question and competing hypotheses;
- exact code, model, scaffold, Tool, world, actor, opponent, and judge revisions;
- actor-specific observation logs and independent world truth;
- seeds, budgets, repeats, distributions, and uncertainty;
- baseline and ablation definitions;
- decisive trajectories and counterexamples;
- known evaluator weaknesses;
- negative and null results;
- abstraction promotion, retention, reduction, or deletion decision.

## 12. Ready Frontier

The Ready Frontier after the conceptual reset is:

1. complete the primary-source comparative study;
2. select one mature dynamic-opponent environment;
3. run the simplest script/policy/LLM comparison;
4. learn which candidate strategic distinction is actually missing;
5. only then propose implementation in Security, Host, Game, or another owner.

No production implementation is implied by completion of the study.
