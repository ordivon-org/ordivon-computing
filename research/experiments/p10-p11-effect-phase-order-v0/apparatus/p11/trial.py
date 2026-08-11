from __future__ import annotations
import json,os,pathlib,sys,time,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parent; F=json.loads((ROOT/'finance-evidence.json').read_text()); O=F['oracle']
TARGETS=['SPY','QQQ','XAU','SMH']; DATASETS=list(F['datasetSummaries'])
ORDERS={
'canonical':['holdability','wrapper_screen','instruments','funding_settlements','swap_daily_bars','index_daily_bars'],
'reverse':['index_daily_bars','swap_daily_bars','funding_settlements','instruments','wrapper_screen','holdability'],
'bars_first':['swap_daily_bars','index_daily_bars','funding_settlements','holdability','instruments','wrapper_screen'],
'identity_first':['instruments','wrapper_screen','holdability','funding_settlements','index_daily_bars','swap_daily_bars'],
'funding_first':['funding_settlements','holdability','wrapper_screen','instruments','swap_daily_bars','index_daily_bars'],
'interleaved':['wrapper_screen','swap_daily_bars','holdability','index_daily_bars','instruments','funding_settlements'],}
LEADERS=TARGETS+['unknown']; ADM=['broad-shortlist','secondary-research','wrapper-rejected','blocked','unknown']; YN=['yes','no','unknown']
QUESTION='''Using only the supplied frozen Finance evidence, reconstruct the descriptive wrapper-research state for SPY, QQQ, XAU, and SMH. Return: leader by latest holdability funding_annualized_pct; leader by latest holdability tracking_error_annualized_pct; leader by historical mean absolute funding_rate; whether all four latest instrument states are live; each symbol's wrapper admission; whether all four latest swap bars are confirmed; whether all four latest index bars are confirmed; whether the latest swap/index bar event time is uniform across all four; and whether the latest holdability funding leader matches the historical mean-absolute-funding leader. This is evidence-state reconstruction, not an investment recommendation.'''
def tool():
 props={'latestHoldabilityFundingLeader':{'type':'string','enum':LEADERS},'latestTrackingErrorLeader':{'type':'string','enum':LEADERS},'historicalMeanAbsFundingLeader':{'type':'string','enum':LEADERS},'allInstrumentStatesLive':{'type':'string','enum':YN},'admissionSPY':{'type':'string','enum':ADM},'admissionQQQ':{'type':'string','enum':ADM},'admissionXAU':{'type':'string','enum':ADM},'admissionSMH':{'type':'string','enum':ADM},'latestSwapBarsAllConfirmed':{'type':'string','enum':YN},'latestIndexBarsAllConfirmed':{'type':'string','enum':YN},'latestBarEventTimeUniform':{'type':'string','enum':YN},'latestFundingLeaderMatchesHistoricalAbsFundingLeader':{'type':'string','enum':YN},'summary':{'type':'string'}}
 return {'type':'function','function':{'name':'submit','description':'Submit the Finance evidence-state model.','parameters':{'type':'object','properties':props,'required':list(props),'additionalProperties':False}}}
def evidence(order,t):
 blocks=[{'dataset':n,'rows':F['datasetSummaries'][n]} for n in ORDERS[order]]
 if t=='raw_sequence': return blocks
 if t=='stable_dataset_order': return sorted(blocks,key=lambda x:x['dataset'])
 if t=='identity_map': return {'orderingSemantics':'unordered-by-dataset-identity','datasets':{x['dataset']:x['rows'] for x in sorted(blocks,key=lambda x:x['dataset'])}}
 raise ValueError(t)
def call(msgs,sec):
 body={'model':sec['model'],'messages':msgs,'tools':[tool()],'tool_choice':'required','parallel_tool_calls':False,'thinking':{'type':'disabled'},'max_tokens':5500,'stream':False}; data=json.dumps(body,separators=(',',':')).encode(); retries=0; start=time.time_ns()
 while True:
  req=urllib.request.Request(str(sec['baseUrl']).rstrip('/')+'/chat/completions',data=data,headers={'Authorization':'Bearer '+str(sec['apiKey']),'Content-Type':'application/json','User-Agent':'ordivon-p11-finance/1'},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=180) as r: p=json.loads(r.read(4194304))
  except (urllib.error.URLError,TimeoutError,OSError):
   retries+=1
   if retries>2: raise
   time.sleep(.5*retries); continue
  calls=p['choices'][0]['message'].get('tool_calls') or []
  if len(calls)==1 and calls[0].get('function',{}).get('name')=='submit':
   try:a=json.loads(calls[0]['function']['arguments'])
   except:a={}
   if isinstance(a,dict) and all(k in a for k in ['latestHoldabilityFundingLeader','latestTrackingErrorLeader','historicalMeanAbsFundingLeader','allInstrumentStatesLive','admissionSPY','admissionQQQ','admissionXAU','admissionSMH','latestSwapBarsAllConfirmed','latestIndexBarsAllConfirmed','latestBarEventTimeUniform','latestFundingLeaderMatchesHistoricalAbsFundingLeader','summary']):
    u=p.get('usage') or {}; return a,{'promptTokens':int(u.get('prompt_tokens',0) or 0),'completionTokens':int(u.get('completion_tokens',0) or 0),'totalTokens':int(u.get('total_tokens',0) or 0),'providerCalls':retries+1,'elapsedMs':(time.time_ns()-start)//1_000_000}
  retries+=1
  if retries>2: raise RuntimeError('submit protocol failure')
def norm(x): return 'yes' if x is True else 'no' if x is False else x
NOR={k:norm(v) for k,v in O.items()}
def main():
 order,t=sys.argv[1:3]; rep=int(os.environ.get('ORDIVON_REPLICATE','1')); sec=json.loads(sorted(pathlib.Path('/root/.config/ordivon/secrets').glob('deepseek*.json'))[(rep-1)%len(list(pathlib.Path('/root/.config/ordivon/secrets').glob('deepseek*.json')))].read_text()); ev=evidence(order,t); raw=json.dumps(ev,sort_keys=True,separators=(',',':')); import hashlib; inp='sha256:'+hashlib.sha256(raw.encode()).hexdigest()
 sub,u=call([{'role':'system','content':'You are a fresh Finance evidence synthesizer. Use only the supplied frozen evidence. Unknown is correct when evidence does not justify a requested field. Dataset presentation order is not itself evidence unless the evidence explicitly declares ordering semantics.'},{'role':'user','content':QUESTION+'\n\nEVIDENCE:\n'+raw}],sec)
 fields=list(NOR); good={k:sub.get(k)==NOR[k] for k in fields}; print(json.dumps({'order':order,'treatment':t,'replicate':rep,'inputDigest':inp,'submission':sub,'metrics':{'strictAccepted':all(good.values()),'correctFields':sum(good.values()),'fieldCount':len(fields),'falseFields':[k for k,v in good.items() if not v]},'usage':u},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
