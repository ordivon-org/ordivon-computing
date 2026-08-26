from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'raw-preserving-query-semantic-evaluations-v1.json').read_text())
rows=[]; corrections=[]
for e in src['evaluations']:
    row=dict(e)
    key=(row['ownerId'],row['queryKind'],row['surface'])
    # One positive row is internally rank-inconsistent: its reason says rank 1 is already
    # target-bearing while the structured targetRank says 2. This changes no recall count.
    if key==('ordivon-host','T2_ZH','A0_SYNTHESIS_ONLY') and row['semanticRecall'] and row['targetRank']==2:
        before=dict(row)
        row['targetRank']=1
        row['shortReason']='NORMALIZED_V2_FROM_EVALUATOR_SELF-CONTRADICTION: the evaluator reason itself identifies rank 1 agent-work-realization/successor-continuity material as already target-bearing; recall remains true and only earliest rank is corrected.'
        corrections.append({'key':list(key),'before':before,'after':row})
    rows.append(row)
out={'schemaVersion':2,'kind':'ordivon.computing.discoverability-raw-preserving-query-semantic-evaluations-normalized','source':'raw-preserving-query-semantic-evaluations-v1.json','normalizationCount':len(corrections),'corrections':corrections,'evaluations':rows,'apparatusEvents':src.get('apparatusEvents',[]),'nonClaims':['No target, retrieval candidate, semantic label, currentness source or recall count changed.','Normalization only corrects the earliest target rank where the evaluator reason directly contradicts its structured rank.']}
(ROOT/'raw-preserving-query-semantic-evaluations-normalized-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print({'normalizationCount':len(corrections)})
for s in ['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']:
    for q in ['T2_EN','T2_ZH']:
        rr=[e for e in rows if e['surface']==s and e['queryKind']==q]
        ranks=[e['targetRank'] for e in rr if e['semanticRecall']]
        print(s,q,'recall',sum(e['semanticRecall'] for e in rr),'/',len(rr),'fp',sum(e['falsePositiveDominated'] for e in rr),'avgRank',round(sum(ranks)/len(ranks),2) if ranks else None)
