# Project Atlas — Synthetic M&A Due Diligence VDR

A **v0.1 public teaching preview** for a fictional large AI data and infrastructure acquisition, organized by **Apex Growth Systems LLC (US-based)**. Every company, customer, employee, amount, contract excerpt and observation is synthetic. No private Investor OS implementation, workflow videos, real customer records or actual VDR data are included.

**Join the Frontier Due Diligence Challenge — Season 1:**
https://www.kaggle.com/competitions/frontier-due-diligence-challenge-season-1

Read the rules and rubric, choose one track, and submit a reproducible Kaggle Writeup by **October 17, 2026 at 23:59 UTC**. Free, kudos-only; no cash prizes, Kaggle points/medals or guaranteed investor review/contracts. This dataset is optional; Season 1 rules and scoring remain unchanged.

**Public GitHub monorepo, generator, validator and reproduction instructions:**
https://github.com/AAH20/project-atlas-due-diligence

## What is included
- 66 versioned Markdown VDR documents across corporate, finance, commercial, AI/data/IP, infrastructure/network, cyber, privacy, legal, people, tax, environment, deal and post-close evidence.
- 500 customers, 4096 GPU records, 1200 employee IDs and six synthetic entity labels.
- 36 monthly group financial snapshots; 18036 invoice rows and 107358 double-entry ledger lines.
- Canonical CSV/JSON tables, exact document/version/line locators, SHA-256 manifests, dependency graph, synthetic privacy fixtures and 12 post-close monthly projections.
- 14 public worked findings, clean/control cases and staged T0/T1/T2 evidence updates.

The fictional model reconciles $180m recurring run-rate with $202m recognized TTM revenue. Management misclassifies $22m one-time services as recurring ARR. Other cases cover leased GPU title, negative tenant contribution, customer/data consents, missing IP assignments, assessment scope and privacy deletion/hold boundaries. Clean controls test false positives; later evidence resolves selected findings without clearing unrelated risks.

## Suggested tasks
Reconcile contracts, invoices, cash, ledgers and tenant COGS; merge CMDB/IAM dependencies; request missing evidence; preserve ETL lineage; redact planted synthetic identifiers without losing permitted joins; connect at least three domains; revise cited findings after new evidence; compute post-close contribution updates. State assumptions, human-review boundaries, numeric tolerances, cost/runtime and failure modes.

## Start and reproduce
Start with README.md, COMPETITION.md and data_dictionary.json in the project-atlas payload. Use vdr/ for evidence and data/ for canonical records. Source reproduction requires Python 3.10+ standard library, no API keys or paid services:

```sh
git clone https://github.com/AAH20/project-atlas-due-diligence.git
cd project-atlas-due-diligence
python3 packages/atlas-generator/build.py
python3 packages/atlas-generator/validate.py
python3 packages/atlas-generator/reference_run.py
python3 packages/atlas-generator/check_release.py
```

Automated checks cover balanced journals, all 36 balance sheets, invoice/receipt joins, revenue/COGS/PPE/payroll reconciliation, hashes/locators and deterministic packaging. The small reference is fixture-specific arithmetic, known-value redaction and staged update handling; it is not a general LLM agent or full-domain baseline.

## Leakage and realism limits
Worked answers are deliberately public. This is a teaching/development set, **not a held-out benchmark**. Withhold answers, T1/T2 evidence and future-stage manifest entries in blind exercises. Do not claim unseen performance after reading labels. Independent expert realism review remains pending. Books are group-only, USD-only and pre-tax; local statutory accounts, FX, intercompany, interest, tax and GAAP lease accounting are absent. Salary and asset distributions and flat TTM run-rate are simplified. Text documents do not test scanned PDF/OCR/XLSX metadata. Clauses and assessments are fabricated teaching excerpts. Known-value redaction does not guarantee general PII discovery or anonymization. Production collectors, ETL, permission services and live integrations are not implemented. This is not professional advice, certification or real deal evidence.

## Licence — Other (specified in description)
Copyright 2026 Apex Growth Systems LLC. All rights reserved except the permission below.

Permission is granted to download, copy, modify and redistribute the Project Atlas synthetic teaching data and worked answers for research, education, evaluation and participation in the Frontier Due Diligence Challenge, with attribution to Apex Growth Systems LLC and a link to the GitHub repository. Preserve synthetic-data and limitation notices, and identify modifications. This permission does not grant branding rights, endorsement, exclusivity, commercial resale or rights to private Investor OS/Scale AI software. Commercial integration or resale requires a separate agreement. Data is provided AS IS without warranty. Public labels must not be presented as unseen evaluation results. No participant code is included or licensed by this permission. See LICENSE.md in the payload and DATA_LICENSE.md on GitHub.

## References and contact
Public Investor OS interface: https://investor-os.vercel.app
Public diligence-agent baseline: https://github.com/AAH20/A2Z_due-diligence-agents
Workflow 3 synthetic screenshot walkthrough: https://www.youtube.com/watch?v=0a11vE7aYSA
Organizer: https://a2zsoc.com
Separately scoped customization, technical/AI/cyber diligence, managed evidence/GRC and MSP/MSSP enquiries: https://a2zsoc.com/contact

Challenge questions belong in the competition Discussion tab. No purchase, commercial IP transfer, sponsorship, funding or contract is guaranteed or required for participation.
