# 04 — Fields, Metadata, and Routing

## HTTP fields are not one universal map

RFC 9110 defines HTTP field names and values as extensible metadata. A field can
be interpreted by clients, intermediaries, caches, gateways, applications, or
not interpreted at all by one hop. An intermediary may parse the field name and
forward the field value without understanding its internal syntax. [R01]

Therefore the effective path can be:

```text
sender serializes field
→ intermediary combines, removes, or forwards
→ gateway parses one syntax
→ application library parses another
→ business logic selects one value
```

## Duplicate fields

Different fields define different combination rules. Some field lines can be
combined as comma-separated values; others, such as historically special fields,
have field-specific constraints. A generic map that silently chooses first or
last occurrence can destroy protocol semantics.

Security-relevant duplicate behavior includes:

- first wins versus last wins;
- combine into a list;
- reject all duplicates;
- preserve order;
- field-specific precedence;
- gateway strips one value while origin uses another;
- log records only one occurrence.

The correct rule belongs to the field's specification, not a universal parser
convention.

## Field names and case

HTTP field names are case-insensitive. HTTP/2 and HTTP/3 require lower-case field
names on the wire. Application frameworks may expose canonical display casing or
maps. Security logic should not depend on source casing, while evidence should
retain enough information to reconstruct transformations when required. [R01][R03][R04]

## Whitespace and delimiters

HTTP/1.1 field parsing, line termination, obsolete folding, and prohibited
characters have security significance because later HTTP/1.1 recipients use CR,
LF, colon, and line boundaries as delimiters. HTTP/2 implementations must
validate field values before forwarding them to HTTP/1.1. [R02][R03]

A field value considered opaque by one hop can become syntax at another.

## Structured Fields

RFC 8941 defines common typed Lists, Dictionaries, and Items for new HTTP fields.
It intentionally specifies strict parsing and requires the entire field value to
be ignored when parsing fails. It also defines duplicate-key behavior and exact
serialization rules. [R16]

Structured Fields reduce bespoke-parser variation, but only for fields that
explicitly opt in. They do not retroactively redefine Cookie, authorization,
legacy forwarding fields, or arbitrary application headers.

The architectural lesson is:

```text
common typed grammar
+ strict failure
+ canonical serialization
→ fewer accidental differentials
```

but:

```text
syntax agreement
≠ semantic authorization agreement
```

## Routing and proxy metadata

Deployments often use fields to communicate:

- original host or scheme;
- client address;
- selected route;
- authentication result;
- tenant or region;
- trace context;
- internal authorization metadata.

If an untrusted client can supply the same field name and a trusted proxy only
appends another value, downstream first/last selection can convert attacker data
into trusted routing or identity metadata.

The trust decision must bind:

```text
which hop is authoritative
which connection delivered the field
whether incoming copies were removed
how multiple trusted hops append or sign
which parser and precedence rule the application uses
```

A field name such as `X-Forwarded-*` is not intrinsically trusted.

## Hop-by-hop versus end-to-end metadata

Some fields apply to one connection and must not be forwarded as end-to-end
metadata. If connection-specific semantics leak across a proxy boundary, a
recipient can interpret metadata outside its intended scope.

Similarly, HTTP/2 pseudo-fields are not ordinary application fields. Translation
must preserve their semantics without allowing duplicates or conflicting legacy
fields to create alternate routing meanings.

## Trailers

Trailer fields arrive after content and may be stored or processed separately.
RFC 9112 discourages merging trailers into headers unless the field definition
explicitly permits and defines the merge. [R02]

A policy decision made before trailers arrive cannot assume trailer-provided
integrity or metadata was already validated. Conversely, a downstream component
that merges trailers may act on data unseen by an upstream policy layer.

## Signatures and traces

Evidence systems often canonicalize fields for hashing, signing, or trace
projection. They must state:

- covered field instances and order;
- duplicate treatment;
- whitespace and serialization;
- whether proxy-added fields are included;
- protocol-version translation;
- trailer handling;
- redaction and secret treatment;
- which representation the executor used.

A trace digest over a normalized map is not proof that no discarded duplicate or
wire-level delimiter affected downstream execution.

## Agent amplification

An adaptive Agent can:

- compare duplicate and precedence behavior across hops;
- infer trusted-proxy boundaries;
- generate requests using a lower-level client when a high-level library merges
  fields;
- search which metadata influences cache, route, tenant, or authorization;
- exploit a monitor that records only canonical fields;
- create new application fields with underspecified grammars.

## Defensive principles

- Use field-specific parsers and semantics.
- Reject invalid duplicates where the field requires uniqueness.
- Strip untrusted copies before adding trusted forwarding metadata.
- Bind trusted metadata to authenticated hop identity.
- Prefer Structured Fields for new metadata when appropriate.
- Validate before HTTP version translation and reserialize canonically.
- Keep routing, authentication, and authorization metadata namespaces explicit.
- Preserve enough raw or digest-bound evidence to detect discarded ambiguity.
- Test header and trailer behavior across every intermediary.
- Do not use a generic string map as the sole security representation.

## Ordivon implication

World providers own concrete request, route, proxy, and provider metadata.
Runtime owns local process and library behavior. Security can test differential
interpretation. Host owns semantic Effects and should not infer authorization
from untyped forwarded fields.
