from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'f2-cases-v0.json').read_text())
cases=d['cases']; depth=d['depthScale']

def depth_pred(c):
    r=depth[c['changeClass']]
    return 2 if r>=5 else (1 if r>=3 else 0)

def fit_score(c): return sum(c['fit'].values())
def fit_pred(c):
    s=fit_score(c)
    return 2 if s>=5 else (1 if s>=3 else 0)

def persist_pred(c): return 1  # every frozen case is a retained/persistent change or candidate artifact

def pearson(xs,ys):
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    a=sum((x-mx)*(y-my) for x,y in zip(xs,ys)); b=sum((x-mx)**2 for x in xs); c=sum((y-my)**2 for y in ys)
    return a/math.sqrt(b*c) if b and c else 0.0

def ranks(xs):
    vals=sorted(set(xs)); return [1+sum(1 for v in vals if v<x)+(sum(1 for y in xs if y==x)-1)/2 for x in xs]
def spearman(xs,ys): return pearson(ranks(xs),ranks(ys))
rows=[]
for c in cases:
    preds={'B0_PERSISTENCE':persist_pred(c),'B1_DEPTH':depth_pred(c),'M_FIT':fit_pred(c)}
    rows.append({'id':c['id'],'split':c['split'],'changeClass':c['changeClass'],'depthRank':depth[c['changeClass']],'fitScore':fit_score(c),'oracleValue':c['oracleValue'],'predictions':preds,'absoluteError':{k:abs(v-c['oracleValue']) for k,v in preds.items()}})

def summarize(split=None):
    rs=[r for r in rows if split is None or r['split']==split]
    return {k:{'exact':sum(r['predictions'][k]==r['oracleValue'] for r in rs),'total':len(rs),'mae':sum(r['absoluteError'][k] for r in rs)/len(rs)} for k in ['B0_PERSISTENCE','B1_DEPTH','M_FIT']}
out={'schemaVersion':1,'kind':'ordivon.computing.pal-f2-change-depth-result','status':'completed','development':summarize('development'),'holdout':summarize('holdout'),'all':summarize(),'correlations':{'depthSpearmanVsOracle':spearman([r['depthRank'] for r in rows],[r['oracleValue'] for r in rows]),'fitScoreSpearmanVsOracle':spearman([r['fitScore'] for r in rows],[r['oracleValue'] for r in rows])},'rows':rows,'residuals':{'depth':[r['id'] for r in rows if r['predictions']['B1_DEPTH']!=r['oracleValue']],'fit':[r['id'] for r in rows if r['predictions']['M_FIT']!=r['oracleValue']]},'claimBoundary':'Small hand-coded historical/held-out court. Change depth and fit features are frozen descriptive codings, not natural constants. Use residuals to design prospective experiments rather than promote the score.'}
(ROOT/'f2-results-v0.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print(json.dumps({'development':out['development'],'holdout':out['holdout'],'all':out['all'],'correlations':out['correlations'],'residuals':out['residuals']},ensure_ascii=False,indent=2))
