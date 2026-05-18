# ShyftR May 18 frontier roadmap: comprehensive phased and tranched plan

Date: 2026-05-18
Repo: `/Users/stefan/ShyftR`
Primary input report: `May18DeepResearch+Roadmap/may18-deep-research-report.md`
Vault source note: `/Users/stefan/Documents/local wiki/Sources/ShyftR May 18 Deep Research Audit.md`
Status: execution plan. This document does not claim implementation or benchmark completion.

> For Hermes: use the ShyftR, writing-plans, and test-driven-development skills before executing this plan. Use strict RED-GREEN-REFACTOR for every behavior change. Treat the repo and ledgers as operational truth; do not use Hermes-main memory for tranche state.

## 0. Executive intent

This roadmap turns the May 18 deep research audit into an executable program.

The report's central finding is that ShyftR is already architecturally strong as a local-first, append-only, review-gated memory-cell substrate, but it is not yet justified in claiming broad superiority over Mem0 or other mature memory systems. The next work must therefore do two things at once:

1. remove correctness, privacy, CI, and performance debt that would make later research claims unsafe;
2. build the missing retrieval, consolidation, temporal, entity, conflict, benchmark, privacy, and multimodal layers needed for a genuinely frontier memory system.

The plan is intentionally phased. The first phases make the repo safe and measurable. The middle phases create the quality jumps. The later phases add frontier differentiation. Every phase includes documentation, tests, hardening, and explicit stop conditions.

## 1. Grounding and current repo truth

### 1.1 Report findings scraped into this plan

The report requires this plan to address all of the following surfaces:

- manifest/path contract inconsistency;
- CI and release gates being smoke-heavy but test-light;
- privacy redaction gaps across text and list-like fields;
- repeated lifecycle replay and retrieval-state recomputation;
- in-memory vector scans and full rebuild indexing;
- default deterministic embeddings being a test scaffold rather than production semantics;
- sqlite-vec placeholder/runtime behavior;
- lack of bitemporal valid-time, transaction-time, and supersession semantics;
- lack of entity/relation memory and graph expansion;
- continuity behaving mostly as guarded pack merging rather than a true consolidation tier;
- brittle selection policy for carry/memory merging;
- missing conflict, uncertainty, hypothesis, entailment, contradiction, and abstention handling;
- benchmark evidence limited to fixture-safe runs;
- mem0 comparator not yet producing a valid local result;
- local HTTP service lacking a hosted-production auth model;
- privacy/consent/export receipts not yet first-class;
- multimodal observation memory not yet modeled;
- need for outcome/causal memory and learned policy loops.

### 1.2 Current actual implementation baseline

Current committed baseline at plan creation:

- branch: `main` tracking `origin/main`;
- latest committed work includes Phase 14 planning and a simple BM25 baseline commit;
- Phase 14 actual standard benchmark execution has not run;
- Phase 14 service inventory and run registry docs exist;
- full standard LongMemEval, LOCOMO-standard, BEAM, real mem0 OSS, mem0 Cloud, Zep, Letta, LangGraph Store, and LLM-judge agreement runs are not yet complete.

Current uncommitted worktree caveat at plan creation:

- modified tracked files: `src/shyftr/cli.py`, `src/shyftr/layout.py`, `src/shyftr/mcp_server.py`, `src/shyftr/server.py`;
- untracked files include `blob_store.py`, `bootstrap.py`, `context_assembly.py`, `context_compaction.py`, `context_expansion.py`, and Phase-15-style tests;
- untracked report directory: `May18DeepResearch+Roadmap/`.

No implementation should start until Phase A reconciles this dirty surface. Do not overwrite it casually; it may already contain useful context-compaction work, but it is not committed, pushed, or CI-proven.

## 2. External research hardening used by this plan

Bounded current research found these practical constraints:

- Mem0's current public benchmark posture is the bar to beat: LoCoMo, LongMemEval, and BEAM claims; entity linking; BM25 + semantic + entity fusion; temporal reasoning; ADD-only extraction. URLs: `https://github.com/mem0ai/mem0`, `https://github.com/mem0ai/memory-benchmarks`, `https://mem0.ai/research`.
- LongMemEval should start with `longmemeval_s_cleaned.json` and deterministic answer/judge templates before any large run. URLs: `https://github.com/xiaowu0162/LongMemEval`, `https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned`.
- LOCOMO is small but license-sensitive; keep standard inputs private and operator-provided. URL: `https://github.com/snap-research/locomo`.
- BEAM is CC BY-SA 4.0; any report using BEAM-derived metrics needs attribution and license handling. URL: `https://huggingface.co/datasets/Mohammadta/BEAM`.
- Vector backend choices should stay local-first: sqlite-vec for simple SQLite-native baseline, LanceDB for embedded production-scale local vector storage, Qdrant Edge as a possible HNSW local option, pgvector only if a Postgres deployment becomes justified. URLs: `https://github.com/asg017/sqlite-vec`, `https://github.com/lancedb/lancedb`, `https://qdrant.tech/documentation/edge/`, `https://github.com/pgvector/pgvector`.
- Bitemporal design should separate valid time from recorded time and represent supersession explicitly. Reference: `https://martinfowler.com/articles/bitemporal-history.html`.
- Hierarchical memory systems worth borrowing from: MemMachine's working/episodic/profile split and graph-like episodic memory; TeleMem-style batch consolidation; MemFactory-style policy learning.

## 3. Program architecture

The program has ten phases. Each phase can be implemented as one or more commits. Each tranche should leave the repo in a reviewable state with exact evidence.

- Phase A: Baseline reconciliation and source-linked planning
- Phase B: Contract, CI, and privacy stabilization
- Phase C: Materialized state and incremental indexing
- Phase D: Early benchmark baseline and recurring measurement loop
- Phase E: Production retrieval substrate
- Phase F: Temporal, entity, and relation memory
- Phase G: Hierarchical consolidation engine
- Phase H: Conflict, uncertainty, and belief-state management
- Phase I: Privacy, consent, export, and local service hardening
- Phase J: Multimodal, outcome memory, and adaptive policy learning

Default sequencing rule:

1. Complete Phase A first.
2. Complete Phase B before any public-facing benchmark claims.
3. Complete enough of Phase C to make benchmark runs scale honestly.
4. Run Phase D as an early stabilized baseline measurement, not as a final victory lap.
5. Use Phase D findings to prioritize Phases E-G.
6. Re-run the relevant Phase D benchmark slices after each major retrieval, temporal/entity, consolidation, conflict, or privacy/reporting improvement.
7. Run a final end-of-program comparison pass after Phases E-J, unless the earlier recurring benchmark loop already proves no material implementation changed since the last comparable run.
8. Do Phases H-J only after the core quality and safety loops are stable.

## 4. Global guardrails

### 4.1 Safety and privacy

- Do not commit raw third-party datasets, converted private fixtures, raw judge logs, or private benchmark reports.
- Do not auto-download datasets.
- Do not infer API keys from ambient environment.
- Do not run paid or remote APIs without explicit approval.
- Do not publish superiority claims until run configuration, dataset license, comparator version, reports, and claim text are reviewed.
- Treat the HTTP service as local-first unless and until a dedicated auth/hosting phase explicitly changes that posture.
- Durable memory direct-write authority remains review-gated unless a separate policy file explicitly says otherwise.

### 4.2 Testing doctrine

Every production behavior change must follow:

1. write a focused failing regression test first;
2. run the focused test and confirm the expected failure;
3. implement the smallest production change;
4. run the focused test and adjacent tests;
5. run repo gates before closeout.

Default verification bundle from repo root:

```bash
PYTHONPATH=.:src python -m compileall -q src scripts examples
PYTHONPATH=.:src pytest -q
python scripts/terminology_inventory.py --fail-on-public-stale
python scripts/terminology_inventory.py --fail-on-capitalized-prose
python scripts/public_readiness_check.py
git diff --check
git status --short --branch
```

If full `pytest` is too slow during an inner loop, run the focused tests first, then the full bundle before tranche closeout.

### 4.3 Documentation doctrine

Every phase must update the docs nearest the changed surface. At minimum:

- `docs/concepts/...` for model/contract changes;
- `docs/benchmarks/...` for evaluation changes;
- `docs/mcp.md`, `docs/api.md`, or local API docs for surface changes;
- `README.md` only when public claim posture changes;
- a root closeout or handoff packet when a phase completes.

### 4.4 Public claim doctrine

Allowed claim before Phase D real runs:

- ShyftR is a local-first, append-only, review-gated memory substrate with fixture-safe evaluation evidence.

Forbidden claim before Phase D real runs:

- ShyftR beats Mem0 or other memory systems overall.

Allowed claim after Phase D only if reports prove it:

- On the named dataset subset, under the named configuration, ShyftR achieved the reported result against the named baselines/comparators.

## 5. Phase A — baseline reconciliation and source-linked planning

Goal: make the current repo state safe to execute from, link the May 18 report into operator knowledge, and prevent Phase 14/Phase 15 drift.

### A0. Read and freeze starting truth

Objective: record the actual starting state before modifying code.

Read first:

- `May18DeepResearch+Roadmap/may18-deep-research-report.md`
- `2026-05-18-shyftr-phase-14-actual-benchmark-roadmap.md`
- `2026-05-18-shyftr-phase-14-handoff-packet.md`
- `docs/benchmarks/phase14-service-inventory.md`
- `docs/benchmarks/phase14-run-registry.md`
- `git status --short --branch`

Steps:

1. Run `git status --short --branch` and save output in the phase closeout.
2. Run `git diff --stat` and list every dirty tracked file.
3. List untracked files with `git status --short -uall`.
4. Decide whether each dirty/untracked file is:
   - report/planning input;
   - Phase 15 context-compaction work to preserve;
   - generated artifact to ignore/remove later;
   - unrelated local scratch.

Verification:

```bash
git status --short --branch
git diff --stat
git status --short -uall
```

Stop boundary: no source mutation yet except writing this classification if a closeout/handoff file is part of the tranche.

### A1. Preserve or isolate current uncommitted Phase-15-like work

Objective: avoid losing useful context-compaction work while preventing it from contaminating the May 18 roadmap execution.

Files to inspect:

- `src/shyftr/context_compaction.py`
- `src/shyftr/context_expansion.py`
- `src/shyftr/context_assembly.py`
- `src/shyftr/blob_store.py`
- `src/shyftr/bootstrap.py`
- `tests/test_context_compaction_phase15.py`
- `tests/test_phase15_cli_mcp_integration.py`
- `tests/test_phase15_feedback_index_recommendations.py`

Steps:

1. Run focused tests for the dirty surface if feasible:

```bash
PYTHONPATH=.:src pytest -q \
  tests/test_context_compaction_phase15.py \
  tests/test_phase15_cli_mcp_integration.py \
  tests/test_phase15_feedback_index_recommendations.py
```

2. If tests pass, create a dedicated closeout note explaining what this uncommitted work proves and how it maps into Phase G/J.
3. If tests fail, record failures and decide whether to commit as WIP is forbidden; default is to leave it uncommitted and plan a clean TDD tranche later.
4. Do not stage the dirty files unless the operator explicitly chooses to preserve them now.

Verification:

```bash
PYTHONPATH=.:src python -m py_compile \
  src/shyftr/context_compaction.py \
  src/shyftr/context_expansion.py \
  src/shyftr/context_assembly.py \
  src/shyftr/blob_store.py \
  src/shyftr/bootstrap.py
```

Stop boundary: dirty work classified, not accidentally merged into unrelated phases.

### A2. Link the May 18 report into the Obsidian vault

Objective: ensure the deep report is findable from the vault before execution begins.

Already completed during plan creation:

- created `/Users/stefan/Documents/local wiki/Sources/ShyftR May 18 Deep Research Audit.md`;
- linked it from `/Users/stefan/Documents/local wiki/Projects/shyftr.md`;
- linked it from `/Users/stefan/Documents/local wiki/Notes/README.md`.

Verification:

```bash
python - <<'PY'
from pathlib import Path
for p in [
  Path('/Users/stefan/Documents/local wiki/Sources/ShyftR May 18 Deep Research Audit.md'),
  Path('/Users/stefan/Documents/local wiki/Projects/shyftr.md'),
  Path('/Users/stefan/Documents/local wiki/Notes/README.md'),
]:
    text = p.read_text()
    assert 'ShyftR May 18 Deep Research Audit' in text
    print('ok', p)
PY
```

Stop boundary: vault linked; no mass vault restructuring.

### A3. Create May 18 roadmap handoff packet

Objective: provide a short restart anchor next to this long plan.

Create:

- `2026-05-18-shyftr-may18-frontier-roadmap-handoff-packet.md`

Required content:

- current repo state and dirty-worktree caveat;
- link to this plan;
- link to May 18 report;
- next tranche: A0/A1 if not already resolved, otherwise B0;
- explicit forbidden actions: no benchmark claims, no dataset commits, no API-key use, no hosted API exposure.

Verification:

```bash
test -f 2026-05-18-shyftr-may18-frontier-roadmap-handoff-packet.md
python - <<'PY'
from pathlib import Path
p=Path('2026-05-18-shyftr-may18-frontier-roadmap-handoff-packet.md')
t=p.read_text()
for s in ['may18-frontier-roadmap', 'May18DeepResearch+Roadmap', 'dirty']:
    assert s in t
print('handoff ok')
PY
```

## 6. Phase B — contract, CI, and privacy stabilization

Goal: remove the report's immediate correctness and safety blockers.

### B0. Manifest/path contract unification

Objective: one canonical manifest resolver and one cell-id lookup path.

Likely files:

- `src/shyftr/layout.py`
- `src/shyftr/cell_manifest.py`
- `src/shyftr/provider/memory.py`
- `src/shyftr/server.py`
- `src/shyftr/mcp_server.py`
- tests near existing manifest/provider tests, or create `tests/test_cell_manifest_contract.py`

RED tests:

1. A cell initialized with `config/cell_manifest.json` is read correctly by provider memory.
2. Legacy `manifest.json` still works as compatibility input if present.
3. If both exist and disagree, canonical `config/cell_manifest.json` wins or the resolver raises a documented conflict error; pick one policy and test it.
4. Pack/provenance outputs carry the same `cell_id` after CLI, provider, MCP, and HTTP paths.

Implementation steps:

1. Create or harden `load_cell_manifest(cell_path)` and `read_cell_id(cell_path)`.
2. Replace local manifest probing in `provider/memory.py`.
3. Replace any ad-hoc manifest reads in CLI/MCP/server paths.
4. Document the manifest path in `docs/concepts/cells.md` or nearest current cell-layout doc.

Focused verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_cell_manifest_contract.py
PYTHONPATH=.:src pytest -q tests/test_memory_provider.py tests/test_mcp_server.py tests/test_server.py
```

Stop boundary: manifest resolution unified; no unrelated storage migration.

### B1. CI pytest and coverage gate

Objective: CI must run the real test suite, not only smoke gates.

Likely files:

- `.github/workflows/ci.yml`
- `pyproject.toml` if coverage config is needed
- `scripts/release_gate.sh` if the release gate should also run a focused test slice
- `docs/development.md` or `docs/benchmarks/README.md` for verification expectations

RED test / proof:

1. Inspect CI workflow and prove no pytest step currently exists.
2. Add a local workflow lint or text assertion test if the repo already has CI config tests.

Implementation steps:

1. Add `PYTHONPATH=.:src pytest -q --maxfail=1` to CI.
2. Add coverage upload only if existing CI secrets/actions support it; otherwise generate local XML as a non-uploaded artifact.
3. Keep smoke gates; do not replace them.
4. Document local command parity.

Focused verification:

```bash
python - <<'PY'
from pathlib import Path
ci=Path('.github/workflows/ci.yml').read_text()
assert 'pytest' in ci
assert 'PYTHONPATH=.:src' in ci or 'PYTHONPATH' in ci
print('ci pytest gate present')
PY
PYTHONPATH=.:src pytest -q --maxfail=1
```

Stop boundary: test gate added; no benchmark execution yet.

### B2. Privacy redaction expansion

Objective: widen redaction so all user-visible/exportable projections scrub sensitive fields consistently.

Likely files:

- `src/shyftr/privacy.py`
- `src/shyftr/pack.py`
- `src/shyftr/provider/memory.py`
- `src/shyftr/server.py`
- `src/shyftr/mcp_server.py`
- tests near privacy/export/pack behavior, or create `tests/test_privacy_redaction_contract.py`

RED tests:

1. Sensitive/private records redact `statement`, `rationale`, `summary`, `title`, `content`, and `source_excerpt` in non-audit exports.
2. List-like fields `tags`, `grounding_refs`, `artifact_refs`, and `evidence_refs` are redacted or replaced according to policy when sensitivity requires it.
3. Nested mappings and lists are recursively scrubbed.
4. Audit-mode export preserves allowed unredacted data only when explicitly requested.
5. Pack/loadout assembly cannot leak raw sensitive text through candidate metadata.

Implementation steps:

1. Add named constants for redacted text and list fields.
2. Harden recursive redaction for lists of strings and dictionaries.
3. Apply redaction at downstream assembly edges, not only direct export helpers.
4. Document audit mode versus normal projection mode.

Focused verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_privacy_redaction_contract.py
PYTHONPATH=.:src pytest -q tests/test_privacy.py tests/test_pack.py tests/test_memory_provider.py
```

Stop boundary: redaction widened; encryption/consent receipts deferred to Phase I.

### B3. Public readiness and vocabulary gate reconciliation

Objective: keep the public product surface coherent after B0-B2.

Likely files:

- `README.md`
- `docs/concepts/implementation-guardrails.md`
- `docs/concepts/storage-retrieval-learning.md`
- `docs/concepts/runtime-integration-contract.md`
- `scripts/terminology_inventory.py` only if classification is wrong, not to hide real issues

Steps:

1. Run terminology gates before docs changes and record any pre-existing failures.
2. Patch docs to reflect new manifest, CI, and redaction truth.
3. Avoid broad superiority claims.
4. Keep legacy aliases only in compatibility notes.

Verification:

```bash
python scripts/terminology_inventory.py --fail-on-public-stale
python scripts/terminology_inventory.py --fail-on-capitalized-prose
python scripts/public_readiness_check.py
git diff --check
```

## 7. Phase C — materialized state and incremental indexing

Goal: stop replaying the entire ledger/index stack on every retrieval-heavy operation.

### C0. Effective lifecycle state materializer

Objective: persist and update effective lifecycle state keyed by ledger-head fingerprints.

Likely files:

- `src/shyftr/ledger_state.py`
- `src/shyftr/mutations.py`
- `src/shyftr/pack.py`
- `src/shyftr/provider/memory.py`
- `src/shyftr/layout.py`
- `src/shyftr/store/sqlite.py`
- create `tests/test_effective_state_materializer.py`

RED tests:

1. Active memory IDs computed from materialized state match replayed ledger state.
2. A lifecycle event append updates only affected state rows.
3. Ledger-head fingerprint mismatch triggers rebuild.
4. Corrupt or partial materialized state fails safe by rebuilding from ledgers.
5. Read-only pack retrieval does not append state rows unless explicit refresh is needed and policy allows it.

Implementation steps:

1. Add a state artifact under a clearly named cell state path.
2. Define state row schema: memory id, lifecycle status, confidence, trust tier, timestamps, ledger offsets, head fingerprint.
3. Add rebuild and incremental refresh helpers.
4. Route pack/provider active-state queries through the helper.
5. Keep raw ledgers canonical.

Focused verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_effective_state_materializer.py
PYTHONPATH=.:src pytest -q tests/test_mutations.py tests/test_pack.py tests/test_memory_provider.py
```

Stop boundary: effective state materialized; no vector backend change yet.

### C1. Incremental sparse index refresh

Objective: avoid full SQLite FTS rebuilds when only new rows changed.

Likely files:

- `src/shyftr/retrieval/sparse.py`
- `src/shyftr/ledger.py`
- `src/shyftr/layout.py`
- `src/shyftr/retrieval/hybrid.py`
- create `tests/test_incremental_sparse_index.py`

RED tests:

1. First build indexes all approved rows.
2. Appending one row indexes only the new row.
3. Updating lifecycle state removes or suppresses inactive rows from search results.
4. Index offset/fingerprint mismatch triggers safe rebuild.
5. Quoted FTS queries remain safe and do not raise SQLite MATCH syntax errors.

Implementation steps:

1. Store index metadata: ledger path, last byte offset or row count, content hash, index version.
2. Add incremental append path.
3. Add forced rebuild flag for CLI and tests.
4. Document index truth: acceleration only, never canonical.

Focused verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_incremental_sparse_index.py tests/test_retrieval_sparse.py
```

### C2. Incremental vector index refresh and backend registry

Objective: define a backend registry that can support deterministic vectors, sqlite-vec, LanceDB, and future Qdrant without changing pack code.

Likely files:

- `src/shyftr/retrieval/vector.py`
- `src/shyftr/retrieval/embeddings.py`
- `src/shyftr/retrieval/lancedb_adapter.py`
- optional new `src/shyftr/retrieval/backends.py`
- create `tests/test_vector_backend_registry.py`

RED tests:

1. Deterministic backend remains default in tests and no-dependency mode.
2. Missing optional backend reports `skipped` or `not_available`, not a runtime crash in normal optional paths.
3. Backend metadata records provider name, embedding model, dimension, index type, and dependency version when available.
4. Query results include backend metadata in benchmark reports.
5. Reindexing one appended memory does not rebuild all vectors when backend supports incremental append.

Implementation steps:

1. Define backend capability flags: `supports_incremental`, `supports_metadata_filter`, `supports_ann`, `supports_persistence`.
2. Wrap existing deterministic and LanceDB paths behind the registry.
3. Implement sqlite-vec as optional baseline only if dependency is present; otherwise skip cleanly.
4. Keep Qdrant Edge deferred until Phase E unless a spike proves it is low-friction.

Focused verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_vector_backend_registry.py tests/test_retrieval_vector.py tests/test_retrieval_lancedb.py
```

### C3. Live-context active-set and freshness index

Objective: make live-context pack/checkpoint generation scale beyond full session scans.

Likely files:

- `src/shyftr/live_context.py`
- `src/shyftr/continuity.py`
- `src/shyftr/layout.py`
- tests near live context/continuity

RED tests:

1. Active-set index matches full-scan pack output for a small fixture.
2. Closing/resolving an entry removes it from active pack candidates.
3. Freshness/priority order is stable and deterministic.
4. Rebuild occurs if active-set metadata is stale.
5. Continuity pack still prioritizes carry/checkpoint entries over ordinary durable memory where policy says so.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_live_context.py tests/test_continuity.py
```

## 8. Phase D — early benchmark baseline and recurring measurement loop

Goal: create defensible evidence early enough to steer the roadmap, then keep reusing the same measurement harness after each major improvement. Phase D is not the final benchmark-only phase; it is the measurement backbone for Phases E-J.

This phase extends the existing Phase 14 roadmap, not replaces it. If Phase 14 artifacts are already partly complete, preserve them and update their status honestly.

Phase D has three roles:

1. establish the first stabilized baseline after Phases B/C, before retrieval/consolidation rewrites;
2. produce the measured gap taxonomy that prioritizes Phases E-G/H;
3. provide repeatable benchmark slices that must be re-run after meaningful retrieval, temporal/entity, consolidation, conflict, privacy/reporting, or multimodal/policy changes.

Do not postpone all benchmarking until the end. Waiting until the end would hide which improvements actually moved the metrics. Do not benchmark immediately on a dirty or pre-stabilized worktree either; the early baseline starts only after Phase A is reconciled and Phase B plus the minimal Phase C prerequisites are complete.

### D0. Phase 14 registry refresh after B/C changes

Objective: update the service inventory and run registry with actual local truth after stabilization.

Files:

- `docs/benchmarks/phase14-service-inventory.md`
- `docs/benchmarks/phase14-run-registry.md`
- `2026-05-18-shyftr-phase-14-actual-benchmark-roadmap.md` if status needs correction

Steps:

1. Record current ShyftR SHA and dirty/clean status.
2. Record installed local comparator dependencies.
3. Record dataset availability without committing private paths.
4. Assign run IDs for fixture, LongMemEval dry/scaled, LOCOMO dry/scaled, BEAM small.

Verification:

```bash
python - <<'PY'
from pathlib import Path
for p in ['docs/benchmarks/phase14-service-inventory.md','docs/benchmarks/phase14-run-registry.md']:
    t=Path(p).read_text()
    assert 'run' in t.lower()
    assert 'mem0' in t.lower()
    print('ok', p)
PY
```

### D1. Simple BM25/vector baseline proof

Objective: prove ShyftR beats or does not beat a simple retrieval-only baseline before comparing to memory services.

Likely files:

- `src/shyftr/benchmarks/adapters/simple_bm25.py`
- optional `src/shyftr/benchmarks/adapters/simple_vector.py`
- `src/shyftr/benchmarks/runner.py`
- `scripts/run_memory_benchmark.py`
- `tests/test_benchmark_simple_baseline.py`

RED tests:

1. Baseline adapter supports reset, ingest, search, and stats under the base adapter contract.
2. Runner can include ShyftR, no-memory, and simple baseline in one report.
3. Report metadata distinguishes retrieval-only baseline from memory-system comparator.
4. Empty corpus behavior is deterministic.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_simple_baseline.py tests/test_benchmark_adapter_contract.py
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-name synthetic-mini \
  --run-id phaseD-simple-baseline-smoke \
  --output reports/benchmarks/phaseD-simple-baseline-smoke.json \
  --include-simple-bm25 \
  --top-k-cutoffs 1,3,5 \
  --enable-answer-eval
```

Stop boundary: public-safe fixture reports only.

### D2. mem0 OSS comparator real local fixture run

Objective: replace skipped mem0 comparator status with a real ok/skip/not-suitable result.

Likely files:

- `src/shyftr/benchmarks/adapters/mem0_backend.py`
- `docs/benchmarks/phase14-service-inventory.md`
- `tests/test_benchmark_mem0_backend.py`

RED tests:

1. Missing mem0 dependency reports `skipped` with reason and version fields empty.
2. Installed mem0 path records package version, config, retrieval mode, and whether entity/BM25 features are active.
3. Runner cannot silently compare against a degraded mem0 mode without metadata disclosure.
4. mem0 results use runner-owned answer/judge, not mem0's own answer generation.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_mem0_backend.py
# Only after explicit local environment approval:
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-name synthetic-mini \
  --run-id phaseD-mem0-oss-fixture \
  --output reports/benchmarks/phaseD-mem0-oss-fixture.json \
  --include-mem0-oss \
  --include-simple-bm25 \
  --top-k-cutoffs 1,3,5 \
  --enable-answer-eval
```

Stop boundary: no paid/cloud mem0 and no public superiority claim.

### D3. LongMemEval dry and scaled runs

Objective: first real standard-dataset path.

Prerequisite: operator-provided local LongMemEval path. No auto-download.

Likely files:

- `src/shyftr/benchmarks/datasets/longmemeval.py`
- `scripts/convert_longmemeval_fixture.py` if present/current
- `docs/benchmarks/p12-1-longmemeval-mapping.md`
- `docs/benchmarks/phase14-run-registry.md`

Steps:

1. Convert local `longmemeval_s_cleaned.json` into ignored artifact path.
2. Run 10-question dry run.
3. If stable, run 50-question and 200-question scaled runs.
4. Do not run full set until scaled reports are reviewed.
5. Add question-class breakdown: single-session, preference, temporal, knowledge-update, multi-session, abstention.

Verification command shape:

```bash
PYTHONPATH=.:src python scripts/run_memory_benchmark.py \
  --fixture-path artifacts/benchmarks/<RUN_ID>.longmemeval.fixture.json \
  --fixture-format shyftr-fixture \
  --run-id <RUN_ID>-longmemeval-dryrun \
  --output reports/benchmarks/<RUN_ID>-longmemeval-dryrun.json \
  --top-k-cutoffs 1,3,5,10 \
  --limit-questions 10 \
  --isolate-per-case \
  --timeout-seconds 300 \
  --max-retries 2 \
  --resume-existing \
  --enable-answer-eval \
  --allow-private-fixture
```

Stop boundary: results are private until reviewed.

### D4. LOCOMO dry/scaled runs

Objective: test multi-session and temporal conversation memory.

Prerequisite: operator-provided local LOCOMO path and license review.

Steps:

1. Reuse mapping/conversion scaffolds.
2. Run dry 10-question subset.
3. Compare ShyftR/no-memory/simple baseline/mem0 OSS if available.
4. Produce failure taxonomy: temporal miss, entity resolution miss, stale fact, support gap, answerer gap, privacy block, timeout.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_locomo_standard_mapping.py tests/test_benchmark_locomo_mini_fixture.py
```

Run commands mirror D3 with LOCOMO fixture path and run ID.

### D5. BEAM small subset with license-safe reporting

Objective: test scale and ability-class breakdown without license mistakes.

Prerequisite: local BEAM path and explicit CC BY-SA 4.0 attribution in any report summary.

Steps:

1. Confirm the report schema can carry license metadata.
2. Run smallest private BEAM subset.
3. Summarize by memory ability category.
4. Do not commit BEAM-derived private raw outputs unless license/public review approves.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_beam_standard_mapping.py tests/test_benchmark_phase13_runner_controls.py
python - <<'PY'
from pathlib import Path
schema=Path('docs/benchmarks/report-schema.md').read_text().lower()
assert 'license' in schema or 'attribution' in schema
print('license metadata documented')
PY
```

### D6. Benchmark-driven improvement backlog

Objective: convert measured failures into implementation backlog, not marketing copy.

Create/update:

- `docs/benchmarks/phase14-improvement-backlog.md`

Required categories:

- retrieval representation gap;
- entity linking gap;
- temporal reasoning gap;
- stale/superseded fact gap;
- support coverage gap;
- answerer/judge limitation;
- privacy/export block;
- latency/indexing bottleneck;
- comparator fairness caveat.

Verification:

```bash
test -f docs/benchmarks/phase14-improvement-backlog.md
python - <<'PY'
from pathlib import Path
t=Path('docs/benchmarks/phase14-improvement-backlog.md').read_text().lower()
for s in ['retrieval', 'entity', 'temporal', 'privacy', 'latency']:
    assert s in t
print('backlog shape ok')
PY
```

### D7. Recurring and final comparison passes

Objective: make benchmark timing explicit so early measurement steers the work and final measurement validates the program.

Recurring benchmark rule:

- After Phase E, re-run the retrieval-focused benchmark slice: synthetic-mini, LOCOMO-mini, LongMemEval dry/scaled if available, plus ShyftR/no-memory/simple baseline/mem0 OSS where available.
- After Phase F, re-run temporal/entity-heavy slices: LongMemEval temporal and knowledge-update classes, LOCOMO temporal/entity questions, and any relation-fixture tests.
- After Phase G, re-run continuity/consolidation-sensitive slices and compare pack compactness, useful context per token, and support coverage.
- After Phase H, re-run contradiction/knowledge-update/conflict slices and report abstention or uncertainty behavior separately from plain accuracy.
- After Phase I, re-run safety/privacy/reporting gates and any benchmark reports affected by redaction, consent, retention, export, or API posture changes.
- After Phase J, run multimodal/policy-specific fixtures only if those capabilities actually landed.

Final comparison pass:

Run a final end-of-program comparison if any material retrieval, temporal/entity, consolidation, conflict, privacy/reporting, multimodal, or policy behavior changed after the last comparable benchmark run.

The final pass should include, as available and approved:

- ShyftR current HEAD;
- no-memory baseline;
- simple BM25/vector baseline;
- mem0 OSS with version/config disclosure;
- LongMemEval dry/scaled or full approved local run;
- LOCOMO dry/scaled run;
- BEAM small subset with CC BY-SA 4.0 attribution metadata;
- pre/post comparison against the earliest Phase D stabilized baseline.

The final pass is not needed only if the recurring loop already produced an equivalent comparison after the last material implementation change and no public claim/report needs a fresh end-of-program bundle.

Create/update:

- `docs/benchmarks/final-comparison-report.md` or a private ignored equivalent if reports cannot be public;
- `docs/benchmarks/phase14-improvement-backlog.md` with resolved, improved, unchanged, and deferred categories.

Verification:

```bash
python - <<'PY'
from pathlib import Path
p=Path('docs/benchmarks/phase14-improvement-backlog.md')
assert p.exists()
t=p.read_text().lower()
for s in ['resolved', 'improved', 'unchanged', 'deferred']:
    assert s in t
print('final comparison backlog categories ok')
PY
```

## 9. Phase E — production retrieval substrate

Goal: close the quality gap with modern memory systems without sacrificing local-first auditability.

### E0. Embedding provider contract

Objective: separate test embeddings from real embeddings and make report metadata honest.

Likely files:

- `src/shyftr/retrieval/embeddings.py`
- `src/shyftr/retrieval/vector.py`
- `src/shyftr/benchmarks/runner.py`
- `tests/test_embedding_provider_contract.py`

RED tests:

1. Default deterministic provider declares `quality='test'` or equivalent metadata.
2. Real provider requires explicit selection and cannot be implied by ambient credentials.
3. Provider metadata appears in pack/debug and benchmark reports.
4. Dimension mismatch fails with a clear error.
5. Redacted/private text is not sent to remote embedding providers unless explicit policy allows it.

Implementation steps:

1. Define provider interface with `embed(texts)`, `metadata()`, and `privacy_mode`.
2. Keep deterministic default for tests.
3. Add local model/provider integration only after explicit dependency choice.
4. Document provider trust and privacy rules.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_embedding_provider_contract.py tests/test_retrieval_vector.py
```

### E1. sqlite-vec local baseline adapter

Objective: implement sqlite-vec as an optional local vector baseline where available.

RED tests:

1. Missing sqlite-vec dependency reports skipped.
2. Installed sqlite-vec adapter ingests/searches fixture records.
3. Adapter records extension/version metadata.
4. Adapter never becomes default until explicitly selected.

Likely files:

- `src/shyftr/retrieval/sqlite_vec_adapter.py`
- `src/shyftr/benchmarks/adapters/simple_vector.py`
- `tests/test_sqlite_vec_adapter.py`

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_sqlite_vec_adapter.py
```

### E2. LanceDB production-scale local backend hardening

Objective: make existing optional LanceDB path viable for larger local cells.

RED tests:

1. Missing LanceDB reports skipped.
2. Installed LanceDB persists vectors across process restart.
3. Metadata filtering by memory type, trust tier, sensitivity, and lifecycle state works.
4. Benchmark reports index type and row count.
5. Rebuild and incremental append produce equivalent top-k on fixture.

Likely files:

- `src/shyftr/retrieval/lancedb_adapter.py`
- `tests/test_retrieval_lancedb.py`
- `docs/concepts/storage-retrieval-learning.md`

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_retrieval_lancedb.py
```

### E3. Qdrant Edge spike and adapter decision

Objective: decide whether Qdrant Edge earns inclusion.

Create:

- `docs/research/qdrant-edge-spike.md`

Rules:

- no Docker requirement for the spike;
- no cloud sync;
- compare against LanceDB and sqlite-vec on install friction, persistence, metadata filtering, HNSW quality, and local-first fit;
- do not add production adapter unless spike proves value.

Verification:

```bash
test -f docs/research/qdrant-edge-spike.md
```

### E4. Hybrid reranker upgrade

Objective: make retrieval fusion explicit and tunable without hidden heuristics.

Likely files:

- `src/shyftr/retrieval/hybrid.py`
- `src/shyftr/metrics.py`
- `tests/test_hybrid_reranker_contract.py`

RED tests:

1. BM25 lower-is-better scores are normalized correctly.
2. Dense, sparse, entity, temporal, trust, confidence, freshness, and negative-space signals are visible in debug output.
3. Weight config is versioned and reported.
4. Same inputs produce deterministic order.
5. Reranker can be evaluated offline against fixture relevance labels.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_hybrid_reranker_contract.py tests/test_benchmark_metrics.py
```

## 10. Phase F — temporal, entity, and relation memory

Goal: add the missing structures that make long-horizon memory accurate.

### F0. Bitemporal schema fields

Objective: add valid-time and supersession fields compatibly.

Likely files:

- `src/shyftr/models.py`
- `src/shyftr/mutations.py`
- `src/shyftr/provider/memory.py`
- `src/shyftr/episodes.py`
- `tests/test_bitemporal_memory_contract.py`

Fields to introduce compatibly:

- `valid_from`
- `valid_until`
- `recorded_at` or existing ledger timestamp normalization
- `supersedes`
- `superseded_by`
- `temporal_confidence`
- optional `time_scope` for current/past/future query hints

RED tests:

1. Existing ledgers without fields still load.
2. New records can carry valid interval and supersession references.
3. Superseded record is still auditable but not selected for current-state queries by default.
4. Historical query can retrieve the previously valid record.
5. Episode records carry temporal anchors separately from durable semantic memory.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_bitemporal_memory_contract.py tests/test_models.py tests/test_episodes.py
```

### F1. Temporal query parser and interval index

Objective: answer current/past/future intent without relying on plain text relevance.

Likely files:

- `src/shyftr/retrieval/temporal.py`
- `src/shyftr/retrieval/hybrid.py`
- `src/shyftr/pack.py`
- `tests/test_temporal_retrieval.py`

RED tests:

1. Query "what is true now" suppresses superseded records.
2. Query "what was true on DATE" retrieves valid interval records.
3. Future-dated planned facts do not pollute current-state packs.
4. Missing valid-time falls back conservatively.
5. Report/debug output explains temporal filtering.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_temporal_retrieval.py
```

### F2. Entity extraction and canonical IDs

Objective: support person/place/tool/project/entity continuity across memories.

Likely files:

- `src/shyftr/entities.py`
- `src/shyftr/models.py`
- `src/shyftr/retrieval/hybrid.py`
- `tests/test_entity_memory_contract.py`

RED tests:

1. Entity records have stable canonical IDs and aliases.
2. Memory records can reference entity IDs without duplicating entity text.
3. Entity linking is deterministic for exact/alias cases.
4. Ambiguous entity matches create review-gated candidates rather than silent merges.
5. Entity metadata participates in retrieval scoring and debug output.

Implementation steps:

1. Start with deterministic local exact/alias linking.
2. Add optional embedding-based linking only after deterministic contract passes.
3. Keep entity merge review-gated.
4. Document entity IDs as local cell artifacts, not global identity claims.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_entity_memory_contract.py
```

### F3. Relation graph sidecar

Objective: model relationships without turning canonical ledgers into an opaque graph store.

Likely files:

- `src/shyftr/relations.py`
- `src/shyftr/retrieval/graph.py`
- `src/shyftr/layout.py`
- `tests/test_relation_graph_sidecar.py`

RED tests:

1. Relations append as review-gated records.
2. Neighbor expansion is bounded by hop count and trust tier.
3. Relation graph can rebuild from canonical ledgers.
4. Deleted/superseded memory suppresses relation expansion unless historical mode is requested.
5. Pack output explains which relations expanded retrieval.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_relation_graph_sidecar.py
```

### F4. Temporal/entity benchmark slice

Objective: measure whether F0-F3 improve actual failures.

Steps:

1. Re-run LongMemEval temporal/knowledge-update slices.
2. Re-run LOCOMO temporal/entity-heavy questions.
3. Compare against pre-F results.
4. Add results to improvement backlog.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_metrics.py
```

## 11. Phase G — hierarchical consolidation engine

Goal: turn live context/carry/continuity/episodic/durable memory into an explicit consolidation pipeline.

### G0. Consolidation contract and state machine

Objective: define tier transitions and review gates.

Likely files:

- `src/shyftr/consolidation.py`
- `src/shyftr/live_context.py`
- `src/shyftr/continuity.py`
- `src/shyftr/episodes.py`
- `src/shyftr/provider/memory.py`
- `tests/test_consolidation_contract.py`

State path:

```text
live context entry
  -> carry checkpoint item
  -> episodic capture
  -> semantic/procedural/rule proposal
  -> reviewed durable memory
```

RED tests:

1. Session-close harvest can propose an episode without directly writing durable memory.
2. Repeated similar episode captures cluster into one semantic proposal.
3. Errors/recoveries/tool outcomes cluster into procedural proposals.
4. Review rejection prevents durable write but leaves audit trail.
5. Direct durable memory remains disabled unless explicit policy allows it.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_consolidation_contract.py tests/test_live_context.py tests/test_continuity.py tests/test_episodes.py
```

### G1. Retention clocks and promotion triggers

Objective: make promotion/demotion explicit instead of heuristic.

Likely files:

- `src/shyftr/consolidation.py`
- `src/shyftr/policy.py`
- `src/shyftr/live_context.py`
- `tests/test_consolidation_retention.py`

RED tests:

1. Live entries expire or archive according to retention hint.
2. High-confidence repeated entries become promotion candidates.
3. Low-confidence or contradicted entries stay episodic/hypothesis-only.
4. Recent carry items remain available across compaction without becoming durable memory.
5. Promotion triggers are visible in proposal metadata.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_consolidation_retention.py
```

### G2. Batch retrieve-cluster-summarize-validate-review

Objective: implement the TeleMem-style consolidation pattern safely.

Likely files:

- `src/shyftr/consolidation.py`
- `src/shyftr/retrieval/hybrid.py`
- `src/shyftr/evolution.py`
- `tests/test_consolidation_batch_pipeline.py`

RED tests:

1. Batch job clusters related episodes deterministically in no-LLM mode.
2. Summary/proposal includes supporting episode IDs and confidence.
3. Proposal validation rejects unsupported claims.
4. Manual/review-gated acceptance writes durable memory append-only.
5. Generated proposals are bounded in token/size and do not include raw private text in normal reports.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_consolidation_batch_pipeline.py tests/test_evolution.py
```

### G3. Context compaction worktree reconciliation

Objective: map existing uncommitted context-compaction files into the formal consolidation contract.

Inputs:

- `src/shyftr/context_compaction.py`
- `src/shyftr/context_expansion.py`
- `src/shyftr/context_assembly.py`
- `src/shyftr/blob_store.py`
- `src/shyftr/bootstrap.py`
- phase15 tests

Steps:

1. Rebase the useful code against G0-G2 contracts.
2. Delete or rewrite any code that bypasses review gates.
3. Ensure blob externalization preserves hashes and provenance.
4. Ensure expansion/grep/describe surfaces do not leak private text without policy.
5. Add CLI/MCP/HTTP tests only after core contract tests are green.

Verification:

```bash
PYTHONPATH=.:src pytest -q \
  tests/test_consolidation_contract.py \
  tests/test_context_compaction_phase15.py \
  tests/test_phase15_cli_mcp_integration.py \
  tests/test_phase15_feedback_index_recommendations.py
```

Stop boundary: context compaction is either integrated under the contract or left as explicitly deferred scratch.

### G4. Causal outcome memory

Objective: store action → context → outcome trajectories and distill procedural patterns.

Likely files:

- `src/shyftr/outcomes.py`
- `src/shyftr/episodes.py`
- `src/shyftr/consolidation.py`
- `tests/test_causal_outcome_memory.py`

RED tests:

1. Tool/action outcome episodes carry action, context, result, verification, and failure mode.
2. Multiple similar outcomes propose a procedural pattern.
3. Harmful outcomes suppress risky procedural suggestions.
4. Outcome trajectory is retrievable separately from stable semantic facts.
5. Feedback can improve or demote a procedural pattern.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_causal_outcome_memory.py tests/test_outcomes.py
```

## 12. Phase H — conflict, uncertainty, and belief-state management

Goal: prevent memory from collapsing contradictions into whichever string was most recently retrieved.

### H0. Claim/hypothesis model

Objective: represent competing claims without prematurely choosing one.

Likely files:

- `src/shyftr/belief.py`
- `src/shyftr/models.py`
- `src/shyftr/mutations.py`
- `tests/test_belief_state_contract.py`

Fields/concepts:

- claim ID;
- claim text or memory reference;
- status: supported, contradicted, uncertain, superseded, rejected;
- confidence and uncertainty budget;
- supporting memory IDs;
- contradicting memory IDs;
- abstention policy.

RED tests:

1. Two contradictory memories create competing claim records rather than one silent winner.
2. Retrieval can return an uncertainty/abstention result for unresolved conflict.
3. Review can mark one claim preferred without deleting the other.
4. Supersession differs from contradiction.
5. Belief records rebuild from append-only ledgers.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_belief_state_contract.py
```

### H1. Entailment/contradiction edge proposals

Objective: detect and propose relation edges between claims.

Likely files:

- `src/shyftr/belief.py`
- `src/shyftr/evolution.py`
- `src/shyftr/retrieval/hybrid.py`
- `tests/test_claim_edge_proposals.py`

RED tests:

1. Exact negation fixture creates contradiction proposal.
2. Same claim restatement creates entailment/support proposal.
3. Ambiguous overlap creates unknown/needs-review edge.
4. Accepted edge affects retrieval explanation.
5. Rejected edge remains audit-visible but inactive.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_claim_edge_proposals.py
```

### H2. Abstention-first pack policy

Objective: when high-risk conflict exists, packs should expose uncertainty instead of pretending certainty.

Likely files:

- `src/shyftr/pack.py`
- `src/shyftr/provider/memory.py`
- `src/shyftr/belief.py`
- `tests/test_abstention_pack_policy.py`

RED tests:

1. Conflicted claim yields pack item with uncertainty metadata.
2. High-sensitivity conflicting data cannot leak raw text in normal mode.
3. Rule memory can force abstention for unresolved conflicts.
4. Runtime feedback on abstention updates usefulness signals.
5. No-conflict paths remain unchanged.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_abstention_pack_policy.py tests/test_pack.py
```

### H3. Conflict benchmark slice

Objective: add synthetic and standard-dataset conflict/knowledge-update measurement.

Steps:

1. Add contradiction-resolution fixture cases.
2. Map LongMemEval knowledge-update and BEAM contradiction-resolution categories.
3. Report stale retrieval and contradiction-resolution separately.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_benchmark_metrics.py tests/test_benchmark_answerer_judge.py
```

## 13. Phase I — privacy, consent, export, and local service hardening

Goal: make ShyftR's governance advantage concrete.

### I0. Export receipts and audit trail

Objective: record who exported what, when, under what policy, and with what content hash.

Likely files:

- `src/shyftr/privacy.py`
- `src/shyftr/export.py`
- `src/shyftr/layout.py`
- `src/shyftr/cli.py`
- `tests/test_export_receipts.py`

RED tests:

1. Export creates a receipt with timestamp, policy, sensitivity filter, exporter identity, output hash, and item count.
2. Dry-run export does not create a receipt unless explicitly requested.
3. Receipt does not leak redacted private content.
4. Re-running export with same content produces same content hash but distinct receipt event.
5. Receipt ledger rebuild is append-only.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_export_receipts.py tests/test_privacy.py
```

### I1. Consent and retention clocks

Objective: model per-scope permission and retention without full hosted auth.

Likely files:

- `src/shyftr/privacy.py`
- `src/shyftr/policy.py`
- `src/shyftr/models.py`
- `tests/test_consent_retention_policy.py`

RED tests:

1. Record with expired retention is excluded from normal export/retrieval.
2. Consent scope limits pack/export surfaces.
3. Audit mode can explain exclusion without revealing content.
4. Retention updates append lifecycle events, not overwrites.
5. Benchmark reports disclose privacy exclusions as support-coverage caveats.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_consent_retention_policy.py
```

### I2. Field-level encryption spike and decision

Objective: decide whether to implement encryption now or keep as future work.

Create:

- `docs/research/field-level-encryption-decision.md`

Compare:

- local keyring;
- passphrase-derived local key;
- age/libsodium sealed boxes;
- SQLite/Parquet/object-snapshot interaction;
- backup/export implications.

Stop boundary: decision doc only unless explicit approval moves to implementation.

Verification:

```bash
test -f docs/research/field-level-encryption-decision.md
```

### I3. Local HTTP auth boundary

Objective: keep the local API honest: either explicitly local-only or protected for non-local binding.

Likely files:

- `src/shyftr/server.py`
- `docs/api.md` or current local API docs
- `SECURITY.md`
- `tests/test_local_api_auth_boundary.py`

RED tests:

1. Default bind remains localhost.
2. Non-local bind without explicit unsafe flag or auth config fails fast.
3. Protected write/export endpoints require local token when auth is enabled.
4. CORS cannot silently open broad origins in non-local mode.
5. Docs warn that current service is not hosted multi-tenant.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_local_api_auth_boundary.py tests/test_server.py
```

## 14. Phase J — multimodal, outcome memory, and adaptive policy learning

Goal: add frontier extensions only after the core state/retrieval/benchmark/governance loop is stable.

### J0. Observation object model

Objective: represent files, screenshots, audio, video, and other artifacts without dumping blobs into memory text.

Likely files:

- `src/shyftr/observations.py`
- `src/shyftr/models.py`
- `src/shyftr/blob_store.py` if accepted from Phase G
- `src/shyftr/episodes.py`
- `tests/test_observation_object_model.py`

RED tests:

1. Observation object stores handle, MIME/type, hash, size, sensitivity, provenance, and optional embedding references.
2. Episode can anchor observations without copying raw blobs.
3. Export can include or exclude observations by policy.
4. Missing blob/handle fails safe and remains audit-visible.
5. Pack includes observation summaries only when policy allows.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_observation_object_model.py
```

### J1. Multimodal embedding hooks

Objective: add adapter seams for image/audio/file embeddings without hard dependency or privacy leaks.

RED tests:

1. Missing multimodal embedding provider reports skipped.
2. Provider metadata and privacy mode are recorded.
3. Sensitive observation cannot be sent to remote provider without explicit policy.
4. Cross-modal retrieval can be disabled by default.
5. Text-only ShyftR behavior remains unchanged.

Likely files:

- `src/shyftr/retrieval/multimodal.py`
- `src/shyftr/observations.py`
- `tests/test_multimodal_retrieval_contract.py`

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_multimodal_retrieval_contract.py
```

### J2. Feedback-driven selection policy baseline

Objective: use existing pack feedback to tune retrieval/consolidation policy in a deterministic, reviewable way before RL.

Likely files:

- `src/shyftr/feedback.py`
- `src/shyftr/outcomes.py`
- `src/shyftr/retrieval/hybrid.py`
- `src/shyftr/consolidation.py`
- `tests/test_feedback_selection_policy.py`

RED tests:

1. Useful feedback increases future selection score within bounded limits.
2. Harmful feedback decreases or quarantines memory according to policy.
3. Missing-memory feedback creates proposal candidates.
4. Policy changes are versioned and reversible.
5. Offline replay reproduces the same recommendations.

Verification:

```bash
PYTHONPATH=.:src pytest -q tests/test_feedback_selection_policy.py tests/test_feedback.py tests/test_outcomes.py
```

### J3. Learned policy research spike

Objective: decide whether a MemFactory-style learned policy belongs in the public repo, private core, or future research lane.

Create:

- `docs/research/learned-memory-policy-spike.md`

Required sections:

- what existing feedback signals can train;
- what would be private-core versus public-safe;
- how to avoid optimizing toward benchmark overfit;
- offline replay/evaluation protocol;
- stop/go decision.

Verification:

```bash
test -f docs/research/learned-memory-policy-spike.md
```

## 15. Cross-phase documentation deliverables

Each phase closeout should create or update one status artifact:

- Phase A: `2026-05-18-shyftr-may18-frontier-roadmap-handoff-packet.md`
- Phase B: `2026-05-18-shyftr-phase-B-contract-ci-privacy-closeout.md`
- Phase C: `2026-05-18-shyftr-phase-C-materialized-state-indexing-closeout.md`
- Phase D: `2026-05-18-shyftr-phase-D-benchmark-truth-closeout.md`
- Phase E: `2026-05-18-shyftr-phase-E-production-retrieval-closeout.md`
- Phase F: `2026-05-18-shyftr-phase-F-temporal-entity-relation-closeout.md`
- Phase G: `2026-05-18-shyftr-phase-G-consolidation-closeout.md`
- Phase H: `2026-05-18-shyftr-phase-H-belief-state-closeout.md`
- Phase I: `2026-05-18-shyftr-phase-I-privacy-consent-service-closeout.md`
- Phase J: `2026-05-18-shyftr-phase-J-multimodal-policy-closeout.md`

Each closeout must include:

- starting SHA and ending SHA if committed;
- dirty/clean worktree status;
- exact tests run;
- focused test outputs;
- full gate outputs or explicit deferred gate reason;
- public/private artifact classification;
- benchmark/report claim boundary;
- next tranche handoff.

## 16. Human approval gates

Human approval is required for:

- installing new global dependencies or mutating system Python;
- running paid/cloud comparator APIs;
- using real API keys or credentials;
- downloading third-party datasets;
- committing raw or derived standard-dataset artifacts;
- publishing benchmark reports or public superiority claims;
- binding HTTP service to non-localhost or enabling hosted mode;
- implementing field-level encryption beyond a decision spike;
- deleting or overwriting the existing uncommitted Phase-15-like worktree files.

No human approval is required for:

- reading repo files;
- writing docs/plans/status artifacts;
- adding tests;
- running local pytest/compile/readiness gates;
- fixture-safe synthetic benchmark runs already supported by the repo;
- writing ignored/private local reports under existing output guards, as long as no third-party dataset or credential is involved.

## 17. Phase dependency map

```text
A baseline reconciliation
  -> B contract/CI/privacy
    -> C state/indexing
      -> D early benchmark baseline
        -> E retrieval substrate
          -> D retrieval re-run
          -> F temporal/entity/relation
            -> D temporal/entity re-run
            -> G consolidation
              -> D consolidation re-run
              -> H conflict/uncertainty
                -> D conflict re-run
                -> I privacy/consent/service hardening
                  -> D safety/reporting re-run
                  -> J multimodal/policy learning
                    -> D final comparison pass when needed
```

Fast-track exceptions:

- D1 simple baseline can run after B if C is not blocking fixture scale.
- D2 mem0 fixture run can run after B if it is isolated and fixture-only.
- I3 local HTTP auth boundary can be moved earlier if any work requires non-local binding.
- G3 context compaction reconciliation can be moved directly after A if the operator wants to salvage the current dirty worktree first.

## 18. Success criteria for the full program

The program is complete only when all of these are true:

1. manifest/cell-id handling is unified and tested;
2. CI runs the real pytest suite;
3. privacy redaction covers all identified text/list projection leaks;
4. lifecycle state is materialized and verified against ledger replay;
5. sparse/vector indexes can refresh incrementally or cleanly disclose rebuild behavior;
6. deterministic/test embeddings are separated from real retrieval providers;
7. benchmark reports include ShyftR, no-memory, simple baseline, and mem0 OSS where possible;
8. Phase D has produced an early stabilized baseline, recurring post-improvement re-runs, and a final comparison pass unless explicitly unnecessary because the latest recurring run is already equivalent;
9. LongMemEval and LOCOMO have at least dry/scaled local results under reviewed private handling;
10. BEAM handling includes attribution/license metadata before any report publication;
11. temporal valid-time and supersession behavior exists and is evaluated;
12. entity/relation retrieval exists with review-gated ambiguity handling;
13. live→carry→episode→semantic/procedural/rule consolidation is explicit and tested;
14. contradictions produce belief/conflict states rather than silent string overwrites;
15. export receipts and retention/consent policies are implemented or explicitly deferred by decision docs;
16. local API auth/bind posture is enforced and documented;
17. multimodal observation objects exist or are explicitly deferred after a spike;
18. feedback-driven policy uses recorded outcomes to improve or suppress future selection;
19. public README/docs claims match actual evidence.

## 19. Immediate next action

Start with Phase A, not Phase B.

The correct next command sequence is:

```bash
cd /Users/stefan/ShyftR
git status --short --branch
git diff --stat
git status --short -uall
PYTHONPATH=.:src pytest -q \
  tests/test_context_compaction_phase15.py \
  tests/test_phase15_cli_mcp_integration.py \
  tests/test_phase15_feedback_index_recommendations.py
```

If the Phase-15-like tests pass, write the Phase A handoff packet and decide whether to preserve that work as the first consolidation/compaction tranche. If they fail, record the failures and proceed to B0 with the dirty worktree preserved but not merged.

## 20. Final note on positioning

The product story should remain:

ShyftR is not trying to win by being the loudest hosted memory service. It should win by being the most inspectable, review-gated, portable, locally auditable memory substrate for serious agent runtimes.

The technical path to making that story true is this roadmap: stabilize contracts, prove with fair benchmarks, upgrade retrieval, formalize consolidation, manage uncertainty, harden privacy, and only then add multimodal and learned-policy capabilities.
