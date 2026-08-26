from __future__ import annotations
import json,sys
from pathlib import Path
ATLAS_WS=Path('/var/lib/ordivon/runtime/workspaces/atlas-discoverability-trials-20260826')
sys.path.insert(0,str(ATLAS_WS/'src'))
from ordivon_atlas.first_look import prior_result_first_look,inspect_prior_result_candidate
ROOT=Path(__file__).resolve().parent
CASES=[
 {'id':'C1','query':'Network owner communicability cross-locus capability why rename Network','oracleClass':'same-owner-semantic-successor','expected':'Historical Network should resolve to current Interlocus while preserving stable research-owner:network identity.'},
 {'id':'C2','query':'Normative owners/ordivon-normative shared research repository physical home','oracleClass':'physical-migration-no-semantic-change','expected':'Current standalone ordivon-normative physical home; old shared location is historical/tombstone; semantic owner unchanged.'},
 {'id':'C3','query':'Post-Host PHR1 PHR2 PHR3 PHR4 current owner','oracleClass':'partial-successor-plus-sibling-history','expected':'PHR1 is origin of current Normative; PHR2-PHR4 remain sibling historical research, not active Normative subprojects.'},
 {'id':'C4','query':'Ordivon Workstation current owner repository semantic MCP physical realization binding','oracleClass':'owner-rehome-no-current-standalone','expected':'Historical Workstation recoverable; no current standalone Workstation repository/owner; public MCP retired and operations consumed via Runtime/domain paths.'},
 {'id':'C5','query':'GoalCoordinatorHost shared Goal coordination current Host','oracleClass':'historical-valid-currently-removed-mechanism','expected':'Historical GoalCoordinatorHost sufficiency may remain valid for old workload, but current Host removed GoalCoordinatorHost/Goal snapshot ownership and retains generic terminal/revision invariants.'},
]
SURFACES={'A0_SYNTHESIS_ONLY':str(ATLAS_WS/'generated'),'A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS':'/root/projects/ordivon-atlas/generated'}
rows=[]
for case in CASES:
 for surface,gen in SURFACES.items():
  r=prior_result_first_look(case['query'],repository_root=ATLAS_WS,generated_dir=gen,limit=8)
  inspected=[]
  for rank,c in enumerate(r['candidates'],1):
   z=inspect_prior_result_candidate(case['query'],c['path'],c['locator'],repository_root=ATLAS_WS,generated_dir=gen,limit=8,max_projection_bytes=3600)
   content=z.get('content')
   if isinstance(content,dict) and isinstance(content.get('sections'),list): text='\n'.join(str(s.get('text','')) for s in content['sections'])
   else: text=json.dumps(content,ensure_ascii=False,sort_keys=True) if content is not None else ''
   inspected.append({'rank':rank,'candidate':c,'inspectionText':text,'contentDigest':z.get('contentDigest')})
  rows.append(case|{'surface':surface,'candidateCount':r['candidateCount'],'projectionHealth':r['projectionHealth'],'inspectedCandidates':inspected})
out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-successor-negative-history-raw-controls','atlasSourceRevision':'d01dc76cb82b8a05dab9b6cf16ffacc370d7b390','contract':'successor-negative-history-contract.md','rows':rows}
(ROOT/'successor-negative-history-raw-controls-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print('rows',len(rows),'inspections',sum(len(r['inspectedCandidates']) for r in rows),'bytes',(ROOT/'successor-negative-history-raw-controls-v1.json').stat().st_size)
for r in rows: print(r['id'],r['surface'],'candidates',r['candidateCount'],[(c['rank'],c['candidate'].get('sourceClass'),c['candidate'].get('path')) for c in r['inspectedCandidates'][:3]])
