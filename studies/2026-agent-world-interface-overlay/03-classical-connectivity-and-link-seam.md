# 03 — Classical Connectivity Stack and the Link Seam

## Classical layers

```text
physical link
→ IP and transport
→ tunnel, overlay, proxy, CNI, virtual interface
→ DNS, discovery, endpoint and workload identity
→ firewall, policy, service mesh, load balancer
→ telemetry, health, route control and failover
→ application protocol and Task relationship
```

The lower layers already own byte delivery, route mutation, identity proof,
policy enforcement, retry, failover, telemetry, and traffic shaping. Link must
not rebuild them.

## Structural gap candidate

Classical networking normally serves a declared application graph. An open Task
may discover new data sources, services, Agents, devices, and humans during
work. The Task must express why the relation exists, what identity and evidence
it requires, and how path or participant changes affect prior observations and
pending work.

## Semantic separations

```text
logical relationship ≠ physical path ≠ communication identity
reachability ≠ authority
transport success ≠ Effect satisfaction
same URL ≠ same observation conditions
path failover ≠ evidence equivalence
endpoint replacement ≠ participant continuity
connection loss ≠ work relationship deletion
```

## Candidate Link seam

The narrow seam is not packet transport. It is:

- deriving a connectivity requirement from current work;
- publishing versioned and expiring path/identity observations;
- binding one logical relation to one exact path and identity condition;
- preserving path-conditioned provenance;
- invalidating dependent claims after change;
- reconciling uncertain delivery and reply;
- continuing or handing off relationships across path and participant
  replacement.

## Current evidence

The observation chain already produces useful path and service facts. The
private VPN tools demonstrate explicit isolated egress. The reference transport
proves bounded framing and identity experiments. Network World demonstrates
deterministic modeled conditions and independent events.

The missing evidence is Task-level connectivity binding, invalidation, and
recovery under real Host workloads.
