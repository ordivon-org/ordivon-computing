from __future__ import annotations
import json,sys
from pathlib import Path
ATLAS_WS=Path('/var/lib/ordivon/runtime/workspaces/atlas-discoverability-trials-20260826')
sys.path.insert(0,str(ATLAS_WS/'src'))
from ordivon_atlas.first_look import prior_result_first_look
ROOT=Path(__file__).resolve().parent
TARGETS=json.loads((ROOT/'prefrozen-targets-v2.json').read_text())
SURFACES={
  'A0_SYNTHESIS_ONLY': {'generated': str(ATLAS_WS/'generated')},
  'A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS': {'generated':'/root/projects/ordivon-atlas/generated'},
}
QUERY_FIELDS={'QK':'qkOwnerKnown','QU_E':'quEnglish','QU_ZH':'quChinese'}
rows=[]
for t in TARGETS['targets']:
  for qkind,field in QUERY_FIELDS.items():
    query=t[field]
    for surface,spec in SURFACES.items():
      result=prior_result_first_look(query,repository_root=ATLAS_WS,generated_dir=spec['generated'],limit=8)
      rows.append({
        'ownerId':t['ownerId'],'targetKey':t['targetKey'],'targetStanding':t['targetStanding'],'sourcePath':t['sourcePath'],'sourceAnchorQuote':t['sourceAnchorQuote'],
        'queryKind':qkind,'query':query,'surface':surface,
        'candidateCount':result['candidateCount'],'projectionHealth':result['projectionHealth'],'candidates':result['candidates'],'claims':result['claims']
      })
out={
 'schemaVersion':1,'kind':'ordivon.computing.discoverability-atlas-raw-trials',
 'atlasSourceRevision':'d01dc76cb82b8a05dab9b6cf16ffacc370d7b390',
 'targetFile':'prefrozen-targets-v2.json','targetGeneratedBeforeRetrieval':True,
 'surfaces':{
  'A0_SYNTHESIS_ONLY':'Committed Atlas main synthesis with no generated owner projection; projectionHealth should be unavailable.',
  'A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS':'Same committed Atlas code/synthesis, but consuming the exact existing /root/projects/ordivon-atlas/generated snapshot. External audit already established its configured sourceTransportRevision fences predate all ten configured owner current-main freezes, despite its internal CURRENT_TO_SOURCE labels.',
  'A2_REFRESHED_CURRENT':'NOT_AVAILABLE: committed Atlas check/refresh attempt timed out after 120 seconds before producing a generated snapshot.'
 },
 'rows':rows
}
(ROOT/'atlas-raw-trials-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
from collections import Counter,defaultdict
print('rows',len(rows))
for s in SURFACES:
 print('\n',s)
 for q in QUERY_FIELDS:
  rr=[r for r in rows if r['surface']==s and r['queryKind']==q]
  print(q,'nonempty',sum(bool(r['candidateCount']) for r in rr),'/',len(rr),'candidateCounts',dict(Counter(r['candidateCount'] for r in rr)))
