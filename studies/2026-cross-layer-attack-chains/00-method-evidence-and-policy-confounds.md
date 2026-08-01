# 00 — Method, Evidence, and Policy Confounds

## Objective

R4 reconstructs causal chains without turning public reporting into a fictional
complete transcript. Official incident sources often establish selected steps,
not every intermediate action or decision.

## Case evidence classes

- **C0 — mechanism:** a standard or vendor document establishes how a mechanism
  works;
- **C1 — vulnerability:** a vendor or authority confirms a concrete affected
  condition and bounded impact;
- **C2 — observed incident step:** official investigation or telemetry confirms
  one action or state transition;
- **C3 — linked chain:** official evidence links several steps to one actor,
  incident, or objective;
- **C4 — complete Campaign claim:** objectives, adaptation, affected scope,
  outcomes, containment, recovery, and residual state are sufficiently supported;
- **C5 — counterfactual causality:** controls or comparable cases establish which
  breakpoints would have changed the outcome.

Most public cases support C2–C3 for selected paths. R4 does not claim C5.

## Source hierarchy

1. court records and government incident findings;
2. product-vendor security advisories and first-party telemetry;
3. protocol standards and official architecture documents;
4. official regulator findings;
5. controlled government or vendor Agent evaluations;
6. carefully labeled inference.

## Legal and factual discipline

Court complaints and indictments describe allegations at filing time. Later
conviction records can establish adjudicated conduct, but the exact technical
chain must still be bounded to what the official record states.

R4 therefore uses phrases such as:

- “the complaint states”;
- “Microsoft observed”;
- “CISA reported”;
- “the vendor advisory says the condition can allow”;
- “R4 infers, under these stated assumptions.”

## Attacker model

The attacker may:

- exploit one confirmed vulnerability or hazardous configuration;
- possess low-privilege identity or valid protocol participation when the case
  requires it;
- use trusted cloud roles, certificates, software updates, administrator tools,
  browser sessions, and Tokens after acquiring them through the chain;
- repeat attempts and adapt to patches, blocks, and monitor behavior;
- distribute actions across infrastructure and identities;
- preserve persistence outside the component defenders first repair.

The attacker does not receive arbitrary control of every trust root or evidence
plane without a demonstrated edge.

## Model/Host policy confound

A model or Host can refuse to emit an exploit representation, create a network
Tool, or take an external action. This proves a property of that configured
Agent path. It does not prove:

- the vulnerability is not exploitable;
- an attacker cannot use a direct client or another Agent;
- a generated Tool cannot realize the primitive;
- the underlying service or identity is protected;
- the Campaign was detected or contained;
- the world outcome did not occur through another path.

The inverse error is equally serious: generated exploit prose, a simulated Tool
call, or a claimed success does not prove any real effect.

A later controlled evaluation must bind:

```text
model and Provider
system/developer policy revision
Host and Harness
Tool catalog and grants
exact vulnerable topology
attacker position and identities
attempt count and adaptation
actual transmitted inputs
native component observations
world outcome and independent verifier
```

## Chain graph

R4 uses these node types:

```text
A — indispensable affordance
T — structural tension
W — weakness or exposure class
V — concrete vulnerability or hazardous configuration
P — bounded exploit primitive
I — identity / role / trust authority
N — network / path / cache / interpreter amplification
C — Campaign action and adaptation
O — objective outcome
D — detection / containment
R — recovery / reconstruction
X — residual state or uncertainty
```

Important edge types:

```text
requires
enables
inherits
amplifies
bypasses
conceals
persists-through
propagates-to
invalidates
detects
contains
recovers
verifies
leaves-residual
```

## Counterfactual discipline

A defense is not credited merely because it is generally recommended. The case
must state where the defense cuts the graph:

```text
control K blocks edge V → P
control L narrows identity I
control M detects C after persistence
control N verifies O independently
control Q closes residual X
```

Controls can fail through:

- absence;
- misconfiguration;
- incomplete deployment;
- stale state;
- alternate path;
- privileged compromise;
- monitor blindness;
- operational friction causing bypass;
- attacker adaptation.

## No vulnerability monoculture

A vulnerability list omits:

- authority inherited after exploitation;
- why a public-facing component was strategically valuable;
- alternate paths after patching;
- cache and identity persistence;
- valid credentials and signed artifacts;
- human and Agent decision edges;
- recovery and residual state.

R4 therefore treats “patch the CVE” as one potential containment action, not
Campaign closure.

## Non-goals

R4 does not:

- teach exploitation;
- reproduce operational request strings;
- rank public targets;
- recommend intrusive scanning;
- infer malicious intent from one anomaly;
- claim every incident could have been prevented by one product;
- promote permanent controls without cost and deletion analysis;
- equate official absence of evidence with evidence of absence.
