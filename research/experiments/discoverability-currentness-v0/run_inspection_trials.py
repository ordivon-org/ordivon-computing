from __future__ import annotations
import json,sys
from pathlib import Path
ATLAS_WS=Path('/var/lib/ordivon/runtime/workspaces/atlas-discoverability-trials-20260826')
sys.path.insert(0,str(ATLAS_WS/'src'))
from ordivon_atlas.first_look import inspect_prior_result_candidate
ROOT=Path(__file__).resolve().parent
RAW=json.loads((ROOT/'atlas-raw-trials-v1.json').read_text())
SURFACE_GEN={
 'A0_SYNTHESIS_ONLY':str(ATLAS_WS/'generated'),
 'A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS':'/root/projects/ordivon-atlas/generated',
}
rows=[]
for r in RAW['rows']:
 inspected=[]
 for rank,c in enumerate(r['candidates'],1):
  z=inspect_prior_result_candidate(r['query'],c['path'],c['locator'],repository_root=ATLAS_WS,generated_dir=SURFACE_GEN[r['surface']],limit=8,max_projection_bytes=2400)
  content=z.get('content')
  if isinstance(content,dict) and isinstance(content.get('sections'),list):
   text='\n'.join(str(s.get('text','')) for s in content['sections'])
   shape={'projection':content.get('projection'),'sectionCount':content.get('sectionCount'),'matchedSectionCount':content.get('matchedSectionCount'),'projectionTruncated':content.get('projectionTruncated'),'projectedBytes':content.get('projectedBytes')}
  else:
   text=json.dumps(content,ensure_ascii=False,sort_keys=True) if content is not None else ''
   shape={'projection':'exact-generated-row-or-other'}
  inspected.append({'rank':rank,'candidate':c,'inspectionText':text,'inspectionShape':shape,'contentDigest':z.get('contentDigest')})
 rows.append({k:r[k] for k in ['ownerId','targetKey','targetStanding','sourcePath','sourceAnchorQuote','queryKind','query','surface','candidateCount','projectionHealth'] } | {'inspectedCandidates':inspected})
out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-atlas-inspection-trials','rawTrials':'atlas-raw-trials-v1.json','inspectionProjectionByteLimitPerCandidate':2400,'rows':rows}
(ROOT/'atlas-inspection-trials-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print({'rows':len(rows),'inspections':sum(len(r['inspectedCandidates']) for r in rows),'bytes':(ROOT/'atlas-inspection-trials-v1.json').stat().st_size})
