# Ordivon managed metadata validator

`ordivon-content` is a small dependency-free validator for documents a repository has explicitly admitted through `.ordivon/project.yaml` `managed_paths`. It validates project boundaries, front-matter identity, lifecycle, source role, required metadata shape, and duplicate managed/canonical identifiers.

It deliberately does **not** inventory the whole documentation corpus, score warning counts, generate cross-repository baselines, own templates, or judge claim truth. Markdown structure, prose, spelling, and links belong to markdownlint-cli2, Vale, CSpell, and Lychee.

Source-tree compatibility entry:

```bash
python scripts/ordivon_content.py project --root .
python scripts/ordivon_content.py check --root . --mode strict
```

`strict` blocks malformed or missing metadata only inside explicitly managed paths. Unmanaged historical/ordinary documentation is outside this custom governance surface.
