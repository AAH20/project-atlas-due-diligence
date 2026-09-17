import { readFileSync,readdirSync } from 'node:fs';
import { resolve,dirname,relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
const repo=resolve(dirname(fileURLToPath(import.meta.url)),'../..');
export const defaultRoot=resolve(repo,'datasets/project-atlas/v0.2');
export function validate(root=defaultRoot) {
  const load=name=>JSON.parse(readFileSync(resolve(root,`data/${name}.json`),'utf8'));
  const manifest=JSON.parse(readFileSync(resolve(root,'manifest.json'),'utf8'));
  const paths=new Set();
  for(const item of manifest) {
    assert(!paths.has(item.path));paths.add(item.path);
    assert(!item.path.includes('..')&&!item.path.startsWith('/'));
    const bytes=readFileSync(resolve(root,item.path));
    assert.equal(bytes.length,item.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),item.sha256);
    assert(!item.path.includes('organizer'));
  }
  function files(dir) {return readdirSync(dir,{withFileTypes:true}).flatMap(x=>x.isDirectory()?files(resolve(dir,x.name)):[relative(root,resolve(dir,x.name))]);}
  assert.deepEqual(files(root).filter(p=>!['manifest.json','SHA256SUMS'].includes(p)).sort(),[...paths].sort());
  assert.equal(readFileSync(resolve(root,'SHA256SUMS'),'utf8'),manifest.map(x=>`${x.sha256}  ${x.path}`).join('\n')+'\n');
  const entities=load('entities'),ids=new Set(entities.map(e=>e.id));assert.equal(ids.size,3);
  const assets=load('assets');for(const a of assets)assert(ids.has(a.entity_id));
  const nodes=new Set([...ids,...assets.map(a=>a.id)]);
  for(const r of load('relationships'))assert(nodes.has(r.from)&&nodes.has(r.to));
  const journal=load('journal'),groups=new Map();
  for(const row of journal) {
    assert(ids.has(row.entity_id));assert(Number.isSafeInteger(row.signed_cents));
    if(!groups.has(row.journal_id))groups.set(row.journal_id,[]);groups.get(row.journal_id).push(row);
  }
  for(const rows of groups.values()) {assert.equal(rows.length,2);assert.equal(rows[0].entity_id,rows[1].entity_id);assert.equal(rows[0].period,rows[1].period);assert.equal(rows.reduce((s,r)=>s+r.signed_cents,0),0);}
  const finance=load('monthly_finance');assert.equal(finance.length,72);
  for(const opening of load('opening_balances')) {
    const balances={...opening.accounts};assert.equal(Object.values(balances).reduce((a,b)=>a+b,0),0);
    const months=finance.filter(x=>x.entity_id===opening.entity_id);assert.equal(months.length,24);
    for(const s of months) {
      const rows=journal.filter(r=>r.entity_id===s.entity_id&&r.period===s.period);
      for(const row of rows)balances[row.account]=(balances[row.account]||0)+row.signed_cents;
      assert.equal(Object.values(balances).reduce((a,b)=>a+b,0),0);
      assert.equal(s.revenue_cents,rows.filter(r=>r.kind==='invoice'&&r.account==='ar').reduce((a,r)=>a+r.signed_cents,0));
      for(const [column,account] of [['cogs_cents','cogs'],['payroll_cents','payroll'],['interest_cents','interest'],['depreciation_cents','depreciation']])assert.equal(s[column],rows.filter(r=>r.account===account&&r.kind!=='close_expense').reduce((a,r)=>a+r.signed_cents,0));
      assert.equal(s.net_income_cents,s.revenue_cents-s.cogs_cents-s.payroll_cents-s.interest_cents-s.depreciation_cents);
      assert.equal(s.cash_cents,balances.cash);assert.equal(s.ar_cents,balances.ar);
      assert.equal(s.ppe_net_cents,balances.ppe+balances.accumulated_depreciation);
      assert.equal(s.debt_cents,-balances.debt);assert.equal(s.equity_cents,-balances.equity);assert.equal(s.retained_earnings_cents,-balances.retained_earnings);
      assert.equal(s.cash_cents+s.ar_cents+s.ppe_net_cents,s.debt_cents+s.equity_cents+s.retained_earnings_cents);
    }
  }
  const documents=load('documents_and_versions'),docmap=new Map(documents.map(d=>[d.id,d]));assert.equal(docmap.size,documents.length);
  const economics=load('compute_economics_assumptions');
  for(const s of load('financial_facts')) {
    const revenue=Math.round(economics.gpu_units*economics.hours_per_month*economics.price_per_gpu_hour_cents*s.utilization_basis_points/10000);
    const power=Math.round(economics.gpu_units*economics.hours_per_month*economics.power_kw_per_gpu*economics.pue_basis_points/10000*s.power_price_per_kwh_cents);
    assert.equal(s.revenue_cents,revenue);assert.equal(s.power_cents,power);assert.equal(s.cogs_cents,power+economics.monthly_gpu_cost_cents);
    assert.equal(s.contribution_margin_cents,revenue-s.cogs_cents-s.support_cents);
    assert.equal(s.payback_days_proxy,s.contribution_margin_cents>0?Math.ceil(economics.customer_acquisition_cost_cents/(s.contribution_margin_cents/30)):null);
  }
  const evidence=load('evidence_passages'),emap=new Map(evidence.map(e=>[e.id,e]));assert.equal(emap.size,evidence.length);
  const stages=['T0','T1','T2','T3','T4'];
  for(const d of documents) {
    assert(paths.has(d.path));assert.equal(manifest.find(m=>m.path===d.path).sha256,d.sha256);assert(stages.includes(d.stage));
    assert(d.roles.length&&d.roles.every(r=>['buyer','lender','engineering','administrator'].includes(r)));
    if(d.supersedes){const old=docmap.get(d.supersedes);assert(old&&d.version===old.version+1&&stages.indexOf(d.stage)>stages.indexOf(old.stage));}
  }
  for(const e of evidence) {
    const d=docmap.get(e.document_id);assert(d);
    const lines=readFileSync(resolve(root,d.path),'utf8').split('\n');
    assert.equal(lines.slice(e.line_start-1,e.line_end).join('\n'),e.quote);
  }
  const cases=load('cases');assert.equal(cases.length,36);assert.equal(new Set(cases.map(c=>c.id)).size,36);
  for(const c of cases)for(const id of c.document_ids)assert(docmap.has(id));
  const answers=JSON.parse(readFileSync(resolve(root,'worked_answers/cases.json'),'utf8'));
  assert.equal(answers.length,36);
  for(const a of answers){assert(cases.some(c=>c.id===a.case_id));for(const e of a.required_evidence_ids)assert(emap.has(e));}
  for(const f of load('findings')){assert(cases.some(c=>c.id===f.case_id));for(const e of f.evidence_ids)assert(emap.has(e));for(const id of f.affected_entity_ids)assert(ids.has(id));}
  for(const o of load('obligations_and_milestones'))assert(ids.has(o.entity_id));
  for(const r of load('review_decisions'))assert(load('findings').some(f=>f.id===r.finding_id));
  for(const event of load('change_events')) {assert(docmap.has(event.document_id)&&emap.has(event.evidence_id));assert(Number.isSafeInteger(event.available_funding_usd)&&Number.isSafeInteger(event.committed_capex_usd));}
  return {status:'PASS',files:manifest.length,cases:cases.length,documents:documents.length,journal_lines:journal.length,monthly_statements:finance.length,checks:['checksums','journal_pairing','per_entity_accounts','income_and_balance_sheets','graph_references','evidence_locators','version_chain','case_and_finding_references']};
}
if(process.argv[1]===fileURLToPath(import.meta.url))console.log(JSON.stringify(validate(process.argv[2]?resolve(process.argv[2]):defaultRoot),null,2));
