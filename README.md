# Project Atlas — Synthetic M&A Due Diligence Lab

A reproducible **v0.1 teaching preview** for a fictional large AI data/infrastructure acquisition. Built by **Apex Growth Systems LLC (US-based)**.

**Join the [Frontier Due Diligence Challenge — Season 1](https://www.kaggle.com/competitions/frontier-due-diligence-challenge-season-1)**: choose a track, compare a documented baseline on material, clean/control and evidence-update cases, and submit a reproducible Kaggle Writeup by **October 17, 2026 at 23:59 UTC**. Free, kudos-only; no cash prizes, Kaggle points/medals or guaranteed investor review/contracts. This dataset is optional; the published rubric stays unchanged.

[Download on Kaggle](https://www.kaggle.com/datasets/ahmedalaahassan/project-atlas-synthetic-m-and-a-due-diligence-vdr) · [Workflow 3 public walkthrough](https://www.youtube.com/watch?v=0a11vE7aYSA) · [Investor OS public demo](https://investor-os.vercel.app) · [Public diligence-agent baseline](https://github.com/AAH20/A2Z_due-diligence-agents)

## Contents

### Local v0.2 expansion

[Expansion dataset](datasets/project-atlas/v0.2/README.md) adds a separate fictional three-entity acquisition, 36 material/control/insufficient-evidence exercises, 72 monthly entity statements, forward compute economics, a five-stage financing timeline, role/stage fixtures and four commercial reporting samples. v0.1 remains intact; do not combine the two accounting histories. The existing Kaggle dataset remains v0.1; this repository includes the v0.2 expansion.

[Evidence interface](docs/ATLAS_V02_EVIDENCE_INTERFACE.md) · [Evaluation design](docs/ATLAS_V02_EVALUATION.md) · [Commercial scope](docs/ATLAS_V02_COMMERCIAL.md)

Node 22 standard library; no providers or private software required:

```sh
node packages/atlas-expansion/build.mjs
node packages/atlas-expansion/validate.mjs
node --test packages/atlas-expansion/expansion.test.mjs
```

Public author labels and fixture checks do not establish frontier agent performance or expert realism. Organizer evaluation candidates and their generator are kept outside this public monorepo. The published competition rubric is unchanged.

### Agentic benchmark development pilot

[Benchmark pilot](benchmarks/atlas-agentic-v0.1/README.md) · [Kaggle suite](https://www.kaggle.com/benchmarks/ahmedalaahassan/atlas-agentic-due-diligence-development-pilot): nine public evidence/calculation cases, a budgeted staged investigation simulator with JSON replays, two Kaggle SDK adapters and an engineering repair exercise. Public oracle self-checks are not model rankings. The competition rubric stays unchanged.

### v0.1 teaching preview

- 66 versioned Markdown VDR documents spanning corporate, finance, commercial, AI/data/IP, infrastructure, security, privacy, legal, people, tax, environment, deal and post-close evidence.
- 500 synthetic customers, 4096 GPUs, 1200 employee IDs, 36 monthly group snapshots, 18036 invoice rows and 107358 double-entry ledger lines.
- 14 worked findings, clean controls, staged T0/T1/T2 updates, synthetic privacy fixtures, a dependency graph and 12 monthly post-close projections.
- $180m recurring run-rate and $202m recognized TTM revenue; $22m services classification discrepancy; 1024 leased GPUs; negative contribution for one tenant. All are fictional scenario inputs/results.

## Monorepo layout

| Path | Purpose |
|---|---|
| packages/atlas-generator | Deterministic generator, independent validator, small reference, release checks |
| datasets/project-atlas/v0.1 | VDR, canonical tables, dictionary, manifests, public worked answers |
| evaluations/reference/results | Executable reference outputs; fixture-specific, not full-domain agents |
| docs | Scope, commercial offering architecture, release evidence and participation guidance |
| releases | Deterministically packaged teaching ZIP |

## Reproduce

Python 3.10+ standard library; no API keys, provider access or paid subscription.

```sh
git clone https://github.com/AAH20/project-atlas-due-diligence.git
cd project-atlas-due-diligence
python3 packages/atlas-generator/build.py
python3 packages/atlas-generator/validate.py
python3 packages/atlas-generator/reference_run.py
python3 packages/atlas-generator/check_release.py
```

The validator checks receipt joins, paired journals, all 36 balance sheets, revenue/cost/PPE/payroll reconciliation, manifest hashes/locators, graph integrity and projection arithmetic. Release checks regenerate an identical ZIP and reject a deliberately corrupted journal. The reference performs fixture-specific arithmetic, known-value redaction and two staged updates; it is not a general agent or claimed frontier result. Its naive comparator only repeats management ARR.

## Tasks and leakage boundaries

Investigate ARR vs recognized revenue, tenant-level COGS/margin, asset title/leases, data training/transfer rights, missing IP assignments, customer consent, network/identity dependencies, assessment scope, deletion/hold conflicts and updated evidence. Cite exact versions/locations and state unknowns.

Worked answers are intentionally public teaching labels. For blind exercises withhold worked_answers, T1/T2 documents and future-stage manifest entries until release time. A genuine held-out benchmark needs independent structurally different cases and separate seeds/oracle. No rule changes or undisclosed mandatory hidden grading apply to this season.

## Limits

Automated arithmetic checks pass; independent expert realism review remains pending. Six entities are structural labels; books are group-only, USD-only and pre-tax. No local statutory accounts, tax, FX, intercompany, interest, GAAP lease treatment or realistic salary distributions. Flat TTM revenue and evenly distributed asset values are teaching simplifications. Text-only documents do not test scanned PDFs/OCR/XLSX metadata. Assessment reports and clauses are fabricated excerpts. Known-value redaction does not guarantee general PII detection or anonymization. Collectors, production ETL, authorization services, LLM agents and live integrations are not implemented here. Not professional advice or real-world acquisition evidence.

## Commercial layers

[Offering design](docs/COMMERCIAL_AND_DATASET_DESIGN.md): free public lab; licensed private evaluation packs; A2Z SOC scoped technical/AI/cyber diligence; managed evidence/GRC; separately contracted MSP/MSSP; continuous portfolio BI; custom integrations. These are proposed layers, not claims that all features/services are live. Hero metrics: contribution margin per tenant/deal, COGS, payback and cost per verified material finding.

No private application implementation or other private workflow videos are included.

## Permission and contact

See [LICENSE](LICENSE) and [DATA_LICENSE.md](DATA_LICENSE.md): attributed research/education/evaluation and challenge reuse permitted; commercial resale/integration needs separate agreement. No participant IP transfer or purchase required.

Challenge questions: competition Discussion tab. Separately scoped customization, diligence, managed evidence/GRC and MSP/MSSP enquiries: [A2Z SOC contact](https://a2zsoc.com/contact). No sponsorship, investment, certification or contract is guaranteed.
