from __future__ import annotations
import argparse, json, shutil, time, hashlib
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import (
    HarnessAgentRun, HarnessBoundReference, HarnessPrivacyPolicy, HarnessRunContract,
    NO_TOOL_AGENT_GRANT_DIGEST, NO_TOOL_AGENT_SURFACE_DIGEST,
    DeepSeekSettings, DeepSeekTurnAdapter,
)
ROOT=Path(__file__).resolve().parent
QUESTION='你是一个第一次接触 Ordivon Book 的强 Agent。只根据下面这本 Book，回答一个问题：这套系统/有限智能现在因此能够可靠地做哪些以前不能稳定做到的事情？请优先描述已经由书中结构真正支持的 capability，而不是重复“什么不能推出”。同时必须保留 scope、authority、currentness、maturity 和 non-claim 边界。不要使用你在问题外知道的 Ordivon 历史。输出 700–1200 个中文字符的一段高密度能力模型；若某能力只是研究性/条件性的，要明确写出。不要按章节复述，也不要为了积极而夸大。直接把完整能力模型写在普通 assistant content 中；最后可附一个很短的 conclusion summary。'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--arm',required=True,choices=['BASELINE','REORDER','GESTALT']); ap.add_argument('--replicate',type=int,required=True); args=ap.parse_args()
    book=(ROOT/f'{args.arm}.mdx').read_text(encoding='utf-8')
    run_id=f'harness-run:book-capexp-v1b-{args.arm.lower()}-{args.replicate}-{int(time.time()*1000)}'; created=int(time.time()*1000)
    prompt=QUESTION+'\n\n--- BEGIN BOOK ---\n'+book+'\n--- END BOOK ---'
    contract=HarnessRunContract(
      harness_run_id=run_id,harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:book-capability-exposure-v1b',caller_run_ref=f'trial:book-capability-exposure-v1b:{args.arm}:{args.replicate}',
      objective_ref=HarnessBoundReference('objective:capability-recovery-v1b','objective',canonical_digest(QUESTION)),context_refs=(HarnessBoundReference(f'book:{args.arm.lower()}','book-projection','sha256:'+hashlib.sha256(book.encode()).hexdigest()),),
      provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id='deepseek-v4-flash',tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
      budget={'maxModelCalls':1,'maxToolCalls':1,'maxObservationBytes':4096,'maxWallTimeMs':120000,'maxTotalTokens':300000,'maxModelRetries':1,'maxToolCorrections':1,'maxConclusionCorrections':2,'maxObservationOnlyTurns':1,'maxNoProgressTurns':1},
      completion_contract={'mode':'record'},system_manifest_ref=HarnessBoundReference('manifest:book-capexp-v1b','system-manifest',canonical_digest({'harnessRevision':'684333be5146d4f705a91edb396e83c6a1150e1f','model':'deepseek-v4-flash','tools':0,'semanticCarrier':'assistant-content'})),created_at_ms=created,
      source_refs=(HarnessBoundReference('source:media-book','git-book',canonical_digest({'mediaRevision':'9aa03e1eef97093af772c9020e66bee231ad1cfe','bookSha256':'799af49c40d0e4162cc0c7cfdeebf563b0c915157a97fd789004ea388fff23b1'})),),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False),deadline_ms=created+180000)
    state=ROOT/'.state-v1b'/run_id.replace(':','_'); settings=DeepSeekSettings.from_secret_file(max_output_tokens=2048,timeout_seconds=120.0)
    handle=HarnessAgentRun.create(state,contract,lambda exact: DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); exc=handle.run(({'role':'user','content':prompt},))
    assistant=[m.get('content') for m in exc.loop_result.messages if m.get('role')=='assistant' and isinstance(m.get('content'),str)]
    content=assistant[-1] if assistant else None; conclusion=exc.loop_result.conclusion
    summary=None if conclusion is None else conclusion.summary
    semantic=max([x for x in [content,summary] if isinstance(x,str)], key=len, default=None)
    row={'arm':args.arm,'replicate':args.replicate,'runId':run_id,'stopCode':exc.loop_result.stop_code.value,'usage':dict(exc.loop_result.usage),'capabilityModel':semantic,'assistantContent':content,'conclusionSummary':summary,'bookSha256':hashlib.sha256(book.encode()).hexdigest()}
    print(json.dumps(row,ensure_ascii=False)); shutil.rmtree(state,ignore_errors=True)
if __name__=='__main__': main()
