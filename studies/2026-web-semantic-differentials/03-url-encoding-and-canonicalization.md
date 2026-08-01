# 03 — URL, Encoding, and Canonicalization

## A URL is a parsed record, not merely a string

The WHATWG URL Standard defines state-machine parsing for URLs, domains, hosts,
IP addresses, percent encoding, and `application/x-www-form-urlencoded`. It
exists partly because browser interoperability required one detailed algorithm
rather than divergent ad hoc parsers. [R06]

Different software ecosystems may still use RFC 3986-oriented parsers, WHATWG
parsers, framework routers, reverse proxies, filesystem paths, or application-
specific logic. The same source string can therefore produce different records.

## Component boundaries precede decoding

RFC 3986 requires URI components and subcomponents significant to dereferencing
to be parsed before percent-decoded octets are interpreted; otherwise encoded
data may become structural delimiters. It also warns not to encode or decode the
same string more than once. [R11]

This establishes two critical relations:

```text
parse component boundaries
→ then decode component data under that component's rules
```

and:

```text
one declared decode stage
→ typed internal representation
→ no accidental second decode downstream
```

## Percent encoding is context-sensitive

The URL Standard defines several percent-encode sets. Characters encoded in a
path, query, fragment, userinfo component, or form body do not all follow the
same rules. The `application/x-www-form-urlencoded` format also maps `+` to
space during parsing and performs percent decoding before UTF-8 decoding. [R06]

Therefore:

```text
percent-decode(input)
```

without naming the component and format is underspecified.

## Legacy encodings

The URL Standard notes that HTML documents using legacy character encodings can
produce query bytes different from UTF-8 documents for the same visible text.
Using UTF-8 consistently removes this source of divergence. [R06]

The Encoding Standard centralizes legacy decoder behavior because differing
error recovery has historically produced security problems. [R07]

## Canonicalization weaknesses

MITRE CWE identifies:

- double decoding of the same data;
- validating before canonicalization;
- improper input validation where parsing is scattered across the program;
- inconsistent interpretation of HTTP requests.

[R12][R13][R14][R15]

The dangerous chain is:

```text
raw representation R0
→ security component validates interpretation M0
→ downstream decodes or normalizes again
→ representation R1 obtains delimiters or path semantics
→ executor acts on M1
```

## Path layers

A Web path can pass through:

```text
URL parser
→ proxy route matcher
→ framework router
→ application path logic
→ object-store key or filesystem path
```

Each layer may differ on:

- repeated separators;
- dot segments;
- percent-encoded delimiters;
- case;
- trailing separators;
- Unicode normalization;
- empty segments;
- reserved characters;
- platform-specific filesystem rules.

A safe decision must be made on the exact typed path used by the final resource
owner, or the resource owner must accept only a canonical path produced before
policy.

## Query parameters and duplicates

Query parsers can differ on:

- first versus last duplicate value;
- list accumulation;
- semicolon or ampersand separators;
- missing versus empty values;
- plus versus percent-encoded space;
- nested parameter syntax;
- invalid percent sequences;
- character decoding.

If a gateway authorizes one duplicate while the application uses another, an
attacker can cross the policy/execution boundary without violating either
parser's local rules.

## Host and domain interpretation

Hosts can involve:

- case folding;
- internationalized domain processing;
- IPv4 and IPv6 textual forms;
- default ports;
- trailing dots;
- opaque versus special schemes;
- userinfo rendering;
- browser display decisions.

Security comparisons should use parsed host and origin records from the relevant
standard implementation, not substring tests or visually rendered URLs.

## Signatures and canonical requests

When a request is signed, the signer and verifier must agree on:

```text
which fields are covered
which URL form is signed
which percent encoding is preserved
how duplicates and whitespace are handled
whether intermediaries may rewrite
what representation the executor uses
```

A cryptographically valid signature over a non-authoritative representation can
still authorize a different downstream meaning.

## Agent amplification

An Agent can:

- generate equivalent-looking URL variants;
- compare parser outputs across languages and services;
- infer hidden normalization stages from errors;
- build a local differential corpus and minimizer;
- combine a path differential with valid identity or cache state;
- follow redirects and discover that a later component re-parses values;
- create a Tool that bypasses high-level client normalization.

This is an amplification of parser-differential research, not proof that all
systems are exploitable.

## Defensive principles

- Adopt one standards-conformant URL parser per boundary.
- Convert to typed URL, host, path, and parameter objects early.
- Reject invalid encodings and ambiguous values.
- Decode exactly once under the declared component format.
- Validate after the transformations that define the resource identity.
- Avoid security decisions on raw string prefixes or rendered URLs.
- Define duplicate-parameter policy explicitly and enforce it end to end.
- Pass typed values to downstream resource APIs rather than re-concatenating.
- Log raw digest, parsed components, canonical representation, and selected
  resource without leaking secrets.
- Test across proxy, framework, language, filesystem, and object-store parsers.

## Ordivon implication

World-native providers own target URL and selected external resource facts. Host
owns the semantic target and Effect. Security can compare interpretations in a
controlled World. Ordivon should not invent a universal URL canonicalizer.
