# External Semantic Contract v0

This experiment separates public Agent Effect representation, executable Tool contracts, and immutable Effect bindings from the closed Semantic Kernel v0 experiment.

```text
anc-canonical
   ├── anc-effect-ir
   └── anc-tool-contract
            │
anc-effect-ir ─┴─→ anc-effect-binding
                         │
                         ▼ BindingAdmission
                  Semantic Kernel edge
                         │
                         ▼
                  Adapter / Backend
```

The production Kernel does not import this workspace. Integration translates a signed binding into the Kernel's minimal `BindingAdmission` record.

## Commands

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 scripts/external_contract_report.py --source-revision "$(git rev-parse HEAD)"
rustc --edition=2021 rust/canonical-verifier/main.rs -o /tmp/anc-canonical-verifier
/tmp/anc-canonical-verifier fixtures/canonical/canonical-vectors.tsv
```

## Exact P0–P6 evidence

Implementation: `2f4d7ca8db6756b8add3356db52dcd237ed7a256`

- [`evidence/external-contract-2f4d7ca.json`](evidence/external-contract-2f4d7ca.json)
- [`evidence/live-ordivon-2f4d7ca.json`](evidence/live-ordivon-2f4d7ca.json)
- [`../semantic-core-v0/benchmark-results/binding-edge-2f4d7ca.json`](../semantic-core-v0/benchmark-results/binding-edge-2f4d7ca.json)

P0–P6 freezes a minimal Effect IR v1 and closes the public Effect-identity question. It does not claim a complete general Tool ABI, catalog service, Host, compiler, Task Runtime, or plugin platform.
