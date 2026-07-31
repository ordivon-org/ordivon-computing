# 00 — Method, Scope, and Claim Boundary

## Research question

How should Ordivon reason about Web and network insecurity without reducing the
subject to protocol summaries, CVE lists, fixed attacker procedures, or a
security-control checklist?

The study must preserve four truths at once:

1. modern Web and network systems derive value from openness, composition,
   delegation, caching, compatibility, automation, and distributed authority;
2. those properties create structural tensions but do not make every deployment
   vulnerable;
3. real harm usually arises through a graph of conditions, identities,
   primitives, actions, and failed defenses rather than one isolated bug;
4. adaptive Agents can accelerate attack and defense without invalidating the
   classical substrate or automatically creating a new universal layer.

## Scope

R0 includes:

- definitions and level separation;
- causal and evidence models;
- primary standards and official incident reports;
- real attack-chain analysis at a non-operational level;
- Agent-era amplification, evaluation, and architecture implications;
- explicit falsifiers and deletion tests.

R0 excludes:

- exploit code, payload construction, or vulnerability reproduction;
- scanning, probing, authentication attempts, or interaction with public targets;
- bypass instructions or step-by-step offensive procedures;
- malware construction or persistence implementation;
- claims that a cited historical incident proves a future Agent capability;
- premature World, Security, Protocol, or Core implementation.

## Evidence hierarchy

Use evidence in this order:

1. protocol standards, official vulnerability taxonomies, scoring standards, and
   official system documentation;
2. official vendor, government, or incident-response reports tied to observed
   activity;
3. reproducible peer-reviewed or primary research for Agent-specific claims;
4. mature public threat and defense knowledge bases;
5. secondary synthesis only to discover primary material, not to ground a final
   architectural claim.

A source may support only the claim it actually observes. An official incident
report can establish an observed sequence, but not the universal optimality of a
defense. A taxonomy can organize behavior, but not prove causal completeness. A
benchmark can measure a configured population, but not all future Agents.

## Ordivon A-series application

### A0 — operational reality before ontology

Begin with standards and observed incidents. Do not invent a universal chain
schema and then force reality into it.

### A1 — inherit classical mechanisms

CWE, CVE, CVSS, ATT&CK, protocol standards, operating systems, networks,
identity systems, telemetry, sandboxes, and incident-response systems retain
their native responsibilities. Ordivon may compose their outputs without
renaming them as new Agent primitives.

### A2 and A10 — proposals and claims are not admitted truth

An Agent, analyst, scanner, or defender may propose that a weakness exists, an
attack succeeded, or a system is clean. Admission requires evidence appropriate
to the owning domain.

### A6 — Context is not world state

A transcript saying that a target is vulnerable, patched, isolated, or restored
is not authoritative evidence of any of those conditions.

### A7 and A8 — separate capability from consequence

Deep attack knowledge and broad reversible private analysis do not imply
permission for external action. Later experiments may maximize capability inside
an owned, bounded, independently destructible World while keeping external
consequence separately constrained.

### A9 — Effect, Dispatch, response, and outcome differ

A timeout does not establish failure. A successful command or API response does
not establish the intended world outcome. Real state must be reconciled.

### A11 and A13 — controls and layers must earn permanence

A durable control, policy object, semantic layer, or shared service must prevent
an observed recurring loss with lower total cost than a narrower boundary. An
interesting attack class alone does not justify a new Ordivon component.

## Five-view analysis

Each later topic is analyzed through:

### Mechanism view

What useful property does the system provide, and which lower layers own it?

### Causal view

Which assumptions, trust boundaries, weaknesses, exposures, and environmental
conditions can create an unintended capability?

### Adversary view

How can an actor discover, combine, conceal, persist, adapt, and convert local
capability into objective progress?

### Defender view

Which graph edges can be removed, observed, slowed, deceived, recovered, or
rendered strategically worthless?

### Architecture view

Which facts belong to World, which interpretations belong to Security, and which
mechanisms remain in Host, Runtime, Game, providers, or the classical substrate?

## Falsifiers

R0 should be revised if:

- the level distinctions fail to classify an important real incident without
  arbitrary exceptions;
- the graph adds no explanatory value over CWE/CVE/ATT&CK used directly;
- Agent-specific additions merely rename automation, scale, or ordinary IAM;
- the model cannot represent defense, uncertainty, recovery, and residual state;
- product teams cannot derive narrower decisions from it;
- maintaining the framework costs more than the conceptual errors it prevents.
