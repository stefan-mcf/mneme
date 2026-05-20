from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest

import importlib

mem0_backend = importlib.import_module("shyftr.benchmarks.adapters.mem0_backend")
AdapterSkip = importlib.import_module("shyftr.benchmarks.adapters.base").AdapterSkip


def test_mem0_missing_dependency_reports_adapter_skip(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda name: None if name == "mem0" else object())

    with pytest.raises(AdapterSkip) as excinfo:
        mem0_backend._import_mem0()

    assert "mem0 (OSS) Python package not installed" in str(excinfo.value)


def test_mem0_constructor_cloud_key_requirement_is_skip_not_failure() -> None:
    class NeedsCloudKey:
        def __init__(self) -> None:
            raise RuntimeError("The api_key client option must be set either by passing api_key to the client")

    fake_mem0 = types.SimpleNamespace(Memory=NeedsCloudKey, __version__="fixture-version")

    with pytest.raises(AdapterSkip) as excinfo:
        mem0_backend._construct_mem0_memory(fake_mem0)

    message = str(excinfo.value)
    assert "mem0 OSS package imported" in message
    assert "fixture-version" in message
    assert "requires API key" in message or "external provider" in message


def test_mem0_constructs_from_explicit_local_config_path_and_discloses_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path = tmp_path / "mem0-local.json"
    config_payload = {
        "vector_store": {"provider": "qdrant", "config": {"path": str(tmp_path / "qdrant")}},
        "embedder": {"provider": "fastembed", "config": {"model": "BAAI/bge-small-en-v1.5"}},
        "llm": {"provider": "ollama", "config": {"model": "llama3.2:1b", "ollama_base_url": "http://localhost:11434"}},
    }
    config_path.write_text(json.dumps(config_payload), encoding="utf-8")

    constructed = {}

    class FakeMemory:
        @classmethod
        def from_config(cls, config):
            constructed["config"] = config
            return types.SimpleNamespace(add=lambda *args, **kwargs: None, search=lambda *args, **kwargs: [])

    fake_mem0 = types.SimpleNamespace(Memory=FakeMemory, __version__="fixture-version")
    monkeypatch.setenv("SHYFTR_MEM0_LOCAL_CONFIG", str(config_path))

    memory, details = mem0_backend._construct_mem0_memory(fake_mem0, run_id="unit-run")

    assert memory is not None
    assert constructed["config"] == config_payload
    assert details["mode"] == "explicit-local-config"
    assert details["config_source"] == "SHYFTR_MEM0_LOCAL_CONFIG"
    assert details["vector_store_provider"] == "qdrant"
    assert details["embedder_provider"] == "fastembed"
    assert details["embedder_model"] == "BAAI/bge-small-en-v1.5"
    assert details["llm_provider"] == "ollama"
    assert details["llm_model"] == "llama3.2:1b"
    assert details["llm_base_url"] == "http://localhost:11434"
    assert details["api_key_configured"] is False


def test_mem0_explicit_local_config_rejects_api_key_material(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_path = tmp_path / "mem0-local.json"
    config_path.write_text(
        json.dumps({"llm": {"provider": "openai", "config": {"api_key": "sk-test"}}}),
        encoding="utf-8",
    )
    fake_mem0 = types.SimpleNamespace(Memory=object, __version__="fixture-version")
    monkeypatch.setenv("SHYFTR_MEM0_LOCAL_CONFIG", str(config_path))

    with pytest.raises(AdapterSkip) as excinfo:
        mem0_backend._construct_mem0_memory(fake_mem0, run_id="unit-run")

    assert "credential-bearing" in str(excinfo.value)


def test_cli_include_mem0_oss_reports_skip_or_ok_with_runner_owned_answer_eval(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output = Path("tmp/benchmarks/test_mem0_oss_cli_report.json")
    output_abs = repo_root / output
    if output_abs.exists():
        output_abs.unlink()

    run_id = f"mem0-oss-cli-test-{tmp_path.name}"
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
            "--include-mem0-oss",
            "--include-simple-bm25",
            "--enable-answer-eval",
        ],
        cwd=repo_root,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr

    payload = json.loads(output_abs.read_text(encoding="utf-8"))
    by_name = {r["backend_name"]: r for r in payload["backend_results"]}

    # Control: core backends always run.
    assert by_name["shyftr"]["status"] == "ok"
    assert by_name["no-memory"]["status"] == "ok"
    assert by_name["simple-bm25"]["status"] == "ok"

    # mem0-oss may be ok (if installed) or skipped (if not installed / unusable).
    assert by_name["mem0-oss"]["status"] in {"ok", "skipped"}

    # Runner-owned answerer/judge are used.
    assert payload["models"]["answerer"]["name"].startswith("deterministic")
    assert payload["models"]["judge"]["name"].startswith("deterministic")

    # Optional LLM judge must remain disabled unless explicitly enabled.
    assert payload["models"]["llm_judge"]["provider"] == "none"

    if by_name["mem0-oss"]["status"] == "skipped":
        reason = (by_name["mem0-oss"].get("status_reason") or "").lower()
        assert "mem0" in reason

    # Cleanup
    if output_abs.exists():
        output_abs.unlink()
    shutil.rmtree(repo_root / "tmp" / "bench_cells" / run_id, ignore_errors=True)
