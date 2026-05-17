# Phase 14 P14-0 run registry (planning)

This registry defines planned runs, execution gates, and reporting boundaries before any real benchmark execution. It is a planning artifact only for P14-0.

Repo-local references:

- `2026-05-18-shyftr-phase-14-handoff-packet.md`
- `2026-05-18-shyftr-phase-14-actual-benchmark-roadmap.md`
- `docs/benchmarks/README.md`
- `src/shyftr/benchmarks/runner.py`
- `scripts/run_memory_benchmark.py`
- `docs/benchmarks/phase14-service-inventory.md`

## Private / public posture for P14-0

- Allowed output directories: `artifacts/`, `reports/`, `tmp/` only.
- Default for P14-0 planning runs: private-local by default.
- Public release of any output requires explicit operator approval and a scrubbed summary policy.
- Any run using local third-party datasets marked `contains_private_data=true` or unreviewed license text is private-only.
- Secret-bearing values, raw provider credentials, and absolute local user paths are never written into docs.
- P14-0 does not run paid/remote APIs and does not enable optional LLM judging.

## Approval checklist (P14-0)

- [ ] Comparator status and dataset status are confirmed from `docs/benchmarks/phase14-service-inventory.md`.
- [ ] Branch is current for the local repo state.
- [ ] `--llm-judge-provider none` is confirmed for default planning/dry runs.
- [ ] `--allow-private-fixture` is set only for local private runs with explicit approval.
- [ ] Output paths remain under allowed roots and path placeholders are redacted.
- [ ] Comparator inclusion respects readiness/approval status.
- [ ] Report claim language is limited to configured scope; no global benchmark claims.

## Planned run registry

| run_id | comparator set | dataset | dataset status | backends included | output path | private/public posture | stop condition | approval gate | private-only results policy |
|---|---|---|---|---|---|---|---|---|---|
| p14-0-dryrun-synthetic-mini-v1 | shyftr,no-memory | synthetic-mini | local-file-ready | `ShyftRBackendAdapter`, `NoMemoryBackendAdapter` | `tmp/benchmarks/p14-0/<REDACTED_HANDLE>/synthetic-mini/report.json` | fixture is public-safe; output remains private-local until reviewed | stop if any backend status is `failed`, report schema is invalid, or question mapping mismatch appears | proceed after registry review | private-default for planning; publish only after scrubbed summary approval |
| p14-0-dryrun-locomo-mini-v1 | shyftr,no-memory | LOCOMO-mini | local-file-ready | `ShyftRBackendAdapter`, `NoMemoryBackendAdapter` | `tmp/benchmarks/p14-0/<REDACTED_HANDLE>/locomo-mini/report.json` | fixture is public-safe; output remains private-local until reviewed | stop if LOCOMO-mini mapping errors or timeout/retry count exceeds run policy before adding more comparators | proceed after synthetic-mini validation | private-default for planning; publish only if metadata is scrubbed |
| p14-1-dryrun-synthetic-mini-simple-baseline-v1 | shyftr,no-memory,simple-bm25 | synthetic-mini | local-file-ready | P14-1 adapter plus existing ready baselines | `tmp/benchmarks/p14-1/<REDACTED_HANDLE>/synthetic-mini-simple-baseline/report.json` | public-safe fixture; output private-local until reviewed | stop if simple baseline adapter violates reset/ingest/search/report contract | requires P14-1 implementation and focused tests first | private-default until P14-1 closeout review |
| p14-2-dryrun-locomo-mini-mem0-oss-v1 | shyftr,no-memory,mem0-oss,simple-bm25 | LOCOMO-mini | local-file-ready | optional `Mem0OSSBackendAdapter` only if dependency/config is approved and available | `tmp/benchmarks/p14-2/<REDACTED_HANDLE>/locomo-mini-mem0-oss/report.json` | public-safe fixture; dependency/config summary must be redacted | stop if mem0 reports degraded fallback, missing dependency, or failed ingestion/search after retry budget | requires mem0 OSS install/config approval | private-default; publish only after comparator config summary review |
| p14-3-dryrun-longmemeval-v1 | shyftr,no-memory,simple-bm25,mem0-oss-if-approved | LongMemEval | obtain-needed | backends phased by P14-1/P14-2 readiness | `tmp/benchmarks/p14-3/<REDACTED_HANDLE>/longmemeval-dryrun/report.json` | private only; dataset not committed and local path redacted | stop if conversion, manifest, case grouping, per-case reset, or 10-question answer eval is not reproducible | requires approved local LongMemEval input and converted fixture review | private-only; no public release from dry run |
| p14-4-dryrun-locomo-standard-v1 | shyftr,no-memory,simple-bm25,mem0-oss-if-approved | LOCOMO-standard | obtain-needed | backends phased by P14-1/P14-2 readiness | `tmp/benchmarks/p14-4/<REDACTED_HANDLE>/locomo-standard-dryrun/report.json` | private only unless input/license review says otherwise | stop if conversion/manifest step fails or `--allow-private-fixture` is missing for private-marked data | requires approved local normalized LOCOMO input | private-only until explicit data-share approval |
| p14-5-dryrun-beam-v1 | shyftr,no-memory,simple-bm25,mem0-oss-if-approved | BEAM | license-review-needed | excludes non-approved external comparators | `tmp/benchmarks/p14-5/<REDACTED_HANDLE>/beam-dryrun/report.json` | private only; licensing review required before any shared summary | stop if mapper outputs no manifest, license review is incomplete, or report size/runtime exceeds agreed budget | proceed only after license/attribution review | private-only regardless of run status until reviewed |
| p14-6-service-zep-v1 | zep plus ready local baselines | first approved fixture or standard dry run | deferred until adapter exists | no Zep backend included yet | `tmp/benchmarks/p14-6/<REDACTED_HANDLE>/zep/report.json` | credential-backed; private-only | stop if credentials/config are absent or adapter cannot preserve runner-owned answer/judge path | requires adapter, credential approval, and cost/risk review | private-only until service config is scrubbed |
| p14-6-service-letta-v1 | letta plus ready local baselines | first approved fixture or standard dry run | deferred until adapter exists | no Letta backend included yet | `tmp/benchmarks/p14-6/<REDACTED_HANDLE>/letta/report.json` | local/cloud mode disclosed; private-only | stop if retrieval-only memory path cannot be isolated from agent-loop answering | requires adapter and local/cloud config approval | private-only until service config is scrubbed |
| p14-6-framework-langgraph-store-v1 | langgraph-store plus ready local baselines | first approved fixture or standard dry run | deferred until adapter exists | no LangGraph backend included yet | `tmp/benchmarks/p14-6/<REDACTED_HANDLE>/langgraph-store/report.json` | framework baseline; private-local until reviewed | stop if backend behaves as short-term graph state instead of retrieval-store baseline | requires adapter and dependency/config approval | private-only until framework config is scrubbed |

## Planned command envelope by run

First dry-run path placeholder (required):

```bash
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture synthetic-mini \
  --run-id p14-0-dryrun-synthetic-mini-v1 \
  --output tmp/benchmarks/p14-0/<REDACTED_HANDLE>/synthetic-mini/report.json \
  --top-k 1,3,5,10 \
  --limit-questions 10 \
  --enable-answer-eval \
  --llm-judge-provider none
```

Common options for approved P14 planning/dry runs:

- `--timeout-seconds 60`
- `--max-retries 1`
- `--include-retrieval-details`
- `--resume-existing`
- `--isolate-per-case` for LongMemEval/LOCOMO-standard dry runs when per-case haystacks apply
- comparator controls only from approved statuses in `docs/benchmarks/phase14-service-inventory.md`

## Run-level controls and safety gates

- Comparator inclusion is driven by status in `docs/benchmarks/phase14-service-inventory.md`.
- `mem0 Cloud`, Zep, Letta, and LangGraph Store remain off until implementation and credential/dependency gates are approved.
- `--include-mem0-oss` is optional and may stay off when dependency/config is absent.
- `simple-bm25` is not included in P14-0 commands because adapter implementation is deferred to P14-1.
- No run may silently tune ShyftR between comparator runs without recording git SHA and rerunning affected baselines.

## Stop conditions

- Any backend returns unrecoverable `failed` after retry budget.
- Dry-run fixture mapping mismatch or missing manifest.
- Timeout/retry breach from runner control policy for one backend while running first 10 questions.
- Any unapproved secret path or credential is required by command.
- Any output target escapes `artifacts/`, `reports/`, or `tmp/`.

## Approval rule by dataset

- synthetic-mini: proceed with standard dry-run command once registry review is complete.
- LOCOMO-mini: proceed after synthetic-mini validation and no new runner failure class.
- LongMemEval and LOCOMO-standard: require local normalized input approval before any non-placeholder command.
- BEAM: require license/attribution review before non-private share; stay private even when converted only.

## Private-only results policy

For P14-0, records, manifests, and diagnostics are private by default. Any output is published publicly only with:

1. explicit operator approval,
2. path-safe scrubbing,
3. disclosure of data scope and limits,
4. comparator list and skipped status,
5. omitted raw private fields and secrets,
6. claim-safe wording in line with terminology gates.
