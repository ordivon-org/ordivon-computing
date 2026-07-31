# 04 — Cross-Origin Requests, CSRF, and CORS

## The most important distinction

CORS primarily governs when browser script can read a cross-origin response. It
is not a universal mechanism preventing the browser from sending cross-origin
requests.

The Fetch Standard unifies request modes, credentials, redirects, origins,
response tainting, CORS, and network behavior across Web APIs. [R10]

A browser may be able to create a cross-origin navigation, form submission, or
resource request even when script receives only an opaque response or no readable
response.

```text
send capability
≠ read capability
≠ server authorization
≠ participant intent
```

## CSRF

CSRF occurs when an attacker causes a user agent to make a request that carries
ambient authority accepted by a server, without the participant choosing the
concrete action.

The causal chain is:

```text
attacker controls request designation
+ browser carries valid ambient credential
+ endpoint accepts request shape
+ server treats session as sufficient authorization
→ unintended state change
```

The attacker may not know the session secret or read the response.

## CORS

The CORS protocol allows a server to opt into selected cross-origin response
sharing. It involves request mode, Origin, possible preflight, response headers,
credential rules, and cache behavior. [R10]

CORS policy answers a browser question:

> May this requesting origin's script access this response under these request
> conditions?

It does not answer:

- Is the requester the intended human?
- Is the request authorized for this resource and action?
- Is the external content driving an Agent malicious?
- Is the origin's own code trustworthy?
- Should the action have durable consequence?

## Credentialed CORS

Credentialed cross-origin requests intentionally allow one origin's script to
act with browser-managed credentials toward another origin when the server opts
in. This is useful for distributed applications, but the trust decision is
powerful:

```text
allowed origin
+ credentials
+ readable response
→ remote script can exercise and observe session authority
```

Origin reflection, broad allowlists, weak parsing, and mistaken assumptions
about subdomains or `null` origins can widen this authority. The exact risk must
be derived from the live policy and endpoint behavior, not from one header in
isolation.

## Preflight is not authorization

A preflight asks whether a cross-origin request with particular method and
headers may proceed under CORS. It does not authenticate the user or approve the
business Effect. A server that treats successful preflight as authorization
confuses browser protocol negotiation with resource policy.

Some request shapes do not require preflight, which is necessary for Web
compatibility. Therefore:

```text
no preflight observed
≠ request was same-origin
≠ request was harmless
```

## Origin header

The Origin header communicates request-origin information under browser rules.
RFC 6454 defined its original semantics; the Fetch Standard now owns Web
platform generation and redirect behavior. [R02][R10]

Origin validation can help bind requests to expected Web principals. It is not
proof of participant identity or intent, and server or non-browser clients can
construct headers unless another trust boundary applies.

## Fetch Metadata

Fetch Metadata request headers expose context including request destination,
mode, site relationship, and user activation. They are intended to help servers
make early decisions about whether to service a request. [R07]

Examples of useful distinctions include:

- same-origin versus same-site versus cross-site;
- navigation versus subresource or API fetch;
- document, image, script, or other destination;
- browser-indicated user activation.

Because `Sec-` headers are controlled by the user agent in browser contexts,
they provide stronger request-context evidence than arbitrary application
headers. However:

- direct clients and compromised privileged components differ;
- user activation is not a complete semantic-intent proof;
- same-site can include hostile sibling origins;
- redirects alter context;
- endpoint-specific authorization remains required.

## Defense graph

### Anti-CSRF token

A transaction-bound unpredictable value unavailable to an attacker origin can
prove that the request originated from a context that received current
application state. Its strength depends on binding, secrecy, lifetime,
validation, and resistance to same-origin compromise.

### SameSite Cookies

Reduce cross-site ambient credential attachment under defined contexts.

### Origin or Referer validation

Checks expected initiator context, with deployment-specific handling for missing
or privacy-reduced information.

### Fetch Metadata policy

Rejects requests whose site, destination, mode, or user context is inconsistent
with the endpoint.

### Custom request and content rules

May move requests out of simple cross-origin forms and require application
protocol state. This is defense in depth, not a substitute for authorization.

### Explicit transaction authorization

Binds the participant's approval to resource, action, parameters, amount,
recipient, and freshness. This is stronger than generic session possession.

## Adaptive attack considerations

An adaptive Agent can test:

- which endpoints accept simple cross-origin requests;
- whether alternate methods or navigations reach the same business Effect;
- whether sibling origins receive different treatment;
- how redirect chains affect Origin and Fetch Metadata;
- whether a browser extension, Tool, or direct API path bypasses browser-only
  controls;
- whether same-origin compromise renders cross-site defenses irrelevant.

R1 does not provide procedures for carrying out these tests. The architectural
point is that defensive evaluation must cover alternative request channels and
held-out paths.

## Agent-specific confused deputy

```text
malicious external content
→ Agent interprets content as a reason to act
→ Agent uses browser or API Tool with legitimate identity
→ browser-origin and server authorization checks pass
→ Effect violates participant Task or intent
```

CSRF defenses may not detect this because the action originates from the correct
origin and contains correct transaction state. Agent systems require a separate
instruction/authority boundary.

## Evidence requirements

Record:

- initiator origin, site, frame, and top-level site;
- request mode, destination, credential mode, and redirect chain;
- relevant Cookie and session class, without leaking bearer secrets;
- Origin and Fetch Metadata as observed by the server;
- anti-CSRF or transaction binding;
- server authorization decision;
- actual world Effect and verification;
- whether a human, page, extension, or Agent selected the action.

## Ordivon implication

World should expose request and browser-context facts. Host should bind the
Effect to the current Task and participant. Security should evaluate whether a
valid request channel was used adversarially. A generic CORS or CSRF policy
engine is not admitted by R1.
