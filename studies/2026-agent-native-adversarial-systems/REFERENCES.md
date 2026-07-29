# References

Primary and original sources are preferred. Descriptions state what each source
supports and what it does not establish for Ordivon.

## [R01] MITRE ATT&CK — Enterprise tactics

- Source: MITRE ATT&CK, “Enterprise Tactics.”
- URL: <https://attack.mitre.org/tactics/enterprise/>
- Supports: tactics represent adversary tactical goals across reconnaissance,
  access, execution, persistence, discovery, movement, collection, command and
  control, exfiltration, and impact.
- Limitation: ATT&CK is a behavior knowledge base, not an autonomous Campaign,
  opponent-belief, or strategic-resource model.

## [R02] MITRE ATT&CK — Get Started

- Source: MITRE ATT&CK, “Get Started.”
- URL: <https://attack.mitre.org/resources/get-started/>
- Supports: ATT&CK organizes tactics, techniques, sub-techniques, and procedures
  from observed adversary behavior and is not one mandatory linear sequence.
- Limitation: does not determine how an adaptive Agent should select or revise
  behavior against a particular opponent.

## [R03] MITRE D3FEND

- Source: MITRE D3FEND, “About D3FEND.”
- URL: <https://d3fend.mitre.org/about/>
- Supports: D3FEND is a semantic knowledge graph for cybersecurity
  countermeasures and their engineering mechanisms and relations to offensive
  techniques.
- Limitation: does not prescribe optimal strategic selection or prove
  effectiveness against adaptive Agent opponents.

## [R04] MITRE Engage

- Source: MITRE Engage, “About Engage.”
- URL: <https://engage.mitre.org/about/>
- Supports: adversary engagement, denial, and deception can be planned as a
  deliberate defensive activity that influences adversary behavior.
- Limitation: primarily a human planning framework rather than an autonomous
  second-order Agent reasoning system.

## [R05] MITRE Engage Handbook

- Source: MITRE Engage, “Engage Handbook.”
- URL: <https://engage.mitre.org/engage-handbook/>
- Supports: deception planning considers what the adversary should do, what it
  must believe, and what it must observe to form that belief.
- Limitation: does not establish that Ordivon needs a new information-state
  protocol.

## [R06] DARPA Cyber Grand Challenge

- Source: DARPA, “Cyber Grand Challenge.”
- URL: <https://www.darpa.mil/research/programs/cyber-grand-challenge>
- Supports: automated Cyber Reasoning Systems can find flaws, patch software,
  attack opponents, defend hosts, and preserve service functionality in an
  all-machine competition.
- Limitation: focuses on purpose-built binary reasoning and competition rather
  than open-ended language/tool Agent strategy and organization.

## [R07] DARPA AI Cyber Challenge — scoring and final results

- Source: DARPA, “AI Cyber Challenge Scoring and Final Competition Results.”
- URL: <https://www.darpa.mil/news/2025/ai-cyber-challenge-scoring>
- Supports: AIxCC evaluated autonomous systems on vulnerability discovery,
  proof, patching, patch quality, and real open-source software challenges.
- Limitation: competition results do not by themselves establish strategic
  opponent modelling or long-horizon Campaign capability.

## [R08] DARPA AI Cyber Challenge

- Source: DARPA, “AI Cyber Challenge.”
- URL: <https://aicyberchallenge.com/>
- Supports: AI and LLM components are composed with mature analysis systems for
  autonomous vulnerability discovery and remediation; finalist systems and
  resources were released openly.
- Limitation: the primary task remains software vulnerability discovery and
  repair.

## [R09] CAGE Challenge overview

- Source: CAGE Challenge, “About.”
- URL: <https://cage-challenge.github.io/>
- Supports: CybORG/CAGE provides challenge environments for autonomous cyber
  defense and progressively complex Red/Blue research.
- Limitation: individual challenges use designed action, observation, and reward
  structures.

## [R10] CAGE Challenge 4

- Source: CAGE Challenge, “CAGE Challenge 4.”
- URL: <https://cage-challenge.github.io/cage-challenge-4/>
- Supports: multi-Agent reinforcement-learning defense in an enterprise cyber
  scenario with changing missions, communications, and multiple actors.
- Limitation: does not establish open-ended Agent tool construction or general
  strategic transfer.

## [R11] CAGE Challenge 4 — Getting Started

- Source: CAGE Challenge 4 documentation, “Getting Started.”
- URL: <https://cage-challenge.github.io/cage-challenge-4/pages/tutorials/01_Getting_Started/2_Getting_Started/>
- Supports: Red, Blue, and Green actors; action duration; network and service
  effects; decoys; monitoring; analysis; restore and remove actions; false alerts
  and mission phases.
- Limitation: documentation describes one designed environment rather than a
  universal adversarial ontology.

## [R12] CAGE Challenge 4 — Red Agent and actions

- Source: CAGE Challenge 4 documentation, Red agents and action space.
- URL: <https://cage-challenge.github.io/cage-challenge-4/pages/tutorials/02_Agents/2_Red_Agent/>
- Supports: baseline Red behavior can use finite-state strategies and predefined
  cyber actions, providing a strong non-LLM baseline.
- Limitation: a finite action space may omit open-ended Tool creation and
  strategic reorganization.

## [R13] Microsoft CyberBattleSim

- Source: Microsoft Research, “CyberBattleSim.”
- URL: <https://www.microsoft.com/en-us/research/project/cyberbattlesim/>
- Supports: reinforcement-learning agents can be studied in an abstract simulated
  enterprise-network cyber environment.
- Limitation: high-level abstraction and fixed interfaces simplify real-world
  tools, information conflict, and organization.

## [R14] UK AISI ControlArena

- Source: UK AI Security Institute, ControlArena documentation.
- URL: <https://control-arena.aisi.org.uk/>
- Repository: <https://github.com/UKGovernmentBEIS/control-arena>
- Supports: Settings, main and side tasks, honest/attack modes, trusted and
  untrusted policies, monitors, protocols, scorers, and safety/usefulness
  evaluation for potentially subversive Agents.
- Limitation: primarily frames an untrusted policy inside a control protocol,
  not a complete theory of multiple competing strategic Campaigns.

## [R15] UK AISI Research Agenda

- Source: UK AI Security Institute, “Research Agenda.”
- URL: <https://www.aisi.gov.uk/research-agenda>
- Supports: future control research must consider long-horizon behavior,
  sabotage, collusion, steganography, monitoring evasion, and increasingly
  capable adversarial Agents.
- Limitation: research agenda statements identify open problems rather than
  validated Ordivon architecture.

## [R16] Partially Observable Stochastic Games

- Source: Eric A. Hansen, Daniel S. Bernstein, and Shlomo Zilberstein,
  “Dynamic Programming for Partially Observable Stochastic Games.”
- URL: <https://arxiv.org/abs/1301.3787>
- Supports: formal sequential multi-agent decision-making under hidden state and
  partial observation.
- Limitation: formal models require declared state, action, observation, and
  reward structures and do not automatically cover open-ended Tool systems.

## [R17] OpenSpiel

- Source: Marc Lanctot et al., “OpenSpiel: A Framework for Reinforcement Learning
  in Games.”
- URL: <https://arxiv.org/abs/1908.09453>
- Repository: <https://github.com/google-deepmind/open_spiel>
- Supports: extensive-form and normal-form game research, imperfect information,
  algorithms, evaluation, and multi-agent learning baselines.
- Limitation: a game framework is not itself a persistent Agent Host or open
  digital-world Campaign system.

## [R18] Opponent Modelling in Deep Reinforcement Learning

- Source: He He et al., “Opponent Modeling in Deep Reinforcement Learning.”
- URL: <https://arxiv.org/abs/1609.05559>
- Supports: learned representations of other agents can address non-stationarity
  and improve policy decisions in multi-agent settings.
- Limitation: does not establish that explicit natural-language or durable
  opponent records outperform latent policy representations.

## [R19] Melting Pot paper

- Source: Joel Z. Leibo et al., “Scalable Evaluation of Multi-Agent Reinforcement
  Learning with Melting Pot.”
- URL: <https://arxiv.org/abs/2107.06857>
- Supports: evaluation across cooperation, competition, deception, trust,
  reciprocation, and unfamiliar social situations and partners.
- Limitation: substrates remain designed games rather than unrestricted cyber or
  Tool environments.

## [R20] Melting Pot repository

- Source: Google DeepMind, Melting Pot.
- URL: <https://github.com/google-deepmind/meltingpot>
- Supports: executable multi-agent substrates, scenarios, background populations,
  and held-out social-generalization evaluation.
- Limitation: does not provide Ordivon Host/Runtime continuity or strategic
  Campaign semantics.
