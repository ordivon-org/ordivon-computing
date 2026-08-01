# The Agent-native game design space

## 1. Beyond dialogue NPCs

The minimum threshold for an Agent-native game is not fluent conversation. Dialogue becomes structurally important only when it can change knowledge, commitment, relationship, authority, coordination, or later action.

A useful decomposition is:

```text
Actor
+ Body
+ Observation
+ Memory
+ Goal and role
+ Capability
+ Relationship
+ Communication
+ World consequence
+ Continuity
```

Different games may omit many of these. The decomposition prevents model prose from being mistaken for participation.

## 2. Open policy over bounded consequence

Classical game design usually pre-enumerates much of the behavior policy. Agent-native design can move some authorship to runtime:

```text
designer authors
world rules, information boundaries, capabilities, incentives,
aesthetic direction, roles, and consequence

Agent authors
interpretation, plan, negotiation, language, composition,
strategy, and selected creations
```

The stable seam is not unrestricted action. It is open policy over bounded and legible consequence.

## 3. Longitudinal characters

A persistent Agent character may change because of:

- observed events;
- shared experiences with the player or other characters;
- commitments made and broken;
- acquired skills or tools;
- changes in role, status, resources, or body;
- reflection or reinterpretation;
- migration across models or Providers while character identity continues.

Persistence is valuable only when it changes future experience. Retaining a transcript or biography that never affects action is storage, not character development.

## 4. Relationships as world state

Relationship should not be one scalar affinity score by default. Candidate dimensions include:

- trust by domain;
- obligations and promises;
- shared artifacts and places;
- remembered cooperation or harm;
- information access;
- authority and dependence;
- expectations about future behavior;
- public versus private claims.

These dimensions should remain local to a game until multiple worlds require the same semantics.

## 5. Self-directed activity

A world becomes more than a Task surface when Actors can initiate bounded activity:

- propose a project;
- explore an unexplained place;
- repair or decorate a shared environment;
- create a tool or artifact;
- organize an event;
- teach another Actor;
- form or leave a group;
- refuse, postpone, or reinterpret a goal;
- play a game inside the world.

Self-direction still needs authored opportunity, resource limits, and consequence. Random background model calls are not agency.

## 6. Capability construction

Research such as Voyager suggests that Agents can accumulate executable, compositional skills through environment feedback and self-verification. In Game, this creates a design space beyond static action catalogs:

```text
Capability need
→ candidate creation
→ bounded build or composition
→ test
→ World admission
→ scoped use
→ observation
→ retain, revise, or retire
```

The Game World must distinguish a proposed artifact from an admitted capability. Arbitrary code execution is neither required nor desirable for the first experiments. A deterministic recipe, constructed tool, authored procedure, or compositional Action can test the same semantic question safely.

## 7. Social and organizational emergence

Generative Agents, AI Town, and Project Sid explore persistent social behavior at different scales. Ordivon should treat their results as possibility evidence, not proof that scale itself creates society.

A credible social world requires explicit environment participation:

- who can observe whom;
- where interaction can occur;
- how time and scheduling work;
- how resources and institutions constrain behavior;
- how messages propagate;
- how consequences persist;
- how the player participates;
- how the system distinguishes World truth from Agent claims.

Many-Agent chat without these structures may generate interesting text while failing as a coherent world.

## 8. Human roles

The player need not always be a commander or avatar. Possible roles include:

- director;
- collaborator;
- resident;
- caretaker;
- creator;
- audience;
- investigator;
- opponent;
- constitutional designer;
- intermittent visitor.

A world may permit role changes over time. Station Zero currently emphasizes remote command; later worlds should not assume that relation is universal.

## 9. Multiple timescales

Agent-native worlds may operate across:

```text
seconds: movement and direct interaction
minutes: tasks, conversations, and encounters
hours: projects and local crises
days: routines, relationships, and institutional change
seasons: construction, migration, and cultural history
```

Each added timescale increases persistence, scheduling, summarization, and cost pressure. The first experiment should show player-visible value at one new timescale before building a general temporal framework.

## 10. Generated worlds and authored coherence

World models and generative tools widen the supply of environments, events, characters, assets, and scenarios. This reduces some production costs but does not remove design.

Ordivon should preserve:

- aesthetic selection;
- rule and identity continuity;
- legible consequence;
- stable interaction contracts;
- player comprehension;
- replayable or at least inspectable history;
- explicit uncertainty when generation breaks consistency.

Generation is a material. It is not the authorial judgment that decides what belongs.
