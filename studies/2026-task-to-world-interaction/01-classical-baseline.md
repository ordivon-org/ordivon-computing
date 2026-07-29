# 01 — Classical Baseline and Insertion Seam

## Mature execution mechanisms

- OS processes, filesystems, namespaces, cgroups and permissions;
- containers, VMs, microVMs, browsers, functions, devices and Sandboxes;
- schedulers, provider control planes, snapshots, operation polling and quotas;
- durable workflow activities, retry, timers, signals and callbacks;
- queues, object stores, databases and transactional systems.

## Mature connectivity mechanisms

- DNS, discovery, endpoints, IP, TCP, UDP, QUIC and HTTP;
- VPNs, proxies, CNI, overlays, service meshes and load balancers;
- PKI, workload identity, OAuth and provider credentials;
- retries, failover, health checks, tracing and network telemetry;
- network namespaces, traffic control and simulation.

## Mature evidence mechanisms

- provider operation IDs and audit logs;
- OpenTelemetry traces and links;
- W3C-PROV-style entity/activity/agent provenance;
- content digests, signed Artifacts and immutable event journals.

## Candidate seam

The candidate World seam exists only if these systems plus direct Host adapters
still fail to preserve:

- the distinction among semantic Effect, Dispatch, delivery and provider
  execution;
- unknown world outcomes before retry;
- path/provider/identity-conditioned evidence;
- exact invalidation after external changes;
- Task continuation across combined path, provider and participant replacement;
- remote-to-remote work without central data proxying.

## Strong-baseline experiment

For every World abstraction, implement or measure the strongest simpler route:

```text
Host
+ direct provider SDK or Tool
+ direct network/identity observation
+ workflow engine or queue where appropriate
+ tracing/provenance
```

World is admitted only when it prevents a repeated real failure or removes
material duplicated recovery logic across two workloads.
