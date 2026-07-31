# 06 — Workload, Agent, and Generated-Tool Identity

## Human sessions are not enough

Agent systems contain several non-human actors:

- Host service;
- model or model session;
- Harness run;
- Runtime Job;
- browser worker or extension;
- cloud function, container, VM, or remote body;
- Tool or Adapter;
- generated one-use Tool;
- provider service;
- delegated specialist Agent.

Assigning every action directly to the human user hides which system component
actually selected and executed it.

## Workload identity

SPIFFE defines standards for securely identifying software systems in dynamic
and heterogeneous environments. It uses short-lived cryptographic identity
documents and workload APIs so workloads can mutually authenticate independent
of static network location. [R16]

The classical lesson is important for Ordivon:

```text
IP address or machine location
≠ durable workload identity
```

A body can move while identity is reissued under attested policy. Conversely, a
stable hostname can serve a different workload generation.

## Identity dimensions

A useful Agent trace may need separate identities for:

```text
Participant
  owns purpose, resources, and commitments

Agent Actor
  strategic or application-level acting role

Model Session
  one probabilistic cognition episode

Host Run / Harness Run
  one orchestration and policy configuration

Runtime Attempt / Job
  one concrete local execution

Body / Workload generation
  one process, container, VM, browser, or provider instance

Tool revision
  one executable capability implementation

Credential or token family
  one revocable authority path

Effect
  one stable intended world observation or change
```

One global Agent ID cannot replace these relations without creating false
continuity.

## Authentication is not authorization

A workload identity proves that a current workload satisfied issuance or
attestation policy. It does not automatically determine:

- which participant it represents;
- which Task it may serve;
- which external resources it may access;
- which Tools it may create;
- whether it may delegate;
- which consequences are allowed;
- whether its current behavior remains aligned with the original purpose.

## Agent identity

An Agent Actor may persist semantically across model, process, Host, or body
replacement, but that persistence must not imply that old bearer authority,
memory, or trust automatically transfers.

A replacement requires explicit relations:

```text
same Task or Campaign role
new model/session identity
new Host/Harness configuration
new body generation
new or reissued credentials
retained and invalidated evidence
current delegation and consequence scope
```

## Generated Tool identity

When an Agent constructs a Tool, the Tool is initially an Artifact, not an
implicitly trusted capability.

Minimum provenance:

```text
capability requirement
requesting Task and Agent
source inputs and generator revision
Workspace and build environment
dependencies and fetched origins
source and binary digests
tests and verifier
requested identities, paths, and resources
admitted scope and lifetime
actual executions and Effects
retirement or revocation condition
```

A generated Tool can be benign code used adversarially, malicious code produced
by hijacked Context, or flawed code produced by an honest Agent. Intent labels do
not replace evidence.

## Tool authority patterns

### Inherited ambient authority

The Tool runs inside a process that already contains browser sessions, cloud
credentials, filesystem access, or network reachability.

### Explicit delegated authority

The Tool receives a narrow token or capability for one resource and action.

### Brokered authority

The Tool submits a structured Effect to a separate component that enforces
current Task, participant, and consequence policy.

### Self-acquired authority

The Tool discovers local credentials, authenticates interactively, or creates a
new service identity. This changes the authority graph and must be observed.

## Agent delegation

An Agent can delegate to another Agent, service, Tool, or body. The receiving
actor needs enough context and authority to perform the assignment, but copying
all parent credentials and Context maximizes propagation risk.

A narrow delegation should bind:

```text
parent participant and actor
child actor or workload
Task or subtask
resource and action
budget and deadline
allowed Tool construction
allowed onward delegation
result and evidence return path
revocation and expiry
```

Existing OAuth token exchange and fine-grained authorization can express parts
of this; Host Task semantics and World bindings express other parts. No new
universal delegation object is earned by R1 alone.

## Credential continuity and body replacement

Credentials should not silently survive body destruction unless an owning
identity system intentionally preserves them. The architecture should distinguish:

- body-local ephemeral key;
- workload identity reissued to a new generation;
- long-lived service credential;
- user session;
- delegated access token;
- refresh or renewal authority;
- external provider API key.

Destroying one body does not prove that externally stored credentials or tokens
were revoked.

## Attack chains

### Hijacked Tool construction

```text
external data influences Agent
→ Agent identifies a plausible capability gap
→ generated Tool includes unintended behavior or dependency
→ Tool inherits broad Runtime or browser authority
→ world Effect occurs under legitimate identity
```

### Identity laundering through delegation

```text
compromised Agent delegates to benign-looking specialist
→ downstream service logs specialist or user only
→ original decision actor disappears
→ malicious sequence appears legitimate
```

### Body replacement with stale authority

```text
old body compromised
→ replacement body starts
→ shared long-lived credentials remain valid
→ attacker continues outside the replaced body
```

### Tool supply-chain inheritance

```text
Agent searches for dependency at runtime
→ dependency source or package is compromised
→ build succeeds and receives Tool authority
→ trusted Task executes untrusted capability
```

## Defensive principles

- Use first-class workload identity rather than network location where mature
  mechanisms fit.
- Keep participant, Agent, session, run, body, Tool, credential, and Effect
  identities distinct.
- Prefer short-lived, audience- and action-restricted delegated authority.
- Record onward delegation and actor chains.
- Build and test generated Tools in disposable environments before granting
  external authority.
- Separate Tool construction from Tool admission.
- Avoid placing general-purpose Agent code in environments with broad ambient
  credentials.
- Destroy or rotate body-local authority with body generations.
- Verify residual external tokens and identities after teardown.

## Ordivon implication

Runtime owns build and process truth. World owns externally realized Tool,
workload, identity, path, and provider facts. Host owns Task and delegation
meaning. Security owns adversarial interpretation and Campaign outcome.
