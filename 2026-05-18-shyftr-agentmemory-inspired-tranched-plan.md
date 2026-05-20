# ShyftR agentmemory-inspired frontier plan

> **For Hermes:** follow ShyftR doctrine and writing-plans tranche discipline. Keep additive, review-gated, and source-grounded.

**Status:** source/addendum only. This is not a standalone execution sequence. Its tranches are absorbed into `2026-05-18-shyftr-may18-frontier-roadmap-tranched-plan.md` at the phase where each dependency is safe.

**Goal:** Add AgentMemory-grade operator ergonomics, surface parity, and retrieval/continuity tooling to ShyftR without weakening ShyftR's review-gated memory doctrine.

**Architecture:** Preserve ShyftR's cell/carry/live-context/evolution substrate. Add thin product surfaces and adapters above existing primitives first; only then add new storage or agent-behavior semantics where the substrate is genuinely missing.

**Integration rule:** Do not execute Tranche 1 -> 7 in this file as written. Use this file as a source map:
- Tranche 1 informs Phase B4/G/I operator-surface parity work.
- Tranche 2 informs Phase D/E/F retrieval-mode reporting and productization.
- Tranche 3 informs Phase G opt-in runtime evidence hooks.
- Tranche 4 informs Phase C3/G branch-aware working context.
- Tranche 5 informs Phase I operations health/recovery surfaces.
- Tranche 6 is deferred to a late Phase J or post-roadmap team/multi-agent overlay spike.
- Tranche 7 informs Phase F/G/J graph-temporal, replay, and multimodal work.

## Tranche 1 — advanced operator surface parity
- Objective: expose existing high-value ShyftR primitives through consistent MCP/CLI/HTTP surfaces.
- Read first: `src/shyftr/mcp_server.py`, `src/shyftr/cli.py`, `src/shyftr/console_api.py`, `src/shyftr/live_context.py`, `src/shyftr/frontier.py`, `src/shyftr/audit.py`, `src/shyftr/pack.py`.
- Add explicit surfaces for: replay/timeline inspection, carry-state checkpoint inspection, proposal inbox/review surfaces, audit summary, frontier review surface, pack assembly inspection.
- Stop boundary: no doctrine changes; no automatic durable-memory writes.

## Tranche 2 — retrieval mode productization
- Objective: make sparse/vector/hybrid/query-expansion/graph/temporal retrieval modes first-class operator choices.
- Read first: `src/shyftr/retrieval/*.py`, `src/shyftr/context_assembly.py`, `src/shyftr/context_expansion.py`, `src/shyftr/graph.py`, `src/shyftr/simulation.py`.
- Add inspectable comparison outputs and per-query routing metadata.
- Stop boundary: no new benchmark claims until evaluated via existing harnesses.

## Tranche 3 — ambient evidence hooks
- Objective: create an opt-in hook/event layer for session start/end, prompt submit, tool use, failures, and compaction signals.
- Map hooks into live-context capture and proposal generation, not direct durable-memory mutation.
- Stop boundary: keep hooks off by default; explicit config gates only.

## Tranche 4 — working-memory and branch-aware context
- Objective: add first-class temporary working memory, sliding windows, and branch/fork semantics for speculative work.
- Reuse carry/live-context/checkpoint machinery where possible.
- Stop boundary: forked/working state must not silently promote into approved memory.

## Tranche 5 — service-grade operations plane
- Objective: add direct diagnostics/privacy/retention/backup/export/import/health surfaces.
- Read first: `src/shyftr/privacy.py`, `src/shyftr/backup.py`, `src/shyftr/ledger_verify.py`, `src/shyftr/observability.py`, `src/shyftr/readiness.py`.
- Stop boundary: keep operator data local-first and public-safe.

## Tranche 6 — team/multi-agent overlays
- Objective: add shared-team memory views and provenance overlays without collapsing the cell model.
- Likely files: new `team`/`mesh` modules plus pack/profile integrations.
- Stop boundary: do not weaken per-cell review authority.

## Tranche 7 — multimodal/frontier extensions
- Objective: add file/image-aware retrieval, replay-rich continuity debugging, and stronger graph-temporal reasoning surfaces.
- Gate all new claims through benchmark/evaluation artifacts.

## Verification posture
- Focused commands per tranche should hit touched modules first, then full ShyftR gates (`compileall`, terminology, public readiness, `PYTHONPATH=.:src pytest -q`, `git diff --check`).
- Every new public surface must have parity checks across CLI/MCP/HTTP where applicable.
- Every new autonomous or hook-driven behavior must prove dry-run / review-gated safety first.

## Non-goals
- Do not replace ShyftR's governed memory lifecycle with unreviewed convenience writes.
- Do not chase raw surface count parity as a vanity metric.
- Do not overclaim benchmark or frontier performance before measurements exist.
