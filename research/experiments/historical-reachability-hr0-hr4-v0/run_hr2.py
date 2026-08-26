from __future__ import annotations
import argparse,json,random,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
EXTRACT_SCHEMA={"type":"object","additionalProperties":False,"properties":{
"beforeBlocker":{"type":"string"},"basisChange":{"type":"string"},"pathDelta":{"type":"string"},"remainingBoundary":{"type":"string"},"evidenceCeiling":{"type":"string"}},"required":["beforeBlocker","basisChange","pathDelta","remainingBoundary","evidenceCeiling"]}
JUDGE_SCHEMA={"type":"object","additionalProperties":False,"properties":{
"beforeBlockerEquivalent":{"type":"boolean"},"basisChangeEquivalent":{"type":"boolean"},"pathDeltaEquivalent":{"type":"boolean"},"remainingBoundaryEquivalent":{"type":"boolean"},"evidenceCeilingEquivalent":{"type":"boolean"},"replicateASourceGrounded":{"type":"boolean"},"replicateBSourceGrounded":{"type":"boolean"},"materialContradiction":{"type":"boolean"},"reason":{"type":"string"}},"required":["beforeBlockerEquivalent","basisChangeEquivalent","pathDeltaEquivalent","remainingBoundaryEquivalent","evidenceCeilingEquivalent","replicateASourceGrounded","replicateBSourceGrounded","materialContradiction","reason"]}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def run_prompt(prompt,schema,kind,rid_suffix,model,secret):
 now=time.time_ns()//1_000_000; settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=1200); completion={"mode":"structured-result-v1","resultKind":kind,"resultSchema":schema}; rid=f"harness-run:historical-reachability-hr2:{rid_suffix}:{now}"
 contract=HarnessRunContract(harness_run_id=rid,harness_implementation_id="ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f",caller_id="caller:ordivon-computing-historical-reachability-hr2",caller_run_ref=rid_suffix,objective_ref=ref(f"objective:{rid_suffix}:v1","objective",{"kind":kind}),context_refs=(ref(f"context:{rid_suffix}:v1","context",{"prompt":prompt}),),provider_id="provider:deepseek",adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=65536,max_wall_time_ms=120000,max_total_tokens=24576,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f"system:{rid_suffix}:v1","system-manifest",{"experiment":"historical-reachability-hr2","kind":kind}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content",allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix='hr2-') as state:
  run=HarnessAgentRun.create(state,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); ex=run.run(({"role":"user","content":prompt},)); c=ex.loop_result.conclusion; result=None if c is None else decode_structured_completion_result(contract,c); return {"result":result,"usage":ex.loop_result.usage,"stopCode":ex.loop_result.stop_code.value}
def extract_prompt(item):
 return "You are a skeptical historical research coder. Using ONLY the source-native trajectory, recover the minimal causal reachability delta. Do not assign taxonomy labels, innovation scores, future-importance scores, or current capability. beforeBlocker = what relation prevented the later path/question/service; basisChange = what materially changed that relation; pathDelta = what path/question/action became newly open, closed, or moved; remainingBoundary = what still did not follow; evidenceCeiling = the strongest claim this historical packet can support and what it cannot support. If the source is too thin, say so explicitly. Return only structured output.\n\nSOURCE:\n"+json.dumps(item['record'],ensure_ascii=False,sort_keys=True)
def judge_prompt(item,a,b):
 return "You are an independent skeptical adjudicator. Compare two causal-delta extractions against the SAME source-native trajectory. Semantic paraphrases count as equivalent; do not require word overlap. Mark each field equivalent only if the two outputs identify materially the same causal relation at compatible scope. Source-grounded means the output does not invent material facts or lift the history beyond its evidence. materialContradiction means the two replicas assert incompatible load-bearing causal stories, not merely different levels of detail. Return only structured output.\n\nSOURCE:\n"+json.dumps(item['record'],ensure_ascii=False,sort_keys=True)+"\n\nA:\n"+json.dumps(a,ensure_ascii=False,sort_keys=True)+"\n\nB:\n"+json.dumps(b,ensure_ascii=False,sort_keys=True)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--phase',choices=['extract','judge'],required=True); ap.add_argument('--output',required=True); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); ap.add_argument('--model',default='deepseek-v4-flash'); ap.add_argument('--seed',type=int,default=2026082611); args=ap.parse_args()
 source=json.loads((ROOT/'hr0-source-freeze-v0.json').read_text()); con=json.loads((ROOT/'hr2-contract.json').read_text()); selected=set(con['selectedTrajectories']); items=[x for x in source['records'] if x['trajectoryId'] in selected]; assert len(items)==10; by={x['trajectoryId']:x for x in items}; out=Path(args.output)
 if args.phase=='extract':
  full_schedule=[(x,r) for x in items for r in (1,2)]; random.Random(args.seed).shuffle(full_schedule); rows=[]
  if out.exists():
   prior=json.loads(out.read_text())
   if prior.get('contractDigest')!=canonical_digest(con) or prior.get('sourceFreezeDigest')!=canonical_digest(source): raise RuntimeError('refusing resume: digest mismatch')
   rows=list(prior.get('rows',[]))
  done={(r.get('trajectoryId'),r.get('replicate')) for r in rows if r.get('result') is not None}
  schedule=[(x,r) for x,r in full_schedule if (x['trajectoryId'],r) not in done]
  for n,(item,r) in enumerate(schedule,1):
   try: z=run_prompt(extract_prompt(item),EXTRACT_SCHEMA,'historical-reachability-hr2-extract-v0',f"extract:{item['trajectoryId']}:r{r}",args.model,Path(args.secret)); row={"trajectoryId":item['trajectoryId'],"recordDigest":item['recordDigest'],"replicate":r,**z}
   except Exception as e: row={"trajectoryId":item['trajectoryId'],"recordDigest":item['recordDigest'],"replicate":r,"result":None,"errorType":type(e).__name__,"error":str(e)[:1200]}
   rows=[q for q in rows if not (q.get('trajectoryId')==item['trajectoryId'] and q.get('replicate')==r)] + [row]
   out.write_text(json.dumps({"schemaVersion":1,"kind":"ordivon.computing.historical-reachability-hr2-extract-live-v0","contractDigest":canonical_digest(con),"sourceFreezeDigest":canonical_digest(source),"plannedTrials":20,"completedTrials":len(rows),"rows":rows},ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({"n":n,"remainingAtStart":len(schedule),"completed":len(rows),"tid":item['trajectoryId'],"r":r,"result":row.get('result'),"error":row.get('error')},ensure_ascii=False),flush=True)
 else:
  exdata=json.loads((ROOT/'hr2-extract-live-v0.json').read_text()); grouped={}
  for r in exdata['rows']:
   if r.get('result') is not None: grouped.setdefault(r['trajectoryId'],{})[r['replicate']]=r['result']
  tids=[t for t in con['selectedTrajectories'] if set(grouped.get(t,{}))=={1,2}]; rows=[]
  for n,tid in enumerate(tids,1):
   try: z=run_prompt(judge_prompt(by[tid],grouped[tid][1],grouped[tid][2]),JUDGE_SCHEMA,'historical-reachability-hr2-judge-v0',f"judge:{tid}",args.model,Path(args.secret)); row={"trajectoryId":tid,**z}
   except Exception as e: row={"trajectoryId":tid,"result":None,"errorType":type(e).__name__,"error":str(e)[:1200]}
   rows.append(row); out.write_text(json.dumps({"schemaVersion":1,"kind":"ordivon.computing.historical-reachability-hr2-judge-live-v0","contractDigest":canonical_digest(con),"extractDigest":canonical_digest(exdata),"plannedTrials":len(tids),"completedTrials":len(rows),"rows":rows},ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({"n":n,"tid":tid,"result":row.get('result'),"error":row.get('error')},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
