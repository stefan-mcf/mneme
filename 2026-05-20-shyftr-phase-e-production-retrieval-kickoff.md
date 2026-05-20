# ShyftR Phase E production retrieval kickoff

Date: 2026-05-20 AEST
Repo: `/Users/stefan/ShyftR`
Branch: `main`
Starting HEAD: `6e15eef82922a86216439b1dfb1fdd4b69df4a1e`
Remote status: `origin/main` matches starting HEAD.
Status: Phase E is ready to start from a clean pushed repository.

## Starting truth

Phase D is closed and pushed in commit `6e15eef`.

Verified before commit/push:

```bash
PYTHONPATH=.:src python -m compileall -q src scripts examples
python scripts/terminology_inventory.py --fail-on-public-stale
python scripts/terminology_inventory.py --fail-on-capitalized-prose
python scripts/public_readiness_check.py
git diff --check
git diff --cached --check
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

Observed result:

- public readiness: PASS
- focused benchmark regression: `47 passed in 3.12s`
- `git diff --check`: clean
- pushed: `main -> origin/main` at `6e15eef`

A supplemental swarm review lane (`swarm2`) reviewed public-safety risk before commit. It blocked committing generated benchmark JSON/HTML reports because those reports contained local paths and dataset/model-output text. The final commit therefore excluded `reports/benchmarks/phaseD-*.json`, `reports/benchmarks/phaseD-benchmark-report.html`, and `docs/benchmarks/phaseD-benchmark-report.html`.

## Preserved but not committed

Phase C / native context-compaction and related future-phase WIP was not committed as part of Phase D cleanup because it did not pass the current staged gate and belongs to a different tranche boundary.

Preserved local copy:

```text
/Users/stefan/shyftr-preserved-phase-c-g-wip-20260520
```

There is also a stash created during cleanup:

```text
stash@{0}: WIP on main: e5a8a68 feat: complete phase b contract and readiness tranche
```

Do not apply the stash blindly before Phase E. Inspect it first if needed.

## Phase E objective

Phase E: production retrieval substrate.

Goal: close the measured retrieval-quality gap with modern memory systems without sacrificing local-first auditability, review-gated doctrine, or privacy boundaries.

Phase E must be measured against Phase D baselines after material retrieval changes land. No public superiority claim is allowed from Phase E implementation alone.

## Exact first tranche: E0 embedding provider contract

Start with E0, not E1/E2/E4.

Objective: separate test embeddings from real embeddings and make report metadata honest.

Likely files:

- `src/shyftr/retrieval/embeddings.py`
- `src/shyftr/retrieval/vector.py`
- `src/shyftr/benchmarks/runner.py`
- `tests/test_embedding_provider_contract.py`

Minimum RED tests:

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

Focused verification for E0:

```bash
PYTHONPATH=.:src pytest -q tests/test_embedding_provider_contract.py tests/test_retrieval_vector.py
```

Broader Phase E guard after E0 is green:

```bash
PYTHONPATH=.:src python -m compileall -q src scripts examples
python scripts/terminology_inventory.py --fail-on-public-stale
python scripts/terminology_inventory.py --fail-on-capitalized-prose
python scripts/public_readiness_check.py
git diff --check
```

## Non-goals for E0

- Do not add hosted/cloud embedding defaults.
- Do not infer real provider use from ambient credentials.
- Do not send private/redacted text to a remote provider without explicit policy.
- Do not add sqlite-vec/LanceDB/Qdrant behavior before the provider contract is pinned.
- Do not claim benchmark improvement until a post-E Phase D rerun is performed.

## Clean-start check before implementation

Before touching E0 code, run:

```bash
cd /Users/stefan/ShyftR
git status --short --branch
git rev-parse HEAD origin/main
```

Expected:

```text
## main...origin/main
6e15eef82922a86216439b1dfb1fdd4b69df4a1e
6e15eef82922a86216439b1dfb1fdd4b69df4a1e
```
