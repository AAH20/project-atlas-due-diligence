"""Small transparent teaching reference, NOT full-domain agentic diligence."""
from pathlib import Path
import csv,json,re,time,hashlib
BASE=Path(__file__).resolve().parents[2];ROOT=BASE/'datasets/project-atlas/v0.1'
start=time.perf_counter()
def rows(name):
    with (ROOT/f'data/{name}.csv').open() as f:return list(csv.DictReader(f))
customers=rows('customers');assets=rows('assets');costs=rows('cost_allocations')
arr=sum(int(c['mrr_cents']) for c in customers)*12
body=(ROOT/'vdr/02_finance/ARR-v1.md').read_text()
stated=int(re.search(r'Management stated ARR USD ([\d,]+)',body)[1].replace(',',''))*100
customer=next(c for c in customers if c['customer_id']=='CUS-0001')
cost=next(c for c in costs if c['customer_id']=='CUS-0001' and c['period']=='2026-08')
outputs={'arr_cents':arr,'management_arr_cents':stated,'arr_discrepancy_cents':stated-arr,'leased_gpu_count':sum(a['ownership']=='leased' for a in assets),'customer_0001_monthly_contribution_cents':int(customer['mrr_cents'])-int(cost['total_cents']),'clean_arr_discrepancy_cents':18000000000-arr}
fixture=(ROOT/'vdr/07_privacy/REDACTION-v1.md').read_text()
# Deliberately explicit fixture rules; does not claim general PII discovery.
redacted=fixture
for value in ['Fictional Atlas Person','atlas.person@example.invalid','+1-202-555-0142','PRIV-ATLAS-ONLY']:redacted=redacted.replace(value,'[REDACTED]')
assert 'EMP-0001' in redacted
assert all(x not in redacted for x in ['atlas.person@example.invalid','PRIV-ATLAS-ONLY'])
result=BASE/'evaluations/reference/results';result.mkdir(exist_ok=True);(result/'redacted-fixture.md').write_text(redacted)
# Version-aware reference: no T1/T2 evidence used in T0.
stages=[]
for stage,version,consent_version in [('T0',1,1),('T1',2,1),('T2',2,2)]:
    vuln=(ROOT/f'vdr/06_security/VULN-v{version}.md').read_text()
    consent=(ROOT/f'vdr/03_commercial/CONSENT-v{consent_version}.md').read_text()
    stages.append({'stage':stage,'vulnerability_status':'resolved' if 'reports not reproducible' in vuln else 'open','customer_consent_status':'resolved' if 'consent recorded' in consent else 'request consent','assessment_scope_gap':'ENT-06 remains unassessed','data_transfer_consent':'outstanding'})
report={'reference':'fixture-specific arithmetic and staged evidence reference; not an LLM or general agent','outputs':outputs,'stages':stages,'runtime_ms':round((time.perf_counter()-start)*1000,3),'provider_cost_usd':0,'manual_intervention':'none during execution; rules authored for this public teaching fixture','scope':'four numeric assertions and two update transitions; no full 14-finding precision/recall claim','naive_comparator':{'method':'repeat management ARR assertion without reconciliation','arr_cents':stated,'absolute_error_cents':abs(stated-arr)},'checked_ground_truth':{'numeric_matches':outputs=={'arr_cents':18000000000,'management_arr_cents':20200000000,'arr_discrepancy_cents':2200000000,'leased_gpu_count':1024,'customer_0001_monthly_contribution_cents':-30000000,'clean_arr_discrepancy_cents':0}},'release_inputs_sha256':hashlib.sha256((ROOT/'SHA256SUMS').read_bytes()).hexdigest()}
assert report['checked_ground_truth']['numeric_matches']
assert stages[0]['vulnerability_status']=='open' and stages[1]['vulnerability_status']=='resolved'
assert stages[1]['customer_consent_status']=='request consent' and stages[2]['customer_consent_status']=='resolved'
(result/'reference-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
