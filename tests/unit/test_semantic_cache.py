"""
Tests for SemanticCache and its integration with LiteLLMProvider.

Covers:
  - Basic get/set/miss semantics
  - TTL expiration
  - Max-size eviction (LRU-oldest)
  - Thread safety (concurrent reads/writes)
  - Hit-rate statistics
  - Cache disabled (enabled=False / use_cache=False)
  - LiteLLMProvider.generate cache hit avoids LLM call
  - LiteLLMProvider.generate cache miss stores result
  - use_cache=False bypasses cache entirely
  - Cache key includes model (different models → different entries)
  - Module-level default cache and reset
"""

import time
import threading
from unittest.mock import MagicMock, patch

import pytest

from mycontext.utils.semantic_cache import (
    CacheStats,
    SemanticCache,
    get_default_cache,
    reset_default_cache,
)
from mycontext.providers.base import ProviderResponse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fake_response(text: str = "hello") -> ProviderResponse:
    return ProviderResponse(response=text, model="test-model", tokens_used=10)


# ---------------------------------------------------------------------------
# Basic semantics
# ---------------------------------------------------------------------------

class TestSemanticCacheBasic:

    def setup_method(self):
        self.cache = SemanticCache(ttl_seconds=60, max_size=10)

    def test_miss_on_empty_cache(self):
        assert self.cache.get("any prompt", "gpt-4o") is None

    def test_set_then_get(self):
        resp = _fake_response("answer")
        self.cache.set("prompt A", "gpt-4o", resp)
        result = self.cache.get("prompt A", "gpt-4o")
        assert result is resp

    def test_different_prompt_is_miss(self):
        self.cache.set("prompt A", "gpt-4o", _fake_response())
        assert self.cache.get("prompt B", "gpt-4o") is None

    def test_different_model_is_miss(self):
        self.cache.set("prompt A", "gpt-4o", _fake_response("A"))
        assert self.cache.get("prompt A", "gpt-4o-mini") is None

    def test_same_prompt_different_model_different_entries(self):
        resp_a = _fake_response("for gpt-4o")
        resp_b = _fake_response("for gpt-4o-mini")
        self.cache.set("shared prompt", "gpt-4o", resp_a)
        self.cache.set("shared prompt", "gpt-4o-mini", resp_b)
        assert self.cache.get("shared prompt", "gpt-4o") is resp_a
        assert self.cache.get("shared prompt", "gpt-4o-mini") is resp_b

    def test_overwrite_existing_entry(self):
        self.cache.set("prompt", "gpt-4o", _fake_response("v1"))
        self.cache.set("prompt", "gpt-4o", _fake_response("v2"))
        assert self.cache.get("prompt", "gpt-4o").response == "v2"

    def test_len_tracks_entries(self):
        assert len(self.cache) == 0
        self.cache.set("p1", "m", _fake_response())
        assert len(self.cache) == 1
        self.cache.set("p2", "m", _fake_response())
        assert len(self.cache) == 2

    def test_invalidate_removes_entry(self):
        self.cache.set("prompt", "m", _fake_response())
        removed = self.cache.invalidate("prompt", "m")
        assert removed is True
        assert self.cache.get("prompt", "m") is None

    def test_invalidate_nonexistent_returns_false(self):
        assert self.cache.invalidate("never stored", "m") is False

    def test_clear_empties_cache(self):
        self.cache.set("p1", "m", _fake_response())
        self.cache.set("p2", "m", _fake_response())
        self.cache.clear()
        assert len(self.cache) == 0
        assert self.cache.get("p1", "m") is None


# ---------------------------------------------------------------------------
# TTL expiry
# ---------------------------------------------------------------------------

class TestSemanticCacheTTL:

    def test_entry_expired_after_ttl(self):
        cache = SemanticCache(ttl_seconds=0.05)  # 50ms TTL
        cache.set("prompt", "m", _fake_response("fresh"))
        time.sleep(0.1)  # wait for expiry
        assert cache.get("prompt", "m") is None

    def test_entry_valid_before_ttl(self):
        cache = SemanticCache(ttl_seconds=10)
        cache.set("prompt", "m", _fake_response("still valid"))
        assert cache.get("prompt", "m") is not None

    def test_expired_entry_removed_on_get(self):
        cache = SemanticCache(ttl_seconds=0.05)
        cache.set("prompt", "m", _fake_response())
        time.sleep(0.1)
        cache.get("prompt", "m")  # triggers removal
        assert len(cache) == 0

    def test_expiration_counted_in_stats(self):
        cache = SemanticCache(ttl_seconds=0.05)
        cache.set("prompt", "m", _fake_response())
        time.sleep(0.1)
        cache.get("prompt", "m")
        stats = cache.stats()
        assert stats.expirations == 1


# ---------------------------------------------------------------------------
# Eviction
# ---------------------------------------------------------------------------

class TestSemanticCacheEviction:

    def test_oldest_evicted_when_full(self):
        cache = SemanticCache(ttl_seconds=60, max_size=3)
        cache.set("a", "m", _fake_response("A"))
        time.sleep(0.01)
        cache.set("b", "m", _fake_response("B"))
        time.sleep(0.01)
        cache.set("c", "m", _fake_response("C"))
        # Cache is now full (3 entries)
        cache.set("d", "m", _fake_response("D"))  # triggers eviction of "a"

        assert len(cache) == 3
        assert cache.get("a", "m") is None   # evicted
        assert cache.get("b", "m") is not None
        assert cache.get("c", "m") is not None
        assert cache.get("d", "m") is not None

    def test_eviction_counted_in_stats(self):
        cache = SemanticCache(ttl_seconds=60, max_size=2)
        cache.set("a", "m", _fake_response())
        cache.set("b", "m", _fake_response())
        cache.set("c", "m", _fake_response())  # evicts "a"
        assert cache.stats().evictions == 1


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

class TestCacheStats:

    def test_initial_stats_are_zero(self):
        cache = SemanticCache()
        s = cache.stats()
        assert s.hits == 0
        assert s.misses == 0
        assert s.total == 0
        assert s.hit_rate == 0.0

    def test_hit_increments_hits(self):
        cache = SemanticCache()
        cache.set("p", "m", _fake_response())
        cache.get("p", "m")
        assert cache.stats().hits == 1
        assert cache.stats().misses == 0

    def test_miss_increments_misses(self):
        cache = SemanticCache()
        cache.get("never stored", "m")
        assert cache.stats().misses == 1
        assert cache.stats().hits == 0

    def test_hit_rate_calculation(self):
        cache = SemanticCache()
        cache.set("p", "m", _fake_response())
        cache.get("p", "m")     # hit
        cache.get("p", "m")     # hit
        cache.get("miss", "m")  # miss
        s = cache.stats()
        assert s.hits == 2
        assert s.misses == 1
        assert abs(s.hit_rate - 2/3) < 0.01

    def test_stats_to_dict(self):
        cache = SemanticCache()
        d = cache.stats().to_dict()
        assert "hits" in d
        assert "misses" in d
        assert "hit_rate" in d
        assert "evictions" in d
        assert "total" in d

    def test_clear_resets_stats(self):
        cache = SemanticCache()
        cache.set("p", "m", _fake_response())
        cache.get("p", "m")  # hit
        cache.clear()
        s = cache.stats()
        assert s.hits == 0
        assert s.misses == 0


# ---------------------------------------------------------------------------
# Disabled cache
# ---------------------------------------------------------------------------

class TestSemanticCacheDisabled:

    def test_get_always_returns_none_when_disabled(self):
        cache = SemanticCache(enabled=False)
        cache.set("p", "m", _fake_response())  # should not actually store
        assert cache.get("p", "m") is None

    def test_set_does_nothing_when_disabled(self):
        cache = SemanticCache(enabled=False)
        cache.set("p", "m", _fake_response())
        assert len(cache) == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestSemanticCacheThreadSafety:

    def test_concurrent_writes_no_exception(self):
        cache = SemanticCache(ttl_seconds=60, max_size=1000)
        errors = []

        def writer(i):
            try:
                for j in range(20):
                    cache.set(f"prompt_{i}_{j}", "m", _fake_response(f"{i}_{j}"))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Thread errors: {errors}"

    def test_concurrent_reads_writes_consistent(self):
        cache = SemanticCache(ttl_seconds=60, max_size=1000)
        cache.set("shared", "m", _fake_response("original"))
        errors = []

        def reader():
            try:
                for _ in range(50):
                    result = cache.get("shared", "m")
                    # result is either the stored response or None (evicted)
                    if result is not None:
                        assert isinstance(result, ProviderResponse)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=reader) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0


# ---------------------------------------------------------------------------
# Default cache module API
# ---------------------------------------------------------------------------

class TestDefaultCache:

    def setup_method(self):
        reset_default_cache()

    def test_get_default_cache_returns_instance(self):
        cache = get_default_cache()
        assert isinstance(cache, SemanticCache)

    def test_get_default_cache_same_instance(self):
        c1 = get_default_cache()
        c2 = get_default_cache()
        assert c1 is c2

    def test_reset_clears_default_cache(self):
        cache = get_default_cache()
        cache.set("p", "m", _fake_response())
        reset_default_cache()
        assert cache.get("p", "m") is None


# ---------------------------------------------------------------------------
# LiteLLMProvider integration
# ---------------------------------------------------------------------------

class TestLiteLLMProviderCache:
    """Verify that LiteLLMProvider.generate() uses the cache correctly."""

    def setup_method(self):
        reset_default_cache()

    def _make_provider(self):
        from mycontext.providers.litellm_provider import LiteLLMProvider
        provider = LiteLLMProvider.__new__(LiteLLMProvider)
        provider._provider = "openai"
        provider.api_key = "test-key"
        provider.default_model = "gpt-4o-mini"
        provider.timeout = 30
        provider.max_retries = 1
        provider.retry_backoff = 1.0
        return provider

    def test_cache_hit_skips_litellm_call(self):
        """On a cache hit, litellm.completion() must NOT be called."""
        from mycontext import Context

        provider = self._make_provider()
        ctx = Context("test guidance")

        # Pre-populate cache
        fake_resp = _fake_response("cached answer")
        cache = get_default_cache()
        assembled = ctx.assemble()
        cache.set(prompt=assembled, model="gpt-4o-mini", response=fake_resp)

        with patch("litellm.completion") as mock_litellm:
            result = provider.generate(ctx, model="gpt-4o-mini", use_cache=True)

        mock_litellm.assert_not_called()
        assert result is fake_resp

    def test_cache_miss_calls_litellm(self):
        """On a cache miss, litellm.completion() MUST be called."""
        from mycontext import Context
        from mycontext.providers.base import ProviderResponse

        provider = self._make_provider()
        ctx = Context("unique guidance for miss test")

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "fresh answer"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = MagicMock(
            total_tokens=50, prompt_tokens=30, completion_tokens=20
        )

        with patch("litellm.completion", return_value=mock_response) as mock_litellm:
            with patch("litellm.completion_cost", return_value=0.001):
                result = provider.generate(ctx, model="gpt-4o-mini", use_cache=True)

        mock_litellm.assert_called_once()
        assert result.response == "fresh answer"

    def test_cache_stores_response_after_miss(self):
        """After a cache miss, the response is stored so the next call hits."""
        from mycontext import Context

        provider = self._make_provider()
        ctx = Context("guidance for store test")

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "stored answer"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = MagicMock(
            total_tokens=50, prompt_tokens=30, completion_tokens=20
        )

        with patch("litellm.completion", return_value=mock_response):
            with patch("litellm.completion_cost", return_value=0.0):
                first = provider.generate(ctx, model="gpt-4o-mini", use_cache=True)

        # Second call should hit the cache
        with patch("litellm.completion") as mock_litellm_2:
            second = provider.generate(ctx, model="gpt-4o-mini", use_cache=True)

        mock_litellm_2.assert_not_called()
        assert second.response == "stored answer"

    def test_use_cache_false_bypasses_cache(self):
        """use_cache=False must always call the LLM, even on repeated identical prompts."""
        from mycontext import Context

        provider = self._make_provider()
        ctx = Context("guidance for bypass test")

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "fresh"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = MagicMock(
            total_tokens=10, prompt_tokens=5, completion_tokens=5
        )

        with patch("litellm.completion", return_value=mock_response) as mock_litellm:
            with patch("litellm.completion_cost", return_value=0.0):
                provider.generate(ctx, model="gpt-4o-mini", use_cache=False)
                provider.generate(ctx, model="gpt-4o-mini", use_cache=False)

        assert mock_litellm.call_count == 2

    def test_cache_hit_has_zero_latency_overhead(self):
        """A cache hit should complete in under 5ms (no network I/O)."""
        from mycontext import Context

        provider = self._make_provider()
        ctx = Context("latency test guidance")

        fake_resp = _fake_response("fast")
        cache = get_default_cache()
        cache.set(prompt=ctx.assemble(), model="gpt-4o-mini", response=fake_resp)

        start = time.monotonic()
        for _ in range(100):
            provider.generate(ctx, model="gpt-4o-mini", use_cache=True)
        elapsed_ms = (time.monotonic() - start) * 1000

        # 100 cache hits in under 50ms total → < 0.5ms per hit
        assert elapsed_ms < 50, f"Cache hits too slow: {elapsed_ms:.1f}ms for 100 hits"
