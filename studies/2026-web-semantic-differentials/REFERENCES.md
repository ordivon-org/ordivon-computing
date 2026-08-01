# References

Primary standards and official taxonomies are preferred. Each entry states what
it supports and what it does not establish for Ordivon.

## [R01] RFC 9110 — HTTP Semantics

- Source: IETF, RFC 9110 / STD 97.
- URL: <https://www.rfc-editor.org/info/rfc9110>
- Supports: shared HTTP semantics, messages, fields, methods, status codes,
  routing, authority, intermediaries, and version-independent abstractions.
- Limitation: does not define one deployment's application semantics or every
  version-specific wire parser.

## [R02] RFC 9112 — HTTP/1.1

- Source: IETF, RFC 9112, updated by RFC 9931.
- URL: <https://www.rfc-editor.org/info/rfc9112>
- Supports: HTTP/1.1 syntax, message framing, connection management, strict
  handling of ambiguity, response splitting, and request smuggling.
- Limitation: conformance does not prove every intermediary or origin implements
  the rules identically.

## [R03] RFC 9113 — HTTP/2

- Source: IETF, RFC 9113.
- URL: <https://www.rfc-editor.org/info/rfc9113>
- Supports: binary framing, streams, pseudo-fields, field validation,
  translation concerns, authority, and cross-protocol attacks.
- Limitation: does not define application parser, cache, or browser semantics.

## [R04] RFC 9114 — HTTP/3

- Source: IETF, RFC 9114.
- URL: <https://www.rfc-editor.org/info/rfc9114>
- Supports: HTTP semantics over QUIC, streams, pseudo-fields, authority, and
  security relationship to HTTP/2.
- Limitation: HTTP/3 does not eliminate downstream translation or application
  interpretation failures.

## [R05] RFC 9931 — Security Considerations for Optimistic Protocol Transitions in HTTP/1.1

- Source: IETF, RFC 9931, 2026.
- URL: <https://www.rfc-editor.org/info/rfc9931>
- Supports: temporal protocol-state disagreement, request smuggling through
  optimistic post-transition data, and trust-boundary requirements; updates RFC
  9112.
- Limitation: addresses optimistic HTTP/1.1 transitions, not all parser
  differentials.

## [R06] WHATWG URL Standard

- Source: WHATWG, URL Living Standard.
- URL: <https://url.spec.whatwg.org/>
- Supports: URL records, parsing state machine, hosts, percent encoding,
  `application/x-www-form-urlencoded`, and browser interoperability.
- Limitation: non-browser ecosystems and downstream filesystems or routers can
  use different semantics.

## [R07] WHATWG Encoding Standard

- Source: WHATWG, Encoding Living Standard.
- URL: <https://encoding.spec.whatwg.org/>
- Supports: standardized encoders, decoders, labels, legacy encodings, error
  handling, and security background.
- Limitation: correct character decoding does not determine HTML, URL, or
  application semantics.

## [R08] WHATWG HTML — Parsing HTML documents

- Source: WHATWG, HTML Living Standard.
- URL: <https://html.spec.whatwg.org/multipage/parsing.html>
- Supports: byte decoding, encoding confidence, tokenization, tree construction,
  error recovery, and security requirement for precise invalid-byte handling.
- Limitation: HTML parser conformance does not establish application trust or
  prevent same-origin malicious code.

## [R09] WHATWG MIME Sniffing Standard

- Source: WHATWG, MIME Sniffing Living Standard.
- URL: <https://mimesniff.spec.whatwg.org/>
- Supports: declared and effective MIME type, compatibility motivation, and
  security risk when clients interpret content as more active than servers
  intended.
- Limitation: browser MIME behavior does not classify model-visible content or
  every nested application format.

## [R10] RFC 9111 — HTTP Caching

- Source: IETF, RFC 9111 / STD 98.
- URL: <https://www.rfc-editor.org/info/rfc9111>
- Supports: cache operation, keys, freshness, variants, persistence, sensitive
  cache state, poisoning, and parser-difference risk.
- Limitation: higher-level application, Agent, and memory caches require their
  own semantics.

## [R11] RFC 3986 — URI Generic Syntax

- Source: IETF, RFC 3986 / STD 66.
- URL: <https://www.rfc-editor.org/info/rfc3986>
- Supports: URI components, percent encoding, normalization, parse-before-
  decode requirement, and warning against repeated encode/decode.
- Limitation: WHATWG URL defines current browser parsing and differs in scope and
  algorithms.

## [R12] CWE-174 — Double Decoding of the Same Data

- Source: MITRE CWE 4.20.
- URL: <https://cwe.mitre.org/data/definitions/174.html>
- Supports: repeated decoding can expose special meaning only to downstream
  components.
- Limitation: a weakness class does not prove one implementation is vulnerable.

## [R13] CWE-180 — Validate Before Canonicalize

- Source: MITRE CWE 4.20.
- URL: <https://cwe.mitre.org/data/definitions/180.html>
- Supports: validating a pre-canonical representation can permit a dangerous
  canonical form to reach execution.
- Limitation: “canonicalize first” remains domain-specific and can be unsafe if
  the wrong canonicalizer is chosen.

## [R14] CWE-20 — Improper Input Validation

- Source: MITRE CWE 4.20.
- URL: <https://cwe.mitre.org/data/definitions/20.html>
- Supports: parsing as a distinct boundary, syntactic and semantic validation,
  consistency, and avoidance of scattered parser logic.
- Limitation: broad taxonomy does not prescribe one universal validation layer.

## [R15] CWE-444 — Inconsistent Interpretation of HTTP Requests

- Source: MITRE CWE 4.20.
- URL: <https://cwe.mitre.org/data/definitions/444.html>
- Supports: intermediary and destination disagreement can create HTTP request or
  response smuggling and cache poisoning.
- Limitation: focuses on HTTP interpretation and not every downstream or Agent
  interpreter.

## [R16] RFC 8941 — Structured Field Values for HTTP

- Source: IETF, RFC 8941.
- URL: <https://www.rfc-editor.org/info/rfc8941>
- Supports: common typed HTTP field structures, intentionally strict parsing,
  canonical serialization, and explicit duplicate behavior.
- Limitation: only applies to fields that opt into the specification and does
  not define business authorization.

## [R17] RFC 9205 — Building Protocols with HTTP

- Source: IETF, RFC 9205 / BCP 56.
- URL: <https://www.rfc-editor.org/info/rfc9205>
- Supports: preserving HTTP semantics, intermediaries, fields, content types,
  caching, application state, browser security controls, and API design.
- Limitation: best-practice guidance does not prove a particular deployment is
  conformant or secure.

## [R18] NIST CAISI — Strengthening AI Agent Hijacking Evaluations

- Source: NIST Center for AI Standards and Innovation.
- URL: <https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations>
- Supports: trusted-instruction versus untrusted-data failure, adaptive attacks,
  repeated attempts, and complete-system evaluation.
- Limitation: results are bounded to evaluated Agents and scenarios.

## [R19] NIST CAISI — Cheating on AI Agent Evaluations

- Source: NIST Center for AI Standards and Innovation.
- URL: <https://www.nist.gov/caisi/cheating-ai-agent-evaluations>
- Supports: gaps between intended tasks and implemented affordances or scorers
  can create false capability conclusions.
- Limitation: does not define a complete parser-differential evaluation system.
