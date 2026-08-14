from __future__ import annotations
import json,tempfile
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.ordivon.loop import OrdivonAgentLoop,RunStopCode
from ordivon_harness.ordivon.model import AgentTurnRequest,AgentTurnResult,ScriptedTurnAdapter
from ordivon_harness.ordivon.sqlite_run_store import SQLiteHarnessRunContinuityStore
from ordivon_harness.ordivon.sqlite_runtime_bridge import SQLiteHarnessRuntimeBridge
from ordivon_harness.sqlite_store import SQLiteHarnessStore
from ordivon_harness.working_view import AgentCallerIngressPromotionProposal,AgentWorkingSetTransitionProposal,HarnessWorkingSetPin,HarnessWorkingSetSpec,HarnessWorkingViewSource,WorkingSetViewProjector
from tests.test_p0_sqlite_runtime_bridge import FakeRuntime,FixedClock,execution_binding
from tests.test_pc111_interaction_durable_promotion import promotion_turn
from tests.test_pc14_candidate_discovery_overlay import transition_turn
from tests.test_pc15_epistemic_control import needs_input_turn,private_contract,run_budget
ROOT=Path(__file__).resolve().parent
ARMS=['none','promotion_only','addressability_only','both']

def initialize(root:Path,c:dict,arm:str):
 suffix=f"f12-{c['caseId']}-{arm}"
 contract=private_contract(suffix,max_model_calls=8,max_tool_calls=0)
 store=SQLiteHarnessStore.initialize(root); store.create_run(contract); clock=FixedClock(); continuity=SQLiteHarnessRunContinuityStore(store,contract,clock_ms=clock)
 task=HarnessWorkingViewSource(logical_ref=f"source://f12/{c['caseId']}/task",logical_generation='generation:task',messages=({'role':'user','content':f"F12_TASK {c['caseId']}: keep the task context selected."},))
 stale=HarnessWorkingViewSource(logical_ref=f"source://f12/{c['caseId']}/stale",logical_generation='generation:stale',messages=({'role':'user','content':c['staleText']},))
 to=continuity.store_working_view_source(task); so=continuity.store_working_view_source(stale)
 tp=HarnessWorkingSetPin(slot='task',logical_ref=task.logical_ref,logical_generation=task.logical_generation,resolved_digest=to.digest)
 sp=HarnessWorkingSetPin(slot=c['staleSlot'],logical_ref=stale.logical_ref,logical_generation=stale.logical_generation,resolved_digest=so.digest)
 initial=HarnessWorkingSetSpec.initial(f"working-attempt:{suffix}-a",pins=tuple(sorted((tp,sp),key=lambda p:p.slot)))
 continuity.record_working_set(initial); continuity.record_working_set(initial.commit('seed task plus stale durable fact'))
 bridge=SQLiteHarnessRuntimeBridge(contract,continuity,execution_binding(contract,continuity),FakeRuntime('direct')); projector=WorkingSetViewProjector(store,continuity)
 pause_adapter=ScriptedTurnAdapter((needs_input_turn(f'{suffix}-pause','authoritative correction required'),))
 paused=OrdivonAgentLoop(pause_adapter,bridge,budget=run_budget(max_model_calls=8,max_tool_calls=0),clock_ms=clock,monotonic_ms=clock,working_view_projector=projector).run(harness_run_id=contract.harness_run_id,assignment_id=continuity.binding.assignment_id,context_digest=contract.context_refs[0].digest,initial_messages=({'role':'user','content':'canonical F12 root'},))
 assert paused.stop_code is RunStopCode.NEEDS_INPUT
 return store,clock,contract,continuity,projector,tp,sp,continuity.load_current_snapshot()

class AddressabilityOnlyAdapter:
 adapter_id=ScriptedTurnAdapter.adapter_id; model_id=ScriptedTurnAdapter.model_id; provider_request_digest=ScriptedTurnAdapter.provider_request_digest
 def __init__(self,c): self.c=c; self.i=0; self.requests=[]
 def invoke(self,request:AgentTurnRequest)->AgentTurnResult:
  self.requests.append(request); self.i+=1
  if self.i==1:
   by={r.pin.slot:r.pin for r in request.working_set_refs}; assert set(by)=={'task',self.c['staleSlot']}
   return transition_turn('f12-address-only',AgentWorkingSetTransitionProposal(next_attempt_id=f"working-attempt:f12-{self.c['caseId']}-address-b",pins=(by['task'],),basis='authoritative caller correction makes stale fact unsafe to keep, but caller bytes are not durable without promotion'))
  if self.i==2:return needs_input_turn('f12-address-only-boundary','cross interaction boundary')
  raise AssertionError('unexpected turn')

class BothAdapter:
 adapter_id=ScriptedTurnAdapter.adapter_id; model_id=ScriptedTurnAdapter.model_id; provider_request_digest=ScriptedTurnAdapter.provider_request_digest
 def __init__(self,c): self.c=c; self.i=0; self.requests=[]
 def invoke(self,request:AgentTurnRequest)->AgentTurnResult:
  self.requests.append(request); self.i+=1
  if self.i==1:
   return promotion_turn('f12-both-promote',AgentCallerIngressPromotionProposal(next_attempt_id=f"working-attempt:f12-{self.c['caseId']}-both-b",promotion_slot=self.c['correctedSlot'],caller_message_indexes=(0,),basis='preserve exact authoritative correction beyond this interaction'))
  if self.i==2:
   by={r.pin.slot:r.pin for r in request.working_set_refs}; assert set(by)=={'task',self.c['staleSlot'],self.c['correctedSlot']}
   pins=tuple(sorted((by['task'],by[self.c['correctedSlot']]),key=lambda p:p.slot))
   return transition_turn('f12-both-drop-stale',AgentWorkingSetTransitionProposal(next_attempt_id=f"working-attempt:f12-{self.c['caseId']}-both-c",pins=pins,basis='retain task plus durable correction and omit stale current fact'))
  if self.i==3:return needs_input_turn('f12-both-boundary','cross interaction boundary')
  raise AssertionError('unexpected turn')

def run_arm(c,arm):
 with tempfile.TemporaryDirectory(prefix=f"ordivon-pal-f12-{c['caseId']}-{arm}-") as td:
  store,clock,contract,continuity,projector,tp,sp,retained=initialize(Path(td)/'state',c,arm)
  try:
   if arm=='none':
    adapter=ScriptedTurnAdapter((needs_input_turn('f12-none-boundary','do not persist caller correction'),)); kwargs={}
   elif arm=='promotion_only':
    proposal=AgentCallerIngressPromotionProposal(next_attempt_id=f"working-attempt:f12-{c['caseId']}-promotion-b",promotion_slot=c['correctedSlot'],caller_message_indexes=(0,),basis='preserve exact authoritative correction beyond this interaction')
    adapter=ScriptedTurnAdapter((promotion_turn('f12-promotion-only',proposal),needs_input_turn('f12-promotion-boundary','cross interaction boundary'))); kwargs={'caller_ingress_promotion_handler':continuity}
   elif arm=='addressability_only': adapter=AddressabilityOnlyAdapter(c); kwargs={'working_set_transition_handler':continuity}
   elif arm=='both': adapter=BothAdapter(c); kwargs={'working_set_transition_handler':continuity,'caller_ingress_promotion_handler':continuity}
   else: raise ValueError(arm)
   bridge=SQLiteHarnessRuntimeBridge(contract,continuity,execution_binding(contract,continuity),FakeRuntime('direct'),provider_source=continuity.snapshot_provider_source(retained))
   res=OrdivonAgentLoop(adapter,bridge,budget=run_budget(max_model_calls=8,max_tool_calls=0),clock_ms=clock,monotonic_ms=clock,working_view_projector=projector,**kwargs).resume(retained=retained,assignment_id=continuity.binding.assignment_id,context_digest=contract.context_refs[0].digest,additional_messages=({'role':'user','content':c['correctionText']},))
   current=continuity.load_current_working_set(); view=projector.project(); slots={p.slot for p in current.pins}; text='\n'.join(str(m.get('content','')) for m in view.messages); hist=str(continuity.inspect_working_set_history(limit=32)); doctor=continuity.doctor()
   corrected=c['correctedSlot'] in slots and c['correctionText'] in text
   stale_absent=c['staleSlot'] not in slots and c['staleText'] not in text
   task_preserved='task' in slots
   stale_history=(sp in current.pins) or (sp.resolved_digest in hist)
   healthy=bool(doctor.get('healthy'))
   closure=all([corrected,stale_absent,task_preserved,stale_history,healthy,res.stop_code is RunStopCode.NEEDS_INPUT])
   return {'caseId':c['caseId'],'split':c['split'],'arm':arm,'A_promotion':arm in {'promotion_only','both'},'B_addressability':arm in {'addressability_only','both'},'stopCode':res.stop_code.value,'currentSlots':sorted(slots),'currentText':text,'correctedDurable':corrected,'staleAbsentCurrent':stale_absent,'taskPreserved':task_preserved,'staleHistoricalEvidencePreserved':stale_history,'continuityHealthy':healthy,'fullCorrectionClosure':closure,'staleDigest':sp.resolved_digest}
  finally: store.close()

def main():
 doc=json.load(open(ROOT/'f12-cases-v0.json')); rows=[]
 for c in doc['cases']:
  for arm in ARMS:
   row=run_arm(c,arm); rows.append(row); print(json.dumps(row,ensure_ascii=False),flush=True)
 out={'schemaVersion':1,'kind':'ordivon.computing.pal-f12-factorial-evidence','caseDigest':canonical_digest(doc),'rows':rows}
 (ROOT/'evidence'/'f12-factorial-v0.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'rows':len(rows),'digest':canonical_digest(out)},indent=2))
if __name__=='__main__':main()
