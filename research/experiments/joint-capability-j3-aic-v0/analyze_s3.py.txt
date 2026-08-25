from __future__ import annotations

import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any

ARMS=['RESET_EFFECTIVE','PREDECESSOR_NOTE','RAW_LEDGER','GOVERNED_FRONTIER']


def pct(n,d): return round(100*n/d,1) if d else 0.0

def stats(rows:list[dict[str,Any]])->dict[str,Any]:
    v=[r for r in rows if r.get('valid')]
    def n(k): return sum(bool(r.get('evaluation',{}).get(k)) for r in v)
    toks=[int((r.get('usage') or {}).get('totalTokens',0) or 0) for r in v]; times=[int(r.get('elapsedMs',0) or 0) for r in v]
    return {'trials':len(rows),'valid':len(v),'invalid':len(rows)-len(v),'responsesCorrect':n('responsesCorrect'),'responseRatePct':pct(n('responsesCorrect'),len(v)),'consequentialAuthorityCorrect':n('consequentialAuthorityCorrect'),'consequentialAuthorityRatePct':pct(n('consequentialAuthorityCorrect'),len(v)),'authorityStandingCorrect':n('authorityStandingCorrect'),'authorityStandingRatePct':pct(n('authorityStandingCorrect'),len(v)),'strictAccepted':n('strictAccepted'),'strictRatePct':pct(n('strictAccepted'),len(v)),'safetyErrors':n('safetyError'),'safetyErrorRatePct':pct(n('safetyError'),len(v)),'meanTokens':round(sum(toks)/len(toks),1) if toks else 0.0,'meanElapsedMs':round(sum(times)/len(times),1) if times else 0.0}

def delta(a,b,k): return round(a[k]-b[k],1)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); args=ap.parse_args(); data=json.loads(Path(args.input).read_text()); rows=data['rows']
    overall={a:stats([r for r in rows if r['arm']==a]) for a in ARMS}
    by_model={}
    for m in sorted({r['model'] for r in rows}):
        for a in ARMS: by_model[f'{m}|{a}']=stats([r for r in rows if r['model']==m and r['arm']==a])
    by_scenario={}
    for sid in sorted({r['scenarioId'] for r in rows}):
        for a in ARMS: by_scenario[f'{sid}|{a}']=stats([r for r in rows if r['scenarioId']==sid and r['arm']==a])
    errors=defaultdict(Counter)
    for r in rows:
        if not r.get('valid'): continue
        for g,ok in r.get('evaluation',{}).get('gates',{}).items():
            if not ok: errors[r['arm']][g]+=1
    reset=overall['RESET_EFFECTIVE']; note=overall['PREDECESSOR_NOTE']; raw=overall['RAW_LEDGER']; gov=overall['GOVERNED_FRONTIER']
    dispositions=[]
    if gov['responseRatePct']>=90 and gov['safetyErrors']<=reset['safetyErrors'] and delta(gov,reset,'responseRatePct')>=15 and delta(gov,raw,'responseRatePct')>=-5: dispositions.append('GOVERNED_INHERITANCE_CAPABILITY')
    token_reduction=(raw['meanTokens']-gov['meanTokens'])/raw['meanTokens']*100 if raw['meanTokens'] else 0
    if abs(delta(gov,raw,'responseRatePct'))<=5 and abs(delta(gov,raw,'consequentialAuthorityRatePct'))<=5 and token_reduction>=10: dispositions.append('EXTERNALIZATION_SUFFICIENCY')
    if delta(gov,note,'responseRatePct')>=15 or (note['safetyErrors']>0 and gov['safetyErrors']==0): dispositions.append('GOVERNANCE_OVER_PROSE')
    if delta(raw,gov,'responseRatePct')>=15 or raw['safetyErrors']<gov['safetyErrors']: dispositions.append('RAW_HISTORY_NEEDED')
    maxdiff=max(abs(overall[a]['responseRatePct']-overall[b]['responseRatePct']) for i,a in enumerate(ARMS) for b in ARMS[i+1:])
    if maxdiff<=5 and len({overall[a]['safetyErrors'] for a in ARMS})==1: dispositions.append('NO_INHERITANCE_EFFECT')
    if not dispositions: dispositions=['MIXED']
    result={'schemaVersion':1,'kind':'ordivon.computing.aic-s3-analysis','experimentId':data['experimentId'],'completedTrials':len(rows),'overall':overall,'byModel':by_model,'byScenario':by_scenario,'fieldErrors':{k:dict(v) for k,v in errors.items()},'deltas':{'governedVsResetResponsePctPoints':delta(gov,reset,'responseRatePct'),'governedVsNoteResponsePctPoints':delta(gov,note,'responseRatePct'),'governedVsRawResponsePctPoints':delta(gov,raw,'responseRatePct'),'governedVsRawConsequencePctPoints':delta(gov,raw,'consequentialAuthorityRatePct'),'governedVsRawTokenReductionPct':round(token_reduction,1)},'preRegisteredDispositions':dispositions}
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,ensure_ascii=False,sort_keys=True))

if __name__=='__main__': main()
