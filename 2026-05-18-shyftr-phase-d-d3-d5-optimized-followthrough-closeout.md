# ShyftR Phase D optimized D3-D5 follow-through closeout

Date: 2026-05-20 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Verified HEAD: `e5a8a68`
Status: optimized follow-through completed for the four requested next steps where bounded local execution was feasible. D3 tiny10 now has mem0 full-top-k and combined core+mem0 reports. D4/D5 have smallest local private proof fixtures and reports. D3 50-question scaling was attempted and converted, but the current runner/backend path is not yet bounded enough for 50-question LongMemEval-derived execution; that is now a documented scaling blocker rather than an untried next step.

## Scope and boundary

User approval: proceed optimally, complete the best next steps, harden/optimize ShyftR as work proceeds, document everything.

Boundaries preserved:

- non-paid local only;
- no API keys or cloud services;
- no mem0 Cloud;
- no public benchmark/superiority claims;
- private/local reports only;
- no full LongMemEval run;
- no standard LOCOMO/BEAM dataset claim.

## Swarm lane

Persistent swarm review lane:

```text
profile: swarm3
process session: proc_f116d73f2d00
swarm session: 20260520_102014_aa76f4
status: exited 0
mode: read-only review
```

Swarm findings applied/verified by controller:

- scaled D3 runs must keep `--isolate-per-case` and unique run IDs;
- CLI docs should use `--top-k`, not stale `--top-k-cutoffs`;
- D4/D5 should start with smallest local/private normalized proofs;
- report schema needed explicit license/attribution/source metadata before D5 closeout.

## Step 1 — D3 tiny10 mem0 full top-k

Report:

```text
reports/benchmarks/phaseD-longmemeval-tiny10-mem0-topk13510.json
```

Command shape:

```bash
SHYFTR_MEM0_LOCAL_CONFIG=tmp/bench_configs/mem0-local-ollama-fastembed-runid.json \
MEM0_TELEMETRY=False \
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/phaseD-longmemeval-s-cleaned-tiny10.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id phaseD-longmemeval-tiny10-mem0-topk13510 \
  --output reports/benchmarks/phaseD-longmemeval-tiny10-mem0-topk13510.json \
  --top-k 1,3,5,10 \
  --limit-questions 10 \
  --isolate-per-case \
  --timeout-seconds 120 \
  --max-retries 0 \
  --enable-answer-eval \
  --allow-private-fixture \
  --include-mem0-oss \
  --include-retrieval-details
```

Readback:

```text
backend_status_counts: {'ok': 3}
backends: shyftr ok, no-memory ok, mem0-oss ok
mem0 backend_wall_ms: 13309.869416989386
mem0 ingest_ms: 635.1274159387685
mem0 search_ms_total: 5.25058398488909
mem0 retrieval.question_count: 10
mem0 retrieval.recall_at_k: 0.6848484848484849
mem0 retrieval.precision_at_k: 0.21999999999999997
mem0 retrieval.answer_support_coverage: 1.0
mem0 answer_eval.correctness: 0.0
mem0 answer_eval.abstention_rate: 1.0
```

Result: completed. mem0 is now bounded and `ok` across all intended tiny10 cutoffs.

## Step 2 — D3 tiny10 combined core + mem0 full top-k

Report:

```text
reports/benchmarks/phaseD-longmemeval-tiny10-core-mem0-topk13510.json
```

Readback:

```text
backend_status_counts: {'ok': 4}
backends: shyftr ok, no-memory ok, simple-bm25 ok, mem0-oss ok
```

Key metrics:

```text
shyftr:
  recall_at_k: 0.23333333333333334
  precision_at_k: 0.07
  answer_support_coverage: 0.4
  answer_eval.correctness: 0.6

no-memory:
  recall_at_k: 0.0
  precision_at_k: 0.0
  answer_eval.correctness: 0.0

simple-bm25:
  recall_at_k: 0.7090909090909091
  precision_at_k: 0.22222222222222224
  answer_support_coverage: 1.0
  answer_eval.correctness: 0.7

mem0-oss:
  recall_at_k: 0.6848484848484849
  precision_at_k: 0.21999999999999997
  answer_support_coverage: 1.0
  answer_eval.correctness: 0.0
  answer_eval.abstention_rate: 1.0
```

Result: completed. This is the strongest private tiny10 D3 comparison so far, with all local comparators at `ok`.

## Step 3 — D3 50-question private subset

Created fixtures:

```text
artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled50.fixture.json
artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled50.fixture.json.manifest.json
artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled50-answeronly.fixture.json
artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled50-answeronly.fixture.json.manifest.json
```

Manifest summaries:

```text
scaled50 case-group subset:
  case_count: 50
  session_count: 2436
  message_count: 25024
  sha256: 4080aa1838ab8904cac2d968296c455f8d28dd044036b0fd6edba031b4c402b4

scaled50 answer-session-only diagnostic subset:
  case_count: 50
  session_count: 3442
  message_count: 35023
  sha256: 9f2e8e066cb3447cc997d1f90dba82f9371d81573b611698c606d505be7fb225
```

Attempted runs:

```text
phaseD-longmemeval-scaled50-core
  status: killed after repeated waits; no report accepted
  reason: still running after ~7 minutes; bounded execution stop

phaseD-longmemeval-scaled50-bm25
  status: command timeout after 600s
  reason: runner/backend path not bounded enough for this subset

phaseD-longmemeval-scaled50-answeronly-bm25
  status: killed after repeated waits; no report accepted
  reason: still running after ~2 minutes; bounded execution stop
```

Additional downscale diagnostics:

```text
scaled20 answeronly:
  fixture created: artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled20-answeronly.fixture.json
  run status: timeout after 600s

scaled12 answeronly:
  fixture created: artifacts/benchmarks/phaseD-longmemeval-s-cleaned-scaled12-answeronly.fixture.json
  run status: timeout after 600s
```

Result: converted and attempted, but not runtime-complete. This is now a verified scaling blocker: LongMemEval-derived runs above tiny10 need runner/backend scaling work before 50-question execution is honest. The blocker is not dataset availability; it is runtime boundedness.

## Step 4 — D4/D5 smallest local private proofs

### D4 LOCOMO tiny local proof

Input:

```text
tmp/external_datasets/locomo/locomo_tiny_local.json
```

Converted fixture:

```text
artifacts/benchmarks/phaseD-locomo-tiny-local.fixture.json
artifacts/benchmarks/phaseD-locomo-tiny-local.fixture.json.manifest.json
```

Report:

```text
reports/benchmarks/phaseD-locomo-tiny-local-core.json
```

Readback:

```text
dataset.name: locomo-standard
dataset.version: local-normalized-tiny/v0
dataset.split: locomo-tiny-local
dataset.question_count: 2
dataset.conversation_count: 2
backend_status_counts: {'ok': 3}
backends: shyftr ok, no-memory ok, simple-bm25 ok

shyftr correctness: 1.0
no-memory correctness: 0.0
simple-bm25 correctness: 1.0
```

Interpretation: smallest local normalized LOCOMO-style proof completed. This is not a standard LOCOMO run.

### D5 BEAM tiny local proof

Input:

```text
tmp/external_datasets/beam/beam_tiny_local.json
```

Converted fixture:

```text
artifacts/benchmarks/phaseD-beam-tiny-local.fixture.json
artifacts/benchmarks/phaseD-beam-tiny-local.fixture.json.manifest.json
```

Report:

```text
reports/benchmarks/phaseD-beam-tiny-local-core.json
```

Readback:

```text
dataset.name: beam-standard
dataset.version: local-normalized-tiny/v0
dataset.split: beam-tiny-local
dataset.question_count: 2
dataset.conversation_count: 2
backend_status_counts: {'ok': 3}
backends: shyftr ok, no-memory ok, simple-bm25 ok

shyftr correctness: 1.0
no-memory correctness: 0.0
simple-bm25 correctness: 1.0
```

Interpretation: smallest local normalized BEAM-style proof completed with synthetic local data and private-only handling. This is not BEAM benchmark data and does not trigger a public BEAM claim.

## Hardening applied

### mem0 adapter

File:

```text
src/shyftr/benchmarks/adapters/mem0_backend.py
```

Current behavior:

- uses mem0 v2 chat-style add payloads;
- uses `infer=False` for bounded fixture-safe ingestion;
- uses `search(query, filters={"user_id": run_id}, top_k=top_k)`;
- preserves older search fallbacks;
- keeps explicit local config and credential refusal.

### Report schema docs

File:

```text
docs/benchmarks/report-schema.md
```

Added dataset metadata fields:

```text
license_id
license_text
attribution
source_url
source_commit
claim_limit
```

Purpose: D5 BEAM and future licensed benchmark summaries now have a documented report surface for attribution and source/license metadata.

### Roadmap command correction

File:

```text
2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md
```

Changed stale command examples from:

```text
--top-k-cutoffs
```

to the real runner flag:

```text
--top-k
```

## Verification

Regression tests:

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

Observed:

```text
47 passed in 3.66s
```

Docs assertions:

```text
report schema contains license_id, attribution, source_url
roadmap no longer contains --top-k-cutoffs
docs assertions passed
```

Whitespace check:

```bash
git diff --check -- \
  src/shyftr/benchmarks/adapters/mem0_backend.py \
  src/shyftr/benchmarks/adapters/shyftr_backend.py \
  docs/benchmarks/report-schema.md \
  2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md \
  tests/test_benchmark_mem0_backend.py
```

Observed: clean.

## Process hygiene

No ShyftR benchmark/swarm worker from this pass remained running at closeout. Ollama remains running from D2 setup. A separate unrelated portfolio-site swarm lane was visible and was not touched.

## Current Phase D state

Completed:

1. D3 tiny10 mem0 full top-k `ok`.
2. D3 tiny10 combined ShyftR/no-memory/simple-bm25/mem0 full top-k `ok`.
3. D3 50-question private subset conversion + bounded execution attempts, with runtime blocker proven.
4. D4 LOCOMO-style smallest local proof `ok`.
5. D5 BEAM-style smallest local proof `ok`.
6. Report schema and roadmap docs hardened for license/top-k correctness.

Still blocked / next hardening target:

- D3 scaled LongMemEval-derived runs above tiny10 require runner/backend optimization before 50-question proof can complete. Suggested next engineering path:
  - add progress logging/checkpointing for long benchmark runs;
  - profile ShyftR and BM25 ingestion/search on scaled12/scaled20 answer-only fixtures;
  - add a no-answer-eval/no-retrieval-details scaled smoke mode;
  - only then retry scaled50.

Canonical result: Phase D is substantially advanced through D5 local proof surfaces, but scaled D3 remains blocked by runtime boundedness rather than missing data or approval.
