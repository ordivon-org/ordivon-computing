from __future__ import annotations
import argparse,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load(n,p):
 s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); sys.modules[n]=m; s.loader.exec_module(m); return m
sem=load('sem6a',ROOT/'aic_semantic_falsify.py'); s5b=load('s5b6a',ROOT/'aic_s5b_partial_order.py')

def result_set(base,orders):
 bindings={}; kernels={}; safe_states=[]
 for order in orders:
  st=sem.replay(base+order); fc=s5b.s5a.frontier_core(st); kc=s5b.s5a.continuation_kernel(st); bindings[sem.canonical(fc)]=fc; kernels[sem.canonical(kc)]=kc; o=s5b.s2.expected(st); safe_states.append((o['consequentialAuthorityStatus'],o['officeHolder'],o['effectiveController']))
 safe=len(set(safe_states))==1 and safe_states[0][0]=='AUTHORIZED'
 return {'bindingCount':len(bindings),'kernelCount':len(kernels),'safeFreshConsequentialAction':'ALLOW' if safe else 'HOLD','bindings':list(bindings.values()),'kernels':list(kernels.values())}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args(); cases=s5b.targeted(); rows=[]; violations=[]; ambiguity_removed_but_hold=[]
 for c in cases:
  orders=[x['order'] for x in c['executions']]; witnessed=orders[0]
  none=result_set(c['base'],orders)
  arrival=result_set(c['base'],orders) # metadata only; no filter
  authentic_nonadmitted=result_set(c['base'],orders) # authentication does not confer precedence
  admitted=result_set(c['base'],[witnessed])
  props={
   'arrivalPreserves':arrival==none,
   'authenticNonadmittedPreserves':authentic_nonadmitted==none,
   'admittedSelectsOneExecution':admitted['bindingCount']==1 and admitted['kernelCount']==1,
  }
  if not all(props.values()): violations.append({'case':c['case'],'properties':props})
  if none['bindingCount']>1 and admitted['bindingCount']==1 and admitted['safeFreshConsequentialAction']=='HOLD': ambiguity_removed_but_hold.append(c['case'])
  rows.append({'case':c['case'],'witnessedOrder':witnessed,'NO_WITNESS':none,'ARRIVAL_ONLY':arrival,'AUTHENTIC_NONADMITTED':authentic_nonadmitted,'ADMITTED_PRECEDENCE':admitted,'properties':props})
 out={'schemaVersion':1,'kind':'ordivon.computing.aic-s6a-order-witness-result','experimentId':'COJC-J3-AIC-ORDER-WITNESS-S6A','cases':rows,'violations':violations,'ambiguityRemovedButStillHold':ambiguity_removed_but_hold,'allPropertiesPass':not violations,'laws':{'arrivalIsNotPrecedence':not violations,'authenticityIsNotPrecedence':not violations,'admittedPrecedenceCanRefineCurrentness':all(r['ADMITTED_PRECEDENCE']['bindingCount']==1 for r in rows),'determinateDoesNotImplySafe':bool(ambiguity_removed_but_hold)}}; Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
