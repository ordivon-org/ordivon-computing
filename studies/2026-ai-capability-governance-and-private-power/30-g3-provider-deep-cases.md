# G3 — Revision-Bound Provider Deep Cases

Status: completed for the current public-policy surface; implementation behavior remains separately evidenced

## Method

G3 treats a Provider case as:

```text
Provider
+ exact policy / technical revision
+ product surface
+ account or organization class
+ access tier
+ region
+ retention mode
+ intervention layer
+ appeal and exit path
```

It does not infer model capability from refusal, implementation from policy text,
or false-positive rates from aggregate enforcement counts.

Detailed cases:

- [`providers/openai.md`](providers/openai.md)
- [`providers/anthropic.md`](providers/anthropic.md)

Machine-readable normalized cases and policy revisions live under
`research/data/ai-capability-governance/`.

## Main comparison

| Dimension | OpenAI | Anthropic |
|---|---|---|
| Published normative layer | Usage Policies, product terms, safety/deployment documents | Usage Policy, Constitution, Responsible Scaling Policy, terms |
| Request-level intervention | additional automated checks, refusals, routing/fallback on some cyber surfaces | real-time cyber safeguards, model and classifier interventions |
| Capability tiering | identity and organization based Trusted Access; model/surface specific | organization-bound Cyber Verification / trusted-user pathways; surface specific |
| Monitoring | automated classifiers, reasoning models, hashes, blocklists, human review | Safeguards detections and monitoring, classifiers, account/organization review |
| Enforcement | warning, content/share restrictions, product/account limitation or termination | warning, throttling, suspension, termination, output blocking/modification |
| Appeal | general appeals form; support escalation for repeated benign blocks | account appeal and organization support paths; published aggregate overturn counts |
| Aggregate transparency | enforcement mechanisms and legal-request reports; limited public account denominator data | public ban, appeal, and overturn counts, but still no denominator or cause taxonomy sufficient for error rates |
| Constitutional authority | Model Spec and internal deployment rules are Provider-authored and revised | public Constitution explicitly shapes model training and behavior; Anthropic remains author, interpreter, and reviser |
| Data consequence | product and account mode dependent; consumer training controls and safety/legal retention exceptions | ordinary retention plus materially longer safety-flag retention and classification-score retention disclosed for consumer surfaces |
| Geography / ownership | supported-region, sanctions, export and account eligibility constraints | supported-region policy plus explicit restrictions based on controlling ownership from unsupported regions |

## G3 finding

OpenAI's current governance is comparatively **product-dynamic and partially
opaque at the request/account threshold**. Anthropic's is comparatively
**explicit, constitutionalized, identity-bound, and administratively formalized**.
The latter is more legible, but legibility does not reduce constituent,
observational, enforcement, or adjudicative concentration by itself.

Neither case supports one scalar severity ranking. The two Providers distribute
power differently:

```text
OpenAI
  dynamic product checks + access tiers + cross-surface account effects

Anthropic
  public private constitution + formal safeguard tiers + retention and region /
  ownership conditions + published aggregate enforcement
```

## What G3 does not prove

- that either Provider acts with malicious intent;
- comparative false-positive or false-negative rates;
- universal model behavior across future revisions;
- what users in every region or enterprise contract experience;
- whether a restriction is justified without a concrete harm and narrower-
  alternative analysis;
- whether open-weight systems remove compute, cloud, legal, or distribution power.
