# Atlas benchmark pilot build report — 2026-09-18

Public development release; no frontier model scores or Game Arena acceptance claimed. Season 1 unchanged.

Commands executed from repository root:

- `python3 packages/atlas-benchmark/pilot.py`: PASS, nine public cases and reference/replays generated.
- `python3 -m unittest discover -s packages/atlas-benchmark -p 'test_*.py' -v`: PASS initially 9 tests; parser regression brings total to 10 passing tests.
- `python3 -m py_compile packages/atlas-benchmark/kaggle_task.py`: PASS, syntax only; SDK not installed locally.
- Engineering verification: copied provided candidate and public contract to a temporary directory; `python3 -B -m unittest discover` failed 3 of 4 intentionally. Replaced temporary candidate with `inspect.getsource(pilot.reconcile)`; same command passed 4 of 4. No participant code executed.
- `git diff --check`: PASS.

Kaggle signed-in task notebook created. Local notebook upload stalled at Loading file; importing the public GitHub raw notebook succeeded. Live Gemini 3.7 Flash first scored 0/9 because of JSON fences; corrected strict fence parsing scored 9/9 on one run. `%choose atlas_evidence_json` retained task/run artifacts; Build Task started. Dynamic adapter live run and public benchmark suite remain pending. This is a public arithmetic fixture diagnostic, not frontier performance. Docker isolation command is documented but not executed.

References: official Kaggle SDK user guide on branch `ci` checked for decorated task, float return scoring and `llm.prompt`; custom Game Arena inclusion requires a separate Kaggle collaboration process.
