---
schema_version: 1
id: computing.projects.media-studio-transition
title: Media Owner and Studio Packaging Transition
type: decision
profile: engineering
lifecycle: accepted
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-19
summary: Contracts Computing's stale Studio project-identity authority after Ordivon Media became the current repository/semantic owner while Studio remains a Media-local capability and historical package/tool identity.
evidence_status: observed
readiness: not_applicable
applies_to:
  - ordivon-project-family
  - ordivon-media
related:
  - computing.authority
  - computing.projects.decisions
---
# Media Owner and Studio Packaging Transition

## Pressure

Computing historically registered `ordivon-studio` as a stable project-family identity and coupled that registry to generated project maps and the retained world-model observation frontier.

The current owner reality has changed. At observed clean Media revision `5b5dbb4145ca91b575e517b6d56fe119f0853a18`, Ordivon Media states that **Media owns structured mediation**, while **Studio is retained inside Media as the authoring and production capability plane**. Existing `ordivon-studio` CLI/package/tool identities remain valid capability names rather than repository-owner names. The old local `/root/projects/ordivon-studio` checkout is no longer present; `/root/projects/ordivon-media` is the current repository checkout.

Meanwhile, Computing's retained world-model frontier and assimilation rounds contain source-fenced historical `ordivon-studio` observations. Rewriting those records to Media would fabricate provenance and incorrectly transfer historical standing.

## Decision

1. `projects/registry.yaml` is a Computing-local, non-exhaustive project-family packaging/compatibility roster, not semantic-owner identity/currentness authority.
2. The current registry packaging row changes from `ordivon-studio` to `ordivon-media` and points to the current Media repository.
3. `ordivon-studio` remains valid in historical evidence and as a Media-local CLI/package/tool capability identity. Historical uses are not bulk-renamed.
4. Current semantic owner identity, authority and currentness remain owner-native; Atlas generated owner/current-recovery projections may provide non-authoritative recovery where covered.
5. Historical `research/world-model-frontier.json` and `world-model-assimilation-round-*.json` Studio observations remain unchanged. `StudioHistoricalObservation != MediaCurrentAssimilation`.
6. World-model validation/freshness must no longer require the historical frontier project set to equal the current packaging registry. Freshness senses the retained frontier itself.
7. If a historical frontier repository checkout is unavailable, freshness reports a mechanical unavailable state. `MissingLocalCheckout != MissingSemanticOwner`.

## Consequences

- Current Computing navigation no longer presents Studio as the current repository/semantic owner.
- Generated project-family maps become packaging projections rather than owner registries.
- Historical Studio evidence, production commands, package identities and assimilation records remain recoverable without acquiring current owner authority.
- Media does not inherit old Studio world-model assimilation standing by rename or packaging transition.
- A future world-model assimilation may observe Media under its own exact revision if independent research pressure requires it; this decision does not manufacture that round.
- Later independent semantic owners are not added to the Computing packaging roster merely for semantic completeness.

## Rejected

- Copy every current Atlas owner into `projects/registry.yaml`.
- Rewrite historical Studio assimilation rounds as Media.
- Treat `ordivon-studio` CLI/package identity as proof of a current Studio semantic owner.
- Make Atlas a universal packaging registry.
- Create a new global owner/project registry service.

## Reopen conditions

Reopen if a concrete Computing consumer requires a separate Studio repository/package registry identity again, if Media later splits that capability into an independently authoritative project, or if current world-model research independently admits Media as a fresh observed target.
