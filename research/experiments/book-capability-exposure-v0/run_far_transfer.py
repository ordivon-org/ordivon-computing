from __future__ import annotations
import argparse,json,hashlib,shutil,time
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,DeepSeekSettings,DeepSeekTurnAdapter
ROOT=Path(__file__).resolve().parent

def render_cases():
    battery=json.loads((ROOT/'far-transfer.json').read_text())
    out=[]
    for c in battery['cases']:
        out.append(f"{c['id']}\nEvidence: {c['evidence']}\nQuestion: {c['q']}\n"+'\n'.join(f"  {k}. {v}" for k,v in c['options'].items()))
    return battery,'\n\n'.join(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--arm',required=True,choices=['NOBOOK','BASELINE','REORDER','GESTALT','GESTALT_ONLY']); ap.add_argument('--replicate',type=int,required=True); a=ap.parse_args()
    battery,cases=render_cases(); book='' if a.arm=='NOBOOK' else (ROOT/f'{a.arm}.mdx').read_text(encoding='utf-8')
    instruction=('你是 fresh Agent。目标不是复述理论，而是对 10 个陌生 case 做最可靠的 operation/action routing。每题只选一个选项。所有 case evidence 都是本实验冻结的当前/合成 evidence；Book（若提供）只是非权威 representation，不能覆盖 case evidence。最终必须调用 submit_run_conclusion，summary 必须严格采用如下格式并包含全部 10 行：\nF1=B | <最多20中文字的理由>\n...\nF10=B | <理由>\n不要在 summary 之外输出答案，不要遗漏 case，不要为了与 Book 一致而牺牲 owner evidence。')
    context=('没有提供 Book；只根据 case evidence 与一般推理作答。' if a.arm=='NOBOOK' else '以下是非权威 Book projection：\n---BOOK---\n'+book+'\n---END BOOK---')
    prompt=instruction+'\n\n'+context+'\n\n---CASES---\n'+cases
    run_id=f'harness-run:book-capexp-far-transfer-{a.arm.lower()}-{a.replicate}-{int(time.time()*1000)}'; now=int(time.time()*1000)
    bhash='none' if not book else hashlib.sha256(book.encode()).hexdigest(); bdigest='sha256:'+hashlib.sha256((ROOT/'far-transfer.json').read_bytes()).hexdigest()
    contract=HarnessRunContract(harness_run_id=run_id,harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:book-capability-far-transfer-v0',caller_run_ref=f'trial:far-transfer:{a.arm}:{a.replicate}',objective_ref=HarnessBoundReference('objective:far-transfer-routing','objective',canonical_digest(instruction)),context_refs=(HarnessBoundReference(f'book:{a.arm.lower()}','book-projection',('sha256:'+bhash if bhash!='none' else canonical_digest({'arm':'NOBOOK'}))),HarnessBoundReference('battery:far-transfer-v0','far-transfer-battery',bdigest)),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id='deepseek-v4-flash',tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget={'maxModelCalls':1,'maxToolCalls':1,'maxObservationBytes':4096,'maxWallTimeMs':120000,'maxTotalTokens':320000,'maxModelRetries':1,'maxToolCorrections':1,'maxConclusionCorrections':2,'maxObservationOnlyTurns':1,'maxNoProgressTurns':1},completion_contract={'mode':'record'},system_manifest_ref=HarnessBoundReference('manifest:far-transfer-v0','system-manifest',canonical_digest({'model':'deepseek-v4-flash','tools':0,'harness':'684333be5146d4f705a91edb396e83c6a1150e1f'})),created_at_ms=now,source_refs=(HarnessBoundReference('source:far-transfer-battery','experiment',bdigest),),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False),deadline_ms=now+180000)
    state=ROOT/'.far-transfer-state'/run_id.replace(':','_'); settings=DeepSeekSettings.from_secret_file(max_output_tokens=1800,timeout_seconds=120.0); handle=HarnessAgentRun.create(state,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); exc=handle.run(({'role':'user','content':prompt},)); con=exc.loop_result.conclusion; summary=None if con is None else con.summary
    print(json.dumps({'arm':a.arm,'replicate':a.replicate,'runId':run_id,'stopCode':exc.loop_result.stop_code.value,'summary':summary,'usage':dict(exc.loop_result.usage),'bookSha256':bhash,'batterySha256':bdigest},ensure_ascii=False)); shutil.rmtree(state,ignore_errors=True)
if __name__=='__main__':main()
