from __future__ import annotations
import json,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'successor-negative-history-raw-controls-v1.json').read_text())
CONTRACT=(ROOT/'successor-negative-history-contract.md').read_text()
CASES=['C1','C2','C3','C4','C5']; SURF=['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def schema(case):
 item={'type':'object','additionalProperties':False,'properties':{
  'caseId':{'type':'string','enum':[case]},'surface':{'type':'string','enum':SURF},
  'historicalRecovered':{'type':'boolean'},'currentSuccessorOrRemovalRecovered':{'type':'boolean'},'currentOwnerResolved':{'type':'boolean'},'historicalCurrentDistinctionExplicit':{'type':'boolean'},'physicalVsSemanticDistinctionPreserved':{'type':'boolean'},'falseCurrentActivationRisk':{'type':'boolean'},'ownerNativeEscapeAvailable':{'type':'boolean'},
  'finalStatus':{'type':'string','enum':['CURRENT_RESOLVED','HISTORICAL_ONLY','MIXED_REQUIRES_REENTRY','MISLEADING_REACTIVATION','NOT_RECOVERED']},'shortReason':{'type':'string'}},
  'required':['caseId','surface','historicalRecovered','currentSuccessorOrRemovalRecovered','currentOwnerResolved','historicalCurrentDistinctionExplicit','physicalVsSemanticDistinctionPreserved','falseCurrentActivationRisk','ownerNativeEscapeAvailable','finalStatus','shortReason']}
 return {'type':'object','additionalProperties':False,'properties':{'evaluations':{'type':'array','minItems':2,'maxItems':2,'items':item}},'required':['evaluations']}
def compact(r):
 return {'caseId':r['id'],'query':r['query'],'oracleClass':r['oracleClass'],'expected':r['expected'],'surface':r['surface'],'projectionHealth':r['projectionHealth'],'candidates':[{'rank':c['rank'],'sourceClass':c['candidate'].get('sourceClass'),'path':c['candidate'].get('path'),'currentness':c['candidate'].get('currentness'),'inspectionText':c['inspectionText']} for c in r['inspectedCandidates']]}
def run(idx,case):
 rows=[compact(r) for r in DATA['rows'] if r['id']==case]
 prompt='''You are evaluating a preregistered SUCCESSOR / NEGATIVE-HISTORY retrieval control. The expected current relation is supplied by the frozen audit contract and current owner-native oracle; Atlas itself remains only the candidate instrument.

For each of the two Atlas surfaces, judge the bounded top-8 + inspect-candidate journey. Historical evidence may be genuinely valid. The question is whether the journey also recovers or safely points toward the CURRENT successor/removal and prevents a finite consumer from silently reactivating obsolete owner/mechanism state.

Definitions:
- CURRENT_RESOLVED: bounded journey itself recovers enough current successor/removal + history distinction + owner route to act safely.
- HISTORICAL_ONLY: useful historical material recovered but current successor/removal is absent.
- MIXED_REQUIRES_REENTRY: candidates expose both useful lineage/currentness warning or owner escape, but current answer still requires owner-native re-entry.
- MISLEADING_REACTIVATION: ranked journey materially encourages treating historical state/mechanism/location as current.
- NOT_RECOVERED: even the relevant history/transition is not materially recovered.

`projectionHealth` labels on the existing generated snapshot are not current oracle: the audit already established their source fences predate present owner mains. Do not let a stale `CURRENT_TO_SOURCE` label override the supplied current oracle.

Evaluate every boolean literally. `physicalVsSemanticDistinctionPreserved` is relevant to migration/rehome cases; for other cases set true if the journey does not conflate these categories. `ownerNativeEscapeAvailable` requires a usable source/owner pointer in the inspected content, not merely knowing the answer from this prompt.

FROZEN CONTRACT:\n'''+CONTRACT+'\n\nROWS:\n'+json.dumps(rows,ensure_ascii=False,sort_keys=True)
 completion={'mode':'structured-result-v1','resultKind':f'discoverability-successor-eval-{case}','resultSchema':schema(case)}
 settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=4500)
 now=time.time_ns()//1_000_000
 c=HarnessRunContract(harness_run_id=f'harness-run:discoverability-successor-eval:{case}:{now}',harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-discoverability-audit',caller_run_ref=f'discoverability-successor-eval|{case}',objective_ref=ref(f'objective:successor-eval:{case}','objective',{'target':'evaluate successor/negative-history currentness legibility'}),context_refs=(ref(f'context:successor-eval:{case}','context',{'prompt':prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=180000,max_total_tokens=170000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f'system:successor-eval:{case}','system-manifest',{'experiment':'discoverability-currentness-v0','role':'successor-currentness-journey-evaluator'}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix=f'successor-eval-{case}-') as state:
  ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},)); result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
 if not result: raise RuntimeError(f'{case} failed {ex.loop_result.stop_code.value}')
 expected={(case,s) for s in SURF}; got={(e['caseId'],e['surface']) for e in result['evaluations']}
 if got!=expected: raise RuntimeError(f'{case} coverage mismatch')
 return {'case':case,'evaluations':result['evaluations'],'usage':ex.loop_result.usage,'stopCode':ex.loop_result.stop_code.value}
def main():
 partial=ROOT/'successor-eval-partials-v2'; partial.mkdir(exist_ok=True)
 bs=[]; apparatus=[]
 for i,c in enumerate(CASES):
  path=partial/f'{i+1:02d}-{c}.json'
  if path.exists():
   b=json.loads(path.read_text()); bs.append(b); print('reuse',c,flush=True); continue
  last=None
  for attempt in (1,2):
   try:
    b=run(i+1,c); b['apparatusAttempt']=attempt; path.write_text(json.dumps(b,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); bs.append(b); print('done',c,'attempt',attempt,flush=True); last=None; break
   except Exception as exc:
    last=f'{type(exc).__name__}: {exc}'; apparatus.append({'case':c,'attempt':attempt,'error':last}); print('retryable-failure',c,'attempt',attempt,last,flush=True)
  if last is not None: raise RuntimeError(f'{c} exhausted apparatus retries: {last}')
 es=[e for b in bs for e in b['evaluations']]
 out={'schemaVersion':2,'kind':'ordivon.computing.discoverability-successor-negative-history-evaluations','rawControlsDigest':canonical_digest(DATA),'evaluations':es,'batches':[{k:v for k,v in b.items() if k!='evaluations'} for b in bs],'apparatusEvents':apparatus,'reliabilityRepair':'per-case durable partial; at most one identical-contract retry after evaluator structure/coverage failure'}
 (ROOT/'successor-negative-history-evaluations-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 for e in es: print(e['caseId'],e['surface'],e['finalStatus'],'history',e['historicalRecovered'],'current',e['currentSuccessorOrRemovalRecovered'],'owner',e['currentOwnerResolved'],'risk',e['falseCurrentActivationRisk'],'escape',e['ownerNativeEscapeAvailable'])
 print('tokens',[b['usage'].get('totalTokens') for b in bs]); print('apparatusEvents',apparatus)
if __name__=='__main__': main()
