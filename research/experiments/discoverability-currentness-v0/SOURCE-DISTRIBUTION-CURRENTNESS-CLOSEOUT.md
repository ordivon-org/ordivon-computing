# Source Distribution Currentness — Cross-Owner Closeout

Date: 2026-08-28

Status: **CLOSED IN CURRENT SCOPE / APPLIED ENGINEERING SYNTHESIS / NO GLOBAL SOURCE MANAGER ADMITTED**

This closeout extends the discoverability/currentness programme with a source-distribution pressure that became visible only after owner-native environment and deployment work matured. It does not create a new Foundation and does not redefine Git, Atlas, Host, Runtime, or any owner as a global currentness authority.

## Problem

Several relations had been compressed into the word `current`:

```text
working checkout revision
!= distributed/default-source revision
!= deployed release revision
!= semantic owner-authority version
!= Atlas transport revision
!= downstream publication revision
```

That compression became consequential. Host deployment planning showed that the running release contained two real capabilities absent from distributed `main`; a candidate built only from distributed source was schema-compatible yet would have regressed those deployed capabilities. Conversely, Game, Runtime, SCD, and Media each had clean committed successor lineages that passed their owner-native gates but had never entered their advertised remote `main`. Web added a third case: source integration itself is policy-governed by PR plus required CI and therefore cannot be repaired by a generic direct push.

## Pressure evidence

The audit used exact source fences, owner-native cold-start/test gates, advertised remote refs, deployment receipts where available, and Atlas owner observations.

### Host — deployed source outran distributed source

- observed deployed release: `4d5a04e738d2fbd99fca0ff1af6f8703de0ae8fb`;
- distributed source before repair: `e1fc92188918d4ecfd357f032430123e31b20596`;
- deployed-only work comprised the owner cold-start environment and Runtime-hint carrier-authority repair;
- the first Host 0.5 candidate based only on distributed source was correctly not activated;
- the deployed changes were replayed after the 0.5 cutover, fully revalidated, and distributed without force;
- current distributed Host source after institutional closeout: `50e51bde55e24da5a31ffb3e3a738ead17c123a8`;
- production activation remains intentionally at `4d5a04e...`; this is now an explicit deployment lag, not an unobserved source-distribution drift.

### Runtime — committed successor was not distributed

- advertised `main` before repair: `f7600266c97aa9dd77dfb52873ad0c8f58f2f547`;
- clean committed local successor: `350a3a74fdb44c52e57c2bba04e0bfab86ab3cd0`;
- owner `cold-start` gate passed from a fresh environment;
- exact remote-fenced fast-forward publication succeeded;
- Runtime semantic authority remained `sha256:9c67d1b4094ce85a2465579430bb1a941f1923457087fb74cde0642d7b9a51b3` and Atlas remained `CURRENT_TO_SOURCE`.

### Game — six coherent committed changes were not distributed

- advertised `main` before repair: `5d52be37e3188ad83e1a06e32fb1eb580bbe48ff`;
- clean successor through development-core/player-evidence/environment work: `cb2fa80a34239cd9d5318a47975cda5b6da1b2ed`;
- owner `cold-start` gate passed the complete Game test surface;
- exact remote-fenced fast-forward publication succeeded;
- semantic authority stayed `sha256:b0e16e2cd6fe40685d7b96f94d78ef89bd55ed7f92db4de1408e33d2539bb2f0`; source advancement therefore did not fabricate a new Game Foundation/current authority version.

### SCD — owner-native recovery material existed only locally

- advertised `main` before repair: `ff793dcf1a5c98552094a906abb97d95ef1ac1da`;
- recovery successor: `fc2977cefedd83b7d99054b7260bda21f5e10273`;
- byte-exact recovery manifest/current-pointer and 5 owner recovery tests passed;
- exact remote-fenced fast-forward publication succeeded;
- SCD semantic authority remained `sha256:f98fef8a3389b9234d95dc5f1e3ce8a18f34045e117bd7c2cf267ec5351a07ba`, with Atlas `CURRENT_TO_SOURCE` after transport advancement.

### Media — nine committed Book/Studio/environment changes were not distributed

- advertised GitHub `main` before repair: `b7de468f0637059344055e82835f87a0f671a610`;
- clean successor: `7db6c27c144ec8baf7075ae962c5109262445da0`;
- HTTPS `ls-remote` was unavailable in the audit environment, so the same repository was source-fenced through its SSH transport instead of treating the local tracking ref as remote truth;
- fresh owner cold-start passed 97 Python core tests, TypeScript checks, and preview build;
- exact SSH remote-fenced fast-forward publication succeeded;
- Media semantic authority remained `sha256:e26649a077eacfd0964e0d6ace7a3454d27c60ebcc96251dbb9b1861d867823e`, with Atlas `CURRENT_TO_SOURCE`.

### Web — source integration is itself a governed consequence

- advertised `main`: `f6c6af0d04e6968db0a6018d9751ae3ec4a18d0d`;
- existing owner-environment successor: `467fc3df0a404af4f4a289af6923826874ea03e1`;
- copied no-`.git` cold-start passed; Git diagnostics emitted by caught probes were not failures;
- `doctor-browser` initially failed because it bypassed the already-owned `browser-runtime.mjs` short-temp-path rule, causing Chromium `SingletonSocket path too long` inside the Runtime Workspace path;
- rebinding `doctor-browser` to `configureBrowserTempEnvironment()` made cold-start, browser doctor, full check, and Playwright smoke pass;
- repaired PR head: `8a33dc94056445c4c94c430b8a670d6405d6a39b`;
- direct `main` push was correctly rejected by GitHub branch policy: changes require a pull request and required status check `check`;
- PR #68 was opened rather than weakening or bypassing Web's owner-native source-admission policy; required check `check` passed, and the PR was merged normally as `ed1cf5726c56e8d5dccbceced6cfaad897e5c36f`, preserving `8a33dc9...` as an ancestor of distributed `main`.

## Result

The observed cases support a **relation model**, not a scalar `CurrentRevision`:

```text
WorkingSource(repo, revision)
DistributedSource(repo, remote/ref, revision)
DeployedSource(owner, release identity, revision)
SemanticAuthority(owner, authorityVersionRef)
ProjectionTransport(consumer, owner, transportRevision)
Publication(owner, publication identity, source revision)
```

A transition may legitimately advance one relation without advancing the others. The obligation is to preserve the relation and its source fence, not to force all revisions equal.

### Supported laws

1. **Distributed source is not implementation currentness.** A remote ref may lag a committed or deployed successor.
2. **Deployed bytes are not canonical source by mere liveness.** A live release can contain changes absent from distributed source and must be reconciled before a successor release is admitted.
3. **Source advancement is not semantic-authority advancement.** Runtime, Game, SCD, and Media all advanced transport revisions while retaining the same owner authority version.
4. **Tracking refs are observations, not remote truth.** Consequential publication requires advertised-remote revalidation; Media's stale/blocked HTTPS path could not be silently replaced by `origin/main` cache as evidence.
5. **Publication policy is owner-relative.** Web requires PR + CI; other repositories admitted exact fast-forwards. A cross-owner tool may observe these relations but cannot bypass the owner repository's publication policy.
6. **Successor capability must rebind predecessor verification.** Web already owned short browser temp-path realization; `doctor-browser` still bypassed it. Reusing the successor seam removed the failure without another browser workaround.
7. **Projection currentness is downstream and non-authoritative.** Atlas should observe the owner after source publication; it must not promote every source commit into a semantic authority version.

## Rejected routes

- **Global Source Manager / CurrentRevision registry:** rejected. It would collapse relations with different owners and transition laws.
- **Treat `origin/main` cache as remote authority:** rejected for consequential publication.
- **Treat live deployment as source authority:** rejected by the Host counterexample.
- **Auto-promote owner semantic authority on every Git commit:** rejected by Runtime/Game/SCD/Media observations.
- **One universal push workflow:** rejected by Web branch-policy evidence.
- **Keep duplicate environment workaround in each verifier:** rejected by the Web browser-runtime rebind result.

## Engineering consequence

The preferred pattern is:

```text
owner-native work / deployment evidence
→ exact relation observation
→ owner-native gate
→ owner-native publication/admission policy
→ advertised source re-observation
→ semantic authority changes only if separately admitted
→ downstream projections refresh/compare
```

Cross-owner audits may provide disposable read-only comparison instruments. They do not become publication, deployment, semantic-authority, or source-control owners.

## Reopen conditions

Reopen if one of the following appears:

- repeated source-distribution drift survives owner-native publication gates and causes real consumer/deployment regressions;
- multiple owners independently require the same nontrivial publication transaction/reconciliation machinery beyond ordinary Git/CI and extracting it would reduce error without centralizing policy;
- Atlas or another consumer cannot distinguish source transport advancement from semantic-authority advancement;
- deployment and distributed-source lineages cannot be reconciled without loss of provenance;
- a repository's publication policy cannot be represented as an owner-native admission relation without a new shared primitive.

Absent those pressures, no daemon, central registry, or new owner is admitted.
