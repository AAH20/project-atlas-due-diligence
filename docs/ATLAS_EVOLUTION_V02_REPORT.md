# Atlas evolution development report — 2026-09-18

Commands from public repository root:

- `python3 packages/atlas-benchmark/evolution.py`: PASS, four public trajectories/twelve stage decisions generated.
- `python3 -m unittest discover -s packages/atlas-benchmark -p 'test_*.py' -v`: PASS, 17 tests.
- Standalone notebook code compiled with Python `compile`: PASS.

Added fresh case/repetition context, evidence supersession and withdrawal, explicit probability distribution validation/Brier metric, failure-inclusive denominators, UTC/wall latency and nullable case-level SDK usage. Tests cover stale evidence, withdrawn funding, all-failed provider responses, repeat bounds and no oracle in prompts. SDK references checked against the official ci user guide on 2026-09-18.

Existing v0.1 tasks and Season 1 judging rules unchanged. Live Kaggle SDK 0.6.1 run completed 12/12 stage decisions, zero failed calls, pass fraction 1.0 and completed-stage Brier 0.0. Saved artifact corpus hash matches local corpus. Observed first-case chat usage: 1443 input tokens, 1034 output tokens, 1082250 input-cost nanodollars, 3877500 output-cost nanodollars, 4930ms backend latency. This is not the full run cost. Browser-transcribed summary is included separately from the Kaggle raw artifact. Task built as v1 and public visibility verified with Kaggle PUBLIC indicator and Successfully updated the visibility confirmation. URL: https://www.kaggle.com/benchmarks/tasks/ahmedalaahassan/atlas-evidence-evolution-v0-2 . Its parent notebook was also published; existing v0.1 suite was not edited. Full cost completeness, broad domains, scanned evidence, independent realism and semantic entailment remain unmeasured. No hidden-case generator or private software published. Game Arena proposal remains a draft, not an accepted collaboration or sent email.
