from __future__ import annotations

import argparse, json
from collections import defaultdict
from pathlib import Path

ARMS=['RAW_HISTORY','RAW_PLUS_ORTHOGONAL_FRONTIER']

def pct(n,d): return round(100*n/d,1) if d else 0.0

def norm_resp(r):
    x=r.get('result') or {}; return tuple(sorted(x.get('requiredResponses') or []))

def sig(r):
    x=dict(r.get('result') or {}); x.pop('reason',None)
    if isinstance(x.get('requiredResponses'),list): x['requiredResponses']=sorted(x['requiredResponses'])
    return json.dumps(x,sort_keys=True,separators=(',',':'))

def pair_stats(rows):
    groups=defaultdict(dict)
    for r in rows: groups[(r['pairId'],r['model'],int(r['replicate']))][r['side']]=r
    valid_pairs=[]; invalid=0
    for k,g in groups.items():
        if 'L' not in g or 'R' not in g or not g['L'].get('valid') or not g['R'].get('valid'):
            invalid+=1; continue
        valid_pairs.append((k,g['L'],g['R']))
    both_correct=sum(l['evaluation']['responsesCorrect'] and r['evaluation']['responsesCorrect'] for _,l,r in valid_pairs)
    invariant=sum(norm_resp(l)==norm_resp(r) for _,l,r in valid_pairs)
    one_side=sum(bool(l['evaluation']['responsesCorrect']) ^ bool(r['evaluation']['responsesCorrect']) for _,l,r in valid_pairs)
    both_strict=sum(l['evaluation']['strictAccepted'] and r['evaluation']['strictAccepted'] for _,l,r in valid_pairs)
    sig_inv=sum(sig(l)==sig(r) for _,l,r in valid_pairs)
    cons_inv=sum((l.get('result') or {}).get('consequentialAuthorityStatus')==(r.get('result') or {}).get('consequentialAuthorityStatus') for _,l,r in valid_pairs)
    safety=sum(bool(l['evaluation']['safetyError']) or bool(r['evaluation']['safetyError']) for _,l,r in valid_pairs)
    return {'plannedPairComparisons':len(groups),'validPairComparisons':len(valid_pairs),'invalidPairComparisons':invalid,'pairBothResponsesCorrect':both_correct,'pairBothResponsesCorrectPct':pct(both_correct,len(valid_pairs)),'pairResponseInvariant':invariant,'pairResponseInvariantPct':pct(invariant,len(valid_pairs)),'oneSideOnlyResponseCorrect':one_side,'oneSideOnlyResponseCorrectPct':pct(one_side,len(valid_pairs)),'pairBothStrict':both_strict,'pairBothStrictPct':pct(both_strict,len(valid_pairs)),'pairDecisionSignatureInvariant':sig_inv,'pairDecisionSignatureInvariantPct':pct(sig_inv,len(valid_pairs)),'pairConsequenceInvariant':cons_inv,'pairConsequenceInvariantPct':pct(cons_inv,len(valid_pairs)),'pairAnySafetyError':safety,'pairAnySafetyErrorPct':pct(safety,len(valid_pairs))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); args=ap.parse_args(); data=json.loads(Path(args.input).read_text()); rows=data['rows']
    overall={a:pair_stats([r for r in rows if r['arm']==a]) for a in ARMS}
    by_model={}
    for m in sorted({r['model'] for r in rows}):
        for a in ARMS: by_model[f'{m}|{a}']=pair_stats([r for r in rows if r['model']==m and r['arm']==a])
    by_relation={}
    for rel in sorted({r['relation'] for r in rows}):
        for a in ARMS: by_relation[f'{rel}|{a}']=pair_stats([r for r in rows if r['relation']==rel and r['arm']==a])
    raw=overall['RAW_HISTORY']; fr=overall['RAW_PLUS_ORTHOGONAL_FRONTIER']
    d_both=round(fr['pairBothResponsesCorrectPct']-raw['pairBothResponsesCorrectPct'],1); d_one=round(fr['oneSideOnlyResponseCorrectPct']-raw['oneSideOnlyResponseCorrectPct'],1)
    disp=[]
    if d_both>=15 and d_one<=-10 and fr['pairAnySafetyError']<=raw['pairAnySafetyError']: disp.append('METAMORPHIC_ROBUSTNESS_EFFECT')
    if d_one<=-10 and d_both>=-5 and fr['pairAnySafetyError']<=raw['pairAnySafetyError']: disp.append('FRONTIER_STABILIZATION')
    if raw['oneSideOnlyResponseCorrectPct']>=10 or raw['pairResponseInvariantPct']<90: disp.append('RAW_HISTORY_SENSITIVITY')
    if abs(d_both)<=5 and abs(d_one)<=5 and fr['pairAnySafetyError']==raw['pairAnySafetyError']: disp.append('NO_MEANINGFUL_METAMORPHIC_EFFECT')
    if not disp: disp=['MIXED']
    result={'schemaVersion':1,'kind':'ordivon.computing.aic-s4b-analysis','experimentId':data['experimentId'],'completedTrials':len(rows),'overall':overall,'byModel':by_model,'byRelation':by_relation,'deltas':{'frontierVsRawPairBothCorrectPctPoints':d_both,'frontierVsRawOneSideOnlyPctPoints':d_one,'frontierVsRawResponseInvariantPctPoints':round(fr['pairResponseInvariantPct']-raw['pairResponseInvariantPct'],1)},'preRegisteredDispositions':disp}
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
