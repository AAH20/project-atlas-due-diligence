> Historical design blueprint. The v0.1 public teaching implementation and its limitations are documented in the repository README; expert realism remains unreviewed. Public release was explicitly authorized by the owner on 2026-09-17.

# Proposed synthetic acquisition lab — Project Atlas

Status: design, not a generated dataset or announced change to Season 1 scoring. All company names, records, amounts and events below are fictional assumptions. No private Investor OS workflows or customer information are inputs.

## Scenario
A fictional strategic acquirer evaluates a fictional AI data and infrastructure provider at an illustrative USD 1.8 billion enterprise value. Target: USD 180 million contracted ARR, USD 202 million trailing revenue, 500 enterprise customers, 1,200 employees, six legal entities, three hosted regions, two leased colocation sites and 4,096 owned/leased GPU units. These are initial design anchors; the final generator must produce internally reconciled numbers rather than treating ARR, recognised revenue and cash receipts as interchangeable.

Three revenue lines: enterprise inference subscriptions/usage; reserved GPU capacity; licensed datasets and managed data pipelines. Separately model professional services and pass-through charges. Follow 36 historical months, diligence at T0, supplemental disclosures at T1/T2, signing/closing conditions and 12 post-close monthly events. The lab supports buy-side diligence, sell-side readiness and post-close integration.

## Build from a canonical synthetic business model
Generate versioned entities, customers, contracts/amendments, invoices, ledger postings, cash settlements, employees, vendors, assets, network components, datasets, models, processing activities, incidents and controls. Stable identifiers link every artifact. Units, currency, exchange rates, dates, entity boundaries, accounting policy and reporting cutoffs are explicit.

Maintain an internally correct base state. Create issues using documented deterministic mutations: scope changes, stale versions, misclassifications, missing evidence and genuine exceptions. Keep an oracle change log. Documents are rendered views of the structured records; they are never independent LLM inventions of financial totals.

Revenue bridge: contracts and obligations -> usage -> invoices -> revenue/deferred revenue -> receivables -> cash -> segment/customer metrics. Infrastructure bridge: asset ownership/lease -> workload allocation -> metering -> cloud/colo/power cost -> tenant/product COGS. Balance sheets balance; cash-flow changes reconcile; no ARR conversion for one-time revenue; no double counting a shared asset or risk.

## Proposed VDR
00 index, manifests, data dictionary, access-policy simulator and Q&A
01 corporate structure, ownership, board approvals, cap table, debt and liens
02 finance: monthly trial balances, statements, revenue policies, invoices, receivables, cash and quality-of-earnings bridges
03 commercial: customer cohorts, CRM snapshots, contracts, amendments, renewals, concentration and pipeline
04 AI/data/IP: dataset registries, provenance, licences, training rights, model cards, evaluations, source/SBOM inventories, contractor IP assignments
05 infrastructure/network: owned versus leased assets, CMDB, cloud inventory, IPAM, DNS, IAM, Kubernetes/storage snapshots, network rules, GPU metering and capacity commitments
06 security: synthetic vulnerability exports, incident timelines, logs, backup/restore evidence, access reviews, scoped assessment reports and exceptions
07 privacy: synthetic PII fixtures, processing inventories, DPAs, retention, deletion requests, legal holds and cross-border flow records
08 legal/regulatory: disputes, material obligations, change-of-control, assignment, consents and jurisdiction assumptions
09 people/operations: synthetic roster, retention obligations, key-person dependencies, vendor contracts, support and business continuity
10 tax: synthetic entity tax schedules, transfer-pricing assumptions and contingent exposure evidence
11 environmental/supply chain: power/water metering, supplier concentration, equipment provenance and lease obligations
12 deal/integration: buyer thesis, transaction assumptions, diligence requests, conditions, integration dependencies and 100-day plan
13 post-close event feeds: customer, financial, capacity, security, privacy and operational updates

Release target: small 60–100 document teaching pack first; extended 250–400 document VDR with 100k–500k structured rows next. Each file gets document_id, entity_id, version, effective_at, observed_at, classification, SHA-256, authoritative-source designation and locator mapping. Provide PDF/CSV/JSON/Parquet/XLSX where justified; retain originals plus normalized outputs. Include scanned/low-quality, duplicated and superseded documents deliberately, with labelled cases in public teaching material.

## Agent tasks and boundaries
1. Asset/network mapping: merge conflicting inventories and identify service, identity, dataset, vendor and tenant dependencies. Use synthetic exported observations or an isolated local simulator; never scan a real target network.
2. Evidence collection: request relevant evidence, record source/time/scope/hash, preserve originals, label absence versus contradiction and enforce simulated role permissions.
3. ETL: parse/OCR, normalize dates/currency/entities, deduplicate, quarantine malformed rows and preserve lineage. Retry idempotently; record rejected rows.
4. Privacy preparation: locate planted synthetic direct/quasi-identifiers, redact required spans, preserve necessary document structure and use consistent pseudonyms for permitted joins. Store reversible mappings separately; do not call token substitution anonymization. Test PDFs, OCR text, spreadsheets, filenames and metadata.
5. Domain diligence: produce cited findings, reproducible calculations, counter-evidence, materiality rationale, next requests and required human review. Connect risks across domains without double counting financial exposure.
6. Transaction support: buyer-specific memo, supported price/earnings sensitivities, conditions precedent, consent/retention requests and integration dependencies. Separate assumed exposures from verified amounts.
7. Continuous BI: revise affected claims after events, reconcile changed KPIs and surface operational actions with owner/deadline/evidence. Maintain as-of views and late-arriving corrections; assess both alert precision and missed change detection.

## High-value cross-domain cases
- Management ARR includes nonrecurring implementation fees; contract/ledger/cash evidence exposes the bridge.
- A material inference customer has a change-of-control termination right; apparent concentration and valuation assumptions depend on renewal evidence.
- Promotional inference pricing appears profitable until GPU reservation commitments, power, support and retries are allocated by tenant.
- GPUs counted as owned collateral are leased; liens and lease schedules change net debt and available capacity assumptions.
- A dataset permits inference but not training or sublicensing; a model and acquisition transfer depend on those rights.
- Contractor-created model components lack an executed IP assignment.
- A clean CMDB misses a privileged service account linking a public endpoint to a synthetic sensitive-data store.
- Assessment scope excludes a recently acquired subsidiary; a clean report is not group-wide evidence.
- Privacy deletion evidence conflicts with immutable backup retention and a legal hold.
- An apparent critical vulnerability is stale and demonstrably remediated; an updated report must retire the claim.
- Water/power constraints and a cloud vendor minimum commitment weaken a capacity expansion plan.
- Tax/entity inconsistencies change a cash forecast; legal/accounting interpretations remain expert-reviewed assumptions.

Include clean lookalikes, legitimate explanations and unresolved questions. Do not make every exception a red flag. Avoid a single composite score pretending to establish whether an acquisition is objectively good.

## Evaluation
Use task-level grades and the already published Season 1 track rubric. Do not introduce new mandatory datasets, secret grading or weights mid-season. Publish this pack as optional reference material with an announcement; a future season may define standardized held-out tasks in advance.

Measure entity/edge mapping precision and recall; source/version fidelity; evidence sufficiency and useful requests; ETL accounting reconciliation and lineage retention; PII recall, false-positive redaction, relationship preservation and simulated permission violations; domain risk precision/recall; numeric error within explicit tolerances; update correctness; cost/runtime/retries. Privileged planted markers must not appear in prohibited outputs or logs. Treat tiny zero-leakage tests as finite test results, not universal privacy guarantees.

Future formal benchmark: public development pack with worked answers; structurally different private evaluation cases stored separately; frozen baseline and submitted releases; independent human review of ambiguous/material labels; repeat runs; disclosed graders; an appeal process. Private evaluation oracle, seeds and issue-placement rules are not included in public files. Independent case variants must change business relationships, not just names/numbers.

## Commercial layers and offerings
Public lab: free dataset, schema, starter cases, baseline reference and reproducible tasks. Buyer: builders/researchers. Value: demonstrable engineering assets. No platform purchase, IP assignment or commercial lead consent required.

Evaluation product: licensed private case packs, hosted isolated evaluation, regression suite and detailed reliability/cost reports. Buyer: AI diligence vendors and enterprise engineering teams. Charge per licensed pack or evaluation workload; publish clear scope and commercial rights. Do not charge for a better competition rank.

Investor OS deal workspace: permissioned evidence/Q&A, risk register, IC memo workflow, approvals and transaction integration plan. Buyer: VC/PE/strategic M&A teams. Pricing hypothesis: per deal/workspace with seats/storage/processing allowances. Needs demonstrated reproducibility, secure deployment and a real human review workflow.


A2Z SOC evidence/diligence sprint: authorised asset discovery, evidence readiness, technical/AI/cyber review and integration priorities. Buyer: acquirer or target. Fixed scoped engagement with explicit exclusions, signed access authority and expert-reviewed deliverables. Separate financial/legal/tax professionals where needed.

Managed evidence and GRC: recurring evidence refresh, exceptions, control tracking, supplier review and audit support. Buyer: target/post-close operator. Retainer per entity/environment; certification is a separate accredited process.

MSP/MSSP: cloud/identity/infrastructure operations, vulnerability remediation, monitoring and incident response under separately contracted service levels. Buyer: portfolio operating teams. Retainer plus disclosed usage/response scope; does not imply a staffed 24/7 service already exists.

Continuous portfolio BI: recurring financial, capacity, margin and risk updates tied to retained evidence and action owners. Buyer: portfolio operations/CFO/platform team. Subscription per portfolio company with compute/connectors priced explicitly.

Custom integrations/private deployment: paid connector implementation, customer taxonomies, residency requirements, deployment and support. Buyer: enterprise teams. Statement of work and annual support; integration of participant work requires a separate voluntary licence/contract.

Commercial hero metrics: contribution margin per tenant/deal, cost per verified material finding, analyst time to resolve uncertainty, repeat-service retention, onboarding cost and acquisition payback. Keep cloud/GPU/model/data costs, analyst review, support, onboarding and incident obligations in the costing model. Prices require buyer validation; none are claimed as market-proven.

## Release gates
Schema and arithmetic reconciliation -> expert realism review -> artifact/locator validation -> planted-PII and metadata inspection -> licence review -> baseline reproduction -> independent case review -> immutable manifest/checksums -> optional public Kaggle upload. Document simulated collectors, synthetic assessments and non-executed integrations clearly. Publish no customer data, private videos, prompts or Investor OS implementation.

## References
NIST SP 800-188: https://csrc.nist.gov/pubs/sp/800/188/final
NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
FinOps unit economics: https://www.finops.org/framework/capabilities/unit-economics/
FinOps data ingestion: https://www.finops.org/framework/capabilities/data-ingestion/
AgentDojo: https://github.com/ethz-spylab/agentdojo
FinanceBench: https://github.com/patronus-ai/financebench
