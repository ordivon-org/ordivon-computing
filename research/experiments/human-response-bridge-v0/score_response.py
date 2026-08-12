#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text())
def mean(xs): return sum(xs)/len(xs) if xs else 0.0
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--private-oracle',default='/root/.config/ordivon/hr0/private-oracle-v1.json'); ap.add_argument('--packet',required=True); ap.add_argument('--response',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
 priv=load(args.private_oracle); packet=load(args.packet); response=load(args.response); ms={m['mechanismId']:m for m in priv['mechanisms']}; sched=next(s for s in priv['schedules'] if s['scheduleId']==packet['scheduleId'])
 by={(x['mechanismId'],x['questionId']):x for x in response['answers']}; rows=[]
 for enc in packet['encounters']:
  mid=enc['mechanismId']; variant=sched['variantByMechanism'][mid]; visible=set(ms[mid]['orders'][variant][:4]); qmap={q['questionId']:q for q in ms[mid]['questions']}
  for qid,q in qmap.items():
   ans=by[(mid,qid)]; established=set(q['requiredEvidenceAll']).issubset(visible); factual_correct=ans['optionId']==q['answer']; substantive=ans['optionId']!='O4'; unsupported=substantive and not established; epistemic_correct=(factual_correct if established else ans['optionId']=='O4')
   rows.append({"mechanismId":mid,"variant":variant,"questionId":qid,"stage":q['stage'],"factualCorrect":factual_correct,"evidenceEstablished":established,"unsupportedInference":unsupported,"epistemicDecisionCorrect":epistemic_correct,"confidence0to100":ans['confidence0to100']})
 stages={s:mean([float(r['factualCorrect']) for r in rows if r['stage']==s]) for s in ('perception','comprehension','adaptation')}
 result={"schemaVersion":2,"kind":"ordivon.hr0-human-pilot-score","participantId":packet['participantId'],"naivetyClass":packet['naivetyClass'],"evaluatorClass":packet['evaluatorClass'],"scheduleId":packet['scheduleId'],"oneEvaluatorCluster":True,"factualStageAccuracy":stages,"factualAdaptationAccuracyByVariant":{v:mean([float(r['factualCorrect']) for r in rows if r['stage']=='adaptation' and r['variant']==v]) for v in ('explicit-chain','fragmented','evidence-delayed')},"epistemicDecisionAccuracy":mean([float(r['epistemicDecisionCorrect']) for r in rows]),"epistemicDecisionAccuracyByVariant":{v:mean([float(r['epistemicDecisionCorrect']) for r in rows if r['variant']==v]) for v in ('explicit-chain','fragmented','evidence-delayed')},"unsupportedInferenceCount":sum(int(r['unsupportedInference']) for r in rows),"meanConfidence":mean([r['confidence0to100']/100 for r in rows]),"meanAbsoluteConfidenceErrorAgainstEpistemicDecision":mean([abs(r['confidence0to100']/100-float(r['epistemicDecisionCorrect'])) for r in rows]),"populationInferenceAllowed":False,"interpretationBoundary":"Factual answer accuracy is R6-comparable and remains separate from unsupported inference. Confidence is calibrated to whether the selected response is justified by shown evidence. One participant is one evaluator cluster; non-naive pilots support apparatus/local calibration only."}
 Path(args.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
