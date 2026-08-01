# 04 — Request Smuggling: Proxy, Rewrite, Backend, and Cache

## Evidence boundary

Apache's official vulnerability record for CVE-2023-25690 states that some
`mod_proxy` configurations combined with rewrite rules could allow HTTP request
splitting/smuggling when user-controlled request-target data was reinserted into
a proxied target. Potential consequences included proxy access-control bypass,
proxying unintended URLs to existing origin servers, and cache poisoning. [R09]

Apache has also fixed several other request-smuggling conditions caused by
inconsistent request interpretation or connection handling, demonstrating that
this is a recurring cross-component class rather than one payload. [R09]

RFC 9112 defines strict HTTP/1.1 framing and explains that request smuggling
exploits differences among recipients to hide another request. [R10]

## Causal graph

```text
A1 reverse proxy and rewrite capability
→ T1 public and internal URL spaces must be translated
→ W1 user-controlled target fragment enters rewrite substitution
→ V1 generated proxied request has ambiguous or injected message structure
→ P1 front proxy and backend consume different request boundaries or targets
→ I1 attacker inherits proxy connection and backend reachability
→ N1 backend sees request not admitted by front policy
→ N2 shared cache may associate response with wrong request/key
→ O1 access-control bypass, unintended backend action, or cache poisoning
→ D1 front/backend trace contradiction
→ R1 patch and remove hazardous rewrite composition
→ X1 poisoned cache, alternate proxies, stale config, backend side effects
```

## Why the proxy matters

A reverse proxy often has more reach than an external client:

- internal backend connectivity;
- trusted source identity;
- normalized Host and path;
- authentication metadata;
- persistent backend connections;
- shared cache participation;
- routing to administrative or non-public endpoints.

The smuggled request inherits those conditions.

## Rewrite as a compiler boundary

A rewrite rule is effectively a small compiler:

```text
external request target
→ pattern capture
→ string substitution
→ generated backend request target
→ new HTTP serialization
```

Security fails when captured data that was previously a URL component becomes
HTTP structure or another target after substitution.

This is R2's transformation-order differential:

```text
policy validates source representation
→ rewrite creates a more powerful representation
→ backend executes generated meaning
```

## Framing and routing can combine

Request smuggling is often described only as message-length disagreement. The
Apache case shows another form: request-target data and rewrite/proxy composition
can split or redirect generated backend traffic.

The relevant differential may involve:

- request boundary;
- request target;
- Host/authority;
- backend connection reuse;
- front access policy versus backend route;
- cache key versus origin-selected response.

## Cache amplification

A primitive affecting one backend request can become persistent and multi-user if
a shared cache stores the resulting response under a broader clean key.

```text
attacker-controlled backend interpretation
→ origin emits response
→ cache associates it with victim-visible key
→ later unrelated requests receive stored response
```

The cache is not necessarily vulnerable in isolation. It trusts the request and
response relation produced by the proxy chain.

## Detection graph

Useful evidence includes:

- raw or digest-bound front request;
- front proxy parsed target and request count;
- generated backend request target and serialization;
- backend request count and route;
- connection reuse and request ordering;
- front policy decision;
- backend application action;
- cache key, variant, age, and response source;
- mismatched request IDs or impossible backend routes.

A single front access log can omit the request actually executed downstream.

## Defensive breakpoints

### B1 — update vulnerable proxy implementations

Removes known serialization and connection-handling defects.

### B2 — avoid inserting unconstrained captures into proxy targets

Use typed routing parameters and explicit allowlisted destinations.

### B3 — parse once, reserialize canonically

Do not forward partially parsed request text across trust boundaries.

### B4 — reject ambiguous framing and prohibited characters

Close connections after framing errors rather than attempting divergent repair.

### B5 — align front and backend parser behavior

Use conformance and differential tests across exact versions and translation
paths.

### B6 — narrow backend reach

The proxy should connect only to required services and paths; backend should not
trust proxy location as sufficient authorization.

### B7 — cache carefully

Ensure the cache key covers response-selecting input and purge affected entries
after incidents.

## Recovery and residual closure

Patching the proxy does not automatically reverse:

- backend state changes;
- poisoned cache entries;
- leaked responses;
- created sessions or objects;
- alternate vulnerable rewrite rules;
- other intermediaries with different parser behavior.

Closure requires cache purge, backend audit, configuration inventory, regression
corpus, and verification across each front/back pair.

## Ordivon lesson

Runtime can host controlled differential tests. World/provider modules can expose
front, backend, cache, and Effect observations. Security owns the attack graph.
Host owns the intended resource and Effect. Ordivon should not add a universal
HTTP normalizer or WAF.
