#!/usr/bin/env python3
"""Verify Computer source publication without collapsing local and remote truth."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()
def is_ancestor(a: str, b: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--mode",choices=["preflight","published"],required=True); parser.add_argument("--fetch",action="store_true"); args=parser.parse_args()
    if args.fetch: subprocess.run(["git","fetch","origin","--prune"],cwd=ROOT,check=True)
    local=run("git","rev-parse","HEAD"); tracking=run("git","rev-parse","origin/main"); advertised=run("git","ls-remote","--heads","origin","main").split()[0]
    result={"schemaVersion":1,"kind":"ordivon.source-distribution-assessment","localHead":local,"remoteTrackingMain":tracking,"advertisedRemoteMain":advertised,"remoteTrackingMatchesAdvertised":tracking==advertised,"remoteIsAncestorOfLocal":is_ancestor(advertised,local),"localIsAncestorOfRemote":is_ancestor(local,advertised),"published":local==tracking==advertised}
    print(json.dumps(result,indent=2,sort_keys=True))
    if args.mode=="preflight": return 0 if result["remoteTrackingMatchesAdvertised"] and result["remoteIsAncestorOfLocal"] else 2
    return 0 if result["published"] else 2
if __name__=="__main__": raise SystemExit(main())
