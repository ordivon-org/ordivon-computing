# 01 — Cross-Case Grammar and Comparison

## Normalized causal path

Across the cases, the recurring path is:

```text
useful exposed capability
→ coarse trust or compatibility assumption
→ one concrete weakness or vulnerability
→ limited primitive
→ inherited legitimate authority
→ cross-layer composition
→ persistence or audience expansion
→ objective outcome
→ incomplete local remediation risk
```

The decisive transition is often not `Vulnerability → Code Execution`. It is:

```text
Primitive
→ inherited identity, trust, route, cache, or Tool authority
```

## Case matrix

| Case | First primitive | Main inherited authority | Amplifier | Objective | Residual risk |
|---|---|---|---|---|---|
| Capital One | commands reached cloud-facing server / role credentials obtained | cloud WAF role permissions | object-storage API and broad accessible buckets | data access and extraction | role policy, copied data, similar accounts |
| Exchange | SSRF/RCE chain on Internet-facing server | Exchange/IIS process and administrative environment | Web Shell, PowerShell, AD visibility | recon and exfiltration | Web Shells, credentials, scheduled services |
| Apache proxy | request boundary/target disagreement | proxy connection and backend reachability | rewrite substitution, backend routing, shared cache | access-control bypass or poisoning | poisoned cache, alternate routes, version drift |
| MyEtherWallet | traffic/resolver redirection | user browser session and credentials after TLS override | poisoned recursive DNS and legitimate target reuse | credential theft and asset transfer | stolen credentials, resolver cache, user trust |
| SolarWinds | trusted update executes malicious code | signed software distribution and network foothold | privileged credentials and SAML signing key | cloud impersonation, exfiltration, persistence | forged-token trust, app credentials, unknown scope |
| Agent hijacking | external data changes action selection | legitimate Tool, browser, Token, and user authority | retries, adaptation, generated Tools, memory | unintended world Effects | memory, sent messages, Tokens, generated Tools |
| Retry duplication | response/commit ambiguity | valid client authorization | multiple retry layers and alternate paths | duplicate durable Effect | partial jobs, callbacks, billing, external objects |

## Recurring structures

### 1. Trusted intermediary as deputy

WAFs, proxies, Exchange front ends, CDNs, identity providers, Agent Hosts, and
service meshes act for other participants. A failure in request selection or
interpretation lets an attacker borrow the intermediary's reach or identity.

### 2. Valid mechanisms after initial compromise

Later steps often use mechanisms exactly as designed:

- cloud APIs accept a valid role;
- Exchange admin tools execute under an authorized service context;
- caches reuse a response under their configured key;
- browsers attach valid session state;
- SAML relying parties accept a correctly signed assertion;
- Tools execute with valid grants;
- retry libraries resend authorized requests.

The system can be locally correct and globally wrong.

### 3. Identity wider than the initiating purpose

A server role, certificate, user session, service principal, Tool grant, or
application identity often authorizes more than the narrow operation that led to
its use.

### 4. Persistence moves outside the patched component

After initial access, persistence may live in:

- Web Shells;
- copied data;
- cloud roles and Tokens;
- SAML signing keys;
- application credentials;
- cache entries;
- Agent memory;
- generated Tools;
- queued jobs and callbacks.

### 5. Observer mismatch

The relevant truth may be split among:

- edge and origin logs;
- client and server;
- route collector and affected resolver;
- endpoint and cloud identity;
- model transcript and deterministic Tool trace;
- response and external object state.

### 6. Compatibility and acceleration create attack surface

Features exist for valid reasons:

- reverse proxying;
- automatic cloud credentials;
- trusted software updates;
- federation;
- shared caching;
- transparent browser sessions;
- Agent Tool use;
- retries after transient failure.

The goal is not to delete all capability, but to narrow authority and make
consequence independently visible.

## Primitive versus outcome

```text
SSRF-like server-side request
≠ cloud data theft

request smuggling
≠ administrative compromise

route hijack
≠ credential theft

valid forged SAML token
≠ complete cloud Campaign

prompt injection success
≠ irreversible world damage

timeout
≠ duplicate Effect
```

Each outcome requires additional edges.

## Defensive layers

### Precondition reduction

- reduce exposed administrative surfaces;
- remove broad public routing and proxy rules;
- require current hardened metadata protocols;
- isolate privileged origins and identities;
- disable unused federation and retry paths.

### Primitive blocking

- patch concrete vulnerabilities;
- use strict parsers and translation;
- validate endpoint identity;
- separate data from instruction;
- reject replay-unsafe early actions.

### Authority narrowing

- least-privilege roles;
- resource/action-specific Tokens;
- separate administration identities;
- short-lived credentials;
- narrow Tool grants;
- per-Effect idempotency.

### Detection and contradiction

- correlate front/backend process and request traces;
- detect unusual role/API use;
- compare route, DNS, TLS, and endpoint identity;
- inspect signed-token behavior, not only signature validity;
- compare Agent transcript, Tool call, and World outcome.

### Recovery and residual closure

- rotate credentials and signing keys;
- rebuild compromised bodies;
- remove persistence;
- purge caches and memories;
- revoke sessions and delegated Tokens;
- inventory copied data and external objects;
- verify no alternate path remains.

## Architectural conclusion

The recurring cross-layer invariant is not a universal “security object.” It is a
review discipline:

```text
never promote one component's successful local check
into a broader claim than that component owns
```

Ordivon already has the right foundations: component-native evidence, explicit
Effect, `UNKNOWN`, independent verification, thin ownership, and deletion tests.
R4 determines where those principles matter in adversarial chains.
