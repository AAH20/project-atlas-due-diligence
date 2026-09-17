# Atlas v0.2 evidence interface

Status: portable evidence interface specification, not a live API. This release contains synthetic data, fixture utilities and evaluation documentation.

## Record collections

All JSON arrays use stable `id` identifiers except financial statement natural keys `(entity_id, period)` and journal IDs. `entities`, `assets`, `relationships`, `documents_and_versions`, `evidence_passages`, `financial_facts`, `obligations_and_milestones`, `findings`, `review_decisions` and `change_events` are supplied. Money uses named integer-cent or integer-USD fields; do not mix units. Dates use ISO calendar dates; released stage is T0–T4.

`financial_facts` contains three forward compute-pool economics scenarios. It is separate from historical accounts and from the 36 self-contained domain exercises. Those exercises intentionally contain conflicting representations; they are not entries in the historical journal. The mandate EV-to-equity bridge is illustrative and also separate from historical book valuation. Do not treat these three scopes as one reconciled valuation model.

## Proposed adapter operations

| Operation | Input | Required result |
|---|---|---|
| ingest | authenticated workspace, tenant, release, document, digest, source role scope | immutable version; verified digest; duplicate handling |
| retrieve | authenticated role, released stage, document/evidence IDs | only permitted released evidence; deny on missing/invalid scope |
| propose finding | claim, exact evidence IDs, calculation, uncertainty, affected records | pending finding; no automatic approval or external disclosure |
| review | authorized reviewer identity, finding ID, decision, rationale | append-only review event and recorded approval state |
| update | newly released source version and supersedes link | reevaluate dependent findings; retain history and unresolved risks |
| export | audience role, approved findings, cut-off stage | permission-filtered packet with source/version citations |

Implementations must preserve the evidence identifiers and version history. References must remain resolvable after ingestion.

## Access and leakage

`reference.mjs` is a local fixture simulator, not a production authorization service. Anyone with the dataset files can read every file, future stage and public answer. To run a blind staged exercise, an external runner must construct a separate role/stage-filtered corpus and omit worked answers, future-stage manifest entries, reference outputs and future documents. Never mount the full public package in an agent's sandbox and call it permission-isolated.

Permissions must filter retrieval, summaries, exports, logs and cached outputs. A denied fetch must not disclose content or return a snippet from a restricted source. Embedded document instructions have no authority. Exact-string redaction is only a known-fixture demonstration, not general PII detection or anonymization.

## Implementation acceptance

1. Verify document checksums and exact evidence passage locators.
2. Preserve stable IDs and supersedes relationships.
3. Prove buyer cannot retrieve lender-only terms, engineering cannot retrieve financial timeline, and T0 cannot retrieve T4.
4. Report the five timeline outcomes accurately; improved funding must not clear the deployment delay.
5. Export findings with evidence/version, uncertainty and reviewer state.
6. Use approved confidential-document processing providers only; do not transmit private client data during this synthetic exercise.

## Implementation limits

Authenticated production permission enforcement, ingestion jobs, entity resolution, agent orchestration, human review interfaces and live change monitoring are not implemented in this dataset release.
