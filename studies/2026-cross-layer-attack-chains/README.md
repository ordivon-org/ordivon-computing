# Real Cross-Layer Defect, Vulnerability, and Attack Chains

Status: R4 foundational case study completed

## Purpose

R4 applies the R0–R3 grammar to real incidents, official vulnerability records,
and controlled Agent evaluations. It asks a harder question than “what CVE was
used?”:

> Which necessary capability, weakness, concrete vulnerability, identity,
> network path, interpreter, trusted component, and recovery failure had to join
> before a bounded primitive became an operational or strategic outcome?

The study reconstructs seven chain families:

1. Capital One cloud intrusion — exposed Web intermediary, cloud-role authority,
   object-storage access, detection, and governance failure;
2. Microsoft Exchange exploitation — authenticated entry, chained SSRF/RCE,
   Web Shell persistence, Active Directory reconnaissance, and exfiltration;
3. Apache HTTP request splitting/smuggling — rewrite/proxy composition,
   front/back semantic disagreement, access-control bypass, unintended routing,
   and cache poisoning potential;
4. MyEtherWallet 2018 — BGP route manipulation, resolver poisoning, invalid TLS
   identity, human override, credential theft, and legitimate-site transaction;
5. SolarWinds/Solorigate — trusted software distribution, endpoint foothold,
   privilege escalation, signing-key compromise, valid SAML impersonation,
   cloud access, and systemic recovery;
6. Agent hijacking — untrusted external data, probabilistic instruction
   confusion, legitimate Tool and identity, repeated adaptive attempts, and
   world Effects;
7. timeout/retry duplication — communication ambiguity, multiple retry layers,
   absent stable Effect identity, duplicate commit, and residual state.

## Adversarial stance

R4 assumes an adaptive opponent who:

- can combine vulnerabilities, valid accounts, trusted infrastructure,
  misconfiguration, identity, network position, legitimate APIs, and human or
  Agent decision failures;
- selects paths after observing defenses;
- retries cheaply and coordinates multiple actors or bodies;
- uses validly signed software, valid TLS channels, valid Tokens, valid cloud
  roles, and ordinary administrator tools whenever those provide more leverage
  than malformed input;
- attacks monitors, evaluators, recovery workflows, and residual credentials;
- may construct Tools or direct protocol clients that do not share one model or
  Host's safety behavior.

Model, Provider, Host, system-prompt, policy, and Tool-broker refusals are
recorded as configured-system evidence. They are not used to weaken the attacker
model or infer that lower-layer primitives are absent. Generated descriptions
are also not treated as proof of exploitability.

R4 contains no exploit payloads, commands, target procedures, scanning guidance,
credential acquisition instructions, persistence code, or methods for bypassing
platform policy. Official records that contain operational details are abstracted
to causal relations.

## Central result

A real attack chain should be represented as a typed causal graph:

```text
necessary affordance
→ structural tension
→ weakness or exposure
→ concrete vulnerability / hazardous configuration
→ bounded primitive
→ identity and network amplification
→ persistence and adaptation
→ objective outcome
→ detection and containment
→ recovery and residual proof
```

A CVE usually names one edge. It rarely describes the complete Campaign.

## Study structure

1. [`00-method-evidence-and-policy-confounds.md`](00-method-evidence-and-policy-confounds.md)
   — chain method, evidence grading, attacker assumptions, and Host confounds;
2. [`01-cross-case-grammar-and-comparison.md`](01-cross-case-grammar-and-comparison.md)
   — normalized graph, comparison matrix, and recurring failure structures;
3. [`02-capital-one-cloud-authority-chain.md`](02-capital-one-cloud-authority-chain.md)
   — Web intermediary to cloud-role and storage authority;
4. [`03-exchange-vulnerability-to-organization-chain.md`](03-exchange-vulnerability-to-organization-chain.md)
   — Exchange SSRF/RCE, Web Shell, directory, and exfiltration chain;
5. [`04-request-smuggling-proxy-cache-chain.md`](04-request-smuggling-proxy-cache-chain.md)
   — semantic disagreement across rewrite, proxy, backend, access control, and
   cache;
6. [`05-bgp-dns-tls-human-chain.md`](05-bgp-dns-tls-human-chain.md) — routing,
   resolver, TLS identity, human override, credential, and transaction chain;
7. [`06-solarwinds-trusted-update-identity-chain.md`](06-solarwinds-trusted-update-identity-chain.md)
   — supply-chain trust, identity-signing compromise, cloud impersonation, and
   systemic recovery;
8. [`07-cache-poisoning-persistence-chain.md`](07-cache-poisoning-persistence-chain.md)
   — unkeyed input, shared cache, active interpretation, persistence, and Agent
   memory analogy;
9. [`08-agent-hijacking-tool-identity-chain.md`](08-agent-hijacking-tool-identity-chain.md)
   — external-data instruction confusion and legitimate authority;
10. [`09-timeout-retry-duplicate-effect-chain.md`](09-timeout-retry-duplicate-effect-chain.md)
    — non-CVE distributed failure chain and exactly-once limits;
11. [`10-defensive-breakpoints-and-residual-closure.md`](10-defensive-breakpoints-and-residual-closure.md)
    — cross-case cuts, detection, recovery, and falsifiers;
12. [`11-ordivon-insertion-and-r5-gate.md`](11-ordivon-insertion-and-r5-gate.md)
    — narrow architecture feedback and next route;
13. [`REFERENCES.md`](REFERENCES.md) — official-source ledger.

## Durable learning rule

For each incident or vulnerability ask:

```text
what indispensable capability existed before the defect?
which trust or compatibility assumption failed?
what exact condition produced the first primitive?
which identity, role, route, cache, or interpreter amplified it?
which valid mechanisms did the attacker inherit?
what did each observer actually know?
which actions were persistent or replayable?
which defenses were bypassed versus absent?
what evidence established the real objective outcome?
what had to be rotated, rebuilt, invalidated, purged, or independently verified?
what remains uncertain?
```

## R4 disposition

R4 validates a cross-layer review method. It does not justify a universal
security graph database, scanner, SIEM, WAF, identity broker, network controller,
Agent policy engine, or incident-response platform. Native component evidence
remains authoritative. Shared Ordivon responsibilities require reproduced
unowned failure, a second consumer, measurable net benefit, and a deletion test.
