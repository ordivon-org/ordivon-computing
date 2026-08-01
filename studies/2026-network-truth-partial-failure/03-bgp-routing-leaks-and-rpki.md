# 03 — BGP Routing, Leaks, Hijacks, and RPKI

## BGP distributes reachability under policy

BGP-4 exchanges network reachability information among autonomous systems and
allows policy-based route selection. It was designed for decentralized Internet
routing, not as a complete cryptographic proof of path authorization. RFC 4271
specifies the protocol; RFC 4272 analyzes fundamental security vulnerabilities.
[R11][R12]

A BGP UPDATE can carry:

- reachable prefixes;
- an AS_PATH;
- next-hop and policy attributes;
- withdrawals;
- communities and implementation-specific policy inputs.

The selected route is a local policy result, not a globally authoritative path
truth.

## Route hijack and route leak differ

A route-origin hijack involves an unauthorized or unexpected AS originating a
prefix or a more-specific prefix.

A route leak propagates a route beyond the intended business or topological
relationship—for example, exporting a provider-learned route to another provider
or peer. RFC 7908 classifies common route-leak types. [R13]

A leak can involve a route whose origin is valid. Therefore:

```text
valid origin
≠ valid propagation path
```

## BGP observations are vantage-specific

A route collector sees announcements received through its sessions. Another
network may select a different route. Data-plane forwarding can also diverge from
control-plane expectation because of policy, tunneling, traffic engineering,
failover, stale state, or asymmetric routing.

Evidence should distinguish:

```text
announcement observed
route accepted
route selected
route installed
packet forwarded
destination reached
application succeeded
```

## RPKI Route Origin Validation

RPKI allows holders of Internet number resources to create cryptographically
verifiable statements about which AS may originate a prefix. RFC 6811 defines
Route Origin Validation states; RFC 8481 clarifies that validation state and
routing policy are separate; RFC 8893 addresses origin validation for exported
routes. [R14][R15][R16]

ROV can classify an origin as valid, invalid, or not found under current RPKI
data. It does not validate the entire AS path or business relationship.

```text
ROV-valid
→ origin authorization matches current ROA data
≠ path is leak-free
≠ every AS on path is honest
≠ endpoint identity is correct
```

## RPKI cache and router path

Routers commonly receive validated RPKI data from cache systems using the
RPKI-to-Router protocol. This creates additional freshness, availability,
configuration, and trust relations. A router can have stale or unavailable
validation data even while BGP continues operating. [R17]

## BGP Roles and route-leak prevention

RFC 9234 allows eBGP peers to mutually confirm relationship Roles and applies
export constraints such as the Only-To-Customer attribute to prevent or detect
route leaks. [R18]

This addresses propagation semantics that origin validation alone cannot.
Deployment remains incremental, and misconfiguration or unsupported peers can
leave gaps.

## Default-deny export policy

RFC 8212 changes default external BGP propagation behavior toward requiring
explicit import and export policy before routes are exchanged. [R19]

This is a thin, high-value defensive principle:

```text
no explicit eBGP policy
→ no route propagation
```

It reduces accidental global consequence without creating a central routing
authority.

## AS_PATH simplification

RFC 9774, published in 2025, prohibits origination of AS_SET and AS_CONFED_SET
path segments, simplifying origin semantics and security mechanisms. [R20]

This illustrates a recurring strategy:

> Delete ambiguous legacy representation when its compatibility value no longer
> exceeds the security and implementation cost.

## BGPsec and path security limits

Path-validation mechanisms can authenticate additional path information, but
routing remains policy-driven and operationally complex. RFC 7132's threat model
emphasizes that compromised authorized routers, route suppression, and policy
issues remain relevant. [R21]

Cryptographic path validation cannot prove that traffic physically followed the
advertised path or that the destination service is trustworthy.

## Attack chains

### Origin hijack without endpoint identity

```text
attacker announces victim prefix or more-specific route
→ some networks select attacker path
→ clients lacking strong application identity connect
→ traffic is observed, modified, or terminated
```

TLS identity can prevent silent application impersonation when keys and
validation remain intact, though denial and traffic analysis can still occur.

### Valid-origin route leak

```text
legitimate route learned under one relationship
→ leaked to another provider or peer
→ global traffic shifts through unintended network
→ congestion, interception opportunity, or outage
```

ROV may show valid because the origin is unchanged.

### RPKI control-plane failure

```text
validation cache stale or unavailable
→ router policy changes behavior or treats route as not found
→ availability or security posture shifts
→ Agent path selector interprets shift as endpoint failure and falls back
```

### Monitor-view mismatch

```text
route collector sees normal path
→ affected user network receives leaked route
→ central monitor reports healthy routing
→ attack persists in one region or provider
```

## Defensive principles

- Use explicit import/export policy and default-deny where supported.
- Deploy RPKI origin validation with deliberate policy and freshness handling.
- Use BGP Roles and relationship-aware leak prevention where applicable.
- Reject or retire ambiguous legacy path constructs.
- Monitor announcements from multiple independent vantage points.
- Correlate control-plane route state with data-plane path and endpoint identity.
- Keep route, TLS, application, and Effect evidence separate.
- Design fallback so route anomalies do not silently weaken identity or
  confidentiality.
- Preserve route changes and affected prefixes during incident reconstruction.
- Do not treat one collector or ROV state as global truth.

## Ordivon implication

World may bind external route observations, RPKI state, provider path, and
vantage. Security interprets hijack, leak, suppression, and deception hypotheses.
Host decides whether alternate paths preserve Task requirements. Runtime can run
local measurement Tools. Ordivon should not build a BGP controller or global
route oracle.
