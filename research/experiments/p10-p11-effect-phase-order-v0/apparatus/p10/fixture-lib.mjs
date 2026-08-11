import crypto from 'node:crypto';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
const F='/var/lib/ordivon/runtime/workspaces/finance-p10-ambiguous-effect-20260811';
const r2=await import(pathToFileURL(`${F}/executor/remote-admission-v2.mjs`));
const r3=await import(pathToFileURL(`${F}/executor/remote-admission-v3.mjs`));
const {RemoteEvidenceStore}=await import(pathToFileURL(`${F}/executor/evidence-store.mjs`));
const {ExternalExecutorServiceV3}=await import(pathToFileURL(`${F}/executor/service-v3.mjs`));
const NOW=new Date('2026-08-07T13:00:00Z'); const h=(c)=>`sha256:${c.repeat(64)}`;
function fixture({suffix='1'}={}){
  const authorityKeys=crypto.generateKeyPairSync('ed25519'), effectKeys=crypto.generateKeyPairSync('ed25519');
  const constitution={schemaVersion:0,constitutionId:'constitution:p10',ownerId:'owner:test',capitalScope:{portfolioRefs:['portfolio://portfolio:test']},objective:{kind:'compound-owner-real-capital',description:'p10',continuationPrinciple:'preserve-ability-to-continue-operating',reliabilityPrinciple:'reality-grounded-and-causally-attributable'},primaryAgentDelegation:{actorId:'finance-primary-agent',role:'primary-capital-manager',authorityMode:'native-within-capital-scope',autonomousDomains:['observe','research','portfolio.allocate','trade.execute','delegate.operational']},ownerReservedPowers:['constitution.revise','beneficial-owner.change','capital-scope.expand','capital.transfer-out-of-scope'],changePolicy:{primaryAgentMayReviseConstitution:false,ownerRootRequiredForRevision:true},createdAt:'2026-08-01T00:00:00Z',extensions:{}};
  const authority={mode:'owner-native',authorityRef:`owner-constitution://${constitution.constitutionId}`,ownerConstitution:constitution,authorityLease:null};
  const grantPayload={schemaVersion:0,grantId:'grant:p10',audience:'ordivon-finance-executor:p10',issuedAt:'2026-08-07T12:30:00Z',validUntil:'2026-08-07T13:30:00Z',authority,allowedAdapterCapabilities:['okx.tradfi.swap.order.place@1'],extensions:{}};
  const ug=r2.unsignedGrantV2(Buffer.from(r2.canonicalJson(grantPayload)),{keyId:'authority:p10'}); const signedGrant={...ug,signature:r2.signGrantV2(ug,authorityKeys.privateKey)};
  const trustPolicy={schemaVersion:1,policyId:'trust:p10',audience:grantPayload.audience,disabled:false,trustedSigners:[{keyId:'authority:p10',algorithm:'Ed25519',enabled:true,publicKeyPem:authorityKeys.publicKey.export({type:'spki',format:'pem'}).toString(),purposes:['authority-grant.owner-native','authority-grant.delegated-lease','grant-revocation']},{keyId:'effect:p10',algorithm:'Ed25519',enabled:true,publicKeyPem:effectKeys.publicKey.export({type:'spki',format:'pem'}).toString(),purposes:['effect-admission']}],extensions:{}};
  const key=`p10:effect:${suffix}`, inst='SPY-USDT-SWAP';
  const basis={schemaVersion:1,basisId:`basis:p10:${suffix}`,venueRef:'venue://okx/live-primary',instrumentRef:inst,observedAt:'2026-08-07T12:58:30Z',instrumentState:'live',contractModel:'linear-base-value',ctVal:'0.01',ctValCcy:'SPY',quoteCurrency:'USD',lotSz:'1',minSz:'1',tickSz:'0.01',venueWorld:{institutionEvidenceRef:`evidence://${h('a')}`,snapshotEvidenceRef:`evidence://${h('b')}`,snapshotId:`venue-world-snapshot://${h('c')}`,accountRef:'okx-account://test',tradeMode:'cross'},evidenceRefs:[`evidence://${h('a')}`,`evidence://${h('b')}`],extensions:{}};
  const request={schemaVersion:2,requestId:`request:p10:${suffix}`,proposalRef:'proposal://proposal:p10',proposalIntentDigest:h('1'),authorityRef:authority.authorityRef,actorId:'finance-primary-agent',portfolioRef:'portfolio:test',venueRef:basis.venueRef,instrumentRef:inst,executionBasisRef:`execution-market-basis://${basis.basisId}`,riskEffect:'increase',operation:'order.place',adapterCapability:'okx.tradfi.swap.order.place@1',venueOrder:{instId:inst,tdMode:'cross',side:'buy',posSide:'net',ordType:'limit',sz:'10',px:'500.00',reduceOnly:false,clOrdId:r2.deterministicClientOrderId(key)},createdAt:'2026-08-07T12:50:00Z',expiresAt:'2026-08-07T13:20:00Z',idempotencyKey:key,extensions:{}};
  const effect={effectId:`effect:p10:${suffix}`,capabilityId:'execution.commit',capabilityVersion:5,proposalRef:request.proposalRef,status:'reserved',request};
  const claim={schemaVersion:1,claimId:`dispatch:p10:${suffix}`,effectRef:`effect://${effect.effectId}`,claimedAt:'2026-08-07T12:59:00Z',executorId:'executor:p10',requestHash:r2.sha256Digest(request),venueOrderHash:r2.sha256Digest(request.venueOrder),clientOrderId:request.venueOrder.clOrdId,rule:'exactly-one-network-dispatch-claim; ambiguity requires reconciliation',executionBasisRef:request.executionBasisRef,executionCapabilityVersion:4,effectCapabilityVersion:5,venueWorldSnapshotId:basis.venueWorld.snapshotId,venueWorldSnapshotEvidenceRef:basis.venueWorld.snapshotEvidenceRef,executionAssessmentDigest:h('d')};
  const gate={executionCapabilityVersion:4,effectCapabilityVersion:5,executionBasisRef:request.executionBasisRef,executionBasisDigest:r2.sha256Digest(basis),venueWorldSnapshotId:claim.venueWorldSnapshotId,venueWorldSnapshotEvidenceRef:claim.venueWorldSnapshotEvidenceRef,executionAssessmentDigest:claim.executionAssessmentDigest};
  const effectDigest=r2.sha256Digest(effect), claimDigest=r2.sha256Digest(claim); const admissionId=`effect_admission_v2_${crypto.createHash('sha256').update(`${effectDigest}:${claimDigest}:${gate.executionBasisDigest}:${gate.executionAssessmentDigest}`).digest('hex').slice(0,32)}`;
  const payload={schemaVersion:1,admissionId,audience:grantPayload.audience,issuedAt:'2026-08-07T12:59:30Z',validUntil:'2026-08-07T13:15:00Z',effectDigest,dispatchClaimDigest:claimDigest,effect,dispatchClaim:claim,executionBasis:basis,executionGate:gate,extensions:{}};
  const ue=r3.unsignedEffectAdmissionV2(Buffer.from(r2.canonicalJson(payload)),{keyId:'effect:p10'}); const signedEffectAdmission={...ue,signature:r3.signEffectAdmissionV2(ue,effectKeys.privateKey)};
  return {authorityKeys,effectKeys,trustPolicy,basis,request,effect,claim,gate,payload,pkg:{schemaVersion:3,signedGrant,signedEffectAdmission,extensions:{}}};
}
const live=(over={})=>({instId:'SPY-USDT-SWAP',state:'live',contractModel:'linear-base-value',ctVal:'0.01',quoteCurrency:'USD',lotSz:'1',minSz:'1',tickSz:'0.01',...over});
function serviceFor({instrument=live(),mode='accepted'}){
 const root=mkdtempSync(join(tmpdir(),'p10-owner-probe-')); const ledger=new r3.RemoteAdmissionLedgerV3(join(root,'ledger.sqlite3')); const store=new RemoteEvidenceStore(join(root,'evidence')); let posts=0,reads=0,reconciles=0,currentInstrument=instrument;
 const okx={async publicInstrument(){reads++; return currentInstrument;},async placeOrderOnce(order){posts++; if(mode==='ambiguous') throw Object.assign(new Error('socket reset after write'),{code:'ECONNRESET'}); if(mode==='unbound') return {rawBody:Buffer.from(JSON.stringify({code:'0',data:[{clOrdId:'different',sCode:'0',ordId:'other'}]})),httpStatus:200,contentType:'application/json',date:null,requestPath:'/api/v5/trade/order'}; if(mode==='rejected') return {rawBody:Buffer.from(JSON.stringify({code:'0',data:[{clOrdId:order.clOrdId,sCode:'51008',sMsg:'insufficient balance',ordId:''}]})),httpStatus:200,contentType:'application/json',date:null,requestPath:'/api/v5/trade/order'}; return {rawBody:Buffer.from(JSON.stringify({code:'0',data:[{clOrdId:order.clOrdId,sCode:'0',ordId:'ord-p10'}]})),httpStatus:200,contentType:'application/json',date:null,requestPath:'/api/v5/trade/order'};}};
 const fx=fixture(); const svc=new ExternalExecutorServiceV3({trustPolicy:fx.trustPolicy,ledger,okx,evidenceStore:store,executorInstanceId:'executor:p10'}); return {fx,svc,ledger,store,counts:()=>({posts,reads,reconciles}),setInstrument:(x)=>{currentInstrument=x;},reconcile:()=>{reconciles++; return {clientOrderId:fx.request.venueOrder.clOrdId,found:'unknown'};},close:()=>{ledger.close();rmSync(root,{recursive:true,force:true});}};
}
const actions=['EXECUTE_EXACT_EFFECT','RECONCILE_EXACT_EFFECT','FORM_NEW_EFFECT','HOLD'];
async function scenario(name){
 let env;
 if(name==='new_unchanged') env=serviceFor({instrument:live(),mode:'accepted'});
 else if(name==='new_material_drift') env=serviceFor({instrument:live({state:'suspended'}),mode:'accepted'});
 else if(name==='admitted_response_lost_pre_dispatch') env=serviceFor({instrument:live(),mode:'accepted'});
 else if(name==='post_dispatch_ambiguous') env=serviceFor({instrument:live(),mode:'ambiguous'});
 else if(name==='post_dispatch_unbound') env=serviceFor({instrument:live(),mode:'unbound'});
 else if(name==='post_dispatch_accepted_response_lost') env=serviceFor({instrument:live(),mode:'accepted'});
 else throw new Error(name);
 const {fx,svc,ledger}=env; let setup=null;
 if(name==='admitted_response_lost_pre_dispatch') { setup=ledger.admit(fx.pkg,fx.trustPolicy,live(),{now:NOW}); env.setInstrument(live({state:'suspended'})); }
 if(name.startsWith('post_dispatch_')) { setup=await svc.execute(fx.pkg,{now:NOW}); if(name==='post_dispatch_unbound') env.setInstrument(live({tickSz:'0.10'})); else env.setInstrument(live()); }
 const before=env.counts(); const admission=ledger.replayAdmission(fx.pkg); const dispatch=admission?ledger.dispatchState(admission.admissionId):null;
 const current=await (async()=>{try{return env.svc.okx.publicInstrument(fx.request.instrumentRef)}catch{return null}})(); // explicit probe for battlefield; increments read once
 const afterProbe=env.counts();
 const planningBasis={instrumentState:fx.basis.instrumentState,contractModel:fx.basis.contractModel,ctVal:fx.basis.ctVal,quoteCurrency:fx.basis.quoteCurrency,lotSz:fx.basis.lotSz,minSz:fx.basis.minSz,tickSz:fx.basis.tickSz};
 const currentBasis=current?{instrumentState:current.state,contractModel:current.contractModel,ctVal:current.ctVal,quoteCurrency:current.quoteCurrency,lotSz:current.lotSz,minSz:current.minSz,tickSz:current.tickSz}:null;
 const comparison=currentBasis?Object.fromEntries(Object.keys(planningBasis).map(k=>[k,{before:planningBasis[k],after:currentBasis[k],equal:planningBasis[k]===currentBasis[k]}])):null;
 const phase=!admission?'new_pre_admission':(!dispatch?'admitted_pre_dispatch':`post_dispatch_${dispatch.outcome??'claimed'}`);
 env.close(); return {name,phase,setupCode:setup?.code??null,planning:{effectId:fx.effect.effectId,idempotencyKey:fx.request.idempotencyKey,clientOrderId:fx.request.venueOrder.clOrdId,packageDigest:r2.sha256Digest(fx.pkg),planningBasis},currentInstrument:currentBasis,basisComparison:comparison,ownerReplay:{admissionExists:!!admission,admissionId:admission?.admissionId??null,dispatchPermissionConsumed:!!dispatch,dispatchOutcome:dispatch?.outcome??null,rawEvidenceDigest:dispatch?.rawEvidenceDigest??null},setupCounts:before,probeCounts:afterProbe};
}

export { fixture, live, serviceFor, scenario, actions, NOW, r2, r3 };
