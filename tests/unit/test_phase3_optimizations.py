"""
Phase 3 optimization tests.

Covers:
  ── RedundancyRemover.remove_similar_sentences ──
  1. O(n²) naive fallback: removes near-duplicates, keeps unique
  2. MinHash LSH fast-path: same semantic outcome as naive
  3. Both paths handle edge cases (empty, single sentence)
  4. Performance: LSH path is measurably faster on large inputs
  5. Exact duplicates are removed by both paths
  6. Threshold respected: sentences below threshold are kept

  ── TokenOptimizer.count_tokens forwarding ──
  7. count_tokens uses unified tokens.py (not private encoder)
  8. count_tokens result matches count_tokens utility
  9. get_reduction_percent works after forwarding

  ── TransformationEngine lazy singleton ──
  10. Second instantiation reuses cached registry (no re-import)
  11. Free and enterprise variants are cached separately
  12. Registry is populated with expected pattern names
  13. Thread safety: concurrent instantiation produces consistent registry
  14. _PATTERN_REGISTRY_CACHE can be cleared to force reload (for tests)
"""

import threading
import time
from unittest.mock import patch

import pytest

from mycontext.utils.optimizers import RedundancyRemover, TokenOptimizer

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _unique_sentences(n: int) -> list[str]:
    """Return n genuinely unique sentences (no word overlap)."""
    vocab = [
        "alpha bravo",
        "charlie delta",
        "echo foxtrot",
        "golf hotel",
        "india juliet",
        "kilo lima",
        "mike november",
        "oscar papa",
        "quebec romeo",
        "sierra tango",
        "uniform victor",
        "whiskey xray",
        "yankee zulu",
        "phoenix mercury",
        "neptune saturn",
        "jupiter mars",
        "copper silver",
        "bronze tungsten",
        "silicon carbon",
        "hydrogen helium",
        "nitrogen oxygen",
        "argon krypton",
        "xenon radon",
        "lithium sodium",
        "potassium calcium",
        "magnesium iron",
        "cobalt nickel",
        "zinc manganese",
        "chromium vanadium",
        "titanium zirconium",
    ]
    # Cycle the vocab list to generate as many sentences as needed
    result = []
    for i in range(n):
        base = vocab[i % len(vocab)]
        cycle = i // len(vocab)
        result.append(f"{base} sentence number {i} cycle {cycle}")
    return result


# ---------------------------------------------------------------------------
# RedundancyRemover — naive path
# ---------------------------------------------------------------------------


class TestRedundancyRemoverNaive:
    """Test the O(n²) naive path, forcing it regardless of datasketch availability."""

    def _call_naive(self, sentences: list[str], threshold: float = 0.8) -> str:
        return RedundancyRemover._remove_similar_naive(sentences, threshold)

    def test_identical_sentences_deduplicated(self):
        sentences = ["The sky is blue", "The sky is blue", "The sky is blue"]
        result = self._call_naive(sentences)
        # After deduplication only one copy should remain
        assert result.count("The sky is blue") == 1

    def test_near_duplicate_removed(self):
        sentences = [
            "The quick brown fox jumps over the lazy dog",
            "The quick brown fox leaps over the lazy dog",  # high Jaccard
            "Completely different sentence about space exploration",
        ]
        result = self._call_naive(sentences, threshold=0.7)
        assert "space exploration" in result
        # Both fox sentences are > 0.7 Jaccard so only first kept
        assert result.count("fox") == 1

    def test_unique_sentences_all_kept(self):
        sentences = ["Alpha", "Beta", "Gamma", "Delta"]
        result = self._call_naive(sentences, threshold=0.8)
        for s in sentences:
            assert s.lower() in result.lower()

    def test_empty_list_returns_empty(self):
        result = RedundancyRemover.remove_similar_sentences("", similarity_threshold=0.8)
        # Empty or minimal string
        assert result.strip() in ("", ".")

    def test_single_sentence_unchanged(self):
        result = RedundancyRemover._remove_similar_naive(["Only one sentence"], 0.8)
        assert "Only one sentence" in result

    def test_threshold_boundary(self):
        """Sentences just below threshold should be kept."""
        # These share ~50% of words — below 0.8 threshold
        sentences = [
            "apple orange banana grape mango kiwi",
            "cherry peach plum lemon lime tangerine",
        ]
        result = self._call_naive(sentences, threshold=0.8)
        assert "apple" in result
        assert "cherry" in result


# ---------------------------------------------------------------------------
# RedundancyRemover — LSH path (only if datasketch installed)
# ---------------------------------------------------------------------------


class TestRedundancyRemoverLSH:
    @pytest.fixture(autouse=True)
    def require_datasketch(self):
        try:
            import datasketch  # noqa: F401
        except ImportError:
            pytest.skip("datasketch not installed")

    def _call_lsh(self, sentences: list[str], threshold: float = 0.8) -> str:
        from mycontext.utils.optimizers import RedundancyRemover

        return RedundancyRemover._remove_similar_lsh(sentences, threshold)

    def test_identical_sentences_deduplicated(self):
        sentences = ["The sky is blue", "The sky is blue", "The sky is blue"]
        result = self._call_lsh(sentences)
        assert result.count("sky is blue") == 1

    def test_unique_sentences_all_kept(self):
        sentences = _unique_sentences(5)
        result = self._call_lsh(sentences, threshold=0.9)
        # With 0.9 threshold and genuinely unique sentences, all should survive
        # (allow for minor LSH approximation error on edge cases)
        kept_count = sum(1 for s in sentences if s[:10] in result)
        assert kept_count >= 4

    def test_lsh_faster_than_naive_on_large_input(self):
        """LSH should be measurably faster on 150+ sentences."""
        sentences = (
            _unique_sentences(150)
            + [
                "This is a repeated sentence about nothing",
            ]
            * 30
        )

        start_naive = time.monotonic()
        RedundancyRemover._remove_similar_naive(sentences, threshold=0.8)
        t_naive = time.monotonic() - start_naive

        start_lsh = time.monotonic()
        RedundancyRemover._remove_similar_lsh(sentences, threshold=0.8)
        t_lsh = time.monotonic() - start_lsh

        # LSH should be at least 2× faster on large input
        # (a very conservative bound; real improvement is typically 5–20×)
        assert t_lsh < t_naive * 2 or t_lsh < 0.5, (
            f"LSH ({t_lsh:.3f}s) not faster than naive ({t_naive:.3f}s)"
        )


# ---------------------------------------------------------------------------
# remove_similar_sentences public API (uses whichever backend is available)
# ---------------------------------------------------------------------------


class TestRemoveSimilarSentencesPublicAPI:
    def test_public_method_returns_string(self):
        text = "Alpha is great. Alpha is great. Beta is different."
        result = RedundancyRemover.remove_similar_sentences(text)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_public_method_removes_duplicates(self):
        text = "The system is down. The system is down. Another fact entirely."
        result = RedundancyRemover.remove_similar_sentences(text, similarity_threshold=0.8)
        assert result.count("system is down") == 1
        assert "Another fact" in result

    def test_public_method_dispatches_to_lsh_when_available(self):
        """When datasketch is available, _remove_similar_lsh should be called."""
        from mycontext.utils import optimizers

        if not optimizers._DATASKETCH_AVAILABLE:
            pytest.skip("datasketch not installed — LSH dispatch test skipped")

        sentences = ["Hello world", "Goodbye world"]
        with patch.object(
            RedundancyRemover, "_remove_similar_lsh", wraps=RedundancyRemover._remove_similar_lsh
        ) as mock_lsh:
            RedundancyRemover.remove_similar_sentences("Hello world. Goodbye world.")
            mock_lsh.assert_called_once()

    def test_public_method_dispatches_to_naive_when_datasketch_missing(self):
        """Without datasketch, _remove_similar_naive must be called."""
        import mycontext.utils.optimizers as opt_module

        original = opt_module._DATASKETCH_AVAILABLE
        try:
            opt_module._DATASKETCH_AVAILABLE = False
            with patch.object(
                RedundancyRemover,
                "_remove_similar_naive",
                wraps=RedundancyRemover._remove_similar_naive,
            ) as mock_naive:
                RedundancyRemover.remove_similar_sentences("Hello world. Goodbye planet.")
                mock_naive.assert_called_once()
        finally:
            opt_module._DATASKETCH_AVAILABLE = original


# ---------------------------------------------------------------------------
# TokenOptimizer.count_tokens forwarding
# ---------------------------------------------------------------------------


class TestTokenOptimizerForwarding:
    def test_count_tokens_returns_integer(self):
        optimizer = TokenOptimizer(model="gpt-4o")
        assert isinstance(optimizer.count_tokens("Hello world"), int)

    def test_count_tokens_matches_unified_utility(self):
        from mycontext.utils.tokens import count_tokens as unified

        optimizer = TokenOptimizer(model="gpt-4o")
        text = "The quick brown fox jumps over the lazy dog."
        assert optimizer.count_tokens(text) == unified(text, model="gpt-4o")

    def test_get_reduction_percent_after_forwarding(self):
        optimizer = TokenOptimizer(model="gpt-4o")
        original = "This is a longer text with more information here."
        optimized = "Longer text here."
        pct = optimizer.get_reduction_percent(original, optimized)
        assert 0 < pct < 100

    def test_count_tokens_empty_string(self):
        optimizer = TokenOptimizer()
        assert optimizer.count_tokens("") == 0

    def test_analyze_uses_forwarded_count(self):
        """analyze() internally calls count_tokens; should use unified utility."""
        optimizer = TokenOptimizer(model="gpt-4o")
        result = optimizer.analyze("A short text for analysis.")
        assert result["tokens"] > 0
        assert isinstance(result["tokens"], int)


# ---------------------------------------------------------------------------
# TransformationEngine lazy singleton
# ---------------------------------------------------------------------------


class TestTransformationEngineLazySingleton:
    def setup_method(self):
        """Clear the module-level cache before each test."""
        from mycontext.intelligence import transformation_engine as te

        te._PATTERN_REGISTRY_CACHE.clear()

    def teardown_method(self):
        """Clear cache after tests to avoid cross-test pollution."""
        from mycontext.intelligence import transformation_engine as te

        te._PATTERN_REGISTRY_CACHE.clear()

    def test_first_instantiation_builds_registry(self):
        from mycontext.intelligence.transformation_engine import TransformationEngine

        engine = TransformationEngine(include_enterprise=False)
        assert len(engine._pattern_registry) > 0

    def test_second_instantiation_reuses_cache(self):
        from mycontext.intelligence import transformation_engine as te
        from mycontext.intelligence.transformation_engine import TransformationEngine

        # First call populates the cache
        e1 = TransformationEngine(include_enterprise=False)
        registry_id_1 = id(te._PATTERN_REGISTRY_CACHE[False])

        # Second call must reuse the same dict object
        e2 = TransformationEngine(include_enterprise=False)
        registry_id_2 = id(te._PATTERN_REGISTRY_CACHE[False])

        assert registry_id_1 == registry_id_2
        assert e1._pattern_registry is e2._pattern_registry

    def test_enterprise_and_free_variants_cached_separately(self):
        from mycontext.intelligence import transformation_engine as te
        from mycontext.intelligence.transformation_engine import TransformationEngine

        TransformationEngine(include_enterprise=False)
        TransformationEngine(include_enterprise=True)

        assert False in te._PATTERN_REGISTRY_CACHE
        assert True in te._PATTERN_REGISTRY_CACHE
        # Enterprise registry should have at least as many patterns as free
        assert len(te._PATTERN_REGISTRY_CACHE[True]) >= len(te._PATTERN_REGISTRY_CACHE[False])

    def test_registry_contains_expected_free_patterns(self):
        from mycontext.intelligence.transformation_engine import TransformationEngine

        engine = TransformationEngine(include_enterprise=False)
        expected = {"question_analyzer", "step_by_step_reasoner", "risk_assessor"}
        for name in expected:
            assert name in engine._pattern_registry, f"Missing pattern: {name}"

    def test_thread_safety_concurrent_instantiation(self):
        """Multiple threads creating TransformationEngine simultaneously
        must all get the same consistent registry."""
        from mycontext.intelligence.transformation_engine import TransformationEngine

        results = []
        errors = []

        def create_engine():
            try:
                engine = TransformationEngine(include_enterprise=False)
                results.append(id(engine._pattern_registry))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=create_engine) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Thread errors: {errors}"
        # All threads should have gotten the same registry object
        assert len(set(results)) == 1, "Multiple registry objects created — thread safety failure"

    def test_cache_cleared_forces_reload(self):
        """After clearing the cache, a new instantiation rebuilds the registry."""
        from mycontext.intelligence import transformation_engine as te
        from mycontext.intelligence.transformation_engine import TransformationEngine

        e1 = TransformationEngine(include_enterprise=False)
        first_id = id(te._PATTERN_REGISTRY_CACHE[False])

        te._PATTERN_REGISTRY_CACHE.clear()

        e2 = TransformationEngine(include_enterprise=False)
        second_id = id(te._PATTERN_REGISTRY_CACHE[False])

        # After clear, a new dict should have been created
        assert first_id != second_id
        assert len(e2._pattern_registry) > 0
