# ShyftR Phase D D3 LongMemEval local dry-run closeout

Date: 2026-05-20 09:58 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Verified HEAD: `e5a8a68`
Status: D3 is locally advanced with non-paid LongMemEval acquisition, private fixture conversion, and a verified 10-question trimmed LongMemEval dry run for ShyftR/no-memory/simple-bm25. mem0 OSS remains proven on D2 fixture, but mem0 LongMemEval dry-run did not finish within practical local-run time and needs a separate smaller/optimized lane before scaled D3.

## Roadmap anchor

D3 corresponds to the May 18 roadmap tranche:

```text
D3. LongMemEval dry and scaled runs
```

Roadmap contract: `2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md` lines 691-730.

Operator approval in this session authorized non-paid local dataset acquisition and local benchmark setup. No paid API, cloud memory service, credentials, or public benchmark claim was authorized or used.

## Dataset acquisition

Non-paid local dataset source:

```text
Hugging Face dataset: xiaowu0162/longmemeval-cleaned
Dataset commit SHA: 98d7416c24c778c2fee6e6f3006e7a073259d48f
File: longmemeval_s_cleaned.json
Local path: /Users/stefan/ShyftR/tmp/external_datasets/longmemeval-cleaned/longmemeval_s_cleaned.json
Size: 277383467 bytes
License in dataset card: MIT
Gated/private: false/false from Hugging Face dataset metadata
```

Dataset card excerpt read locally:

```text
license: mit
language: en
splits: longmemeval_oracle.json, longmemeval_s_cleaned.json, longmemeval_m_cleaned.json
```

## Conversion artifacts

Full downloaded `longmemeval_s_cleaned.json` was converted once to a private ShyftR fixture:

```text
artifacts/benchmarks/phaseD-longmemeval-s-cleaned.fixture.json
artifacts/benchmarks/phaseD-longmemeval-s-cleaned.fixture.json.manifest.json
```

Full fixture manifest summary:

```text
case_count: 500
session_count: 23867
message_count: 246750
contains_private_data: true
question_type_counts:
  knowledge-update: 78
  multi-session: 133
  single-session-assistant: 56
  single-session-preference: 30
  single-session-user: 70
  temporal-reasoning: 133
input_sha256: d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442
output_sha256: 2f7d5fff6f1cc872f2d24c47a368c3efe3613e606756ebdb5a9ab05f3d03314f
```

A first-10 subset of the original downloaded file was also created, but it still contained 496 sessions / 5177 messages and was too slow for immediate all-backend local dry-run iteration.

For practical D3 smoke evidence, a derived tiny10 local dry-run subset was created from the first 10 cases by keeping answer sessions plus up to two distractor sessions per case:

```text
Input: tmp/external_datasets/longmemeval-cleaned/longmemeval_s_cleaned_tiny10.json
Fixture: artifacts/benchmarks/phaseD-longmemeval-s-cleaned-tiny10.fixture.json
Manifest: artifacts/benchmarks/phaseD-longmemeval-s-cleaned-tiny10.fixture.json.manifest.json
```

Tiny10 fixture manifest summary:

```text
case_count: 10
session_count: 38
message_count: 188
contains_private_data: true
question_type_counts:
  single-session-user: 10
input_sha256: 4e7a827cfd9ec794dc8083a888966e78d4404c102929202b528b137db8240e5a
output_sha256: dcc44c1ab2168ad60371c1839251fc09449b9544bd695a4a95aebf8cd3c7c88b
claim_limit: mapping and conversion metadata only; not a full LongMemEval run or performance claim
```

## Dry-run command and report

Successful D3 core dry-run command:

```bash
MEM0_TELEMETRY=False \
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/phaseD-longmemeval-s-cleaned-tiny10.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id phaseD-longmemeval-tiny10-core-dryrun \
  --output reports/benchmarks/phaseD-longmemeval-tiny10-core-dryrun.json \
  --top-k 1,3,5,10 \
  --limit-questions 10 \
  --isolate-per-case \
  --timeout-seconds 300 \
  --max-retries 2 \
  --enable-answer-eval \
  --allow-private-fixture \
  --include-simple-bm25 \
  --include-retrieval-details
```

Report:

```text
reports/benchmarks/phaseD-longmemeval-tiny10-core-dryrun.json
```

Report readback evidence:

```text
backend_status_counts: {'ok': 3}
dataset.name: longmemeval-standard
dataset.split: longmemeval_s_cleaned_tiny10
dataset.version: xiaowu0162/longmemeval-cleaned@98d7416c24c778c2fee6e6f3006e7a073259d48f:longmemeval_s_cleaned:tiny10
dataset.question_count: 10
dataset.conversation_count: 38
dataset.contains_private_data: true

shyftr: ok
  retrieval.question_count: 10
  retrieval.recall_at_k: 0.2666666666666667
  retrieval.precision_at_k: 0.08
  answer_eval.question_count: 10
  answer_eval.correctness: 0.6
  answer_eval.abstention_rate: 0.0
  boundary_policy_fallbacks: 2

no-memory: ok
  retrieval.question_count: 10
  retrieval.recall_at_k: 0.0
  retrieval.precision_at_k: 0.0
  answer_eval.question_count: 10
  answer_eval.correctness: 0.0
  answer_eval.abstention_rate: 1.0

simple-bm25: ok
  retrieval.question_count: 10
  retrieval.recall_at_k: 0.7090909090909091
  retrieval.precision_at_k: 0.22222222222222224
  answer_eval.question_count: 10
  answer_eval.correctness: 0.7
  answer_eval.abstention_rate: 0.0

llm_judge.provider: none
```

Interpretation: this is a private local LongMemEval-derived trimmed dry run. It is not a standard full LongMemEval result and does not support public ranking/superiority claims.

## mem0 D3 attempts

mem0 OSS was already proven `ok` in D2 with the local stack:

```text
mem0ai 2.0.2
fastembed 0.8.0
qdrant-client 1.18.0
ollama 0.6.2 / Ollama server 0.12.0
llama3.2:1b
```

D3 mem0 attempts found two practical issues:

1. Reusing a fixed local Qdrant path caused lock conflicts:

```text
Storage folder /Users/stefan/ShyftR/tmp/mem0_qdrant/phaseD-mem0-oss-local-fixture is already accessed by another instance of Qdrant client.
```

A run-id templated config was created to avoid that path reuse:

```text
tmp/bench_configs/mem0-local-ollama-fastembed-runid.json
```

2. mem0 LongMemEval tiny runs were still too slow for immediate D3 closeout. A 3-question mem0-only tiny run remained running after several minutes and was killed for bounded execution.

Therefore D3 core dry-run evidence is complete for ShyftR/no-memory/simple-bm25. mem0 D3 should be handled as the next optimization lane rather than blocking D3 dataset acquisition/conversion/core dry-run proof.

## ShyftR boundary-policy benchmark fallback

The LongMemEval text contains ordinary benchmark-user text with terms such as `branch` / `worktree` that match ShyftR's production memory pollution guard. The ShyftR benchmark adapter was patched to keep dry-runs evaluable while preserving policy honesty:

- production `remember_trusted` is attempted first;
- if `BoundaryPolicyError` occurs, the adapter records `boundary_policy_fallbacks` in retrieval details;
- fallback stores a filtered pending-review benchmark message, not a direct promoted durable memory;
- the report disclosed 2 such fallbacks in this tiny10 run.

Touched file:

```text
src/shyftr/benchmarks/adapters/shyftr_backend.py
```

## Verification commands

Mapping tests:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_longmemeval_standard_mapping.py
```

Observed:

```text
7 passed in 0.26s
```

Regression bundle:

```bash
python -m py_compile src/shyftr/benchmarks/adapters/shyftr_backend.py src/shyftr/benchmarks/adapters/mem0_backend.py tests/test_benchmark_mem0_backend.py
MEM0_TELEMETRY=False PYTHONPATH=.:src pytest -q \
  tests/test_benchmark_adapter_contract.py \
  tests/test_benchmark_simple_baseline.py \
  tests/test_benchmark_mem0_backend.py \
  tests/test_benchmark_longmemeval_standard_mapping.py
git diff --check -- \
  src/shyftr/benchmarks/adapters/shyftr_backend.py \
  src/shyftr/benchmarks/adapters/mem0_backend.py \
  tests/test_benchmark_mem0_backend.py
```

Observed:

```text
18 passed in 2.27s
```

`git diff --check` produced no whitespace errors.

## Boundary preserved

D3 did not:

- use paid APIs
- use API keys or credentials
- use mem0 Cloud
- run a public benchmark
- claim ShyftR beats any comparator
- commit or publish third-party dataset content
- run full LongMemEval, LOCOMO-standard, or BEAM

D3 did use approved non-paid local acquisition of a public MIT-licensed Hugging Face dataset and local private fixture/report artifacts.

## Next gates

Recommended next actions:

1. D3-mem0 optimization lane: make mem0 local LongMemEval runs complete quickly and without Qdrant migration locks. Options include disabling mem0 history/telemetry more completely, using a dedicated local Qdrant server instead of file Qdrant, or using smaller per-case mem0 smoke runs.
2. D3 scaled core lanes: run 50-question and then 200-question trimmed/private subsets after reviewing tiny10 dry-run methodology.
3. D4 LOCOMO-standard: acquire/review local LOCOMO path/license and run the same dry/scaled pattern.
4. D5 BEAM: acquire/review local BEAM path/license and include attribution metadata before any report summary.

## Canonical result

Phase D D3 is no longer blocked on dataset acquisition. A non-paid LongMemEval cleaned dataset was acquired, converted to private ShyftR fixtures, and used for a verified 10-question local dry run across ShyftR/no-memory/simple-bm25. mem0 remains locally configured and D2-proven, but needs a separate optimization lane before it is useful on LongMemEval-derived runs.
