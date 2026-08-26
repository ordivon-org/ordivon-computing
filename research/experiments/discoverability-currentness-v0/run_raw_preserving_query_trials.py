from __future__ import annotations
import json,sys
from pathlib import Path
ATLAS_WS=Path('/var/lib/ordivon/runtime/workspaces/atlas-discoverability-trials-20260826')
sys.path.insert(0,str(ATLAS_WS/'src'))
from ordivon_atlas.first_look import prior_result_first_look_many,inspect_prior_result_candidate
ROOT=Path(__file__).resolve().parent
V=json.loads((ROOT/'prefrozen-authored-query-variants-v2.json').read_text())
T=json.loads((ROOT/'prefrozen-targets-v2.json').read_text())
SURFACES={'A0_SYNTHESIS_ONLY':str(ATLAS_WS/'generated'),'A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS':'/root/projects/ordivon-atlas/generated'}
def t2(raw,authored):
 out=[]
 for q in [raw]+list(authored):
  if q not in out: out.append(q)
  if len(out)==4: break
 return out
rows=[]
for q in V['queries']:
 idx=int(q['queryId'][1:3])-1; t=T['targets'][idx]; qkind='T2_EN' if q['language']=='en' else 'T2_ZH'; variants=t2(q['rawQuery'],q['variants'])
 for surface,gen in SURFACES.items():
  result=prior_result_first_look_many(variants,repository_root=ATLAS_WS,generated_dir=gen,limit=8); inspected=[]
  for rank,c in enumerate(result['candidates'],1):
   best_i=int(c.get('bestVariantIndex',0)); best_q=variants[best_i]
   z=inspect_prior_result_candidate(best_q,c['path'],c['locator'],repository_root=ATLAS_WS,generated_dir=gen,limit=32,max_projection_bytes=2400); content=z.get('content')
   if isinstance(content,dict) and isinstance(content.get('sections'),list): text='\n'.join(str(s.get('text','')) for s in content['sections'])
   else: text=json.dumps(content,ensure_ascii=False,sort_keys=True) if content is not None else ''
   inspected.append({'rank':rank,'candidate':c,'bestVariantQuery':best_q,'inspectionText':text,'contentDigest':z.get('contentDigest')})
  rows.append({'ownerId':t['ownerId'],'targetKey':t['targetKey'],'targetStanding':t['targetStanding'],'sourcePath':t['sourcePath'],'sourceAnchorQuote':t['sourceAnchorQuote'],'queryId':q['queryId'],'queryKind':qkind,'rawQuery':q['rawQuery'],'t2Variants':variants,'surface':surface,'candidateCount':result['candidateCount'],'variantSummaries':result['variantSummaries'],'projectionHealth':result['projectionHealth'],'inspectedCandidates':inspected})
out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-raw-preserving-query-inspection-trials','contract':'raw-preserving-query-ablation-contract.json','construction':'raw exact query + first three distinct already-frozen authored variants in source order, max4','rows':rows}
(ROOT/'raw-preserving-query-inspection-trials-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print('rows',len(rows),'inspections',sum(len(r['inspectedCandidates']) for r in rows),'bytes',(ROOT/'raw-preserving-query-inspection-trials-v1.json').stat().st_size)
