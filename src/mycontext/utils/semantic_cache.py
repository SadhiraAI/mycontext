"""
Semantic Cache for LLM responses.

Research basis:
  GPT Semantic Cache (arxiv 2411.05276, 2024):
    Embedding-based semantic caching reduces LLM API calls by up to 68.8%
    with cache hit rates of 61.6–68.8% and accuracy > 97%.

  VectorQ (arxiv 2502.03771, 2025):
    Adaptive embedding thresholds achieve 26× cache hit rate increases over
    static similarity thresholds.

  IC-Cache (arxiv 2501.12689, 2025):
    1.4–5.9× throughput improvement by reusing semantically similar cached
    responses as in-context demonstrations.

Design
------
Phase 1 (this implementation): In-process exact-match cache using SHA-256 hash
of (model, assembled_prompt). Zero external dependencies, zero latency on hit.

Phase 2 (future): Replace or supplement the hash lookup with an embedding-based
similarity search (e.g. llmgatekeeper / semcache) to catch near-duplicate and
paraphrased prompts.

The cache is opt-in per call via ``use_cache=True`` (default on non-streaming
calls). It respects TTL so stale responses expire.  It caps size with a simple
LRU-like eviction (evict oldest-by-timestamp when full).

Thread safety: All mutations are protected by a threading.Lock so the cache is
safe to use from the ThreadPoolExecutor-based parallel refinement introduced in
Phase 1.
"""

from __future__ import annotations

import hashlib
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A single cached LLM response."""

    response: Any  # ProviderResponse instance
    created_at: float = field(default_factory=time.monotonic)
    hits: int = 0

    def is_expired(self, ttl_seconds: float) -> bool:
        return (time.monotonic() - self.created_at) > ttl_seconds


@dataclass
class CacheStats:
    """Accumulated statistics for the cache instance."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def total(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        return self.hits / self.total if self.total > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": self.total,
            "hit_rate": round(self.hit_rate, 4),
            "evictions": self.evictions,
            "expirations": self.expirations,
        }


class SemanticCache:
    """
    In-process LRU cache for LLM provider responses.

    Uses a SHA-256 hash of ``(model, prompt_text)`` as the cache key.
    Entries expire after ``ttl_seconds`` and the cache is bounded by
    ``max_size``; when full, the oldest entry is evicted.

    Args:
        ttl_seconds: Time-to-live for cached entries in seconds.
                     Default: 3600 (1 hour).
        max_size:    Maximum number of entries.  Default: 512.
        enabled:     Master on/off switch.  Default: True.

    Example::

        cache = SemanticCache(ttl_seconds=1800, max_size=256)

        # Store
        cache.set(prompt="Explain quantum computing", model="gpt-4o", response=resp)

        # Retrieve
        cached = cache.get(prompt="Explain quantum computing", model="gpt-4o")
        if cached is not None:
            return cached  # cache hit — no API call needed

        # Stats
        print(cache.stats().to_dict())
    """

    def __init__(
        self,
        ttl_seconds: float = 3600.0,
        max_size: int = 512,
        enabled: bool = True,
    ) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.enabled = enabled
        self._store: dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
        self._stats = CacheStats()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, prompt: str, model: str) -> Any | None:
        """Return the cached response for (prompt, model), or None on miss.

        Args:
            prompt: The fully assembled prompt string sent to the LLM.
            model:  The model identifier string.

        Returns:
            A ``ProviderResponse`` instance if cached and not expired,
            otherwise ``None``.
        """
        if not self.enabled:
            return None

        key = self._make_key(prompt, model)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._stats.misses += 1
                return None

            if entry.is_expired(self.ttl_seconds):
                del self._store[key]
                self._stats.expirations += 1
                self._stats.misses += 1
                return None

            entry.hits += 1
            self._stats.hits += 1
            logger.debug(
                "SemanticCache HIT  model=%s  key=%s...  total_hits=%d  hit_rate=%.1f%%",
                model,
                key[:12],
                self._stats.hits,
                self._stats.hit_rate * 100,
            )
            return entry.response

    def set(self, prompt: str, model: str, response: Any) -> None:
        """Store *response* in the cache under (prompt, model).

        Args:
            prompt:   The assembled prompt string.
            model:    The model identifier.
            response: The ``ProviderResponse`` to cache.
        """
        if not self.enabled:
            return

        key = self._make_key(prompt, model)
        with self._lock:
            if len(self._store) >= self.max_size and key not in self._store:
                self._evict_oldest()
            self._store[key] = CacheEntry(response=response)

    def invalidate(self, prompt: str, model: str) -> bool:
        """Remove a specific entry.  Returns True if it existed."""
        key = self._make_key(prompt, model)
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def clear(self) -> None:
        """Remove all entries and reset statistics."""
        with self._lock:
            self._store.clear()
            self._stats = CacheStats()

    def stats(self) -> CacheStats:
        """Return a snapshot of cache statistics."""
        with self._lock:
            return CacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
                expirations=self._stats.expirations,
            )

    def __len__(self) -> int:
        with self._lock:
            return len(self._store)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _make_key(prompt: str, model: str) -> str:
        """SHA-256 hash of model:prompt — compact, collision-resistant key."""
        raw = f"{model}:{prompt}".encode()
        return hashlib.sha256(raw).hexdigest()

    def _evict_oldest(self) -> None:
        """Evict the entry with the earliest created_at timestamp (called under lock)."""
        if not self._store:
            return
        oldest_key = min(self._store, key=lambda k: self._store[k].created_at)
        del self._store[oldest_key]
        self._stats.evictions += 1
        logger.debug("SemanticCache EVICT  key=%s...", oldest_key[:12])


# ---------------------------------------------------------------------------
# Module-level default instance used by LiteLLMProvider
# ---------------------------------------------------------------------------

_default_cache = SemanticCache(ttl_seconds=3600, max_size=512)


def get_default_cache() -> SemanticCache:
    """Return the shared default cache instance."""
    return _default_cache


def reset_default_cache() -> None:
    """Clear the default cache (useful in tests and CLI tools)."""
    _default_cache.clear()
