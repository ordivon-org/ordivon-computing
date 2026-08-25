#!/usr/bin/env python3
"""Mechanical headline-stat reconstruction for Book Representation Effect v0."""
from __future__ import annotations
import json, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'book-result-value-compression-v0'

def load(p): return json.loads(Path(p).read_text())

def agg(rows, arm):
    rs=[r for r in rows if r.get('arm')==arm and r.get('ok')]
    return {
      'runs':len(rs),
      'exact':sum(r['score']['exactCases'] for r in rs),
      'cases':sum(r['score']['totalCases'] for r in rs),
      'labelErrors':sum(r['score']['labelErrors'] for r in rs),
      'meanTotalTokens':statistics.mean(r['usage']['providerUsage'][0]['total_tokens'] for r in rs),
    }

flash=load(OLD/'followup-raw-runs.json')['rows']
pro=load(ROOT/'A-model-variant/v4-pro-raw-runs.json')['rows']
assert agg(flash,'BASELINE')['exact']==10 and agg(flash,'BASELINE')['labelErrors']==28
assert agg(flash,'TREATMENT_PREBOOK')['exact']==12 and agg(flash,'TREATMENT_PREBOOK')['labelErrors']==14
assert agg(pro,'BASELINE')['exact']==12 and agg(pro,'BASELINE')['labelErrors']==19
assert agg(pro,'TREATMENT_PREBOOK')['exact']==20 and agg(pro,'TREATMENT_PREBOOK')['labelErrors']==4

traces=load(ROOT/'B-persistent-trace/acquisition-traces.json')['rows']
assert len(traces)==6 and all(r['normalizedBytes']==2200 and len(r['note'].encode())==2200 for r in traces)
recovery=load(ROOT/'B-persistent-trace/recovery-raw-runs.json')['rows']
assert agg(recovery,'BOOK_TRACE')['exact']==11 and agg(recovery,'BOOK_TRACE')['labelErrors']==20
assert agg(recovery,'MAP_BOOK_TRACE')['exact']==11 and agg(recovery,'MAP_BOOK_TRACE')['labelErrors']==26

nat=load(ROOT/'C-natural-result-audit/raw-runs.json')['rows']
cards=load(ROOT/'C-natural-result-audit/cards-raw-runs.json')['rows']
mapcards=load(ROOT/'C-natural-result-audit/map-cards-raw-runs.json')['rows']

def natural(rows, arm=None):
    rs=[r for r in rows if r.get('ok') and (arm is None or r.get('arm')==arm)]
    raw=sum(r['score']['correct'] for r in rs); total=sum(r['score']['total'] for r in rs)
    challenged={('CEL','currentConsumption'),('P5','currentConsumption'),('P5','realizedBenefit')}
    robust=0; robust_total=0
    for r in rs:
      wrong={(x['id'],x['field']) for x in r['score']['wrong']}
      for iid in ['RV','OPD','SKILL','CEL','P0','P5']:
       for field in ['objectiveAchievement','boundedImprovement','currentConsumption','realizedBenefit','broaderPromotion']:
        if (iid,field) in challenged: continue
        robust_total+=1; robust += ((iid,field) not in wrong)
    prompt=statistics.mean(r['usage']['providerUsage'][0]['prompt_tokens'] for r in rs)
    return raw,total,robust,robust_total,prompt

b=natural(nat,'BOOK_PACKET'); m=natural(nat,'MAP_BOOK_PACKET'); c=natural(cards); mc=natural(mapcards)
assert b[:4]==(73,90,73,81)
assert m[:4]==(72,90,72,81)
assert c[:4]==(77,90,76,81)
assert mc[:4]==(67,90,67,81)
assert round(b[4])==27869 and round(m[4])==28645 and round(c[4])==23218 and round(mc[4])==23993

print(json.dumps({
 'status':'ok',
 'A_modelVariant':{
   'flashBook':agg(flash,'BASELINE'),'flashMapBook':agg(flash,'TREATMENT_PREBOOK'),
   'proBook':agg(pro,'BASELINE'),'proMapBook':agg(pro,'TREATMENT_PREBOOK')},
 'B_persistentTrace':{'bookTrace':agg(recovery,'BOOK_TRACE'),'mapBookTrace':agg(recovery,'MAP_BOOK_TRACE')},
 'C_naturalAudit':{
   'bookFull':{'raw':list(b[:2]),'robust':list(b[2:4]),'promptTokens':b[4]},
   'mapBookFull':{'raw':list(m[:2]),'robust':list(m[2:4]),'promptTokens':m[4]},
   'bookCards':{'raw':list(c[:2]),'robust':list(c[2:4]),'promptTokens':c[4]},
   'mapBookCards':{'raw':list(mc[:2]),'robust':list(mc[2:4]),'promptTokens':mc[4]}},
 'mediaBookMutationAdmitted':False,
 'humanOutcomeClaimEstablished':False
},indent=2))
