from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from shyftr.benchmarks.fixture import synthetic_mini_fixture


def test_simple_bm25_import_and_backend_name_constant() -> None:
    # P14-1: adapter should exist and expose backend_name exactly 'simple-bm25'.
    from shyftr.benchmarks.adapters.simple_bm25 import SimpleBM25BackendAdapter

    adapter = SimpleBM25BackendAdapter()
    assert adapter.backend_name == "simple-bm25"


def test_simple_bm25_retrieves_expected_message_ids_on_synthetic_mini() -> None:
    from shyftr.benchmarks.adapters.simple_bm25 import SimpleBM25BackendAdapter

    fixture = synthetic_mini_fixture()
    adapter = SimpleBM25BackendAdapter()

    adapter.reset_run("run-001")
    for conv in fixture.conversations:
        adapter.ingest_conversation(conv)

    by_id = {q.question_id: q for q in fixture.questions}

    out1 = adapter.search(query_id="q-001", query=by_id["q-001"].query, top_k=3)
    assert [i.item_id for i in out1.items][:1] == ["m-001"]

    out2 = adapter.search(query_id="q-002", query=by_id["q-002"].query, top_k=3)
    assert [i.item_id for i in out2.items][:1] == ["m-003"]

    # Adapter must export retrieval details and cost/latency stats.
    details = adapter.export_retrieval_details()
    stats = adapter.export_cost_latency_stats()
    assert isinstance(details, dict)
    assert isinstance(stats, dict)

    adapter.close()


def test_cli_include_simple_bm25_writes_backend_result(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output = Path("tmp/benchmarks/test_simple_bm25_cli_report.json")
    output_abs = repo_root / output
    if output_abs.exists():
        output_abs.unlink()

    run_id = f"simple-bm25-cli-test-{tmp_path.name}"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_memory_benchmark.py",
            "--fixture",
            "synthetic-mini",
            "--run-id",
            run_id,
            "--output",
            str(output),
            "--top-k",
            "1,3",
            "--include-simple-bm25",
            "--enable-answer-eval",
        ],
        cwd=repo_root,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    try:
        payload = json.loads(output_abs.read_text(encoding="utf-8"))
        by_name = {r["backend_name"]: r for r in payload["backend_results"]}
        assert by_name["simple-bm25"]["status"] == "ok"
        assert by_name["simple-bm25"]["metrics"]["retrieval_by_k"]["1"]["recall_at_k"] > 0
    finally:
        if output_abs.exists():
            output_abs.unlink()
        shutil.rmtree(repo_root / "tmp" / "bench_cells" / run_id, ignore_errors=True)
