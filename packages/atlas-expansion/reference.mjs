import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
export const read = (root,name) => JSON.parse(readFileSync(resolve(root,`data/${name}.json`),'utf8'));
const stages=['T0','T1','T2','T3','T4'];
export function visibleDocuments(root,role,stage) {
  if(!['buyer','lender','engineering','administrator'].includes(role)||!stages.includes(stage))throw new Error('Invalid role or stage');
  return read(root,'documents_and_versions').filter(d=>d.roles.includes(role)&&stages.indexOf(d.stage)<=stages.indexOf(stage));
}
export function retrieve(root,role,stage,documentId) {
  const document=visibleDocuments(root,role,stage).find(d=>d.id===documentId);
  if(!document)throw new Error('Evidence unavailable in this role/stage');
  return readFileSync(resolve(root,document.path),'utf8');
}
export function timelineSummary(root,role,stage) {
  const ids=new Set(visibleDocuments(root,role,stage).map(d=>d.id));
  const events=read(root,'change_events').filter(e=>ids.has(e.document_id));
  const latest=events.at(-1);
  if(!latest)return {status:'insufficient_evidence',stage};
  return {status:'requires_review',stage,document_id:latest.document_id,evidence_id:latest.evidence_id,
    deployment_delay_days:Math.round((Date.parse(latest.energization)-Date.parse('2027-03-01'))/86400000),
    funding_gap_usd:Math.max(0,latest.committed_capex_usd-latest.available_funding_usd),
    offtake_threshold_exceeded:latest.energization>latest.termination_threshold};
}
export function redactKnownFixtures(text,terms) {
  for(const term of terms)text=text.split(term).join('[REDACTED]');
  return text;
}
export function scoreCases(predictions,answers,evidence) {
  if(!Array.isArray(predictions))throw new Error('Predictions must be an array');
  const oracle=new Map(answers.map(a=>[a.case_id,a]));
  const sources=new Map(evidence.map(e=>[e.id,e]));
  const seen=new Set();let correct=0,tp=0,fp=0,cited=0,validCitations=0,sufficient=0;
  for(const p of predictions) {
    if(!p||!oracle.has(p.case_id)||seen.has(p.case_id)||!['material','clean','insufficient_evidence'].includes(p.status)||!Array.isArray(p.evidence_ids))throw new Error('Invalid, duplicate or unknown prediction');
    if(Object.keys(p).some(k=>!['case_id','status','evidence_ids','explanation','calculation','review_request'].includes(k))||p.evidence_ids.some(e=>typeof e!=='string')||new Set(p.evidence_ids).size!==p.evidence_ids.length||['explanation','review_request'].some(k=>k in p&&typeof p[k]!=='string')||('calculation' in p&&(!p.calculation||typeof p.calculation!=='object'||Array.isArray(p.calculation))))throw new Error('Prediction violates the documented schema');
    seen.add(p.case_id);const a=oracle.get(p.case_id);
    correct+=Number(p.status===a.status);
    tp+=Number(p.status==='material'&&a.status==='material');
    fp+=Number(p.status==='material'&&a.status!=='material');
    const unique=new Set(p.evidence_ids);
    cited+=unique.size;validCitations+=[...unique].filter(e=>sources.has(e)).length;
    sufficient+=Number(a.required_evidence_ids.every(id=>unique.has(id)));
  }
  const materialCount=answers.filter(a=>a.status==='material').length;
  return {submitted:seen.size,expected:answers.length,coverage:seen.size/answers.length,status_accuracy:correct/answers.length,
    material_recall:materialCount?tp/materialCount:null,false_material_flags:fp,
    citation_id_validity:cited?validCitations/cited:null,required_evidence_coverage:sufficient/answers.length,
    limitations:'ID validity and required-evidence coverage do not establish entailment, severity calibration or expert correctness. Missing predictions count against accuracy/recall. Reviewer time and cost need separate measured logs.'};
}
