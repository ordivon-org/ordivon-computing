# 05 — OAuth, Delegation, and Token Chains

## OAuth solves delegated access, not general identity truth

OAuth allows a client to obtain limited authority to access a protected resource
on behalf of a resource owner or under another grant. It separates:

```text
resource owner
client
authorization server
resource server
access token
refresh token
authorization grant
```

OAuth is often used beneath federated login, but an access token is not by
itself a universal statement of human identity, current intent, or Actor
continuity.

## Current security baseline

RFC 9700 is the current OAuth 2.0 Security Best Current Practice. It updates the
attacker model based on practical deployment experience, dynamic multi-party
relationships, token leakage, redirect attacks, mix-up attacks, and other
implementation failures. [R04]

Its attacker model includes:

- Web attackers operating arbitrary endpoints, sites, clients, authorization
  servers, and resource servers;
- network attackers controlling unprotected communication;
- attackers who can read authorization responses or requests;
- attackers who obtain access tokens;
- collaborating attackers and legitimate protocol participants.

This closely matches the strong R1 Web attacker baseline, before adding Agent
adaptation.

## Redirect binding

Redirect-based flows move the user agent between principals. Security depends on
binding:

```text
client identity
exact redirect URI
authorization server identity
transaction and user agent
authorization code
PKCE or equivalent proof
token endpoint
```

RFC 9700 requires exact redirect URI matching except defined native-app cases,
prohibits open redirectors in relevant roles, requires CSRF protection, requires
mix-up defenses for multi-issuer clients, and requires PKCE support. [R04]

A redirect is not merely navigation. It transfers protocol state through a
browser controlled by several parties.

## Authorization code and transaction continuity

The authorization code is a temporary capability that must be bound to the
initiating transaction and client. PKCE adds proof that the redeemer possesses a
transaction-specific verifier associated with the original authorization
request. [R04]

This is conceptually similar to Ordivon Effect continuity:

```text
proposal and initiation
→ stable transaction binding
→ later redemption
→ reject detached or injected continuation
```

## Bearer tokens

A bearer token can generally be used by whoever possesses it. This makes
confidentiality, audience restriction, scope, lifetime, storage, and revocation
critical.

Token theft and token misuse are different:

- theft obtains the credential;
- misuse may occur because a legitimate client or Agent has a token broader than
  its current Task.

## Sender-constrained tokens

RFC 9449 defines DPoP, an application-layer proof-of-possession mechanism that
binds OAuth tokens to a public key and requires a per-request proof. It reduces
replay by parties that steal only the token. [R11]

DPoP itself is not authentication or authorization and does not prove human
intent. A compromised client holding both the token and key can still act.

This yields a precise hierarchy:

```text
bearer token
  possession of token is enough

sender-constrained token
  token + proof of bound key possession

authorized Effect
  valid identity + resource/action policy + current Task/intent
```

## Audience, resource, and action restriction

RFC 9700 recommends restricting tokens to the minimum required privileges,
specific resource servers, resources, and actions. RFC 8707 allows a client to
identify the target protected resource. [R04][R12]

RFC 9396 Rich Authorization Requests allows fine-grained authorization details
such as action, location, amount, and recipient rather than relying only on
coarse scope strings. [R13]

This is especially relevant to Agents:

```text
"can use payment API"
```

is much broader than:

```text
"may initiate this amount to this recipient before this deadline"
```

R1 does not prescribe RAR as a universal Ordivon protocol. It demonstrates that
mature standards already support consequence-specific authorization patterns.

## Delegation versus impersonation

RFC 8693 distinguishes:

- **impersonation** — actor A is treated as subject B within the authorized
  context;
- **delegation** — A remains identifiable as the actor representing B.

It defines token-exchange mechanisms and an `act` claim capable of representing
an actor chain. [R14]

For accountable Agent systems, delegation is generally more informative than
silent impersonation because it preserves:

```text
participant / subject
acting Agent or service
delegating service chain
current resource and action
```

But a token format alone does not guarantee that downstream logs, authorization,
or evidence retain the chain.

## JWT boundaries

JWT is a token format, not a complete trust model. RFC 8725 documents common
implementation hazards and requires explicit algorithm and validation choices.
[R15]

A signed token can be:

- authentic but overbroad;
- authentic but intended for another audience;
- authentic but stale or revoked under external policy;
- authentic but issued by an unexpected issuer;
- authentic but used by the wrong actor if bearer semantics apply;
- correctly validated but insufficient to prove current intent.

## OAuth attack-chain classes

### Redirect and endpoint confusion

```text
client supports dynamic or multiple parties
→ endpoint or issuer identity is confused
→ authorization response or credential reaches wrong participant
→ attacker redeems or reuses authority
```

### Token replay

```text
bearer token leaks
→ attacker presents token to accepted resource
→ resource validates token but cannot distinguish sender
```

Sender constraint removes this path when the key remains protected.

### Overbroad delegated authority

```text
Agent receives broad token
→ external content changes chosen action
→ action remains within token scope
→ resource server correctly authorizes
→ participant Task or intent is violated
```

This is not solved by stronger token validation alone.

### Delegation-chain erasure

```text
user delegates to Agent A
→ Agent A calls service B
→ B obtains token for service C
→ downstream evidence records only user or final client
→ responsible actor and transformation chain are lost
```

### Refresh-token persistence

```text
short-lived access token expires or is revoked
→ refresh token or delegated renewal path remains
→ authority is recreated
```

Incident closure requires revocation across the grant family and dependent
sessions.

## Defensive principles

- Follow current OAuth Security BCP rather than legacy permissive profiles.
- Bind exact redirect URIs, issuer, client, user agent, code, and redemption
  transaction.
- Use PKCE and mix-up defenses.
- Restrict token audience, resource, action, lifetime, and delegation.
- Prefer sender constraint where token replay is a material threat.
- Preserve subject and actor identity through delegation.
- Separate login identity, API authorization, and participant intent.
- Inventory refresh and exchange paths during revocation.
- Treat authorization metadata and endpoint discovery as security-sensitive
  dynamic state.
- Verify actual resource effects independently of token success.

## Ordivon implication

Host owns the semantic Effect and participant delegation. World/provider
adapters own concrete OAuth clients, endpoints, token families, and Receipts.
Security evaluates misuse, impersonation, delegation-chain loss, and residual
authority. Ordivon should reuse OAuth mechanisms instead of inventing a generic
identity protocol.
