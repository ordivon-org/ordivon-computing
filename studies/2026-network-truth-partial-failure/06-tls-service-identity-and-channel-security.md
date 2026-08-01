# 06 — TLS, Service Identity, and Channel Security

## Current TLS baseline

RFC 9846, published in July 2026, is the current TLS 1.3 specification and
obsoletes RFC 8446. It preserves TLS 1.3 compatibility while tightening and
clarifying requirements. [R28]

TLS aims to provide:

- peer authentication, with server authentication normally required and client
  authentication optional;
- confidentiality of protected application data between endpoints;
- integrity against undetected modification;
- negotiated algorithms and keys bound to the handshake transcript.

TLS assumes an attacker can control the network. It does not assume endpoints or
credential authorities are uncompromised.

## Channel security is not service correctness

A successful TLS handshake proves that the peer demonstrated possession of
credential material accepted under the client's configured trust and identity
matching process.

It does not prove:

- the endpoint software is benign or uncompromised;
- the DNS or route was globally correct;
- the participant intended the connection;
- the application request is authorized;
- a proxy did not terminate and originate a separate TLS connection;
- the service completed an Effect;
- data is hidden from the TLS endpoints;
- traffic length and timing reveal nothing.

## Reference identity

RFC 9525 defines how clients construct and match application-service reference
identifiers such as DNS-ID, IP-ID, SRV-ID, and URI-ID. [R34]

The reference identity should come from a source appropriate to the application,
such as a configured or user-provided service name, not be silently replaced by
an untrusted intermediate DNS target.

This distinction matters:

```text
DNS resolves service.example to host.example
→ certificate should match the application's reference identity according to
  its protocol rules
```

not automatically every intermediate name encountered during resolution.

## Certificate validity and authorization

A valid certificate chain and identity match establish cryptographic service
identity under the trust model. They do not define which resource or operation
the service may perform for the user, nor whether a certificate holder remains
organizationally authorized.

Revocation, compromise response, certificate transparency, issuance policy,
short lifetimes, and endpoint inventory remain operational concerns.

## TLS termination

Common deployments terminate TLS at:

- CDN;
- reverse proxy;
- load balancer;
- API gateway;
- service-mesh sidecar;
- enterprise inspection proxy;
- VPN or secure relay.

The terminator sees plaintext and creates a second trust boundary toward the
origin or next hop.

```text
client ↔ TLS terminator
terminator ↔ origin TLS or plaintext
```

TLS properties apply to each connection separately. End-to-end application
security cannot be inferred from the client-side lock indicator alone.

## SNI, ALPN, and routing

The ClientHello can carry server-name and application-protocol information.
Intermediaries may route based on those values before application data is
available. The handshake authenticates negotiated parameters, but initial
metadata and traffic patterns can still expose information unless additional
mechanisms protect them.

Routing and identity must agree:

```text
reference service identity
+ selected certificate
+ negotiated application protocol
+ actual backend route
```

A valid certificate for a broad shared service does not prove the correct tenant
or backend was selected.

## Session resumption and PSKs

TLS 1.3 supports resumption through PSKs and tickets. Resumption reduces latency
and can preserve authentication context, but introduces:

- ticket lifetime and rotation;
- cluster-wide key sharing;
- replay and correlation considerations;
- changed endpoint deployment since original connection;
- stale authorization assumptions;
- operational difficulty revoking all resumable state.

A resumed cryptographic session does not automatically revalidate application
permissions or current Task scope.

## 0-RTT early data

TLS 1.3 permits early application data before handshake completion in configured
resumption cases. RFC 9846 emphasizes that 0-RTT does not provide inherent
replay protection. Applications must define which operations are safe and how
anti-replay is handled. [R28]

```text
confidential early data under resumption keys
≠ fresh, unique, non-replayed Effect
```

High-consequence non-idempotent operations should not be admitted merely because
0-RTT is cryptographically protected.

## Downgrade and fallback

TLS negotiates versions and algorithms through authenticated handshake data.
Applications can still weaken security through external fallback logic:

```text
TLS or QUIC attempt fails
→ application retries older protocol, alternate endpoint, or plaintext path
```

Fallback must preserve required confidentiality, identity, and authorization
properties. RFC 9308 warns that QUIC fallback can degrade performance and
security and must not silently violate application expectations. [R31]

## Mutual TLS

Client certificates or workload identities can authenticate both endpoints.
Mutual TLS identifies a credentialed client or workload, not the human's current
intent or the exact permitted Effect. Broad mTLS identities can become ambient
service authority.

## Traffic analysis and metadata

TLS does not hide endpoint addresses, all handshake metadata, packet sizes,
timing, or traffic volume. Padding and privacy extensions can reduce selected
leakage, but channel confidentiality is not anonymity.

## Attack chains

### Correct certificate, compromised endpoint

```text
service body or deployment pipeline compromised
→ endpoint retains valid certificate
→ clients authenticate successfully
→ malicious application behavior occurs inside protected channel
```

### TLS-terminator trust expansion

```text
client authenticates CDN or proxy
→ proxy routes plaintext or separately encrypted traffic
→ internal route or origin identity is weak
→ attacker compromises intermediary or next hop
```

### Replayed early Effect

```text
client sends state-changing operation in 0-RTT
→ early data is replayed or accepted more than once
→ server processes duplicate Effect
```

### Stale resumption authority

```text
user or workload privilege revoked
→ old ticket or application Token remains usable
→ resumed channel succeeds
→ application fails to re-evaluate current authorization
```

## Defensive principles

- Use the current TLS specification and secure deployment profiles.
- Construct and verify application-specific reference identities correctly.
- Treat certificate validation, endpoint trust, application authorization, and
  Effect intent as separate checks.
- Make every TLS terminator and plaintext boundary explicit.
- Revalidate current authorization after resumption.
- Restrict 0-RTT to operations safe under replay or use application-level
  anti-replay and Effect identity.
- Avoid insecure fallback.
- Rotate and inventory resumption and termination keys.
- Bind ALPN, tenant, route, and backend expectations.
- Verify final application Effects independently.

## Ordivon implication

World/providers own concrete endpoint, certificate, TLS, terminator, and Receipt
facts. Host owns Task, identity requirements, Effect, and retry admission.
Security evaluates endpoint compromise, fallback, replay, and trust expansion.
Runtime owns local client and key-mount facts. Ordivon should not implement TLS.
