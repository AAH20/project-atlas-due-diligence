# Project Atlas v0.1 build report — 2026-09-17

Scope: standalone synthetic teaching dataset; no Investor OS writes, no private inputs. Dataset-only build evidence follows.

## Commands and results
Executed from `/Users/ahmedhassan/Downloads/a2z-soc-main 2`:

1. `python3 packages/atlas-generator/build.py` — exit 0. 66 VDR Markdown documents, 500 customers, 4096 assets, 1200 employees, 18036 invoices, 107358 ledger lines, 36 monthly snapshots, 14 worked findings; ZIP generated.
2. `python3 packages/atlas-generator/validate.py` — exit 0, PASS. Invoice/receipt joins, journal balance, monthly revenue/expense reconciliation, all balance sheets, opening/closing balances, TTM revenue $202m, ARR $180m, payroll, ownership/PPE, hashes/locators, graph and projection arithmetic checked.
3. `python3 packages/atlas-generator/reference_run.py` — exit 0. Correct six numeric outputs: ARR $180m; management ARR $202m; discrepancy $22m; 1024 leased GPUs; CUS-0001 monthly contribution -$300k; clean bridge discrepancy zero. Correct T0→T1 vulnerability resolution and T1→T2 customer consent resolution; unrelated scope/data rights remain outstanding. Planted-value redaction preserved employee join. Runtime 23.911ms on this run; no provider calls, provider cost zero. Fixture-specific hand-authored reference, not a general agent result.
4. `python3 packages/atlas-generator/check_release.py` — exit 0, PASS. Deterministic ZIP regeneration and independent rejection of a +$1 unbalanced journal. ZIP SHA-256 `ba1ae353ab38cbaea4b9e295410b4054b38cf2847d2b518224683e17b8bfba2b`.

## Release state
LOCAL_REVIEW_CANDIDATE. No Kaggle upload, no public benchmark announcement, no hidden grading or Season 1 rule change. Expert finance/infra/privacy/legal realism review, license approval and independent case review remain pending. Model limits and simulated capabilities are documented in README and data_dictionary.json. Do not equate automated accounting checks with real-world acquisition realism or full agentic diligence performance.
