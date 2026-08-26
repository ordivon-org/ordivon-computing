from __future__ import annotations
import json,sys
from pathlib import Path
ATLAS_WS=Path('/var/lib/ordivon/runtime/workspaces/atlas-discoverability-trials-20260826')
sys.path.insert(0,str(ATLAS_WS/'src'))
from ordivon_atlas.first_look import prior_result_first_look_many,inspect_prior_result_candidate
ROOT=Path(__file__).resolve().parent
V=json.loads((ROOT/'prefrozen-authored-query-variants-v2.json').read_text())
T=json.loads((ROOT/'prefrozen-targets-v2.json').read_text())
SURFACES={
 'A0_SYNTHESIS_ONLY':str(ATLAS_WS/'generated'),
 'A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS':'/root/projects/ordivon-atlas/generated',
}
targets=T['targets']
rows=[]
for q in V['queries']:
    # q01 corresponds to targets[0], q15 to targets[14]
    idx=int(q['queryId'][1:3])-1
    t=targets[idx]
    qkind='AQ_EN' if q['language']=='en' else 'AQ_ZH'
    variants=q['variants']
    for surface,gen in SURFACES.items():
        result=prior_result_first_look_many(variants,repository_root=ATLAS_WS,generated_dir=gen,limit=8)
        inspected=[]
        for rank,c in enumerate(result['candidates'],1):
            best_i=int(c.get('bestVariantIndex',0)); best_q=variants[best_i]
            # Candidate may rank below 8 in its source variant because first-look-many merged top32.
            z=inspect_prior_result_candidate(best_q,c['path'],c['locator'],repository_root=ATLAS_WS,generated_dir=gen,limit=32,max_projection_bytes=2400)
            content=z.get('content')
            if isinstance(content,dict) and isinstance(content.get('sections'),list):
                text='\n'.join(str(s.get('text','')) for s in content['sections'])
                shape={'projection':content.get('projection'),'sectionCount':content.get('sectionCount'),'matchedSectionCount':content.get('matchedSectionCount'),'projectionTruncated':content.get('projectionTruncated'),'projectedBytes':content.get('projectedBytes')}
            else:
                text=json.dumps(content,ensure_ascii=False,sort_keys=True) if content is not None else ''
                shape={'projection':'exact-generated-row-or-other'}
            inspected.append({'rank':rank,'candidate':c,'bestVariantQuery':best_q,'inspectionText':text,'inspectionShape':shape,'contentDigest':z.get('contentDigest')})
        rows.append({
          'ownerId':t['ownerId'],'targetKey':t['targetKey'],'targetStanding':t['targetStanding'],'sourcePath':t['sourcePath'],'sourceAnchorQuote':t['sourceAnchorQuote'],
          'queryId':q['queryId'],'queryKind':qkind,'rawQuery':q['rawQuery'],'authoredVariants':variants,'surface':surface,
          'candidateCount':result['candidateCount'],'variantSummaries':result['variantSummaries'],'projectionHealth':result['projectionHealth'],'inspectedCandidates':inspected
        })
out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-authored-query-inspection-trials','variantsFile':'prefrozen-authored-query-variants-v2.json','variantsGeneratedBeforeRetrieval':True,'atlasSourceRevision':'d01dc76cb82b8a05dab9b6cf16ffacc370d7b390','inspectionProjectionByteLimitPerCandidate':2400,'rows':rows}
(ROOT/'authored-query-inspection-trials-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
from collections import Counter
print('rows',len(rows),'inspections',sum(len(r['inspectedCandidates']) for r in rows),'bytes',(ROOT/'authored-query-inspection-trials-v1.json').stat().st_size)
for s in SURFACES:
  for qk in ['AQ_EN','AQ_ZH']:
    rr=[r for r in rows if r['surface']==s and r['queryKind']==qk]
    print(s,qk,'nonempty',sum(bool(r['candidateCount']) for r in rr),'/',len(rr),'counts',dict(Counter(r['candidateCount'] for r in rr)))
