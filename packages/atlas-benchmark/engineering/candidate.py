"""Repair this faulty teaching implementation without changing its interface."""
def reconcile(invoices, receipts):
    return {'revenue': sum(i['amount'] for i in invoices), 'cash': sum(i['amount'] for i in invoices)}
