# G0 Scope and Claim Boundaries

## 1. Research object

The object is **AI capability governance**: the institutions and technical
mechanisms that determine which actors may access which model capabilities,
under what identity, organization, product surface, retention mode, geography,
Tool authority, and appeal conditions.

The study covers six power dimensions:

1. **normative power** — defining constitutions, usage rules, risk classes,
   trusted-user criteria, and exceptions;
2. **observational power** — seeing prompts, outputs, sessions, Tool Calls,
   account history, identity, geography, and risk signals;
3. **enforcement power** — refusing, delaying, rewriting, degrading, limiting,
   suspending, banning, retaining, or reporting;
4. **adjudicative power** — deciding violation, trust, exemption, appeal, remedy,
   and reinstatement;
5. **infrastructural power** — controlling model weights, APIs, compute, cloud,
   identity, payment, distribution, or other unavoidable dependency points;
6. **epistemic power** — shaping which questions, explanations, evidence, and
   interpretive resources are available to which users.

## 2. Units of analysis

A company name is too coarse. The minimum case unit is:

```text
Provider
+ exact policy revision
+ model and model revision if available
+ product surface
+ account / organization class
+ access or verification tier
+ region
+ data-retention mode
+ Tool / action surface
+ observation date
```

The same model exposed through consumer chat, first-party API, enterprise tenant,
cloud marketplace, verified cyber program, or self-hosted weights may represent
materially different governance systems.

## 3. Questions excluded from G0-G2

G0-G2 does not:

- determine whether a named provider is malicious, corrupt, or politically
  captured;
- estimate policy false-positive or false-negative rates without denominators
  and controlled observations;
- treat one account report as representative of a population;
- infer hidden classifier logic from a single refusal;
- provide methods for bypassing provider safeguards, identity checks, regional
  controls, or account enforcement;
- equate open weights with absence of power or absence of externalities;
- decide a final normative constitution for Ordivon;
- create a universal safety, governance, or reputation platform.

## 4. Claim classes

Every material claim must declare one class.

### D — descriptive

What a source, policy, interface, experiment, or enforcement record says or does.

### C — causal

What mechanism produced an outcome. Causal claims require temporal ordering,
mechanism evidence, and a credible counterfactual or comparison.

### N — normative

What powers, restrictions, procedures, or distributions are justified. Normative
claims must name the protected interest, affected parties, alternatives,
proportionality standard, and burden allocation.

### A — architecture implication

What Ordivon should retain, localize, change, or reject. Architecture claims
require a reproduced engineering failure, not merely a political preference.

A valid descriptive claim does not automatically establish a causal, normative,
or architecture claim.

## 5. Non-equivalences

```text
published policy != actual implementation
classifier intervention != model judgment
model judgment != capability absence
no Tool Call != lower-layer Tool unavailability
no observed Effect != attack impossibility
appeal channel != meaningful contestability
transparency != power limitation
market alternatives != low-cost exit
open weights != decentralized compute or governance
state regulation != public accountability
provider self-regulation != illegitimacy by definition
```

## 6. Provisional working stance

The study begins with a falsifiable stance:

> Cognition access, Task authority, Tool authority, and external Effect authority
> should not be bundled by default in one Provider. Rich cognition and controlled
> owned-world experimentation should be maximized, while irreversible or
> third-party Effects should be constrained at identity, resource, Tool, and
> Effect boundaries.

This stance is provisional. It fails if content- or capability-level controls
consistently prevent serious harms that cannot be contained at narrower Effect
boundaries without unacceptable residual risk or cost.

## 7. Affected-party model

Every case must identify at least:

- the user or organization requesting capability;
- the Provider and infrastructure operators;
- directly affected third parties;
- communities carrying distributed or delayed externalities;
- regulators or states exercising delegated or direct authority;
- researchers and open-source ecosystems bearing innovation or access costs.

The requester is not the only rights-bearing or risk-bearing actor.

## 8. Research ethics and safety

Empirical work must use legal, owned, reversible, bounded resources. Provider
policies may be measured through ordinary authorized use, published interfaces,
and approved research programs. The study does not authorize evasion, account
fraud, unauthorized access, live third-party targeting, or concealment from
Provider enforcement.

Provider refusal and moderation remain valid observations. They must be recorded
without weakening the attacker or capability model and without attempting to
circumvent the Provider.

## 9. Admission and deletion rule

A concept enters shared Ordivon architecture only after:

1. a concrete failure appears in at least two materially different Providers,
   surfaces, or workloads;
2. the failure cannot remain in an adapter, Host application schema, or local
   experiment;
3. a stable owner and deletion test exist;
4. measured benefit exceeds permanent complexity and governance cost.

Otherwise it remains research-local or is deleted after closeout.
