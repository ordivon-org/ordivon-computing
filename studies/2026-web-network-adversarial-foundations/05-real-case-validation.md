# 05 — Real-Case Validation

## Method

These cases validate the R0 distinctions against standards and official reports.
They intentionally omit payloads, exploit construction, vulnerable endpoint
syntax, and operational reproduction steps.

Public evidence is incomplete. Each case supports a bounded causal account, not
a complete reconstruction of every actor decision.

## Case A — HTTP parser disagreement

### Claim boundary

RFC 9112 establishes a structural class of failure: lenient parsing and unique
interpretations among multiple recipients can create request-smuggling
vulnerabilities. [R12]

### Graph

```text
intermediary compatibility and robustness
→ tolerance for non-canonical messages
→ two recipients interpret framing differently
→ front policy and downstream execution apply to different logical requests
→ hidden downstream request primitive
→ possible composition with cache, identity, routing, or internal services
```

### Why this case matters

- the indispensable property is heterogeneous intermediary composition;
- the weakness is semantic disagreement, not merely one dangerous byte string;
- the relevant evidence includes what every recipient parsed;
- a front-layer allow decision does not prove downstream semantics;
- an adaptive Agent could search parser differentials, but the underlying failure
  remains classical.

### Defensive breakpoints

Canonical parsing, rejection of ambiguity, aligned framing semantics, end-to-end
conformance testing, and component-specific observation remove graph edges
without deleting HTTP intermediation.

## Case B — Log4Shell followed by persistence and movement

### Claim boundary

CISA and the FBI reported an incident in which actors exploited Log4Shell in an
unpatched VMware Horizon server, installed a cryptocurrency miner, moved to a
domain controller, compromised credentials, and installed reverse proxies on
several hosts to maintain access. [R15]

### Graph

```text
application logging and dynamic lookup behavior
→ remotely reachable vulnerable service
→ code-execution primitive under service identity
→ host and domain discovery
→ credential compromise
→ lateral movement
→ additional persistence paths
→ continuing access beyond the initial vulnerable request
```

### R0 lessons

- the CVE was an entry edge, not the Campaign;
- egress and identity determined what the primitive could become;
- patching the initial service could not revoke already compromised credentials
  or remove established persistence;
- defender closure required host, identity, network, and residual evidence;
- World must expose native facts, while Security interprets their Campaign value.

## Case C — Exchange vulnerability chaining

### Claim boundary

Microsoft reported limited targeted attacks chaining an authenticated Exchange
SSRF vulnerability with an Exchange PowerShell remote-code-execution
vulnerability. Observed post-exploitation included a web shell, Active Directory
reconnaissance, and data exfiltration. [R16]

### Graph

```text
valid standard-user identity
+ reachable Exchange surface
+ server-side request primitive
+ downstream code-execution condition
→ execution under a high-value service context
→ persistent web shell
→ directory reconnaissance
→ collection and exfiltration
```

### R0 lessons

- authentication was a precondition, not proof of benign intent;
- two vulnerabilities formed a more valuable route than either label alone;
- the high strategic value came partly from Exchange's position and authority;
- intended administrative mechanisms and valid identity can participate in an
  attack chain;
- detection needed post-exploitation behavior, not only exploit signatures.

## Case D — SolarWinds supply-chain compromise

### Claim boundary

CISA described compromise of the SolarWinds Orion software supply chain together
with widespread abuse of commonly used authentication mechanisms, and warned
that the actor could resist eviction and preserve risk after initial discovery.
[R17]

### Graph

```text
trusted software composition and update distribution
→ compromised production or distribution trust
→ customers install apparently legitimate software
→ code executes through expected deployment paths
→ existing identities and authentication mechanisms are abused
→ long-lived access and difficult eviction
```

### R0 lessons

- the attack inherited trust instead of bypassing every perimeter control;
- signatures and approved deployment channels can faithfully distribute a
  compromised artifact;
- supply-chain provenance includes production process and authority, not only a
  package digest;
- recovery requires identity, build, deployment, and environment reconstruction;
- Agent-generated Tool supply chains inherit the same classical problem at
  higher speed and runtime dynamism.

## Case E — Agent hijacking

### Claim boundary

NIST describes Agent hijacking as indirect prompt injection in which malicious
instructions are placed in external data such as email, files, or websites and
cause an Agent to pursue an unintended task. Its evaluations included simulated
arbitrary code execution, data exfiltration, and automated phishing scenarios,
and found that adaptive and repeated testing materially changed measured attack
success. [R13]

### Graph

```text
Agent must ingest external task-relevant data
→ trusted instruction and untrusted data share one model-visible representation
→ malicious data influences action selection
→ Agent uses legitimate Tools and identity
→ unintended world Effect
→ possible persistence through memory, generated Tools, or downstream messages
```

### R0 lessons

- the initial weakness is semantic trust separation, not necessarily memory
  corruption or a protocol bug;
- the dangerous primitive comes from the Agent's legitimate Tool and identity;
- prompt filtering alone cannot prove the final world outcome;
- repeated probabilistic attempts and system-specific attack adaptation matter;
- defensive evaluation must bind affordances, World scope, and cumulative
  success, not only model text.

## Cross-case comparison

| Case | Initial source | Primitive | High-value join | Residual concern |
|---|---|---|---|---|
| HTTP parser disagreement | semantic differential | hidden downstream request | cache, identity, route, internal service | intermediary state and ambiguous logs |
| Log4Shell incident | vulnerable dynamic lookup | service-context execution | credentials and domain position | proxies, credentials, host persistence |
| Exchange chain | identity plus two vulnerabilities | service execution | Exchange/AD position | web shell, data access, credentials |
| SolarWinds | compromised trusted production path | legitimate code execution | distribution and authentication trust | identity and environment reconstruction |
| Agent hijacking | untrusted data in action loop | legitimate Tool use | user identity, memory, generated Tools | durable state and propagated instructions |

## Validation result

The grammar classifies all five cases without equating:

- affordance with weakness;
- weakness with concrete vulnerability;
- vulnerability with primitive;
- primitive with objective;
- patch with eradication;
- model output with world truth.

The cases also show that no single universal identifier or central World journal
is required for analysis. Native component identities plus explicit causal and
evidence bindings remain sufficient at R0.
