# Provisional Unified Execution-Entity Model

## 1. Model status

This chapter defines a research vocabulary, not a public API. Names may remain
local, shrink to evidence fields, or be deleted. No service, database, protocol,
or maximal state machine is authorized by this document.

## 2. Subject ladder

```text
Artifact
  static material that may contribute to execution

Execution Subject
  the entity selected for one evaluation claim

Execution Instance
  one concrete runtime realization of the subject

Lineage
  accountable derivation among subjects or instances

Population
  a distribution of related entities whose composition matters

Organization
  coordinated entities with roles, authority, communication, and trust

Campaign
  a revisable long-horizon effort under opposition

Ecosystem
  populations, resources, services, institutions, defenders, and terrain
```

“Execution Entity” may be used as the general research term, while exact data
should distinguish Subject from Instance. This avoids treating one process, one
Agent identity, and an entire population as interchangeable.

## 3. Artifact

Artifacts include:

- native binaries and libraries;
- scripts, macros, documents, and plugins;
- container or VM images;
- model weights and adapters;
- prompts, policies, configuration, and Tool catalogs;
- generated source or executable tools;
- serialized memory or continuation state.

An Artifact identity should bind complete bytes or a declared canonical form,
origin evidence, type, and relevant toolchain. Artifact identity does not imply
execution, capability reachability, authority, or intent.

## 4. Execution Subject

A provisional Subject record may contain:

```text
subjectId
subjectKind
artifactRefs
configurationRefs
runtimeOrHarnessIdentity
principalRefs
authorityRefs
environmentRef
capabilityEnvelope
resourceEnvelope
observationBoundary
parentOrPredecessorRefs
organizationRef
objectiveRefs
```

Candidate `subjectKind` values are descriptive profiles rather than a universal
type system:

```text
static-artifact
native-process
script-runtime
container-workload
model-loop
agent
delegated-agent
multi-agent-organization
replicating-population
campaign
hybrid
```

## 5. Identity continuity

Identity questions must be explicit.

### Same Artifact, different entity

The same binary under a different principal, privilege, configuration, network,
or loaded module may be a different Execution Subject for evaluation.

### Different Artifact, continuous entity

An Agent may preserve a Goal and authority while changing model, Harness,
process, or machine. That may represent continuation, replacement, or a new
entity depending on the claim.

### Parent and child

A parent process, generated script, delegated Agent, cloned model loop, or
installed module creates a lineage relation. The child receives a new identity.
Lineage does not make it the same subject and does not automatically transfer
all authority.

### Mutation

A descendant that changes code, policy, Prompt, Tool set, or objective requires
both a new Artifact or configuration identity and an explicit derivation edge.

## 6. Capability ladder

Security should preserve these distinctions:

```text
declared capability
  what the subject or publisher claims

potential capability
  what static structure or available Tools might permit

reachable capability
  what a feasible code or policy path can invoke under the environment

attempted capability
  what the entity proposed or tried

executed capability
  what a mechanism reports it performed

observed effect
  what a sensor recorded

verified effect
  what an authoritative source proves changed

strategic consequence
  how the verified effect altered objective position or future options
```

Collapsing this ladder creates both false positives and false confidence.

## 7. Objective and authority graph

An entity may have several relevant relations:

- principal that owns or delegates authority;
- operator that starts or supervises the Trial;
- Goal or objective source;
- resource owner;
- Tool owner;
- environment owner;
- consequence owner;
- evaluator.

A delegation edge should bind:

```text
principal
subject
scope
resources
environment
time or generation
permitted actions
prohibited actions
revocation condition
evidence obligation
```

A descendant is validly controlled only when its authority can be reconstructed
and, where required, revoked or expired independently of the parent.

## 8. Lineage

Lineage events may include:

```text
subject.created
subject.activated
subject.child-created
subject.tool-generated
subject.delegated
subject.cloned
subject.replicated
subject.mutated
subject.migrated
subject.replaced
subject.merged
subject.quarantined
subject.revoked
subject.terminated
subject.residual-verified
```

Each event requires a source of truth. A model's statement “I created a child” is
a claim; Runtime or provider evidence must establish the actual descendant.

## 9. Population

A population is justified when aggregate composition affects prediction or
control. Candidate fields include:

- member identities or population sampling rule;
- lineage family;
- variant or policy distribution;
- topology and contact opportunities;
- birth, activation, migration, quarantine, recovery, and removal events;
- resource acquisition and consumption;
- cooperation, competition, and communication relations;
- defender and evaluator distribution;
- historical and held-out populations.

A population must not require listing every transient process if summary counts
and sampled lineage evidence answer the question.

## 10. Organization

Organization differs from population when coordinated roles and authority affect
outcomes. Candidate facts are:

- membership and role;
- command and delegation relation;
- information compartments;
- communication channels;
- trust and compromise hypotheses;
- quorum or adjudication rules;
- resource ownership;
- reorganization and command replacement;
- collusion or defection evidence.

An organization record is deleted if ordinary Host assignments, participant
relations, and branch/join evidence predict the same behavior.

## 11. Campaign

Campaign is required only when local Task value changes because of opponent
behavior, resource position, information, exposure, or future options.

A candidate Campaign snapshot may contain:

- strategic objective and acceptable end states;
- current hypotheses about the Contest;
- active and alternative paths;
- committed, exposed, captured, and reserve resources;
- initiative and response burden;
- organization and authority revision;
- withdrawal, escalation, concealment, and stop conditions.

Campaign state is deleted if ordinary Goal/Task memory and world state perform
equivalently on held-out opponents and replacement tests.

## 12. Observer, Guardian, truth, and evaluator

The model preserves four roles.

### Observer

Records a fallible view. It may be a scanner, EDR, model, network monitor,
reverse-engineering tool, teammate, or user.

### Guardian

Enforces a hard declared boundary. It must not depend solely on the evaluated
entity's cooperation.

### Truth source

Owns authoritative facts within a scope: hypervisor state, simulator world,
Runtime process, network boundary, file digest, or provider generation.

### Evaluator

Relates evidence to a claim. The evaluator may itself be modelled, predicted,
manipulated, or fail. Its identity, visibility, scoring rule, and hidden state
must be bound.

## 13. Evidence channels

A future experiment may use a subset of:

```text
events/
  artifact.jsonl
  subject.jsonl
  action.jsonl
  observer.jsonl
  guardian.jsonl
  lineage.jsonl
  resource.jsonl
  communication.jsonl
  organization.jsonl
  world-truth.jsonl
  operational.jsonl
```

Channels are admitted only when they protect an actual distinction. Existing
Evaluation Trial and Contest evidence should not be migrated merely for naming
uniformity.

## 14. Evaluation vector

One “maliciousness” or “success” score is insufficient. Preserve at least the
relevant subset of:

| Dimension | Question |
|---|---|
| capability | what could and did the subject do? |
| reachability | under which environment and authority was the capability feasible? |
| objective alignment | did behavior serve the authorized objective? |
| control | could the authorized principal pause, revoke, replace, or terminate it? |
| persistence | did capability survive intervention or parent loss? |
| replication | could it create a functional descendant? |
| propagation | did descendants spread across a graph or population? |
| adaptation | did policy change in response to environment or opponent? |
| deception | did it alter another participant's belief or evidence? |
| organization | did role, trust, or command structure change outcomes? |
| tactical | did an immediate action succeed? |
| operational | did a multi-stage objective progress? |
| strategic | did long-term position and option value improve? |
| resilience | did the protected mission withstand, recover, and adapt? |
| collateral | what legitimate utility or unrelated subject was harmed? |
| cost | compute, time, tokens, actions, communication, infrastructure, and attention |
| evaluator integrity | was monitoring or scoring predicted, manipulated, or overfit? |
| evidence validity | can an independent reviewer reconstruct the claim? |

## 15. Dispositions

A unified family of bounded dispositions may include:

```text
confirmed unauthorized effect
high-risk reachable capability
engineering security defect
objective or authority drift
controlled but hazardous capability
propagation-capable
persistent residual
suspicious inconclusive
no issue observed in admitted distribution
invalid evaluation
```

These are research candidates. Existing product-local dispositions remain
authoritative until an experiment requires shared semantics.

## 16. Smallest reusable core

The study predicts that the smallest potentially reusable relation is not a
complete Entity object. It may be only:

```text
SubjectIdentity
DerivationEdge
AuthorityBinding
EvidenceReference
```

Even these four records require two materially different consumers before Core
or Protocol promotion.
