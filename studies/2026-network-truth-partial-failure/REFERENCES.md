# References

Primary IETF standards, BCPs, and official Agent-security sources are preferred.
Each entry states what it supports and what it does not establish.

## [R01] RFC 1034 — Domain Names: Concepts and Facilities

- Source: IETF, RFC 1034.
- URL: <https://www.rfc-editor.org/info/rfc1034>
- Supports: DNS architecture, zones, delegation, resolvers, caching, and naming
  concepts.
- Limitation: later standards update DNS security, transport, and operations.

## [R02] RFC 1035 — Domain Names: Implementation and Specification

- Source: IETF, RFC 1035.
- URL: <https://www.rfc-editor.org/info/rfc1035>
- Supports: DNS message and resource-record formats and implementation basis.
- Limitation: does not include modern DNSSEC, encrypted transport, or current
  implementation guidance.

## [R03] RFC 5452 — Measures for Making DNS More Resilient against Forged Answers

- Source: IETF, RFC 5452.
- URL: <https://www.rfc-editor.org/info/rfc5452>
- Supports: off-path answer-forgery and cache-poisoning threat, transaction
  matching, and entropy requirements.
- Limitation: resilience measures do not authenticate DNS data as DNSSEC does.

## [R04] RFC 7873 — DNS Cookies

- Source: IETF, RFC 7873.
- URL: <https://www.rfc-editor.org/info/rfc7873>
- Supports: lightweight client/server Cookie mechanism reducing selected
  off-path forgery, cache poisoning, and amplification risks.
- Limitation: not full data-origin authentication or confidentiality.

## [R05] RFC 9018 — Interoperable DNS Server Cookies

- Source: IETF, RFC 9018.
- URL: <https://www.rfc-editor.org/info/rfc9018>
- Supports: interoperable anycast server-cookie construction, secret rotation,
  and privacy considerations; updates RFC 7873.
- Limitation: depends on correct implementation and does not replace DNSSEC.

## [R06] RFC 9364 — DNS Security Extensions

- Source: IETF, RFC 9364 / BCP 237.
- URL: <https://www.rfc-editor.org/info/rfc9364>
- Supports: DNSSEC document roadmap and best-current-practice status for origin
  authentication of DNS data.
- Limitation: DNSSEC does not provide query confidentiality, route security, or
  application service correctness.

## [R07] RFC 8914 — Extended DNS Errors

- Source: IETF, RFC 8914.
- URL: <https://www.rfc-editor.org/info/rfc8914>
- Supports: structured resolver error information including DNSSEC and policy
  conditions.
- Limitation: error reports are resolver observations and not independent world
  truth.

## [R08] RFC 9520 — Negative Caching of DNS Resolution Failures

- Source: IETF, RFC 9520.
- URL: <https://www.rfc-editor.org/info/rfc9520>
- Supports: negative caching requirements for resolution and selected validation
  failures.
- Limitation: cached failure can outlive the cause and does not diagnose every
  outage.

## [R09] RFC 9267 — DNS Resource Record Processing Anti-Patterns

- Source: IETF, RFC 9267.
- URL: <https://www.rfc-editor.org/info/rfc9267>
- Supports: recurring DNS RR parser implementation weaknesses across transports.
- Limitation: informational analysis, not proof that every current resolver is
  vulnerable.

## [R10] RFC 9250 — DNS over Dedicated QUIC Connections

- Source: IETF, RFC 9250.
- URL: <https://www.rfc-editor.org/info/rfc9250>
- Supports: DNS over QUIC transport, TLS integration, privacy considerations, and
  application-specific 0-RTT restrictions.
- Limitation: protects client-to-resolver transport, not resolver correctness or
  application endpoint identity.

## [R11] RFC 4271 — A Border Gateway Protocol 4

- Source: IETF, RFC 4271.
- URL: <https://www.rfc-editor.org/info/rfc4271>
- Supports: BGP-4 reachability exchange, attributes, route selection, and policy
  substrate.
- Limitation: does not provide full cryptographic route or path authorization.

## [R12] RFC 4272 — BGP Security Vulnerabilities Analysis

- Source: IETF, RFC 4272.
- URL: <https://www.rfc-editor.org/info/rfc4272>
- Supports: fundamental BGP threat and vulnerability analysis.
- Limitation: predates later RPKI and route-leak mechanisms and is not a current
  deployment audit.

## [R13] RFC 7908 — Problem Definition and Classification of BGP Route Leaks

- Source: IETF, RFC 7908.
- URL: <https://www.rfc-editor.org/info/rfc7908>
- Supports: route-leak definitions, topological relationships, and categories.
- Limitation: classification does not itself prevent leaks.

## [R14] RFC 6811 — BGP Prefix Origin Validation

- Source: IETF, RFC 6811.
- URL: <https://www.rfc-editor.org/info/rfc6811>
- Supports: RPKI-based origin-validation states and route classification.
- Limitation: validates origin authorization, not the full AS path or business
  relationship.

## [R15] RFC 8481 — Clarifications to BGP Origin Validation

- Source: IETF, RFC 8481.
- URL: <https://www.rfc-editor.org/info/rfc8481>
- Supports: separation of validation state from operator routing policy and
  clarification of route coverage.
- Limitation: does not prescribe one universal ROV policy.

## [R16] RFC 8893 — RPKI Origin Validation for BGP Export

- Source: IETF, RFC 8893.
- URL: <https://www.rfc-editor.org/info/rfc8893>
- Supports: applying origin validation to exported routes and effective origin
  after policy transformations.
- Limitation: not full path validation.

## [R17] RFC 8210 — RPKI to Router Protocol Version 1

- Source: IETF, RFC 8210.
- URL: <https://www.rfc-editor.org/info/rfc8210>
- Supports: distribution of validated RPKI prefix-origin data from caches to
  routers.
- Limitation: introduces cache freshness, availability, and configuration
  dependencies.

## [R18] RFC 9234 — Route Leak Prevention and Detection Using Roles

- Source: IETF, RFC 9234.
- URL: <https://www.rfc-editor.org/info/rfc9234>
- Supports: mutually confirmed BGP Roles, relationship-aware export constraints,
  and route-leak prevention/detection.
- Limitation: incremental deployment and correct relationship configuration are
  required.

## [R19] RFC 8212 — Default External BGP Route Propagation Behavior without Policies

- Source: IETF, RFC 8212.
- URL: <https://www.rfc-editor.org/info/rfc8212>
- Supports: explicit import/export policy requirement before eBGP route
  propagation.
- Limitation: local policy can still be incorrect.

## [R20] RFC 9774 — Deprecation of AS_SET and AS_CONFED_SET in BGP

- Source: IETF, RFC 9774, May 2025.
- URL: <https://www.rfc-editor.org/info/rfc9774>
- Supports: prohibition of originating ambiguous AS_SET and AS_CONFED_SET path
  segments and simplification of origin semantics.
- Limitation: does not solve all routing security issues.

## [R21] RFC 7132 — Threat Model for BGP Path Security

- Source: IETF, RFC 7132.
- URL: <https://www.rfc-editor.org/info/rfc7132>
- Supports: path-security attacker model, compromised routers, suppression, and
  residual threats.
- Limitation: threat model is not proof of data-plane path use.

## [R22] RFC 4787 — NAT Behavioral Requirements for Unicast UDP

- Source: IETF, RFC 4787 / BCP 127.
- URL: <https://www.rfc-editor.org/info/rfc4787>
- Supports: UDP NAT mapping, filtering, lifetime, hairpinning, and port behavior.
- Limitation: real devices vary and later RFCs update the requirements.

## [R23] RFC 7857 — Updates to NAT Behavioral Requirements

- Source: IETF, RFC 7857 / BCP 127.
- URL: <https://www.rfc-editor.org/info/rfc7857>
- Supports: updates across UDP, TCP, and ICMP NAT behavior.
- Limitation: NAT behavior does not establish participant identity or
  authorization.

## [R24] RFC 5382 — NAT Behavioral Requirements for TCP

- Source: IETF, RFC 5382.
- URL: <https://www.rfc-editor.org/info/rfc5382>
- Supports: TCP NAT mapping, connection, timeout, and filtering behavior.
- Limitation: does not define application session or Effect state.

## [R25] RFC 8305 — Happy Eyeballs Version 2

- Source: IETF, RFC 8305.
- URL: <https://www.rfc-editor.org/info/rfc8305>
- Supports: concurrent or sequenced IPv6/IPv4 connection attempts and fallback
  behavior for user-visible connectivity.
- Limitation: racing paths can complicate monitoring and does not define
  application security invariants.

## [R26] RFC 9293 — Transmission Control Protocol

- Source: IETF, RFC 9293 / STD 7.
- URL: <https://www.rfc-editor.org/info/rfc9293>
- Supports: current TCP stream, acknowledgment, retransmission, connection, and
  error semantics.
- Limitation: TCP receipt is not application commit or exactly-once Effect.

## [R27] RFC 8085 — UDP Usage Guidelines

- Source: IETF, RFC 8085 / BCP 145.
- URL: <https://www.rfc-editor.org/info/rfc8085>
- Supports: UDP application responsibilities including congestion control,
  reliability choices, message size, checksums, and middlebox considerations.
- Limitation: individual UDP application protocols define their own guarantees.

## [R28] RFC 9846 — TLS 1.3

- Source: IETF, RFC 9846, July 2026.
- URL: <https://www.rfc-editor.org/info/rfc9846>
- Supports: current TLS 1.3 protocol, authentication, confidentiality, integrity,
  resumption, 0-RTT replay limits, negotiation, and implementation guidance;
  obsoletes RFC 8446.
- Limitation: TLS protects channels, not endpoint integrity, application
  authorization, or world outcome.

## [R29] RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport

- Source: IETF, RFC 9000.
- URL: <https://www.rfc-editor.org/info/rfc9000>
- Supports: QUIC connections, streams, Connection IDs, address validation,
  migration, anti-amplification, and transport semantics.
- Limitation: application protocols define Effect and replay safety.

## [R30] RFC 9001 — Using TLS to Secure QUIC

- Source: IETF, RFC 9001.
- URL: <https://www.rfc-editor.org/info/rfc9001>
- Supports: TLS handshake integration, encryption levels, keys, and 0-RTT in
  QUIC.
- Limitation: predates RFC 9846 text updates but remains the QUIC v1 TLS mapping.

## [R31] RFC 9308 — Applicability of the QUIC Transport Protocol

- Source: IETF, RFC 9308.
- URL: <https://www.rfc-editor.org/info/rfc9308>
- Supports: QUIC fallback, 0-RTT application requirements, Connection IDs,
  migration, NAT rebinding, and deployment caveats.
- Limitation: informational applicability guidance, not one application profile.

## [R32] RFC 9298 — Proxying UDP in HTTP

- Source: IETF, RFC 9298.
- URL: <https://www.rfc-editor.org/info/rfc9298>
- Supports: CONNECT-UDP and UDP tunneling through HTTP proxies.
- Limitation: proxying does not authenticate the final application service or
  prove tunnel policy.

## [R33] RFC 9110 — HTTP Semantics

- Source: IETF, RFC 9110 / STD 97.
- URL: <https://www.rfc-editor.org/info/rfc9110>
- Supports: safe and idempotent method semantics, retries, intermediaries,
  routing, and application-level HTTP claims.
- Limitation: method semantics do not guarantee implementation correctness or
  exactly-once external Effects.

## [R34] RFC 9525 — Service Identity in TLS

- Source: IETF, RFC 9525.
- URL: <https://www.rfc-editor.org/info/rfc9525>
- Supports: DNS-ID, IP-ID, SRV-ID, URI-ID, reference-identity construction, and
  certificate matching for application services.
- Limitation: identity match does not establish endpoint integrity, participant
  intent, or application outcome.

## [R35] NIST — 2026 AI Agent Security RFI Summary

- Source: NIST Trustworthy and Responsible AI 800-5, May 2026.
- URL: <https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai>
- Supports: classical cybersecurity remains relevant but requires adaptation for
  Agent systems; identity, authorization, tools, and evaluation remain active
  concerns.
- Limitation: stakeholder-response synthesis is not a validated network
  architecture or control standard.

## [R36] NIST CAISI — Agent Hijacking Evaluations

- Source: NIST Center for AI Standards and Innovation.
- URL: <https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations>
- Supports: adaptive and repeated Agent attacks, complete-system evaluation, and
  separation of trusted instruction from untrusted data.
- Limitation: results are bounded to evaluated systems and scenarios.
