from __future__ import annotations
import json, os, pathlib, sys, time, urllib.request, urllib.error, glob
import duckdb
ROOT=pathlib.Path(__file__).resolve().parent
FROZEN=json.loads((ROOT/'frozen-evidence.json').read_text())
TARGETS=['SPY','QQQ','XAU','SMH']; DATASETS=['holdability','wrapper_screen','instruments','funding_settlements','swap_daily_bars','index_daily_bars']
ORACLE=FROZEN['oracle']
LEADERS=TARGETS+['unknown']; ADM=['broad-shortlist','secondary-research','wrapper-rejected','blocked','unknown']; YN=['yes','no','unknown']
QUESTION='''Using only the frozen Finance evidence available through inspect_dataset, reconstruct the current descriptive wrapper-research state for SPY, QQQ, XAU, and SMH. Return: leader by latest holdability funding_annualized_pct; leader by latest holdability tracking_error_annualized_pct; leader by historical mean absolute funding_rate; whether all four latest instrument states are live; each symbol's current wrapper admission; whether all four latest swap bars are confirmed; whether all four latest index bars are confirmed; whether the latest swap/index bar event time is uniform across all four; and whether the latest holdability funding leader matches the historical mean-absolute-funding leader. This is evidence-state reconstruction, not an investment recommendation.'''

def tool_schema(include_submit: bool):
 tools=[{'type':'function','function':{'name':'inspect_dataset','description':'Inspect one frozen Finance dataset summary. One call is one physical observation. Each dataset may be inspected independently.','parameters':{'type':'object','properties':{'dataset':{'type':'string','enum':DATASETS}},'required':['dataset'],'additionalProperties':False}}}]
 if include_submit: tools.append(submit_tool())
 return tools
def submit_tool(name='submit'):
 props={
 'latestHoldabilityFundingLeader':{'type':'string','enum':LEADERS},'latestTrackingErrorLeader':{'type':'string','enum':LEADERS},'historicalMeanAbsFundingLeader':{'type':'string','enum':LEADERS},
 'allInstrumentStatesLive':{'type':'string','enum':YN},'admissionSPY':{'type':'string','enum':ADM},'admissionQQQ':{'type':'string','enum':ADM},'admissionXAU':{'type':'string','enum':ADM},'admissionSMH':{'type':'string','enum':ADM},
 'latestSwapBarsAllConfirmed':{'type':'string','enum':YN},'latestIndexBarsAllConfirmed':{'type':'string','enum':YN},'latestBarEventTimeUniform':{'type':'string','enum':YN},'latestFundingLeaderMatchesHistoricalAbsFundingLeader':{'type':'string','enum':YN},'summary':{'type':'string'},'unresolved':{'type':'array','items':{'type':'string'},'maxItems':12}}
 return {'type':'function','function':{'name':name,'description':'Submit the structured Finance evidence-state model. Use unknown when the observed evidence does not justify a field.','parameters':{'type':'object','properties':props,'required':list(props),'additionalProperties':False}}}
def sec(rep):
 paths=sorted(pathlib.Path('/root/.config/ordivon/secrets').glob('deepseek*.json')); return json.loads(paths[(rep-1)%len(paths)].read_text())
def call(messages,tools,secret,max_tokens=5500):
 body={'model':secret['model'],'messages':messages,'tools':tools,'tool_choice':'required','parallel_tool_calls':False,'thinking':{'type':'disabled'},'max_tokens':max_tokens,'stream':False}; data=json.dumps(body,separators=(',',':')).encode(); retries=0; started=time.time_ns()
 while True:
  req=urllib.request.Request(str(secret['baseUrl']).rstrip('/')+'/chat/completions',data=data,headers={'Authorization':'Bearer '+str(secret['apiKey']),'Content-Type':'application/json','User-Agent':'ordivon-p9-finance/1'},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=180) as r: payload=json.loads(r.read(4194304))
  except (urllib.error.URLError,TimeoutError,OSError):
   retries+=1
   if retries>2: raise
   time.sleep(.5*retries); continue
  msg=payload['choices'][0]['message']; calls=msg.get('tool_calls') or []
  if not calls:
   retries+=1
   if retries>2: raise RuntimeError('provider returned no tool call')
   continue
  u=payload.get('usage') or {}; usage={'promptTokens':int(u.get('prompt_tokens',0) or 0),'completionTokens':int(u.get('completion_tokens',0) or 0),'totalTokens':int(u.get('total_tokens',0) or 0),'providerCalls':retries+1,'elapsedMs':(time.time_ns()-started)//1_000_000}
  return msg,calls,usage
def normalize_oracle():
 return {k:('yes' if v is True else 'no' if v is False else v) for k,v in ORACLE.items()}
NORACLE=normalize_oracle()
def inspect(ds):
 # Execute against frozen Parquet snapshot each time; the precomputed frozen-evidence file is only the hidden oracle.
 base=ROOT/'snapshot'/ds; files=glob.glob(str(base/'*.parquet')); con=duckdb.connect(':memory:'); rel='read_parquet(['+','.join(repr(f) for f in files)+'])'; inst=[f'{x}-USDT-SWAP' for x in TARGETS]
 if ds=='holdability': q=f'''WITH x AS (SELECT *, row_number() over(partition by inst_id order by observed_at desc,event_time desc) rn FROM {rel} WHERE inst_id IN ({','.join(repr(x) for x in inst)})) SELECT inst_id,event_time,observed_at,round(funding_annualized_pct,6) AS funding_annualized_pct,round(tracking_error_annualized_pct,6) AS tracking_error_annualized_pct FROM x WHERE rn=1 ORDER BY inst_id'''
 elif ds=='wrapper_screen': q=f'''WITH x AS (SELECT *, row_number() over(partition by symbol order by observed_at desc,event_time desc) rn FROM {rel} WHERE symbol IN ({','.join(repr(x) for x in TARGETS)})) SELECT symbol,inst_id,admission,round(wrapper_score,6) AS wrapper_score,round(funding_annualized_pct,6) AS funding_annualized_pct,event_time,observed_at FROM x WHERE rn=1 ORDER BY symbol'''
 elif ds=='instruments': q=f'''WITH x AS (SELECT *, row_number() over(partition by symbol order by observed_at desc,event_time desc) rn FROM {rel} WHERE symbol IN ({','.join(repr(x) for x in TARGETS)})) SELECT symbol,inst_id,state,inst_category,event_time,observed_at FROM x WHERE rn=1 ORDER BY symbol'''
 elif ds=='funding_settlements': q=f'''WITH d AS (SELECT *, row_number() over(partition by inst_id,event_time order by observed_at desc) rn FROM {rel} WHERE inst_id IN ({','.join(repr(x) for x in inst)})), x AS (SELECT * FROM d WHERE rn=1) SELECT inst_id,count(*) AS settlements,round(avg(funding_rate),9) AS mean_funding_rate,round(avg(abs(funding_rate)),9) AS mean_abs_funding_rate,round(sum(funding_rate),9) AS cumulative_funding_rate,min(event_time) AS min_event,max(event_time) AS max_event FROM x GROUP BY inst_id ORDER BY inst_id'''
 else:
  idcol='inst_id' if ds=='swap_daily_bars' else 'subject_inst_id'; q=f'''WITH d AS (SELECT *, row_number() over(partition by {idcol},event_time order by observed_at desc) rn FROM {rel} WHERE {idcol} IN ({','.join(repr(x) for x in inst)})), x AS (SELECT * FROM d WHERE rn=1), latest AS (SELECT *, row_number() over(partition by {idcol} order by event_time desc) latest_rn FROM x) SELECT {idcol} AS inst_id,event_time,observed_at,confirm,round("close",6) AS close_value,(SELECT count(*) FROM x x2 WHERE x2.{idcol}=latest.{idcol}) AS deduped_bar_count,(SELECT sum(CASE WHEN confirm='1' THEN 1 ELSE 0 END) FROM x x3 WHERE x3.{idcol}=latest.{idcol}) AS confirmed_bar_count FROM latest WHERE latest_rn=1 ORDER BY inst_id'''
 cur=con.execute(q); names=[d[0] for d in cur.description]; rows=[dict(zip(names,r)) for r in cur.fetchall()]; con.close(); return json.dumps({'dataset':ds,'rows':rows},sort_keys=True,separators=(',',':'),default=str)
def validate_candidate(x):
 if not isinstance(x,dict): return False
 for k in ['latestHoldabilityFundingLeader','latestTrackingErrorLeader','historicalMeanAbsFundingLeader']:
  if x.get(k) not in LEADERS:return False
 for k in ['allInstrumentStatesLive','latestSwapBarsAllConfirmed','latestIndexBarsAllConfirmed','latestBarEventTimeUniform','latestFundingLeaderMatchesHistoricalAbsFundingLeader']:
  if x.get(k) not in YN:return False
 for k in ['admissionSPY','admissionQQQ','admissionXAU','admissionSMH']:
  if x.get(k) not in ADM:return False
 return isinstance(x.get('summary'),str) and isinstance(x.get('unresolved'),list)
def score(x):
 fields=list(NORACLE); correct={k:x.get(k)==NORACLE[k] for k in fields}; return {'strictAccepted':all(correct.values()),'correctFields':sum(correct.values()),'fieldCount':len(fields),'falseFields':[k for k,v in correct.items() if not v]}
def synth(observations,secret):
 evidence='\n\n'.join(f"O{i+1} {o['dataset']}\n{o['output']}" for i,o in enumerate(observations)) or '(no observations)'
 msgs=[{'role':'system','content':'You are a fresh Finance evidence synthesizer. Use only the supplied frozen dataset observations. Unknown is correct when a requested field is not justified. Do not infer investment attractiveness, future returns, or hidden rows. Submit exactly one structured candidate.'},{'role':'user','content':QUESTION+'\n\nOBSERVATIONS:\n'+evidence}]
 total={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; diagnostics=[]
 for attempt in range(3):
  msg,calls,u=call(msgs,[submit_tool('candidate')],secret); [total.__setitem__(k,total[k]+u[k]) for k in total]
  try: a=json.loads(calls[0]['function']['arguments'])
  except Exception as e:a={}; diagnostics.append('json:'+repr(e))
  if calls[0].get('function',{}).get('name')=='candidate' and validate_candidate(a): return a,total,diagnostics
  diagnostics.append('schema-invalid'); msgs.append({'role':'user','content':'Protocol error only: re-emit the same evidence interpretation with exact schema enum values and JSON types.'})
 raise RuntimeError('candidate protocol invalid')
def add_usage(total,u):
 for k in total: total[k]+=u[k]
def run_checkpoint(target,rep):
 secret=sec(rep); msgs=[{'role':'system','content':'You are the Finance evidence-acquisition Agent. The frozen universe has exactly six inspectable datasets: '+', '.join(DATASETS)+'. Inspect datasets that discriminate the requested fields. One inspect call is one observation. Do not repeat a dataset unless repetition could add information; the frozen snapshot does not change.'},{'role':'user','content':QUESTION}]
 obs=[]; usage={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}
 while len(obs)<target:
  msg,calls,u=call(msgs,tool_schema(False),secret); add_usage(usage,u); c=calls[0]; fn=c.get('function') or {}; a=json.loads(fn.get('arguments') or '{}'); ds=a.get('dataset')
  if fn.get('name')!='inspect_dataset' or ds not in DATASETS: raise RuntimeError('invalid inspect tool call')
  out=inspect(ds); obs.append({'dataset':ds,'output':out}); msgs.append({'role':'assistant','content':None,'tool_calls':[c]}); msgs.append({'role':'tool','tool_call_id':c['id'],'content':out})
 final,su,diag=synth(obs,secret); add_usage(usage,su)
 return {'schemaVersion':1,'kind':'ordivon.computing.p9-finance-checkpoint-trial','mode':'checkpoint','checkpoint':target,'replicate':rep,'observations':obs,'observationCount':len(obs),'uniqueDatasets':sorted(set(o['dataset'] for o in obs)),'final':final,'metrics':score(final),'protocolDiagnostics':diag,'usage':usage}
def run_selfstop(rep):
 secret=sec(rep); msgs=[{'role':'system','content':'You are the Finance evidence-acquisition Agent. The frozen universe has exactly six inspectable datasets: '+', '.join(DATASETS)+'. Inspect only what you need, then submit when the requested evidence-state model is justified. The snapshot does not change, so repeating a dataset adds no evidence. Unknown is allowed for fields you cannot justify.'},{'role':'user','content':QUESTION}]
 obs=[]; usage={'promptTokens':0,'completionTokens':0,'totalTokens':0,'providerCalls':0,'elapsedMs':0}; final=None
 for _ in range(8):
  msg,calls,u=call(msgs,tool_schema(True),secret); add_usage(usage,u); c=calls[0]; fn=c.get('function') or {}; a=json.loads(fn.get('arguments') or '{}'); name=fn.get('name')
  if name=='submit':
   if not validate_candidate(a): raise RuntimeError('invalid submit candidate')
   final=a; break
  if name!='inspect_dataset' or a.get('dataset') not in DATASETS: raise RuntimeError('invalid tool')
  ds=a['dataset']; out=inspect(ds); obs.append({'dataset':ds,'output':out}); msgs.append({'role':'assistant','content':None,'tool_calls':[c]}); msgs.append({'role':'tool','tool_call_id':c['id'],'content':out})
 result={'schemaVersion':1,'kind':'ordivon.computing.p9-finance-selfstop-trial','mode':'selfstop','replicate':rep,'observations':obs,'observationCount':len(obs),'uniqueDatasets':sorted(set(o['dataset'] for o in obs)),'submitted':final is not None,'final':final,'metrics':{'strictAccepted':False,'correctFields':0,'fieldCount':len(NORACLE),'falseFields':['no-submit']} if final is None else score(final),'usage':usage}; return result
def main():
 mode=sys.argv[1]; rep=int(os.environ.get('ORDIVON_REPLICATE','1')); result=run_selfstop(rep) if mode=='selfstop' else run_checkpoint(int(sys.argv[2]),rep); print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
