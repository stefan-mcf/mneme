from .base import AdapterSkip, BackendAdapter
from .no_memory import NoMemoryBackendAdapter
from .simple_bm25 import SimpleBM25BackendAdapter


def __getattr__(name: str):
    if name == "ShyftRBackendAdapter":
        from .shyftr_backend import ShyftRBackendAdapter

        return ShyftRBackendAdapter
    raise AttributeError(name)


__all__ = [
    "AdapterSkip",
    "BackendAdapter",
    "NoMemoryBackendAdapter",
    "ShyftRBackendAdapter",
    "SimpleBM25BackendAdapter",
]
