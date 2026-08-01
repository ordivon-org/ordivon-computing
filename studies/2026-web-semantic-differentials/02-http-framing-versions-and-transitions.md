# 02 — HTTP Framing, Versions, and Protocol Transitions

## HTTP semantics and wire formats are separate

RFC 9110 defines shared HTTP semantics, while RFC 9112, RFC 9113, and RFC 9114
define HTTP/1.1, HTTP/2, and HTTP/3 message conveyance. This separation allows
versions to evolve while preserving methods, fields, status codes, target
resources, and representation semantics. [R01][R02][R03][R04]

A deployment frequently translates between versions:

```text
client HTTP/2 or HTTP/3
→ CDN / gateway
→ HTTP/1.1 upstream
→ framework
```

Security therefore depends on both version-local validity and translation
fidelity.

## HTTP/1.1 message framing

HTTP/1.1 uses start lines, field lines, an empty line, and optional content. The
recipient determines message-body length through ordered framing rules involving
method/status semantics, transfer coding, and Content-Length. [R02]

RFC 9112 explicitly warns that:

- lenient request-line parsing can create request smuggling when recipients
  interpret robustness differently;
- conflicting Transfer-Encoding and Content-Length can indicate smuggling;
- invalid or ambiguous framing must be treated as an error and often requires
  connection closure;
- extra data must not be treated as a separate response because of cache-
  poisoning risk;
- request smuggling exploits differences among recipients to hide an additional
  request.

The fundamental failure is not the existence of two length mechanisms alone. It
is:

```text
front recipient consumes N bytes
while downstream recipient consumes M bytes
→ remaining bytes enter a different request context
```

## Connection context amplifies the primitive

HTTP/1.1 associates responses to requests by order on a persistent connection,
not by an explicit request identifier. A boundary differential can therefore
shift later requests and responses, causing one participant's bytes to be
interpreted under another participant's connection, authentication, routing, or
cache context. [R02]

## HTTP/2 and translation

HTTP/2 introduces binary framing, streams, pseudo-fields, and HPACK-compressed
field blocks. It removes several textual HTTP/1.1 ambiguities locally, but an
intermediary can translate the message into HTTP/1.1.

RFC 9113 requires field validation and states that failure to validate prohibited
characters can enable request smuggling when translated to HTTP/1.1, where
carriage return, line feed, and colon are delimiters. [R03]

Thus:

```text
validly framed HTTP/2
≠ safely translatable HTTP/1.1
```

The relevant object is the semantic message after every hop, not only the first
wire encoding.

## HTTP/3

HTTP/3 uses QUIC streams and QPACK while retaining HTTP semantics. Its security
considerations aim to be comparable to HTTP/2 with TLS, but authority,
translation, intermediaries, and application interpretation remain relevant.
[R04]

Multiplexed streams reduce ordered connection-level ambiguity, but they do not
eliminate:

- invalid field translation;
- target and authority confusion;
- application parser differentials;
- cache-key omissions;
- content interpretation;
- cross-protocol interaction;
- Agent-driven misuse of valid messages.

## Optimistic protocol transitions

RFC 9931, published in 2026 and updating RFC 9112, addresses clients that send
post-transition data before learning whether an HTTP/1.1 protocol transition
succeeded. [R05]

The ambiguity is:

```text
client assumes transition accepted
→ treats later bytes as new protocol data

server rejects transition
→ treats later bytes as more HTTP/1.1 requests
```

If the post-transition data source is less trusted than the authenticated HTTP
client, the server can interpret attacker-controlled bytes as authenticated
requests from the client. This extends request-smuggling reasoning beyond
traditional length disagreement to **temporal protocol-state disagreement**.

## Cross-protocol attacks

RFC 9113 notes that a Web client can be induced to initiate one protocol toward
a server that understands another, and that the bytes may appear valid to the
second protocol, particularly against poorly protected private-network services.
[R03]

This is a type differential at the connection level:

```text
sender believes protocol A
receiver accepts bytes as protocol B
```

## Routing and authority

HTTP routing depends on target URI, authority, Host or pseudo-fields, connection
reuse, proxy behavior, and server configuration. An intermediary can make a
policy decision on one authority representation while a downstream component
routes on another.

Evidence should preserve:

- negotiated protocol and ALPN;
- connection identity and reuse;
- raw or digest-bound framing evidence;
- pseudo-fields and translated HTTP/1.1 fields;
- target URI, authority, Host, and selected backend;
- transition request, response, and when post-transition bytes were released;
- each recipient's consumed byte range or stream;
- final request identity and Effect.

## Defensive graph cuts

- Strict protocol parsing and rejection of ambiguity.
- Complete field validation before translation.
- One canonical translation path with differential conformance tests.
- No optimistic transmission across a trust boundary unless the specification
  establishes safety.
- Connection closure after framing errors.
- Isolation of untrusted tunneled or post-transition data from authenticated
  HTTP request context.
- Backend routing based on one validated authority representation.
- Independent origin-side request and Effect observation.
- Held-out tests across HTTP versions, downgrade, gateway, and transition paths.

## Ordivon implication

World may observe path, protocol, connection, transition, routing, and provider
facts. Runtime may execute controlled parsers and differential harnesses.
Security interprets whether a discrepancy forms an attack primitive or Campaign.
Host owns the intended Effect. No generic Ordivon HTTP parser is justified.
