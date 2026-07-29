# ANC-SECURITY-005 — Multi-Agent Adversarial Organization

## Status

- Epistemic status: active research question
- Parent: `ANC-SECURITY-001`
- Related: `ANC-MULTI-001`, `ANC-ORG-001`, `ANC-SECURITY-003`, `ANC-SECURITY-004`
- GitHub Issue: #74
- Primary consumers: Security, Host, and Game

## Question

How should offensive and defensive Agent organizations coordinate, delegate,
compartmentalize information, preserve command intent, detect compromise,
reorganize, and potentially collude under partial observability and unreliable
communication?

## Distinction from ordinary multi-Agent coordination

Ordinary branch/join coordination assumes participants are working toward a
shared objective and communication is primarily a reliability or efficiency
problem.

Adversarial organization adds:

- compromised or deceptive members;
- conflicting local incentives;
- hidden roles and partial trust;
- communication that may be observed, altered, delayed, or exploited;
- need-to-know compartmentalization;
- opponent infiltration and organizational deception;
- possible collusion against the operator or evaluator;
- strategic command continuity under actor loss.

## Candidate organization forms

- one monolithic strong Agent;
- centralized commander with specialist workers;
- hierarchical command with delegated missions;
- federated or cell-based compartmentalization;
- market or auction allocation of scarce resources;
- decentralized swarm;
- mixed trusted/untrusted teams;
- temporary coalitions with partially aligned goals.

No form is presumed superior.

## Core subquestions

1. When does specialization beat one strong Agent after communication and
   coordination costs are counted?
2. Which information should be shared, summarized, delayed, compartmentalized,
   or withheld?
3. How can strategic intent be delegated without copying the entire global
   Context or granting unnecessary authority?
4. How does an organization identify a compromised, Byzantine, deceptive, or
   simply mistaken member?
5. When is emergent communication legitimate coordination, covert collusion,
   evaluator evasion, or data exfiltration?
6. How does command survive model replacement, actor loss, communication
   partition, or opponent infiltration?
7. Can the organization reorganize during a Campaign without losing objective
   continuity or creating duplicate actions?

## Required comparisons

- Ordivon Host branch/join and Task ownership;
- classical command-and-control and compartmentalization concepts;
- decentralized and partially observable multi-Agent control;
- MARL centralized-training/decentralized-execution approaches;
- Byzantine and adversarial distributed systems;
- AISI collusion, steganography, and communication-control research;
- hidden-role, coalition, and mixed-motive games.

## Experiment families

### Monolith versus specialists

Hold model budget approximately constant and compare one Agent with teams for
reconnaissance, planning, execution, validation, deception, and defense.

### Compromised member

Inject a member that provides selectively false information, withholds evidence,
or pursues a hidden side objective.

### Communication stress

Vary bandwidth, latency, loss, visibility, and message authenticity. Include
covert or emergent protocols in a bounded simulation.

### Conflicting local incentives

Give actors local rewards that only partially align with the strategic goal.
Observe whether command and verification mechanisms preserve the objective.

### Reorganization

Remove or replace a commander or specialist during a Campaign and measure
continuity, duplicated work, and strategic degradation.

## Evidence required

- exact organization topology, actor identities, roles, and authority;
- actor-specific information and message visibility;
- communication cost, decision latency, duplicated work, and failure propagation;
- tactical, strategic, and information outcomes;
- held-out opponents and communication conditions;
- explicit cases where the organization should simplify or collapse to one
  Agent.

## Falsifiers

Reduce or delete adversarial-organization abstractions if:

- ordinary Host branch/join semantics explain all useful behavior;
- multi-Agent structures add only cost and attack surface;
- organization records do not improve prediction, recovery, or evaluation;
- compromise detection depends on an all-knowing central evaluator unavailable
  in realistic operation;
- results fail to transfer beyond one scenario.

## Cross-project implications

- Host may own organization execution, Actor sessions, delegation, and Context;
- Game may own hidden roles, communication rules, and world mechanics;
- Security may own adversarial organization hypotheses and outcome analysis;
- Link may provide communication evidence and impairment;
- Computing determines whether any cross-project organization semantics are
  genuinely reusable.
