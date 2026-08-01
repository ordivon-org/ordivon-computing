# Anthropic Capability-Governance Case

Observed through: 2026-08-01

Evidence classes: E1 official policy, terms, Constitution and access documentation; E2 safety/classifier and Responsible Scaling materials; E4 aggregate enforcement and appeal reporting

## 1. Private constitutional authority

Anthropic publishes a Constitution that directly shapes Claude's training and
behavior and describes the document occupying that role as the final
constitutional authority. This is unusually legible compared with hidden model
rules, but the authoring, interpretation, implementation, and revision powers
remain concentrated in Anthropic.

The Constitution therefore creates transparency without automatically creating
co-determination, independent review, or user-selectable constitutional forks.

## 2. Responsible Scaling and trusted classes

Anthropic's Responsible Scaling Policy is versioned and redlined. The current
public version observed in G3 is 3.4, updated 2026-07-08. Its roadmap combines
capability evaluation, deployment safeguards, classifiers, access controls,
trusted-user pathways, red teaming, and escalating requirements as capabilities
increase.

This formalizes different capability classes rather than treating all users and
surfaces as equivalent.

## 3. Cyber safeguards and verification

Real-time cyber safeguards apply to specified Claude model families and separate:

```text
prohibited uses
  default blocked and not relaxable through self-service verification

high-risk dual-use work
  default blocked; eligible legitimate organizations may apply for verification
```

The Cyber Verification Program is organization-bound, surface-dependent, and
requires a retention-enabled workspace. Zero-data-retention organizations may
need a separate workspace. Approval does not remove blocks for prohibited uses.
Some cloud marketplaces do not support the same pathway.

This makes capability conditional on institutional identity, channel, data
retention, and organizational approval.

## 4. Monitoring, enforcement, and scale

Anthropic states that its Safeguards Team designs detections and monitoring and
may warn, throttle, suspend, terminate, block, or modify outputs. Account and
organization action may depend on repeated or cumulative behavior rather than
one request alone.

For January-June 2026, the Transparency Hub reports:

```text
11.4 million banned accounts
398,000 appeals
42,000 appeal overturns
```

Derived descriptive ratios are approximately:

```text
appeals / bans       3.49%
overturns / appeals 10.55%
overturns / bans     0.37%
```

These are not false-positive rates. The public data lacks active-account
denominators, reason categories, duplicate-account handling, automated/manual
shares, and unappealed-error estimates.

## 5. Appeals and procedural limits

Banned users can appeal through an account-linked process. Organizations may be
placed on hold for unusual activity and API warnings may reflect behavior across
the account. Public documentation does not expose the precise thresholds,
lookback windows, decay functions, or the evidence available to appellants.

Commercial terms generally provide more notice and cure structure than consumer
terms. Consumer terms allow broad suspension, termination, data deletion, and
law-enforcement reporting powers in specified conditions.

## 6. Data consequences

Anthropic discloses materially different retention paths:

- ordinary deleted consumer chats are removed from history and generally from
  back-end systems within a shorter period;
- data used for model improvement may be retained in de-identified form for a
  much longer period;
- sessions flagged by automated safety systems may have inputs and outputs
  retained for up to two years;
- trust-and-safety classification scores may be retained for up to seven years.

A safety classification can therefore change the data lifecycle independently of
normal training consent.

## 7. Geography and ownership

Anthropic restricts service to supported regions and may consider controlling
ownership, not merely connection location. Its 2025 policy announcement extended
sales restrictions to entities controlled from unsupported regions, explicitly
including China, even when operating through subsidiaries elsewhere.

This is a geopolitical capability-allocation rule based on organizational
identity and ultimate control.

## 8. Counter-power

Anthropic provides more public structure than many Providers:

- public Constitution;
- versioned Responsible Scaling Policy;
- detailed Usage Policy and access programs;
- aggregate bans, appeals, and overturns;
- data-retention disclosures;
- account appeals and commercial support channels.

These improve legibility. They do not independently constrain the same company
from writing the rule, observing behavior, classifying risk, applying sanctions,
and deciding first-instance appeals.

## 9. Current assessment

Anthropic's governance is best described as an explicit private capability-
administration system:

```text
Constitution
+ capability thresholds
+ classifiers
+ organization licensing
+ retention conditions
+ geography / ownership rules
+ account enforcement
+ internal appeal
```

It is more transparent than a purely hidden system and in several dimensions
more systematic and restrictive than OpenAI. The comparison remains dimensional,
not scalar.

## 10. Key evidence references

[G021], [G022], [G023], [G024], [G025], [G029], [G030], [G031], [G032], [G033], [G034].
