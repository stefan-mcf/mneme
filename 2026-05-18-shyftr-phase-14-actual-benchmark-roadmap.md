# ShyftR Phase 14 roadmap: actual benchmark execution and improvement loop

Date: 2026-05-18
Repo: `/Users/stefan/ShyftR`
Starting point: Phase 13 benchmark-readiness harness is complete; post-Phase-13 malformed ledger tolerance hardening is committed and CI-green.
Status: roadmap / execution plan. No full benchmark result is claimed by this document.

## Purpose

Phase 14 turns the Phase 11-13 benchmark harness into real local benchmark evidence.

The goal is to compare ShyftR fairly against leading memory systems and simple baselines, then convert measured gaps into a prioritized ShyftR improvement backlog.

This is not a marketing phase. It is an engineering measurement phase:

1. run approved local standard datasets;
2. compare ShyftR against current memory services and baselines under one runner contract;
3. identify where ShyftR wins, loses, skips, times out, or needs a product or ranking change;
4. feed those results into the next implementation phases.

## Ground truth from prior phases

Already available:

- neutral benchmark adapter contract;
- ShyftR local backend adapter;
- no-memory baseline adapter;
- optional mem0 OSS adapter with skip-safe behavior;
- synthetic-mini and LOCOMO-mini fixture reports;
- LOCOMO-standard, LongMemEval-standard, and BEAM-standard local mapping/conversion scaffolds;
- `--limit-questions` dry-run control;
- `--isolate-per-case` per-question reset/ingest control;
- timeout, retry, and resume controls;
- deterministic runner-owned answer evaluation;
- optional explicit-provider LLM judge scaffold, disabled by default.

Not yet available:

- full LongMemEval results;
- full LOCOMO-standard results;
- BEAM results;
- live mem0 OSS result on this machine;
- mem0 Cloud, Zep, Letta, LangGraph, or other service results;
- optional LLM judge agreement results;
- improvement backlog derived from actual benchmark failures.

## Non-negotiable safety and fairness rules

- Do not auto-download datasets.
- Do not commit raw third-party datasets, converted private fixtures, raw judge logs, or private reports.
- Use local operator-provided dataset paths only.
- Treat all standard-dataset inputs as private unless reviewed otherwise.
- Use ShyftR, comparator services, and baselines through the same runner-owned question, retrieval, answer, and judge path wherever possible.
- Keep memory backends separate from answer generation. Backends retrieve; the runner answers and judges.
- Record skipped comparators explicitly; do not hide missing dependencies or missing credentials.
- Record timeout and retry details explicitly.
- Use deterministic answer evaluation first. Use LLM judging only after explicit approval.
- No public superiority claim until dataset license, config, run reports, and claim text are reviewed.

## Comparator set

Phase 14 starts with two classes: required local baselines and optional service comparators.

### Required baselines

1. `shyftr`
   - ShyftR local cell backend.
   - Required for every run.

2. `no-memory`
   - Empty retrieval baseline.
   - Required for every run.

3. `simple-bm25` or `simple-vector`
   - Local non-memory retrieval baseline.
   - Add before publishing any comparison because it answers whether ShyftR beats a simple retrieval-only index.

### Optional memory-service comparators

Exact adapter details must be verified from current vendor documentation immediately before implementation. Initial target list:

1. `mem0-oss`
   - Already scaffolded.
   - First external comparator to make real, because it can run locally and already has a skip-safe adapter path.

2. `mem0-cloud`
   - Key-gated and opt-in.
   - Useful because mem0 is a direct product comparator.
   - Never infer API keys from ambient environment; require explicit env-var or key-file flag.

3. `zep`
   - Cloud or local mode depending on current supported deployment surface.
   - Useful because it is a widely referenced long-term memory service for agent apps.
   - Adapter must disclose version, deployment mode, embedding/rerank settings, and cost model.

4. `letta`
   - Local or server-backed memory agent system.
   - Useful as an agent-memory architecture comparator, but only if the adapter can isolate retrieval from agent-loop answering.

5. `langgraph-store` / LangChain memory-store baseline
   - Useful as a framework-native persistent memory baseline.
   - Treat it as a framework baseline, not a managed memory-service claim.

6. Optional later comparators
   - LlamaIndex memory or managed index flows;
   - custom vector database baseline with fixed embedding model;
   - any new leading service identified during P14-0 inventory.

## Dataset order

Use the smallest real run that can reveal useful ranking and answer-quality gaps before expensive or large-scale runs.

1. LongMemEval dry run
   - First real standard-dataset path.
   - Use `--limit-questions 10`, `--isolate-per-case`, deterministic answer eval.
   - Primary goal: validate case grouping, answer-support coverage, and per-question reset behavior.

2. LongMemEval scaled local runs
   - 50 questions, then 200 questions, then full approved local file if stable.
   - Primary goal: long-context recall and question-class breakdown.

3. LOCOMO-standard dry run and scaled runs
   - Use after LongMemEval path is stable.
   - Primary goal: multi-session recall, temporal questions, and conversation-memory behavior.

4. BEAM small subset
   - Start with smallest approved local BEAM subset.
   - Primary goal: retrieval scale, latency, memory-index behavior, and attribution-safe report handling.

5. BEAM larger buckets
   - Only after small BEAM run completes without cost/time surprises.
   - Primary goal: scale and throughput, not answer-quality marketing claims.

## Phase 14 tranches

### P14-0: inventory, approvals, and run registry

Deliverables:

- `docs/benchmarks/phase14-service-inventory.md`
- `docs/benchmarks/phase14-run-registry.md`
- checked local paths recorded with placeholders or redacted handles only;
- approval checklist for each dataset and service comparator;
- adapter implementation matrix.

Tasks:

1. Verify current setup commands and APIs for mem0 OSS, mem0 Cloud, Zep, Letta, and LangGraph Store.
2. Record each comparator as one of: ready, install-needed, credential-needed, not suitable, deferred.
3. Record dataset availability as one of: local-file-ready, obtain-needed, license-review-needed, deferred.
4. Assign run IDs before execution.
5. Decide first dry-run dataset path.

Done means:

- no code changes are needed to understand what can run;
- every planned real run has a run ID, dataset status, comparator status, expected cost/risk, and stop condition;
- no credentials or dataset paths are committed.

### P14-1: local baseline adapter hardening

Deliverables:

- simple local BM25 or vector baseline adapter;
- focused tests for adapter reset, ingest, search, and report stats;
- CLI flag for including the local retrieval-only baseline;
- docs update explaining why this baseline matters.

Tasks:

1. Add `simple-bm25` first unless a vector baseline is already easier and deterministic.
2. Keep the baseline dependency-light and local-only.
3. Make it run on synthetic-mini and LOCOMO-mini.
4. Compare ShyftR against `no-memory` and `simple-bm25` before adding paid services.

Done means:

- mini fixture reports show ShyftR, no-memory, and simple baseline side by side;
- full repo gates pass;
- no third-party dataset run is needed for this tranche.

### P14-2: mem0 OSS real local run

Deliverables:

- validated mem0 OSS install/run notes;
- real mem0 OSS result on synthetic-mini and LOCOMO-mini;
- adapter corrections if current mem0 API differs from the scaffold;
- skip-safe behavior preserved when mem0 is absent.

Tasks:

1. Install or use an isolated local mem0 OSS environment only after approval.
2. Run fixture smoke with `--include-mem0-oss`.
3. Confirm mem0 ingestion and search are not silently falling back to degraded keyword mode unless reported.
4. Record version and config in report metadata.

Done means:

- mem0 OSS either has an `ok` result with version/config details, or a clearly justified skipped/not-suitable status;
- ShyftR comparison is still fixture-level only.

### P14-3: LongMemEval dry-run and scaled local runs

Deliverables:

- converted local LongMemEval fixture under ignored/private output path;
- dry-run report with 10 questions;
- scaled reports at 50 and 200 questions if dry-run passes;
- full local run report if approved after scaled runs;
- analysis note summarizing failures by question class.

Default command shape:

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

Add comparator flags only after each comparator is installed and approved.

Done means:

- the dry run and at least one scaled run produce valid reports;
- report explains dataset size, selected question count, reset mode, backend list, skipped backends, and answer-eval settings;
- analysis names ShyftR improvement candidates without overclaiming.

### P14-4: LOCOMO-standard dry-run and scaled local runs

Deliverables:

- converted local LOCOMO fixture under ignored/private output path;
- dry-run report;
- scaled reports;
- comparison against ShyftR, no-memory, simple baseline, and approved memory-service comparators;
- analysis note for temporal and multi-session behavior.

Tasks:

1. Validate converted fixture counts and manifest digest.
2. Start with `--limit-questions 10`.
3. Add `--enable-answer-eval` for runner-owned answer checks.
4. Compare against LongMemEval failure categories.

Done means:

- LOCOMO-standard report exists with clear private/local claim limits;
- ShyftR improvement backlog separates retrieval misses from answerer limitations.

### P14-5: BEAM small subset and scale controls

Deliverables:

- BEAM local subset conversion report and manifest;
- dry-run report;
- small-subset run report;
- scale/cost analysis;
- BEAM attribution block for any shared derivative summary.

Tasks:

1. Start with the smallest approved local BEAM subset.
2. Avoid BEAM-10M until small subset cost and runtime are known.
3. Track latency p50/p95, ingest duration, retry counts, timeout counts, and report size.
4. Keep BEAM-derived files private unless sharing is separately approved and attribution is attached.

Done means:

- ShyftR has at least one scale-oriented BEAM result;
- any failures are classified as mapping, ingestion, retrieval, timeout, memory growth, or report-size issues.

### P14-6: service comparators beyond mem0 OSS

Deliverables per comparator:

- adapter implementation or explicit not-suitable note;
- version/config capture;
- credential gate;
- focused mock tests;
- fixture smoke result;
- one approved standard-dataset dry-run result.

Comparator order:

1. mem0 Cloud;
2. Zep;
3. Letta;
4. LangGraph Store;
5. optional additional service selected after P14-0 inventory.

Done means:

- every comparator is either measured, skipped, or deferred with a reason;
- paid/API-backed services have explicit cost and credential reporting without key leakage;
- ShyftR is not tuned against only one competitor.

### P14-7: optional LLM judge agreement run

Deliverables:

- deterministic-vs-LLM judge agreement report;
- raw judge JSONL stored only in approved private output path if enabled;
- prompt hash and model config recorded;
- disagreement review packet.

Tasks:

1. Run LLM judge only after deterministic reports are stable.
2. Use a small sample first.
3. Review disagreements before trusting aggregate scores.
4. Never use LLM judge as the sole quality metric.

Done means:

- LLM judge adds calibration evidence or is explicitly deferred;
- no raw keys or private prompts are committed.

### P14-8: benchmark synthesis and improvement backlog

Deliverables:

- `docs/benchmarks/phase14-private-results-index.md` with redacted handles only if reports remain private;
- `docs/benchmarks/phase14-improvement-backlog.md`;
- machine-readable benchmark summary JSON if public-safe;
- next-phase implementation plan based on measured gaps.

Gap taxonomy:

- mapping/parsing failure;
- ingestion loss;
- retrieval rank miss;
- answer-support coverage miss;
- temporal or multi-hop miss;
- conflict-handling miss;
- provenance or audit gap;
- sensitivity or privacy risk;
- latency/cost issue;
- timeout/retry issue;
- comparator API mismatch;
- report/schema insufficiency;
- review-gate / authority-mode ablation gap;
- candidate/advisory retrieval gap;
- benchmark-adapter simplification caveat.

Authority-mode synthesis requirement:

Benchmark synthesis must label the ShyftR mode used for each run: benchmark-index, approved-memory, candidate/advisory, pack/loadout, or mixed/unsupported. If a comparator wins because it treats all input as directly searchable memory, record that as a direct-ingest comparator behavior and a fairness caveat rather than weakening ShyftR's review-gated durable-memory doctrine. For every important ShyftR miss, classify whether the evidence was absent from mapping, unindexed, low-ranked, present only as an unapproved candidate/proposal, suppressed by lifecycle/privacy/review policy, or retrieved but not used by the answerer.

Backlog ranking formula:

```text
priority = user-visible impact + benchmark frequency + implementation tractability + safety importance - comparator-only artifact risk
```

Done means:

- each important ShyftR gap has a linked benchmark example and a proposed fix path;
- quick fixes and deeper architecture changes are separated;
- public claims remain separated from private local results.

## Report bundle structure

Private local reports should use this shape:

```text
reports/benchmarks/phase14/<run_id>/
  report.json
  manifest.json
  analysis.md
  commands.txt
  comparator-config-redacted.json
```

Do not commit this directory unless every file is reviewed and approved for public sharing.

If a public-safe summary is later approved, publish only a scrubbed summary that includes:

- dataset name and license notes;
- dataset split or question-count scope;
- git SHA;
- backend list;
- comparator versions;
- answerer and judge settings;
- top-k values;
- timeout/retry/resume settings;
- skipped/failed backends;
- limitations;
- claims allowed;
- claims not allowed.

## Metrics to inspect after every run

Retrieval:

- recall at k;
- precision at k;
- mean reciprocal rank;
- nDCG;
- answer-support coverage;
- rank position of required evidence.

Answer quality:

- correctness;
- token F1;
- missed-answer rate;
- unsupported-answer rate;
- abstention rate;
- question-type breakdown.

Control and audit:

- provenance coverage;
- review-gate compliance where applicable;
- private-data posture;
- report reproducibility;
- skipped backend disclosure;
- retry/timeout disclosure.

Cost and performance:

- ingest duration;
- search latency p50/p95;
- answer/judge latency;
- token usage where applicable;
- estimated cost;
- report size;
- memory/storage growth.

## Decision rules after first real runs

After LongMemEval dry-run:

- If conversion or case grouping fails, stop and fix mapping before running more questions.
- If ShyftR loses to no-memory, inspect answer-eval or fixture labels before changing retrieval.
- If ShyftR loses to simple BM25, prioritize retrieval/ranking and pack assembly changes.
- If ShyftR retrieves the right item but answer eval misses, improve answerer/judge scaffolding before changing memory.
- If service comparators skip, fix adapter/env before claiming comparative evidence.

After scaled runs:

- If latency dominates, profile ingestion/search before adding features.
- If retrieval quality drops with scale, prioritize ranking/index changes.
- If audit/provenance is strong but quality is weak, preserve ShyftR's control model while improving retrieval.
- If quality is strong but cost is high, prioritize compactness and caching.

## Recommended immediate next execution sequence

1. Confirm clean repo and CI for commit `75d9e19`.
2. Land this Phase 14 roadmap as a planning artifact.
3. Create P14-0 service inventory and run registry.
4. Add simple BM25 baseline adapter.
5. Run synthetic-mini and LOCOMO-mini with ShyftR, no-memory, simple baseline, and mem0 OSS if available.
6. Prepare approved local LongMemEval input path.
7. Convert LongMemEval into private fixture output.
8. Run LongMemEval `--limit-questions 10` with ShyftR, no-memory, simple baseline, deterministic answer eval, and per-case reset.
9. Review report before any larger run.
10. Scale LongMemEval to 50, then 200, then full local file if stable.

## Completion criteria for Phase 14

Phase 14 is complete when:

- at least LongMemEval and one of LOCOMO-standard or BEAM have approved local run reports;
- ShyftR is compared against no-memory and a simple local retrieval baseline;
- at least one leading memory comparator is measured or explicitly blocked with a documented reason;
- every report records dataset scope, backend config, top-k, reset mode, timeout/retry/resume settings, answerer, judge, and skipped/failed backends;
- an improvement backlog is created from measured failures;
- full repo verification passes after any code changes;
- public and private result boundaries are explicit.

## Explicit non-goals

- No automatic dataset download.
- No undisclosed paid API use.
- No raw credential logging.
- No benchmark-result publication without review.
- No private-core algorithm release by accident.
- No tuning ShyftR secretly between comparator runs without recording the git SHA and rerunning affected baselines.
