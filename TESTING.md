# Testing policy

Tests protect explicit semantic and foundational invariants; they are not a mandatory precondition for every edit.

## Source layers

Production-candidate protocol code, normative Schemas, and canonical vectors live under `packages/ordivon-protocol/`. Executable experiments, fixtures, live evidence scripts, and conformance suites remain under `research/experiments/`. The independent `ordivon-host` repository owns product Host code; Computing does not carry a shadow Host tree.

Core, Knowledge, the Agent-first research method, research map, live questions, and source-bound evidence form the foundational architecture contract. They are checked mechanically for required files, relative links, reference identifiers, substrate/overlay structure, historical-compression recoverability, and obsolete layer terminology.

## T0 — surgical edit loop

Run the narrow checker or test that protects the touched boundary.

Install the pinned content tools once per checkout, then run the narrow content and research checks:

```bash
mise install
PYTHONPATH=packages/content-cli/src \
  python3.12 -m unittest discover -s packages/content-cli/tests
python3.12 scripts/ordivon_content.py check \
  --root . --mode strict --receipt /tmp/ordivon-content-check.json
vale docs/content-engineering/README.md packages/content-{contract,cli,templates}/**/*.md
markdownlint-cli2 docs/content-engineering/README.md packages/content-{contract,cli,templates}/**/*.md
cspell lint --no-progress --no-summary docs/content-engineering/README.md packages/content-{contract,cli,templates}/**/*.md
lychee --config lychee.toml docs/content-engineering/README.md packages/content-{contract,cli,templates}/**/*.md
python3.12 scripts/check_foundational_docs.py
python3.12 scripts/check_agent_research_method.py
python3.12 scripts/check_computer_responsibility_map.py
python3.12 scripts/check_historical_research_compression.py
python3.12 scripts/check_research_portfolio.py
python3.12 scripts/render_research_portfolio.py --check
python3.12 -m unittest research.evidence.tests.test_foundational_docs
```

For protocol and experiments:

```bash
python3.12 scripts/check_protocol_release.py

cd packages/ordivon-protocol
PYTHONPATH=src python3.12 -m unittest tests.test_promoted_boundaries tests.test_schema_conformance

cd research/experiments/semantic-core-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:src \
  python3.12 tests/test_binding_edge.py

cd ../external-semantic-contract-v0
PYTHONPATH=../../../packages/ordivon-protocol/src:../semantic-core-v0/src:. \
  python3.12 tests/test_binding_authority.py
```

## T1 — complete deterministic gate

The repository root owns the canonical gate. It validates managed content paths and the content CLI, foundational documents, the Agent-first research method, the Computer responsibility map, historical-research compression recoverability, the single-source research portfolio and generated view, project and Protocol manifests, release Artifact digests, Schema/vector/implementation agreement, static checks, deterministic semantic and continuation experiments, evidence, and Rust canonical vectors.

```bash
python3.12 scripts/ordivon_conformance.py gate \
  --receipt /tmp/ordivon-conformance-receipt.json
```

The command uses the active Python interpreter and installed `ruff`, `jsonschema`, and `rustc`; CI fixes these to Python 3.12, Ruff 0.15.14, JSON Schema 4.25.1, and the stable Rust toolchain. Task-continuation subprocess fixtures receive an explicit `/tmp` boundary so Runtime-specific temporary directories do not change their isolation semantics.

## T2 — pull-request CI

`.github/workflows/deterministic-contracts.yml` invokes the same root gate when executable contracts or foundational architecture paths change. This includes root/Core/Knowledge/Studies, the research map and questions, evidence, Protocol, conformance, Schemas, fixtures, tests, and executable scripts.

Ordinary historical notes outside those paths may remain documentation-only. A document promoted into the foundational set inherits deterministic link and source-reference checks.

## T2P — protocol-path consumer compatibility

`.github/workflows/protocol-consumers.yml` runs only when the Protocol package, release manifest, conformance declaration, or consumer-gate code changes. It checks out clean Computing, Host, and Game repositories, verifies that both consumer pins resolve to the released Artifact digests, runs the Host contract suite against the candidate package, and runs the Game TypeScript vector suite.

This is deliberately narrower than a general cross-project gate. Under Core A11 it should be removed or replaced if a mature package/schema registry provides the same immutable release and consumer evidence with lower recurring cost.

## T3 — cross-repository evidence

Revision-vector and System Snapshot capture are deterministic tools, but deciding which exact repositories, services, deployments, and live evidence belong to an experiment remains a bounded research decision.

```bash
python3.12 scripts/ordivon_conformance.py vector \
  --require-all --require-clean \
  --output /tmp/ordivon-revision-vector.json

python3.12 scripts/ordivon_conformance.py snapshot \
  --require-all \
  --snapshot-id ordivon-system-<timestamp> \
  --purpose "<bounded experiment or closeout>" \
  --output research/evidence/snapshots/<snapshot>.json
```

Real Runtime execution, process restart, response-loss injection, benchmarks, service-binary binding, model-provider evidence, deployment observations, and sustained-workload measurements remain explicit T3 work. Their outputs belong in immutable machine receipts rather than mutable status prose.

## Deletion rule

Remove or merge a test only when it duplicates the same observable invariant, protects deleted behavior, or tests an implementation detail with no failure consequence. Remove a Core statement when deleting it creates no specific failure, a mature lower layer already owns the invariant, or the statement freezes a temporary model limitation.

Test count and document length are not value signals. Diagnostic power, falsifiability, execution cost, and downstream leverage decide the cost.
