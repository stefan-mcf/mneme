from __future__ import annotations

import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from shyftr.benchmarks.adapters.base import AdapterCostLatencyStats
from shyftr.benchmarks.types import BenchmarkConversation, RetrievalItem, SearchOutput


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def _tokenize(text: str) -> List[str]:
    # Deterministic, dependency-light tokenization.
    return [t.lower() for t in _TOKEN_RE.findall(str(text))]


@dataclass
class _Doc:
    message_id: str
    text: str
    tokens: List[str]
    tf: Counter[str]
    length: int
    metadata: Dict[str, Any]


@dataclass
class SimpleBM25BackendAdapter:
    """Local-only lexical retrieval baseline.

    This adapter is a deterministic, dependency-light BM25-style retriever over
    ingested benchmark messages.

    Scope: retrieval-only baseline for Phase 14 (P14-1). No embeddings, no remote
    calls.
    """

    backend_name: str = "simple-bm25"

    # BM25 constants (stable defaults)
    k1: float = 1.2
    b: float = 0.75

    def __post_init__(self) -> None:
        self._run_id = ""
        self._stats = AdapterCostLatencyStats()
        self._details: Dict[str, Any] = {
            "backend": self.backend_name,
            "mode": "local",
            "scoring": "bm25",
            "tokenization": "regex_alnum_lower",
        }
        self._docs: List[_Doc] = []
        self._df: Dict[str, int] = {}
        self._N = 0
        self._avgdl = 0.0
        self._ingested_message_ids: List[str] = []

    def _record_ingest_ms(self, elapsed_ms: float) -> None:
        self._stats = AdapterCostLatencyStats(
            ingest_ms=(float(self._stats.ingest_ms or 0.0) + float(elapsed_ms)),
            search_ms=list(self._stats.search_ms),
            notes=dict(self._stats.notes),
        )

    def _record_search_ms(self, elapsed_ms: float) -> None:
        self._stats.search_ms.append(float(elapsed_ms))

    def reset_run(self, run_id: str) -> None:
        self._run_id = str(run_id)
        self._stats = AdapterCostLatencyStats()
        self._details = {
            "backend": self.backend_name,
            "mode": "local",
            "scoring": "bm25",
            "tokenization": "regex_alnum_lower",
        }
        self._docs = []
        self._df = {}
        self._N = 0
        self._avgdl = 0.0
        self._ingested_message_ids = []

    def ingest_conversation(self, conversation: BenchmarkConversation) -> None:
        started = time.perf_counter()

        for msg in conversation.messages:
            text = str(msg.content or "")
            tokens = _tokenize(text)
            tf = Counter(tokens)
            doc = _Doc(
                message_id=str(msg.message_id),
                text=text,
                tokens=tokens,
                tf=tf,
                length=len(tokens),
                metadata={
                    "conversation_id": conversation.conversation_id,
                    "session_id": conversation.session_id,
                    "role": msg.role,
                    **dict(msg.metadata),
                },
            )
            self._docs.append(doc)
            self._ingested_message_ids.append(doc.message_id)

        # Recompute DF/avgdl deterministically after each ingest call.
        self._N = len(self._docs)
        df: Dict[str, int] = defaultdict(int)
        total_len = 0
        for d in self._docs:
            total_len += d.length
            for term in set(d.tokens):
                df[term] += 1
        self._df = dict(df)
        self._avgdl = (float(total_len) / float(self._N)) if self._N else 0.0

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        self._stats = AdapterCostLatencyStats(
            ingest_ms=(self._stats.ingest_ms or 0.0) + elapsed_ms,
            search_ms=list(self._stats.search_ms),
            notes=dict(self._stats.notes),
        )

    def _bm25_idf(self, term: str) -> float:
        # Classic BM25 idf with +1 for stability/non-negative.
        n_q = int(self._df.get(term, 0))
        if self._N <= 0:
            return 0.0
        return math.log(1.0 + ((self._N - n_q + 0.5) / (n_q + 0.5)))

    def _score_doc(self, query_terms: List[str], doc: _Doc) -> float:
        if not query_terms or self._N <= 0:
            return 0.0
        score = 0.0
        dl = float(doc.length)
        avgdl = float(self._avgdl or 1.0)

        for term in query_terms:
            f = float(doc.tf.get(term, 0))
            if f <= 0.0:
                continue
            idf = self._bm25_idf(term)
            denom = f + self.k1 * (1.0 - self.b + self.b * (dl / avgdl))
            score += idf * ((f * (self.k1 + 1.0)) / denom)

        return float(score)

    def search(self, *, query_id: str, query: str, top_k: int) -> SearchOutput:
        started = time.perf_counter()

        q_terms = _tokenize(query)

        scored: List[Tuple[float, int, _Doc]] = []
        for idx, doc in enumerate(self._docs):
            s = self._score_doc(q_terms, doc)
            if s > 0.0:
                # idx is a stable tie-breaker preserving ingest order.
                scored.append((s, idx, doc))

        scored.sort(key=lambda t: (-t[0], t[1]))

        items: List[RetrievalItem] = []
        for rank, (_s, _idx, doc) in enumerate(scored[: int(top_k)]):
            items.append(
                RetrievalItem(
                    item_id=str(doc.message_id),
                    text=str(doc.text),
                    score=float(_s),
                    provenance={
                        "backend": self.backend_name,
                        "message_id": doc.message_id,
                        "rank": rank,
                        "conversation_id": doc.metadata.get("conversation_id"),
                        "session_id": doc.metadata.get("session_id"),
                    },
                )
            )

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        self._record_search_ms(elapsed_ms)

        return SearchOutput(
            backend_name=self.backend_name,
            run_id=self._run_id,
            query_id=str(query_id),
            items=items,
            latency_ms=elapsed_ms,
        )

    def export_retrieval_details(self) -> Dict[str, Any]:
        return {
            **dict(self._details),
            "doc_count": int(self._N),
            "avgdl": float(self._avgdl),
            "ingested_message_ids": list(self._ingested_message_ids),
        }

    def export_cost_latency_stats(self) -> Dict[str, Any]:
        return self._stats.to_dict()

    def close(self) -> None:
        # local-only; best-effort cleanup.
        self._docs = []
        self._df = {}
        self._N = 0
        self._avgdl = 0.0


__all__ = ["SimpleBM25BackendAdapter"]
