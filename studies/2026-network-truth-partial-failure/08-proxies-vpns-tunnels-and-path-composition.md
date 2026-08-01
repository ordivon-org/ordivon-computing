# 08 — Proxies, VPNs, Tunnels, and Path Composition

## Intermediaries intentionally split paths

Modern applications rarely connect directly from one process to one origin
without intermediaries. A path can include:

```text
application
→ local proxy or sidecar
→ VPN tunnel
→ corporate gateway
→ CDN or edge proxy
→ load balancer
→ service mesh
→ origin service
→ downstream provider
```

Each hop may terminate transport, decrypt traffic, rewrite metadata, resolve
names, authenticate a workload, retry requests, cache responses, or select a new
route.

## Proxy types

### Forward proxy

Acts on behalf of a client toward external destinations.

### Reverse proxy

Acts as the public endpoint for one or more origin services.

### Transparent or interception proxy

Receives traffic without ordinary explicit application proxy configuration,
using network or enterprise mechanisms.

### HTTP CONNECT proxy

Establishes a tunnel to a target, often for TCP and TLS traffic.

### CONNECT-UDP / MASQUE-style proxy

RFC 9298 defines proxying UDP in HTTP, enabling UDP traffic to traverse an HTTP
proxy and supporting uses such as QUIC tunneling. [R32]

### Service-mesh proxy

Mediates service-to-service communication, commonly adding workload identity,
TLS, policy, telemetry, routing, and retries.

## Tunnel semantics

A tunnel encapsulates one network or transport relation inside another. The
outer path and inner path have different:

- endpoints;
- identities;
- addresses;
- routing;
- encryption;
- failure modes;
- observability;
- MTU and fragmentation behavior.

```text
outer tunnel connected
≠ inner destination reachable
≠ application Effect complete
```

## VPN scope

A VPN can route:

- all traffic;
- selected prefixes;
- selected applications;
- one address family;
- DNS only or not DNS;
- traffic except local LAN;
- traffic under platform-specific policy.

A UI status of `connected` proves neither that every intended flow uses the
tunnel nor that the exit path reaches the expected service.

## Name resolution and proxying

Depending on protocol and configuration, the client or proxy may resolve the
destination name. This changes:

- which DNS view applies;
- whether local observers see the name;
- whether private zones resolve;
- whether DNSSEC validation occurs;
- which address the TLS reference identity is associated with;
- whether the proxy can redirect to an unexpected endpoint.

Evidence should record where resolution occurred.

## TLS through intermediaries

### End-to-end tunnel

The proxy carries encrypted bytes and the client authenticates the origin.

### TLS termination

The proxy authenticates to the client and creates another channel to the origin.
The proxy becomes a plaintext endpoint and trust authority.

### Enterprise interception

A managed trust root can allow an inspection proxy to issue certificates
accepted by the client. Cryptographic validation succeeds under enterprise
policy, but end-to-origin confidentiality no longer exists.

## Metadata inheritance

Proxies add forwarding fields, client identity, trace context, route metadata,
and authorization claims. R2 showed that duplicate and precedence rules matter.
R3 adds that trust depends on authenticated hop identity and tunnel topology.

## Service mesh

A service mesh can provide mTLS, workload identity, routing, policy, telemetry,
retry, timeout, and circuit-breaking. It can also:

- centralize failure;
- duplicate application retry behavior;
- obscure direct endpoint evidence;
- widen compromise through control-plane authority;
- preserve stale configuration;
- create two TLS connections rather than one end-to-end channel;
- make sidecar identity appear equivalent to application intent.

The mesh proves workload-channel properties, not participant Task alignment.

## Overlay and underlay

An overlay network can report healthy logical connectivity while the underlay
experiences congestion, route anomalies, or interception. Conversely, underlay
reachability does not prove overlay authorization or key state.

## Attack chains

### Split-tunnel leakage

```text
VPN connected
→ destination not covered by tunnel policy or address-family rule
→ application sends directly
→ monitor checks only tunnel health
→ confidentiality or location requirement fails
```

### Proxy destination confusion

```text
client authorizes proxy or dynamic endpoint
→ proxy resolves or rewrites destination differently
→ TLS identity or application routing is weakly bound
→ traffic reaches attacker-controlled endpoint
```

### Mesh retry duplication

```text
application retries state-changing request
+ mesh independently retries
→ several attempts share no stable Effect identity
→ duplicate commits
```

### Control-plane compromise

```text
mesh, VPN, or proxy control plane compromised
→ routes, certificates, policy, or telemetry are changed
→ data plane continues showing encrypted healthy channels
→ attacker inherits trusted infrastructure
```

### Observer blind spot

```text
central monitor observes outer tunnel
→ inner proxy or downstream provider changes endpoint
→ application Effect differs
→ monitor reports path healthy
```

## Defensive principles

- Enumerate every intermediary and termination boundary.
- Bind DNS resolution location, target identity, proxy identity, and final
  service identity.
- Verify destination-specific VPN and split-tunnel behavior.
- Keep outer and inner path evidence separate.
- Avoid duplicate retry layers or preserve one stable Effect identity across
  them.
- Authenticate trusted proxy metadata and strip untrusted copies.
- Protect and independently monitor control planes.
- Preserve a direct provider or endpoint verifier for high-value Effects.
- Test IPv4, IPv6, QUIC, TCP, DNS, and fallback paths through the actual tunnel.
- Treat `connected` as transport state, not Task completion.

## Ordivon implication

World-native adapters may expose intermediary topology, resolution location,
termination, tunnel, route, and provider facts. Host owns path requirements and
Effect semantics. Security evaluates compromised infrastructure, forced path
changes, and deceptive health. Runtime owns local proxy/VPN processes and
configuration evidence. Ordivon should not create a universal proxy or VPN.
