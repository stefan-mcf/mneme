# ShyftR Phase D D3 mem0 OSS optimization closeout

Date: 2026-05-20 10:13 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Verified HEAD: `e5a8a68`
Status: D3 mem0 OSS is now bounded enough for LongMemEval-derived local runs. A 10-question tiny10 mem0 OSS run completed with `status=ok` under the non-paid local stack.

## Active objective

The prior D3 closeout left this gap:

```text
mem0 OSS remains proven on D2 fixture, but mem0 LongMemEval dry-run did not finish within practical local-run time and needs a separate smaller/optimized lane before scaled D3.
```

This closeout addresses that gap.

## Swarm lane

Persistent swarm lane launched per `proceed optimally` routing:

```text
profile: swarm2
session_id: 20260520_100429_ebf65b
process session: proc_4293e22e7840
objective: diagnose/optimize D3 mem0-on-LongMemEval local run
status: exited 0
```

Swarm finding verified by controller:

```text
Root cause: adapter/API mismatch with mem0 OSS v2.0.2.
- Memory.add was being called with a plain string payload, which triggers mem0's slow inference/extraction path.
- Memory.search was initially called with top-level user_id/limit, while mem0 2.0.2 expects search(query, *, top_k=..., filters=...).
```

## Adapter fix

Touched file:

```text
src/shyftr/benchmarks/adapters/mem0_backend.py
```

Effective behavior:

```text
- ingest uses chat-style messages payload: [{role, content}]
- ingest passes infer=False to avoid slow LLM extraction/inference for fixture-safe benchmark ingestion
- ingest passes user_id/run_id plus message_id/conversation_id metadata
- search calls mem0 v2 style: search(query, filters={"user_id": run_id}, top_k=top_k)
- older limit/k fallbacks remain
```

Boundary:

```text
No API keys.
No mem0 Cloud.
No paid API.
No public benchmark claim.
Still uses local qdrant + fastembed + Ollama config from SHYFTR_MEM0_LOCAL_CONFIG.
```

## Config/artifacts

Existing run-id local mem0 config used:

```text
tmp/bench_configs/mem0-local-ollama-fastembed-runid.json
```

Swarm also created a no-LLM config candidate:

```text
tmp/bench_configs/mem0-local-fastembed-qdrant-nollm-runid.json
```

Controller accepted the Ollama-backed config as canonical for this pass because the no-LLM config caused mem0 construction to fall back toward an OpenAI client in this local install.

Controller-created one-case fixture for fastest proof:

```text
artifacts/benchmarks/phaseD-longmemeval-s-cleaned-onecase.fixture.json
```

It contains:

```text
question_count: 1
conversation_count: 3
message_count: 12
question_id: e47becba
```

## Reports produced

### 1. One-case mem0 proof

Report:

```text
reports/benchmarks/phaseD-longmemeval-onecase-mem0-raw.json
```

Readback:

```text
backend_status_counts: {'ok': 3}
backends: shyftr ok, no-memory ok, mem0-oss ok
mem0 backend_wall_ms: 2113.58270898927
mem0 ingest_ms: 890.9741250099614
mem0 search_ms_total: 5.371958017349243
mem0 retrieval.question_count: 1
mem0 retrieval.recall_at_k: 1.0
mem0 retrieval.precision_at_k: 0.3
mem0 retrieval.answer_support_coverage: 1.0
mem0 answer_eval.question_count: 1
mem0 answer_eval.correctness: 0.0
mem0 answer_eval.abstention_rate: 1.0
mem0 provider disclosure:
  mode: explicit-local-config
  vector_store_provider: qdrant
  embedder_provider: fastembed
  llm_provider: ollama
  llm_model: llama3.2:1b
  api_key_configured: false
```

Interpretation: mem0 OSS reaches `ok` on a LongMemEval-derived one-case local fixture and retrieves expected supporting evidence, but the deterministic answerer abstains because mem0 raw memory text/IDs do not yet map cleanly into answer extraction quality.

### 2. Tiny10 mem0 proof

Report:

```text
reports/benchmarks/phaseD-longmemeval-tiny10-mem0-oss-fixed.json
```

Command:

```bash
rm -f reports/benchmarks/phaseD-longmemeval-tiny10-mem0-oss-fixed.json
rm -rf tmp/bench_cells/phaseD-longmemeval-tiny10-mem0-oss-fixed tmp/mem0_qdrant/phaseD-longmemeval-tiny10-mem0-oss-fixed
SHYFTR_MEM0_LOCAL_CONFIG=tmp/bench_configs/mem0-local-ollama-fastembed-runid.json \
MEM0_TELEMETRY=False \
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/phaseD-longmemeval-s-cleaned-tiny10.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id phaseD-longmemeval-tiny10-mem0-oss-fixed \
  --output reports/benchmarks/phaseD-longmemeval-tiny10-mem0-oss-fixed.json \
  --top-k 1 \
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
mem0 backend_wall_ms: 15155.038957949728
mem0 ingest_ms: 695.8719989634119
mem0 search_count: 1
mem0 search_ms_total: 5.555832991376519
mem0 retrieval.question_count: 10
mem0 retrieval.recall_at_k: 0.06666666666666667
mem0 retrieval.precision_at_k: 0.2
mem0 retrieval.answer_support_coverage: 0.2
mem0 answer_eval.question_count: 10
mem0 answer_eval.correctness: 0.0
mem0 answer_eval.abstention_rate: 1.0
mem0 missed_answer_rate: 1.0
mem0 provider disclosure:
  mode: explicit-local-config
  vector_store_provider: qdrant
  embedder_provider: fastembed
  llm_provider: ollama
  llm_model: llama3.2:1b
  api_key_configured: false
```

Interpretation: the D3 mem0 comparator now completes and reports `ok` on the same tiny10 LongMemEval-derived fixture. This is a bounded local comparator-readiness proof, not a performance win claim.

## Verification

Swarm lane evidence:

```text
proc_4293e22e7840 exited 0
session_id: 20260520_100429_ebf65b
```

Focused and regression tests:

```bash
python -m py_compile src/shyftr/benchmarks/adapters/mem0_backend.py
MEM0_TELEMETRY=False PYTHONPATH=.:src pytest -q tests/test_benchmark_mem0_backend.py
```

Observed:

```text
5 passed in 1.84s
```

Regression bundle:

```bash
MEM0_TELEMETRY=False PYTHONPATH=.:src pytest -q \
  tests/test_benchmark_mem0_backend.py \
  tests/test_benchmark_adapter_contract.py \
  tests/test_benchmark_simple_baseline.py \
  tests/test_benchmark_longmemeval_standard_mapping.py

git diff --check -- \
  src/shyftr/benchmarks/adapters/mem0_backend.py \
  src/shyftr/benchmarks/adapters/shyftr_backend.py \
  tests/test_benchmark_mem0_backend.py
```

Observed:

```text
18 passed in 1.84s
git diff --check clean
```

Process hygiene:

```text
No benchmark/swarm background processes remain from this pass.
Ollama server remains running from earlier D2 setup.
```

## Remaining caveats

- mem0 emits non-blocking spaCy warnings:

```text
Failed to load spaCy lemma model: spaCy is not installed. Install it with: pip install mem0ai[nlp]
Failed to load spaCy full model: spaCy is not installed. Install it with: pip install mem0ai[nlp]
```

- Tiny10 mem0 run uses `--top-k 1`, so this proves bounded completion/status and report disclosure, not full top-k-cutoff parity with the core D3 report.
- mem0 retrieval support exists but answer extraction still abstains. This is expected because raw mem0 memory results are not yet shaped for deterministic answer extraction parity.
- The one-case and tiny10 reports are private/local LongMemEval-derived artifacts only.

## Next recommended order

1. Run D3 tiny10 mem0 with `--top-k 1,3,5,10` now that ingestion/search are bounded.
2. If that stays stable, run D3 core+mem0 together on tiny10 with all intended top-k cutoffs.
3. Then run 50-question private D3 subset for ShyftR/no-memory/simple-bm25/mem0.
4. Only after 50-question review, attempt 200-question private D3 subset.
5. D4 LOCOMO and D5 BEAM remain gated by local dataset path/license review.

## Canonical result

The mem0 D3 blocker is resolved for bounded local execution. mem0 OSS now completes with `status=ok` on LongMemEval-derived one-case and tiny10 fixtures using only non-paid local providers. This upgrades D3 from `core dry-run without mem0` to `core dry-run plus mem0 bounded-readiness proof`, while preserving private/local/no-claim boundaries.
