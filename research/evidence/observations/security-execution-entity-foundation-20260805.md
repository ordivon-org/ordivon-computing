# Ordivon Security observation — execution-entity foundation — 2026-08-05

This is a bounded cross-project observation. Implementation authority remains in
`ordivon-security`; Ordivon Computing consumes only the research implication.

## Source binding

- repository: `https://github.com/zycxfyh/ordivon-security`
- observed local repository: `/root/projects/ordivon-security`
- revision: `e37cc70dfddc0c7135d4661da7befed57be6e436`
- package version: `0.4.0`
- commit subject: `feat: add local evaluation trial foundation`
- observation date: `2026-08-05`
- observation type: exact local Git revision plus repository documentation and
  tests

## Implemented facts

### Contest profile

The active Security Contest path provides:

- a multi-Actor Scenario manifest;
- actor-specific observations separated from hidden Range truth;
- proposals collected before world mutation;
- explicit admission and fail-closed tick semantics;
- an authoritative Range backend;
- separate Actor, management, sensor, truth, and operational evidence;
- execution identity binding Security, evidence schema, Range, and Actor
  implementations;
- deterministic replay and evidence verification;
- a local MicroContest fixture and pinned CAGE Challenge 4 Range.

The Contest path evaluates independently controlled Actors in an active
adversarial relation. It does not model software lineage, self-replication, or a
population of descendants.

### Evaluation Trial profile

Revision `e37cc70` adds:

- `SampleIdentity`;
- local content-addressed `SampleVault` with digest verification;
- `AuthorityManifest`;
- `GuardianPolicy`;
- `ObservationPlan`;
- `EnvironmentIdentity`;
- `EvaluationSpec`;
- `EvaluationRangeBackend`;
- `Finding`, disposition, and result records;
- separate Sample, management, Observer, Guardian, truth, and operational
  evidence channels;
- mandatory `ResidualClosureReceipt`;
- a deterministic local fixture backend.

The fixture backend explicitly records `sampleExecution: false`. It verifies
Sample staging and exercises admission, identity, failure, destruction,
residual closure, Finding, and evidence semantics without loading or invoking the
Sample as executable code.

### Verified acceptance at the source revision

The source repository records:

- strict type and formatting checks;
- 28 unit and CAGE integration tests passing;
- local dry-run CLI success;
- source and wheel build success;
- clean wheel API and CLI smoke tests;
- Sample bytes absent from generated evidence in the dedicated tests;
- tamper detection, backend-failure closure, oversized-event rejection, and
  residual-closure invalidation.

This observation does not independently recreate all source acceptance logs. It
binds the exact revision whose tests and documents own those claims.

## Current responsibility boundary

The source states that Security owns Evaluation and adversarial semantics, not:

- a hypervisor or container runtime;
- hostile-code isolation;
- antivirus, reverse engineering, fuzzing, EDR, SIEM, or forensics mechanisms;
- Provider or Agent-loop infrastructure;
- generic process or identity systems.

Current Ordivon Runtime is not used to execute unknown software and does not
claim hostile-code isolation.

## Research implication

The implementation now supplies two materially different local profiles:

```text
Evaluation Trial
  one exact Sample and Environment

Contest
  multiple Actors and one contested Range
```

This is sufficient to motivate, but not prove, a broader research question:

- whether both profiles need a compact common Execution Subject identity;
- whether parent-child derivation and authority can remain in existing Host,
  Harness, Runtime, and Artifact relations;
- whether future replication and population studies require new shared records;
- whether Organization and Campaign semantics remain Security-local.

## Facts not established

Revision `e37cc70` does not establish:

- execution of unknown or malicious software;
- static reverse engineering or dynamic malware analysis;
- CAPE, KVM, Windows Guest, Sysmon, Zeek, Suricata, or external sandbox
  integration;
- Agent hijacking evaluation;
- child-Agent creation or revocation;
- lineage reconstruction;
- autonomous replication;
- propagation across nodes;
- malicious Agent population behavior;
- organization, Campaign, or ecological execution;
- one reusable Execution Entity protocol.

## Consuming research

- [`ANC-SECURITY-007`](../../questions/ANC-SECURITY-007-execution-entity-adversarial-ecology.md)
- [`studies/2026-execution-entity-adversarial-ecology/`](../../../studies/2026-execution-entity-adversarial-ecology/)

The observation should be refreshed only after a material Security change to
Evaluation, subject identity, lineage, propagation, or Contest semantics.
