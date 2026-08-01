# 06 — Cache Keys, Variants, and Persistence

## Caching changes time and audience

HTTP caching reuses earlier responses to reduce latency and bandwidth. RFC 9111
states that proper cache operation preserves HTTP semantics while avoiding
transmission, and that the cache key includes at least method and target URI.
[R10]

A cache is therefore an interpreter of equivalence:

> Which later request is equivalent enough to receive this stored response?

Security failure occurs when the cache's equivalence relation is broader than
the origin application's response-selection or authorization relation.

## Cache key differential

```text
origin response depends on input X
but
cache key omits X
→ response selected for one context reused in another
```

X might be:

- a request field;
- Cookie or authorization state;
- query parameter;
- content negotiation value;
- tenant, region, or route metadata;
- transformed URL;
- method or request body in a nonstandard cache;
- Agent or Tool identity;
- application state hidden from the HTTP cache.

## `Vary` and secondary keys

HTTP uses `Vary` to identify request fields that influenced response selection.
Applications must emit it consistently on all relevant variants. RFC 9205 warns
that request fields affecting content must be reflected in caching behavior or
the response should not be shared. [R17]

`Vary` does not automatically include application state invisible to the cache,
and it does not repair a parser differential between cache and origin.

## Shared and private caches

Shared caches affect multiple users; private caches retain one user's responses.
Both have security implications:

- shared cache poisoning amplifies one request to many users;
- private cache state can reveal history;
- cached sensitive responses can survive apparent logout or deletion;
- stale responses can revive revoked configuration or authorization assumptions.

RFC 9111 notes that cache contents persist after the original request and should
be protected as sensitive information. [R10]

## Cache poisoning

RFC 9111 identifies parsing differences between proxies and user agents as a
common cache-poisoning vector. [R10]

The generic chain is:

```text
attacker controls request representation
→ cache and origin identify request or response differently
→ origin produces attacker-influenced response
→ cache associates response with broader or different key
→ later victims receive stored response
```

The primitive is persistence and audience expansion, not necessarily direct code
execution.

## Unkeyed input

A request value may influence origin output without entering the cache key. If an
attacker can control that value and make the response cacheable, the resulting
content can be served to requests that do not contain the attacker's value.

This can involve intended application metadata, routing fields, forwarded
headers, content negotiation, or parser differences. The safe analysis is based
on actual response dependency and actual cache key, not a generic list of
“dangerous headers.”

## Cache deception and resource classification

A cache, framework, and application can disagree whether a request names a
static public resource or a personalized dynamic resource. Path suffixes,
rewrites, normalization, and route fallbacks can make one layer cache a response
that another layer generated from authenticated state.

## Staleness and revocation

HTTP permits controlled reuse of stale responses in some conditions. Application
validity and HTTP freshness are separate concepts. RFC 9205 requires applications
with separate validity periods to define their relationship to cache age.
[R17]

A cached authorization document, discovery endpoint, Tool manifest, policy,
model configuration, or identity metadata can remain fresh under HTTP rules
while being invalid under current World state unless revocation and versioning
are explicit.

## Agent-specific caches

Agent systems add caches above HTTP:

- browser cache;
- CDN and proxy cache;
- API client cache;
- Host Context cache;
- Tool discovery cache;
- model prompt or retrieval cache;
- memory summaries;
- generated Tool build cache;
- provider result cache.

Each cache defines its own key, freshness, invalidation, and authority. A value
marked `no-store` at HTTP level may still be summarized or copied into an Agent
memory unless the higher-level system defines its behavior.

## Attack chains

### Poisoned Tool description

```text
Tool metadata response varies by unkeyed attacker-controlled context
→ shared cache stores attacker-influenced description or endpoint
→ Agent later discovers cached Tool
→ generated Binding points to attacker-selected capability
```

### Stale authorization metadata

```text
resource or issuer configuration changes
→ client reuses cached discovery or policy
→ Token or request is sent under obsolete trust relation
```

### Personalized response cached publicly

```text
authenticated application route and cache classify path differently
→ response containing private state enters shared cache
→ later unauthenticated request receives it
```

### Prompt or memory cache poisoning

```text
external content enters reusable Agent summary or retrieval cache
→ malicious instruction-like data survives original page
→ future Task compiles it as trusted context
→ authority is exercised later
```

## Defensive principles

- Declare cacheability and freshness explicitly.
- Ensure cache key covers all response-selecting input visible at that layer.
- Use `Vary` consistently where appropriate.
- Avoid shared caching for responses dependent on private identity unless the
  design explicitly and correctly separates variants.
- Align cache and origin URL, field, and route parsing.
- Purge or version configuration and identity metadata on revocation.
- Treat cache contents as sensitive durable state.
- Record cache status, key projection, age, variant, and origin request.
- Define higher-level Agent cache and memory semantics separately from HTTP.
- Include cache purge and residual verification in Campaign closure.

## Ordivon implication

World providers own native HTTP, CDN, browser, and Tool cache facts. Host owns
Context and memory selection. Security evaluates poisoning, audience expansion,
and persistence. Ordivon should not create one universal cache registry.
