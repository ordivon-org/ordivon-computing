# 02 — DNS Naming, Resolution, Validation, and Cache

## DNS is a distributed naming system

DNS maps names to typed resource records through a hierarchy of delegation,
authoritative servers, recursive resolvers, caches, and stub resolvers. The
original architecture is specified by RFC 1034 and RFC 1035. [R01][R02]

A typical path is:

```text
application
→ local stub resolver
→ recursive resolver
→ root delegation
→ TLD delegation
→ authoritative zone
→ cached RRsets and aliases
→ application address or service selection
```

Each step can be cached, delegated, redirected by aliases, served by anycast, or
conditioned by client location and resolver policy.

## DNS answer is not endpoint identity

An address RRset answers a naming query. It does not prove:

- the endpoint is the intended application service;
- the route is correct;
- the service possesses an expected TLS key;
- the selected body is healthy;
- the returned data is globally consistent;
- an application Effect occurred.

TLS service identity and application rules must bind the selected name or other
reference identifier separately. [R34]

## Resolver and authoritative roles

- **authoritative server** publishes data for a zone;
- **recursive resolver** follows delegation and caches answers;
- **stub resolver** requests resolution for an application;
- **validating resolver** verifies DNSSEC where configured;
- **forwarder** sends queries to another recursive service;
- **application resolver** may implement its own cache or encrypted DNS path.

An Agent can unknowingly use several resolvers through OS, browser, VPN, proxy,
container, or application libraries.

## Cache poisoning and forged answers

RFC 5452 describes measures that make off-path DNS answer forgery more difficult
by increasing uncertainty in transaction matching, including source-port and
query matching behavior. [R03]

DNS Cookies add a lightweight transaction mechanism that reduces several
off-path forgery, cache-poisoning, and amplification risks; RFC 9018 refines
interoperable server-cookie construction. [R04][R05]

These mechanisms do not authenticate zone data as DNSSEC does, and they do not
protect against an on-path attacker or compromised authoritative/resolver
component under all conditions.

## DNSSEC

DNSSEC adds data-origin authentication and integrity for DNS data through signed
RRsets and a chain of trust. RFC 9364 states that using DNSSEC for origin
authentication of DNS data is best current practice. [R06]

DNSSEC can establish:

```text
this RRset or authenticated denial
was signed under a validated DNSSEC chain
and was not modified without detection
```

DNSSEC does not provide:

- confidentiality of queries;
- route security;
- server availability;
- correctness of data intentionally signed by a compromised zone authority;
- application service identity unless the application binds DNSSEC data into its
  identity mechanism;
- protection after data is transformed or interpreted incorrectly.

## Secure failure and availability tension

DNSSEC validation can fail because of attack, expired signatures, broken
configuration, clock error, unavailable data, resolver bugs, or path problems.
Treating every failure as insecure data preserves integrity but can reduce
availability; accepting insecure fallback can erase the protection.

Extended DNS Errors can provide more specific resolver explanations, but they
remain resolver claims and may be unavailable or altered outside protected
channels. [R07]

## Negative and stale caching

DNS caches both positive and negative results. RFC 9520 clarifies negative
caching of resolution failures, including some DNSSEC validation failures. [R08]

A negative result can persist after the underlying issue is repaired. A stale
positive result can preserve availability while pointing to an old endpoint.
Applications need to distinguish:

```text
NXDOMAIN
NODATA
validation failure
server failure
timeout
cached failure
stale answer
local policy block
```

## DNS implementation differentials

RFC 9267 documents recurring DNS resource-record parsing anti-patterns found in
major TCP/IP stacks, including problems that can affect UDP, TCP, DoT, and DoH
processing. [R09]

Encrypted DNS transport does not repair unsafe RR parsing. The same lesson from
R2 applies: transport protection and message interpretation are separate.

## DNS privacy

DNS-over-TLS, DNS-over-HTTPS, and DNS-over-QUIC protect queries between client
and resolver against network observers on that segment, depending on correct
identity verification. DoQ integrates QUIC and TLS and can use 0-RTT only under
its application-specific restrictions. [R10]

Encrypted DNS shifts visibility and trust toward the selected resolver. It does
not make the resolver authoritative for service identity or eliminate logging,
correlation, traffic analysis, or endpoint leakage.

## Split horizon and policy views

Enterprise, VPN, CDN, geography, ECS-like mechanisms, private zones, and local
hosts configuration can produce different answers for the same name. That can be
intentional.

A security monitor using a public resolver can therefore observe a different
World from the Agent using a VPN or private resolver.

## Attack chains

### Off-path cache poisoning

```text
resolver issues query
→ attacker races forged response matching accepted transaction state
→ poisoned RRset enters cache
→ later clients receive attacker-selected address
→ missing or weak endpoint identity verification allows connection
```

### Signed malicious data

```text
zone authority or registrar path compromised
→ attacker publishes DNSSEC-valid data
→ validating resolver correctly accepts signature
→ application incorrectly treats DNSSEC validity as benign service intent
```

### Negative-cache persistence

```text
validation or authority failure
→ resolver caches failure
→ service is repaired
→ clients continue receiving cached failure
→ Agent switches to a less secure alternate path
```

### Resolver-view deception

```text
Agent and monitor use different resolvers or network views
→ Agent reaches attacker-selected endpoint
→ monitor validates unrelated public answer
→ evaluation incorrectly reports naming safety
```

## Defensive principles

- Use DNSSEC validation where the trust and failure model requires authenticated
  DNS data.
- Use encrypted DNS transport for client-to-resolver privacy and integrity where
  appropriate, with correct resolver identity verification.
- Preserve resolver identity, validation status, alias chain, TTL, source, and
  error class.
- Do not treat a DNS answer as application service identity.
- Keep public, private, VPN, browser, and application resolver paths explicit.
- Use strict DNS libraries and test RR parsing.
- Handle negative and stale cache deliberately.
- Bind high-value endpoints to TLS/application identity and expected service type.
- Compare multiple vantage points when a naming attack is plausible.
- Reconcile provider objects and final Effects independently.

## Ordivon implication

World may expose resolver, answer, validation, cache, alias, and endpoint
observations. Providers remain authoritative for their native DNS objects. Host
selects evidence sufficient for the Effect. Security evaluates poisoning,
control-plane compromise, and view deception. Ordivon should not build a new DNS
resolver.
