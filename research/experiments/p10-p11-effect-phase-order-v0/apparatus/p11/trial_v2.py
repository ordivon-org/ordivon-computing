from __future__ import annotations
import json,os,pathlib,sys,time,urllib.request,urllib.error,hashlib
ROOT=pathlib.Path(__file__).resolve().parent; F=json.loads((ROOT/'finance-evidence.json').read_text()); O=F['oracle']
TARGETS=['SPY','QQQ','XAU','SMH']; DATASETS=list(F['datasetSummaries'])
ORDERS={
'canonical':['holdability','wrapper_screen','instruments','funding_settlements','swap_daily_bars','index_daily_bars'],
'reverse':['index_daily_bars','swap_daily_bars','funding_settlements','instruments','wrapper_screen','holdability'],
'bars_first':['swap_daily_bars','index_daily_bars','funding_settlements','holdability','instruments','wrapper_screen'],
'identity_first':['instruments','wrapper_screen','holdability','funding_settlements','index_daily_bars','swap_daily_bars'],
'funding_first':['funding_settlements','holdability','wrapper_screen','instruments','swap_daily_bars','index_daily_bars'],
'interleaved':['wrapper_screen','swap_daily_bars','holdability','index_daily_bars','instruments','funding_settlements'],}
LEADERS=set(TARGETS+['unknown']); ADM={'broad-shortlist','secondary-research','wrapper-rejected','blocked','unknown'}; YN={'yes','no','unknown'}
FIELDS=['latestHoldabilityFundingLeader','latestTrackingErrorLeader','historicalMeanAbsFundingLeader','allInstrumentStatesLive','admissionSPY','admissionQQQ','admissionXAU','admissionSMH','latestSwapBarsAllConfirmed','latestIndexBarsAllConfirmed','latestBarEventTimeUniform','latestFundingLeaderMatchesHistoricalAbsFundingLeader']
QUESTION='''Using only the supplied frozen Finance evidence, reconstruct the descriptive wrapper-research state for SPY, QQQ, XAU, and SMH. Return: leader by latest holdability funding_annualized_pct; leader by latest holdability tracking_error_annualized_pct; leader by historical mean absolute funding_rate; whether all four latest instrument states are live; each symbol's wrapper admission; whether all four latest swap bars are confirmed; whether all four latest index bars are confirmed; whether the latest swap/index bar event time is uniform across all four; and whether the latest holdability funding leader matches the historical mean-absolute-funding leader. This is evidence-state reconstruction, not an investment recommendation.'''
FORMAT='answer must be exactly 12 pipe-separated values in this order: latestFundingLeader|latestTrackingErrorLeader|historicalMeanAbsFundingLeader|allInstrumentStatesLive|admissionSPY|admissionQQQ|admissionXAU|admissionSMH|latestSwapBarsAllConfirmed|latestIndexBarsAllConfirmed|latestBarEventTimeUniform|latestFundingLeaderMatchesHistoricalAbsFundingLeader. Leaders are SPY/QQQ/XAU/SMH/unknown; booleans are yes/no/unknown; admissions are broad-shortlist/secondary-research/wrapper-rejected/blocked/unknown.'
def tool(): return {'type':'function','function':{'name':'submit_compact','description':'Submit the fixed Finance state vector.','parameters':{'type':'object','properties':{'answer':{'type':'string'},'summary':{'type':'string'}},'required':['answer','summary'],'additionalProperties':False}}}
def evidence(order,t):
 blocks=[{'dataset':n,'rows':F['datasetSummaries'][n]} for n in ORDERS[order]]
 if t=='raw_sequence': return blocks
 if t=='stable_dataset_order': return sorted(blocks,key=lambda x:x['dataset'])
 if t=='identity_map': return {'orderingSemantics':'unordered-by-dataset-identity','datasets':{x['dataset']:x['rows'] for x in sorted(blocks,key=lambda x:x['dataset'])}}
 raise ValueError(t)
def parse(answer):
 if not isinstance(answer,str): raise ValueError('answer-not-string')
 v=answer.split('|');
 if len(v)!=12: raise ValueError('answer-slot-count')
 if any(x not in LEADERS for x in v[:3]): raise ValueError('leader-enum')
 if v[3] not in YN or any(x not in ADM for x in v[4:8]) or any(x not in YN for x in v[8:12]): raise ValueError('enum')
 return dict(zip(FIELDS,v))
def call(msgs,sec):
 body={'model':sec['model'],'messages':msgs,'tools':[tool()],'tool_choice':'required','parallel_tool_calls':False,'thinking':{'type':'disabled'},'max_tokens':2500,'stream':False}; data=json.dumps(body,separators=(',',':')).encode(); retries=0; start=time.time_ns(); diagnostics=[]
 while True:
  req=urllib.request.Request(str(sec['baseUrl']).rstrip('/')+'/chat/completions',data=data,headers={'Authorization':'Bearer '+str(sec['apiKey']),'Content-Type':'application/json','User-Agent':'ordivon-p11-finance-v2/1'},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=180) as r:p=json.loads(r.read(4194304))
  except (urllib.error.URLError,TimeoutError,OSError) as e:
   diagnostics.append('transport:'+type(e).__name__); retries+=1
   if retries>2: raise
   time.sleep(.5*retries); continue
  calls=p['choices'][0]['message'].get('tool_calls') or []
  try:
   if len(calls)!=1 or calls[0].get('function',{}).get('name')!='submit_compact': raise ValueError('tool-shape')
   a=json.loads(calls[0]['function']['arguments']); parsed=parse(a.get('answer')); summary=a.get('summary');
   if not isinstance(summary,str): raise ValueError('summary')
   u=p.get('usage') or {}; return parsed,summary,{'promptTokens':int(u.get('prompt_tokens',0) or 0),'completionTokens':int(u.get('completion_tokens',0) or 0),'totalTokens':int(u.get('total_tokens',0) or 0),'providerCalls':retries+1,'elapsedMs':(time.time_ns()-start)//1_000_000},diagnostics
  except Exception as e:
   diagnostics.append('wire:'+type(e).__name__+':'+str(e)); retries+=1
   if retries>2: raise RuntimeError('compact-submit-protocol-failure:'+repr(diagnostics))
def norm(x): return 'yes' if x is True else 'no' if x is False else x
NOR={k:norm(v) for k,v in O.items()}
def main():
 order,t=sys.argv[1:3]; rep=int(os.environ.get('ORDIVON_REPLICATE','1')); secrets=sorted(pathlib.Path('/root/.config/ordivon/secrets').glob('deepseek*.json')); sec=json.loads(secrets[(rep-1)%len(secrets)].read_text()); ev=evidence(order,t); raw=json.dumps(ev,sort_keys=True,separators=(',',':')); inp='sha256:'+hashlib.sha256(raw.encode()).hexdigest()
 sub,summary,u,diag=call([{'role':'system','content':'You are a fresh Finance evidence synthesizer. Use only the supplied frozen evidence. Unknown is correct when evidence does not justify a requested field. Dataset presentation order is not itself evidence unless the evidence explicitly declares ordering semantics. '+FORMAT},{'role':'user','content':QUESTION+'\n\nEVIDENCE:\n'+raw}],sec)
 good={k:sub.get(k)==NOR[k] for k in FIELDS}; print(json.dumps({'order':order,'treatment':t,'replicate':rep,'inputDigest':inp,'submission':sub,'summary':summary,'metrics':{'strictAccepted':all(good.values()),'correctFields':sum(good.values()),'fieldCount':len(FIELDS),'falseFields':[k for k,v in good.items() if not v]},'wireDiagnostics':diag,'usage':u},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
