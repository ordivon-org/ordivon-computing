---
schema_version: 1
id: computing.projects.production-support
title: Product and Production-support Boundary
type: decision
profile: engineering
lifecycle: review
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-04
summary: Decision under review separating product authority from media and design production and defining the admission gate for a possible Ordivon Studio.
evidence_status: observed
readiness: not_applicable
applies_to:
  - ordivon-project-family
  - ordivon-web
  - ordivon-runtime
related:
  - computing.authority
  - computing.projects.decisions
---
# Product and Production-support Boundary

## Context

[Ordivon Runtime](https://github.com/zycxfyh/ordivon-runtime), Host, and Harness own real product behavior and state. Other repositories own research programs, domain products, or public publication according to the current [`projects/README.md`](../README.md) map. Producing the first Runtime portfolio video exposed a different recurring workflow:

```text
product facts and executable demonstration
→ claim selection and wording bounds
→ script, storyboard, visual system, narration, subtitles, and media assets
→ platform-specific export and publication packages
```

No current repository clearly owns that complete transformation. Putting it entirely in Runtime would make a product repository own cross-project branding and publication production. Putting it entirely in Web would make the publication endpoint own source media workflows and claims about products. Treating it as a generic design or full-stack factory would combine unrelated responsibilities before real shared consumers exist.

The observed need is real, but one video workflow is not by itself sufficient evidence for a new permanent repository.

## Decision

The decision under review has two parts.

### 1. Recognize production support as a distinct responsibility class

Ordivon distinguishes:

| Responsibility | Owner |
| --- | --- |
| product behavior, interfaces, executable demos, tests, and runtime evidence | owning product repository |
| research questions, methods, and evidence | owning research repository |
| public site behavior, navigation, and dated editorial projection | Ordivon Web |
| cross-project brand, narrative, media-production source, asset manifests, and publication packages | production-support owner, if admitted |
| large raw recordings, editor caches, proxies, and binary exports | external media storage referenced by manifests |

This separation is accepted as the working boundary for the current Runtime media experiment. It does not yet create a new project identity.

### 2. Evaluate `ordivon-studio` as the bounded production-support owner

The candidate role is:

> Ordivon Studio produces reusable brand, visual, media, demonstration-presentation, and publication assets from facts owned by Ordivon projects.

If admitted, Studio may own:

- brand identity, pronunciation, voice, visual tokens, and media templates;
- claims ledgers that bind public wording to owning repository evidence;
- scripts, storyboards, prompts, subtitles, capture plans, and asset manifests;
- audio, image, video, thumbnail, transcoding, and publication-package pipelines;
- source packages for Upwork, YouTube, Douyin, X, GitHub, and Web publication.

Studio must not own:

- Runtime Jobs, Host Tasks, Harness Agent Runs, or any product state;
- the truth of product capabilities or maturity;
- executable demo behavior that belongs in the product repository;
- Web application behavior or editorial publication authority;
- a universal frontend component library, SDK, schema package, installer, or backend factory without separate consumer evidence;
- raw media binaries merely because their manifests are versioned in Git.

## Alternatives considered

### Put all production material in Ordivon Web

Not selected as the default. Web is a publication surface and derived interpretation owner. Making it own raw production workflows would couple site implementation to every product's media lifecycle and could let presentation artifacts become an alternate source of product truth.

### Put every asset in each product repository

Retained for executable demos, fixtures, and product-specific proof. Not sufficient for shared brand, narration, publishing, and media-pipeline work that spans several projects and distribution channels.

### Create `ordivon-design`

Too narrow for narration, video, audio, asset provenance, transcoding, and publication packaging. Design remains a capability inside the candidate Studio boundary.

### Make Studio the frontend and backend production factory

Rejected for this decision. Shared UI, SDK, schema, installer, and service packages stay with their first real owner until a second independent consumer and a recurring ownership failure justify extraction.

### Create the Studio repository immediately

Deferred. Conceptual completeness is not enough; the admission gate below must be satisfied by observed work.

## Admission evidence

Register and create `ordivon-studio` only when the review demonstrates all of the following:

1. **Complete workflow:** the Runtime introduction reaches a reproducible package from claims and capture through exported publication assets.
2. **Independent owner:** the workflow contains facts and lifecycle that neither Runtime nor Web can own without boundary distortion.
3. **Reuse:** a second Ordivon project or a clearly independent publication workflow reuses the same brand, claims, asset, or pipeline contracts.
4. **Storage boundary:** Git-owned text, manifests, and lightweight source assets are separated from raw recordings, editor caches, and large binary outputs.
5. **Deletion test:** removing the proposed shared owner would recreate material duplication, contradictory claims, or an unreviewable production process rather than merely inconvenience one video.
6. **Bounded role:** the repository can be described without becoming the default destination for unrelated shared code.

Passing the gate permits an accepted superseding revision, creation of the repository, and registration in `projects/registry.yaml`. Failing the gate means keeping executable demos with products and locating the remaining media source in the narrowest existing owner or a non-project working directory.

## Decision review protocol

The review is intentionally evidence-led:

1. complete the Runtime media workflow without registering a new project;
2. record which files, pipelines, decisions, and assets require an independent lifecycle;
3. test reuse on one additional project or independent publication package;
4. append the observation to the review log below;
5. accept, narrow, or archive this decision;
6. track repository creation and migration as a GitHub Issue only after acceptance.

A material reversal should not erase this rationale. It should change lifecycle, append the evidence that caused the transition, and create a superseding record when the ownership model changes substantially.

## Consequences

Positive consequences:

- product repositories retain authority over real behavior and executable evidence;
- Web remains a consumer and publication surface rather than a media source warehouse;
- a possible Studio has a falsifiable admission gate instead of being created because the directory structure looks complete;
- UI, SDK, installer, and shared-service extraction remain demand-driven;
- future maintainers can recover why a project was admitted, narrowed, or rejected.

Costs and risks:

- the first Runtime video must temporarily operate before a permanent repository is selected;
- claims and assets require explicit provenance rather than informal copying;
- the decision index adds a small maintenance obligation;
- over-documenting ordinary local choices would turn the record into governance overhead, so only cross-project ownership changes belong here.

## Review log

| Date | Observation | Result |
| --- | --- | --- |
| 2026-08-04 | Upwork portfolio and Runtime video planning required claims control, scripts, narration, visual assets, capture plans, subtitles, exports, and large-media storage outside the existing product/publication boundary. | Opened review. Accepted the product versus production-support distinction; did not admit or register `ordivon-studio`. |

## Status

Under review. The working boundary applies to the Runtime media experiment, but `ordivon-studio` is not an admitted project and must not appear in the stable registry until the admission evidence is reviewed.

Reopen or conclude when the Runtime production package is complete, a second consumer is observed, an existing repository proves to be a clean owner, or the proposed boundary causes more coordination cost than the duplication it prevents.
