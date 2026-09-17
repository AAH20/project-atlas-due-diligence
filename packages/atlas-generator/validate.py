"""Independent artifact and accounting checks. Does not import generator or answers."""
from pathlib import Path
from collections import defaultdict
import csv, hashlib, json
ROOT=Path(__file__).resolve().parents[2]/'datasets/project-atlas/v0.1'
def rows(name):
    with (ROOT/f'data/{name}.csv').open() as f:return list(csv.DictReader(f))
def validate(root=ROOT):
    global ROOT; ROOT=root
    customers=rows('customers'); assets=rows('assets'); employees=rows('employees');invoices=rows('invoices');receipts=rows('cash_receipts');ledger=rows('ledger');alloc=rows('cost_allocations');finance=rows('monthly_finance')
    assert len(customers)==500 and len({x['customer_id'] for x in customers})==500
    assert len(assets)==4096 and len(employees)==1200
    assert sum(int(x['mrr_cents']) for x in customers)*12==18_000_000_000
    assert sum(int(x['monthly_salary_cents']) for x in employees)==200_000_000
    assert sum(x['ownership']=='leased' for x in assets)==1024
    assert sum(int(x['book_value_cents']) for x in assets)==12_000_000_000
    ids={x['customer_id'] for x in customers}; cids={x['contract_id'] for x in rows('contracts')}|{'SOW-01'}
    invmap={x['invoice_id']:x for x in invoices}; assert len(invmap)==len(invoices)
    paid=defaultdict(int)
    for r in receipts:
        assert r['invoice_id'] in invmap
        paid[r['invoice_id']]+=int(r['amount_cents'])
    for i in invoices:
        assert i['customer_id'] in ids and i['contract_id'] in cids
        assert paid[i['invoice_id']]==int(i['collected_cents'])
        assert int(i['recognized_cents'])==int(i['amount_cents'])
    journals=defaultdict(list); period_accounts=defaultdict(lambda:defaultdict(int))
    balances=json.loads((ROOT/'data/opening_balances.json').read_text())
    assert sum(balances.values())==0
    for r in ledger:
        journals[r['journal_id']].append(r)
        period_accounts[r['period']][r['account']]+=int(r['signed_cents'])
    for j,items in journals.items():
        assert len(items)==2 and len({r['reference'] for r in items})==1
        assert sum(int(x['signed_cents']) for x in items)==0, j
    for r in alloc:
        assert int(r['total_cents'])==sum(int(r[x]) for x in ['gpu_cents','power_cents','support_cents','retry_cents'])
    for s in finance:
        period=s['period'];acc=period_accounts[period]
        rev=sum(int(i['recognized_cents']) for i in invoices if i['period']==period)
        recurring_cost=sum(int(x['total_cents']) for x in alloc if x['period']==period)
        service_cost=sum(int(i['amount_cents'])//2 for i in invoices if i['period']==period and i['kind']=='one_time_services')
        assert rev==-acc['revenue']==int(s['revenue_cents'])
        assert recurring_cost+service_cost==acc['cogs']==int(s['cogs_cents'])
        assert acc['payroll']==200_000_000 and acc['depreciation']==100_000_000
        assert rev-acc['cogs']-acc['payroll']-acc['depreciation']==int(s['net_income_cents'])
        for account,amount in acc.items():balances[account]+=amount
        assert sum(balances.values())==0
        assert balances['cash']==int(s['cash_cents']) and balances['ar']==int(s['ar_cents'])
        net_assets=int(s['cash_cents'])+int(s['ar_cents'])+int(s['ppe_net_cents'])
        liabilities_equity=int(s['debt_cents'])+int(s['opening_equity_cents'])+int(s['retained_earnings_cents'])
        assert net_assets==liabilities_equity
    assert balances==json.loads((ROOT/'data/closing_balances.json').read_text())
    assert sum(int(s['revenue_cents']) for s in finance[-12:])==20_200_000_000
    assert balances['ar']==int(finance[-1]['revenue_cents'])
    manifest=json.loads((ROOT/'manifest.json').read_text()); assert len(manifest)==66
    for m in manifest:
        p=ROOT/m['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
        lines=p.read_text().splitlines()
        for loc in m['locators']:assert lines[loc['line']-1]==loc['text']
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,path=line.split('  ',1);assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
    for answer in json.loads((ROOT/'worked_answers/findings.json').read_text()):
        for e in answer['evidence']:
            assert 1<=e['line']<=len((ROOT/e['path']).read_text().splitlines())
    graph=json.loads((ROOT/'data/dependency_graph.json').read_text());nodes={n['id'] for n in graph['nodes']}
    assert all(e['source'] in nodes and e['target'] in nodes for e in graph['edges'])
    for event in json.loads((ROOT/'data/postclose_events.json').read_text()):
        assert event['monthly_revenue_cents']-event['allocated_cost_cents']==event['contribution_cents']
    return dict(status='PASS',checks=['invoice/cash joins','paired journals','monthly revenue/cost reconciliation','balance sheets','opening/closing balances','TTM 202m','ARR 180m','payroll','asset ownership/PPE','hashes/locators','graph integrity','projection arithmetic'],vdr_documents=len(manifest),ledger_rows=len(ledger))
if __name__=='__main__':print(json.dumps(validate(),indent=2))
