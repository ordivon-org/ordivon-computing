# 01 — Terminology and Levels

## Why vocabulary matters

Security discussions frequently use `bug`, `weakness`, `vulnerability`,
`exploit`, `attack`, and `risk` as interchangeable words. That is tolerable in
casual conversation but destructive for architecture. Each word points to a
different owner, evidence requirement, remediation path, and time horizon.

## Indispensable affordance

A useful system property whose wholesale removal would eliminate material
system value.

Examples include remote connectivity, dynamic content, persistent identity,
third-party composition, asynchronous execution, caching, encryption, and
machine-callable business operations.

An affordance is not a defect. It creates a design space with benefits and
structural tensions.

## Structural tension

A persistent trade-off or semantic conflict produced by useful properties.
Examples include compatibility versus strict parsing, delegation versus
least-ambient authority, caching versus freshness, privacy versus intermediate
visibility, or asynchronous recovery versus duplicate effects.

A tension can exist in a correctly implemented system. It becomes security
relevant when assumptions, controls, or compositions make an unintended path
available.

## Assumption and trust boundary

An assumption is a condition on which safe interpretation depends. A trust
boundary separates principals, components, data, identities, or authorities
whose claims cannot be accepted identically.

Examples:

- two HTTP recipients interpret framing identically;
- an authenticated request represents the current user's intent;
- a signed update was produced by an uncompromised build process;
- an external Tool result is data rather than an instruction;
- a retry will not duplicate a durable effect.

## Weakness

CWE describes a weakness as a condition in software, firmware, hardware, or a
service component that can contribute to a vulnerability. A weakness can be
abstract and may exist without being reachable or exploitable in one concrete
deployment. [R01]

Weakness is the right level for reasoning about recurring design and
implementation failure classes.

## Exposure or hazardous configuration

A deployment condition that makes a capability reachable, broadens authority,
removes a compensating control, or creates a useful attacker precondition.

An exposure can be security-relevant without being a software vulnerability:
public reachability, excessive credentials, unsafe egress, stale trust, a broad
browser session, or a permissive integration can connect otherwise separate
weaknesses.

## Vulnerability

A concrete condition in a particular product, protocol, configuration, or
system that enables a threat event or permits behavior outside the intended
control sphere. CWE's vulnerability theory emphasizes that one vulnerability
may arise from one or more related weaknesses. NIST similarly treats a
vulnerability as a condition or weakness that can be exploited or triggered.
[R02][R03]

A CVE record identifies a disclosed concrete vulnerability; it is not the whole
attack, risk, or incident.

## Exploit primitive

A bounded capability obtained by satisfying vulnerability and environment
preconditions.

Examples at a deliberately non-operational level:

- read one class of data;
- make a request with another component's network position;
- write a file in one scope;
- execute under one process identity;
- obtain or reuse one credential;
- alter one authorization decision;
- persist one state item;
- influence one Agent's instruction selection.

A primitive states capability, not strategic meaning. Remote code execution
under a low-value disposable identity and a weak information disclosure inside
a highly privileged control plane can have very different Campaign value.

## Weakness chain and composite

CWE defines a chain as a sequence in which one weakness creates conditions that
allow a later weakness to enter a vulnerable state. A composite requires
multiple weaknesses to coexist for the vulnerability to arise. Chains may be
longer than two elements and may branch. [R04]

These are causal software-weakness relations. They are not synonymous with a
complete adversary attack chain.

## Attack path and attack chain

An attack path is one feasible sequence through prerequisites, trust boundaries,
identities, vulnerabilities, primitives, and defenses toward an attacker
objective.

An attack chain is the realized or hypothesized composition of several such
steps. It may include non-vulnerability mechanisms:

- valid credentials;
- intended administration interfaces;
- social or business-process manipulation;
- network placement;
- supply-chain trust;
- response ambiguity;
- defender delay;
- Tool or Agent hijacking.

## Tactic, technique, and procedure

MITRE ATT&CK uses tactics for the adversary's reason for acting and techniques
or sub-techniques for how the adversary pursues that goal. Procedures describe
specific observed uses. ATT&CK is behavioral knowledge, not a mandatory linear
kill chain and not a causal software-weakness ontology. [R05][R06]

## Campaign

A Campaign is sustained adversarial work toward objectives across changing
world state. It may include:

```text
actor and objective
+ information and uncertainty
+ resources, identities, Tools, and paths
+ attack and defense actions
+ persistence and concealment
+ opponent response and adaptation
+ tactical, operational, and strategic outcomes
+ evidence, evaluator pressure, and residual state
```

One exploit can serve several Campaigns. One Campaign can continue after every
initial vulnerability is patched.

## Threat, threat event, and outcome

NIST defines a threat event as an event or situation with the potential to cause
undesirable consequences. A threat-event outcome is the effect produced when a
threat acts upon a vulnerability. [R07][R08]

This separates latent conditions from realized events and their consequences.

## Severity and risk

CVSS communicates vulnerability characteristics and severity. FIRST explicitly
states that the CVSS Base score measures severity, not deployment risk. Threat
and Environmental metrics are required to approach local prioritization. [R09]

Risk additionally depends on likelihood, exposure, threat activity, local
assets, controls, dependencies, and impact. NIST commonly describes risk as a
function of likelihood and adverse impact. [R10]

Therefore:

```text
high severity ≠ highest local risk
low-severity primitive ≠ low Campaign value
patched CVE ≠ closed incident
successful exploit ≠ achieved objective
```

## Control, mitigation, detection, recovery, and residual closure

- **control** — a mechanism intended to enforce or preserve a property;
- **mitigation** — an action or practice that reduces risk, likelihood, or
  impact; it need not eliminate the underlying weakness [R11];
- **detection** — evidence-driven admission that a condition or behavior may
  have occurred;
- **containment** — reduction of an actor's reachable options or consequences;
- **recovery** — restoration or replacement of required service and authority;
- **eradication** — removal or invalidation of attacker-controlled capability;
- **residual closure** — classification of remaining processes, identities,
  sessions, Tools, data, external objects, and uncertainty after an operation.

## World truth, observation, claim, belief, and fact

- **world truth** — the authoritative state of the relevant domain;
- **observation** — evidence produced through a declared method at a declared
  time and scope;
- **claim** — a proposition supported or asserted by one source;
- **belief** — an actor's uncertain model of world or opponent state;
- **fact** — a claim admitted by the responsible authority under a declared
  evidence method.

These distinctions become mandatory under intelligent opposition because an
observation may be incomplete, manipulated, strategically selected, stale, or
correct but misleading about intent.
