# Phase 14 P14-0 service and dataset inventory

Repo-local references:

- `2026-05-18-shyftr-phase-14-handoff-packet.md`
- `2026-05-18-shyftr-phase-14-actual-benchmark-roadmap.md`
- `docs/benchmarks/adapter-contract.md`
- `docs/benchmarks/methodology.md`
- `docs/benchmarks/README.md`
- code under `src/shyftr/benchmarks/`

This artifact records only planning and verification inventory for P14-0. It does not claim benchmark results.

## Inventory checks performed

Repository checks:

- `shyftr` and `no-memory` benchmark adapters are present in `src/shyftr/benchmarks/adapters/`.
- `mem0 OSS` adapter code is present and skip-safe in `src/shyftr/benchmarks/adapters/mem0_backend.py`.
- No simple BM25/vector, mem0 Cloud, Zep, Letta, or LangGraph Store benchmark adapters are present yet.
- Local import probe on this machine found `mem0`, `zep_cloud`, `letta_client`, and `langgraph` absent.

Public documentation references used for P14-0 posture:

- mem0 OSS repository and docs reference: `https://github.com/mem0ai/mem0`, `https://docs.mem0.ai`
- mem0 Platform/API docs: `https://docs.mem0.ai/platform/overview`, `https://docs.mem0.ai/api-reference`
- Zep docs and repository: `https://help.getzep.com`, `https://github.com/getzep/zep`
- Graphiti repository: `https://github.com/getzep/graphiti`
- Letta docs and repository: `https://docs.letta.com`, `https://github.com/letta-ai/letta`
- LangGraph docs and repository: `https://langchain-ai.github.io/langgraph/`, `https://github.com/langchain-ai/langgraph`

External setup/API details must still be rechecked immediately before any adapter implementation or paid/API-backed run.

## Comparator inventory

Comparator status vocabulary must be one of: `ready`, `install-needed`, `credential-needed`, `not-suitable`, `deferred`.

| comparator | status | repository evidence | P14-0 readiness rationale | notes |
|---|---|---|---|---|
| shyftr | ready | `src/shyftr/benchmarks/adapters/shyftr_backend.py` implements the adapter contract and CLI includes it by default. | Stable local-cell benchmark adapter already used for Phase 11/12/13 harness runs. | Required comparator for all P14 runs. |
| no-memory | ready | `src/shyftr/benchmarks/adapters/no_memory.py` is an explicit baseline adapter and CLI includes it by default. | Stable retrieval-floor comparator for each run. | Required no-memory baseline under the same runner-owned question path. |
| simple local BM25/vector baseline | deferred | No benchmark backend adapter exists under `src/shyftr/benchmarks/adapters/`; sparse retrieval primitives exist outside the benchmark adapter surface. | Comparator is required before public comparison claims, but implementation is explicitly P14-1. | Add a dependency-light local BM25 first unless vector baseline becomes simpler and deterministic. |
| mem0 OSS | install-needed | `src/shyftr/benchmarks/adapters/mem0_backend.py` exists and package import probe reports `mem0` absent. | Adapter exists but needs local package/config setup before an `ok` run on this machine. | Public docs indicate OSS can be local with local LLM/embedder/vector-store choices, or credential-backed if cloud providers are selected. |
| mem0 Cloud | credential-needed | No cloud-specific adapter currently exists in the repo. | Managed API requires explicit API credentials and project/account configuration before any run. | Keep off by default; never infer keys from ambient environment. |
| Zep | credential-needed | No adapter currently exists in the repo; import probe reports `zep_cloud` absent. | Current supported Zep posture is cloud/API-key based; legacy community edition is deprecated. | Retrieval can be isolated from agent-loop answering, but adapter and credential gate are required. Graphiti is a related OSS project, not a drop-in Zep result. |
| Letta | install-needed | No adapter currently exists in the repo; import probe reports `letta_client` absent. | Local/self-hosted and cloud modes exist, but P14 needs a benchmark adapter and careful retrieval-only mapping. | Agent-first design means direct memory retrieval must be validated before treating it as a backend-only comparator; LLM/provider credentials may be needed depending on mode. |
| LangGraph Store | install-needed | No adapter currently exists in the repo; import probe reports `langgraph` absent. | Local in-memory/SQLite-style store baselines are possible after dependency install and adapter design. | Treat as a framework baseline, not a managed memory-service claim; managed/cloud paths are credential-needed. |

## Dataset inventory

Dataset status vocabulary must be one of: `local-file-ready`, `obtain-needed`, `license-review-needed`, `deferred`.

| dataset | status | current repository readiness | gating note |
|---|---|---|---|
| synthetic-mini | local-file-ready | Deterministic builtin fixture via `synthetic_mini_fixture()` in `src/shyftr/benchmarks/fixture.py`; no download needed. | Available for comparator smoke and adapter contract checks. |
| LOCOMO-mini | local-file-ready | Checked fixture file exists as `fixtures/benchmarks/locomo_mini.fixture.json`; CLI supports `--fixture locomo-mini`. | Available for constrained local fixture runs. |
| LongMemEval | obtain-needed | Mapping converter and manifest docs exist, but no local normalized input is committed. | Requires operator-approved local LongMemEval input before conversion/run. |
| LOCOMO-standard | obtain-needed | Mapping converter exists and runner mapping path exists, but no local normalized input is committed. | Requires operator-approved local normalized LOCOMO input. |
| BEAM | license-review-needed | Converter and mapping support exist, but no BEAM files are committed and run path is not approved. | License/attribution review is required before any shared derivative artifact. |

## Adapter implementation matrix

| comparator | backend contract readiness | methods/status | dependency requirements | artifact output support | implementation owner notes |
|---|---|---|---|---|---|
| shyftr | ready | Adapter methods implemented. | local cell only | runner output guard under `artifacts/`, `reports/`, `tmp/` | Existing benchmark contract. |
| no-memory | ready | Adapter methods implemented. | none | same runner output gates | Stable no-memory comparator. |
| simple local BM25/vector baseline | deferred | not yet implemented | P14-1 design | not yet wired | First retrieval-only local comparator for P14-1. |
| mem0 OSS | adapter present / dependency absent | skip-safe adapter present | optional `mem0` package and local/cloud sub-config | runner output only | First external comparator to validate after install approval. |
| mem0 Cloud | credential-needed | not implemented | API key, endpoint/project config, cost policy | not implemented | Add only after explicit credential and cost approval. |
| Zep | credential-needed | not implemented | hosted API package/key and endpoint config | not implemented | Cloud comparator; local Graphiti alternative would need separate scope. |
| Letta | install-needed | not implemented | local/cloud server package plus possible LLM/provider config | not implemented | Validate retrieval-only memory endpoint before benchmark use. |
| LangGraph Store | install-needed | not implemented | LangGraph package/store backend config | not implemented | Framework/store baseline, not service-superiority evidence. |

## Approval checklist for P14-0 execution planning

- [ ] Confirm active branch and clean intent of repository before any benchmark run.
- [ ] Confirm comparator inventory is reviewed against current external vendor docs before adapter implementation starts.
- [ ] Confirm benchmark output directories are set to `artifacts/`, `reports/`, or `tmp/` only.
- [ ] Confirm no raw secrets are embedded in docs or command templates.
- [ ] Confirm mem0 OSS adapter dependency decision: install locally or keep skipped.
- [ ] Confirm LongMemEval and LOCOMO-standard local input acquisition approval.
- [ ] Confirm BEAM license review path and attribution requirements before any shared derivative artifact.
- [ ] Confirm LLM judge remains optional and default `--llm-judge-provider none` unless explicitly approved.
- [ ] Confirm run IDs and output artifact names are policy-compliant and redacted where private.

## P14-0 status summary

- Required baselines (`shyftr`, `no-memory`) are ready.
- `mem0 OSS` has code and skip-safe behavior; dependency install is required to make it runnable on this machine.
- Local dataset scaffolding for LongMemEval and LOCOMO-standard is ready for mapping/conversion; execution still needs approved local data.
- BEAM is blocked pending license/attribution review.
- Cloud/API-backed comparators require explicit credentials and adapter work; no result claims are made from this inventory artifact.
