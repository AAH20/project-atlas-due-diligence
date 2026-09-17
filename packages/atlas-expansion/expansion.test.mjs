import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync,mkdtempSync,cpSync,writeFileSync,rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { defaultRoot,validate } from './validate.mjs';
import { read,retrieve,timelineSummary,redactKnownFixtures,scoreCases } from './reference.mjs';
test('independent artifact/accounting validator passes',()=>assert.equal(validate().status,'PASS'));
test('negative contribution has no positive payback proxy',()=>{
  const low=read(defaultRoot,'financial_facts').find(x=>x.id==='ECON-low_utilization');assert(low.contribution_margin_cents<0);assert.equal(low.payback_days_proxy,null);
});
test('tampered financial journal is rejected',()=>{
  const dir=mkdtempSync(resolve(tmpdir(),'atlas-v02-'));
  try{cpSync(defaultRoot,dir,{recursive:true});const journal=read(dir,'journal');journal[0].signed_cents++;
    writeFileSync(resolve(dir,'data/journal.json'),JSON.stringify(journal));
    // Update checksums too: reject accounting corruption independently of integrity hashes.
    const manifest=JSON.parse(readFileSync(resolve(dir,'manifest.json')));
    const item=manifest.find(x=>x.path==='data/journal.json');const bytes=readFileSync(resolve(dir,item.path));
    item.sha256=createHash('sha256').update(bytes).digest('hex');item.bytes=bytes.length;
    writeFileSync(resolve(dir,'manifest.json'),JSON.stringify(manifest));
    writeFileSync(resolve(dir,'SHA256SUMS'),manifest.map(x=>`${x.sha256}  ${x.path}`).join('\n')+'\n');
    assert.throws(()=>validate(dir));
  }finally{rmSync(dir,{recursive:true,force:true});}
});
test('all five stages have correct independent expected outcomes',()=>{
  const expected=[[0,0,false],[92,0,true],[92,10000000,true],[92,10000000,false],[92,0,false]];
  for(let i=0;i<5;i++){const x=timelineSummary(defaultRoot,'buyer',`T${i}`);assert.deepEqual([x.deployment_delay_days,x.funding_gap_usd,x.offtake_threshold_exceeded],expected[i]);}
});
test('future evidence cannot be retrieved early',()=>assert.throws(()=>retrieve(defaultRoot,'buyer','T0','TIMELINE-v5')));
test('restricted terms cannot be retrieved by buyer',()=>assert.throws(()=>retrieve(defaultRoot,'buyer','T4','PREP-RESTRICTED-v1')));
test('engineering gets insufficient evidence for restricted financial timeline',()=>assert.equal(timelineSummary(defaultRoot,'engineering','T4').status,'insufficient_evidence'));
test('invalid role and stage fail closed',()=>{assert.throws(()=>retrieve(defaultRoot,'owner','T0','TIMELINE-v1'));assert.throws(()=>retrieve(defaultRoot,'buyer','T9','TIMELINE-v1'));});
test('known-fixture redaction preserves numerical evidence',()=>{
  const task=read(defaultRoot,'preparation_tasks');const original=retrieve(defaultRoot,'administrator','T0','PREP-PII-v1');
  const result=redactKnownFixtures(original,task.redact);for(const t of task.redact)assert(!result.includes(t));for(const t of task.preserve)assert(result.includes(t));
});
test('empty predictions do not score perfect accuracy',()=>{
  const a=JSON.parse(readFileSync(resolve(defaultRoot,'worked_answers/cases.json')));const s=scoreCases([],a,read(defaultRoot,'evidence_passages'));assert.equal(s.status_accuracy,0);assert.equal(s.material_recall,0);assert.equal(s.citation_id_validity,null);
});
test('scorer penalizes false alarms and fabricated citations',()=>{
  const a=JSON.parse(readFileSync(resolve(defaultRoot,'worked_answers/cases.json')));const clean=a.find(x=>x.status==='clean');
  const s=scoreCases([{case_id:clean.case_id,status:'material',evidence_ids:['invented']}],a,read(defaultRoot,'evidence_passages'));assert.equal(s.false_material_flags,1);assert.equal(s.citation_id_validity,0);assert.equal(s.required_evidence_coverage,0);
});
test('duplicate case predictions are rejected',()=>{
  const a=JSON.parse(readFileSync(resolve(defaultRoot,'worked_answers/cases.json')));const p={case_id:a[0].case_id,status:'material',evidence_ids:[]};assert.throws(()=>scoreCases([p,p],a,read(defaultRoot,'evidence_passages')));
});
