from __future__ import annotations

import importlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from shyftr.benchmarks.adapters.base import AdapterCostLatencyStats, AdapterSkip
from shyftr.benchmarks.types import BenchmarkConversation, RetrievalItem, SearchOutput


def _import_mem0() -> Any:
    """Import mem0 OSS Python package if installed.

    This intentionally does not support mem0 Cloud / API-key flows.
    """

    spec = importlib.util.find_spec("mem0")
    if spec is None:
        raise AdapterSkip(
            "mem0 (OSS) Python package not installed. Install an OSS/local mem0 package to enable this backend. "
            "This harness does not auto-install optional deps."
        )

    mod = importlib.import_module("mem0")
    return mod


def _contains_credential_material(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).lower()
            if any(marker in normalized_key for marker in ("api_key", "apikey", "token", "secret", "password")):
                if nested not in (None, ""):
                    return True
            if _contains_credential_material(nested):
                return True
    elif isinstance(value, list):
        return any(_contains_credential_material(item) for item in value)
    return False


def _env_flag(name: str) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _load_explicit_local_config(run_id: str) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    raw_path = os.environ.get("SHYFTR_MEM0_LOCAL_CONFIG")
    if not raw_path:
        return None, {}

    path = Path(raw_path).expanduser().resolve()
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AdapterSkip(f"mem0 explicit local config could not be read from SHYFTR_MEM0_LOCAL_CONFIG={path}: {exc}") from exc

    if not isinstance(config, dict):
        raise AdapterSkip("mem0 explicit local config must be a JSON object")
    if _contains_credential_material(config):
        raise AdapterSkip("mem0 explicit local config contains credential-bearing fields; refusing fixture-safe D2 run")

    vector_store = config.get("vector_store") or {}
    embedder = config.get("embedder") or {}
    llm = config.get("llm") or {}
    vector_config = vector_store.get("config") or {} if isinstance(vector_store, dict) else {}
    embedder_config = embedder.get("config") or {} if isinstance(embedder, dict) else {}
    llm_config = llm.get("config") or {} if isinstance(llm, dict) else {}

    # If the caller uses a relative qdrant path in the explicit local config,
    # make it stable per run while preserving the config file as the source of truth.
    if isinstance(vector_config, dict) and vector_config.get("path") == "{run_id}":
        vector_config["path"] = str(Path("tmp") / "mem0_qdrant" / run_id)

    details = {
        "mode": "explicit-local-config",
        "config_source": "SHYFTR_MEM0_LOCAL_CONFIG",
        "config_path": str(path),
        "vector_store_provider": vector_store.get("provider") if isinstance(vector_store, dict) else None,
        "embedder_provider": embedder.get("provider") if isinstance(embedder, dict) else None,
        "embedder_model": embedder_config.get("model") if isinstance(embedder_config, dict) else None,
        "llm_provider": llm.get("provider") if isinstance(llm, dict) else None,
        "llm_model": llm_config.get("model") if isinstance(llm_config, dict) else None,
        "llm_base_url": llm_config.get("ollama_base_url") or llm_config.get("base_url") if isinstance(llm_config, dict) else None,
        "api_key_configured": False,
    }
    return config, details


def _construct_mem0_memory(mem0_mod: Any, run_id: str = "") -> Tuple[Any, Dict[str, Any]]:
    """Best-effort construction for mem0 OSS memory object.

    mem0 OSS APIs may differ by version; we keep this adapter defensive and avoid
    cloud configuration. A real local provider stack is enabled only when the
    operator sets SHYFTR_MEM0_LOCAL_CONFIG to a credential-free JSON config.
    """

    version = str(getattr(mem0_mod, "__version__", "unknown"))

    # Common pattern in mem0 docs: from mem0 import Memory
    Memory = getattr(mem0_mod, "Memory", None)
    config, details = _load_explicit_local_config(run_id=run_id)
    if config is not None:
        if Memory is None or not callable(getattr(Memory, "from_config", None)):
            raise AdapterSkip("mem0 explicit local config was provided, but mem0.Memory.from_config is unavailable")
        try:
            memory = Memory.from_config(config)
        except Exception as exc:
            raise AdapterSkip(
                "mem0 OSS package imported "
                f"(version={version}) and explicit local config was provided, but construction failed. "
                f"Original error: {type(exc).__name__}: {exc}"
            ) from exc
        return memory, details

    if Memory is not None:
        try:
            return Memory(), {"mode": "default-constructor"}
        except TypeError:
            try:
                # Some versions expect config dict.
                return Memory(config={}), {"mode": "empty-config-constructor"}
            except Exception as exc:
                raise AdapterSkip(
                    "mem0 OSS package imported "
                    f"(version={version}) but its local Memory constructor requires API key or external provider configuration; "
                    "skipping fixture-safe D2 run rather than inferring credentials. "
                    f"Original error: {type(exc).__name__}: {exc}"
                ) from exc
        except Exception as exc:
            raise AdapterSkip(
                "mem0 OSS package imported "
                f"(version={version}) but its local Memory constructor requires API key or external provider configuration; "
                "skipping fixture-safe D2 run rather than inferring credentials. "
                f"Original error: {type(exc).__name__}: {exc}"
            ) from exc

    # Some versions may expose a factory.
    factory = getattr(mem0_mod, "create_memory", None)
    if callable(factory):
        return factory({}), {"mode": "create_memory-empty-config"}

    raise AdapterSkip("mem0 import succeeded but no supported OSS Memory API was found (expected mem0.Memory or mem0.create_memory).")


@dataclass
class Mem0OSSBackendAdapter:
    """mem0 OSS/local backend adapter.

    Optional dependency: mem0 Python package. If missing, the adapter raises
    AdapterSkip so the runner can report status=skipped.

    Notes:
    - This adapter is intentionally fixture-safe: it only ingests the synthetic
      fixture payload passed by the harness, and returns RetrievalItem.item_id
      using the fixture message_id values when possible.
    - Cloud / API-key paths are out-of-scope for P11-2.
    """

    backend_name: str = "mem0-oss"

    def __post_init__(self) -> None:
        self._run_id = ""
        self._stats = AdapterCostLatencyStats()
        self._details: Dict[str, Any] = {"backend": "mem0-oss", "mode": "local"}
        self._mem0 = None
        self._memory = None
        self._ingested: List[Dict[str, Any]] = []

    def reset_run(self, run_id: str) -> None:
        self._run_id = str(run_id)
        self._stats = AdapterCostLatencyStats()
        self._details = {"backend": "mem0-oss", "mode": "local"}
        self._ingested = []

        self._mem0 = _import_mem0()
        # Record optional dependency version where possible.
        try:
            import importlib.metadata as _ilm

            try:
                self._details["mem0_version"] = _ilm.version("mem0ai")
            except Exception:
                self._details["mem0_version"] = _ilm.version("mem0")
        except Exception:
            self._details["mem0_version"] = None

        self._memory, construct_details = _construct_mem0_memory(self._mem0, run_id=self._run_id)
        self._details.update(construct_details)
        # Disclose which constructor path we used.
        if getattr(self._mem0, "Memory", None) is not None:
            self._details["memory_api"] = "mem0.Memory"
        elif callable(getattr(self._mem0, "create_memory", None)):
            self._details["memory_api"] = "mem0.create_memory"
        else:
            self._details["memory_api"] = "unknown"

    def ingest_conversation(self, conversation: BenchmarkConversation) -> None:
        if self._memory is None:
            raise RuntimeError("mem0 memory not initialized; did you call reset_run()?")

        started = time.perf_counter()
        # Keep a fixture-safe, stable representation.
        for msg in conversation.messages:
            payload = {
                "id": msg.message_id,
                "conversation_id": conversation.conversation_id,
                "session_id": conversation.session_id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at,
                "metadata": dict(msg.metadata),
            }
            self._ingested.append(payload)

            # Best-effort ingestion into mem0 OSS.
            # We avoid passing any cloud keys/config.
            add_fn = getattr(self._memory, "add", None)
            if callable(add_fn):
                # mem0 OSS v2.x expects a chat-style "messages" payload. We also
                # explicitly disable LLM inference for fixture-safe, bounded local
                # runs (infer=False) so ingestion does not trigger slow model calls.
                messages = [{"role": msg.role, "content": msg.content}]
                metadata = {"message_id": msg.message_id, "conversation_id": conversation.conversation_id}
                try:
                    add_fn(
                        messages,
                        user_id=self._run_id or "shyftr-benchmark",
                        run_id=self._run_id or None,
                        metadata=metadata,
                        infer=False,
                    )
                except TypeError:
                    # Older mem0 variants may accept a dict payload instead.
                    add_fn(
                        {"messages": messages, "metadata": metadata},
                        user_id=self._run_id or "shyftr-benchmark",
                    )
            else:
                # If mem0 doesn't have an add API, we can still run in a degraded
                # local mode by relying on adapter-side retrieval details.
                self._details["ingest_warning"] = "mem0 memory object has no .add(); adapter ran in degraded mode."

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        # AdapterCostLatencyStats is frozen; update via replacement.
        self._stats = AdapterCostLatencyStats(
            ingest_ms=(float(self._stats.ingest_ms or 0.0) + float(elapsed_ms)),
            search_ms=list(self._stats.search_ms),
            notes=dict(self._stats.notes),
        )
        # Duplicate disclosure into cost/latency notes so it appears even when
        # include_retrieval_details is disabled.
        self._stats.notes.setdefault("backend", self.backend_name)
        if "mem0_version" in self._details:
            self._stats.notes.setdefault("mem0_version", self._details.get("mem0_version"))
        if "memory_api" in self._details:
            self._stats.notes.setdefault("memory_api", self._details.get("memory_api"))
        if "ingest_warning" in self._details:
            self._stats.notes.setdefault("ingest_warning", self._details.get("ingest_warning"))

    def search(self, *, query_id: str, query: str, top_k: int) -> SearchOutput:
        if self._memory is None:
            raise RuntimeError("mem0 memory not initialized; did you call reset_run()?")

        started = time.perf_counter()
        items: List[RetrievalItem] = []

        search_fn = getattr(self._memory, "search", None)
        if callable(search_fn):
            raw = None
            try:
                # mem0 OSS v2.x signature: search(query, top_k=..., filters=...)
                raw = search_fn(query, filters={"user_id": self._run_id or "shyftr-benchmark"}, top_k=top_k)
            except (TypeError, ValueError):
                try:
                    raw = search_fn(query, filters={"user_id": self._run_id or "shyftr-benchmark"}, limit=top_k)
                except TypeError:
                    # Some versions may accept 'k' instead of top_k/limit.
                    raw = search_fn(query, filters={"user_id": self._run_id or "shyftr-benchmark"}, k=top_k)

            # Normalize raw results to RetrievalItems.
            # Expected shapes vary, so we accept dicts or objects.
            results = raw or []
            if isinstance(results, dict) and "results" in results:
                results = results.get("results") or []

            for idx, r in enumerate(list(results)[:top_k]):
                if isinstance(r, dict):
                    text = str(r.get("content") or r.get("text") or "")
                    meta = r.get("metadata") or {}
                    item_id = str(meta.get("message_id") or r.get("id") or f"mem0-{query_id}-{idx}")
                    score = r.get("score")
                else:
                    text = str(getattr(r, "content", None) or getattr(r, "text", None) or "")
                    meta = getattr(r, "metadata", None) or {}
                    item_id = str(getattr(r, "id", None) or meta.get("message_id") or f"mem0-{query_id}-{idx}")
                    score = getattr(r, "score", None)

                items.append(
                    RetrievalItem(
                        item_id=item_id,
                        text=text,
                        score=float(score) if score is not None else None,
                        provenance={"backend": self.backend_name, "message_id": meta.get("message_id") or item_id},
                    )
                )
        else:
            # Degraded mode: simple keyword match over ingested fixture for deterministic behavior.
            q = query.lower()
            candidates = []
            for m in self._ingested:
                content = str(m.get("content") or "")
                if any(tok in content.lower() for tok in q.split() if tok):
                    candidates.append(m)
            for idx, m in enumerate(candidates[:top_k]):
                items.append(
                    RetrievalItem(
                        item_id=str(m.get("id") or f"mem0-{query_id}-{idx}"),
                        text=str(m.get("content") or ""),
                        score=None,
                        provenance={"backend": self.backend_name, "message_id": m.get("id")},
                    )
                )
            self._details["search_warning"] = "mem0 memory object has no .search(); adapter ran in degraded keyword mode."

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        # AdapterCostLatencyStats is frozen; update via replacement.
        self._stats = AdapterCostLatencyStats(
            ingest_ms=self._stats.ingest_ms,
            search_ms=list(self._stats.search_ms) + [float(elapsed_ms)],
            notes=dict(self._stats.notes),
        )
        if "search_warning" in self._details:
            self._stats.notes.setdefault("search_warning", self._details.get("search_warning"))
        return SearchOutput(backend_name=self.backend_name, run_id=self._run_id, query_id=query_id, items=items, latency_ms=elapsed_ms)

    def export_retrieval_details(self) -> Dict[str, Any]:
        return {
            **dict(self._details),
            "ingested_message_ids": [m.get("id") for m in self._ingested],
        }

    def export_cost_latency_stats(self) -> Dict[str, Any]:
        return self._stats.to_dict()

    def close(self) -> None:
        # Best-effort resource cleanup.
        self._memory = None
        self._mem0 = None


__all__ = ["Mem0OSSBackendAdapter"]
