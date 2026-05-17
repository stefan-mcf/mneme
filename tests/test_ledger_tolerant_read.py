from __future__ import annotations

import pytest

from shyftr.ledger import read_jsonl, read_jsonl_tolerant


def test_read_jsonl_tolerant_skips_malformed_rows_while_strict_reader_raises(tmp_path):
    ledger = tmp_path / "sample.jsonl"
    ledger.write_text('{"broken": true\n{"ok": true, "row_hash": "ignored", "previous_row_hash": "ignored"}\n', encoding="utf-8")

    with pytest.raises(Exception):
        list(read_jsonl(ledger))

    rows = list(read_jsonl_tolerant(ledger))

    assert rows == [(2, {"ok": True})]
