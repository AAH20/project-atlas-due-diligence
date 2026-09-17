# Atlas Agentic Due Diligence Benchmark — development pilot v0.1

By Apex Growth Systems LLC. Nine public synthetic arithmetic/evidence cases across tenant COGS, acquisition funding and infrastructure capacity, each with material, clean and insufficient-evidence variants. Two Kaggle SDK task adapters plus one engineering repair exercise. Python is the evaluation harness language; application stack is unchanged.

This pilot is separate from the [Season 1 competition](https://www.kaggle.com/competitions/frontier-due-diligence-challenge-season-1). Its rubric, required artifacts and awards are unchanged. Public answers prevent blind evaluation. No institutional realism, official Game Arena acceptance or frontier performance claim is made.

## Published Kaggle pilot

[Public suite](https://www.kaggle.com/benchmarks/ahmedalaahassan/atlas-agentic-due-diligence-development-pilot) · [Evidence task](https://www.kaggle.com/benchmarks/tasks/ahmedalaahassan/atlas-evidence-json-pilot) · [Staged task](https://www.kaggle.com/benchmarks/tasks/ahmedalaahassan/atlas-staged-investigation-pilot). Published 2026-09-18: two tasks, one model, Gemini 3.7 Flash 1.00 on each task. The evidence task was updated to v3 after separating notebooks; staged task is v1. These are development diagnostics, not official Game Arena rankings.

## Reproduce

```sh
python3 packages/atlas-benchmark/pilot.py
python3 -m unittest discover -s packages/atlas-benchmark -p 'test_*.py' -v
python3 packages/atlas-benchmark/pilot.py --predictions your-predictions.json
```

Predictions are a JSON array: `case_id`, `status`, `value`, `evidence_ids`. Missing cases fail; duplicates and unknown case IDs reject the submission. Margin is a fraction; gap/shortfall use synthetic units. Numerical tolerance is 1e-6. Case and document IDs include variant and evidence stage.

`results/reference.json` is an oracle-assisted harness self-check, not a model result. `results/replay.json` records staged actions and responses. Replay does not contain private software, documents or hidden model reasoning.

## Measurements and limits

Report classification, arithmetic, evidence completeness, invented citations, unseen citations and action count separately. Exact evidence IDs do not establish semantic entailment. Calibration, general PII protection, expert judgment, permissions beyond stage gating, real dollar cost and latency are not measured. Do not substitute missing telemetry with zero.

Kaggle task scores are case pass fractions, not the proposed institutional weighted rubric. Dynamic agents receive at most four actions, stage-filtered catalog, observed responses and no oracle. Reading future-stage evidence is denied and consumes an action. The harness rejects decisions citing unread evidence. It currently asks the model for JSON actions rather than using native tool calls. Eight-pass learning or memorizing public answers can still score well: this is an implementation diagnostic.

## Kaggle deployment

Create a task notebook at https://www.kaggle.com/benchmarks/tasks/new. Import `kaggle-evidence.ipynb` or `kaggle-dynamic.ipynb` from its public GitHub raw URL; each contains exactly one decorated task and invokes it. Kaggle publishes one task per notebook. The original combined `kaggle-pilot.ipynb` is retained as a development example, not the publication recipe. Alternatively place `pilot.py` and `kaggle_task.py` in its import path and explicitly select a single task. Inspect `list(kbench.llms.keys())` first. Retain all failed runs and output artifacts. Record SDK version and corpus hash, then publish the tested tasks and assemble them in a benchmark using Kaggle's UI. Engineering candidate execution belongs in a separately reviewed sandbox, not this notebook's unrestricted interpreter.

Evidence SDK integration was run live on Kaggle with Gemini 3.7 Flash: strict JSON fence parsing corrected an initial parser-induced 0/9 to 9/9 on one run. This is a simple public-case diagnostic, not a comparative leaderboard. Local tests use no providers. The initial pilot uses sequential prompts in one task chat; isolate case chats and freeze the context policy before model comparisons. Both tasks and the suite were built and public visibility verified in the account; model availability and quotas may change. No credentials are included.

## Next gate

Independently review structurally different cases across financial, legal, AI/IP, cyber, privacy, operations and commercial domains. Freeze a private evaluation release; document review/adjudication, alternative answers, materiality and leakage boundaries. Evaluate the same model under a fixed scaffold separately from full systems. Use repeated runs and case-family confidence intervals; retain denominators and failures. Validate citation support with qualified blinded reviewers.

Add interrupted tools, post-close monitoring, evidence changes requiring decision reversal, calibration and cost telemetry before a Game Arena proposal. Public contributions receive attribution for accepted cases, validators and reproducibility improvements; no investor recognition or contracts guaranteed.

## References

- [Kaggle Benchmarks documentation](https://www.kaggle.com/docs/benchmarks)
- [Official Kaggle SDK](https://github.com/Kaggle/kaggle-benchmarks)
- [Game Arena harness](https://github.com/google-deepmind/game_arena)
- [SWE-bench](https://github.com/swe-bench/SWE-bench)
- [SWE-Bench Pro paper](https://arxiv.org/abs/2509.16941)
- [UTBoost paper](https://openreview.net/pdf/b6452508eb507eff05a31e2504cb6fb7b03d7880.pdf)

SWE-Bench Pro and UTBoost are different extensions; this repository bundles neither their datasets nor scores. Only this new pilot and packages/atlas-benchmark are Apache 2.0; see LICENSE.md. Existing Atlas datasets retain their current terms.
