# ShyftR Phase D D1 simple baseline closeout

Date: 2026-05-20 07:40 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Verified HEAD: `e5a8a68`
Status: D1 is complete locally. No push, merge, clean-worktree state, service-comparator result, standard-dataset result, or public superiority claim is made.

## Roadmap anchor

D1 corresponds to the May 18 roadmap tranche:

```text
Phase D / D1 — Simple BM25/vector baseline proof
```

Roadmap contract: `2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md` lines 624-656.

D0 predecessor registry refresh:

- `docs/benchmarks/phase14-service-inventory.md`
- `docs/benchmarks/phase14-run-registry.md`

## Local baseline disclosure

This D1 proof intentionally carries the D0 dirty-baseline disclosure forward:

- current HEAD: `e5a8a68`
- branch: `main`
- branch state at D1 start: `main` ahead of `origin/main` by 1
- worktree status at D1 start: dirty
- dirty state included tracked Phase B/C/C3 implementation/doc/test changes and untracked phase artifacts

Interpretation: this is a local proof run from an explicitly disclosed dirty worktree. It is suitable for roadmap steering and D1 readiness, not for a clean published benchmark claim.

## D1 artifacts

Report produced:

- `reports/benchmarks/phaseD-simple-baseline-smoke.json`

Report readback evidence:

- report file exists
- run_id: `phaseD-simple-baseline-smoke`
- backend status counts: `ok: 3`
- included backends:
  - `shyftr`
  - `no-memory`
  - `simple-bm25`
- report has claim-limiting fields and aggregate cost/latency summary
- report includes runner-owned deterministic answer evaluation because `--enable-answer-eval` was used

## Verification commands

Focused D1 tests:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_simple_baseline.py tests/test_benchmark_adapter_contract.py
```

Observed result:

```text
......                                                                   [100%]
6 passed in 0.39s
```

D1 smoke report command, adapted to live CLI syntax (`--fixture`, `--top-k`) while preserving roadmap intent:

```bash
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture synthetic-mini \
  --run-id phaseD-simple-baseline-smoke \
  --output reports/benchmarks/phaseD-simple-baseline-smoke.json \
  --include-simple-bm25 \
  --top-k 1,3,5 \
  --enable-answer-eval
```

Observed readback:

```text
report exists reports/benchmarks/phaseD-simple-baseline-smoke.json bytes 24670
top keys ['aggregate_metrics', 'backend_results', 'claims_allowed', 'claims_not_allowed', 'dataset', 'fairness', 'generated_at', 'limitations', 'models', 'run_id', 'runner', 'schema_version']
backends ['shyftr', 'no-memory', 'simple-bm25']
run_id phaseD-simple-baseline-smoke
```

Backend readback:

```text
backend shyftr status ok
  config {'backend_name': 'shyftr'}
  metrics keys ['answer_eval', 'retrieval', 'retrieval_by_k']
backend no-memory status ok
  config {'backend_name': 'no-memory'}
  metrics keys ['answer_eval', 'retrieval', 'retrieval_by_k']
backend simple-bm25 status ok
  config {'backend_name': 'simple-bm25'}
  metrics keys ['answer_eval', 'retrieval', 'retrieval_by_k']
```

## Boundary preserved

D1 did not:

- run mem0 OSS, mem0 Cloud, Zep, Letta, LangGraph Store, or any service comparator
- use API keys or credentials
- download datasets
- run LongMemEval, LOCOMO-standard, or BEAM
- claim ShyftR beats any external memory system
- convert this local dirty-worktree run into a public benchmark claim

## D2 readiness

The next roadmap tranche is D2:

```text
D2. mem0 OSS comparator real local fixture run
```

Current D2 status: not executable yet on this machine because the D0/D1 import probe found `mem0` absent. D2 remains install/config-gated. The safe next action is to either:

1. explicitly approve local mem0 OSS dependency/config setup for a fixture-only run, or
2. keep mem0 skipped and create the D2 skipped-status closeout before moving to private standard-dataset gates.

## Canonical result

Phase D D1 is locally complete and verified.

The project is now ready for the next gated decision: D2 mem0 OSS setup/skip handling. It is not yet ready for service-comparator result claims or standard-dataset private runs without separate approval gates.
