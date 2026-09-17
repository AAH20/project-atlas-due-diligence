# Evidence evolution v0.2 — public development diagnostic

A separate continuation of the Atlas benchmark pilot, licensed Apache 2.0 under the parent pilot license. Existing Atlas datasets and v0.1 published scores stay unchanged. No hidden institutional evaluation or official Game Arena inclusion is claimed.

Four opaque case IDs, twelve stage decisions: funding clean→material→clean; unknown→material→clean; clean→clean→clean control; material→unknown→clean after a funding confirmation is withdrawn. Each current document supersedes its predecessors. The runner passes only observed evidence/history to the model, never grades or future documents. Labels remain public, so this is not a leakage-resistant benchmark.

## Reproduce

```sh
python3 packages/atlas-benchmark/evolution.py
python3 -m unittest discover -s packages/atlas-benchmark -p 'test_*.py' -v
```

Import the standalone `kaggle-evolution.ipynb` into a **new** Kaggle benchmark task notebook. It contains one decorated task, one explicit live run and a result artifact `atlas-evolution-v0.2-results.json`. Do not replace the published v0.1 tasks. The SDK adapter uses documented `kbench.chats.new`: fresh chat per case/repetition, shared chat only within that case's evidence stages. The notebook fixes one repetition; local evaluator allows 1–10 with an explicit configuration.

## Measurements

- Exact classification/calculation/current evidence version: all must pass for a stage pass.
- Multiclass Brier score: sum of squared probability errors, range 0–2. Lower is better. This tiny sample cannot establish real-world calibration.
- Failed provider calls, malformed JSON and invalid probability distributions score failed stages, remain in the denominator and are recorded by error class.
- Wall latency per stage and available case-chat usage: input/output tokens, their costs in nanodollars, backend latency. Unavailable values are null. Case-chat usage is copied across stage rows for association; deduplicate by case/repetition before summing.
- Corpus hash, UTC start time, repetition, context policy and SDK version; actual model identity must come from Kaggle run metadata.

No metric measures semantic entailment, legal enforceability, investment decision utility, PII protection or expert realism. There are no case confidence intervals: four related funding trajectories are too narrow for an institutional comparison. Expand independent scenario families and expert review before generalizing.

## Contribution gate

Provide a fictional/publicly licensed scenario, timeline, versioned evidence, material/control/unknown variants, independently reproducible arithmetic, expected alternatives, evidence insufficiency conditions and reviewer rubric. Declare generated content and public answer exposure. Never contribute actual client/private transaction evidence. Accepted test/harness contributions receive public attribution; no funding, contracts or recognition by particular investors is promised.

Independent review is still needed. Use two qualified reviewers, record disagreements/adjudication and accepted alternative conclusions. Freeze reviewed cases before testing; keep future evidence, answers and generation seeds outside any agent-accessible held-out corpus. Publishing this development generator does not establish a private benchmark.
