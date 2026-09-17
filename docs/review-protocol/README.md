# Atlas independent case-review workflow v0.3

This workflow prepares expert review of the existing 36 public v0.2 exercises in 12 domains. It does not introduce new competition rules, convert public labels into unseen tests, authenticate reviewer credentials, or certify investment/legal accuracy. There are currently **zero submitted expert reviews** and **zero accepted cases** in this review release.

## Packet preparation

From repository root:

```sh
python3 packages/atlas-benchmark/review_gate.py export datasets/project-atlas/v0.2 ../organizer-evaluation/review-v0.3
python3 packages/atlas-benchmark/review_gate.py check ../organizer-evaluation/review-v0.3
```

The second command reports pending review without treating pending as a software failure. `freeze` is the fail-closed release action.

The prepared local directory sits outside the public Git repository. It contains `manifest.json`, one opaque-ID packet per case, `organizer-mapping.json`, and initially empty reviews/profiles/adjudications arrays. Export refuses an existing target; use a different release directory for changed evidence. Packet IDs use a random export salt so another export has different IDs. The manifest pins packet hashes, rubric hash and source-file hashes.

Share only the case packets and rubric with assigned reviewers. Do not initially share the organizer mapping or author labels. Packets remove original document/case IDs and omit author answers; original evidence quotes, domains, stages and line locators remain. This masks labels/identity in the packet, but a reviewer may recognize the publicly available exercise. Reviewers must disclose prior answer exposure. Sharing requires explicit recipient authorization; this build has sent nothing to anyone.

Derived packets remain governed by the Atlas dataset license. Only the new review-gate code under packages/atlas-benchmark is Apache 2.0. Copying existing dataset excerpts into a packet does not relicense them.

## Independent reviewer assignment

Each case needs exactly two different reviewers, qualified in its domain and independent of its authorship. Verify identity, relevant experience and conflicts outside this software. Record the verification reference and qualified domains in `reviewers.json`. Do not store identity documents, CVs or private contact details in the public repository. A Boolean in a JSON file is an organizer attestation, not authentication of expertise.

Manifest domains: concentration, cyber, earnings, funding, governance, gpu, ip, offtake, power, privacy, revenue and title. Suggested expertise: revenue/earnings—transaction accounting; funding—financing; power/GPU/network—engineering and infrastructure operations; AI data/IP/privacy—appropriate technical and legal specialists; consent/contracts—transaction counsel; cyber—security assessment; other domains—matching specialist expertise. Use the manifest's exact domain names in profiles. Cross-domain cases may need additional specialist consultation, but the protocol still requires a documented final two-reviewer pair. Never discard adverse reviews to cherry-pick two favorable ones; record new review rounds as a new release.

The code checks one reviewer per case, verified expertise references, matching domain, independence and declared absence of conflict. It rejects more than two reviews instead of choosing a favorable pair. Conflicted reviewers must recuse, not merely lower a score. Review records remain local unless reviewers consent to publication of their identities and work.

## Case-quality rubric

Rate every criterion 0–4: 0 unusable/unsupported; 1 major gaps; 2 partial support/revisions needed; 3 supported with explicit limits; 4 fully supported and useful within the stated scope.

| Criterion | Review question |
|---|---|
| Evidence sufficiency | Can a reviewer reproduce the conclusion or determine that evidence is insufficient? |
| Materiality clarity | Are relevance, thresholds and the distinction between a discrepancy and proven loss clear? |
| Answer resolvability | Are units, dates, entities, conditions and expected answer boundaries unambiguous? |
| Alternative answers | Does the case accept defensible conclusions/escalations and avoid punishing appropriate uncertainty? |
| Domain realism | Is the synthetic scenario coherent enough for the proposed narrow evaluation? |

Determine `material`, `clean` or `insufficient_evidence` independently. `clean` means no material issue established within supplied evidence, not a general warranty of the company. Missing documents are not proof of misconduct. Record required evidence, acceptable alternative answers, critical defects and rationale. Legal/accounting conclusions may require full executed instruments, governing jurisdiction, policies and specialist interpretation missing from these short fixtures; flag such gaps rather than inventing certainty.

An accepted case requires all criteria at least 3, verdict accept, no unresolved critical defects, qualified independent review and resolved disagreements. Do not average away a failed criterion. Scores are a proposed release policy, not empirical proof that the threshold guarantees professional adequacy.

## Disagreement and adjudication

Different conclusions, verdicts, evidence sets, alternative-answer sets, critical defects or a criterion gap greater than one require adjudication. Exact text differences in alternative answers can trigger review even when semantically similar; the independent adjudicator resolves that rather than an LLM silently choosing a winner.

The third adjudicator must be qualified, independent of authoring and different from both original reviewers. Its final review references the exact hashes of both source reviews, includes rationale, acceptable answers and all rubric scores. The release retains original reviews. Gate output reports complete-pair conclusion agreement and mean absolute criterion differences; with no pairs, those values are null. These are descriptive checks, not reliability estimates or proof of reviewer qualification. A revised packet invalidates all old review hashes and needs a new release/review round.

Templates are unfilled examples, not valid completed reviews. Unit tests use simulated records only and never count as expert reviews.

## Freeze and integrity

```sh
python3 packages/atlas-benchmark/review_gate.py freeze ../organizer-evaluation/review-v0.3
```

This fails until all cases pass. It writes FROZEN_REVIEW.json exclusively, retaining hashes of manifest, review set, profiles and adjudications. `check` verifies packet integrity and detects subsequent changes to a frozen report or its inputs. This is local content integrity, not a cryptographic signature service or access-control system; protect the release and retain original reviewer attestations externally.

`case_quality_ready` is separate from `held_out_benchmark_ready`, which this workflow always sets false because the source exercises/answers are public. Independent case validation alone does not establish blind agent measurement, broad institutional realism or validated investment decisions.

Before stronger claims: independently author structurally different private cases, obtain domain review, freeze evaluation configuration/cases before running agents, preserve leakage boundaries, measure reviewer agreement and disagreements, test supported alternatives, and report failures/costs/uncertainty. Do not retroactively alter current Season 1 grading.

## Method references

The workflow is an Atlas-specific proposed protocol. [HELM](https://crfm.stanford.edu/2022/11/17/helm.html) motivates transparent, multidimensional evaluation; it does not validate Atlas's chosen thresholds. [SWE-bench](https://www.swebench.com/) provides software-task evaluation and a human-filtered Verified subset; it does not establish diligence expertise or endorse this workflow.
