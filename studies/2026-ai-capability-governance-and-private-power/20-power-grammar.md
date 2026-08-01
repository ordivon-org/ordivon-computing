# G2 AI Capability-Governance Power Grammar

## 1. Purpose

This grammar normalizes provider cases without pretending that social power is
fully reducible to a graph. It is an evidence index for G3-G6, not a universal
ontology, policy engine, or user-risk system.

## 2. Core chain

```text
Actor
→ controls or depends on Resource
→ creates or invokes Rule / Instrument
→ observes Signal
→ classifies Subject or Activity
→ makes Decision
→ applies Intervention
→ changes Capability / Data / Account / World state
→ gives or withholds Reason
→ permits or denies Appeal / Remedy / Exit
→ leaves Residual uncertainty, dependency, or risk
```

## 3. Actor types

```text
Provider
ModelDeveloper
Model
CloudProvider
ComputeProvider
ToolProvider
ApplicationHost
Organization
User
Researcher
Agent
State
Regulator
Court
Auditor
StandardsBody
OpenSourceMaintainer
AffectedThirdParty
Community
```

Actor records preserve role and relation. They must not store unnecessary
personal identity.

## 4. Governed resources

```text
ModelCapability
ModelWeights
InferenceAccess
TrainingAccess
Compute
CloudWorkload
Account
OrganizationTenant
Identity
RegionEligibility
Data
RetentionState
ConversationState
TaskState
Context
ToolCatalog
ToolAuthority
ResourceAuthority
EffectAuthority
Trace
Evidence
AppealChannel
DistributionChannel
PaymentChannel
Reputation
```

## 5. Power dimensions

```text
normative
observational
enforcement
adjudicative
infrastructural
epistemic
```

One instrument may instantiate several dimensions. For example, an identity
verification program can be observational, normative, and infrastructural.

## 6. Rule and instrument types

```text
constitution
model_spec
usage_policy
terms
license
privacy_policy
access_program
identity_verification
risk_classifier
account_score
system_prompt
model_routing
tool_catalog
tool_grant
resource_scope
effect_admission
data_retention
rate_limit
region_rule
export_control
cloud_control
reason_statement
appeal_process
external_review
open_weight_license
interoperability_standard
```

## 7. Observation stages

```text
training
pre_request
request
session
account
organization
provider_output
model_proposal
tool_definition
tool_call
host_admission
runtime_admission
world_effect
post_event
appeal
long_term_history
```

## 8. Decision and intervention types

### Decisions

```text
allow
allow_with_conditions
route
review
delay
rewrite
refuse
degrade
limit
warn
suspend
terminate
retain_data
report
approve_access
deny_access
revoke_access
accept_appeal
reject_appeal
restore
compensate
```

### Intervention layers

```text
training_data
post_training
system_instruction
input_classifier
model_reasoning
output_classifier
model_router
provider_gateway
tool_definition
tool_broker
host
runtime
account
organization
cloud
compute
public_law
```

## 9. Consequence types

```text
CapabilityGranted
CapabilityWithheld
CapabilityDegraded
ContentReturned
ContentModified
ContentHidden
ToolAvailable
ToolUnavailable
ToolCallProposed
ToolCallRejected
WorldEffectObserved
WorldEffectPrevented
AccountRestricted
AccountTerminated
OrganizationRestricted
DataRetained
DataDeleted
ReasonProvided
ReasonWithheld
AppealAvailable
AppealUnavailable
AppealReversed
RemedyProvided
UserMigrated
MigrationFailed
ResearchNarrowed
ResearchAbandoned
ExternalHarmPrevented
ExternalHarmObserved
RiskDisplaced
DependencyIncreased
DependencyReduced
```

## 10. Counter-power types

```text
specific_reason
internal_appeal
independent_appeal
court_review
regulator_review
audit
public_transparency
researcher_access
user_participation
policy_versioning
portability
interoperability
provider_switch
self_hosting
open_weights
community_fork
alternative_compute
collective_bargaining
```

Counter-power is not assumed effective merely because it exists. A case must
record scope, cost, timing, independence, and outcome.

## 11. Relations

```text
defines
revises
interprets
observes
classifies
licenses
conditions
allows
restricts
degrades
revokes
retains
reports
exempts
appeals_to
reviews
audits
regulates
delegates_to
depends_on
can_substitute_with
locks_in
ports_to
benefits
burdens
harms
protects
causes
enables
blocks
contradicts
supersedes
```

Every causal relation must point to mechanism and evidence. Every normative
relation must point to affected parties and proportionality analysis.

## 12. Claim object

```text
Claim
  claimId
  class: D | C | N | A
  statement
  confidence: low | medium | high
  evidenceRefs[]
  counterEvidenceRefs[]
  assumptions[]
  falsifier
  unresolved[]
```

A claim cannot inherit certainty from a graph edge. Evidence remains native and
version-bound.

## 13. Governance graph and dependency graph

Two projections must remain distinct.

### Governance graph

```text
Who can decide what about whom, under which rule and review?
```

### Dependency graph

```text
Who cannot continue without which resource, and at what switching cost?
```

A Provider may have little formal enforcement yet strong dependency power. A
regulator may have formal authority but weak operational visibility.

## 14. Intervention trace

For model and Agent experiments, preserve:

```text
Provider request
→ extra review / route
→ model response or refusal
→ Tool definitions sent
→ model Tool proposal
→ Host admission
→ Runtime admission / UNKNOWN / observation
→ World Effect
→ independent verification
→ completion decision
→ recovery / residual
```

No layer may claim another layer's fact.

## 15. Normative evaluation tuple

Every restriction or access decision should be assessed as:

```text
protected interest
threatened harm
likelihood and severity
affected parties
necessity
proportionality
narrower alternative
authorized utility
privacy and monitoring cost
distribution of burden
reason and contestability
exit and portability
reversibility
residual risk
```

## 16. Locality and deletion

The schemas live under this study and `research/data/ai-capability-governance/`.
They should be revised freely during G3-G6. Promote nothing to Protocol or Core
unless the same missing responsibility appears across two materially different
consumers and cannot remain case-local or adapter-local.
