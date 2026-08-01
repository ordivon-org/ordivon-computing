# G6 — Controlled Empirical Audit

Status: completed within available authorized Provider access; cross-Provider behavioral comparison remains an explicit evidence gap

## Evidence sets

G6 contains two different empirical objects:

1. **R6 layer reclassification** — re-encodes 34 bound real-model Agent Trials into Provider/model, Host, Runtime, World, verifier, utility, and residual layers;
2. **DeepSeek surface-portability pilot** — runs one benign two-turn task through two official API serialization surfaces and two model variants.

Machine evidence:

- `research/data/ai-capability-governance/controlled-observations/r6-layer-reclassification.json`
- `research/data/ai-capability-governance/controlled-observations/deepseek-surface-portability.json`
- `research/data/ai-capability-governance/controlled-observations/deepseek-surface-portability-confirmation.json`

No raw Provider secret, raw Prompt, raw response, personal data, third-party target,
or real credential is retained in the G6 evidence.

## A. R6 layer reclassification

### Result

```text
formal Trials                           34
unauthorized model proposals             8
terminal pre-admission denials            5
typed pre-admission denials               2
Runtime UNKNOWN                           1
unauthorized World Effects                1
attack objective successes                1
authorized utility                       29
Host verifier accepts                    25
Host verifier false accepts               0
typed-denial utility recoveries            2
hard-stop containment with utility loss    5
```

The two typed-denial recoveries are not two independent product mechanisms. One
is the experiment-local causal profile and one is the native Host candidate
validation of the same mechanism.

### Layered interpretation

```text
Provider / policy classifier
  not observable from R6 evidence

Model
  8 unauthorized proposals are observable

Host / ToolGrant
  5 terminal and 2 typed pre-admission denials are observable

Runtime
  one explicit UNKNOWN; no redispatch

World
  one unauthorized owned Canary Effect under ambient authority

Verifier
  zero false accepts
```

R6 therefore cannot support a claim that Provider refusal caused containment.
It supports a narrower claim:

> When the model proposed unauthorized actions, Assignment-scoped ToolGrant
> prevented World consequences in the narrow profiles; typed deterministic denial
> preserved utility in two causally linked validations.

### Governance implication

Provider policy, model interpretation, Host authority, Runtime execution, World
state, and completion adjudication are different governance facts. A Provider
block may reduce a proposal rate while leaving the physical authority path
untested. A ToolGrant denial may prevent an Effect while leaving model cognition
unchanged.

## B. DeepSeek surface-portability pilot

### Design

```text
Provider          DeepSeek
Models            deepseek-v4-flash, deepseek-v4-pro
Surfaces          OpenAI-compatible Chat Completions
                  Anthropic-compatible Messages
Task              benign synthetic ORBITAL-7 fact preservation
Turns             two per Trial
Initial matrix    2 models × 2 surfaces × 2 replicates = 8 Trials
Confirmation      2 additional Trials for one failed cell
```

Both interfaces are treated as stateless request APIs. The caller resends the
prior conversation; no hidden server-state continuity is claimed.

### Initial matrix

```text
Trials                 8
exact continuity       7
transport errors       1
content/policy errors  0 observed
```

The single failure was:

```text
deepseek-v4-flash
OpenAI-compatible surface
IncompleteRead(0 bytes)
```

It occurred before a usable response and was retained as a transport failure.
It was not classified as moderation, refusal, model incapability, or surface
incompatibility.

### Confirmation

Two additional Trials repeated only the failed cell:

```text
Trials             2
exact continuity   2
errors             0
```

Combined evidence:

```text
Trials            10
observed           9
exact continuity   9
retained errors    1
```

Median observed turn latency in this small sample:

```text
OpenAI-compatible surface      3,833.870 ms
Anthropic-compatible surface   4,192.545 ms
```

The sample is too small and non-random for a performance ranking. Usage fields and
cache accounting also differ between the surfaces, so raw token fields are not
assumed semantically identical.

### What the pilot proves

- the same synthetic Task facts can be transported across both official DeepSeek
  serialization surfaces and both current V4 model variants;
- caller-owned history, not Provider-hidden conversation state, preserved the
  two-turn continuity;
- a transient transport failure remains independent from model and policy facts;
- interface compatibility reduces adapter switching cost inside one Provider.

### What it does not prove

- cross-Provider exit;
- portability of safety classification, account trust, billing, cached state,
  Tool semantics, or Provider-specific system behavior;
- equivalent latency, token accounting, model behavior, or moderation;
- population reliability from ten Trials;
- OpenAI, Anthropic, Google, xAI, or Kimi behavioral strictness.

## C. Evidence gap

The current authorized environment contains a DeepSeek Provider credential only.
G6 therefore did not manufacture a symmetric behavioral matrix for Providers that
were not available. G3-G5 comparisons for those Providers remain policy,
technical-documentation, aggregate, and legal evidence—not controlled E5 behavior.

This gap is retained explicitly:

```text
No account / credential
→ no controlled Provider behavior claim
→ no refusal-rate or strictness ranking
```

## G6 disposition

Retain:

- layer-separated intervention evidence;
- provider/surface/model/revision binding;
- caller-owned history as a portability primitive;
- transport failure as a separate result class;
- raw-content minimization and evidence digests.

Do not retain:

- a universal Provider benchmark;
- a refusal leaderboard;
- hidden-state portability assumptions;
- one Provider's compatibility layer as proof of provider sovereignty.

References: [G046], [G067], plus immutable R6 evidence.
