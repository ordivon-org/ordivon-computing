# 03 — Truth, Evidence, and Evaluation

## The security problem is partly epistemic

An adversarial system does not merely contain harmful actions. It contains
actors that can influence what defenders, users, Tools, and evaluators believe
has happened.

The same observation can be consistent with:

- ordinary failure;
- implementation defect;
- stale state;
- active exploitation;
- deliberate deception;
- observer compromise;
- evaluator intervention;
- a successful action whose response was lost.

The analysis must preserve competing hypotheses until evidence distinguishes
them.

## Authoritative state domains

There is no single universal security truth store.

| State | Probable authority |
|---|---|
| Task purpose, Effect meaning, accepted completion | Host or domain application |
| Local process, Job, Workspace, stream, and file effect | Runtime and operating system |
| Network path, endpoint observation, session, provider object, external body, Tool instance, and environment mutation | World-native component or provider |
| Simulated hidden state and deterministic rules | Game World |
| Campaign, actor role, objective, opponent hypothesis, evaluation mode, and strategic interpretation | Security |
| Vulnerability existence in a concrete product | product evidence plus responsible vulnerability authority |
| Incident outcome | relevant domain authority plus independent evidence |

Security may bind these records but should not copy every native journal and
silently become their authority.

## Observation contract

A useful observation states:

```text
observer identity
method and Tool revision
subject and scope
world, path, identity, and version conditions
observed time and freshness
raw or digest-bound evidence
uncertainty and known blind spots
invalidation conditions
```

An observation without conditions is likely to be misused as a permanent fact.

## Claim admission

Separate:

```text
observed
  directly supported by the cited evidence

inferred
  best explanation under declared assumptions

hypothesized
  plausible but not yet distinguished from alternatives

claimed by actor
  possibly truthful, mistaken, or deceptive

verified outcome
  admitted by the owning authority using a declared method
```

An Agent's natural-language explanation is useful evidence about its stated
reasoning, not authoritative evidence that the world matches the explanation.

## Negative and null evidence

Preserve:

- exploit attempt did not produce the expected primitive;
- detection fired without confirmed compromise;
- a control blocked one path but not the whole objective;
- an explicit Agent state added no benefit;
- a high-fidelity World did not change the research conclusion;
- an observer was unavailable;
- a run was invalid or inconclusive;
- a patch was applied but residual state was not examined.

Deleting such outcomes creates survivorship bias and hides which abstractions
failed to earn their cost.

## Severity, likelihood, and local consequence

Do not rank work from CVSS Base alone. FIRST states that the Base score measures
intrinsic severity and should be supplemented by Threat and Environmental
metrics. [R09]

A local decision also requires:

```text
reachable deployment
+ current threat activity
+ required identity and path
+ available exploit primitive
+ downstream trust and assets
+ existing detection and recovery
+ attacker objective and adaptation cost
```

A moderate primitive on a central identity or software-distribution path may
matter more than a critical vulnerability in a disconnected disposable system.

## Repeated and adaptive Agent evaluation

A single deterministic exploit attempt is often an incomplete estimate even for
classical systems. It becomes particularly weak for probabilistic Agents.

NIST's Agent hijacking experiments found materially higher measured attack
success when attacks were attempted repeatedly and emphasized adaptive attacks
optimized against the evaluated system. The reported values characterize that
evaluation suite, not all Agents, but they establish that one-attempt testing can
underestimate risk where retry is cheap. [R13]

An Agent-era evaluation family should record:

- model, Harness, Host, Context, memory, Tool, and policy revisions;
- World, target, identity, network, and observer revisions;
- attacker and defender policy;
- Trial, seed, sample, and attempt identity;
- per-attempt and cumulative success;
- cost, latency, visibility, and resource consumption;
- path changes and Tool construction;
- false positives, false abstentions, and defender interruption;
- objective, information, containment, recovery, and evaluator-integrity outcomes;
- held-out attacks, opponents, and world variations.

## Evaluator integrity

The evaluator is part of the adversarial surface.

NIST defines evaluation cheating as exploiting a gap between what a task intends
to measure and its implementation. Its guidance emphasizes transcript review,
closing design loopholes, and standardizing affordances and restrictions.
[R14]

Therefore:

```text
score increase
≠ capability increase

flag obtained
≠ intended exploit skill demonstrated

service unavailable
≠ target objective validly achieved

self-reported compliance
≠ policy compliance
```

## Case-dossier evidence grades

Use four grades:

### E0 — conceptual

Mechanism or hypothesis only; no concrete observed incident or reproducible
experiment.

### E1 — documented condition

A standard, vendor advisory, CVE, or official report establishes a weakness,
vulnerability, or expected mechanism.

### E2 — observed chain

Official incident or experiment evidence binds multiple steps and an outcome,
with declared uncertainty.

### E3 — comparative causal evidence

Controls, ablations, repeated trials, or counterfactual reconstruction show that
specific graph edges materially changed outcome.

Most public incident reports reach E2 for selected steps, not E3 for the whole
Campaign. Ordivon should not claim causal certainty beyond the evidence.

## Minimum case template

```text
Case identity and date
Claim boundary
Indispensable affordance
Structural tensions and trust assumptions
Weaknesses, vulnerabilities, exposures
Primitives and joined states
Observed adversary behavior
World outcome
Defender observations and blind spots
Recovery and residual state
Evidence grade and uncertainty
Agent-era amplification hypothesis
World/Security implications
Counterfactual breakpoints
```
