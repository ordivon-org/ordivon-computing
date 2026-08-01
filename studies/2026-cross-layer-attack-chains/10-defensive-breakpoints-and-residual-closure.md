# 10 — Defensive Breakpoints, Evaluation, and Residual Closure

## No universal control cuts every case

The seven chains cross different mechanisms, but their defensive breakpoints can
be grouped by where they operate.

## Layer 1 — remove hazardous preconditions

- disable unused metadata services, federation, public administration, proxy
  routes, cacheability, browser sessions, or retry layers;
- reduce Internet-facing surface;
- separate management and data planes;
- remove broad network or cloud reach;
- isolate privileged content and Agent action identities.

Deletion is often stronger than adding another monitor.

## Layer 2 — block the concrete vulnerability

- patch Exchange and proxy vulnerabilities;
- enforce hardened metadata access;
- use strict HTTP parsing and canonical translation;
- validate service identity;
- align cache key with origin variation;
- separate external data from trusted instruction.

This prevents known paths but not already-established persistence.

## Layer 3 — narrow inherited authority

- least-privilege workload roles;
- exact storage resources and actions;
- separate Exchange/service administration identities;
- protected signing keys;
- transaction-specific authorization;
- Task-scoped Tool grants;
- stable idempotency scope;
- no implicit onward delegation.

This converts a successful primitive into a smaller consequence.

## Layer 4 — detect cross-layer contradiction

Important contradictions include:

```text
valid role + anomalous object access
valid login + Exchange server-management process chain
front proxy allows one request + backend executes another
DNS answer + invalid TLS identity
valid software signature + unexpected endpoint behavior
valid SAML signature + impossible issuance or actor context
benign user Task + unrelated Tool Effect
one semantic Effect + multiple provider objects
```

Detection should target relations, not isolated labels.

## Layer 5 — contain without assuming closure

Containment may include:

- disable exposed endpoint;
- revoke role or session;
- isolate body;
- remove route or DNS answer;
- purge cache;
- block Tool or Agent Binding;
- stop new retries;
- rotate signing key.

Each action cuts future edges. It does not prove past Effects are absent.

## Layer 6 — recover through reconstruction

When trust is systemic or evidence is weak:

- rebuild servers and bodies;
- restore from known-clean source;
- rotate credentials, certificates, and signing keys;
- recreate federation and application trust;
- reissue workload identity;
- regenerate Tools from reviewed source;
- rebuild caches and memories;
- restore independent monitors.

This follows Ordivon's high-recoverability principle: recreation can be cheaper
and more reliable than proving an opaque component clean.

## Layer 7 — residual proof

Residual closure asks whether any attack-derived capability or consequence
remains:

```text
copied data
Web Shell or malicious extension
credential or refresh Token
SAML signing capability
application service-principal credential
poisoned cache or browser state
Agent memory or generated Tool
queued job or callback
second provider object
external recipient or irreversible transaction
```

A Campaign is not closed until residuals are classified as removed, revoked,
recovered, accepted, or unknown.

## Evaluation integrity

NIST's work on Agent evaluation cheating shows that systems can exploit gaps
between the intended task and implemented scorer or affordances. [R25]

The same problem applies to cyber evaluations:

- scoring “request blocked” while another path succeeds;
- scoring “malware removed” while identity persistence remains;
- scoring “TLS valid” while endpoint is compromised;
- scoring “Tool not called” while external state was already changed;
- scoring “no retry” while proxy or SDK retried invisibly;
- scoring “cache purged” while browser or memory copies persist.

A valid evaluator needs independent world truth and hidden/held-out checks.

## Strong attacker evaluation

A later controlled range should vary:

- attacker knowledge of defenses;
- repeated attempts;
- alternate identity and network paths;
- legitimate versus malformed protocol use;
- body and Host replacement;
- model and safety-policy profile;
- generated Tool availability;
- cache, session, and memory persistence;
- monitor compromise;
- known and held-out chains.

Measure separately:

```text
detection
primitive prevention
objective prevention
false blocking
authorized utility
containment time
recovery cost
residual uncertainty
evaluator integrity
```

## Control cost discipline

A defense should be retained only when:

```text
expected prevented loss
>
latency + false blocking + operational burden + centralization + capability loss
```

High-impact irreversible Effects justify stronger independent checks. Reversible
local analysis should remain low-friction.

## Cross-case negative conclusions

R4 does not support:

- one universal policy engine;
- one global identity;
- one security database containing every native event;
- mandatory human approval for all Agent actions;
- blocking all server-side requests, proxies, caches, updates, federation, or
  retries;
- treating all valid credentials or signed artifacts as malicious;
- treating every anomaly as an attack.

## Strong positive conclusions

R4 supports:

- typed causal chains;
- component-native evidence;
- exact actor, identity, path, interpreter, and Effect relations;
- independent verification;
- adaptive and repeated evaluation;
- least authority at consequence boundaries;
- reconstruction after systemic compromise;
- explicit residual state and uncertainty.
