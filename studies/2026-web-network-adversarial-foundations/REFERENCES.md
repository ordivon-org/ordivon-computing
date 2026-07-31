# References

Primary and official sources are preferred. Each entry states what it supports
and what it does not establish for Ordivon.

## [R01] MITRE CWE — Introduction to Vulnerability Theory

- Source: MITRE CWE, “Introduction to Vulnerability Theory.”
- URL: <https://cwe.mitre.org/documents/vulnerability_theory/intro.html>
- Supports: distinction between weakness and concrete vulnerability; one
  vulnerability can arise from related weaknesses.
- Limitation: a conceptual taxonomy does not provide complete incident or
  Campaign evidence.

## [R02] NIST CSRC — Vulnerability glossary

- Source: NIST Computer Security Resource Center, “vulnerability.”
- URL: <https://csrc.nist.gov/glossary/term/vulnerability>
- Supports: a vulnerability can be a weakness or condition that enables a threat
  event or violates intended security policy.
- Limitation: NIST aggregates several source definitions; the exact source must
  be selected for formal use.

## [R03] MITRE CWE — Vulnerability theory control sphere

- Source: MITRE CWE, “Introduction to Vulnerability Theory.”
- URL: <https://cwe.mitre.org/documents/vulnerability_theory/intro.html>
- Supports: a vulnerability permits access to resources or behavior outside an
  actor's intended control sphere.
- Limitation: does not model adaptive adversary objectives or organizational
  impact.

## [R04] MITRE CWE — Chains and Composites

- Source: MITRE CWE, “Chains and Composites.”
- URL: <https://cwe.mitre.org/data/reports/chains_and_composites.html>
- Supports: chains connect weaknesses causally; composites require multiple
  weaknesses; chains can branch or exceed two steps.
- Limitation: describes software weakness structure, not a complete adversary
  Campaign.

## [R05] MITRE ATT&CK — Enterprise tactics

- Source: MITRE ATT&CK, “Enterprise Tactics.”
- URL: <https://attack.mitre.org/tactics/enterprise/>
- Supports: tactics describe the adversary's reason for acting; current
  Enterprise ATT&CK organizes fifteen tactical goals.
- Limitation: tactics are not vulnerability causes, one mandatory sequence, or a
  strategic optimization model.

## [R06] MITRE ATT&CK — April 2026 updates

- Source: MITRE ATT&CK, “Updates — April 2026.”
- URL: <https://attack.mitre.org/resources/updates/>
- Supports: ATT&CK v19 is the current release and split the former Defense
  Evasion area into Stealth and Defense Impairment.
- Limitation: taxonomy evolution does not itself establish an Ordivon schema.

## [R07] NIST CSRC — Threat event glossary

- Source: NIST Computer Security Resource Center, “threat event.”
- URL: <https://csrc.nist.gov/glossary/term/threat_event>
- Supports: a threat event is an event or situation with potential undesirable
  consequence.
- Limitation: does not identify which threat event occurred in one incident.

## [R08] NIST CSRC — Threat-event outcome glossary

- Source: NIST Computer Security Resource Center, “threat event outcome.”
- URL: <https://csrc.nist.gov/glossary/term/threat_event_outcome>
- Supports: outcome is the effect of a threat acting upon a vulnerability.
- Limitation: CIA-focused definitions do not exhaust strategic, information, or
  evaluator-integrity outcomes.

## [R09] FIRST — CVSS v4.0 User Guide

- Source: FIRST, “CVSS v4.0 User Guide.”
- URL: <https://www.first.org/cvss/v4.0/user-guide>
- Supports: CVSS communicates vulnerability characteristics and severity; the
  Base score measures severity, not risk; Threat and Environmental metrics add
  time- and deployment-specific information.
- Limitation: CVSS is not a Campaign, incident-closure, or business-risk model.

## [R10] NIST CSRC — Risk glossary

- Source: NIST Computer Security Resource Center, “risk.”
- URL: <https://csrc.nist.gov/glossary/term/risk>
- Supports: risk is commonly a function of likelihood and adverse impact.
- Limitation: the glossary does not prescribe one complete local prioritization
  method.

## [R11] NIST CSRC — Mitigation glossary

- Source: NIST Computer Security Resource Center, “mitigation.”
- URL: <https://csrc.nist.gov/glossary/term/mitigation>
- Supports: mitigation reduces risk, likelihood, or impact and can be temporary.
- Limitation: mitigation is not proof of eradication or residual closure.

## [R12] RFC 9112 — HTTP/1.1

- Source: IETF HTTP Working Group, “RFC 9112: HTTP/1.1.”
- URL: <https://www.rfc-editor.org/rfc/rfc9112.html>
- Supports: lenient parsing and differing recipient interpretations can cause
  request-smuggling vulnerabilities; framing requirements reduce ambiguity.
- Limitation: the RFC defines protocol behavior, not every implementation or
  deployment-specific attack path.

## [R13] NIST CAISI — Strengthening AI Agent Hijacking Evaluations

- Source: NIST Center for AI Standards and Innovation, “Strengthening AI Agent
  Hijacking Evaluations,” January 17, 2025, updated December 19, 2025.
- URL: <https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations>
- Supports: indirect prompt injection exploits weak separation between trusted
  instruction and untrusted data; adaptive attacks and repeated attempts can
  materially change measured success; simulated consequences included code
  execution, exfiltration, and phishing.
- Limitation: reported success rates characterize the evaluated models,
  scenarios, and attack methods, not all Agent systems.

## [R14] NIST CAISI — Cheating on AI Agent Evaluations

- Source: NIST Center for AI Standards and Innovation, “Cheating On AI Agent
  Evaluations.”
- URL: <https://www.nist.gov/caisi/cheating-ai-agent-evaluations>
- Supports: evaluator loopholes can produce apparent task success without the
  intended capability; transcript review and explicit affordance rules improve
  validity.
- Limitation: examples do not form a universal evaluator-integrity protocol.

## [R15] CISA/FBI — Log4Shell incident response advisory

- Source: CISA and FBI, “Iranian Government-Sponsored APT Actors Compromise
  Federal Network, Deploy Crypto Miner, Credential Harvester,” AA22-320A.
- URL: <https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-320a>
- Supports: observed exploitation of Log4Shell in VMware Horizon followed by
  mining, movement to a domain controller, credential compromise, and reverse
  proxies for persistence.
- Limitation: the public advisory is a bounded incident account and does not
  expose every decision or causal counterfactual.

## [R16] Microsoft Threat Intelligence — Exchange vulnerability chain

- Source: Microsoft Threat Intelligence, “Analyzing attacks using the Exchange
  vulnerabilities CVE-2022-41040 and CVE-2022-41082.”
- URL: <https://www.microsoft.com/en-us/security/blog/2022/09/30/analyzing-attacks-using-the-exchange-vulnerabilities-cve-2022-41040-and-cve-2022-41082/>
- Supports: observed chaining of authenticated SSRF and PowerShell RCE followed
  by a web shell, Active Directory reconnaissance, and exfiltration.
- Limitation: describes a small observed campaign set and vendor-visible
  telemetry, not every possible exploitation path.

## [R17] CISA — SolarWinds supply-chain compromise

- Source: CISA, “CISA Releases CISA Insights and Creates Webpage on Ongoing APT
  Cyber Activity,” December 23, 2020.
- URL: <https://www.cisa.gov/news-events/alerts/2020/12/23/cisa-releases-cisa-insights-and-creates-webpage-ongoing-apt-cyber-activity>
- Supports: compromise of the SolarWinds Orion software supply chain, widespread
  abuse of authentication mechanisms, and risk of persistent access resistant to
  eviction.
- Limitation: the alert summarizes a broad investigation and should be combined
  with more specific evidence for detailed forensic claims.

## [R18] NIST — Security considerations for AI agents

- Source: NIST Trustworthy and Responsible AI 800-5, “Summary Analysis of
  Responses to the Request for Information Regarding Security Considerations for
  AI Agents,” May 18, 2026.
- URL: <https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai>
- Supports: respondents broadly agreed that classical cybersecurity remains
  relevant but requires adaptation for Agent security and that novel Agent
  threats impede adoption.
- Limitation: an RFI response synthesis records stakeholder views; it is not a
  validated architecture or control standard.

## [R19] OWASP — Agentic Threats Navigator

- Source: OWASP GenAI Security Project, “Agentic Threats Navigator.”
- URL: <https://genai.owasp.org/resource/owasp-gen-ai-security-project-agentic-threats-navigator/>
- Supports: Agent attack surfaces include reasoning, memory, Tools, identity,
  human oversight, and multi-Agent interactions.
- Limitation: a threat navigator organizes concerns; it does not establish
  causal completeness or prove a new Ordivon layer.
