# Engineering repair exercise E001

Fix `candidate.py`: identical duplicate invoices must count once; conflicting invoices and orphan receipts must raise ValueError; cash equals receipts, not recognized revenue. Preserve `reconcile(invoices, receipts)`. Inputs use integer synthetic units, invoice IDs and receipt invoice IDs. Public contract tests and reference implementation in `pilot.py` are teaching materials.

This is inspired by issue→patch→test evaluation. It is not an official SWE-bench task, SWE-bench score, or concealed test suite. Further tasks (redaction, access enforcement, evidence-version joins) and independently authored hidden tests are required before an engineering leaderboard.

Do not execute submitted code on a host with secrets. In a disposable offline container, with Docker already installed and the official Python image obtained, run:

```sh
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges --pids-limit 64 --memory 256m --cpus 1 --user 65534:65534 --tmpfs /tmp:rw,noexec,nosuid,size=16m -v "$PWD/packages/atlas-benchmark/engineering:/work:ro" -w /work python:3.12-slim timeout 20 python -B -m unittest discover -p 'test_contract.py'
```

The supplied candidate deliberately fails three of four tests. Replace it only in your disposable evaluation copy. Pin the image digest and sandbox policy in any reported run. This command is provided, not a claim of tested production isolation.
