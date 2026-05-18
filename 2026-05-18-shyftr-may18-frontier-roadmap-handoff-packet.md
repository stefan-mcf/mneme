# ShyftR May 18 frontier roadmap handoff packet

Date: 2026-05-18
Repo: `/Users/stefan/ShyftR`
Plan: `2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md`
Benchmark timing note: Phase D is an early stabilized baseline and recurring measurement loop. It should run after Phase A/B and minimal Phase C, then repeat after major Phases E-J changes. A final comparison pass is required unless the latest recurring run is already equivalent.
Primary report: `May18DeepResearch+Roadmap/may18-deep-research-report.md`
Vault source note: `/Users/stefan/Documents/local wiki/Sources/ShyftR May 18 Deep Research Audit.md`
Phase A closeout: `2026-05-18-shyftr-phase-a-a0-a1-context-compaction-classification-closeout.md`
Status: A0/A1 classified and preserved. Ready to start at Phase B0. No implementation or benchmark completion is claimed here.

## Current truth

The May 18 deep research report has been linked into the Obsidian vault and converted into the comprehensive roadmap plan named above.

The repo is still not clean. Live classified dirty surface:

```text
M .gitignore
M src/shyftr/cli.py
M src/shyftr/layout.py
M src/shyftr/mcp_server.py
M src/shyftr/server.py
M tests/test_mcp_server.py
?? 2026-05-18-shyftr-may18-frontier-roadmap-handoff-packet.md
?? 2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md
?? 2026-05-18-shyftr-phase-a-a0-a1-context-compaction-classification-closeout.md
?? src/shyftr/blob_store.py
?? src/shyftr/bootstrap.py
?? src/shyftr/context_assembly.py
?? src/shyftr/context_compaction.py
?? src/shyftr/context_expansion.py
?? src/shyftr/context_feedback.py
?? src/shyftr/context_index.py
?? src/shyftr/context_recommendations.py
?? tests/test_context_compaction_phase15.py
?? tests/test_phase15_cli_mcp_integration.py
?? tests/test_phase15_feedback_index_recommendations.py
```

Phase-15-style validation status from Phase A:

- `PYTHONPATH=.:src pytest -q tests/test_context_compaction_phase15.py tests/test_phase15_cli_mcp_integration.py tests/test_phase15_feedback_index_recommendations.py`
- result: `14 passed in 0.50s`
- `py_compile` over the inspected Phase-15-style modules passed with exit 0.

Interpretation:

- the dirty source surface is coherent preserved context-compaction / feedback-policy WIP;
- it should be treated as preserved input for later Phase G3 / J2 reconciliation;
- it is not merged roadmap truth, not CI-proven, and not grounds to skip Phase B.

## Canonical next tranche

Phase A is resolved enough to continue with:

1. **B0 — Manifest/path contract unification**.
2. Keep the preserved Phase-15-style dirty surface untouched while B0 work proceeds.
3. Re-read the Phase A closeout if there is any ambiguity about what the uncommitted work proves.

Do not silently absorb the preserved context-compaction files into unrelated Phase B edits.

## First commands

```bash
cd /Users/stefan/ShyftR
git status --short --branch
git diff --stat
git status --short -uall
PYTHONPATH=.:src pytest -q tests/test_context_compaction_phase15.py tests/test_phase15_cli_mcp_integration.py tests/test_phase15_feedback_index_recommendations.py
PYTHONPATH=.:src pytest -q tests/test_memory_provider.py tests/test_mcp_server.py tests/test_server.py
```

When starting B0, first add contract-first RED coverage for canonical manifest resolution, legacy compatibility, conflict policy, and consistent `cell_id` propagation across provider/CLI/MCP/HTTP surfaces.

## Hard boundaries

Do not:

- claim ShyftR beats Mem0 overall;
- run paid/cloud APIs;
- infer API keys from the environment;
- auto-download datasets;
- commit raw or converted third-party datasets;
- publish benchmark reports before review;
- bind the local HTTP service to non-localhost without a dedicated auth tranche;
- overwrite or delete the current uncommitted Phase-15-like files without explicit approval.

## Definition of ready for Phase B

Phase B is ready because:

- the dirty worktree has been classified;
- useful Phase-15-like work has been preserved as explicit WIP input for later reconciliation;
- the plan, handoff, and Phase A closeout exist on disk;
- no implementation worker should now be confused about whether Phase 14 benchmark execution has already happened. It has not.
