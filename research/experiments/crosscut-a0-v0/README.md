# Cross-cutting A0 v0

Status: bounded M1/U1 experiment; no production authority and no repository extraction.

This experiment implements the two A0 slices that already have enough evidence to test without inventing a fresh Host→Harness→Runtime workload:

```text
M1  configuration identity
U1  measurement projection
```

O1 fresh trajectory dogfood remains separate because it requires a genuinely current three-owner workload. Historical B3/B4 evidence is not relabeled as a fresh current workload.

## M1 — configuration identity

`configuration_identity.py` tests the narrow responsibility identified by the A0 audit: bind the material facts needed to determine whether two trajectories ran under the same, different, or incompletely explainable configuration.

The common record stores only immutable binding identity, role, digest, availability, and optional owner-native reference. It does not copy Runtime execution state, Harness Run state, Security environment payloads, Evaluation contracts, Provider transcripts, or domain outcome into a new authority.

The first two shapes are intentionally different:

- an Evaluation System Manifest projected into material bindings;
- a Security-style `EnvironmentIdentity` retained as one owner-native environment binding.

If these shapes require a universal environment ontology or domain-field copying, M1 is falsified and should be narrowed back to opaque references.

## U1 — measurement projection

`measurement_projection.py` converts already-retained comparison metrics into the existing Observation `Measurement` shape. Owner-native values remain authoritative; this is a rebuildable query projection.

The profile deliberately does not invent monetary cost. A non-null estimated cost is rejected unless an explicit SHA-256 pricing/billing basis is supplied. OpenTelemetry GenAI names are retained only as rebuildable aliases for compatible token measurements, not as Ordivon recovery-state vocabulary.

## Acceptance

```bash
PYTHONPATH=research/experiments/observation-plane-v0/implementation \
python3 -m unittest discover \
  -s research/experiments/crosscut-a0-v0/tests \
  -p 'test_*.py' -v

PYTHONPATH=research/experiments/observation-plane-v0/implementation \
python3 research/experiments/crosscut-a0-v0/run_acceptance.py
```

`run_acceptance.py` consumes the retained B5 diagnostic System Manifest and Result plus a metadata-only Security environment fixture shaped from the current Security `EnvironmentIdentity` contract. It writes one bounded receipt under `evidence/`; it writes no Host, Harness, Runtime, Security, or Finance state.
