# ShyftR Phase 14 handoff packet

Date: 2026-05-18
UTC handoff timestamp: 2026-05-17T22:56:09Z
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Current HEAD: `145026c` (`docs: plan phase 14 benchmark execution`)
Status: Phase 14 ready to begin at P14-0. No full standard benchmark has been run yet.

## Current truth

Phase 12 and Phase 13 benchmark-readiness work is complete, committed, pushed, and CI-green.

Post-Phase-13 malformed ledger tolerance hardening is also complete, committed, pushed, and CI-green.

Latest commits:

```text
145026c docs: plan phase 14 benchmark execution
75d9e19 fix: tolerate malformed carry ledgers
c650344 docs: mark phase 13 ci green
41038e1 feat: complete phase 13 benchmark readiness
```

Latest CI:

```text
26005005654 success for 145026c
26004947495 success for 75d9e19
26003336874 success for c650344
```

Current worktree at handoff creation was clean:

```text
## main...origin/main
```

## Canonical inputs for Phase 14

Read these before starting implementation or live benchmark execution:

```text
2026-05-18-shyftr-phase-14-actual-benchmark-roadmap.md
docs/benchmarks/phase13-local-full-dataset-runbook.md
docs/benchmarks/phase13-optional-llm-judge-gating.md
docs/benchmarks/README.md
docs/benchmarks/methodology.md
docs/benchmarks/report-schema.md
scripts/run_memory_benchmark.py
src/shyftr/benchmarks/runner.py
src/shyftr/benchmarks/adapters/base.py
src/shyftr/benchmarks/adapters/shyftr_backend.py
src/shyftr/benchmarks/adapters/no_memory.py
src/shyftr/benchmarks/adapters/mem0_backend.py
```

## Phase 14 purpose

Phase 14 turns the benchmark harness into actual local benchmark evidence.

The work should compare ShyftR fairly against leading memory systems and simple baselines, then convert measured gaps into a prioritized ShyftR improvement backlog.

This is an engineering measurement phase, not a marketing/publication phase.

## What is already available

Available harness surfaces:

- neutral benchmark adapter contract;
- ShyftR local backend adapter;
- no-memory baseline adapter;
- optional mem0 OSS adapter with skip-safe behavior;
- synthetic-mini fixture;
- LOCOMO-mini fixture;
- LOCOMO-standard local mapping/conversion scaffold;
- LongMemEval-standard local mapping/conversion scaffold;
- BEAM-standard local mapping/conversion scaffold;
- `--limit-questions N` dry-run control;
- `--isolate-per-case` per-question reset/ingest control;
- timeout, retry, and resume controls;
- deterministic runner-owned answer evaluation;
- optional explicit-provider LLM judge scaffold, disabled by default;
- report output guards under `artifacts/`, `reports/`, and `tmp/`.

Available public-safe fixture reports:

```text
reports/benchmarks/phase11_synthetic_mini.json
reports/benchmarks/phase11_locomo_mini.json
reports/benchmarks/phase12_locomo_mini_answer_eval.json
docs/benchmarks/phase11-final-benchmark-report.json
docs/benchmarks/phase12-final-benchmark-report.json
```

## What has not been run

Do not claim any of the following as completed:

- full LongMemEval;
- full LOCOMO-standard;
- BEAM subset or full BEAM;
- real mem0 OSS result on this machine;
- mem0 Cloud, Zep, Letta, LangGraph Store, or other service comparator runs;
- optional LLM judge agreement runs;
- public benchmark summary or superiority claim.

## Phase 14 starting tranche

Start with P14-0: inventory, approvals, and run registry.

P14-0 deliverables from the roadmap:

```text
docs/benchmarks/phase14-service-inventory.md
docs/benchmarks/phase14-run-registry.md
```

P14-0 must answer, without using credentials or running paid APIs:

1. Which comparator systems are ready, install-needed, credential-needed, not suitable, or deferred?
2. Which datasets are local-file-ready, obtain-needed, license-review-needed, or deferred?
3. What run IDs will be used for the first dry runs and scaled runs?
4. Which local dataset path will be used first, with no committed raw path if it is sensitive?
5. What is the stop condition for each run?
6. What results are private-only until reviewed?

## Recommended immediate execution sequence

1. Confirm repo remains clean:

```bash
git status --short --branch
git pull --rebase origin main
```

2. Create P14-0 docs:

```text
docs/benchmarks/phase14-service-inventory.md
docs/benchmarks/phase14-run-registry.md
```

3. Verify current setup/API surfaces for these comparators before writing adapter claims:

```text
mem0 OSS
mem0 Cloud
Zep
Letta
LangGraph Store
simple local BM25 or vector baseline
```

4. Record each comparator status using this vocabulary:

```text
ready
install-needed
credential-needed
not-suitable
deferred
```

5. Record each dataset status using this vocabulary:

```text
local-file-ready
obtain-needed
license-review-needed
deferred
```

6. After P14-0, begin P14-1 by adding a simple local retrieval baseline before any public comparator claims.

7. First real dataset execution should be LongMemEval dry run, not full BEAM:

```bash
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/<RUN_ID>.longmemeval.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id <RUN_ID>-longmemeval-dryrun \
  --output reports/benchmarks/<RUN_ID>-longmemeval-dryrun.json \
  --top-k 1,3,5,10 \
  --limit-questions 10 \
  --isolate-per-case \
  --timeout-seconds 300 \
  --max-retries 2 \
  --resume-existing \
  --enable-answer-eval \
  --allow-private-fixture
```

Only run this after an operator-approved local LongMemEval file is available and converted.

## Guardrails

Do not:

- auto-download datasets;
- commit raw third-party datasets;
- commit converted private fixtures;
- commit private run reports or raw judge logs;
- infer credentials from ambient environment;
- run paid/remote APIs without explicit approval;
- enable optional LLM judge before deterministic reports are stable;
- publish benchmark results before review;
- tune ShyftR between comparator runs without recording git SHA and rerunning affected baselines.

Do:

- keep deterministic answer evaluation primary;
- keep memory backends as retrieval backends, not answer generators;
- include no-memory baseline in every run;
- add simple BM25/vector baseline before claiming external comparator results;
- record skipped comparators honestly;
- record timeouts and retries honestly;
- turn measured ShyftR misses into an improvement backlog.

Human/operator approval is the only required human review gate. Do not invent external tester/report-count gates.

## P14-1 expected next implementation surface

After P14-0 docs land, the likely next code tranche is P14-1:

- add `simple-bm25` or equivalent dependency-light local retrieval baseline adapter;
- add a CLI flag to include it;
- add focused tests for reset, ingest, search, cost/latency stats, and report output;
- run synthetic-mini and LOCOMO-mini with ShyftR, no-memory, and the simple baseline;
- keep full standard-dataset execution out of P14-1.

Likely files for P14-1:

```text
src/shyftr/benchmarks/adapters/simple_bm25.py
src/shyftr/benchmarks/adapters/__init__.py
scripts/run_memory_benchmark.py
src/shyftr/benchmarks/runner.py
tests/test_benchmark_simple_baseline.py
docs/benchmarks/README.md
docs/benchmarks/methodology.md
```

## Verification commands

For P14-0 docs-only tranche:

```bash
python scripts/terminology_inventory.py --fail-on-public-stale
python scripts/terminology_inventory.py --fail-on-capitalized-prose
python scripts/public_readiness_check.py
git diff --check
git status --short --branch
```

For P14-1 or later code tranches:

```bash
PYTHONPATH=.:src python -m compileall -q src scripts examples
PYTHONPATH=.:src pytest -q tests/test_benchmark_adapter_contract.py tests/test_benchmark_locomo_mini_fixture.py
PYTHONPATH=.:src pytest -q
python scripts/terminology_inventory.py --fail-on-public-stale
python scripts/terminology_inventory.py --fail-on-capitalized-prose
python scripts/public_readiness_check.py
git diff --check
git status --short --branch
```

## Completion criteria for Phase 14

Phase 14 is complete only when:

- at least LongMemEval and one of LOCOMO-standard or BEAM have approved local run reports;
- ShyftR is compared against no-memory and a simple local retrieval baseline;
- at least one leading memory comparator is measured or explicitly blocked with a documented reason;
- every report records dataset scope, backend config, top-k, reset mode, timeout/retry/resume settings, answerer, judge, and skipped/failed backends;
- an improvement backlog is created from measured failures;
- full repo verification passes after code changes;
- public/private result boundaries are explicit.

## First action for the next worker

Begin P14-0. Create the service inventory and run registry. Do not run datasets, install services, or use credentials until the inventory and run registry are reviewed.
