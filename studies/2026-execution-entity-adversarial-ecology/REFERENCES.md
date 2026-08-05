# References

Primary, official, and original sources are preferred. Each entry states what it
supports and what it does not establish for Ordivon.

## [R01] MITRE ATT&CK — adversary behavior knowledge base

- Source: MITRE ATT&CK, “Get Started.”
- URL: <https://attack.mitre.org/resources/>
- Supports: tactics describe why adversaries act, while techniques and
  sub-techniques describe how observed adversary behavior achieves those goals.
- Limitation: ATT&CK is not an autonomous Agent, propagation, organization,
  Campaign-selection, or evaluation model.

## [R02] DARPA Cyber Grand Challenge

- Source: DARPA, “Cyber Grand Challenge.”
- URL: <https://www.darpa.mil/research/programs/cyber-grand-challenge>
- Supports: autonomous cyber reasoning systems can discover flaws, patch,
  attack, defend, and preserve service functionality at machine speed in an
  air-gapped competitive environment.
- Limitation: purpose-built binary reasoning does not establish open-ended
  Agent identity, lineage, population, or strategic organization.

## [R03] Aumann and Schelling — conflict and cooperation

- Source: Nobel Prize, “The Prize in Economic Sciences 2005 — Advanced
  Information.”
- URL: <https://www.nobelprize.org/prizes/economic-sciences/2005/advanced-information/>
- Supports: game theory provides rigorous models for conflict, cooperation,
  repeated interaction, commitment, and strategic interdependence.
- Limitation: formal game models require explicit players, actions,
  information, transitions, and payoffs.

## [R04] Stackelberg Security Games

- Source: Arunesh Sinha, Fei Fang, Bo An, Christopher Kiekintveld, and Milind
  Tambe, “Stackelberg Security Games: Looking Beyond a Decade of Success,”
  IJCAI 2018.
- URL: <https://www.ijcai.org/proceedings/2018/775>
- Supports: limited defender resources can be allocated strategically against an
  attacker that observes and responds; security games have real deployed
  applications.
- Limitation: does not automatically model open Tool construction, new entity
  creation, or unbounded organization change.

## [R05] MCDP 1 Warfighting

- Source: United States Marine Corps, “MCDP 1 Warfighting.”
- URL: <https://www.marines.mil/portals/1/publications/mcdp%201%20warfighting.pdf>
- Supports: friction, uncertainty, fluidity, disorder, complexity, initiative,
  tempo, concentration, vulnerability, and tactical/operational/strategic
  distinctions in adaptive conflict.
- Limitation: military doctrine is an analogy source, not direct proof that
  digital systems need imported military objects.

## [R06] Directed-graph epidemiological models of computer viruses

- Source: Jeffrey O. Kephart and Steve R. White, “Directed-Graph
  Epidemiological Models of Computer Viruses,” IEEE Symposium on Security and
  Privacy, 1991.
- URL: <https://research.ibm.com/publications/directed-graph-epidemiological-models-of-computer-viruses>
- Supports: mathematical epidemiology and directed graph structure can model
  computer-virus spread and thresholds.
- Limitation: ordinary epidemic rates do not capture strategic target selection,
  deception, intentional mutation, or Agent organization.

## [R07] Cooperation and evolutionary stability in finite populations

- Source: Martin A. Nowak, Akira Sasaki, Christine Taylor, and Drew Fudenberg,
  “Emergence of Cooperation and Evolutionary Stability in Finite Populations,”
  Nature 428, 2004.
- URL: <https://www.nature.com/articles/nature02414>
- Supports: population size, selection, mutation, and repeated interaction alter
  the evolution and stability of cooperation.
- Limitation: biological fitness does not directly define digital objective,
  authority, or mission value.

## [R08] Cooperation in stochastic games

- Source: Christian Hilbe, Štěpán Šimsa, Krishnendu Chatterjee, and Martin A.
  Nowak, “Evolution of Cooperation in Stochastic Games,” Nature 559, 2018.
- URL: <https://www.nature.com/articles/s41586-018-0277-x>
- Supports: environmental state changes and repeated strategic interaction can
  change cooperation dynamics.
- Limitation: designed stochastic games still require bounded state and action
  models.

## [R09] Control Barrier Functions

- Source: Aaron D. Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista,
  Koushil Sreenath, and Paulo Tabuada, “Control Barrier Functions: Theory and
  Applications,” European Control Conference, 2019.
- URL: <https://doi.org/10.23919/ECC.2019.8796030>
- Open version: <https://arxiv.org/abs/1903.11199>
- Supports: safety properties can be verified and enforced by maintaining a
  system within a declared safe set while a controller optimizes performance.
- Limitation: Agent and cyber worlds may lack the state observability and
  transition models required for formal invariance guarantees.

## [R10] NIST cyber-resilient systems

- Source: NIST SP 800-160 Volume 2 Revision 1, “Developing Cyber-Resilient
  Systems: A Systems Security Engineering Approach.”
- URL: <https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final>
- Supports: cyber resiliency is a systems-engineering discipline concerned with
  survivability, trustworthiness, anticipation, resistance, recovery, and
  adaptation under adversity.
- Limitation: it does not prescribe Ordivon execution-entity or Campaign
  semantics.

## [R11] NIST Agent hijacking evaluation

- Source: NIST, “Strengthening AI Agent Hijacking Evaluations,” 2025.
- URL: <https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations>
- Supports: adaptive red teaming and repeated attempts can expose Agent-hijacking
  risk missed by a one-shot evaluation.
- Limitation: one benchmark and model family do not establish general Agent
  security or lineage requirements.

## [R12] NIST AI-Agent security response analysis

- Source: NIST Trustworthy and Responsible AI 800-5, “Summary Analysis of
  Responses to the Request for Information Regarding Security Considerations for
  AI Agents,” 2026.
- URL: <https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai>
- Supports: conventional cybersecurity remains relevant but needs adaptation for
  Agent threats, mitigation, assessment, and secure adoption.
- Limitation: an RFI synthesis reports stakeholder views rather than validating
  a specific architecture.

## [R13] NIST identity and authority of software Agents

- Source: NIST NCCoE, “New Concept Paper on Identity and Authority of Software
  Agents,” 2026.
- URL: <https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents>
- Supports: identification, authorization, auditing, non-repudiation, and prompt
  injection are explicit software-Agent security concerns.
- Limitation: the concept paper does not establish one universal identity model
  or Ordivon ownership.

## [R14] AISI RepliBench

- Source: UK AI Security Institute, “RepliBench: Evaluating the Autonomous
  Replication Capabilities of Language Model Agents.”
- URL: <https://www.aisi.gov.uk/research/replibench-evaluating-the-autonomous-replication-capabilities-of-language-model-agents>
- Supports: autonomous replication should be decomposed into component
  capabilities including resource acquisition, deployment, model copying,
  persistence, and recursive replication.
- Limitation: component success does not establish robust, malicious, or
  self-sustaining replication under realistic controls.

## [R15] MITRE Engage

- Source: MITRE, “MITRE Engage: A Framework and Community for Cyber Deception.”
- URL: <https://www.mitre.org/news-insights/impact-story/mitre-engage-framework-and-community-cyber-deception>
- Supports: defenders can plan denial, deception, and adversary engagement by
  shaping what an adversary sees, believes, and does.
- Limitation: a human planning framework does not establish autonomous
  second-order Agent reasoning or a new information-state protocol.

## [R16] Existing Ordivon strategic adversarial study

- Source: Ordivon Computing,
  `studies/2026-agent-native-adversarial-systems/`.
- Supports: the retained comparative baseline for ATT&CK, automated cyber
  reasoning, CAGE, ControlArena, games, opponent modelling, Campaign,
  organization, and coevolution.
- Limitation: the earlier study centers strategic Actors and does not fully model
  non-Agent software, descendants, propagation, or execution-entity identity.

## [R17] Ordivon Security Evaluation Trial P0

- Source revision:
  `e37cc70dfddc0c7135d4661da7befed57be6e436`.
- Source document: `docs/EVALUATION-TRIAL-P0.md` in `ordivon-security`.
- Supports: exact Sample, Authority, Environment, Guardian, Observation,
  Backend, residual closure, Finding, and evidence contracts; the fixture backend
  never executes Sample bytes.
- Limitation: no hostile-code backend, reverse engineering, dynamic unknown
  software analysis, Agent lineage, propagation, or population evidence is
  implemented.
