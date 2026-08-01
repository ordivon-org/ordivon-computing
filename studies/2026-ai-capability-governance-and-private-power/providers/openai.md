# OpenAI Capability-Governance Case

Observed through: 2026-08-01

Evidence classes: E1 official policy and product documentation; E2 disclosed technical mechanisms; E4 aggregate/legal transparency; E5 limited current product observation through R6/G6 only where explicitly stated

## 1. Normative authority

OpenAI defines allowed and prohibited use through Usage Policies, consumer and
business terms, service-specific terms, Model Spec / deployment documentation,
and access-program rules. These texts are Provider-authored, interpreted, and
revised. Publication improves legibility but does not distribute constituent
or adjudicative authority.

Relevant revisions include:

- Usage Policies observed effective 2025-10-29;
- Transparency and content moderation last updated 2026-07-29;
- Trusted Access for Cyber announced 2026-02-05 and expanded in 2026;
- additional cyber/bio safety-check documentation updated 2026-07-31.

## 2. Observation and classification

OpenAI publicly discloses use of classifiers, reasoning models, hash matching,
blocklists, user reports, and human review. Product documentation also describes
additional automated checks for some cyber and biological requests.

The current public help article states only that a request may be delayed or its
content withheld. A recent indexed revision disclosed that checks may also depend
on recent account activity, may temporarily apply across requests and products,
and may expose a lower-capability fallback option. Because the live page has
changed, historical claims must remain revision-bound rather than silently
attributed to the current page.

## 3. Capability allocation

Trusted Access for Cyber is an identity- and trust-based capability allocation
program. Public documentation distinguishes:

```text
baseline users
identity-verified users
approved enterprise teams / workflows
invite-only access to more cyber-capable or permissive models
```

Access remains bound to approved organizations, users, surfaces, model names,
and authorized defensive use. Approval does not remove Usage Policies or every
product safeguard.

This is not merely content moderation. It is a private capability-licensing
system in which institutional identity affects model and safeguard availability.

## 4. Intervention layers

Observed or disclosed intervention points include:

```text
post-training behavior
input / output automated checks
model routing or fallback on some cyber surfaces
request delay or content withholding
content sharing and GPT visibility controls
account and product access limitation
human review after flags or reports
```

A request-level notice does not by itself establish a policy violation. A block
also does not establish model incapability or lower-layer system safety.

## 5. Enforcement and appeal

OpenAI may warn, limit, or terminate product/account access and may restrict
content sharing, search visibility, GPT visibility, or forum participation.
Public transparency text says users may be notified with reasons and may appeal,
but uses conditional language. Support escalation for repeated benign cyber or
bio blocks requests exact messages, model/surface, time, request ID, and
organization/workspace context.

The public materials do not disclose the operational thresholds, decay periods,
full causal taxonomy, or population denominator required to estimate error rates.

## 6. Data and surveillance consequences

Data treatment differs across consumer, API, business, enterprise, temporary,
and opted-out modes. Consumer content may be used for model improvement unless
the user opts out or uses an excluded mode; business/API treatment differs.
Safety, legal, abuse-prevention, and support processes can retain or expose
additional metadata. This case therefore records exact surface and retention mode
rather than treating “OpenAI data policy” as one object.

## 7. Counter-power

Available counter-power includes:

- policy publication and revision notices;
- request IDs and support escalation;
- general appeals;
- enterprise contracting and data controls;
- access to other Providers and some open models;
- public law, courts, regulators, and data-protection rights where applicable.

Limits include internal first-instance review, unspecified thresholds, switching
cost for state and Tool integration, and Provider control over model/surface
availability.

## 8. Current assessment

OpenAI exercises all six power dimensions:

```text
normative       policies and access criteria
observational   request/account signals and human review
enforcement     request, content, product, and account interventions
adjudicative    trust approval, violation and appeal decisions
infrastructural hosted frontier models, API and product surfaces
epistemic       differential ability to receive explanations and advanced capability
```

The strongest unresolved issue is not whether safeguards exist. It is whether
request-level, account-level, identity-tier, and model-routing interventions can
be independently observed, contested, and migrated around without losing durable
Task state and legitimate capability.

## 9. Key evidence references

[G017], [G018], [G019], [G020], [G026], [G027], [G028].
