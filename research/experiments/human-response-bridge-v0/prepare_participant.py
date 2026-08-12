#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text())
def h(s): return hashlib.sha256(s.encode()).digest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--source',default='/root/.config/ordivon/hr0/participant-source-v1.json'); ap.add_argument('--private-oracle',default='/root/.config/ordivon/hr0/private-oracle-v1.json'); ap.add_argument('--participant-id',required=True); ap.add_argument('--naivety-class',choices=['naive','non-naive'],required=True); ap.add_argument('--evaluator-class',default='lay'); ap.add_argument('--output',required=True); args=ap.parse_args()
 src=load(args.source); priv=load(args.private_oracle)
 idx=int.from_bytes(h(priv['assignmentSalt']+'\\0'+args.participant_id)[:8],'big')%len(src['schedules']); schedule=src['schedules'][idx]
 ms={m['mechanismId']:m for m in src['mechanisms']}; encounters=[]
 for mid in ('H1','H2','H3'):
  m=ms[mid]; variant=schedule['variantByMechanism'][mid]; visible=m['orders'][variant][:4]
  facts=[{"evidenceId":i,**m['facts'][i]} for i in visible]
  encounters.append({"mechanismId":mid,"encounterIndex":len(encounters)+1,"evidence":facts,"questions":m['questions']})
 packet={"schemaVersion":1,"kind":"ordivon.hr0-human-pilot-packet","participantId":args.participant_id,"naivetyClass":args.naivety_class,"evaluatorClass":args.evaluator_class,"scheduleId":schedule['scheduleId'],"instructions":"For each mechanism, use only the evidence shown for that encounter. Answer every question with one option ID O1-O4 and then give confidence from 0 to 100. Do not use prior mechanism knowledge. O4 means the shown evidence does not establish the answer.","encounters":encounters,"responseShape":{"answersPerEncounter":6,"fields":["questionId","optionId","confidence0to100"]},"interpretationBoundary":"A non-naive participant can validate apparatus usability but not blinded observer-class effect evidence. One participant is one evaluator cluster, not a population sample."}
 Path(args.output).write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({"ok":True,"participantId":args.participant_id,"naivetyClass":args.naivety_class,"scheduleId":schedule['scheduleId'],"encounters":3,"questions":18,"output":args.output}))
if __name__=='__main__': main()
