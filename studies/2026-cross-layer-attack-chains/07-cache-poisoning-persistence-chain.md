# 07 — Cache Poisoning: Request Difference to Persistent Audience Expansion

## Evidence boundary

Cloudflare describes Web cache poisoning as a condition where an attacker causes
an origin to produce a harmful response that shares a cache key with a clean
request, after which the cached response is served to other users. [R17]

Cloudflare's 2018 response to practical cache-poisoning research explains that
shared caches can amplify origin behavior and that both CDN and origin changes
may be required. [R18]

RFC 9111 defines cache keys, variants, freshness, persistence, and the risk that
parsing differences can enable cache poisoning. [R19]

R4 treats this as an official mechanism and mitigation family, not a claim about
one undisclosed victim incident.

## Causal graph

```text
A1 shared caching for latency and scale
→ T1 many request representations must be grouped into reusable variants
→ W1 origin response depends on input omitted from cache key
→ V1 attacker controls unkeyed input or parser differential
→ P1 origin emits attacker-influenced cacheable response
→ N1 cache stores response under broader clean key
→ C1 later users receive poisoned response without attacker input
→ N2 browser or Agent interprets content as active code/instruction
→ O1 multi-user compromise, misinformation, or unintended Tool action
→ D1 cache/origin/request contradiction
→ R1 patch origin/key logic and purge cache
→ X1 downstream browser state, Agent memory, sessions, copied content
```

## The cache is an audience multiplier

Without cache persistence, the attacker may influence only their own request.
The cache changes:

- time — response survives after original request;
- audience — unrelated users receive it;
- evidence — victim requests do not contain attacker input;
- trust — response arrives from expected domain/CDN;
- scale — one origin response can affect many clients.

## Origin and cache can both be locally correct

The origin may intentionally vary output based on a field or URL interpretation.
The cache may intentionally key only method and target plus declared variants.
Failure occurs when the origin's true response-selection function is wider than
the cache key.

```text
origin equivalence relation
≠ cache equivalence relation
```

## Active interpretation edge

A poisoned response can be:

- inert incorrect data;
- HTML or script interpreted by a browser;
- configuration consumed by a client;
- Tool metadata consumed by an Agent;
- natural language summarized into memory;
- identity or endpoint discovery data.

The Campaign impact depends on the next interpreter and authority.

## Agent memory analogy

Agent systems create higher-level caches:

```text
external document
→ retrieval result
→ summary or memory
→ reused in later Task
```

Even when an HTTP cache is purged, malicious content may persist in:

- vector/retrieval index;
- summary;
- long-term memory;
- Tool description;
- generated Artifact;
- browser storage;
- sent messages.

This is not proof that every memory is vulnerable. It is the same persistence and
audience relation at a different layer.

## Detection graph

- compare origin responses with cache keys and `Vary`;
- record unkeyed request inputs that influenced response;
- inspect cache age, source, variant, and purge state;
- compare victim request to stored response provenance;
- test exact proxy/origin parser versions;
- inspect browser DOM or Agent Context produced from cached content;
- correlate resulting sessions, Tools, and Effects.

## Defensive breakpoints

### B1 — align cache key with response dependency

Include every relevant variant or make the response non-shared/non-cacheable.

### B2 — strict request and header interpretation

Prevent cache and origin from using different target or metadata semantics.

### B3 — isolate active content

Use correct content type, `nosniff`, CSP, and separate origins where applicable.

### B4 — provenance for Tool and Agent content

Cache metadata and memory with source, version, freshness, and trust labels.

### B5 — purge and invalidate recursively

Remove CDN, browser, application, retrieval, and memory copies as required.

### B6 — verify high-value Effects independently

A cached Tool description or instruction cannot authorize a durable action by
itself.

## Recovery and residual closure

Purging one CDN key does not close:

- other variants or regions;
- browser caches;
- service workers;
- origin-side caches;
- downstream mirrors;
- Agent memory and generated Tools;
- sessions or Effects already created.

## Ordivon lesson

World/provider adapters may expose cache and content provenance; Host owns Context
selection and Effect admission; Security evaluates poisoning and persistence;
Runtime owns local cache/build Artifacts. No universal Ordivon cache or memory
scanner is justified.
