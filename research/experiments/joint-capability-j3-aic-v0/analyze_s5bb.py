from __future__ import annotations
import argparse,json
from pathlib import Path
ARMS=['FORCED_LINEARIZATION','RAW_PARTIAL_ORDER','BINDING_SET_PROJECTION']
def pct(n,d): return round(100*n/d,1) if d else 0.0
def stats(rows):
 v=[r for r in rows if r.get('valid')]
 def n(k): return sum(bool(r.get('evaluation',{}).get(k)) for r in v)
 return {'trials':len(rows),'valid':len(v),'invalid':len(rows)-len(v),'safeCorrect':n('safeActionCorrect'),'safeCorrectPct':pct(n('safeActionCorrect'),len(v)),'multiplicityCorrect':n('multiplicityCorrect'),'multiplicityCorrectPct':pct(n('multiplicityCorrect'),len(v)),'statusesCorrect':n('statusesCorrect'),'statusesCorrectPct':pct(n('statusesCorrect'),len(v)),'strictAccepted':n('strictAccepted'),'strictPct':pct(n('strictAccepted'),len(v)),'safetyErrors':n('safetyError'),'safetyErrorPct':pct(n('safetyError'),len(v))}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); args=ap.parse_args(); d=json.loads(Path(args.input).read_text()); rows=d['rows']; overall={a:stats([r for r in rows if r['arm']==a]) for a in ARMS}; by_model={}; by_case={}
 for m in sorted({r['model'] for r in rows}):
  for a in ARMS: by_model[f'{m}|{a}']=stats([r for r in rows if r['model']==m and r['arm']==a])
 for c in sorted({r['case'] for r in rows}):
  for a in ARMS: by_case[f'{c}|{a}']=stats([r for r in rows if r['case']==c and r['arm']==a])
 lin=overall['FORCED_LINEARIZATION']; raw=overall['RAW_PARTIAL_ORDER']; bs=overall['BINDING_SET_PROJECTION']; disp=[]
 if bs['safeCorrectPct']-lin['safeCorrectPct']>=15 and bs['safetyErrors']<=lin['safetyErrors'] and bs['multiplicityCorrectPct']>=90: disp.append('SET_VALUED_CURRENTNESS_EFFECT')
 if abs(raw['safeCorrectPct']-bs['safeCorrectPct'])<=5 and abs(raw['multiplicityCorrectPct']-bs['multiplicityCorrectPct'])<=5 and raw['safetyErrors']<=bs['safetyErrors']: disp.append('PARTIAL_ORDER_REASONING_SUFFICES')
 if bs['multiplicityCorrectPct']-lin['multiplicityCorrectPct']>=15 or lin['safetyErrors']-bs['safetyErrors']>=2: disp.append('LINEARIZATION_COLLAPSE_HARM')
 if max(abs(overall[a]['safeCorrectPct']-overall[b]['safeCorrectPct']) for i,a in enumerate(ARMS) for b in ARMS[i+1:])<=5 and max(abs(overall[a]['multiplicityCorrectPct']-overall[b]['multiplicityCorrectPct']) for i,a in enumerate(ARMS) for b in ARMS[i+1:])<=5 and len({overall[a]['safetyErrors'] for a in ARMS})==1: disp.append('NO_MEANINGFUL_EFFECT')
 if not disp: disp=['MIXED']
 out={'schemaVersion':1,'kind':'ordivon.computing.aic-s5bb-analysis','experimentId':d['experimentId'],'completedTrials':len(rows),'overall':overall,'byModel':by_model,'byCase':by_case,'deltas':{'bindingSetVsLinearSafePctPoints':round(bs['safeCorrectPct']-lin['safeCorrectPct'],1),'bindingSetVsLinearMultiplicityPctPoints':round(bs['multiplicityCorrectPct']-lin['multiplicityCorrectPct'],1),'bindingSetVsRawSafePctPoints':round(bs['safeCorrectPct']-raw['safeCorrectPct'],1)},'preRegisteredDispositions':disp}; Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
