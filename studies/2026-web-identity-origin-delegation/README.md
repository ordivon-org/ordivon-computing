# Web Identity, Origin, Delegation, and Ambient Authority

Status: R1 foundational study completed

## Purpose

R1 studies how modern Web systems convert names, browser state, identities,
credentials, delegation, and user interaction into authority over external
resources. The central question is:

> How does a participant's intent become a browser or Agent action, and where can
> another actor redirect, inherit, replay, widen, or confuse that authority?

This is not a Cookie, CORS, or OAuth tutorial. It is a causal and adversarial
study of the complete authority path:

```text
participant intent
→ browser or Agent context
→ origin, site, and top-level context
→ authenticated session or delegated token
→ concrete resource and action
→ request execution
→ server authorization
→ world consequence
→ evidence, revocation, and residual state
```

## Adversarial stance

The study assumes a strong adaptive opponent that can:

- operate arbitrary Web origins, clients, authorization servers, resource
  servers, browser sessions, and network endpoints;
- lure users or Agents to attacker-chosen content and URIs;
- possess valid low-privilege accounts and participate honestly in protocols
  until deviation is useful;
- exploit same-origin compromise, supply-chain compromise, browser extension or
  renderer compromise, token leakage, redirect confusion, and weak delegation;
- repeat attempts, compare system behavior, construct Tools, coordinate multiple
  actors, and adapt after defenses are exposed;
- use legitimate browser, identity, API, and Agent affordances rather than rely
  only on malformed input.

The model does not assume that strong cryptography can be broken without key
access or implementation failure, and it does not grant control of an
independent management or evidence plane without a demonstrated path.

R1 separates the strength of the attacker model from permission to act. It
contains no exploit code, payloads, target procedures, token theft instructions,
or live-system testing. Later executable work requires an independently admitted
owned range.

## Central result

Origin, authentication, authorization, delegation, and user intent are distinct
relations:

```text
Origin
  which Web principal or protection domain produced the request

Authentication
  which participant or workload proved control of an identity

Authorization
  which action on which resource is allowed under current policy

Delegation
  which actor is acting for which participant, with what retained identity

Intent
  which concrete consequence the participant actually chose
```

A system can be correct at four of these layers and still fail at the fifth.
Examples include:

- a cross-site request with a valid ambient session but no current user intent;
- a correctly authenticated Agent using a token broader than its Task;
- a valid delegated token whose actor chain is lost in downstream logs;
- a same-origin script that is authorized by the browser but compromised by the
  site's supply chain;
- a successful passkey ceremony followed by an overbroad session or API token;
- a Tool call initiated from malicious external content using legitimate user
  identity.

## Study structure

1. [`00-method-and-attacker-model.md`](00-method-and-attacker-model.md) — strong
   attacker assumptions, evaluation confounds, evidence, and scope;
2. [`01-url-origin-site-and-principal.md`](01-url-origin-site-and-principal.md) —
   URL, origin, site, DNS, TLS, and protection-domain semantics;
3. [`02-browser-authority-and-isolation.md`](02-browser-authority-and-isolation.md)
   — same-origin policy, cross-origin communication, process isolation, and
   browser authority;
4. [`03-cookies-sessions-and-ambient-authority.md`](03-cookies-sessions-and-ambient-authority.md)
   — HTTP state, Cookie scope, sessions, SameSite, and confused deputy;
5. [`04-cross-origin-requests-csrf-and-cors.md`](04-cross-origin-requests-csrf-and-cors.md)
   — request creation versus response readability, CSRF, CORS, Fetch Metadata,
   and request-context evidence;
6. [`05-oauth-delegation-and-token-chains.md`](05-oauth-delegation-and-token-chains.md)
   — OAuth attacker models, redirect binding, token restriction, delegation,
   impersonation, and proof of possession;
7. [`06-workload-agent-and-generated-tool-identity.md`](06-workload-agent-and-generated-tool-identity.md)
   — non-human identity, workload attestation, Agent identity, generated Tools,
   and authority continuity;
8. [`07-agent-era-attack-and-defense-chains.md`](07-agent-era-attack-and-defense-chains.md)
   — maximal Agent attack paths and corresponding defensive graph cuts;
9. [`08-ordivon-insertion-and-r2-gate.md`](08-ordivon-insertion-and-r2-gate.md) —
   Host, World, Runtime, Security, and Game responsibilities plus the R2 route;
10. [`REFERENCES.md`](REFERENCES.md) — primary standards and official sources.

## Durable learning rule

For every identity mechanism ask:

```text
who is the principal?
what names or binds the principal?
what proves identity now?
what exact resource and action are authorized?
who delegated to whom?
what browser, path, body, and Tool conditions apply?
what event represents current participant intent?
what evidence survives redirects, retries, and handoffs?
how is authority narrowed, revoked, expired, and proven absent?
what residual authority remains after the Task or Campaign closes?
```

## R1 disposition

R1 changes Ordivon's knowledge and architecture tests. It does not promote a
universal identity service, policy engine, browser broker, token format, or
World database. Mature browser, OAuth, WebAuthn, workload-identity, and
cryptographic mechanisms remain inherited. New Ordivon responsibilities require
a reproduced cross-layer failure and a deletion test.
