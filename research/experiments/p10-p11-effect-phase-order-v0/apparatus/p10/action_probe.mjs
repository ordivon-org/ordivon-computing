import crypto from 'node:crypto';
import { fixture, live, serviceFor, NOW, r2, r3 } from './fixture-lib.mjs';
function makeNewPackage(fx, suffix='new') {
  const request=structuredClone(fx.request); request.requestId=`request:p10:${suffix}`; request.idempotencyKey=`p10:effect:${suffix}`; request.venueOrder.clOrdId=r2.deterministicClientOrderId(request.idempotencyKey);
  const effect={...structuredClone(fx.effect),effectId:`effect:p10:${suffix}`,request};
  const claim={...structuredClone(fx.claim),claimId:`dispatch:p10:${suffix}`,effectRef:`effect://${effect.effectId}`,requestHash:r2.sha256Digest(request),venueOrderHash:r2.sha256Digest(request.venueOrder),clientOrderId:request.venueOrder.clOrdId};
  const gate=structuredClone(fx.gate); const effectDigest=r2.sha256Digest(effect), claimDigest=r2.sha256Digest(claim); const admissionId=`effect_admission_v2_${crypto.createHash('sha256').update(`${effectDigest}:${claimDigest}:${gate.executionBasisDigest}:${gate.executionAssessmentDigest}`).digest('hex').slice(0,32)}`;
  const payload={schemaVersion:1,admissionId,audience:fx.trustPolicy.audience,issuedAt:'2026-08-07T12:59:30Z',validUntil:'2026-08-07T13:15:00Z',effectDigest,dispatchClaimDigest:claimDigest,effect,dispatchClaim:claim,executionBasis:structuredClone(fx.basis),executionGate:gate,extensions:{}};
  const unsigned=r3.unsignedEffectAdmissionV2(Buffer.from(r2.canonicalJson(payload)),{keyId:'effect:p10'}); const signedEffectAdmission={...unsigned,signature:r3.signEffectAdmissionV2(unsigned,fx.effectKeys.privateKey)};
  return {schemaVersion:3,signedGrant:fx.pkg.signedGrant,signedEffectAdmission,extensions:{}};
}
async function setup(name) {
  let env;
  if(name==='new_unchanged') env=serviceFor({instrument:live(),mode:'accepted'});
  else if(name==='new_material_drift') env=serviceFor({instrument:live({state:'suspended'}),mode:'accepted'});
  else if(name==='admitted_response_lost_pre_dispatch') env=serviceFor({instrument:live(),mode:'accepted'});
  else if(name==='post_dispatch_ambiguous') env=serviceFor({instrument:live(),mode:'ambiguous'});
  else if(name==='post_dispatch_unbound') env=serviceFor({instrument:live(),mode:'unbound'});
  else if(name==='post_dispatch_accepted_response_lost') env=serviceFor({instrument:live(),mode:'accepted'});
  else throw new Error(name);
  if(name==='admitted_response_lost_pre_dispatch') { env.ledger.admit(env.fx.pkg,env.fx.trustPolicy,live(),{now:NOW}); env.setInstrument(live({state:'suspended'})); }
  if(name.startsWith('post_dispatch_')) { await env.svc.execute(env.fx.pkg,{now:NOW}); if(name==='post_dispatch_unbound') env.setInstrument(live({tickSz:'0.10'})); }
  return env;
}
async function one(name, action){
  const env=await setup(name); const before=env.counts(); let result=null, error=null;
  try {
    if(action==='EXECUTE_EXACT_EFFECT') result=await env.svc.execute(env.fx.pkg,{now:NOW});
    else if(action==='RECONCILE_EXACT_EFFECT') result=env.reconcile();
    else if(action==='FORM_NEW_EFFECT') result=await env.svc.execute(makeNewPackage(env.fx,`new-${name}`),{now:NOW});
    else if(action==='HOLD') result={held:true}; else throw new Error(action);
  } catch(e) { error={name:e.name,code:e.code??null,message:e.message,externalFinancialWriteAttempted:e.externalFinancialWriteAttempted??false}; }
  const after=env.counts(); const out={scenario:name,action,before,after,delta:{posts:after.posts-before.posts,reads:after.reads-before.reads,reconciles:after.reconciles-before.reconciles},duplicateEconomicWrite:before.posts>=1 && after.posts>before.posts,resultCode:result?.code??null,result,error}; env.close(); return out;
}
const scenarios=['new_unchanged','new_material_drift','admitted_response_lost_pre_dispatch','post_dispatch_ambiguous','post_dispatch_unbound','post_dispatch_accepted_response_lost']; const actions=['EXECUTE_EXACT_EFFECT','RECONCILE_EXACT_EFFECT','FORM_NEW_EFFECT','HOLD']; const rows=[];
for(const s of scenarios) for(const a of actions) rows.push(await one(s,a));
const oracle={new_unchanged:'EXECUTE_EXACT_EFFECT',new_material_drift:'HOLD',admitted_response_lost_pre_dispatch:'EXECUTE_EXACT_EFFECT',post_dispatch_ambiguous:'RECONCILE_EXACT_EFFECT',post_dispatch_unbound:'RECONCILE_EXACT_EFFECT',post_dispatch_accepted_response_lost:'RECONCILE_EXACT_EFFECT'};
console.log(JSON.stringify({schemaVersion:1,kind:'ordivon.computing.p10-finance-physical-consequence-matrix',financeRevision:'999672a068e1de16b59516cd1079f7d504e81a47',oracle,rows},null,2));
