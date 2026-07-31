# References

Primary standards, official implementation documents, and official evaluation
reports are used. Each entry states its support and limitation.

## [R01] WHATWG HTML — Origins

- Source: WHATWG, HTML Living Standard, “Origins.”
- URL: <https://html.spec.whatwg.org/multipage/browsers.html#origins>
- Supports: origins are the fundamental currency of the Web security model;
  same-origin actors generally share authority; opaque origins and origin
  relaxation have explicit semantics.
- Limitation: a browser protection domain is not a participant or application
  authorization model.

## [R02] RFC 6454 — The Web Origin Concept

- Source: IETF, RFC 6454.
- URL: <https://www.rfc-editor.org/info/rfc6454>
- Supports: origin principles, scheme/host/port protection domains, Origin
  header, DNS dependency, authority and trust implications of resource URIs.
- Limitation: the Fetch Standard now owns several current Web-platform details,
  and origin is intentionally a coarse isolation unit.

## [R03] Chromium — Site Isolation overview

- Source: Chromium, “Site Isolation.”
- URL: <https://www.chromium.org/Home/chromium-security/site-isolation/>
- Supports: Chromium's site definition and process separation as defense in
  depth against cross-site data exposure.
- Limitation: Chromium implementation does not define all user agents or replace
  Web standards.

## [R04] RFC 9700 — OAuth 2.0 Security Best Current Practice

- Source: IETF, RFC 9700 / BCP 240.
- URL: <https://www.rfc-editor.org/info/rfc9700>
- Supports: current OAuth attacker model, exact redirect matching, PKCE, mix-up
  defenses, token restriction, sender constraint, and dynamic-party risks.
- Limitation: OAuth does not define Ordivon Task semantics or participant intent.

## [R05] Chromium — Site Isolation Design Document

- Source: Chromium, “Site Isolation Design Document.”
- URL: <https://www.chromium.org/developers/design-documents/site-isolation/>
- Supports: process and sandbox architecture, browser-process enforcement, and
  site-per-process threat model.
- Limitation: implementation-specific and not a defense against every same-site,
  same-origin, or server-side attack.

## [R06] Chromium — Site Isolation limitations

- Source: Chromium, “Site Isolation Design Document.”
- URL: <https://www.chromium.org/developers/design-documents/site-isolation/>
- Supports: Site Isolation is not intended to mitigate ordinary XSS, CSRF,
  clickjacking, or attacks within the victim page.
- Limitation: does not measure all current browser exploit paths.

## [R07] W3C — Fetch Metadata Request Headers

- Source: W3C Web Application Security Working Group.
- URL: <https://www.w3.org/TR/fetch-metadata/>
- Supports: request-context headers for site relationship, mode, destination,
  user activation, redirect handling, and server-side early policy.
- Limitation: Working Draft status and request context do not prove participant
  identity or semantic intent.

## [R08] RFC 10025 — Cookies: HTTP State Management Mechanism

- Source: IETF, RFC 10025, July 2026.
- URL: <https://www.rfc-editor.org/info/rfc10025>
- Supports: current Cookie semantics, security attributes, historical flaws,
  and ambient-authority analysis; obsoletes RFC 6265.
- Limitation: Cookie conformance does not define application session,
  authorization, or incident closure.

## [R09] W3C — Web Authentication Level 3

- Source: W3C Web Authentication Working Group, WebAuthn Level 3.
- URL: <https://www.w3.org/TR/webauthn-3/>
- Supports: scoped public-key credentials, RP ID, origin validation, user
  presence, user verification, and authenticator-mediated authentication.
- Limitation: strong authentication does not define every later application
  authorization or Effect.

## [R10] WHATWG Fetch Standard

- Source: WHATWG, Fetch Living Standard.
- URL: <https://fetch.spec.whatwg.org/>
- Supports: unified request, response, credential, redirect, Origin, CORS,
  response-tainting, and network-fetch semantics.
- Limitation: does not define application business authorization or participant
  intent.

## [R11] RFC 9449 — OAuth 2.0 DPoP

- Source: IETF, RFC 9449.
- URL: <https://www.rfc-editor.org/info/rfc9449>
- Supports: sender-constrained OAuth tokens and per-request proof of possession
  to reduce token replay.
- Limitation: DPoP alone is neither authentication nor authorization and does not
  prevent misuse by a compromised legitimate client holding the key.

## [R12] RFC 8707 — Resource Indicators for OAuth 2.0

- Source: IETF, RFC 8707.
- URL: <https://www.rfc-editor.org/info/rfc8707>
- Supports: explicit protected-resource indication and resource-specific token
  requests.
- Limitation: resource identity alone does not express action, transaction, or
  participant intent.

## [R13] RFC 9396 — OAuth 2.0 Rich Authorization Requests

- Source: IETF, RFC 9396.
- URL: <https://www.rfc-editor.org/info/rfc9396>
- Supports: fine-grained authorization details for resource, action, amount,
  location, recipient, and similar transaction data.
- Limitation: deployments define authorization detail types; this is not a
  universal Ordivon Effect format.

## [R14] RFC 8693 — OAuth 2.0 Token Exchange

- Source: IETF, RFC 8693.
- URL: <https://www.rfc-editor.org/info/rfc8693>
- Supports: token exchange, delegation versus impersonation, subject and actor
  relations, and the `act` claim.
- Limitation: trust model, token security profile, and downstream evidence are
  deployment-specific.

## [R15] RFC 8725 — JSON Web Token Best Current Practices

- Source: IETF, RFC 8725 / BCP 225.
- URL: <https://www.rfc-editor.org/info/rfc8725>
- Supports: JWT algorithm, validation, typing, and implementation security
  guidance.
- Limitation: JWT is a token format, not an authorization, revocation, or intent
  system.

## [R16] SPIFFE — Overview and specifications

- Source: SPIFFE project, “SPIFFE Overview.”
- URL: <https://spiffe.io/docs/latest/spiffe-about/overview/>
- Supports: workload identity across dynamic heterogeneous environments,
  short-lived cryptographic identity documents, workload APIs, and mutual
  authentication independent of static IP location.
- Limitation: workload authentication does not define Agent Task authority,
  participant purpose, or external consequence.

## [R17] NIST CAISI — Strengthening AI Agent Hijacking Evaluations

- Source: NIST Center for AI Standards and Innovation.
- URL: <https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations>
- Supports: indirect prompt injection exploits weak trusted-instruction versus
  untrusted-data separation; adaptive and repeated attacks materially affect
  evaluation.
- Limitation: results are bounded to evaluated systems and do not prove every
  Agent attack path.

## [R18] NIST CAISI — Cheating on AI Agent Evaluations

- Source: NIST Center for AI Standards and Innovation.
- URL: <https://www.nist.gov/caisi/cheating-ai-agent-evaluations>
- Supports: Agents can exploit gaps between intended and implemented evaluation;
  transcript review and explicit affordance rules improve validity.
- Limitation: does not define a complete adversarial Agent evaluation protocol.
