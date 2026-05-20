# ShyftR Phase D D2 mem0 OSS comparator closeout

Date: 2026-05-20 08:56 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Verified HEAD: `e5a8a68`
Status: D2 is complete locally with a verified `ok` mem0 OSS fixture comparator result using a non-paid local provider stack. No push, merge, clean-worktree state, mem0 Cloud/API result, standard-dataset result, or public superiority claim is made.

## Roadmap anchor

D2 corresponds to the May 18 roadmap tranche:

```text
Phase D / D2 — mem0 OSS comparator real local fixture run
```

Roadmap contract: `2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md` lines 658-690.

User approval: local non-paid mem0 OSS dependency/config setup was approved for fixture-only D2. This did not include approval for mem0 Cloud, API keys, paid APIs, standard-dataset auto-downloads, or public claims.

## Local baseline disclosure

This D2 proof carries the D0/D1 dirty-baseline disclosure forward:

- current HEAD: `e5a8a68`
- branch: `main`
- branch state at D2 start: `main` ahead of `origin/main` by 1
- worktree status at D2 start: dirty
- dirty state included tracked Phase B/C/C3 implementation/doc/test changes, D0/D1 docs/reports, and untracked phase artifacts

Interpretation: this is a local fixture-gated comparator run from an explicitly disclosed dirty worktree. It is suitable for roadmap steering and D2 comparator-status classification, not for clean published benchmark claims.

## Environment setup performed

Local Python/package/model setup was performed in the active local Anaconda environment:

```bash
python -m pip install 'mem0ai==2.0.2'
python -m pip install fastembed
python -m pip install ollama
ollama pull llama3.2:1b
```

The local Ollama server was started with:

```bash
ollama serve
```

Observed local provider inventory:

```text
mem0ai 2.0.2
fastembed 0.8.0
qdrant-client 1.18.0
ollama model available: llama3.2:1b
```

Side-effect disclosure: `fastembed` installation updated shared Anaconda packages including `huggingface-hub`, `tokenizers`, and `tqdm`, and pip reported conflicts with existing `transformers`/`datasets` version constraints. This is recorded because D2 setup mutated the shared local Python environment.

## Non-paid local mem0 config

The local mem0 config used for the successful D2 run is:

```text
/Users/stefan/ShyftR/tmp/bench_configs/mem0-local-ollama-fastembed.json
```

It selects:

- vector store: `qdrant` local path
- embedder: `fastembed`
- embedder model: `BAAI/bge-small-en-v1.5`
- LLM provider: local `ollama`
- LLM model: `llama3.2:1b`
- local base URL: `http://localhost:11434`
- API key configured: `false`

The adapter only uses this path when `SHYFTR_MEM0_LOCAL_CONFIG` is explicitly set. It refuses credential-bearing config fields such as API keys, tokens, secrets, or passwords.

## Code/test changes

Implementation hardening:

- `src/shyftr/benchmarks/adapters/mem0_backend.py`
  - supports explicit credential-free local config via `SHYFTR_MEM0_LOCAL_CONFIG`
  - constructs mem0 through `mem0.Memory.from_config(...)` for local provider stacks
  - discloses provider metadata in retrieval details
  - rejects credential-bearing config material
  - passes a run-scoped `user_id` to mem0 add/search because mem0ai 2.0.2 requires an entity selector
  - records `mem0ai` package version as `2.0.2`
  - preserves skip-safe default behavior when no explicit local config is set
  - updates frozen `AdapterCostLatencyStats` by replacement rather than mutation

Test coverage:

- `tests/test_benchmark_mem0_backend.py`
  - missing dependency reports `AdapterSkip`
  - default constructor cloud/API-key requirement reports `AdapterSkip`, not failure
  - explicit local config path constructs via `Memory.from_config(...)`
  - explicit local config metadata discloses provider/model/base-url/no-key facts
  - credential-bearing local config is refused
  - CLI run with `--include-mem0-oss` preserves runner-owned deterministic answer/judge path

## D2 artifacts

Successful local mem0 report:

```text
reports/benchmarks/phaseD-mem0-oss-local-fixture.json
```

Report readback evidence:

```text
run_id phaseD-mem0-oss-local-fixture
backend_status_counts {'ok': 4}
backends [('shyftr', 'ok'), ('no-memory', 'ok'), ('simple-bm25', 'ok'), ('mem0-oss', 'ok')]
mem0 retrieval details:
  mode explicit-local-config
  config_source SHYFTR_MEM0_LOCAL_CONFIG
  vector_store_provider qdrant
  embedder_provider fastembed
  embedder_model BAAI/bge-small-en-v1.5
  llm_provider ollama
  llm_model llama3.2:1b
  llm_base_url http://localhost:11434
  mem0_version 2.0.2
  memory_api mem0.Memory
  api_key_configured false
llm judge provider none; api_key_env null; api_key_file_configured false
```

Earlier skipped-status report retained for chain-of-custody:

```text
reports/benchmarks/phaseD-mem0-oss-fixture.json
```

It recorded the pre-local-config state where mem0ai imported but default construction required API key/provider configuration.

## Verification commands

Focused D2 tests:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_mem0_backend.py
```

Observed result:

```text
5 passed in 2.33s
```

D2 local fixture command:

```bash
SHYFTR_MEM0_LOCAL_CONFIG=/Users/stefan/ShyftR/tmp/bench_configs/mem0-local-ollama-fastembed.json \
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture synthetic-mini \
  --run-id phaseD-mem0-oss-local-fixture \
  --output reports/benchmarks/phaseD-mem0-oss-local-fixture.json \
  --include-mem0-oss \
  --include-simple-bm25 \
  --top-k 1,3,5 \
  --enable-answer-eval \
  --include-retrieval-details
```

Observed result: exit 0, with `mem0-oss` recorded as `ok` and local baselines also recorded as `ok`.

Regression bundle:

```bash
python -m py_compile src/shyftr/benchmarks/adapters/mem0_backend.py tests/test_benchmark_mem0_backend.py
PYTHONPATH=.:src pytest -q tests/test_benchmark_mem0_backend.py tests/test_benchmark_simple_baseline.py tests/test_benchmark_adapter_contract.py
git diff --check -- src/shyftr/benchmarks/adapters/mem0_backend.py tests/test_benchmark_mem0_backend.py
```

Observed result:

```text
11 passed in 1.94s
```

`git diff --check` produced no whitespace errors.

## Boundary preserved

D2 did not:

- use mem0 Cloud
- infer or read API keys
- use paid provider calls
- download standard benchmark datasets
- run LongMemEval, LOCOMO-standard, or BEAM
- claim ShyftR beats mem0 or any external memory system
- convert this local dirty-worktree run into a public benchmark claim

D2 did use non-paid local downloads/installations approved by the operator:

- `fastembed` package/model assets
- `ollama` Python package
- `llama3.2:1b` Ollama model

## D3 readiness

The next roadmap tranche is D3:

```text
D3. LongMemEval dry and scaled runs
```

Current D3 status: implementation is ready for a local input path, but dataset acquisition/path is still gated. D3 requires an operator-provided local LongMemEval input path. No automatic standard-dataset download is allowed by this closeout.

## Canonical result

Phase D D2 is locally complete and verified with an `ok` mem0 OSS comparator fixture run using non-paid local providers.

The project is now ready for the next gated decision: provide/approve a local LongMemEval input path for D3, or authorize non-paid local dataset acquisition under the roadmap/license constraints.
