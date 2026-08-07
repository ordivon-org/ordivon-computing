# Cross-cutting A0 v0

Status: A0 first closeout accepted. O1 fresh three-owner dogfood, M1 configuration identity, and U1 measurement projection all have bounded evidence. No production authority, daemon, shared database, or repository extraction was admitted.

This experiment tests three related responsibilities without merging their authorities:

```text
O1  owner-native cross-owner Observation reconstruction
M1  material configuration identity
U1  owner-native usage → non-authoritative measurements
```

## O1 — fresh current trajectory

`run_o1_current_trajectory.py` runs one new deterministic infrastructure workload rather than relabeling B3/B4 history:

```text
Host Task
→ Host external request
→ independent Harness Run
→ observation-only Runtime Tool
→ one real Runtime Job
→ Harness CompletionProposal
→ Host verification + TaskOutcome
→ three read-only owner exporters
→ Observation Gateway + Selection
```

The retained acceptance is under [`evidence/o1-current-a0-o1-1786086849266-5a8cef08ce/`](evidence/o1-current-a0-o1-1786086849266-5a8cef08ce/). It binds exact clean revisions for Computing, Host, Harness, Runtime, and the Runtime exporter.

The accepted run proved:

- a complete 25-event Host/Harness/Runtime Selection anchored on one Host Task;
- one exact Runtime Job exported while the long-lived Registry contained 20,399 Jobs;
- Host verification and outcome remained semantic authority;
- Observation remained metadata/reference-only and inferred no Trial validity;
- the Runtime Workspace was closed and independently confirmed absent;
- Harness terminal usage was projected on exactly one terminal Observation event;
- Provider-call usage detail was not copied into the retained cross-cutting evidence.

Dogfood exposed a real Runtime exporter defect before O1 could pass: the old exporter rejected a Registry whose total Job count exceeded its bounded `job_limit`, even when only one known Job was relevant. Runtime now supports exact Job selection while preserving the old full-registry bound when no selection is supplied.

## M1 — configuration identity

`configuration_identity.py` tests the narrow responsibility identified by the A0 audit: bind material facts needed to determine whether two trajectories ran under the same, different, or incompletely explainable configuration.

The common record stores only immutable binding identity, role, digest, availability, and optional owner-native reference. It does not copy Runtime execution state, Harness Run state, Security environment payloads, Evaluation contracts, Provider transcripts, or domain outcomes into a new authority.

The first accepted shapes are deliberately different:

- a retained B5 Evaluation System Manifest projected into material bindings;
- a Security-shaped `EnvironmentIdentity` retained as one opaque owner-native environment binding.

The experiment correctly marks Evaluation's environment as `digest_only`: equality can be tested, but the common layer cannot pretend to explain which environment dimensions differ when the owner payload is unavailable. This is sufficient to retain the composition experiment, not sufficient to promote a universal System Manifest schema.

## U1 — measurement projection

`measurement_projection.py` converts retained comparison metrics into the existing Observation `Measurement` shape. Owner-native values remain authoritative; the projection is rebuildable.

The first offline acceptance maps real B5 Evaluation metrics and deliberately refuses to invent monetary cost. A non-null estimated cost requires an explicit SHA-256 pricing/billing basis. OpenTelemetry GenAI names remain optional rebuildable aliases rather than Ordivon recovery-state vocabulary.

O1 then exercised the owner path and found a Harness accounting defect: `inputTokens + outputTokens` Provider records were retained, but the Run aggregate `totalTokens` stayed at zero because the token helper recognized only `total*` or `prompt* + completion*` naming. Harness fixed that owner-local normalization before measurement promotion.

The current Harness exporter projects only terminal Run aggregates from an `IndependentHarnessRunReceipt`:

```text
ordivon.harness.model_calls
ordivon.harness.tool_calls
ordivon.harness.observation_bytes
ordivon.harness.total_tokens
ordivon.harness.wall_time
ordivon.harness.tool_corrections
```

The final O1 run produced `total_tokens=58`, exactly matching the repaired owner-native Run aggregate. Per-call Provider usage stayed owner-native and was not copied into the Observation Bundle or outer O1 receipt.

## Acceptance

Bounded deterministic tests:

```bash
PYTHONPATH=research/experiments/observation-plane-v0/implementation \
python3 -m unittest discover \
  -s research/experiments/crosscut-a0-v0/tests \
  -p 'test_*.py' -v
```

M1/U1 offline acceptance:

```bash
PYTHONPATH=research/experiments/observation-plane-v0/implementation \
python3 research/experiments/crosscut-a0-v0/run_acceptance.py
```

O1 is intentionally a local live acceptance because it requires the real Runtime MCP service and private local Runtime token. Its retained evidence is validated by `tests/test_o1_evidence.py`; credentials and Provider-call payload detail are not retained.

## Disposition

Retain:

- Observation contract, read-only owner exporters, reference Gateway, and Selection semantics;
- material-binding configuration identity as a Computing experiment;
- terminal Harness measurement projection for already-owned Run aggregates;
- exact Runtime Job export as an owner-local mechanical operation.

Do not promote yet:

- no `ordivon-observation` repository;
- no Observation daemon or mandatory Collector;
- no universal System Manifest schema;
- no global `UsageRecord` authority or cost service;
- no measurement database/index until a real query cannot be served cheaply from canonical envelopes;
- no USD estimate without an explicit billing/pricing basis;
- no CPU/peak-memory/IO accounting schema until those values change a real decision.

A later A-series stage should reopen one of these decisions only when a materially different workload reproduces the same missing responsibility or the current file/in-process composition becomes measurably more expensive than extraction.
