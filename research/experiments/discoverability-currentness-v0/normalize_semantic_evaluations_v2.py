from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'inspection-semantic-evaluations-normalized-v1.json').read_text())
CORRECTIONS={
 ('ordivon-runtime','QU_E','A0_SYNTHESIS_ONLY'):'Evaluator label contradicted its own reason: reason states no candidate explicitly ties Runtime to command/process-tree authoritative records and target is not recovered.',
 ('ordivon-runtime','QU_E','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS'):'Evaluator label contradicted its own reason: reason states none of the candidates directly recover Runtime as the command/process-tree/physical-execution owner.',
 ('ordivon-normative','QK','A0_SYNTHESIS_ONLY'):'Evaluator label contradicted its own reason: reason states none of the synthesis candidates recover the Normative disposable-conformance-witness / no-enforcement-authority target and explicitly concludes RELATED_ONLY.',
}
rows=[]; corrections=[]
for e in src['evaluations']:
 row=dict(e); key=(row['ownerId'],row['queryKind'],row['surface'])
 if key in CORRECTIONS:
  before=dict(row); row['semanticRecall']=False; row['targetRank']=0; row['matchClass']='RELATED_ONLY'; row['falsePositiveDominated']=True; row['shortReason']='NORMALIZED_V2_FROM_EVALUATOR_SELF-CONTRADICTION: '+CORRECTIONS[key]; corrections.append({'key':list(key),'before':before,'after':row,'basis':CORRECTIONS[key]})
 rows.append(row)
out={'schemaVersion':2,'kind':'ordivon.computing.discoverability-inspection-semantic-evaluations-normalized','source':'inspection-semantic-evaluations-normalized-v1.json','normalizationCount':len(corrections),'corrections':corrections,'evaluations':rows,'nonClaims':['Normalization only resolves labels that directly contradict the evaluator\'s own written semantic reason and inspected-candidate content.','Raw evaluator outputs and v1 normalization remain preserved.','No target, retrieval candidate, rank or currentness source was changed.']}
(ROOT/'inspection-semantic-evaluations-normalized-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print('corrections',len(corrections))
for s in ['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']:
 for q in ['QK','QU_E','QU_ZH']:
  rr=[e for e in rows if e['surface']==s and e['queryKind']==q]; ranks=[e['targetRank'] for e in rr if e['semanticRecall']]; print(s,q,'recall',sum(e['semanticRecall'] for e in rr),'/',len(rr),'fp',sum(e['falsePositiveDominated'] for e in rr),'avgRank',round(sum(ranks)/len(ranks),2) if ranks else None)
