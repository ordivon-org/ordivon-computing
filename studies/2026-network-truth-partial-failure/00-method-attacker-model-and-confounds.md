# 00 — Method, Attacker Model, and Confounds

## Research question

How should Ordivon reason about highly capable network attackers and defenders
without granting network evidence more authority than the protocols actually
provide, and without mistaking one model or Host policy for a universal security
boundary?

## Strong bounded attacker

The attacker may hold one or more positions:

### Off-path attacker

Can send traffic but cannot directly observe the victim flow. May exploit weak
transaction entropy, reflection, amplification, exposed services, or predictable
state.

### On-path attacker

Can observe, delay, drop, duplicate, reorder, and modify traffic not protected
against that position. Can interfere with protected traffic even when unable to
forge valid ciphertext.

### Naming attacker

Controls a zone, registrar path, authoritative server, recursive resolver, local
configuration, or poisoned cache under the case assumptions.

### Routing attacker

Controls or compromises one autonomous system, router, route policy, or peering
relationship; can originate, leak, suppress, or prefer routes within that
position.

### Endpoint attacker

Controls a server, proxy, VPN exit, relay, browser, client, or cloud workload
that legitimately terminates one channel.

### Identity attacker

Possesses or controls one certificate key, Token, workload credential, account,
or delegated identity through a separately demonstrated chain.

### Agent attacker

Can synthesize measurement clients and adapters, compare paths, retry cheaply,
coordinate multiple vantage points, exploit protocol-valid behavior, and adapt
to defensive feedback.

### Evaluator attacker

Can exploit gaps between visible network signals and the objective actually
measured.

The attacker is not assumed to break current cryptography without key access,
forge DNSSEC or certificate signatures under uncompromised trust roots, or alter
an independently isolated evidence store without a path.

## Network positions are composable

Real attacks often join positions:

```text
route manipulation
+ valid certificate or compromised endpoint
→ encrypted traffic delivered to attacker-controlled service
```

or:

```text
DNS cache poisoning
+ broad TLS trust or missing identity verification
→ successful connection to wrong endpoint
```

One position alone may be insufficient. The chain must state every required
identity, route, cache, and endpoint condition.

## Model and Host safety confounds

A model, Provider, Host, Harness, system prompt, policy layer, or Tool broker may
refuse to describe, construct, or execute one network action. That behavior is a
real property of the configured Agent system, but it cannot establish that:

- the protocol primitive is impossible;
- another model, direct client, generated Tool, compromised body, or malicious
  workload lacks the capability;
- the target network path is protected;
- the endpoint did not receive traffic through another channel;
- an on-path or control-plane actor is absent;
- the final world Effect was prevented.

Conversely, a model claiming that it discovered a route, bypassed a firewall, or
completed an Effect is not authoritative evidence.

Later experiments must separately record:

```text
hypothesis and plan
policy refusal or transformation
Tool proposal and admission
actual process and socket creation
DNS, route, path, transport, and TLS observations
request and response
provider-native Receipt
world Effect
independent verification
```

## Measurement confounds

### Vantage point

DNS, BGP, latency, reachability, and path observations vary by resolver, network,
region, time, interface, and policy.

### Cache

A response can originate from a local stub, recursive resolver, CDN, proxy,
browser, application cache, or Agent memory.

### Anycast and load balancing

One address or name can route to different physical or logical service instances.
A repeated observation need not reach the same body.

### Middleboxes

NAT, firewall, proxy, VPN, TLS terminator, load balancer, service mesh, and cloud
edge can transform addressing, transport, encryption, and evidence.

### Fallback

Applications may race IPv4/IPv6, fall back from QUIC to TCP, use alternate
resolvers, change proxy or VPN, retry another region, or accept downgraded
features. Success may therefore occur through a path different from the path
under test.

### Observer effect

Active measurement can create state, warm caches, trigger rate limits, change
route selection, or reveal defensive policy.

## Evidence levels

- **N0 — standard property:** the protocol specification establishes a semantic
  or security limit;
- **N1 — one-vantage observation:** one exact observer reports current state;
- **N2 — corroborated path fact:** independent observers or endpoint evidence
  bind a path or identity relation;
- **N3 — bounded primitive:** a controlled experiment demonstrates influence over
  naming, routing, delivery, replay, or endpoint selection;
- **N4 — objective consequence:** independent domain evidence confirms the
  intended Campaign or defensive outcome;
- **N5 — adaptive transfer:** the result survives held-out paths, providers,
  versions, and opponent policies.

R3 is primarily N0 research. It does not claim N3–N5 Ordivon evidence.

## Safety and execution boundary

R3 may explain:

- protocol guarantees and omissions;
- attacker positions;
- causal network and consequence chains;
- defensive graph cuts;
- evidence requirements;
- controlled-range experiment design.

R3 does not provide:

- instructions for route announcements, DNS poisoning, packet injection,
  interception, amplification, credential capture, or bypass;
- public-target scanning or traffic generation;
- methods for defeating provider or Host policy;
- malicious proxy, VPN, or relay deployment procedures.

## Source hierarchy

1. current IETF Standards, BCPs, and official protocol guidance;
2. official routing, resolver, browser, and identity specifications;
3. official government or vendor incident evidence;
4. mature measurement systems with explicit vantage and methodology;
5. later Ordivon owned-range evidence.

## Falsifiers

Revise or delete the R3 model if:

- its claim ladder cannot classify major network failures;
- native standards and component evidence already provide every needed relation;
- path and Effect evidence can safely be collapsed in realistic workloads;
- Agent additions merely rename ordinary automation without changing evaluation;
- a proposed shared World abstraction becomes a copy of network telemetry;
- recurring collection cost exceeds decision, recovery, or attribution value.
