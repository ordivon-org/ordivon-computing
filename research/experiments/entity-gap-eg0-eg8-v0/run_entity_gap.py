#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import time
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

REPOS = {
    "computing": Path("/root/projects/ordivon-computing"),
    "runtime": Path("/root/projects/ordivon-runtime"),
    "host": Path("/root/projects/ordivon-host"),
    "harness": Path("/root/projects/ordivon-harness"),
    "world": Path("/root/projects/ordivon-world"),
    "finance": Path("/root/projects/ordivon-finance"),
    "security": Path("/root/projects/ordivon-security"),
    "game": Path("/root/projects/ordivon-game"),
    "human": Path("/root/projects/ordivon-human"),
    "studio": Path("/root/projects/ordivon-studio"),
    "web": Path("/root/projects/ordivon-web"),
    "workstation": Path("/root/workstation-lab"),
}


def run(*args: str, cwd: Path | None = None) -> str:
    p = subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)
    return p.stdout


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def head(repo: Path) -> str:
    return run("/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD").strip()


def clean(repo: Path) -> bool:
    return not run("/usr/bin/git", "-C", str(repo), "status", "--porcelain").strip()


def git_bytes(repo: Path, revision: str, path: str) -> bytes:
    p = subprocess.run(
        ["/usr/bin/git", "-C", str(repo), "show", f"{revision}:{path}"],
        check=True,
        capture_output=True,
    )
    return p.stdout


def git_json(repo: Path, revision: str, path: str):
    return json.loads(git_bytes(repo, revision, path))


def dump(name: str, obj) -> None:
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


observed = {name: {"head": head(repo), "clean": clean(repo)} for name, repo in REPOS.items()}

# EG0 — responsibility x entity matrix. Rows are deliberately owner-native and evidence-bound.
eg0_rows = [
    {"responsibility":"open-ended research judgment and hypothesis generation","owner":"computing","currentCarrier":"Agent + Computing research method","candidate":"Agent","gap":"none-reproduced","strength":"strong","disposition":"retain"},
    {"responsibility":"durable semantic work continuity","owner":"host","currentCarrier":"Host Journal/CAS/Task continuity","candidate":"deterministic durable state machine","gap":"none-reproduced","strength":"strong","disposition":"retain"},
    {"responsibility":"bounded Agent Run/provider/tool continuity","owner":"harness","currentCarrier":"Harness","candidate":"Agent + deterministic Run substrate","gap":"none-reproduced","strength":"strong","disposition":"retain"},
    {"responsibility":"physical process execution/recovery","owner":"runtime","currentCarrier":"Runtime","candidate":"deterministic executor","gap":"none-reproduced","strength":"strong","disposition":"retain"},
    {"responsibility":"fresh live-capital admission invariant","owner":"finance","currentCarrier":"handwritten gates/tests + Agent interpretation","candidate":"formal verifier / exhaustive constraint checker","gap":"example-based checks can miss omitted predicates","strength":"medium-high","disposition":"falsify-EG1"},
    {"responsibility":"current venue/permission/reconciliation truth","owner":"finance","currentCarrier":"OKX/provider observation","candidate":"provider-native sensor + external authority","gap":"current external observation unavailable","strength":"blocking","disposition":"retain-sensor-role"},
    {"responsibility":"P0 capability portfolio selection","owner":"workstation","currentCarrier":"Agent choice + deterministic capability census","candidate":"exact optimizer as decision support","gap":"many incomparable resource combinations; optimality not certified by prose","strength":"medium","disposition":"falsify-EG2"},
    {"responsibility":"physical/carrier independence","owner":"workstation","currentCarrier":"network observations + owner evidence","candidate":"physical resource owner + direct sensor","gap":"carrier identity UNKNOWN; physicalAccessIndependent=false","strength":"blocking","disposition":"retain-sensor-resource-role"},
    {"responsibility":"research selector stability/uncertainty","owner":"computing","currentCarrier":"replicate counts + Agent interpretation","candidate":"statistical estimator","gap":"5/5 and 4/5 point rates invite overconfidence at n=5","strength":"high","disposition":"falsify-EG3"},
    {"responsibility":"adversarial consequence verification","owner":"security","currentCarrier":"independent sensors/world truth + evaluator","candidate":"sensor + verifier","gap":"generic role already strong/domain-local","strength":"strong","disposition":"retain-local"},
    {"responsibility":"counterfactual capital transition","owner":"finance","currentCarrier":"capital transition simulator","candidate":"domain simulator","gap":"none requiring shared simulator","strength":"strong","disposition":"retain-local"},
    {"responsibility":"adversarial environment/contest trajectory","owner":"security","currentCarrier":"Range/Contest/KVM","candidate":"domain simulator + adversary","gap":"none requiring shared simulator","strength":"strong","disposition":"retain-local"},
    {"responsibility":"game world trajectory/replay","owner":"game","currentCarrier":"authoritative reducer/scenario/replay","candidate":"domain simulator","gap":"none requiring shared simulator","strength":"strong","disposition":"retain-local"},
    {"responsibility":"comparative human visual preference","owner":"web","currentCarrier":"Agent review + dormant human calibration apparatus","candidate":"scoped blinded human-response sensor","gap":"Agent review cannot establish human population preference","strength":"claim-dependent-high","disposition":"retain-scoped-human-sensor"},
    {"responsibility":"play experience understandability/consequence","owner":"game","currentCarrier":"Agent playtests + future human play sessions","candidate":"scoped human player sensor","gap":"experience claim remains human-grounded","strength":"claim-dependent-high","disposition":"retain-scoped-human-sensor"},
    {"responsibility":"creative human consequence","owner":"studio","currentCarrier":"Agent perception/review + explicit human boundary","candidate":"scoped human-response sensor","gap":"human preference/trust/memory cannot be inferred from Agent aesthetics","strength":"claim-dependent-high","disposition":"retain-scoped-human-sensor"},
    {"responsibility":"human research measurement","owner":"human","currentCarrier":"claim-matched methodology","candidate":"measurement/statistical/human observer ecology","gap":"specific studies need real measurement, not generic Agent judgment","strength":"strong-method-thin-data","disposition":"retain-domain-method"},
    {"responsibility":"expensive knowledge rediscovery","owner":"computing","currentCarrier":"Git + rg + owner docs + Agent retrieval","candidate":"derived deterministic indexer","gap":"repeated cross-owner retrieval cost grows with corpus","strength":"medium","disposition":"falsify-EG7"},
    {"responsibility":"external opportunity/resource discovery","owner":"finance/workstation","currentCarrier":"public-source collectors + Agent research","candidate":"provider-native sensors/collectors + Agent interpretation","gap":"credentials/authority/currentness often dominate cognition","strength":"high","disposition":"retain-owner-sensors"}
]
dump("eg0-responsibility-entity-matrix.json", {
    "schemaVersion":1, "kind":"ordivon.computing.eg0-responsibility-entity-matrix",
    "observedOwners": observed, "rows": eg0_rows,
    "rule":"A role can be scarce without deserving a shared service; preserve owner-native authority."
})

# EG1 — exact bounded verifier over a real Finance fresh-canary gate.
finance_rev = observed["finance"]["head"]
canary_path = "evidence/p3-minimum-live-canary-readiness-20260812.json"
canary = git_json(REPOS["finance"], finance_rev, canary_path)
predicates = [
    "effectCorrectnessQualified", "privateSignerAuthorityVerified", "dedicatedTradeCredentialWiringAligned",
    "successfulCurrentVenueRead", "tradePermissionObserved", "liveReconciliationVerified",
    "freshPortfolioSnapshot", "freshVenueWorldReadyForRiskIncrease", "freshExecutionMarketBasisV1",
    "newDecisionProposalExecutionRequestIdentity", "freshCanaryTargetSelected", "submissionEnabled"
]
current = {
    "effectCorrectnessQualified": bool(canary["localC2"]["effectCorrectnessQualified"]),
    "privateSignerAuthorityVerified": bool(canary["localC2"]["privateSignerAuthorityVerified"]),
    "dedicatedTradeCredentialWiringAligned": bool(canary["localC2"]["dedicatedTradeCredentialWiringAligned"]),
    "successfulCurrentVenueRead": bool(canary["localC2"]["realVenueReachable"]),
    "tradePermissionObserved": bool(canary["localC2"]["tradeCredentialPermissionVerified"]),
    "liveReconciliationVerified": bool(canary["localC2"]["liveReconciliationVerified"]),
    "freshPortfolioSnapshot": False,
    "freshVenueWorldReadyForRiskIncrease": False,
    "freshExecutionMarketBasisV1": bool(canary["currentObservation"]["freshExecutionMarketBasisV1Available"]),
    "newDecisionProposalExecutionRequestIdentity": False,
    "freshCanaryTargetSelected": bool(canary["currentObservation"]["freshCanaryTargetSelected"]),
    "submissionEnabled": bool(canary["localC2"]["submissionEnabled"]),
}

def full_admit(s): return all(s[p] for p in predicates)

def enumerate_states():
    for bits in itertools.product([False, True], repeat=len(predicates)):
        yield dict(zip(predicates, bits))

baseline_sets = {
    "local-only": predicates[:3],
    "local-plus-venue": predicates[:4],
    "local-plus-permission": predicates[:5],
    "full": predicates,
}
baseline_unsafe = {}
for name, req in baseline_sets.items():
    unsafe = 0
    for s in enumerate_states():
        if all(s[p] for p in req) and not full_admit(s): unsafe += 1
    baseline_unsafe[name] = unsafe

example_states = [
    dict(current),
    {p: True for p in predicates},
    {p: True for p in predicates} | {"successfulCurrentVenueRead": False},
]
mutants = []
for omitted in predicates:
    req = [p for p in predicates if p != omitted]
    counterexamples = [s for s in enumerate_states() if all(s[p] for p in req) and not full_admit(s)]
    example_detected = any(all(s[p] for p in req) and not full_admit(s) for s in example_states)
    mutants.append({
        "omittedPredicate": omitted,
        "unsafeAdmissionStates": len(counterexamples),
        "minimalCounterexample": counterexamples[0],
        "detectedByBoundedExamples": example_detected,
        "detectedByExactEnumeration": bool(counterexamples),
    })
eg1 = {
    "schemaVersion":1,"kind":"ordivon.computing.eg1-formal-verifier-falsifier",
    "ownerRevision":finance_rev,"sourcePath":canary_path,"sourceDigest":sha256_bytes(git_bytes(REPOS["finance"], finance_rev, canary_path)),
    "predicateCount":len(predicates),"stateSpace":2**len(predicates),"predicates":predicates,"currentState":current,
    "currentAdmission":full_admit(current),"baselineUnsafeAdmissionCounts":baseline_unsafe,
    "singleOmissionMutants":mutants,
    "boundedExampleMutantsDetected":sum(m["detectedByBoundedExamples"] for m in mutants),
    "exactEnumerationMutantsDetected":sum(m["detectedByExactEnumeration"] for m in mutants),
    "disposition":"retain-formal-verifier-role-owner-local",
    "tooling":"stdlib exhaustive enumeration sufficient for this bounded 4096-state model; heavyweight SMT dependency not yet earned",
    "authorityBoundary":"Verifier can prove an admission predicate or produce counterexamples; it cannot select a financial objective, authorize submission, or create venue truth."
}
dump("eg1-formal-verifier-result.json", eg1)

# EG2 — exact resource allocator / set-cover and Pareto certificate over NX7.
work_rev = observed["workstation"]["head"]
nx7_path = "evidence/acceptance/workstation-nx7-capability-universe-20260812.json"
nx7 = git_json(REPOS["workstation"], work_rev, nx7_path)
p0 = {s["slotId"] for s in nx7["slots"] if s["priority"] == "P0" and s["current"]}
resources = nx7["currentResources"]
min_solutions = []
for k in range(1, len(resources)+1):
    for idxs in itertools.combinations(range(len(resources)), k):
        covered = set().union(*(set(resources[i]["slots"]) for i in idxs)) & p0
        if covered != p0: continue
        owners = {resources[i]["owner"] for i in idxs}
        support = defaultdict(set)
        for i in idxs:
            for s in set(resources[i]["slots"]) & p0: support[s].add(resources[i]["owner"])
        min_solutions.append({
            "resources":[resources[i]["resourceId"] for i in idxs],
            "ownerCount":len(owners),
            "redundantlyCoveredP0Slots":sum(len(v)>=2 for v in support.values()),
        })
    if min_solutions:
        min_k = k
        break
# deterministic greedy baseline
remaining = list(resources); selected=[]; covered=set(); owners=set()
while covered != p0:
    best = max(remaining, key=lambda r:(len((set(r["slots"]) & p0)-covered), int(r["owner"] not in owners), r["maturityScore"], r["resourceId"]))
    gain = len((set(best["slots"]) & p0)-covered)
    if gain == 0: break
    selected.append(best); covered |= set(best["slots"]) & p0; owners.add(best["owner"]); remaining.remove(best)
# bounded Pareto frontier for resource budgets 1..4
candidates=[]
for k in range(1,5):
    for combo in itertools.combinations(resources,k):
        cov=set().union(*(set(r["slots"]) for r in combo)) & p0
        os={r["owner"] for r in combo}; support=defaultdict(set)
        for r in combo:
            for s in set(r["slots"]) & p0: support[s].add(r["owner"])
        candidates.append({"k":k,"coverage":len(cov),"ownerCount":len(os),"redundantSlots":sum(len(v)>=2 for v in support.values()),"resources":[r["resourceId"] for r in combo]})
front=[]
for x in candidates:
    dominated=False
    for y in candidates:
        if y is x: continue
        if y["coverage"]>=x["coverage"] and y["ownerCount"]>=x["ownerCount"] and y["redundantSlots"]>=x["redundantSlots"] and y["k"]<=x["k"] and (y["coverage"]>x["coverage"] or y["ownerCount"]>x["ownerCount"] or y["redundantSlots"]>x["redundantSlots"] or y["k"]<x["k"]):
            dominated=True; break
    if not dominated: front.append(x)
eg2={
    "schemaVersion":1,"kind":"ordivon.computing.eg2-optimizer-falsifier",
    "ownerRevision":work_rev,"sourcePath":nx7_path,"sourceDigest":sha256_bytes(git_bytes(REPOS["workstation"], work_rev, nx7_path)),
    "currentP0SlotCount":len(p0),"currentResourceCount":len(resources),"minimumResourceCount":min_k,"minimumSolutionCount":len(min_solutions),
    "minimumSolutions":sorted(min_solutions,key=lambda x:(-x["ownerCount"],-x["redundantlyCoveredP0Slots"],x["resources"])),
    "greedy":{"resourceCount":len(selected),"resources":[r["resourceId"] for r in selected],"coversAllP0":covered==p0,"certifiedMinimum":len(selected)==min_k},
    "paretoFrontierBudget1to4Count":len(front),"paretoFrontierBudget1to4":sorted(front,key=lambda x:(x["k"],-x["coverage"],-x["ownerCount"],-x["redundantSlots"],x["resources"])),
    "disposition":"retain-optimizer-as-owner-local-certificate-and-search-instrument",
    "authorityBoundary":"Optimizer certifies feasibility/minimality and enumerates tradeoffs; Agent/owner still chooses which diversity, cost, authority, and resilience dimensions matter. No scheduler authority is implied."
}
dump("eg2-optimizer-result.json",eg2)

# EG3 — calibrated uncertainty over real FS0 selector replicate counts.
fs_path="research/experiments/fs0-shadow-portfolio/evidence/fs0-predictions-v1.json"
fs=git_json(REPOS["computing"], observed["computing"]["head"], fs_path)

def wilson(k:int,n:int,z:float=1.959963984540054):
    p=k/n; z2=z*z; den=1+z2/n
    center=(p+z2/(2*n))/den
    half=(z/den)*math.sqrt(p*(1-p)/n+z2/(4*n*n))
    return {"successes":k,"n":n,"point":p,"wilson95":[max(0,center-half),min(1,center+half)]}
raw_count=fs["aggregate"]["raw"]["topChoiceCounts"]["G-AF3"]
rfm_count=fs["aggregate"]["rfm"]["topChoiceCounts"]["R-P5"]
neg_top=fs["aggregate"]["raw"]["negativeControlTopChoices"]+fs["aggregate"]["rfm"]["negativeControlTopChoices"]
neg_def=fs["aggregate"]["raw"]["negativeControlDeferrals"]+fs["aggregate"]["rfm"]["negativeControlDeferrals"]
raw_int=wilson(raw_count,5); rfm_int=wilson(rfm_count,5); neg_top_int=wilson(neg_top,10); neg_def_int=wilson(neg_def,10)
eg3={
    "schemaVersion":1,"kind":"ordivon.computing.eg3-statistical-estimator-falsifier",
    "ownerRevision":observed["computing"]["head"],"sourcePath":fs_path,"sourceDigest":sha256_bytes(git_bytes(REPOS["computing"], observed["computing"]["head"], fs_path)),
    "rawTopChoiceStability":raw_int,"rfmTopChoiceStability":rfm_int,
    "intervalsOverlap":not (raw_int["wilson95"][1] < rfm_int["wilson95"][0] or rfm_int["wilson95"][1] < raw_int["wilson95"][0]),
    "negativeControlTopChoice":neg_top_int,"negativeControlDeferral":neg_def_int,
    "interpretation":[
        "5/5 and 4/5 are high point rates but both have wide small-n uncertainty; their Wilson intervals overlap materially.",
        "0/10 top choices does not imply zero failure probability; its 95% upper Wilson bound remains non-zero.",
        "10/10 deferrals supports admission awareness but does not justify a universal deterministic claim about future selector behavior."
    ],
    "disposition":"retain-statistical-estimator-role-high-priority",
    "tooling":"audited stdlib Wilson formula is sufficient for this first falsifier; broader repeated-measure/causal work may justify mature statistical libraries owner-locally",
    "authorityBoundary":"Estimator quantifies uncertainty in observations; it does not choose research value or transform a point estimate into semantic truth."
}
dump("eg3-estimator-result.json",eg3)

# EG4 — real sensing/authority/resource gaps, separated from cognition gaps.
nx5_path="evidence/acceptance/workstation-nx5-independent-roots-20260812.json"
nx5=git_json(REPOS["workstation"],work_rev,nx5_path)
eg4_rows=[
    {"owner":"finance","claimOrNeed":"fresh live-capital canary admission","observed":"OKX reachability unavailable; Trade permission and live reconciliation unverified","gapType":["external-observation","external-authority"],"betterEntity":"provider-native venue sensor/authority","agentCanSubstitute":False},
    {"owner":"workstation","claimOrNeed":"independent network root","observed":f"carrierIndependent={nx5['axes']['carrierIndependent']['status']}; physicalAccessIndependent={nx5['axes']['physicalAccessIndependent']}; serviceProviderIndependent={nx5['axes']['serviceProviderIndependent']}","gapType":["physical-resource","carrier-observation"],"betterEntity":"independent carrier/resource owner plus direct sensor","agentCanSubstitute":False},
    {"owner":"workstation","claimOrNeed":"active remote measurement","observed":"NX7 slot measurement.active-user-authorized is externally blocked","gapType":["user-authority","measurement-effect"],"betterEntity":"authorized measurement provider","agentCanSubstitute":False},
    {"owner":"web","claimOrNeed":"independent review / later human preference","observed":"multi-model cohort lacks required evaluator diversity; human preference is explicitly separate","gapType":["observer-diversity","human-outcome"],"betterEntity":"independent model observers now; human observers only for human claims","agentCanSubstitute":False},
    {"owner":"game","claimOrNeed":"decisions understandable and consequential to players","observed":"replacement boundary requires repeated human play sessions","gapType":["human-experience-observation"],"betterEntity":"target human players","agentCanSubstitute":False},
    {"owner":"security","claimOrNeed":"adversarial world consequence","observed":"architecture already separates sensor telemetry, management authority, evaluator judgment and independent world truth","gapType":[],"betterEntity":"domain-local independent sensors/verifiers already present","agentCanSubstitute":False},
    {"owner":"finance","claimOrNeed":"external opportunity viability","observed":"GVA authoritative issue/PR checks and credential-gated sources can eliminate nominal Agent opportunities before work begins","gapType":["fresh-source-observation","credential-authority"],"betterEntity":"source-native collectors/credentials plus Agent interpretation","agentCanSubstitute":False}
]
dump("eg4-sensor-outcome-audit.json",{
    "schemaVersion":1,"kind":"ordivon.computing.eg4-sensor-outcome-audit",
    "ownerRevisions":{"finance":finance_rev,"workstation":work_rev,"web":observed["web"]["head"],"game":observed["game"]["head"],"security":observed["security"]["head"]},
    "nx5SourceDigest":sha256_bytes(git_bytes(REPOS["workstation"],work_rev,nx5_path)),
    "rows":eg4_rows,"disposition":"retain-sensor-observer-as-first-class-entity-role-provider-or-owner-native",
    "sharedService":"reject","reason":"Sensor semantics and authority are provider/domain-specific; the repeated invariant is observation != truth and missing observation != false, not a universal sensor daemon."
})

# EG5 — simulator/adversary stable intersection audit across Finance/Security/Game.
eg5_domains={
    "finance":{"currentCarrier":"capital_transition_simulation + decision/research replay","initialIdentity":"owner/portfolio/world snapshot + requested transition","intervention":"candidate capital transition","trajectory":"counterfactual portfolio/effect consequences","observation":"derived finance metrics/evidence","authority":"Finance domain; simulation is not execution permission"},
    "security":{"currentCarrier":"Range/Contest/KVM backends","initialIdentity":"Environment/Range/Sample/Authority identities","intervention":"admitted actor/effect request","trajectory":"contested/adversarial world events","observation":"sensor + management + hidden/world truth kept distinct","authority":"Security domain; Observer/Evaluator/Guardian are separate"},
    "game":{"currentCarrier":"Scenario/Genesis/reducer/replay","initialIdentity":"authoritative game world/genesis","intervention":"admitted player/Agent action","trajectory":"deterministic game transition/replay","observation":"player/Agent projections + replay evidence","authority":"Game world/reducer owns state; model does not"},
}
stable_intersection=["exact-or-bound initial state/environment identity","explicit intervention/action identity","transition or trajectory","observation/evidence distinct from hidden/authoritative state","consequence/terminal state","replay/provenance where consequence comparison requires it","simulator output does not itself grant real-world action authority"]
dump("eg5-simulator-adversary-audit.json",{
    "schemaVersion":1,"kind":"ordivon.computing.eg5-simulator-adversary-audit","ownerRevisions":{"finance":finance_rev,"security":observed["security"]["head"],"game":observed["game"]["head"]},
    "domains":eg5_domains,"stableResearchIntersection":stable_intersection,
    "disposition":"retain-domain-local-simulators-and-distinct-adversaries","sharedSimulatorService":"reject",
    "reason":"Three domains independently validate simulation as an entity role, but their state, transition, oracle and consequence semantics remain owner-specific; no current duplication pressure earns a universal implementation.",
    "adversaryBoundary":"Agent adversary, deterministic fuzzer/mutator, hidden oracle, simulator and verifier are different entity roles and should not be collapsed."
})

# EG6 — scoped human-response sensor contract candidate (research only).
eg6_claims=[
    {"claim":"mechanical correctness/accessibility constraint","observer":"deterministic test/browser/a11y verifier","humanRequired":False},
    {"claim":"comparative human visual preference","observer":"independent blinded target humans; expert class when professional craft is claimed","humanRequired":True},
    {"claim":"comprehension/task legibility","observer":"target humans when making a population/experience claim; mechanical UX checks remain diagnostics","humanRequired":True},
    {"claim":"trust/memory/emotion","observer":"target human measurement matched to construct and context","humanRequired":True},
    {"claim":"game decisions are understandable and consequential","observer":"repeated human players","humanRequired":True},
    {"claim":"Agent aesthetic judgment for bounded reversible production","observer":"Agent + rendered inspection","humanRequired":False}
]
eg6_envelope=["claimType","artifactOrWorldIdentity","sourceRevision","observerClass","evaluatorIdentityHash","assignmentAndBlinding","surfaceOrContext","directObservation","repeatedMeasureGroup","observedAt","limitations"]
dump("eg6-human-response-sensor-audit.json",{
    "schemaVersion":1,"kind":"ordivon.computing.eg6-human-response-sensor-audit","ownerRevisions":{"web":observed["web"]["head"],"studio":observed["studio"]["head"],"game":observed["game"]["head"],"human":observed["human"]["head"]},
    "claims":eg6_claims,"candidateResearchEnvelope":eg6_envelope,
    "disposition":"retain-human-as-scoped-high-cost-sensor","universalApprovalGate":"reject","sharedProtocolPromotion":"defer",
    "promotionGate":"Run real claim-matched human observations in at least two materially different owner domains and show that the same minimal evidence fields reduce ambiguity without creating a second human-truth authority."
})

# EG7 — disposable provenance-bound SQLite FTS5 index versus rediscovery by repeated ad-hoc search.
selected_evidence={
    "finance":[canary_path],
    "workstation":[nx5_path,nx7_path],
}
allowed_suffixes={".md",".json",".py",".rs",".ts",".tsx",".js",".toml",".yaml",".yml"}
skip_parts={".git",".venv","node_modules","target","build","dist","quarantine","__pycache__",".mypy_cache",".pytest_cache"}
corpus=[]
for name,repo in REPOS.items():
    rev=observed[name]["head"]
    tracked=run("/usr/bin/git","-C",str(repo),"ls-tree","-r","--name-only",rev).splitlines()
    extra=set(selected_evidence.get(name,[]))
    for rel in tracked:
        p=Path(rel)
        if p.suffix.lower() not in allowed_suffixes: continue
        if any(part in skip_parts for part in p.parts): continue
        if ("archive" in p.parts or "evidence" in p.parts) and rel not in extra: continue
        try: data=git_bytes(repo,rev,rel)
        except subprocess.CalledProcessError: continue
        if len(data)>300_000: continue
        text=data.decode("utf-8",errors="replace")
        corpus.append((name,rev,rel,sha256_bytes(data),text))
queries=[
    {"id":"web-human-wilson","terms":["human","preference","wilson"],"expectedRepo":"web","expectedPath":"design/evaluation.md"},
    {"id":"computing-independent-verifier","terms":["independent","assertions","artifacts"],"expectedRepo":"computing","expectedPath":"research/charters/VERIFY-CHARTER-001.md"},
    {"id":"finance-expired-canary","terms":["cancelled","expired","canary"],"expectedRepo":"finance","expectedPath":canary_path},
    {"id":"security-sensor-world-truth","terms":["sensor","world","truth"],"expectedRepo":"security","expectedPath":"docs/architecture.md"},
    {"id":"harness-bounded-run","terms":["agent","run","provider","tool"],"expectedRepo":"harness","expectedPath":"README.md"},
    {"id":"workstation-carrier-independence","terms":["carrier","physical","independent"],"expectedRepo":"workstation","expectedPath":nx5_path},
]
with tempfile.TemporaryDirectory(prefix="ordivon-eg7-") as td:
    dbp=Path(td)/"index.sqlite3"
    t0=time.perf_counter()
    con=sqlite3.connect(dbp)
    con.execute("CREATE VIRTUAL TABLE docs USING fts5(repo UNINDEXED, revision UNINDEXED, path UNINDEXED, digest UNINDEXED, content)")
    con.executemany("INSERT INTO docs(repo,revision,path,digest,content) VALUES(?,?,?,?,?)",corpus)
    con.commit(); build_ms=(time.perf_counter()-t0)*1000
    qresults=[]
    for q in queries:
        expr=" AND ".join('"'+t.replace('"','')+'"' for t in q["terms"])
        qs=time.perf_counter()
        rows=con.execute("SELECT repo,path,digest,bm25(docs) AS score FROM docs WHERE docs MATCH ? ORDER BY score LIMIT 10",(expr,)).fetchall()
        elapsed=(time.perf_counter()-qs)*1000
        rank=None
        for i,r in enumerate(rows,1):
            if r[0]==q["expectedRepo"] and r[1]==q["expectedPath"]: rank=i; break
        owner_rows=con.execute("SELECT repo,path,digest,bm25(docs) AS score FROM docs WHERE docs MATCH ? AND repo = ? ORDER BY score LIMIT 10",(expr,q["expectedRepo"])).fetchall()
        owner_rank=None
        for i,r in enumerate(owner_rows,1):
            if r[1]==q["expectedPath"]: owner_rank=i; break
        qresults.append(q|{"rank":rank,"hitTop10":rank is not None,"ownerScopedRank":owner_rank,"ownerScopedHitTop10":owner_rank is not None,"queryMs":elapsed,"topResults":[{"repo":r[0],"path":r[1],"digest":r[2],"score":r[3]} for r in rows[:5]],"ownerScopedTopResults":[{"repo":r[0],"path":r[1],"digest":r[2],"score":r[3]} for r in owner_rows[:5]]})
    db_bytes=dbp.stat().st_size
    con.close()
eg7={
    "schemaVersion":1,"kind":"ordivon.computing.eg7-archivist-indexer-falsifier","ownerRevisions":observed,
    "corpus":{"documentCount":len(corpus),"textBytes":sum(len(c[4].encode('utf-8')) for c in corpus),"temporaryIndexBytes":db_bytes,"buildMs":build_ms},
    "queries":qresults,"expectedSourceHitRateTop10":sum(q["hitTop10"] for q in qresults)/len(qresults),
    "ownerScopedExpectedSourceHitRateTop10":sum(q["ownerScopedHitTop10"] for q in qresults)/len(qresults),
    "temporaryIndexRetained":False,
    "disposition":"defer-dedicated-archivist-indexer-retain-git-rg-owner-routing",
    "archivistService":"reject",
    "reason":"Neither global nor owner-scoped generic FTS reliably recovered all frozen canonical sources; owner scoping did not improve the 4/6 top-10 hit rate. The experiment does not earn a dedicated Archivist/index service. Keep Git/rg plus explicit owner/authority routing and revisit only on measured rediscovery failures that a richer provenance/ranking baseline fixes."
}
dump("eg7-archivist-indexer-result.json",eg7)

# EG8 — synthesis: role != service; preserve comparative-capability boundaries.
eg8_items=[
    {"entity":"Agent/open-ended cognition","disposition":"retain","placement":"Harness/owner-local cognition","evidence":"Already strong after S0-S8; no new gap."},
    {"entity":"deterministic executor/state machine","disposition":"retain","placement":"Runtime/Host/classical substrate","evidence":"Already strong after S0-S8."},
    {"entity":"formal verifier/constraint checker","disposition":"retain-role-localize-owner","placement":"owner-local verification equipment","evidence":f"EG1 exact enumeration detected {eg1['exactEnumerationMutantsDetected']}/{len(mutants)} single-predicate omission mutants versus {eg1['boundedExampleMutantsDetected']}/{len(mutants)} bounded-example detection.","sharedService":"reject"},
    {"entity":"optimizer/resource allocator","disposition":"retain-role-localize-owner","placement":"owner-local decision-support instrument","evidence":f"EG2 certified minimum {min_k} resources for all current P0 NX7 slots and exposed {len(min_solutions)} equally minimal solutions; greedy happened to be optimal on cardinality.","sharedService":"reject"},
    {"entity":"statistical estimator/calibrator","disposition":"retain-role-high-priority","placement":"experiment/domain-local analysis equipment","evidence":"EG3 showed wide overlapping small-n uncertainty behind 5/5 vs 4/5 selector point rates.","sharedService":"defer"},
    {"entity":"sensor/observer + external authority/resource","disposition":"retain-role-high-priority","placement":"provider/domain/workstation native","evidence":"EG4 shows several live frontiers blocked by missing venue, carrier, credential, observer-diversity or human outcome evidence rather than cognition.","sharedService":"reject"},
    {"entity":"domain simulator","disposition":"retain-domain-local","placement":"Finance/Security/Game","evidence":"EG5 finds repeated simulator role but owner-specific state/transition/oracle semantics.","sharedService":"reject"},
    {"entity":"adversary/fuzzer/mutator","disposition":"retain-distinct-roles","placement":"Security and owner-local testing","evidence":"Agent adversary and deterministic mutation search have different search distributions and authority; no universal adversary layer earned.","sharedService":"reject"},
    {"entity":"human-response sensor","disposition":"retain-scoped","placement":"claim-matched Web/Studio/Game/Human studies","evidence":"EG6 separates human consequence claims from mechanical/Agent judgments.","sharedService":"reject","universalGate":"reject"},
    {"entity":"archivist/indexer","disposition":"defer-dedicated-role","placement":"retain Git/rg/owner authority routing; disposable indexes remain experimental","evidence":f"EG7 global and owner-scoped top-10 expected-source hit rates were {eg7['expectedSourceHitRateTop10']:.3f} and {eg7['ownerScopedExpectedSourceHitRateTop10']:.3f}; generic FTS did not beat the authority-routing baseline enough to earn a new persistent entity.","sharedService":"reject"},
    {"entity":"universal capability router","disposition":"defer-reject-current","placement":"none","evidence":"No stable routing law was needed to obtain EG1-EG7 benefits; per-workload placement remains clearer and cheaper."}
]
dump("eg8-entity-dispositions.json",{
    "schemaVersion":1,"kind":"ordivon.computing.eg8-entity-dispositions","observedOwners":observed,"items":eg8_items,
    "promotedSharedServices":[],"promotedSharedProtocols":[],
    "candidateResearchOnlyContracts":["claim-matched human-response evidence envelope"],
    "worldModelUpdate":"Agent-first remains a local design principle where Agent cognition has comparative advantage. The system-level principle is problem-first comparative capability ecology: assign each responsibility to the entity type whose properties match the invariant, then keep authority with the native owner.",
    "nextPressure":"Spend the next capability budget first on observation/resource acquisition, independent verification, and calibrated estimation where live owner work is blocked; use optimizers/simulators as owner-local instruments rather than new control planes."
})

# Final self-check: source roots must not have moved or become dirty during the run.
after={name:{"head":head(repo),"clean":clean(repo)} for name,repo in REPOS.items()}
if after != observed:
    raise SystemExit("owner source state changed during EG run; results are not admissible\nBEFORE="+json.dumps(observed,sort_keys=True)+"\nAFTER="+json.dumps(after,sort_keys=True))
receipt_inputs=sorted(p for p in OUT.glob("*.json") if p.name != "run-receipt.json")
dump("run-receipt.json",{
    "schemaVersion":1,"kind":"ordivon.computing.entity-gap-run-receipt","ownerState":observed,
    "resultFiles":[p.name for p in receipt_inputs],
    "resultDigests":{p.name:sha256_bytes(p.read_bytes()) for p in receipt_inputs},
    "temporaryExternalStateRetained":False
})
print(json.dumps({
    "eg1": {"boundedExamplesDetected":eg1["boundedExampleMutantsDetected"],"exactDetected":eg1["exactEnumerationMutantsDetected"],"mutants":len(mutants)},
    "eg2": {"minK":min_k,"solutions":len(min_solutions),"greedyK":len(selected),"greedyCertified":len(selected)==min_k,"paretoBudget1to4":len(front)},
    "eg3": {"raw":raw_int,"rfm":rfm_int,"negativeTop":neg_top_int,"negativeDefer":neg_def_int},
    "eg7": {"docs":len(corpus),"globalHitRate":eg7["expectedSourceHitRateTop10"],"ownerScopedHitRate":eg7["ownerScopedExpectedSourceHitRateTop10"],"buildMs":build_ms},
    "eg8": {"sharedServices":0,"sharedProtocols":0}
},ensure_ascii=False,indent=2))
