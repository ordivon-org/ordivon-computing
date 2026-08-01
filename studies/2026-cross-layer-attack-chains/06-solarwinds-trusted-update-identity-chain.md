# 06 — SolarWinds/Solorigate: Trusted Update to Systemic Identity Compromise

## Evidence boundary

CISA reported active exploitation of compromised SolarWinds Orion software
updates and later described the event as a supply-chain compromise combined with
widespread abuse of common authentication mechanisms. CISA emphasized that the
actor could resist eviction and continue to put affected organizations at risk.
[R13][R14]

Microsoft's incident-response guidance describes a chain from malicious
SolarWinds code to elevated credentials, access to a trusted SAML token-signing
certificate, forged SAML tokens impersonating privileged users, and illegitimate
credentials added to application service principals. [R15]

Microsoft's Solorigate analysis further links the compromised DLL to remote
control, credential theft, privilege escalation, SAML token creation, cloud
access, email exfiltration, and persistence. [R16]

## Causal graph

```text
A1 trusted software build and update distribution
→ T1 customers must execute vendor-signed maintenance software at scale
→ V1 build/distribution chain inserts malicious code into legitimate update
→ P1 malicious component executes under trusted Orion deployment
→ I1 inherits server identity, network reach, credentials, and monitoring trust
→ C1 privilege escalation and lateral movement
→ I2 access to SAML signing key or federation trust
→ P2 create assertions accepted as valid by relying parties
→ C2 impersonate privileged users and access cloud resources
→ C3 add persistent application credentials / exfiltrate data
→ O1 cross-domain systemic identity compromise
→ D1 endpoint, identity, and cloud correlation
→ R1 rebuild, rotate signing keys and credentials, restore trust
→ X1 unknown scope, forged Tokens, app credentials, cloud persistence
```

## Signed software was an attack amplifier

Code signing and trusted distribution normally provide integrity and origin
assurance. In this case, compromise occurred before or inside the trusted
production path, so downstream verification could correctly accept the artifact.

```text
valid signature
→ artifact came through the trusted signing process
≠ artifact serves the vendor/customer's intended purpose
```

The attacker inherited:

- trusted publisher reputation;
- broad customer deployment;
- privileged service execution;
- network management reach;
- reduced suspicion in monitoring systems.

## The Campaign moved across authority domains

Patching or removing the malicious DLL addressed the first foothold. The actor
could already have moved into:

- privileged accounts;
- federation infrastructure;
- SAML signing keys;
- cloud sessions;
- service-principal credentials;
- mail and API access;
- other hosts.

This is a textbook `persists-through` edge:

```text
initial product compromise removed
but
identity compromise remains independently usable
```

## Valid SAML as adversarial authority

Once the signing key or federation trust is compromised, forged assertions can
be cryptographically valid to relying parties.

```text
signature validation succeeds
→ assertion was signed by trusted key
≠ legitimate identity provider issued it for a legitimate actor
```

Detection must therefore include behavior, issuance context, key custody, and
cross-domain identity evidence—not only signature correctness.

## Service-principal persistence

Adding credentials to an existing application identity creates a durable path
that can survive user password resets and endpoint remediation. It also blends
with legitimate API activity.

## Defensive breakpoints

### B1 — secure and attest build/signing systems

Separate source, build, signing, and release authority; monitor unexpected build
changes and protect signing keys.

### B2 — reduce management-plane privilege

Network-management products should not automatically possess unrestricted
identity and cloud reach.

### B3 — monitor identity-system changes

Detect signing-key access, federation trust changes, anomalous SAML assertions,
and new application credentials.

### B4 — separate management and evidence planes

A compromised management product should not control all logs and incident
signals.

### B5 — cross-domain correlation

Join endpoint, identity, cloud, application, and network evidence.

### B6 — reconstruction over uncertain cleaning

When systemic trust is lost, rebuild affected infrastructure and rotate trust
roots rather than relying on local malware removal.

## Recovery and residual closure

CISA and Microsoft guidance imply a recovery scope larger than software update:

- isolate and rebuild affected systems;
- rotate privileged credentials;
- replace SAML signing certificates and federation trust where affected;
- invalidate sessions and Tokens;
- remove illegitimate application credentials;
- review cloud and mail activity;
- establish clean management and evidence planes;
- preserve uncertainty until scope is independently established.

## Ordivon lesson

This case supports Ordivon's high-recoverability principle: code can be rebuilt,
but trust roots, identities, and external Effects need explicit rotation and
verification. Security owns Campaign synthesis; World/provider adapters expose
native identity/cloud facts; Host owns Task and Effect meaning; Runtime owns
local body evidence. No universal supply-chain or identity platform is earned.
