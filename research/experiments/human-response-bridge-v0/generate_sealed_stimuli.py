#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, random, secrets
from pathlib import Path

VARIANTS=("explicit-chain","fragmented","evidence-delayed")
ORDERS={
 "explicit-chain":["F1","F2","F3","F4","F5","D1","D2"],
 "fragmented":["D1","F5","D2","F3","F4","F2","F1"],
 "evidence-delayed":["F2","F3","F4","D1","D2","F5","F1"],
}
EXPECTED_VIEWPORT={
 "explicit-chain":["F1","F2","F3","F4"],
 "fragmented":["D1","F5","D2","F3"],
 "evidence-delayed":["F2","F3","F4","D1"],
}

def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest_bytes(data): return "sha256:"+hashlib.sha256(data).hexdigest()
def digest(obj): return digest_bytes(canonical(obj))
def rng_for(seed): return random.Random(int.from_bytes(hashlib.sha256(seed.encode()).digest()[:16],"big"))

def mechanism(seed, mid):
 r=rng_for(seed)
 gauges=["Neral","Tovin","Keral","Miran","Sovel","Lethin","Rovan","Pelin","Dovin","Aster"]
 colors=["amber","violet","copper","silver","indigo","crimson","teal","ochre"]
 chambers=["blue chamber","ceramic chamber","north chamber","glass chamber","inner chamber","cooling chamber","sealed chamber","lower chamber"]
 spindles=["Varo spindle","Kelm rotor","Sorin wheel","Daro shaft","Mek spindle","Teral rotor","Orin wheel","Vesk shaft"]
 trigger=r.choice([5,6,7,8,9]); safe=r.choice([36,38,40,42,44]); gauge=r.choice(gauges); latch=f"{r.choice(colors)} latch"; chamber=r.choice(chambers); spindle=r.choice(spindles)
 facts={
  "F1":{"heading":"Trigger","text":f"When the fictitious {gauge} gauge reaches {trigger}, the {latch} opens; below {trigger}, it remains closed. The gauge is only the upstream trigger and does not directly move the final actuator."},
  "F2":{"heading":"Transfer","text":f"The {latch} controls coolant access to the {chamber}. An open latch permits coolant entry; a closed or mechanically jammed latch blocks coolant even when the {gauge} gauge has reached its trigger."},
  "F3":{"heading":"Cooling","text":f"Coolant entering the {chamber} lowers it below {safe} degrees. If coolant does not enter, the chamber remains above that threshold in the situations described here. No second cooling path is defined."},
  "F4":{"heading":"Permission boundary","text":f"The {spindle} may rotate safely only when the {chamber} is below {safe} degrees. At or above {safe} degrees it must remain stopped, regardless of the upstream gauge or latch state."},
  "F5":{"heading":"Causal boundary","text":f"A {gauge} reading of {trigger} is not by itself permission for the {spindle} to rotate. Latch opening, coolant entry, and chamber cooling must still succeed; an intermediate failure can leave the actuator unsafe."},
  "D1":{"heading":"Non-causal identifier","text":f"A maintenance plate beside the {chamber} carries the code {r.choice(['PX-14','QR-22','LM-31','VK-08','TN-17','CS-24'])}. It identifies the assembly but has no causal role in the gauge, latch, coolant, temperature, or spindle sequence."},
  "D2":{"heading":"Non-causal service signal","text":f"A service lamp near the {spindle} records inspection hours. Its color may change during maintenance, but it neither opens the {latch} nor changes coolant flow or the {safe}-degree safety boundary."},
 }
 questions=[
  {"questionId":"Q1","stage":"perception","question":f"What {gauge} gauge reading opens the {latch}?","options":{"O1":str(trigger),"O2":str(safe),"O3":str(trigger+3),"O4":"The visible evidence does not establish this"},"answer":"O1","requiredEvidenceAll":["F1"]},
  {"questionId":"Q2","stage":"comprehension","question":f"What does a mechanically jammed closed {latch} do to coolant flow?","options":{"O1":"It blocks coolant entry","O2":"It forces coolant entry","O3":"It directly cools the chamber","O4":"The visible evidence does not establish this"},"answer":"O1","requiredEvidenceAll":["F2"]},
  {"questionId":"Q3","stage":"comprehension","question":f"Why does coolant matter to the {safe}-degree boundary?","options":{"O1":"It lowers the chamber below the boundary","O2":"It raises the gauge reading","O3":"It changes the service-lamp color","O4":"The visible evidence does not establish this"},"answer":"O1","requiredEvidenceAll":["F3"]},
  {"questionId":"Q4","stage":"adaptation","question":f"The {gauge} gauge reaches {trigger}, but the {latch} is mechanically jammed closed and the chamber remains warm. May the {spindle} rotate safely?","options":{"O1":"Yes","O2":"No","O3":"Only because the service lamp can override it","O4":"The visible evidence does not establish this"},"answer":"O2","requiredEvidenceAll":["F2","F4"]},
  {"questionId":"Q5","stage":"adaptation","question":f"The gauge reaches {trigger}, the latch opens, coolant enters, and the {chamber} is measured below {safe} degrees. May the {spindle} rotate safely under the stated mechanism?","options":{"O1":"Yes","O2":"No","O3":"Only if the maintenance code changes","O4":"The visible evidence does not establish this"},"answer":"O1","requiredEvidenceAll":["F4"]},
  {"questionId":"Q6","stage":"adaptation","question":f"The gauge reaches {trigger} and the latch opens, but coolant fails to enter and the {chamber} stays above {safe} degrees. May the {spindle} rotate safely?","options":{"O1":"Yes","O2":"No","O3":"The gauge alone makes it safe","O4":"The visible evidence does not establish this"},"answer":"O2","requiredEvidenceAll":["F3","F4"]},
 ]
 return {"mechanismId":mid,"seedCommitment":digest_bytes(seed.encode()),"facts":facts,"orders":ORDERS,"questions":questions}

def manifest(mech,eid,salt):
 return {"schemaVersion":1,"kind":"ordivon.web.r6-encounter-manifest","experimentId":eid,"assignmentSalt":salt,"encounter":{"mode":"initial-viewport-no-scroll","viewport":{"width":1080,"height":1050}},"variants":[{"variantId":v,"probability":1/3,"title":f"Mechanism {mech['mechanismId']}","sections":[{"evidenceId":i,**mech['facts'][i]} for i in ORDERS[v]]} for v in VARIANTS]}

def public_mech(mech):
 return {"mechanismId":mech["mechanismId"],"facts":mech["facts"],"orders":mech["orders"],"questions":[{k:q[k] for k in ("questionId","stage","question","options")} for q in mech["questions"]]}

def schedules():
 perms=[
  ("explicit-chain","fragmented","evidence-delayed"),("explicit-chain","evidence-delayed","fragmented"),
  ("fragmented","explicit-chain","evidence-delayed"),("fragmented","evidence-delayed","explicit-chain"),
  ("evidence-delayed","explicit-chain","fragmented"),("evidence-delayed","fragmented","explicit-chain")]
 return [{"scheduleId":f"S{i+1}","variantByMechanism":dict(zip(("H1","H2","H3"),p))} for i,p in enumerate(perms)]

def write_private(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True).encode()+b"\n"); os.chmod(path,0o600)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['smoke','seal'],required=True); ap.add_argument('--private-root',default='/root/.config/ordivon/hr0'); ap.add_argument('--seal-receipt'); ap.add_argument('--output-dir'); args=ap.parse_args()
 if args.mode=='smoke':
  ms=[mechanism(f'hr0-smoke-{i}','T'+str(i)) for i in range(1,4)]
  out={"mechanisms":ms,"manifests":[manifest(m,f'experiment:web:hr0-smoke:{m["mechanismId"].lower()}',f'hr0-smoke-{m["mechanismId"]}') for m in ms]}
  if args.output_dir:
   od=Path(args.output_dir); od.mkdir(parents=True,exist_ok=True)
   for m,man in zip(ms,out["manifests"]):
    (od/f"{m['mechanismId'].lower()}.manifest.json").write_text(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
  print(json.dumps({"ok":True,"digest":digest(out),"mechanisms":len(ms),"variants":len(ms)*3,"outputDir":args.output_dir}))
  return
 private=Path(args.private_root)
 master=secrets.token_hex(32); assignment_salt=secrets.token_hex(32)
 human=[mechanism(f'{master}:human:{i}',f'H{i}') for i in range(1,4)]
 preflight=[mechanism(f'hr0-preflight-fixed-v1:{i}',f'P{i}') for i in range(1,3)]
 human_private={"schemaVersion":1,"kind":"ordivon.hr0-private-oracle","masterSeed":master,"assignmentSalt":assignment_salt,"mechanisms":human,"schedules":schedules()}
 participant={"schemaVersion":1,"kind":"ordivon.hr0-participant-source","mechanisms":[public_mech(m) for m in human],"schedules":schedules(),"assignmentSaltCommitment":digest_bytes(assignment_salt.encode())}
 pre={"schemaVersion":1,"kind":"ordivon.hr0-preflight-source","mechanisms":preflight,"manifests":[manifest(m,f'experiment:web:hr0-preflight:{m["mechanismId"].lower()}',f'hr0-preflight-{m["mechanismId"]}-v1') for m in preflight]}
 oracle=private/'private-oracle-v1.json'; packet=private/'participant-source-v1.json'; prepath=private/'preflight-source-v1.json'
 write_private(oracle,human_private); write_private(packet,participant); write_private(prepath,pre)
 receipt={"schemaVersion":1,"kind":"ordivon.hr0-seal-receipt","humanMechanisms":3,"preflightMechanisms":2,"scheduleCount":6,"masterSeedCommitment":digest_bytes(master.encode()),"assignmentSaltCommitment":digest_bytes(assignment_salt.encode()),"privateOracleDigest":digest_bytes(oracle.read_bytes()),"participantSourceDigest":digest_bytes(packet.read_bytes()),"preflightSourceDigest":digest_bytes(prepath.read_bytes()),"privateRoot":str(private),"privateFilesMode":"0600","humanStimulusMutableAfterSeal":False}
 if not args.seal_receipt: raise SystemExit('--seal-receipt required in seal mode')
 Path(args.seal_receipt).write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:v for k,v in receipt.items() if k!='privateRoot'},indent=2))
if __name__=='__main__': main()
