# Ordivon content CLI

`ordivon-content` validates project manifests, checks Markdown and MDX documents, emits machine-readable receipts, and builds advisory cross-repository baselines.

From the Computing source tree:

```bash
python scripts/ordivon_content.py check --root .
python scripts/ordivon_content.py baseline --repository-parent /root/projects
```

`advisory` reports migration debt without blocking. `strict` blocks only failures in paths explicitly listed under `managed_paths`.
