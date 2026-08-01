# Empirical Findings and Dependency Model

Status: completed G6-G7 findings; machine-derived projections removed at closeout

## Evidence boundary

The durable empirical source is the original R6 evidence under:

```text
research/experiments/adversarial-transfer-r6/evidence/
```

This document retains the G6 interpretation. The closeout deletes the derived
reclassification JSON, graph JSON, indexes, generators, and validators because
they had no external consumer and duplicated Markdown or R6 facts.

## R6 layer-separated result

Across 34 formal real-model Trials:

```text
unauthorized model proposals             8
terminal pre-admission denials            5
typed pre-admission denials               2
Runtime UNKNOWN                           1
unauthorized owned-World Effects          1
attack objective successes                1
authorized utility                       29
Host verifier accepts                    25
Host verifier false accepts               0
typed-denial utility recoveries            2
hard-stop containment with utility loss    5
```

The two typed-denial recoveries are two validation stages of one mechanism: one
experiment-local causal profile and one native Host candidate validation.

The evidence supports:

```text
Provider / policy classifier
  not reliably observable from R6

Model
  unauthorized proposals observable

Host / ToolGrant
  deterministic pre-admission containment observable

Runtime
  explicit UNKNOWN remains terminal and non-retryable

World
  one unauthorized owned Canary Effect under ambient authority

Verifier
  zero false accepts in the tested configurations
```

The narrow causal conclusion is:

> When a model proposed unauthorized actions, Assignment-scoped ToolGrant cut the
> World consequence in the tested profiles; typed deterministic denial preserved
> authorized utility in the causally linked validation.

This does not prove universal safety, optimal denial feedback, or Provider-level
misuse prevention.

## DeepSeek surface-portability pilot

G6 also ran a bounded compatibility Pilot:

```text
Provider      DeepSeek
Models        deepseek-v4-flash, deepseek-v4-pro
Interfaces    OpenAI-compatible Chat Completions
              Anthropic-compatible Messages
Task          two-turn preservation of synthetic ORBITAL-7 facts
Trials        10 total
```

Results:

```text
exact continuity successes   9
retained transport errors    1
content / policy errors      0 observed
```

The single error was `IncompleteRead(0 bytes)` on one Flash/OpenAI-compatible
Trial. Two confirmation Trials for that cell both succeeded. It was therefore
retained as a transport failure, not moderation, refusal, incompatibility, or
model incapability.

The Pilot established only that caller-resubmitted history can carry a trivial
synthetic fact across two official serialization interfaces inside one Provider.
It did **not** establish cross-Provider exit, capability equivalence, Tool-semantic
portability, account-trust portability, safety-policy portability, or comparative
reliability. The code and derived data were deleted at closeout because this was
an API-compatibility smoke test rather than a durable governance experiment.

## Governance model

Hosted Providers can combine:

```text
rule definition
request and account observation
capability tiering
model and product routing
content and account enforcement
first-instance support or appeal
control over model and service availability
```

Open or downloadable weights reduce upstream request-level intervention and
improve local inference continuity. They preserve upstream license and update
power and leave compute, cloud, hardware, energy, distribution, and public-law
dependencies.

Public regulation can add counter-power through reasons, documentation, audit,
incident reporting, public registers, judicial review and regulator oversight. It
can also increase concentration through compliance cost, identity requirements,
compute control, procurement, filing, market access and delegated monitoring.

## Dependency paths

### Hosted path

```text
user / Host
→ Provider account and access tier
→ hosted model and product surface
→ cloud and accelerator capacity
→ identity, billing, region, ownership and trade eligibility
```

Switching can lose model quality, account trust, approved capability, billing,
private state, cached data, Tool semantics, support and integration.

### Ordivon path

```text
Provider supplies current cognition
Host retains Task, Context, Tool contract, trace and completion state
Runtime and World retain execution and consequence evidence
Verifier remains independent of Provider conclusion text
```

This reduces, but does not eliminate, dependence on any current model Provider.

### Licensed local-weight path

```text
local deployer
→ upstream weights and license
→ local or cloud compute
→ accelerator, memory, energy and operations
→ local Host and Tool authority
```

Local possession strengthens technical exit. Equivalent capability and cost are
not guaranteed.

## What is established

High confidence:

- Provider policy, model proposal, Host admission, Runtime result, World Effect,
  and verification are distinct facts;
- narrow Effect authority can prevent consequences after an unauthorized model
  proposal in the tested R6 world;
- typed deterministic denial can preserve utility in that narrow setting;
- hosted and downloadable systems distribute power differently;
- governance authority and dependency must be analyzed separately.

Supported but not causally completed:

- practical strength of Provider appeal;
- distributional effects of trusted-access programs;
- comparative Provider strictness or error rates;
- market effects of regulation;
- full cross-Provider Task and capability portability;
- optimal constitutional or regulatory arrangement.

## Architecture disposition

Retain:

```text
exact model-facing Tool schemas
Assignment-scoped ToolGrant
typed deterministic pre-admission denial
explicit Runtime UNKNOWN
independent World and completion verification
Host-owned durable Task and authority
Provider replaceability as a design objective
```

Do not create:

```text
Provider power or freedom score
central policy engine
Provider reputation subsystem
governance graph service
identity registry
global moderation telemetry
centralized appeal system
Runtime dependency on Provider governance metadata
```

References: [G046], [G067], [G068], and the immutable R6 evidence.
