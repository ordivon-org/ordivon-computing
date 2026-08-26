from __future__ import annotations
import json, subprocess
from pathlib import Path
CASES=[
("S6-WEB-CURRENTNESS","/root/projects/ordivon-web","e278ad113e58813f8f4d202ecafbe91e22c93931"),
("S6-SECURITY-CONSUMPTION","/root/projects/ordivon-security","cac3fe19240a87b6ea39750ad19ad5e2b7664e2b"),
("S6-HOST-PROVIDER-FIRST","/root/projects/ordivon-host","507589eb1ae602f788913c7a8fdfd7bad355fe6c"),
("S6-HOST-CAPABILITY-CONTRACTION","/root/projects/ordivon-host","bc5c83f9a1ca50cf0fbff5b529d386f070db373f"),
("S6-HOST-COORDINATION-CONTRACTION","/root/projects/ordivon-host","6b3ce2c38e24a6fa8b1c229ae1184ec3efe4d24a"),
("S6-METHOD-CANON","/root/projects/ordivon-computing","1f4283610190d0097ddacf38ebb5a99f8a0eab85"),
("S6-ATLAS-M0","/root/projects/ordivon-atlas","5da63ed2f0dd67391ec2da63c44f42bdf9171890"),
("S6-HARNESS-CLAIM-STANDING","/root/projects/ordivon-harness","ada33b5562e214e07b587de181126b8349dfebae"),
("S6-FINANCE-REALIZABILITY","/root/projects/ordivon-finance","480e7480bc58d3e21b5c5ef5f2db47935d1a48b4"),
("S6-MEDIA-OMPC","/root/projects/ordivon-media","608bfe654016297700335df97c13ce6c2b479319"),
]
def run(repo,args,check=True):
    p=subprocess.run(["git","-C",repo,*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode: raise RuntimeError((repo,args,p.stderr))
    return p.stdout.strip(),p.returncode
out=[]
for cid,repo,rev in CASES:
    meta,_=run(repo,["show","-s","--format=%H%x1f%aI%x1f%s",rev]); h,dt,sub=meta.split("\x1f",2)
    files,_=run(repo,["diff-tree","--no-commit-id","--name-only","-r",rev]); paths=[x for x in files.splitlines() if x]
    main,_=run(repo,["rev-parse","refs/heads/main"])
    _,anc_rc=run(repo,["merge-base","--is-ancestor",rev,"refs/heads/main"],check=False)
    branches,_=run(repo,["branch","--contains",rev,"--format=%(refname:short)"],check=False)
    current=[]
    for p in paths:
        _,rc=run(repo,["cat-file","-e",f"refs/heads/main:{p}"],check=False)
        current.append({"path":p,"existsOnMain":rc==0})
    later=[]
    if anc_rc==0:
        log,_=run(repo,["log","--date=iso-strict","--format=%H%x1f%aI%x1f%s",f"{rev}..refs/heads/main","--",*paths],check=False)
        for line in log.splitlines():
            if not line: continue
            a=line.split("\x1f",2)
            if len(a)==3: later.append({"revision":a[0],"date":a[1],"subject":a[2]})
    else:
        # Trace descendants anywhere for historical branch plus current-main semantic divergence separately.
        log,_=run(repo,["log","--all","--date=iso-strict","--format=%H%x1f%aI%x1f%s","--ancestry-path",f"{rev}..","--",*paths],check=False)
        for line in log.splitlines():
            if not line: continue
            a=line.split("\x1f",2)
            if len(a)==3: later.append({"revision":a[0],"date":a[1],"subject":a[2]})
    out.append({"caseId":cid,"repo":repo,"t0Revision":h,"t0Date":dt,"t0Subject":sub,"currentMain":main,"t0AncestorOfMain":anc_rc==0,"branchesContainingT0":[x.strip() for x in branches.splitlines() if x.strip()],"t0Paths":paths,"currentPathState":current,"laterPathCommits":later[:100]})
Path("research/experiments/s6-longitudinal-v0/lineage-mining-v1.json").write_text(json.dumps({"schemaVersion":1,"cases":out},ensure_ascii=False,indent=2,sort_keys=True)+"\n")
for c in out:
    print(c['caseId'], 'ancestor='+str(c['t0AncestorOfMain']), 'paths='+str(len(c['t0Paths'])), 'survive='+str(sum(x['existsOnMain'] for x in c['currentPathState']))+'/'+str(len(c['currentPathState'])), 'laterPathCommits='+str(len(c['laterPathCommits'])), 'main='+c['currentMain'][:10])
