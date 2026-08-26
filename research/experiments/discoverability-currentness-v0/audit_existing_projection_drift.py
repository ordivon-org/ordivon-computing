from __future__ import annotations
import json,subprocess
from pathlib import Path
atlas=Path('/root/projects/ordivon-atlas')
registry=json.loads((atlas/'config/sources.json').read_text())['sources']
health=json.loads((atlas/'generated/projection-health.json').read_text())
health_rows=health if isinstance(health,list) else health.get('projectionHealth',[])
by={r.get('ownerResearchRef'):r for r in health_rows}
rows=[]
for s in registry:
 ref=s['ownerResearchRef']; repo=s['repo']; current=subprocess.check_output(['git','-C',repo,'rev-parse','refs/heads/main'],text=True).strip(); h=by.get(ref,{})
 old=h.get('sourceTransportRevision') or h.get('transportRevision')
 rows.append({'ownerResearchRef':ref,'repo':repo,'snapshotHealthLabel':h.get('health') or h.get('currentness'),'snapshotSourceTransportRevision':old,'currentCommittedMain':current,'snapshotFenceEqualsCurrentMain':old==current})
out={'schemaVersion':1,'kind':'ordivon.computing.atlas-existing-projection-drift-audit','observedAt':'2026-08-26','truthRole':'cross-source mechanical revision comparison; does not mint owner semantic currentness','rows':rows,'counts':{'configuredOwners':len(rows),'snapshotFenceEqualsCurrentMain':sum(r['snapshotFenceEqualsCurrentMain'] for r in rows),'snapshotFenceDiffersFromCurrentMain':sum(not r['snapshotFenceEqualsCurrentMain'] for r in rows)},'law':'A projection health label describes the projection against its observed source fence; it is not a timeless claim that the projection still matches a later owner main.'}
p=Path('research/experiments/discoverability-currentness-v0/existing-projection-drift-v1.json');p.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n');print(json.dumps(out['counts'],indent=2));
for r in rows: print(r['ownerResearchRef'],r['snapshotHealthLabel'],r['snapshotSourceTransportRevision'],'->',r['currentCommittedMain'],'same=',r['snapshotFenceEqualsCurrentMain'])
