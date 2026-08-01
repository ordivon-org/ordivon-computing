# 10 — Agent Path Discovery, Switching, and Defense

## What Agents amplify

Network measurement, failover, traffic engineering, routing analysis, and
incident response already exist. Agents change their cost and integration.

An Agent can:

- read protocol standards and provider documentation;
- inspect local interfaces, route tables, resolver configuration, proxy state,
  certificates, and application receipts;
- construct measurement clients and adapters;
- compare DNS, BGP, path, transport, TLS, and application observations;
- deploy multiple authorized vantage points;
- infer hidden middleboxes and fallback paths;
- switch resolver, address family, region, provider, protocol, VPN, proxy, or
  body;
- retry and update beliefs after each observation;
- coordinate Red and Blue roles;
- attack or defend evaluators and monitors.

## Safety-profile confound

NIST's 2026 Agent-security synthesis concludes that classical cybersecurity
remains relevant but requires adaptation for Agent systems, while NIST's
hijacking evaluations show that adaptive and repeated attacks can materially
change measured outcomes. These sources justify complete-system evaluation but
do not establish one universal Agent network-control layer. [R35][R36]

A model or Host may refuse network enumeration, route manipulation, interception,
or Tool creation. That refusal is recorded as configured behavior. It cannot be
used as proof that a malicious Agent or lower-level client lacks the capability.

Likewise, a model claiming “VPN is active,” “TLS is secure,” or “request
completed” is not network or World evidence.

## Agent path-selection objective

A path selector should not optimize latency alone. One Task can require:

```text
service identity
confidentiality
allowed jurisdictions or providers
VPN or private network
address family
resolver and DNSSEC policy
maximum latency and cost
callback reachability
observability
recovery and fallback rules
```

The selector proposes a path; native components and Host policy admit it.

## Adaptive attack graph

```text
observe defender path checks
→ degrade or deceive one layer
→ cause Agent to switch path
→ exploit weaker fallback identity, monitoring, or authorization
→ preserve objective while avoiding blocked edge
```

Examples at a conceptual level:

- poison one resolver view to force an alternate endpoint;
- leak a route only in the user's provider region;
- block UDP to force QUIC fallback;
- degrade IPv6 to force an unmonitored IPv4 path;
- preserve TLS identity but compromise the legitimate endpoint;
- delay responses after commit to induce retries;
- present healthy outer-tunnel telemetry while inner path changes;
- manipulate a route collector or evaluator rather than the data plane.

## Defensive Agent graph

A Blue Agent can:

```text
inventory paths and trust boundaries
→ collect conditioned observations
→ compare control and data planes
→ identify contradiction
→ narrow or switch capability
→ verify service identity
→ reconcile Effects
→ rotate or rebuild compromised components
→ verify residual closure
```

## Multi-vantage reasoning

One Agent can compare:

- local resolver versus validating public resolver;
- user network versus cloud vantage;
- route collector versus active data-plane path;
- IPv4 versus IPv6;
- QUIC versus TCP fallback;
- VPN versus direct route;
- client trace versus provider Receipt;
- endpoint body versus external object state.

Disagreement is evidence to investigate, not automatic proof of attack.

## Deception and moving target

Defenders may use decoy endpoints, synthetic records, canary Tokens, shadow
services, address rotation, or hidden verification paths. These can expose
adversary behavior but also create operational and evaluator complexity.

Security should own the strategic interpretation of deception. World components
should expose native facts without labeling every anomaly malicious.

## Tool construction

An Agent may build:

- resolver and DNSSEC comparison tools;
- route-view adapters;
- transport probes;
- TLS identity inspectors;
- QUIC/TCP path comparators;
- provider-state reconcilers;
- callback verifiers;
- topology and evidence visualizers.

Generated Tools remain candidate Artifacts. Build them in disposable,
credential-empty environments and grant only declared targets, paths, and
resources after admission.

## Evaluation family

A future owned experiment should vary:

```text
attacker position
vantage point
resolver and cache state
route and RPKI state
IPv4 / IPv6
NAT / VPN / proxy
TCP / QUIC
TLS identity and terminator
0-RTT and resumption
loss, delay, duplication, and reset
timeout and retry policy
model and Host policy profile
known and held-out path changes
```

Measure separately:

- detection;
- correct diagnosis;
- authorized utility;
- path-security preservation;
- false positives;
- retry cost;
- containment;
- recovery;
- residual state;
- evaluator integrity.

## Defensive graph cuts

### Narrow path requirements

Bind the Task to required service identity, provider, network, region, and
fallback properties only where consequence justifies them.

### Independent observations

Use separate data sources for route, endpoint, and Effect verification.

### Preserve native identity

Do not authorize by IP or route alone when workload or application identity is
available.

### Make fallback explicit

A fallback is a new Binding with its own evidence and authorization.

### Bound retries

Use stable Effect identity, `UNKNOWN`, reconciliation, backoff, and total budgets.

### Separate management and data planes

The Agent being evaluated should not control all route policy, monitor state,
scoring, and evidence.

### Recover by reconstruction

When path, proxy, resolver, body, or credential trust is lost, rebuilding and
rotating can be cheaper and more reliable than proving every component clean.

## Extreme attacker does not imply maximum permanent control

A strong adversary model supports powerful analysis. It does not justify an
always-on central blocker. Permanent controls must still satisfy A11:

```text
prevented expected loss
>
latency + false blocking + maintenance + centralization + lost capability
```

## Ordivon implication

World can expose available and observed path facts. Host chooses a Binding based
on Task requirements. Security models opponent and deception. Runtime executes
local Tools. Game can provide hidden path truth and controlled adversarial
variation. No universal path-optimization Agent is admitted by R3.
