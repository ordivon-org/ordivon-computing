from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import time
import urllib.error
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "stress-corpus-v1.json").read_text(encoding="utf-8"))
STATIC = ["CLASSICAL_SUBSTRATE", "CALLER_OR_DOMAIN", "NO_SHARED_MECHANISM"]


def canonical(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(v: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(v)).hexdigest()


def secrets() -> list[pathlib.Path]:
    out = []
    for path in sorted(pathlib.Path("/root/.config/ordivon/secrets").glob("deepseek*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if all(isinstance(value.get(k), str) and value[k] for k in ("apiKey", "baseUrl", "model")):
            out.append(path)
    if not out:
        raise RuntimeError("no usable DeepSeek secret")
    return out


def mapping(rep: int) -> dict[str, str]:
    labels = list(CORPUS["opaqueLabels"])
    random.Random(f"ex1b-labels:{rep}").shuffle(labels)
    return {"{{HOST}}": labels[0], "{{HARNESS}}": labels[1], "{{RUNTIME}}": labels[2]}


def render(text: str, m: dict[str, str]) -> str:
    for old, new in m.items():
        text = text.replace(old, new)
    return text


def call(secret: dict[str, Any], treatment: str, rep: int, cases: list[dict[str, Any]], m: dict[str, str]) -> tuple[dict[str, Any], dict[str, Any]]:
    labels = list(CORPUS["opaqueLabels"]) + STATIC
    ids = [c["id"] for c in cases]
    explanation = render(CORPUS["treatments"][treatment], m)
    visible = [{"caseId": c["id"], "scenario": render(c["scenario"], m)} for c in cases]
    tool = {"type":"function","function":{"name":"submit_existence","description":"Choose the smallest justified owner for every scenario. The opaque labels name the three Ordivon responsibilities defined in the explanation. CLASSICAL_SUBSTRATE means mature existing computing already owns the complete requirement. CALLER_OR_DOMAIN means the unresolved truth/effect contract is domain-local. NO_SHARED_MECHANISM means the proposed shared abstraction has not earned existence.","parameters":{"type":"object","additionalProperties":False,"properties":{"answers":{"type":"array","minItems":len(ids),"maxItems":len(ids),"items":{"type":"object","additionalProperties":False,"properties":{"caseId":{"type":"string","enum":ids},"owner":{"type":"string","enum":labels},"reason":{"type":"string","minLength":1,"maxLength":700}},"required":["caseId","owner","reason"]}}},"required":["answers"]}}}
    system = "You are a fresh evaluator. Learn only from the supplied explanation. Apply deletion/minimality reasoning: choose the smallest owner that must exist for the exact stated requirement, and do not award architecture merely because an Ordivon component is nearby. Return only the required tool call.\n\nEXPLANATION:\n" + explanation
    body = {"model":secret["model"],"messages":[{"role":"system","content":system},{"role":"user","content":json.dumps(visible,ensure_ascii=False,separators=(",", ":"))}],"tools":[tool],"tool_choice":{"type":"function","function":{"name":"submit_existence"}},"parallel_tool_calls":False,"thinking":{"type":"disabled"},"max_tokens":10000,"stream":False}
    data = canonical(body); corrections=[]; started=time.time_ns()
    for attempt in range(1,4):
        req=urllib.request.Request(str(secret["baseUrl"]).rstrip("/")+"/chat/completions",data=data,headers={"Authorization":"Bearer "+secret["apiKey"],"Content-Type":"application/json","User-Agent":"ordivon-ex1b-existence/1"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=180) as response: payload=json.loads(response.read(8_388_608))
        except (urllib.error.URLError,TimeoutError,OSError) as exc:
            corrections.append({"attempt":attempt,"kind":"transport","error":type(exc).__name__})
            if attempt==3: raise
            time.sleep(.5*attempt); continue
        try:
            calls=payload["choices"][0]["message"].get("tool_calls") or []
            if len(calls)!=1 or calls[0].get("function",{}).get("name")!="submit_existence": raise ValueError("tool call differs")
            args=json.loads(calls[0]["function"]["arguments"]); answers=args.get("answers")
            if not isinstance(answers,list) or len(answers)!=len(ids): raise ValueError("cardinality differs")
            by={}
            for a in answers:
                if not isinstance(a,dict) or set(a)!={"caseId","owner","reason"}: raise ValueError("fields differ")
                if a["caseId"] not in ids or a["caseId"] in by or a["owner"] not in labels or not isinstance(a["reason"],str) or not a["reason"]: raise ValueError("value invalid")
                by[a["caseId"]]=a
            if set(by)!=set(ids): raise ValueError("coverage differs")
            u=payload.get("usage") or {}
            return {"answers":[by[x] for x in ids],"providerModel":payload.get("model",secret["model"])},{"promptTokens":int(u.get("prompt_tokens",0) or 0),"completionTokens":int(u.get("completion_tokens",0) or 0),"totalTokens":int(u.get("total_tokens",0) or 0),"providerCalls":attempt,"wireCorrections":corrections,"elapsedMs":(time.time_ns()-started)//1_000_000,"requestDigest":digest(body)}
        except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:
            corrections.append({"attempt":attempt,"kind":"schema","error":str(exc)[:300]})
            if attempt==3: raise RuntimeError(str(corrections)) from exc
    raise AssertionError


def analyze(trials: list[dict[str, Any]]) -> dict[str, Any]:
    out={}
    opaque=set(CORPUS["opaqueLabels"])
    for treatment in CORPUS["treatments"]:
        selected=[t for t in trials if t["treatment"]==treatment]; rows=[r for t in selected for r in t["result"]]
        anti=[r for r in rows if r["subset"]=="anti-overbuild"]
        strict=sum(r["correct"] for r in rows); total=len(rows)
        out[treatment]={"strictCorrect":strict,"strictTotal":total,"accuracy":strict/total,"antiOverbuildFalseOrdivon":sum(1 for r in anti if r["owner"] in opaque),"antiOverbuildTotal":len(anti),"antiOverbuildFalseOrdivonRate":sum(1 for r in anti if r["owner"] in opaque)/len(anti),"totalTokens":sum(t["usage"]["totalTokens"] for t in selected),"providerCalls":sum(t["usage"]["providerCalls"] for t in selected)}
    a=out["repository_first"]; b=out["causal_first"]
    superior=b["accuracy"]>=a["accuracy"]+.08 and b["antiOverbuildFalseOrdivonRate"]<=a["antiOverbuildFalseOrdivonRate"]
    ceiling=a["accuracy"]>=.95 and b["accuracy"]>=.95 and b["accuracy"]>=a["accuracy"] and b["antiOverbuildFalseOrdivonRate"]<=a["antiOverbuildFalseOrdivonRate"]
    return {"treatments":out,"classification":"SUPERIOR" if superior else ("CEILING_EQUIVALENT" if ceiling else "MIXED_OR_FAILED"),"pairedReplicates":[{"replicate":r,"repositoryCorrect":next(t for t in trials if t["replicate"]==r and t["treatment"]=="repository_first")["strictCorrect"],"causalCorrect":next(t for t in trials if t["replicate"]==r and t["treatment"]=="causal_first")["strictCorrect"]} for r in range(1,CORPUS["replicates"]+1)]}


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=pathlib.Path,default=ROOT/"evidence"/"stress-live-v1.json"); args=parser.parse_args()
    secpaths=secrets(); trials=[]
    for rep in range(1,CORPUS["replicates"]+1):
        m=mapping(rep); sp=secpaths[(rep-1)%len(secpaths)]; sec=json.loads(sp.read_text(encoding="utf-8")); order=["repository_first","causal_first"] if rep%2 else ["causal_first","repository_first"]
        for treatment in order:
            cases=list(CORPUS["cases"]); random.Random(f"ex1b:{rep}:{treatment}").shuffle(cases)
            result,usage=call(sec,treatment,rep,cases,m); bycase={c["id"]:c for c in cases}; rows=[]
            for answer in result["answers"]:
                c=bycase[answer["caseId"]]; oracle=render(c["oracle"],m); rows.append({"caseId":c["id"],"subset":c["subset"],"oracle":oracle,"owner":answer["owner"],"correct":answer["owner"]==oracle,"reason":answer["reason"]})
            trial={"treatment":treatment,"replicate":rep,"ownerMapping":{"HOST":m["{{HOST}}"],"HARNESS":m["{{HARNESS}}"],"RUNTIME":m["{{RUNTIME}}"]},"secretSlot":sp.name,"caseOrder":[c["id"] for c in cases],"result":rows,"strictCorrect":sum(r["correct"] for r in rows),"strictTotal":len(rows),"usage":usage,"providerModel":result["providerModel"]}; trials.append(trial); print(json.dumps({"replicate":rep,"treatment":treatment,"correct":trial["strictCorrect"],"total":trial["strictTotal"],"tokens":usage["totalTokens"],"calls":usage["providerCalls"]},sort_keys=True),flush=True)
    ev={"schemaVersion":1,"kind":"ordivon.explanation-existence-stress-live-evidence","corpusDigest":digest(CORPUS),"trialCount":len(trials),"trials":trials,"analysis":analyze(trials)}; args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(ev,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(ev["analysis"],sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
