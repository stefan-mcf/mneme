from __future__ import annotations

import json
from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from shyftr.layout import init_cell
from shyftr.ledger import read_jsonl
from shyftr.mcp_server import _handle_json_rpc_message
from shyftr.provider.memory import remember
from shyftr.server import _get_app


def _records(path: Path) -> list[dict]:
    return [record for _, record in read_jsonl(path)]


def _write_manifest(path: Path, *, cell_id: str, cell_type: str = "user") -> None:
    path.write_text(
        json.dumps({"cell_id": cell_id, "cell_type": cell_type}, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def test_provider_memory_uses_config_cell_manifest_cell_id(tmp_path: Path) -> None:
    cell = init_cell(tmp_path, "core", cell_type="user")
    _write_manifest(cell / "config" / "cell_manifest.json", cell_id="canonical-core")

    remember(cell, "User prefers concise terminal updates.", "preference")

    sources = _records(cell / "ledger" / "sources.jsonl")
    assert sources[0]["cell_id"] == "canonical-core"


def test_provider_memory_prefers_config_manifest_when_both_manifests_exist(tmp_path: Path) -> None:
    cell = init_cell(tmp_path, "core", cell_type="user")
    _write_manifest(cell / "config" / "cell_manifest.json", cell_id="canonical-core")
    _write_manifest(cell / "manifest.json", cell_id="legacy-core")

    remember(cell, "Use pytest before pushing Python changes.", "workflow")

    sources = _records(cell / "ledger" / "sources.jsonl")
    assert sources[0]["cell_id"] == "canonical-core"


def test_mcp_json_rpc_accepts_legacy_manifest_only_cell_path(tmp_path: Path) -> None:
    cell = init_cell(tmp_path, "core", cell_type="user")
    (cell / "config" / "cell_manifest.json").unlink()
    _write_manifest(cell / "manifest.json", cell_id="legacy-core")

    called = _handle_json_rpc_message(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "shyftr_search",
                "arguments": {"cell_path": str(cell), "query": "concise"},
            },
        }
    )

    assert called is not None
    assert "error" not in called
    payload = json.loads(called["result"]["content"][0]["text"])
    assert payload["status"] == "ok"
    assert payload["cell_path"] == str(cell)


def test_http_episode_search_accepts_legacy_manifest_only_cell_path(tmp_path: Path) -> None:
    cell = init_cell(tmp_path, "core", cell_type="user")
    (cell / "config" / "cell_manifest.json").unlink()
    _write_manifest(cell / "manifest.json", cell_id="legacy-core")
    client = TestClient(_get_app())

    response = client.get("/episode/search", params={"cell_path": str(cell), "query": "concise"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["cell_path"] == str(cell)
