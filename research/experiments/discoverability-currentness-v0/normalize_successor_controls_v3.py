from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'successor-negative-history-evaluations-v2.json').read_text())
# Final dispositions enforce the pre-frozen currentness oracle boundary against the actual
# observed surfaces. A0 has no generated currentness proof. A1 consumes an existing
# generated snapshot whose 10/10 sourceTransportRevision fences were independently shown
# to differ from the current committed owner mains. Therefore semantically correct lineage
# content may earn MIXED_REQUIRES_REENTRY, never CURRENT_RESOLVED, until owner-native
# currentness is actually re-entered.
FINAL={
 ('C1','A0_SYNTHESIS_ONLY'):('MIXED_REQUIRES_REENTRY',True,True,True,True,False,True,'Network→Interlocus same-owner successor and stable research-owner:network identity are explicitly recovered, with owner-native recovery pointers; A0 itself has no fresh currentness proof, so present-tense use requires owner re-entry.'),
 ('C1','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS'):('MIXED_REQUIRES_REENTRY',True,True,True,True,False,True,'Same-owner Network→Interlocus successor is recovered, but the existing generated snapshot is revision-stale against current owner main; semantic correctness does not upgrade stale projection health into currentness proof.'),
 ('C2','A0_SYNTHESIS_ONLY'):('NOT_RECOVERED',False,False,False,False,False,False,'Only generic semantic-rehome/repository-move distinctions are returned; the specific 2026-08-22 Normative standalone migration and old shared-corpus tombstone are not recovered.'),
 ('C2','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS'):('NOT_RECOVERED',False,False,False,False,False,False,'Adding the stale generated snapshot does not surface the specific Normative physical migration/current standalone home; generic migration concepts are insufficient for this control.'),
 ('C3','A0_SYNTHESIS_ONLY'):('NOT_RECOVERED',False,False,False,False,False,False,'Post-Host/PHR1-PHR4 specific history is absent from the bounded synthesis-only journey.'),
 ('C3','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS'):('MIXED_REQUIRES_REENTRY',True,True,True,True,False,True,'Generated owner projections recover PHR1 as historical origin of current Normative and PHR2-PHR4 as sibling history, with authorityRef escape; the snapshot fence is stale, so current Normative standing still requires owner-native re-entry.'),
 ('C4','A0_SYNTHESIS_ONLY'):('HISTORICAL_ONLY',True,False,False,True,False,False,'Workstation history is recovered, but the current no-standalone-owner/public-MCP-retired rehome is absent.'),
 ('C4','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS'):('HISTORICAL_ONLY',True,False,False,True,False,False,'Workstation historical material remains discoverable; stale generated projections add no current rehome/public-MCP retirement recovery.'),
 ('C5','A0_SYNTHESIS_ONLY'):('NOT_RECOVERED',False,False,False,True,False,False,'Neither GoalCoordinatorHost historical sufficiency nor the current Host removal/contraction is materially recovered in the bounded journey.'),
 ('C5','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS'):('NOT_RECOVERED',False,False,False,True,False,False,'A generic Host coordination NOT_ADMITTED projection is adjacent but does not recover GoalCoordinatorHost history or its current removal; stale CURRENT_TO_SOURCE labels are not currentness proof.'),
}
rows=[]; corrections=[]
for e in src['evaluations']:
 row=dict(e); key=(row['caseId'],row['surface']); status,hist,curr,owner,hcd,risk,escape,reason=FINAL[key]; before=dict(row)
 row.update({'finalStatus':status,'historicalRecovered':hist,'currentSuccessorOrRemovalRecovered':curr,'currentOwnerResolved':owner,'historicalCurrentDistinctionExplicit':hcd,'falseCurrentActivationRisk':risk,'ownerNativeEscapeAvailable':escape,'shortReason':'NORMALIZED_V3: '+reason})
 # Physical/semantic distinction: cases C1/C2/C3/C4 all preserve it only when specific transition is recovered; C5 N/A=true.
 if row['caseId']=='C2': row['physicalVsSemanticDistinctionPreserved']=False
 elif row['caseId']=='C3' and row['surface']=='A0_SYNTHESIS_ONLY': row['physicalVsSemanticDistinctionPreserved']=False
 else: row['physicalVsSemanticDistinctionPreserved']=True
 if row!=before: corrections.append({'key':list(key),'before':before,'after':row})
 rows.append(row)
out={'schemaVersion':3,'kind':'ordivon.computing.discoverability-successor-negative-history-evaluations-normalized','source':'successor-negative-history-evaluations-v2.json','normalizationCount':len(corrections),'evaluations':rows,'corrections':corrections,'normalizationPrinciples':['Evaluator structured labels cannot override their own written reason/content.','A0 synthesis has no fresh owner-currentness proof.','A1 existing generated snapshot is semantically useful history/recovery material but its 10 configured source fences all differ from current committed owner mains.','Semantic successor resolution + owner escape therefore earns MIXED_REQUIRES_REENTRY, not CURRENT_RESOLVED, until current owner source is actually re-entered.']}
(ROOT/'successor-negative-history-evaluations-normalized-v3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
from collections import Counter
for s in ['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']:
 rr=[e for e in rows if e['surface']==s]; print(s,dict(Counter(e['finalStatus'] for e in rr)))
 for e in rr: print(e['caseId'],e['finalStatus'],'history',e['historicalRecovered'],'semanticCurrentRelation',e['currentSuccessorOrRemovalRecovered'],'escape',e['ownerNativeEscapeAvailable'])
