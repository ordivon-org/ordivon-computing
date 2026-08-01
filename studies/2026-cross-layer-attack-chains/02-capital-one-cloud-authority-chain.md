# 02 — Capital One: Web Intermediary to Cloud Authority

## Evidence boundary

The 2019 DOJ complaint states that a firewall misconfiguration permitted commands
to reach and execute on a server, that one command obtained security credentials
for a cloud WAF role, and that the role was used to list and copy data from cloud
storage for which it had permissions. Capital One logs corroborated role use and
bucket operations. [R04]

The later DOJ conviction record states that the actor used a self-built scanning
tool to find misconfigured cloud accounts and stole data from more than 30
entities. [R05]

The OCC later found failures in effective risk assessment before major public-
cloud migration and failure to correct deficiencies in a timely manner. [R06]

R4 does not reproduce the commands contained in the court filing.

## Causal graph

```text
A1 public Web application / WAF capability
→ T1 intermediary must reach application and cloud services
→ W1 hazardous firewall/proxy configuration
→ V1 attacker-controlled commands reach server-side execution path
→ P1 server-side request or command primitive
→ I1 cloud WAF role credentials obtained
→ I2 role grants access to selected storage resources
→ C1 storage enumeration
→ C2 data copy/extraction
→ O1 large-scale confidentiality loss
→ D1 external disclosure and log correlation
→ R1 containment, notification, policy review
→ X1 copied data, similar misconfigurations, role-policy and governance residual
```

## Indispensable affordance

MITRE classifies SSRF as a weakness in which a server retrieves an unintended
resource because upstream input insufficiently constrains the destination. The
security significance comes from the server's own network position and authority,
not merely from URL parsing. [R01]

The cloud role existed to let the Web infrastructure access required cloud
resources without hardcoded long-lived credentials. This is a sound capability
pattern when the workload identity and permissions are narrow.

The structural tension was:

```text
application needs local cloud credentials and network reach
vs.
untrusted external requests must not inherit that reach
```

## The first primitive was not the objective

Reaching the server or inducing a server-side operation was only P1. The major
impact required:

- access to workload credentials;
- role permissions broad enough to enumerate or copy relevant storage;
- external execution and data transfer;
- insufficient early anomaly detection;
- persistence of copied data outside the account.

## Cloud identity amplification

The role converted one Web-layer weakness into cloud API authority:

```text
attacker does not need direct storage credentials initially
→ vulnerable intermediary acts from trusted cloud position
→ workload role provides temporary valid credentials
→ storage APIs correctly authorize permitted actions
```

The APIs were not necessarily bypassed. Their authorization was inherited.

## IMDS defense-in-depth

AWS introduced IMDSv2 as a session-oriented metadata protocol designed to add
defense in depth against SSRF, open firewalls, and reverse proxies. It requires a
session-creation request and a secret token bound to the instance; AWS recommends
requiring IMDSv2 and supports disabling metadata access entirely. [R02][R03]

This cuts many—but not all—paths:

```text
simple URL-only server-side fetch
→ cannot complete token acquisition/use sequence
```

It does not replace:

- application input validation;
- outbound destination control;
- least-privilege IAM;
- process isolation;
- storage policy;
- anomaly detection;
- data-classification and recovery.

A sufficiently capable server-side primitive that controls method, headers, and
multi-step state can defeat weaker assumptions. AWS explicitly frames IMDSv2 as
defense in depth, not a universal cure. [R02]

## Defensive breakpoints

### B1 — eliminate or constrain server-side destination selection

Prevent untrusted input from becoming arbitrary server-side network or command
targets.

### B2 — require hardened metadata protocol or disable metadata

Use IMDSv2-only or disable IMDS when the workload does not need it.

### B3 — narrow the role

The WAF or application role should access only exact resources and actions
required by its Task.

### B4 — separate read/list/copy authority

Enumeration and bulk extraction should not be ambient consequences of a generic
front-end role.

### B5 — detect behavior, not only credential validity

A valid role performing unusual list, sync, region, source, or volume patterns is
still suspicious.

### B6 — independent storage evidence

Provider object and audit logs must establish what was accessed and copied.

## Recovery and residual closure

Patching the WAF or changing one firewall rule does not close:

- issued credentials or sessions;
- copied data;
- alternate misconfigured accounts;
- overly broad IAM policies;
- automation built around the same role;
- unreviewed public cloud migration assumptions.

Closure requires role and policy review, credential invalidation, storage audit,
similar-system discovery, log retention, and external data-impact assessment.

## Ordivon lesson

Host should bind an external Effect to a narrow provider action. World/provider
adapters should expose native role, request, Receipt, and object observations.
Security should reconstruct the chain. Runtime should not own cloud IAM policy.
No generic Ordivon SSRF proxy or cloud-security platform is earned by this case.
