# 01 — URL, Origin, Site, and Principal

## Names are not identities

A URL designates a resource and carries structured components such as scheme,
host, port, path, query, and fragment. Different security mechanisms deliberately
select different subsets of those components.

```text
URL
  detailed designation of a resource

origin
  usually scheme + host + port; a browser protection domain

site
  scheme + registrable domain in modern browser security contexts

host
  a network naming component; often resolved through DNS

endpoint
  one current network destination, connection, or provider object

participant identity
  a human, workload, organization, Agent, or other accountable actor
```

These are related but not interchangeable.

## Origin as browser protection domain

The WHATWG HTML Standard calls origins the fundamental currency of the Web
security model: actors sharing an origin are generally assumed to trust one
another and have the same authority, while different origins are treated as
potentially hostile and isolated to varying degrees. [R01]

RFC 6454 describes an origin approximately as scheme, host, and port, and
explains why the Web groups many resources into one protection domain rather
than treating every URL as a separate principal. [R02]

This grouping is indispensable for functional Web applications, but it creates
a coarse trust boundary:

```text
all active code admitted into one origin
→ potentially receives the origin's browser authority
```

The browser does not know which script file represents the bank's core logic,
which is analytics, which is a compromised dependency, or which is generated at
runtime. Same-origin admission is therefore often a transitive authority grant.

## Origin is not participant identity

An origin answers where Web content was obtained and which browser privileges it
shares. It does not establish:

- which human initiated the action;
- which service account is active;
- which Agent or Tool selected the action;
- whether the current code still serves the site's owner;
- whether the user intended this concrete consequence;
- whether a downstream service should trust the same authority;
- whether the DNS, TLS, hosting, or deployment chain remains uncompromised.

One origin may serve millions of users and many application roles. One
participant may use many origins.

## Origin depends on lower-layer naming and transport

RFC 6454 notes that origin security for common URI schemes relies partly on DNS,
while HTTPS adds resistance through authenticated secure transport. [R02]

A browser origin therefore inherits assumptions from:

```text
URL parsing
DNS resolution
certificate and TLS validation
browser trust store
hosting and deployment control
redirect handling
current browser implementation
```

An origin comparison can be perfectly implemented while the code served at that
origin is malicious.

## Same-origin and same-site differ

An origin commonly includes scheme, host, and port. A site is a coarser grouping
used for several browser policies and process decisions. Chromium describes a
site as scheme plus registered domain, ignoring subdomain, port, and path for its
Site Isolation model. [R03]

This creates important distinctions:

```text
https://a.example.com
https://b.example.com

same site
but different origins
```

A policy that says `same-site` may permit a compromised sibling subdomain to
participate even though same-origin DOM access would remain blocked.

## Opaque origins

Some documents and contexts receive opaque origins that cannot be recreated by
serializing a tuple. Opaque origins are intentionally isolated, but their string
serialization may appear as `null`; the string alone must not be treated as one
shared principal. [R01]

This is a recurring security lesson:

> A serialized label may collapse distinctions that the browser's internal
> identity model preserves.

## Origin relaxation and compatibility

The HTML Standard warns against `document.domain` because relaxing origin checks
undermines same-origin protections and can be especially dangerous with shared
hosting. [R01]

This illustrates R0's structural tension:

```text
subdomain compatibility and legacy composition
vs.
precise isolation and authority
```

A compatibility mechanism can intentionally merge protection domains. The
security effect must be understood as an authority expansion, not merely a DOM
convenience.

## Resource designation grants trust

RFC 6454 explains that importing a script from a URI effectively grants the
resource the importing document's privileges, while submitting secrets to a URI
expresses trust in the confidentiality of the designated endpoint. [R02]

Thus a URL is not just a location. In active Web contexts, designation can cause:

- code execution with origin authority;
- disclosure of data;
- credential attachment;
- navigation and user-interface replacement;
- creation of persistent browser state;
- downstream service calls.

## Attack chains

### Same-origin supply-chain compromise

```text
trusted origin
→ imports third-party or generated active content
→ content executes with origin authority
→ reads session-visible data or performs authorized actions
→ server sees a legitimate origin and valid session
```

The same-origin policy is working as designed. The failure is transitive trust
inside the origin.

### Same-site sibling compromise

```text
broad registrable domain
+ sibling subdomain controlled or compromised
+ same-site Cookie or request policy
→ ambient authority or request-context assumptions widen
```

The exact feasibility depends on Cookie attributes, host scoping, browser policy,
and server authorization. `same-site` must never be read as `same principal`.

### Endpoint substitution

```text
dynamic configuration or redirect
→ client accepts an attacker-controlled authorization or resource endpoint
→ legitimate credentials or protocol messages are delivered to the wrong party
```

OAuth Security BCP emphasizes that dynamic relationships create endpoint and
mix-up risks that were less prominent in OAuth's original static model. [R04]

## Defensive principles

- Keep important trust distinctions visible in origins and exact endpoint
  configuration.
- Treat every active resource admitted to an origin as potentially receiving
  origin authority.
- Distinguish same-origin, same-site, top-level site, frame origin, endpoint,
  participant, and workload identity in evidence.
- Do not infer user intent from origin alone.
- Bind authorization to specific resources and actions, not merely a domain.
- Preserve redirect chains and endpoint metadata when evaluating identity.
- Use process isolation as defense in depth, not a replacement for Web policy.

## Ordivon implication

World may report:

```text
URL and endpoint
resolved identity and transport evidence
origin, site, top-level context, and redirect chain
provider and body revision
observation time and invalidation
```

Security may interpret whether a relation is adversarial. Host retains Task and
participant intent. No component should promote `origin == participant` into a
universal invariant.
