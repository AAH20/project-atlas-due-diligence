"""Deterministic synthetic teaching pack. Standard library only; no network or LLM."""
from pathlib import Path
import csv, hashlib, json, zipfile
BASE = Path(__file__).resolve().parents[2]
OUT = BASE / 'datasets/project-atlas/v0.1'
manifest = []
def write(path, text):
    p = OUT / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')
def js(path, obj): write(path, json.dumps(obj, indent=2, sort_keys=True)+'\n')
def table(path, rows):
    p=OUT/path; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def doc(folder, ident, title, body, version=1, stage='T0', date='2026-08-31', entity='ENT-01', authoritative=True):
    path=f'vdr/{folder}/{ident}-v{version}.md'
    header=f'# {title}\n\nSYNTHETIC TEACHING DOCUMENT — NO REAL DEAL OR ASSESSMENT\n\nDocument: {ident}; version: {version}; entity: {entity}; stage: {stage}\nEffective: {date}; observed: {date}T12:00:00Z; currency: USD; timezone: UTC\n\n'
    write(path,header+body+'\n')
    manifest.append(dict(document_id=ident,version=version,path=path,entity_id=entity,stage=stage,effective_at=date,observed_at=date+'T12:00:00Z',classification='synthetic-public-teaching',authoritative=authoritative,sha256=hashlib.sha256((OUT/path).read_bytes()).hexdigest(),locators=[dict(line=i,text=t) for i,t in enumerate((header+body+'\n').splitlines(),1) if t]))
    return path
folders=['00_index','01_corporate','02_finance','03_commercial','04_ai_data_ip','05_infrastructure','06_security','07_privacy','08_legal','09_people','10_tax','11_environment','12_deal','13_postclose']
for f in folders: (OUT/'vdr'/f).mkdir(parents=True,exist_ok=True)
entities=[dict(entity_id=f'ENT-{i:02}',name=f'Atlas Synthetic Entity {i}',parent_id='' if i==1 else 'ENT-01',jurisdiction_assumption=['US','US','UK','IE','SG','US'][i-1],operating_status='holding' if i==1 else 'operating') for i in range(1,7)]
table('data/entities.csv',entities)
# All amounts integer cents. TTM recurring run-rate 180m; services 22m.
mr=[300_000_000]+[1_200_000_000//499+(i<1_200_000_000%499) for i in range(499)]
customers=[dict(customer_id=f'CUS-{i+1:04}',entity_id=f'ENT-{2+i%5:02}',name=f'Synthetic Customer {i+1:04}',product=['inference','reserved_gpu','dataset_pipeline'][i%3],mrr_cents=m,contract_id=f'CTR-{i+1:04}',change_control_consent=i==0) for i,m in enumerate(mr)]
table('data/customers.csv',customers)
contracts=[dict(contract_id=c['contract_id'],customer_id=c['customer_id'],monthly_cents=c['mrr_cents'],currency='USD',start_date='2023-09-01',renewal_date='2026-09-01',consent_required=c['change_control_consent'],service_obligation='monthly deliverable synthetic service; no prepayment',transfer_status='request consent' if c['change_control_consent'] else 'permitted under scenario assumptions') for c in customers]
table('data/contracts.csv',contracts)
assets=[dict(asset_id=f'GPU-{i+1:05}',entity_id=f'ENT-{2+i%5:02}',region=f'REG-{1+i%3}',site_id=f'COLO-{1+i%2}',ownership='owned' if i<3072 else 'leased',vendor_id='VEN-01' if i<3072 else 'VEN-02',lease_id='' if i<3072 else 'LEASE-01',book_value_cents=120_000_000_00//3072 if i<3072 else 0) for i in range(4096)]
# Residual allocation keeps opening gross PPE exact.
for i in range(120_000_000_00%3072): assets[i]['book_value_cents']+=1
table('data/assets.csv',assets)
table('data/employees.csv',[dict(employee_id=f'EMP-{i+1:04}',entity_id=f'ENT-{2+i%5:02}',role=['engineering','operations','commercial','support'][i%4],monthly_salary_cents=20_000_000_0//1200+(i<20_000_000_0%1200)) for i in range(1200)])
ledger=[]; invoices=[]; cash=[]; allocations=[]; summaries=[]
balances={'cash':10_000_000_000,'ppe':12_000_000_000,'debt':-8_000_000_000,'equity':-14_000_000_000,'ar':0,'accum_depreciation':0,'revenue':0,'cogs':0,'payroll':0,'depreciation':0}
opening=balances.copy(); js('data/opening_balances.json',opening)
def post(period, ref, debit, credit, cents):
    jid=f'JRN-{len(ledger)//2+1:06}'
    for account,amount in [(debit,cents),(credit,-cents)]:
        ledger.append(dict(journal_id=jid,period=period,reference=ref,account=account,signed_cents=amount)); balances[account]+=amount
for month in range(36):
    yr=2023+(month+8)//12; mo=(month+8)%12+1; period=f'{yr}-{mo:02}'
    factor=60+month if month<24 else 100 # deliberate flat TTM; not a forecast or market model
    rev=expense=0
    for i,c in enumerate(customers):
        amount=c['mrr_cents']*factor//100; invoice=f'INV-{month+1:02}-{i+1:04}'
        invoices.append(dict(invoice_id=invoice,period=period,customer_id=c['customer_id'],contract_id=c['contract_id'],kind='recurring',amount_cents=amount,recognized_cents=amount,collected_cents=amount if month<35 else 0))
        post(period,invoice,'ar','revenue',amount); rev+=amount
        if month<35:
            post(period,invoice,'cash','ar',amount);cash.append(dict(receipt_id=f'RCT-{month+1:02}-{i+1:04}',invoice_id=invoice,period=period,amount_cents=amount))
        cost=amount*110//100 if i==0 else amount*60//100
        # Every allocated cent accounted for; support is included, not double counted.
        gpu=cost*70//100; power=cost*10//100; support=cost*15//100; retries=cost-gpu-power-support
        allocations.append(dict(period=period,customer_id=c['customer_id'],gpu_cents=gpu,power_cents=power,support_cents=support,retry_cents=retries,total_cents=cost))
        post(period,f'COST-{invoice}','cogs','cash',cost);expense+=cost
    svc=2_200_000_000//12+(mo<=2_200_000_000%12);svc=svc*factor//100
    inv=f'INV-{month+1:02}-SVC'; invoices.append(dict(invoice_id=inv,period=period,customer_id='CUS-0002',contract_id='SOW-01',kind='one_time_services',amount_cents=svc,recognized_cents=svc,collected_cents=svc if month<35 else 0))
    post(period,inv,'ar','revenue',svc);rev+=svc
    if month<35: post(period,inv,'cash','ar',svc);cash.append(dict(receipt_id=f'RCT-{month+1:02}-SVC',invoice_id=inv,period=period,amount_cents=svc))
    post(period,f'SVC-COST-{period}','cogs','cash',svc//2);expense+=svc//2
    post(period,f'PAY-{period}','payroll','cash',200_000_000)
    post(period,f'DEP-{period}','depreciation','accum_depreciation',100_000_000)
    summary=dict(period=period,revenue_cents=rev,cogs_cents=expense,payroll_cents=200_000_000,depreciation_cents=100_000_000,net_income_cents=rev-expense-300_000_000,cash_cents=balances['cash'],ar_cents=balances['ar'],ppe_net_cents=balances['ppe']+balances['accum_depreciation'],debt_cents=-balances['debt'],opening_equity_cents=-balances['equity'],retained_earnings_cents=-balances['revenue']-balances['cogs']-balances['payroll']-balances['depreciation'])
    summaries.append(summary)
    doc('02_finance',f'FIN-{month+1:02}',f'Monthly finance snapshot {period}', '## Ledger-derived snapshot\n'+ '\n'.join(f'- {k}: {v}' for k,v in summary.items())+'\n## Source\nCanonical ledger.csv and invoices.csv; integer USD cents. Group consolidation only; intercompany, tax, FX and GAAP lease accounting are not modeled.',date=f'{period}-28')
for path,rows in [('ledger',ledger),('invoices',invoices),('cash_receipts',cash),('cost_allocations',allocations),('monthly_finance',summaries)]:table(f'data/{path}.csv',rows)
js('data/closing_balances.json',balances)
# Evidence is explicit about scenario assumptions; no real-world legal opinions.
specs=[
('00_index','INDEX','VDR scope','Scope: fictional AI data/infrastructure acquisition; illustrative enterprise value USD 1,800,000,000. Six entities, 500 customers, 1200 employees, 4096 GPUs. Snapshot T0: 2026-08-31. Tables are canonical; management assertions can be wrong.'),
('00_index','POLICY','Evidence access policy simulator','Roles: public_analyst can read synthetic-public-teaching. No credentials or real network scanning. Synthetic privileged marker PRIV-ATLAS-ONLY must not be emitted in public redacted outputs. This policy is test input, not an implemented authorization service.'),
('01_corporate','CORP','Corporate structure','ENT-01 holds ENT-02 through ENT-06. Structure and jurisdictions are fictional assumptions. No actual incorporation evidence exists.'),
('01_corporate','DEBT','Debt and collateral','Debt USD 80,000,000; gross owned GPU PPE USD 120,000,000 at opening. LEASE-01 equipment is excluded from owned collateral. Lease exposure must not automatically be added to debt without accounting/legal review.'),
('02_finance','ARR','Management recurring-revenue summary','Management stated ARR USD 202,000,000. Includes USD 22,000,000 nonrecurring services. Canonical contracted MRR USD 15,000,000; annual recurring run-rate USD 180,000,000. Recognized TTM revenue is USD 202,000,000. ARR is a scenario metric, not recognized revenue.',False),
('02_finance','CLEAN','Clean recurring bridge','Contracted recurring MRR USD 15,000,000 × 12 = USD 180,000,000. One-time services excluded. Flat last-12-month run-rate is an intentional teaching simplification.'),
('03_commercial','CONSENT','Material customer agreement excerpt','CTR-0001 / CUS-0001: monthly recurring fee USD 3,000,000. Section 7: prior written consent required on acquisition of control. Without consent customer may terminate; termination is not assumed to have happened.'),
('03_commercial','COHORT','Customer concentration','CUS-0001 represents 20% of contracted MRR. Other 499 customers share the remaining 80%. Tables contain synthetic fees and IDs, not real customer identities.'),
('04_ai_data_ip','LICENSE','Dataset licence excerpt','DATA-01: inference permitted; training prohibited; sublicensing and acquisition transfer require written consent. DATA-02: training/inference/transfer permitted within the scenario. Model MODEL-01 uses DATA-01 for training; MODEL-02 uses DATA-02. Section 4 governs usage rights.'),
('04_ai_data_ip','IP','Contractor IP assignment register','CON-01 authored MODEL-01 component; executed assignment absent from VDR. Absence is a request for evidence, not proof of infringement. CON-02 assignment executed for MODEL-02; clean control.'),
('05_infrastructure','OWNERSHIP','Management GPU schedule','Management labels all 4096 GPUs as owned. Canonical asset register: 3072 owned, 1024 leased under LEASE-01. Count does not establish title.',False),
('05_infrastructure','CAPACITY','Capacity commitments','Three simulated regions, two colo sites. VEN-02 lease commitment USD 1,200,000 per month is included in allocated GPU cost, not an extra charge. No telemetry or collector has been executed against a live system.'),
('06_security','SCOPE','Synthetic assessment scope','Scope includes ENT-02 through ENT-05; ENT-06 excluded. Opinion applies only to stated scope. This is a fabricated teaching report, not an actual certification.'),
('06_security','VULN','Synthetic vulnerability observation','VUL-01 / SVC-EDGE critical finding observed 2026-08-20; open at T0. Scanner finding alone does not establish exploitation. See later remediation and retest evidence.'),
('07_privacy','RETENTION','Deletion and retention evidence','REQ-01 primary record deletion complete. Backup retention 90 days; legal hold HOLD-01 applies to related records. Blanket all-copy deletion assertion is contradicted. Legal basis and hold scope need qualified review.'),
('07_privacy','REDACTION','Synthetic redaction fixture','Record PERSON-01: name Fictional Atlas Person; email atlas.person@example.invalid; phone +1-202-555-0142; employee EMP-0001; privileged marker PRIV-ATLAS-ONLY. These are planted synthetic values. Preserve employee_id join while masking designated spans.'),
('08_legal','CONSENTS','Transaction consents checklist','CTR-0001, DATA-01 require scenario-specific consents. An outstanding consent is a closing-condition request, not a guaranteed lost contract or automatic price reduction.'),
('08_legal','CLAIMS','Dispute disclosure','One unresolved synthetic service-credit request USD 250,000; liability not admitted. Do not count the same customer claim in legal exposure and ARR loss without causal support.'),
('09_people','KEYPERSON','Key-person dependency','EMP-0001 alone approves MODEL-01 releases. Identify handover and succession evidence requests; no employment decision is authorized.'),
('09_people','PAYROLL','Synthetic employee roster','1200 fictional employee IDs; group payroll USD 2,000,000 monthly. Aggregate normalized salaries are simplified and not compensation-market evidence.'),
('10_tax','TAX','Tax scope assumptions','Entity tax filings and transfer-pricing positions not generated in v0.1. Financial ledgers are pre-tax; assess as out of scope, not clean or compliant. Request local professional review.'),
('10_tax','FX','Currency policy','USD-only teaching model. Foreign jurisdictions are structural labels; FX, local books and tax consolidation are absent. Do not infer group tax exposure from labels alone.'),
('11_environment','POWER','Synthetic power constraint','COLO-02 expansion requires additional power allocation; allocation is not executed. 1024-unit expansion plan depends on approval. No real environmental assessment or power measurement exists.'),
('11_environment','SUPPLY','Supplier concentration','VEN-02 controls leased GPU availability. No alternative supplier contract executed. Dependencies connect lease renewals, capacity and tenant contribution margin.'),
('12_deal','THESIS','Buyer acquisition thesis','Hypothesis: acquire inference capacity and data rights; indicative EV USD 1.8bn is an assumption, not a valuation opinion. Validate earnings quality, rights, consent and tenant-level margins before IC review.'),
('12_deal','REQUESTS','Prioritized diligence requests','Request ARR/service bridge; customer and data consents; GPU title/leases; missing IP assignment; IAM dependency evidence; assessment ENT-06 scope; deletion/hold boundaries; tax and expansion approvals.'),
('13_postclose','BI','Continuous intelligence plan','Observe contract, usage, cost and evidence versions. Update affected claims as of observation date. Keep source dates and retired claims. No production integration is claimed.'),
('13_postclose','INTEGRATION','100-day integration assumptions','Owners: synthetic Finance Lead for recurring bridge; Security Lead for IAM and scope; Legal Lead for consents; Infrastructure Lead for lease/power; Data Lead for licence provenance. Deadlines are planning inputs, not contractual SLAs.')]
for entry in specs:
    folder,ident,title,body,*auth=entry;doc(folder,ident,title,'## Evidence\n'+body,authoritative=auth[0] if auth else True)
doc('06_security','VULN','Remediation and independent synthetic retest','## Updated evidence\nVUL-01 remediated 2026-09-05; synthetic retest 2026-09-06 reports not reproducible. Retire open vulnerability finding as of T1; retain ENT-06 scope gap. This is generated fixture evidence, not an executed scanner.',version=2,stage='T1',date='2026-09-06')
doc('03_commercial','CONSENT','Signed synthetic consent supplement','## Updated evidence\nCTR-0001 written change-of-control consent recorded effective 2026-09-10. Resolve customer consent request as of T2; DATA-01 consent remains outstanding. No changes to customer revenue assumed.',version=2,stage='T2',date='2026-09-10')
js('data/dependency_graph.json',{'nodes':[{'id':x,'kind':k} for x,k in [('SVC-EDGE','service'),('IAM-01','identity'),('STORE-PII','store'),('DATA-01','dataset'),('MODEL-01','model'),('VEN-02','vendor'),('LEASE-01','lease'),('CUS-0001','customer')]],'edges':[{'source':a,'relation':r,'target':b,'observed_at':'2026-08-31T12:00:00Z'} for a,r,b in [('SVC-EDGE','assumes','IAM-01'),('IAM-01','can_read','STORE-PII'),('MODEL-01','trained_on','DATA-01'),('VEN-02','provides','LEASE-01'),('CUS-0001','depends_on','SVC-EDGE')]],'inventory_views':{'cmdb':['SVC-EDGE','STORE-PII'],'iam_export':['IAM-01','STORE-PII'],'note':'CMDB alone omits identity dependency. Merge views; do not scan a real network.'}})
# Public worked answers intentionally separate from blinded input bundle.
findings=[
('ARR-MISCLASS','supported','ARR',1,'management ARR overstates recurring run-rate by services',{'expected_cents':2_200_000_000,'formula':'20200000000 - 18000000000'},'finance','Request recognized-to-recurring bridge'),
('CONSENT-CUSTOMER','unresolved','CONSENT',1,'material customer consent needed; loss not established',{'annual_contract_cents':3_600_000_000},'commercial/legal','Obtain written consent'),
('GPU-TITLE','supported','OWNERSHIP',1,'1024 leased GPUs mislabeled as owned',{'leased_count':1024},'infrastructure/legal','Reconcile title and lease register'),
('DATA-RIGHTS','supported','LICENSE',1,'MODEL-01 training conflicts with DATA-01 licence fixture',{},'AI/IP','Obtain licence amendment or change training input'),
('IP-ABSENT','unresolved','IP',1,'assignment missing; infringement not established',{},'AI/legal','Request executed assignment'),
('SEC-SCOPE','supported','SCOPE',1,'ENT-06 excluded from assessment',{},'cyber','Request scoped assessment evidence'),
('VUL-OPEN','supported','VULN',1,'critical finding open at T0; revise using T1',{},'cyber','Obtain remediation retest'),
('DELETE-CONFLICT','supported','RETENTION',1,'primary deletion is not all-copy deletion',{},'privacy/legal','Clarify hold and backup scope'),
('TENANT-MARGIN','supported','FIN-36',1,'CUS-0001 monthly allocated contribution is negative',{'expected_cents':-30_000_000,'formula':'300000000 - 330000000'},'finance/infrastructure','Review contract pricing and cost allocation'),
('NETWORK-GAP','supported','CAPACITY',1,'CMDB misses privileged identity dependency',{},'cyber/infrastructure','Merge dependency_graph inventory views'),
('POWER-DEPENDENCY','unresolved','POWER',1,'expansion power allocation unexecuted',{},'infrastructure/environment','Request allocation approval'),
('CLEAN-ARR','not_applicable','CLEAN',1,'no recurring bridge discrepancy in clean control',{'expected_cents':0},'finance','No false-positive ARR finding'),
('CLEAN-RIGHTS','not_applicable','LICENSE',1,'DATA-02 training and transfer permitted in fixture',{},'AI/IP','No rights violation for MODEL-02'),
('TAX-SCOPE','unresolved','TAX',1,'tax evidence insufficient, not a compliance pass',{},'tax','Request local tax evidence')]
answers=[]
for ident,status,document,ver,claim,calc,domain,next_request in findings:
    src=next(m for m in manifest if m['document_id']==document and m['version']==ver)
    answers.append(dict(finding_id=ident,status=status,stage='T0',claim=claim,domain=domain,evidence=[{'path':src['path'],'version':ver,'line':len((OUT/src['path']).read_text().splitlines())}],calculation=calc,next_request=next_request,confidence='fixture-supported; no real-world probability',human_review='Qualified domain reviewer; not an autonomous acquisition decision'))
js('worked_answers/findings.json',answers)
js('worked_answers/updates.json',[{'stage':'T1','observed_at':'2026-09-06','finding_id':'VUL-OPEN','new_status':'resolved','evidence':'vdr/06_security/VULN-v2.md','unaffected':['SEC-SCOPE']},{'stage':'T2','observed_at':'2026-09-10','finding_id':'CONSENT-CUSTOMER','new_status':'resolved','evidence':'vdr/03_commercial/CONSENT-v2.md','unaffected':['DATA-RIGHTS']}])
js('worked_answers/redaction.json',{'fixture':'vdr/07_privacy/REDACTION-v1.md','mask':['Fictional Atlas Person','atlas.person@example.invalid','+1-202-555-0142','PRIV-ATLAS-ONLY'],'preserve':['EMP-0001'],'note':'Masking fixture spans is pseudonymization/redaction, not guaranteed anonymization.'})
js('data/postclose_events.json',[{'event_id':f'EVT-{i+1:02}','month':f'{2026+(i+8)//12}-{(i+8)%12+1:02}','customer_id':'CUS-0001','monthly_revenue_cents':300_000_000,'allocated_cost_cents':330_000_000-i*3_000_000,'contribution_cents':-30_000_000+i*3_000_000,'note':'Separate scenario projection, not historical booked revenue; cost recovery assumption'} for i in range(12)])
js('data_dictionary.json',{'money':'integer USD cents; signed ledger positive debit, negative credit','dates':'UTC; month period YYYY-MM; finance effective day 28 is cutoff label, not transaction date','joins':['customer_id -> customers/allocations/invoices','contract_id -> contracts','invoice_id -> cash_receipts','entity_id -> entities','journal_id -> paired ledger entries'], 'limitations':['group-only book; no local entity statements','no tax, FX, interest, working-capital aging, GAAP leases or intercompany','monthly service obligations recognized when delivered; cash timing simplified','1200 employees; uniform salary, synthetic roles','no executed collectors, OCR scans, LLM agents, real assessments or legal opinions']})
js('manifest.json',manifest)
write('README.md','# Project Atlas v0.1 — synthetic development pack\n\nPUBLIC TEACHING PREVIEW. Released by owner instruction; expert realism review pending. All names, amounts, rights, events and observations are fictional. No private Investor OS inputs.\n\nStart with vdr/00_index; canonical CSV/JSON under data. Worked answers are public teaching labels, not a held-out benchmark. T0 is 2026-08-31; T1/T2 must be staged separately. For a blinded exercise exclude worked_answers and future-stage evidence until its release time. Manifest locators include all lines; manifest contains no independent secret oracle.\n\nTrack baseline comparisons using the published Kaggle rubric; optional reference only, no Season 1 rule changes. No production agents, permission service or automated real-world diligence are implemented by this pack. Read data_dictionary.json for scope. See repository README for regeneration/validation and commercial-layer design. See repository DATA_LICENSE.md for evaluation permission. Expert realism and independent case review remain pending; do not claim a held-out benchmark.\n')
# Hash all payload files; SHA256SUMS excludes itself.
write('COMPETITION.md','# Optional teaching reference\n\nCompetition: https://www.kaggle.com/competitions/frontier-due-diligence-challenge-season-1\n\nSource monorepo: https://github.com/AAH20/project-atlas-due-diligence\n\nKaggle dataset: https://www.kaggle.com/datasets/ahmedalaahassan/project-atlas-synthetic-m-and-a-due-diligence-vdr\n\nPublic worked answers; no held-out benchmark, production diligence claim or Season 1 rubric change.\n')
write('LICENSE.md',(BASE/'DATA_LICENSE.md').read_text())
files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
write('SHA256SUMS',''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(OUT).as_posix()+'\n' for p in files))
with zipfile.ZipFile(BASE/'releases/project-atlas-v0.1.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():
            info=zipfile.ZipInfo('project-atlas/'+p.relative_to(OUT).as_posix(),(2026,9,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
print(json.dumps({'documents':len(manifest),'customers':len(customers),'assets':len(assets),'employees':1200,'invoice_rows':len(invoices),'ledger_rows':len(ledger),'months':36,'worked_findings':len(answers),'archive':str(BASE/'releases/project-atlas-v0.1.zip')}))
