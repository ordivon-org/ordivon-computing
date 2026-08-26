from __future__ import annotations
import json, subprocess
from pathlib import Path

OWNERS = [
    ("ordivon-computing", "/root/projects/ordivon-computing", ["README.md", "research/README.md"]),
    ("ordivon-runtime", "/root/projects/ordivon-runtime", ["README.md", "research/README.md"]),
    ("ordivon-host", "/root/projects/ordivon-host", ["README.md", "research/README.md"]),
    ("ordivon-harness", "/root/projects/ordivon-harness", ["README.md", "research/README.md"]),
    ("ordivon-world", "/root/projects/ordivon-world", ["README.md", "docs/authority.md"]),
    ("ordivon-game", "/root/projects/ordivon-game", ["README.md", "research/README.md"]),
    ("ordivon-security", "/root/projects/ordivon-security", ["README.md", "docs/authority.md"]),
    ("ordivon-finance", "/root/projects/ordivon-finance", ["README.md", "docs/authority.md"]),
    ("ordivon-human", "/root/projects/ordivon-human", ["README.md", "docs/authority.md"]),
    ("ordivon-media", "/root/projects/ordivon-media", ["README.md", "docs/authority.md"]),
    ("ordivon-web", "/root/projects/ordivon-web", ["README.md", "content/editorial/agent-web-system.md"]),
    ("ordivon-scd", "/root/projects/ordivon-scd", ["README.md"]),
    ("ordivon-computational-possibility", "/root/projects/ordivon-computational-possibility", ["README.md"]),
    ("ordivon-interlocus", "/root/projects/ordivon-interlocus", ["README.md"]),
    ("ordivon-normative", "/root/projects/ordivon-normative", ["README.md"]),
]

def git(repo: str, *args: str, check: bool = True) -> str:
    p = subprocess.run(["git", "-C", repo, *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo}: {p.stderr}")
    return p.stdout

def bounded_text(text: str, max_chars: int = 14000) -> str:
    # Keep the beginning/current entry surface, but avoid enormous owner packets.
    return text[:max_chars]

rows=[]
for owner, repo, paths in OWNERS:
    rev=git(repo,"rev-parse","refs/heads/main").strip()
    sources=[]
    for path in paths:
        exists=subprocess.run(["git","-C",repo,"cat-file","-e",f"{rev}:{path}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if not exists:
            continue
        text=git(repo,"show",f"{rev}:{path}")
        sources.append({"path":path,"text":bounded_text(text)})
    if not sources:
        raise RuntimeError(f"no source packet for {owner}")
    rows.append({"ownerId":owner,"repo":repo,"revision":rev,"sources":sources})

out={
  "schemaVersion":1,
  "kind":"ordivon.computing.discoverability-owner-source-packet",
  "truthRole":"committed-owner-source-input-for-query-generation-not-cross-owner-truth",
  "owners":rows,
  "constraints":[
    "Each source is read from committed refs/heads/main, not dirty working-tree bytes.",
    "Packet is generated before any Atlas retrieval result is supplied to the target/query generator.",
    "A generated target remains bounded to the exact source excerpt and owner revision."
  ]
}
path=Path("research/experiments/discoverability-currentness-v0/owner-source-packet-v1.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
print(json.dumps({"owners":len(rows),"revisions":{r['ownerId']:r['revision'] for r in rows},"bytes":path.stat().st_size},indent=2))
