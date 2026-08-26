from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'owner-source-packet-v1.json').read_text())
rows=[]
for owner in src['owners']:
    sources=[]
    for s in owner['sources']:
        sources.append({'path':s['path'],'text':s['text'][:4500]})
    rows.append({**{k:v for k,v in owner.items() if k!='sources'},'sources':sources})
out={
 'schemaVersion':1,
 'kind':'ordivon.computing.discoverability-owner-source-packet-compact-v2',
 'truthRole':src['truthRole'],
 'owners':rows,
 'derivedFrom':'owner-source-packet-v1.json',
 'compactionRule':'first 4500 Unicode characters per already-source-fenced supplied file; no semantic selection and no Atlas result observed',
 'constraints':src['constraints']+['Compaction is mechanical and performed after a no-result budget-exhaustion event; no retrieval outcome informed retained text.']
}
(ROOT/'owner-source-packet-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print({'owners':len(rows),'bytes':(ROOT/'owner-source-packet-v2.json').stat().st_size,'chars':sum(len(s['text']) for o in rows for s in o['sources'])})
