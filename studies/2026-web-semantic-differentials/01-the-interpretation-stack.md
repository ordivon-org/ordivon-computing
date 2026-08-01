# 01 — The Interpretation Stack

## Representation changes are normal

Modern Web systems do not pass one immutable semantic object from client to
application. They transform representations:

```text
human or Agent intent
→ API object or source string
→ serializer output
→ HTTP version-specific message
→ intermediary parse and possible rewrite
→ target URL and routing decision
→ field-value parse
→ body decoding and media-type parse
→ framework parameter model
→ application schema
→ downstream query, template, command, or Tool input
→ world Effect
```

Most transformations are indispensable. Security failure arises when a decision
made on one representation is assumed to apply to a materially different later
representation.

## Core objects

### Raw representation

Exact bytes, characters, frames, or structured values received at one boundary.

### Parsed representation

A component's internal structure: message, URL record, field list, DOM tree,
JSON object, query AST, command argument vector, or model Context.

### Canonical representation

A declared normalized form used for comparison, signing, caching, validation, or
policy. Canonicalization is domain-specific; no universal canonical string
preserves every intended distinction.

### Semantic interpretation

The meaning a component assigns: target resource, message boundary, active
content type, authorization metadata, command, query, instruction, or Effect.

### Authority context

Identity, connection, session, origin, workload, Tool, and Task conditions under
which that interpretation can cause consequence.

## Differential classes

### D1 — Boundary differential

Components disagree where one message, token, record, or protocol ends and the
next begins.

Examples: HTTP message length, protocol transition point, line termination,
stream association.

### D2 — Name differential

Components disagree which resource, origin, host, path, parameter, or field a
representation identifies.

### D3 — Transformation-order differential

Decode, normalize, validate, route, sign, and execute operations occur in
different orders.

### D4 — Duplicate and precedence differential

Components disagree which repeated value wins, whether values are combined, or
whether a duplicate is invalid.

### D5 — Type differential

One component treats content as inert data while another treats it as HTML,
script, executable template, serialized object, or model instruction.

### D6 — Cache differential

The cache key and variant model omit an input that changes origin response or
authorization.

### D7 — Protocol-version or translation differential

HTTP/1.1, HTTP/2, HTTP/3, proxy translation, or optimistic transition produces
non-equivalent messages or assumptions.

### D8 — Evidence differential

Logs, traces, signatures, or monitors preserve a representation different from
the one actually executed.

### D9 — Cognitive differential

A model interprets external data as an instruction, a Tool description as an
authority grant, or a successful response as verified completion.

## Security-critical order

A common unsafe sequence is:

```text
validate R0
→ transform R0 into R1
→ execute R1
```

when the transformation can introduce special meaning not present during
validation.

CWE identifies validate-before-canonicalize and double decoding as recurring
weaknesses, while RFC 3986 warns that URI components must be separated before
safe decoding and that the same string must not be encoded or decoded more than
once. [R11][R12][R13]

The safer pattern is not simply “normalize everything first.” It is:

```text
parse at the correct domain boundary
→ reject invalid or ambiguous representations
→ produce one typed internal representation
→ apply policy to the fields and semantics actually used
→ avoid later interpretation changes
→ reserialize canonically when crossing a new declared boundary
```

## Canonicalization limits

Canonicalization can itself collapse distinctions:

- percent-encoded versus literal delimiters;
- Unicode characters with similar appearance or normalization behavior;
- duplicate fields or parameters;
- path segments and filesystem semantics;
- case-sensitive application identifiers;
- empty versus absent values;
- ordered versus unordered collections;
- signed versus unsigned metadata;
- actor and subject identity chains.

Therefore every canonicalizer needs:

```text
input domain
output type
preserved distinctions
collapsed distinctions
error behavior
idempotence expectation
version
consumers
```

## Interpretation authority map

| Decision | Required authority |
|---|---|
| HTTP message boundary | protocol recipient at that hop |
| target URI and server authority | HTTP implementation and routing layer |
| cache key and variant | cache implementation under HTTP semantics |
| effective media type | Fetch/MIME/browser or declared application parser |
| DOM and script execution | HTML/browser implementation |
| API schema | application parser and schema owner |
| database query | parameterized database interface |
| command execution | process API and argument model |
| Agent instruction selection | Host/model configuration |
| authorized Effect | Host/domain policy plus owning World/provider |
| verified outcome | independent domain verifier |

No early parser can truthfully claim ownership of all later meanings.

## Differential graph

```text
representation R
├─ I1 → M1 → policy allows
├─ I2 → M2 → route changes
├─ I3 → M3 → cache stores
└─ I4 → M4 → executor acts

if M1 != M4 and the difference crosses authority:
  security-relevant differential
```

## Defensive principles

- Minimize parser count on security-critical paths.
- Prefer shared libraries and typed structures to repeated ad hoc parsing.
- Reject ambiguity rather than repair it differently at each hop.
- Apply policy to the representation that controls execution.
- Preserve raw and canonical evidence where privacy and cost permit.
- Record transformation identity and order.
- Test translation and downgrade paths, not only nominal protocol versions.
- Separate inert data, executable code, Agent instruction, and Effect authority.
- Close residual cache, session, Tool, and external-object state after incidents.
