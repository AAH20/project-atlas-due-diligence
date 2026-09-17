# Atlas evolution development report — 2026-09-18

Commands from public repository root:

- `python3 packages/atlas-benchmark/evolution.py`: PASS, four public trajectories/twelve stage decisions generated.
- `python3 -m unittest discover -s packages/atlas-benchmark -p 'test_*.py' -v`: PASS, 17 tests.
- Standalone notebook code compiled with Python `compile`: PASS.

Added fresh case/repetition context, evidence supersession and withdrawal, explicit probability distribution validation/Brier metric, failure-inclusive denominators, UTC/wall latency and nullable case-level SDK usage. Tests cover stale evidence, withdrawn funding, all-failed provider responses, repeat bounds and no oracle in prompts. SDK references checked against the official ci user guide on 2026-09-18.

Existing v0.1 tasks and Season 1 judging rules unchanged. New v0.2 SDK task requires live execution validation before any measured model claims. Full cost completeness, broad domains, scanned evidence, independent realism and semantic entailment remain unmeasured. No hidden-case generator or private software published. Game Arena proposal remains a draft, not an accepted collaboration or sent email.
