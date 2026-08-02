# Ordivon content CLI

`ordivon-content` validates Ordivon project manifests and document metadata, lifecycle, source roles, required sections, and canonical identities. It emits machine-readable receipts and advisory cross-repository baselines. General Markdown, prose, spelling, and link checks are delegated to markdownlint-cli2, Vale, CSpell, and Lychee.

From the Computing source tree:

```bash
python scripts/ordivon_content.py check --root .
python scripts/ordivon_content.py baseline --repository-parent /root/projects
```

`advisory` reports migration debt without blocking. `strict` blocks only failures in paths explicitly listed under `managed_paths`.
