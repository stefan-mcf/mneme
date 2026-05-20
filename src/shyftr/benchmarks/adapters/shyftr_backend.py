from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from shyftr.benchmarks.adapters.base import AdapterCostLatencyStats
from shyftr.benchmarks.types import BenchmarkConversation, RetrievalItem, SearchOutput
from shyftr.layout import init_cell
from shyftr.policy import BoundaryPolicyError, check_provider_memory_policy
from shyftr.provider import MemoryProvider


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_RE.findall(str(text))]


@dataclass
class ShyftRBackendAdapter:
    """ShyftR local-cell backend adapter for fixture-safe benchmark runs.

    The benchmark adapter exercises ShyftR cell initialization and boundary
    policy, then uses a harness-scoped in-memory BM25 index for retrieval. That
    keeps scaled benchmark runs bounded without turning fixture runs into
    product claims about the durable append-only memory path.
    """

    cell_root: Path
    cell_id: str = "bench-cell"
    backend_name: str = "shyftr"
    isolate_cell_per_run: bool = True
    trust_actor: str = "benchmark-runner"
    trust_reason: str = "synthetic-fixture"
    pulse_channel: str = "benchmark"

    def __post_init__(self) -> None:
        self.cell_root = Path(self.cell_root)
        self._run_id = ""
        self._active_cell_id: Optional[str] = None
        self._cell_path: Optional[Path] = None
        self._provider: Optional[MemoryProvider] = None
        self._stats = AdapterCostLatencyStats()
        self._details: Dict[str, Any] = {"searches": []}
        self._benchmark_docs: List[Tuple[str, str, List[str], Counter[str], Dict[str, Any]]] = []
        self._benchmark_df: Dict[str, int] = {}
        self._benchmark_avgdl = 0.0
        self._benchmark_total_len = 0

    def _derived_cell_id(self) -> str:
        base = str(self.cell_id)
        if not self.isolate_cell_per_run or not self._run_id:
            return base
        suffix = hashlib.sha256(self._run_id.encode("utf-8")).hexdigest()[:10]
        return f"{base}-{suffix}"

    def reset_run(self, run_id: str) -> None:
        self._run_id = str(run_id)
        self._active_cell_id = self._derived_cell_id()
        self._cell_path = init_cell(self.cell_root, self._active_cell_id, cell_type="benchmark")
        self._provider = MemoryProvider(self._cell_path)
        self._stats = AdapterCostLatencyStats()
        self._details = {
            "searches": [],
            "cell_id": self._active_cell_id,
            "benchmark_search_mode": "in_memory_bm25_policy_checked",
            "durable_write_mode": "disabled_for_scaled_benchmark_harness",
        }
        self._benchmark_docs = []
        self._benchmark_df = {}
        self._benchmark_avgdl = 0.0
        self._benchmark_total_len = 0

    def ingest_conversation(self, conversation: BenchmarkConversation) -> None:
        if self._provider is None:
            raise RuntimeError("adapter not initialized; call reset_run first")

        started = time.perf_counter()
        for msg in conversation.messages:
            statement = f"[{conversation.conversation_id}/{conversation.session_id or 'na'}/{msg.role}/{msg.message_id}] {msg.content}"
            metadata = {
                "conversation_id": conversation.conversation_id,
                "session_id": conversation.session_id,
                "message_id": msg.message_id,
                "role": msg.role,
                "benchmark": True,
                "actor": self.trust_actor,
                "trust_reason": self.trust_reason,
                "pulse_channel": self.pulse_channel,
                "created_at": msg.created_at or conversation.started_at or "2026-01-01T00:00:00Z",
            }
            effective_statement = statement
            try:
                check_provider_memory_policy(statement, "preference", metadata=metadata, raise_on_reject=True)
            except BoundaryPolicyError as exc:
                self._details.setdefault("boundary_policy_fallbacks", []).append(
                    {"message_id": msg.message_id, "reasons": list(exc.reasons)}
                )
                effective_statement = f"[{conversation.conversation_id}/{conversation.session_id or 'na'}/{msg.role}/{msg.message_id}] [boundary-policy-filtered benchmark message]"

            tokens = _tokenize(effective_statement)
            tf = Counter(tokens)
            self._benchmark_docs.append((str(msg.message_id), effective_statement, tokens, tf, metadata))
            self._benchmark_total_len += len(tokens)
            for term in set(tokens):
                self._benchmark_df[term] = int(self._benchmark_df.get(term, 0)) + 1

        doc_count = len(self._benchmark_docs)
        self._benchmark_avgdl = (float(self._benchmark_total_len) / float(doc_count)) if doc_count else 0.0
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        self._stats = AdapterCostLatencyStats(
            ingest_ms=(float(self._stats.ingest_ms or 0.0) + elapsed_ms),
            search_ms=list(self._stats.search_ms),
            notes={
                **dict(self._stats.notes),
                "benchmark_search_mode": "in_memory_bm25_policy_checked",
                "durable_write_mode": "disabled_for_scaled_benchmark_harness",
            },
        )

    def _score_doc(self, query_terms: List[str], doc: Tuple[str, str, List[str], Counter[str], Dict[str, Any]]) -> float:
        _message_id, _statement, doc_tokens, tf, _metadata = doc
        doc_count = len(self._benchmark_docs)
        if not query_terms or doc_count <= 0:
            return 0.0
        avgdl = float(self._benchmark_avgdl or 1.0)
        doc_len = float(len(doc_tokens))
        score = 0.0
        for term in query_terms:
            freq = float(tf.get(term, 0))
            if freq <= 0.0:
                continue
            n_q = int(self._benchmark_df.get(term, 0))
            idf = math.log(1.0 + ((doc_count - n_q + 0.5) / (n_q + 0.5)))
            denom = freq + 1.2 * (1.0 - 0.75 + 0.75 * (doc_len / avgdl))
            score += idf * ((freq * (1.2 + 1.0)) / denom)
        return float(score)

    def search(self, *, query_id: str, query: str, top_k: int) -> SearchOutput:
        if self._provider is None:
            raise RuntimeError("adapter not initialized; call reset_run first")

        started = time.perf_counter()
        query_terms = _tokenize(query)
        scored: List[Tuple[float, int, Tuple[str, str, List[str], Counter[str], Dict[str, Any]]]] = []
        for idx, doc in enumerate(self._benchmark_docs):
            score = self._score_doc(query_terms, doc)
            if score > 0.0:
                scored.append((score, idx, doc))
        scored.sort(key=lambda row: (-row[0], row[1]))

        items: List[RetrievalItem] = []
        detail_items: List[Dict[str, Any]] = []
        for rank, (score, _idx, doc) in enumerate(scored[: int(top_k)]):
            message_id, statement, _tokens, _tf, metadata = doc
            item = RetrievalItem(
                item_id=str(message_id),
                text=statement,
                score=float(score),
                provenance={
                    "backend": self.backend_name,
                    "message_id": str(message_id),
                    "rank": rank,
                    "conversation_id": metadata.get("conversation_id"),
                    "session_id": metadata.get("session_id"),
                },
                sensitivity=None,
                review_status="benchmark_index",
            )
            items.append(item)
            detail_items.append(
                {
                    "item_id": item.item_id,
                    "score": item.score,
                    "review_status": item.review_status,
                    "has_provenance": bool(item.provenance),
                }
            )

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        self._stats.search_ms.append(elapsed_ms)
        self._details["searches"].append(
            {
                "query_id": query_id,
                "query": query,
                "top_k": int(top_k),
                "returned": len(items),
                "latency_ms": elapsed_ms,
                "items": detail_items,
            }
        )

        return SearchOutput(
            backend_name=self.backend_name,
            run_id=self._run_id,
            query_id=query_id,
            items=items,
            latency_ms=elapsed_ms,
        )

    def export_retrieval_details(self) -> Dict[str, Any]:
        return {
            **dict(self._details),
            "doc_count": len(self._benchmark_docs),
            "avgdl": float(self._benchmark_avgdl),
        }

    def export_cost_latency_stats(self) -> Dict[str, Any]:
        return self._stats.to_dict()

    def close(self) -> None:
        self._provider = None
        self._benchmark_docs = []
        self._benchmark_df = {}
        self._benchmark_avgdl = 0.0
        self._benchmark_total_len = 0


__all__ = ["ShyftRBackendAdapter"]
