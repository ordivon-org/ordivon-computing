# 04 — IP, NAT, Endpoint, and Path Identity

## IP addresses locate interfaces, not participants

An IP address identifies a network-layer destination or source under one routing
and interface context. It is not a durable identity for a human, Agent, service,
workload, or organization.

The same address can represent:

- an anycast service;
- a load balancer;
- a NAT or carrier-grade NAT;
- a proxy or VPN exit;
- a cloud address reassigned to another workload;
- many containers or tenants;
- one mobile endpoint before migration;
- a temporary IPv6 address.

One workload can also use several addresses simultaneously.

## Source address limits

A source IP observed by a server can mean:

- the client interface;
- the client's NAT;
- a corporate proxy;
- a VPN exit;
- a service-mesh sidecar;
- a cloud egress gateway;
- another relay.

It does not reliably identify the participant or acting Agent.

## NAT state

NAT creates mappings among internal and external addresses and ports. RFC 4787
and RFC 7857 define behavioral requirements for UDP NAT, while RFC 5382 covers
TCP NAT behavior. [R22][R23][R24]

NAT behavior varies in:

- mapping dependence;
- filtering dependence;
- port preservation;
- mapping lifetime;
- hairpinning;
- ICMP handling;
- address pooling;
- endpoint-independent versus endpoint-dependent behavior.

An application cannot infer inbound reachability or mapping persistence from one
outbound send alone.

## NAT is not a security identity layer

NAT can incidentally block unsolicited inbound traffic, but it is not equivalent
to an explicit authorization policy. Existing mappings, port forwarding,
hairpinning, UPnP-like mechanisms, relays, and outbound-initiated channels can
create reachability.

Similarly:

```text
private address
≠ trusted workload
public address
≠ hostile participant
```

## Carrier-grade NAT and attribution

Many subscribers can share one public address. Attribution can require address,
port, protocol, timestamp, provider mapping logs, and clock accuracy. Even then,
the mapping identifies a subscriber path, not the individual actor or process.

## Address family selection

Hosts may have IPv4 and IPv6 addresses with different routing, filtering, DNS,
NAT, VPN, and monitoring. Happy Eyeballs races or sequences connection attempts
to reduce delay when one family is impaired. [R25]

This improves availability but creates observation complexity:

```text
monitor tests IPv4
client wins IPv6 race
→ monitor and client traverse different policy and path
```

An attacker may selectively degrade one family to force fallback to the other.
Fallback must preserve required identity and security properties.

## Interface and policy routing

A laptop or Agent body may have:

- Ethernet;
- Wi-Fi;
- mobile network;
- VPN;
- overlay network;
- container bridge;
- WSL virtual interface;
- proxy configuration.

DNS can use one interface while application traffic uses another. Split tunnels
can send only selected prefixes through a VPN. Source address, route table,
policy rules, and application socket options determine the effective path.

## Anycast and load balancing

Anycast intentionally routes one IP prefix to several sites. Load balancers and
service discovery can select among many bodies. A stable address or TLS identity
therefore does not imply stable process, region, storage replica, or deployment
revision.

This matters for:

- consistency;
- callback routing;
- session affinity;
- incident containment;
- evidence correlation;
- body replacement;
- residual compromise.

## Endpoint rebinding

Network state can change while application identity persists:

```text
NAT mapping expires or changes
mobile interface switches
IPv6 temporary address rotates
QUIC connection migrates
load balancer selects another body
```

The architecture should preserve connection, body, workload, and participant
identity separately.

## Attack chains

### IP allowlist confusion

```text
service trusts source IP range
→ attacker obtains execution through proxy, VPN, cloud tenant, or compromised
  workload inside range
→ network location is treated as participant authorization
```

### Split-tunnel observation gap

```text
Agent believes VPN protects destination
→ routing policy sends some traffic directly
→ monitor observes only tunnel health
→ sensitive traffic exits through local network
```

### Address reuse

```text
cloud address or NAT mapping is reassigned
→ stale allowlist, cache, or identity binding persists
→ new workload inherits access intended for old workload
```

### Selective family degradation

```text
attacker or network blocks preferred IPv6 path
→ client falls back to IPv4 path with different proxy or filtering
→ endpoint identity survives but confidentiality, visibility, or policy changes
```

## Defensive principles

- Use workload and service identity rather than IP as primary authorization.
- Treat IP as conditioned path evidence.
- Make VPN, proxy, interface, route, and address-family decisions observable.
- Define fallback invariants.
- Rotate or invalidate access when addresses or body generations change.
- Correlate CGN attribution with ports and time, while preserving uncertainty.
- Test IPv4 and IPv6 independently.
- Verify split-tunnel policy using destination-specific observations.
- Bind callbacks and inbound services explicitly rather than assuming symmetry.
- Reconcile endpoint identity and final Effect after path change.

## Ordivon implication

World may expose source body, interface, address family, NAT/proxy/VPN relation,
selected endpoint, and path observations. Security evaluates location-based
trust abuse and forced fallback. Host owns required path properties for a Task.
Runtime owns local socket and interface evidence. No global IP identity layer is
admitted.
