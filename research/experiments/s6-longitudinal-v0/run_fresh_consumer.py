from __future__ import annotations
import json,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
SCHEMA={"type":"object","additionalProperties":False,"properties":{
"boundedLocalS6Established":{"type":"boolean"},"systemWideAutonomousRatchetEstablished":{"type":"boolean"},"monthOrYearHorizonEstablished":{"type":"boolean"},"survivalAloneEstablishesBenefit":{"type":"boolean"},"challengeRebindCanBePositiveS6Evidence":{"type":"boolean"},"financeHistoricalBranchCausesCurrentWorldBoundCapabilityEstablished":{"type":"boolean"},"harnessClaimStandingProductionRealizedBenefitEstablished":{"type":"boolean"},"deletionOrNoChangeCanBePositiveConsequence":{"type":"boolean"},"nextParentFrontier":{"type":"string"},"rationale":{"type":"string"}},"required":["boundedLocalS6Established","systemWideAutonomousRatchetEstablished","monthOrYearHorizonEstablished","survivalAloneEstablishesBenefit","challengeRebindCanBePositiveS6Evidence","financeHistoricalBranchCausesCurrentWorldBoundCapabilityEstablished","harnessClaimStandingProductionRealizedBenefitEstablished","deletionOrNoChangeCanBePositiveConsequence","nextParentFrontier","rationale"]}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def run(rep):
    cases=json.loads((ROOT/'case-results-v1.json').read_text())
    contract=json.loads((ROOT/'fresh-consumer-contract.json').read_text())
    packet={"truthRole":"source-bound-audit-result-projection-not-owner-truth","caseResults":cases["cases"],"globalNonClaims":cases["globalNonClaims"]}
    prompt="You are a fresh finite research-method consumer with no prior Ordivon memory. Read the source-bound S6 audit result projection. Recover only the bounded system-level standing supported by the packet. Do not treat survival/citation/test pass as benefit, do not attribute current Finance capability to an unmerged historical branch, do not upgrade Harness research validation to production benefit, and do not infer a cumulative ratchet or month/year horizon. Return the exact structured result requested.\n\nPACKET:\n"+json.dumps(packet,ensure_ascii=False,sort_keys=True)
    completion={"mode":"structured-result-v1","resultKind":"s6-fresh-consumer-v1","resultSchema":SCHEMA}
    settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=900)
    now=time.time_ns()//1_000_000; rid=f"harness-run:s6-longitudinal-v0:r{rep}:{now}"
    c=HarnessRunContract(harness_run_id=rid,harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-s6-audit',caller_run_ref=f's6-longitudinal-v0|r{rep}',objective_ref=ref(f'objective:s6-longitudinal-v0:r{rep}','objective',{"target":"recover bounded S6 standing"}),context_refs=(ref(f'context:s6-longitudinal-v0:r{rep}','context',{"prompt":prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=120000,max_total_tokens=24000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f'system:s6-longitudinal-v0:r{rep}','system-manifest',{"experiment":"s6-longitudinal-v0","role":"representation-check-only"}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
    with tempfile.TemporaryDirectory(prefix='s6-fresh-consumer-') as state:
        ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({"role":"user","content":prompt},))
        result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
    expected=contract['acceptanceVector']; check={k:result.get(k)==v for k,v in expected.items()} if result else {}
    return {"replicate":rep,"result":result,"matches":check,"exact":bool(check) and all(check.values()),"usage":ex.loop_result.usage,"stopCode":ex.loop_result.stop_code.value}
def main():
    rows=[run(i) for i in range(1,4)]
    out={"schemaVersion":1,"kind":"ordivon.computing.s6-fresh-consumer-result","contractDigest":canonical_digest(json.loads((ROOT/'fresh-consumer-contract.json').read_text())),"caseResultsDigest":canonical_digest(json.loads((ROOT/'case-results-v1.json').read_text())),"rows":rows,"exactReplicates":sum(r['exact'] for r in rows)}
    (ROOT/'fresh-consumer-result-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"exactReplicates":out['exactReplicates'],"rows":[{"replicate":r['replicate'],"exact":r['exact'],"result":r['result'],"usage":r['usage']} for r in rows]},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
