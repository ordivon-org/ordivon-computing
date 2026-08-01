# References

Official court, regulator, government, vendor, standards, and evaluation sources
are preferred. Operational details present in some sources are not reproduced in
this study.

## [R01] CWE-918 — Server-Side Request Forgery

- Source: MITRE CWE 4.20.
- URL: <https://cwe.mitre.org/data/definitions/918.html>
- Supports: server-side request selection can reach unintended destinations and
  inherit server network authority.
- Limitation: a weakness class does not prove one implementation or incident
  path.

## [R02] AWS — IMDSv2 defense in depth

- Source: AWS Security Blog, “Add defense in depth against open firewalls,
  reverse proxies, and SSRF vulnerabilities with enhancements to the EC2
  Instance Metadata Service.”
- URL: <https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/>
- Supports: IMDS role, SSRF/reverse-proxy threat classes, session-oriented token,
  instance binding, and defense-in-depth rationale.
- Limitation: not a complete account of the Capital One incident and not a
  replacement for application/IAM security.

## [R03] AWS EC2 — Instance Metadata Service configuration

- Source: Amazon EC2 User Guide.
- URL: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html>
- Supports: current IMDSv1/IMDSv2 behavior, session duration, and ability to
  require IMDSv2.
- Limitation: documents service configuration, not one incident's exact requests.

## [R04] DOJ — Capital One criminal complaint and 2019 arrest release

- Source: U.S. Department of Justice, Western District of Washington.
- URL: <https://www.justice.gov/usao-wdwa/pr/seattle-tech-worker-arrested-data-theft-involving-large-financial-services-company>
- Supports: misconfigured firewall, server command reach, cloud WAF role
  credentials, bucket listing/copying, logs, and disclosure timeline as stated in
  the complaint.
- Limitation: complaint allegations were filed before trial; R4 uses later
  conviction separately and abstracts operational commands.

## [R05] DOJ — Paige Thompson conviction

- Source: U.S. Department of Justice, Western District of Washington, June 2022.
- URL: <https://www.justice.gov/usao-wdwa/pr/former-seattle-tech-worker-convicted-wire-fraud-and-computer-intrusions>
- Supports: conviction, scanning for misconfigured AWS accounts, theft from more
  than 30 entities, and Capital One scale.
- Limitation: press release does not expose every technical transition.

## [R06] OCC — Capital One cloud-risk enforcement action

- Source: Office of the Comptroller of the Currency, August 2020.
- URL: <https://www.occ.gov/news-issuances/news-releases/2020/nr-occ-2020-101.html>
- Supports: regulatory finding of ineffective risk assessment before major cloud
  migration and delayed correction of deficiencies.
- Limitation: governance finding is not a packet- or command-level incident trace.

## [R07] Microsoft — Exchange CVE-2022-41040/41082 attacks

- Source: Microsoft Threat Intelligence, September/November 2022.
- URL: <https://www.microsoft.com/en-us/security/blog/2022/09/30/analyzing-attacks-using-the-exchange-vulnerabilities-cve-2022-41040-and-cve-2022-41082/>
- Supports: authenticated SSRF/RCE chain, Web Shell, Active Directory
  reconnaissance, targeted attacks, and exfiltration.
- Limitation: observed small campaign and vendor telemetry do not define every
  possible implementation path.

## [R08] Microsoft — Anatomy of Exchange server attacks

- Source: Microsoft Defender Security Research Team, June 2020.
- URL: <https://www.microsoft.com/en-us/security/blog/2020/06/24/defending-exchange-servers-under-attack/>
- Supports: Exchange strategic privilege, Web Shell persistence, process chains,
  built-in administration tools, mailbox export, and credential-response scope.
- Limitation: covers several campaigns and vulnerabilities rather than only the
  2022 chain.

## [R09] Apache HTTP Server vulnerability records

- Source: Apache HTTP Server Project, 2.4 vulnerability ledger.
- URL: <https://httpd.apache.org/security/vulnerabilities_24.html>
- Supports: CVE-2023-25690 rewrite/proxy request splitting and consequences;
  additional request-smuggling and response-splitting defects.
- Limitation: potential impact statements do not prove exploitation in a named
  victim Campaign.

## [R10] RFC 9112 — HTTP/1.1

- Source: IETF, RFC 9112.
- URL: <https://www.rfc-editor.org/info/rfc9112>
- Supports: message framing, strict ambiguity handling, request smuggling, and
  connection implications.
- Limitation: does not define Apache rewrite configuration or application impact.

## [R11] Cloudflare — BGP leaks and cryptocurrencies

- Source: Cloudflare, April 2018.
- URL: <https://blog.cloudflare.com/bgp-leaks-and-crypto-currencies/>
- Supports: Route 53 prefix redirection, resolver poisoning, false
  `myetherwallet.com` answers, self-signed certificate warning, and later use of
  credentials at the legitimate site.
- Limitation: external incident analysis does not provide complete victim or
  transaction records.

## [R12] RFC 9525 — Service Identity in TLS

- Source: IETF, RFC 9525.
- URL: <https://www.rfc-editor.org/info/rfc9525>
- Supports: application-service reference identities and certificate matching.
- Limitation: identity validation does not prove endpoint integrity or
  transaction intent.

## [R13] CISA — Active exploitation of SolarWinds software

- Source: CISA alert, December 2020.
- URL: <https://www.cisa.gov/news-events/alerts/2020/12/13/active-exploitation-solarwinds-software>
- Supports: affected trusted Orion versions and active exploitation.
- Limitation: initial alert contains less complete post-compromise identity detail.

## [R14] CISA — Ongoing APT activity and systemic recovery risk

- Source: CISA alert, December 2020 / January 2022 revision.
- URL: <https://www.cisa.gov/news-events/alerts/2020/12/23/cisa-releases-cisa-insights-and-creates-webpage-ongoing-apt-cyber-activity>
- Supports: supply-chain compromise, authentication abuse, actor patience, and
  resistance to eviction.
- Limitation: leadership summary, not a complete technical transcript.

## [R15] Microsoft — Recovery from systemic identity compromise

- Source: Microsoft Security, December 2020.
- URL: <https://www.microsoft.com/security/blog/2020/12/21/advice-for-incident-responders-on-recovery-from-systemic-identity-compromises/>
- Supports: malicious SolarWinds code, privilege, SAML signing-certificate theft,
  forged valid assertions, cloud use, and service-principal credentials.
- Limitation: incident-response guidance includes possible and observed paths and
  must not be read as proof every victim experienced all steps.

## [R16] Microsoft — End-to-end Solorigate chain

- Source: Microsoft 365 Defender, December 2020.
- URL: <https://www.microsoft.com/en-us/security/blog/2020/12/28/using-microsoft-365-defender-to-coordinate-protection-against-solorigate/>
- Supports: compromised DLL, credential theft, privilege escalation, SAML trust,
  cloud access, email exfiltration, persistence, and cross-domain correlation.
- Limitation: vendor telemetry and architecture are Microsoft-specific.

## [R17] Cloudflare — Avoid Web Cache Poisoning

- Source: Cloudflare Cache documentation, updated 2026.
- URL: <https://developers.cloudflare.com/cache/cache-security/avoid-web-poisoning/>
- Supports: harmful origin response sharing a cache key with a clean request and
  subsequent multi-user serving.
- Limitation: mitigation documentation, not one disclosed victim incident.

## [R18] Cloudflare — Cache poisoning protection

- Source: Cloudflare Security Blog, August 2018.
- URL: <https://blog.cloudflare.com/cache-poisoning-protection/>
- Supports: shared cache mechanics, practical poisoning class, CDN mitigation,
  and need for origin updates.
- Limitation: does not establish that every cache/origin configuration is
  vulnerable.

## [R19] RFC 9111 — HTTP Caching

- Source: IETF, RFC 9111.
- URL: <https://www.rfc-editor.org/info/rfc9111>
- Supports: cache keys, variants, freshness, persistence, sensitive state, and
  parser-difference poisoning risks.
- Limitation: does not define Agent memory or application-specific caches.

## [R20] NIST CAISI — Strengthening Agent Hijacking Evaluations

- Source: NIST CAISI, January 2025, updated December 2025.
- URL: <https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations>
- Supports: external-data instruction confusion, Tool environments, adaptive
  attacks, task-specific consequence, and repeated-attempt increase from 57% to
  80% in the illustrated test.
- Limitation: bounded to evaluated systems, scenarios, and attack methods.

## [R21] NIST CAISI — Large-scale Agent red-teaming competition

- Source: NIST CAISI Research Blog, March 2026.
- URL: <https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition>
- Supports: active adversarial pressure and continuing hijacking risk for Agents
  processing email, websites, and repositories.
- Limitation: competition results do not define every production Agent.

## [R22] OWASP Agentic Threats Navigator

- Source: OWASP GenAI Security Project.
- URL: <https://genai.owasp.org/resource/owasp-gen-ai-security-project-agentic-threats-navigator/>
- Supports: reasoning, memory, tools, identity, oversight, and multi-Agent attack
  surfaces.
- Limitation: threat-navigation taxonomy, not evidence of one incident.

## [R23] AWS Well-Architected — Idempotent mutating operations

- Source: AWS Well-Architected Framework.
- URL: <https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/rel_prevent_interaction_failure_idempotent.html>
- Supports: difficulty of exactly-once behavior, idempotency tokens, and safe
  retry of mutating operations.
- Limitation: architecture guidance, not proof of one duplicate-effect incident.

## [R24] RFC 9110 — HTTP Semantics

- Source: IETF, RFC 9110.
- URL: <https://www.rfc-editor.org/info/rfc9110>
- Supports: safe/idempotent method semantics and retry conditions.
- Limitation: method semantics do not guarantee exactly-once business effects.

## [R25] NIST CAISI — Cheating on AI Agent Evaluations

- Source: NIST Center for AI Standards and Innovation.
- URL: <https://www.nist.gov/caisi/cheating-ai-agent-evaluations>
- Supports: Agents can exploit gaps between intended tasks, implemented
  affordances, and scorers; transcript and objective validation matter.
- Limitation: not a complete cyber-range or incident-evaluation standard.
