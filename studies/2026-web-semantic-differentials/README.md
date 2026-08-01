# Web Interpretation, Parsing, and Semantic Differentials

Status: R2 foundational study completed

## Purpose

R2 studies what happens when the same bytes, characters, fields, URLs, messages,
documents, or model-visible content pass through several interpreters that do not
produce the same meaning.

The central question is:

> When multiple components interpret one input, which interpretation controls
> admission, routing, caching, execution, evidence, and recovery—and what happens
> when those answers differ?

The study spans:

```text
transport bytes
→ HTTP version and message framing
→ fields and routing metadata
→ URL and form parsing
→ decoding and canonicalization
→ cache key and variant selection
→ media type and content interpretation
→ HTML and script parsing
→ application format and schema parsing
→ query, template, command, and code interpreters
→ model interpretation of data as instruction
→ authorized world Effect
```

## Adversarial stance

R2 assumes an adaptive opponent capable of:

- controlling inputs at several protocol and application boundaries;
- comparing front-end, back-end, browser, cache, framework, and Tool behavior;
- using valid as well as malformed representations;
- selecting alternative HTTP versions, intermediaries, redirects, encodings,
  methods, media types, and execution channels;
- generating differential-testing Tools and minimizing interesting inputs;
- repeating attempts and learning from errors, timing, cache state, and visible
  policy behavior;
- combining a weak interpretation difference with valid identity, ambient
  authority, internal network position, or downstream interpreters;
- exploiting Agent Context, generated Tools, memory, and evaluation semantics.

A model, Provider, Host, system prompt, Tool broker, or policy refusal is recorded
as one configured component's behavior. It is not evidence that another Agent,
custom Tool, direct protocol client, or malicious actor lacks the underlying
capability. Conversely, generated aggressive text does not prove exploitability
or world consequence.

R2 contains no exploit payloads, parser evasions, target-specific requests,
scanning procedures, or instructions for acting against public systems.

## Central result

A security-relevant semantic differential exists when:

```text
one representation R
→ interpreter I1 produces meaning M1
→ interpreter I2 produces meaning M2
→ at least one security decision depends on M1
→ later routing, execution, caching, or evidence depends on M2
```

The highest-risk form is:

```text
validator or policy sees safe meaning
while
executor or downstream authority sees dangerous meaning
```

But differentials can also produce:

- cache keys that omit response-selecting input;
- logs that record a different target than the application used;
- signatures computed over a different representation than the receiver acts on;
- one protocol endpoint consuming bytes another component considered post-
  transition data;
- a browser treating uploaded content as active when the server intended inert
  data;
- an Agent interpreting untrusted evidence as instruction and then using valid
  Tools and identity.

## Study structure

1. [`00-method-attacker-model-and-confounds.md`](00-method-attacker-model-and-confounds.md)
   — method, strong attacker, evidence, and policy-layer confounds;
2. [`01-the-interpretation-stack.md`](01-the-interpretation-stack.md) — stages,
   authority, representations, and differential taxonomy;
3. [`02-http-framing-versions-and-transitions.md`](02-http-framing-versions-and-transitions.md)
   — HTTP/1.1 framing, HTTP/2 translation, optimistic transitions, and routing;
4. [`03-url-encoding-and-canonicalization.md`](03-url-encoding-and-canonicalization.md)
   — URL parsing, percent encoding, form encoding, Unicode, and decode order;
5. [`04-fields-metadata-and-routing.md`](04-fields-metadata-and-routing.md) —
   header fields, structured fields, duplicates, forwarding, and trust metadata;
6. [`05-content-type-html-and-active-interpretation.md`](05-content-type-html-and-active-interpretation.md)
   — encoding, MIME sniffing, HTML error recovery, and active-content boundaries;
7. [`06-cache-keys-variants-and-persistence.md`](06-cache-keys-variants-and-persistence.md)
   — cache semantics, keys, variants, poisoning, persistence, and Agent caches;
8. [`07-downstream-interpreters-and-injection.md`](07-downstream-interpreters-and-injection.md)
   — schema, query, template, command, serialization, and model interpreters;
9. [`08-agent-differential-discovery-and-defense.md`](08-agent-differential-discovery-and-defense.md)
   — Agent amplification, Tool generation, evaluation, and defensive graph cuts;
10. [`09-ordivon-insertion-and-r3-gate.md`](09-ordivon-insertion-and-r3-gate.md)
    — Host, World, Runtime, Security, and Game implications plus the R3 route;
11. [`REFERENCES.md`](REFERENCES.md) — primary-source ledger.

## Durable learning rule

For each representation boundary ask:

```text
what exact bytes or values entered?
which component parsed first?
which transformations occurred, and in what order?
which representation was validated, authorized, signed, cached, routed, logged,
and executed?
what was forwarded verbatim versus reserialized?
which errors were rejected, repaired, ignored, or normalized?
which identity and connection context were inherited?
what did the final executor act upon?
what evidence can reconstruct every interpretation?
what state persists after the request ends?
```

## R2 disposition

R2 establishes a research and review discipline. It does not promote a universal
canonicalizer, parser service, Web firewall, central request journal, or generic
injection policy engine. Mature protocol implementations and typed libraries
remain the default. New Ordivon machinery requires a reproduced unowned failure,
multiple consumers, measurable benefit, and a deletion test.
