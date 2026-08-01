# 05 — MyEtherWallet 2018: BGP, DNS, TLS, Human Override, and Transaction

## Evidence boundary

Cloudflare's incident analysis describes a 2018 BGP leak/hijack in which traffic
toward an Amazon Route 53 prefix was redirected. Recursive resolvers that
followed the affected route received malicious DNS answers for
`myetherwallet.com`, even if the end user did not directly accept the hijacked
route. [R11]

Cloudflare reported that the fraudulent site presented a self-signed certificate.
The attack required users to continue despite the certificate warning. Once
credentials were entered or browser state was disclosed, the attacker used the
legitimate site to transfer cryptocurrency. [R11]

RFC 9525 establishes that TLS clients must verify application-service reference
identities rather than treating reachability or DNS alone as service identity.
[R12]

## Causal graph

```text
A1 decentralized BGP and recursive DNS
→ T1 global reachability and cache efficiency rely on distributed policy
→ V1 unauthorized or leaked more-preferred route toward DNS infrastructure
→ P1 selected resolvers send queries to attacker-controlled path
→ P2 attacker returns false DNS answer
→ N1 browser connects to attacker endpoint
→ D1 TLS identity mismatch and certificate warning
→ W1 human overrides cryptographic contradiction
→ I1 credentials, session information, or user-entered secrets exposed
→ C1 attacker reuses valid credentials against legitimate service
→ O1 authorized-looking cryptocurrency transfer
→ X1 stolen credentials, transferred assets, poisoned resolver cache
```

## The route attack did not directly steal assets

The BGP action produced path influence. It did not by itself provide:

- valid DNS authority;
- a trusted certificate;
- user credentials;
- wallet authorization;
- access to the legitimate transaction system.

The full outcome required several independent failures and affordances.

## Resolver as audience amplifier

The attacker did not need every victim's network to select the malicious route.
Poisoning a recursive resolver affected clients that trusted its cached answer.

```text
routing impact on resolver
→ naming impact on many clients
```

This is similar to cache poisoning: compromise one shared interpretation point,
then inherit its audience.

## TLS worked as a detection boundary

The invalid/self-signed certificate was not a TLS failure in the cryptographic
sense. It was a successful contradiction signal:

```text
DNS and network say “this is the service”
TLS reference identity says “credential is not trusted for this service”
```

The attack progressed because the warning was overridden.

This case demonstrates why:

```text
DNS answer
+ successful TCP connection
≠ authenticated service
```

## Human decision as a graph edge

Security UI is an authority boundary. A warning can be:

- correctly understood and obeyed;
- ignored because of habituation;
- overridden under urgency;
- hidden or reframed by an application;
- inaccessible to an automated Agent;
- treated as a recoverable connectivity error.

An Agent that automatically bypasses certificate failures to maximize task
completion would recreate the vulnerable human edge at machine speed.

## Legitimate-service reuse

After obtaining credentials, the attacker used the genuine service to perform
the final transaction. The final system could see:

- correct endpoint;
- valid TLS;
- valid credentials;
- syntactically valid transaction.

The malicious origin occurred earlier in the chain.

## Defensive breakpoints

### B1 — routing security and monitoring

RPKI origin validation, explicit route policy, and multiple-vantage monitoring
can reduce or detect the route edge, though route leaks and path issues remain.

### B2 — resilient resolver operation

DNSSEC validation, protected resolver transport, cache handling, and independent
vantage comparisons constrain naming manipulation.

### B3 — strict TLS identity verification

Do not continue after certificate identity failure for high-value services.

### B4 — phishing-resistant transaction authorization

Bind approval to destination, amount, and transaction, not only reusable login
credentials.

### B5 — anomaly detection at legitimate service

Detect new location, session, device, transfer pattern, or beneficiary even when
credentials are valid.

### B6 — Agent fallback policy

Certificate failure must not silently trigger alternate clients, disabled
verification, or insecure paths.

## Recovery and residual closure

Restoring the BGP route does not:

- purge recursive DNS caches immediately;
- revoke stolen credentials;
- reverse completed transactions;
- restore user trust decisions;
- prove no other resolver was affected.

Closure spans route state, DNS cache, credentials, sessions, transactions, and
user notification.

## Ordivon lesson

World observations should keep route, resolver, certificate, browser decision,
session, and transaction facts distinct. Host must treat identity contradiction
as a failed Binding, not a connectivity inconvenience. Security reconstructs the
chain. Runtime may collect local evidence. No central route/DNS truth service is
justified.
