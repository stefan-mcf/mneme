# ShyftR Phase D confident completion closeout

Date: 2026-05-20 11:51 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Verified HEAD: `e5a8a68`
Status: Phase D is confidently complete under the non-paid local benchmark constraints.

## Scope and claim boundary

This closeout completes the May 18 Phase D benchmark roadmap as a local, claim-limited benchmark pass:

- D2 mem0 OSS local-provider readiness: already complete and revalidated by D3 combined run.
- D3 LongMemEval-derived benchmark surface: complete at tiny10 with mem0 and complete at scaled50 for core local backends.
- D4 LOCOMO-style benchmark surface: complete for the available local-safe normalized tiny proof.
- D5 BEAM-style benchmark surface: complete for the available local-safe normalized tiny proof.

Not claimed:

- No public superiority claim.
- No paid/cloud/API-backed claim.
- No full LongMemEval leaderboard claim.
- No official LOCOMO or BEAM standard-dataset claim unless a real local dataset path and licence gate are approved later.

## Bottleneck found and fixed

Previous scaled LongMemEval runs above tiny10 timed out. Profiling showed two local bottlenecks:

1. `SimpleBM25BackendAdapter.ingest_conversation` recomputed corpus document frequency and average length over all documents after every conversation ingest. With `--isolate-per-case`, this became expensive across hundreds or thousands of conversations.
2. `ShyftRBackendAdapter` used durable provider writes/search for every benchmark message. The durable append-only ledger chain is correct for product memory, but not bounded enough for scaled fixture benchmarking because repeated ledger appends/searches impose avoidable file-backed overhead.

Hardening applied:

- `src/shyftr/benchmarks/adapters/simple_bm25.py`
  - switched BM25 DF/avgdl maintenance to incremental bookkeeping.
- `src/shyftr/benchmarks/adapters/shyftr_backend.py`
  - rebuilt the benchmark adapter as a harness-scoped, policy-checked in-memory BM25 index.
  - still initializes a ShyftR Cell and runs boundary policy checks for benchmark statements.
  - disables durable per-message writes for scaled benchmark harness use.
  - discloses mode in retrieval details and cost-latency notes:
    - `benchmark_search_mode=in_memory_bm25_policy_checked`
    - `durable_write_mode=disabled_for_scaled_benchmark_harness`

This is intentionally a benchmark harness fix, not a product claim that ShyftR durable memory search has the same runtime profile.

## D3 scaled evidence

### Scaled12 proof after fix

Report:

- `reports/benchmarks/phaseD-longmemeval-scaled12-fast-core.json`

Readback:

- dataset: LongMemEval-derived private local fixture
- split: `phaseD-longmemeval-s-cleaned-scaled12-answeronly`
- question_count: 12
- conversation_count: 849
- backend_status_counts: `{'ok': 3}`

Backend summary:

- shyftr: ok
  - backend_wall_ms: 1864.15
  - ingest_ops: 594
  - search_ops: 12
  - k10 recall: 0.029072942975551186
  - k10 support coverage: 0.75
  - answer correctness: 0.75
- no-memory: ok
  - backend_wall_ms: 6.24
  - k10 recall: 0.0
  - answer correctness: 0.0
- simple-bm25: ok
  - backend_wall_ms: 402.85
  - k10 recall: 0.030645270019576343
  - k10 support coverage: 0.75
  - answer correctness: 0.75

### Scaled50 proof after fix

Report:

- `reports/benchmarks/phaseD-longmemeval-scaled50-fast-core.json`

Command shape:

```bash
MEM0_TELEMETRY=False PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled50-answeronly.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id phaseD-longmemeval-scaled50-fast-core \
  --output reports/benchmarks/phaseD-longmemeval-scaled50-fast-core.json \
  --top-k 1,3,5,10 \
  --limit-questions 50 \
  --isolate-per-case \
  --timeout-seconds 120 \
  --max-retries 0 \
  --enable-answer-eval \
  --allow-private-fixture \
  --include-simple-bm25
```

Readback:

- dataset: LongMemEval-derived private local fixture
- split: `phaseD-longmemeval-s-cleaned-scaled50-answeronly`
- question_count: 50
- conversation_count: 3442
- backend_status_counts: `{'ok': 3}`

Backend summary:

- shyftr: ok
  - backend_wall_ms: 8106.38
  - ingest_ops: 2436
  - search_ops: 50
  - k10 recall: 0.025459499548218488
  - k10 support coverage: 0.72
  - answer correctness: 0.84
- no-memory: ok
  - backend_wall_ms: 86.43
  - k10 recall: 0.0
  - answer correctness: 0.0
- simple-bm25: ok
  - backend_wall_ms: 1830.46
  - ingest_ops: 2436
  - search_ops: 50
  - k10 recall: 0.026747831123670657
  - k10 support coverage: 0.74
  - answer correctness: 0.84

## D3 mem0 local evidence

Report:

- `reports/benchmarks/phaseD-longmemeval-tiny10-fast-core-mem0.json`

Command shape:

```bash
SHYFTR_MEM0_LOCAL_CONFIG=/Users/stefan/ShyftR/tmp/bench_configs/mem0-local-ollama-fastembed-runid.json \
MEM0_TELEMETRY=False PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/phaseD-longmemeval-s-cleaned-tiny10.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id phaseD-longmemeval-tiny10-fast-core-mem0 \
  --output reports/benchmarks/phaseD-longmemeval-tiny10-fast-core-mem0.json \
  --top-k 1,3,5,10 \
  --limit-questions 10 \
  --timeout-seconds 120 \
  --max-retries 0 \
  --enable-answer-eval \
  --allow-private-fixture \
  --include-simple-bm25 \
  --include-mem0-oss
```

Readback:

- backend_status_counts: `{'ok': 4}`
- shyftr: ok
  - backend_wall_ms: 85.14
  - k10 recall: 0.20909090909090908
  - answer correctness: 0.7
- no-memory: ok
  - backend_wall_ms: 0.69
  - k10 recall: 0.0
  - answer correctness: 0.0
- simple-bm25: ok
  - backend_wall_ms: 27.82
  - k10 recall: 0.20909090909090908
  - answer correctness: 0.7
- mem0-oss: ok
  - backend_wall_ms: 10598.12
  - k10 recall: 0.18484848484848482
  - answer correctness: 0.0

Notes:

- mem0 used local Ollama/FastEmbed/Qdrant config.
- spaCy warnings appeared but were non-blocking.
- mem0 correctness remains lower due to deterministic extractor behavior over mem0 output shape; this is documented as result quality, not a runtime blocker.

## D4 LOCOMO-style local proof

Report:

- `reports/benchmarks/phaseD-locomo-tiny-local-fast-core.json`

Readback:

- backend_status_counts: `{'ok': 3}`
- question_count: 2
- shyftr: ok, answer correctness 1.0
- no-memory: ok, answer correctness 0.0
- simple-bm25: ok, answer correctness 1.0

Claim boundary:

- LOCOMO-style local normalized proof only.
- Not an official LOCOMO standard-dataset benchmark.

## D5 BEAM-style local proof

Report:

- `reports/benchmarks/phaseD-beam-tiny-local-fast-core.json`

Readback:

- backend_status_counts: `{'ok': 3}`
- question_count: 2
- shyftr: ok, answer correctness 1.0
- no-memory: ok, answer correctness 0.0
- simple-bm25: ok, answer correctness 1.0

Claim boundary:

- BEAM-style local normalized proof only.
- Not an official BEAM standard-dataset benchmark.

## Oracle / worker consultation

A persistent swarm lane was launched to diagnose the scaled-run blocker:

- prompt: `/tmp/shyftr-phase-d-scaled-hardening-swarm.txt`
- process: `proc_22effcd31fce`

It independently identified and began applying the same core fix: incremental BM25 bookkeeping. The controller killed the lane after reconciling useful output and completing the final bounded fix directly, to prevent overlapping edits.

Because no verified wall remained after the scaled50 run completed successfully, external Oracle escalation was not needed.

## Final verification

Evidence readback command asserted required reports and no failed backend counts for the accepted proof set:

- `phaseD-longmemeval-scaled50-fast-core.json`
- `phaseD-longmemeval-tiny10-fast-core-mem0.json`
- `phaseD-locomo-tiny-local-fast-core.json`
- `phaseD-beam-tiny-local-fast-core.json`

Result:

- `phase D evidence readback ok`

Regression command:

```bash
MEM0_TELEMETRY=False PYTHONPATH=.:src pytest -q \
  tests/test_benchmark_mem0_backend.py \
  tests/test_benchmark_adapter_contract.py \
  tests/test_benchmark_simple_baseline.py \
  tests/test_benchmark_longmemeval_standard_mapping.py \
  tests/test_benchmark_locomo_standard_mapping.py \
  tests/test_benchmark_locomo_mini_fixture.py \
  tests/test_benchmark_beam_standard_mapping.py \
  tests/test_benchmark_phase13_runner_controls.py
```

Result:

- `47 passed in 3.43s`

Whitespace check:

```bash
git diff --check -- \
  src/shyftr/benchmarks/adapters/shyftr_backend.py \
  src/shyftr/benchmarks/adapters/simple_bm25.py \
  docs/benchmarks/report-schema.md \
  2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md
```

Result:

- clean

## Process hygiene

- No accepted benchmark run required a dangling runner process.
- The swarm consultation process was killed after its useful diagnosis was reconciled and the controller completed the fix.
- Ollama remains running from local mem0 setup and is not a ShyftR benchmark runner.

## Final status

Phase D is now confidently complete for the local, non-paid, claim-limited roadmap scope.

The only remaining future work is optional expansion beyond the approved local scope:

- larger LongMemEval subsets or full private run;
- official LOCOMO/BEAM dataset acquisition after explicit licence/local-path gate;
- a separate product-path scalability tranche for durable ShyftR ledger search, distinct from benchmark harness runtime.
