from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'inspection-semantic-evaluations-v1.json').read_text())
rows=[]; corrections=[]
for e in src['evaluations']:
    row=dict(e)
    invalid=(row['semanticRecall'] and row['targetRank']==0) or ((not row['semanticRecall']) and row['targetRank']!=0) or (row['semanticRecall'] and row['matchClass'] not in ('TARGET','CORRECT_SUCCESSOR')) or ((not row['semanticRecall']) and row['matchClass'] in ('TARGET','CORRECT_SUCCESSOR'))
    if invalid:
        # Only one raw row is inconsistent. Its own model-authored reason explicitly says
        # A0 contains no genuine target-bearing candidate and rank 0 is correct; the model
        # cross-contaminated the A1 rank-5 generated projection while setting TARGET=true.
        if (row['ownerId'],row['queryKind'],row['surface']) != ('ordivon-scd','QK','A0_SYNTHESIS_ONLY'):
            raise RuntimeError(f'unexpected invalid row: {row}')
        before=dict(row)
        row['semanticRecall']=False
        row['targetRank']=0
        row['matchClass']='RELATED_ONLY'
        row['falsePositiveDominated']=True
        row['shortReason']='NORMALIZED_FROM_CONTRACT_INCONSISTENCY: raw reason itself states A0 has no genuine target-bearing synthesis candidate; TARGET=true was caused by cross-row contamination from the A1 rank-5 generated projection. A0 inspected candidates are SCD-related but do not recover the frozen SCDF1-SCDF10 immutable-identity target.'
        corrections.append({'key':['ordivon-scd','QK','A0_SYNTHESIS_ONLY'],'before':before,'after':row,'normalizationBasis':'pre-frozen semantic contract + raw evaluator self-explanation + exact A0/A1 candidate source-class separation; no retrieval rerun or target change'})
    rows.append(row)
out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-inspection-semantic-evaluations-normalized','source':'inspection-semantic-evaluations-v1.json','sourceDigest':src.get('inspectionTrialsDigest'),'normalizationCount':len(corrections),'corrections':corrections,'evaluations':rows,'nonClaims':['Normalization does not change retrieval candidates or targets.','The raw evaluator output remains preserved.','No currentness claim is minted by semantic normalization.']}
(ROOT/'inspection-semantic-evaluations-normalized-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print({'normalizationCount':len(corrections)})
for s in ['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']:
    for q in ['QK','QU_E','QU_ZH']:
        rr=[e for e in rows if e['surface']==s and e['queryKind']==q]
        ranks=[e['targetRank'] for e in rr if e['semanticRecall']]
        print(s,q,'recall',sum(e['semanticRecall'] for e in rr),'/',len(rr),'fp',sum(e['falsePositiveDominated'] for e in rr),'avgRank',round(sum(ranks)/len(ranks),2) if ranks else None)
