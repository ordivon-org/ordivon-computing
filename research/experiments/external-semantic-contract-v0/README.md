# External Semantic Contract v0

This experiment owns the public backend-neutral Effect representation, executable Tool contracts, immutable Effect bindings, and the signed projection admitted by the closed Semantic Kernel v0 experiment.

```text
anc-canonical
   ├── anc-effect-ir
   └── anc-tool-contract
            │
anc-effect-ir ─┴─→ anc-effect-binding
                         │
                         ▼ signed BindingAdmission
                  Semantic Kernel edge
                         │
                         ▼
                  Adapter / Backend
```

The Kernel does not import this workspace. Complete signed Bindings remain in a content-addressed external store; Kernel state keeps only the immutable identity, Effect digest, Binding digest, revision, supersedes edge, and Kernel Authority attestation.

## Deterministic gate

```bash
PYTHONPATH=src:../semantic-core-v0/src:. python3.12 -m unittest discover -s tests
ruff check src integration tests scripts
rustc --edition=2021 rust/canonical-verifier/main.rs -o /tmp/anc-canonical-verifier
/tmp/anc-canonical-verifier ../../../packages/ordivon-protocol/src/ordivon_protocol/vectors/canonical-vectors.tsv
```

## Manual real-system evidence

```bash
set -a
source /etc/ordivon/ordivon-mcp.env
set +a

PYTHONPATH=src:../semantic-core-v0/src:../semantic-core-v0/scripts:. \
  python3.12 scripts/live_bound_ordivon_restart.py \
  --source-revision <exact-commit>

PYTHONPATH=src:../semantic-core-v0/src:../semantic-core-v0/scripts:. \
  python3.12 scripts/live_bound_ordivon_files.py \
  --source-revision <exact-commit>
```

The public Effect IR v1 is intentionally small. It does not claim a complete general Tool ABI, catalog service, Host, compiler, Task Runtime, Provider selector, or plugin platform.

See [`ARCHITECTURE.md`](ARCHITECTURE.md), [`SPEC.md`](SPEC.md), [`CONFORMANCE.md`](CONFORMANCE.md), and [`EVIDENCE.md`](EVIDENCE.md).
