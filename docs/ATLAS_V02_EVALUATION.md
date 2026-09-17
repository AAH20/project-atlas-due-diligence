# Atlas v0.2 evaluation design

This is a development diagnostic, not a replacement for the published Season 1 rubric. Dataset expansion is optional. No undisclosed mandatory organizer grading is introduced.

## Public cases

36 self-contained case exercises: material, clean/control and insufficient-evidence variants in 12 domains. Labels and required evidence IDs are public. Excerpts are short teaching fixtures; not full executed contracts, statutory accounts, scanned PDFs or independently realistic transaction evidence. The five-stage timeline tests dependency updates separately.

## Prediction format

Submit a JSON array conforming to `schemas/predictions.schema.json`. One entry per case: `case_id`, status (`material`, `clean`, `insufficient_evidence`), `evidence_ids`, plus optional explanation, calculation and review request. Missing cases count against coverage, accuracy and recall. Duplicate or unknown cases fail validation. Citations from another case may have valid IDs but do not satisfy that case's required evidence.

Run `node packages/atlas-expansion/score.mjs predictions.json result.json`. The scorer measures status accuracy, material recall, false material flags, citation-ID validity and required-evidence coverage. It does NOT evaluate semantic entailment, full textual answer quality, severity or investment judgment. Public author labels are not independent truth.

## Timeline expected outcomes

| Stage | Deployment delay | Funding gap | Energization past offtake threshold |
|---|---:|---:|---|
| T0 | 0 days | $0 | No |
| T1 | 92 days | $0 | Yes |
| T2 | 92 days | $10m | Yes |
| T3 | 92 days | $10m | No |
| T4 | 92 days | $0 | No |

Dates are conditional scenario inputs; a target date is not evidence of actual energization. The off-take Boolean compares dates, not a legal enforceability judgment. Financing arithmetic counts only stated available amounts and does not independently prove their availability.

## Human review rubric (future institutional study)

Qualified reviewers should assess each finding with a 0–4 ordinal scale: unsupported (0), weak/incomplete (1), partially supported (2), supported with limitations (3), fully supported and decision-useful (4). Review evidence sufficiency, calculation reproducibility, materiality, appropriate uncertainty, specialist escalation, correct dependency interpretation and update correctness separately. Do not average away a permission breach: record it as a failed safety gate.

Use at least two independent reviewers; record expertise, blinded comparisons, disagreements, adjudication and accepted alternative answers. Keep initial labels separate from reviewer-approved labels. Set materiality and review instructions before evaluation. Compare the same evidence, stage, role, time budget and cost budget for every system. Human baseline measurement requires consent and actual timed work.

## Measured execution log

Record system/version, prompt/config hashes, model/provider, allowed corpus digest, case, role, stage, start/end UTC, tool actions, approved disclosures, token counts, actual cost and reviewer minutes. Missing telemetry is `unmeasured`, never zero. Distinguish provider usage COGS from support labor and infrastructure cost. Report distributions, case counts and limitations; do not invent frontier rankings or investor endorsement.

## Organizer candidates

Twelve composite funding exercises and their generator/answers are stored outside the public monorepo under `organizer-evaluation/v0.2`. They have different evidence layout and values, but limited domain diversity and no independent adjudication. They are local evaluation candidates, not an established held-out institutional benchmark. No answers or generator should be uploaded publicly. Before an institutional study, obtain expert review and add structurally different cases across domains; freeze the benchmark before testing.
