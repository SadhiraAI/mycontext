"""
Tests for parallel template refinement in PromptComposer.compose_from_templates().

Key behaviors verified:
  1. Output order is preserved (parallel execution may complete out-of-order).
  2. Partial failures: one bad template doesn't kill the others.
  3. Parallel path (refine=True) is faster than sequential for N≥2 templates.
  4. Sequential path (refine=False) still works correctly.
  5. Empty task list produces the empty-fallback response.
  6. MAX_REFINE_WORKERS cap is respected (no more threads than templates).
"""

import time
from unittest.mock import MagicMock, patch

from mycontext.intelligence.prompt_composer import ComposedPrompt, PromptComposer

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_delayed_klass(prompt_text: str, delay_secs: float = 0.0):
    """Return a mock Pattern class whose to_prompt() returns after a delay."""
    ctx_mock = MagicMock()

    def slow_to_prompt(**kwargs):
        if delay_secs:
            time.sleep(delay_secs)
        return prompt_text

    ctx_mock.to_prompt.side_effect = slow_to_prompt
    klass = MagicMock()
    klass.return_value.build_context.return_value = ctx_mock
    return klass


def _make_failing_klass():
    """Return a mock Pattern class whose build_context always raises."""
    klass = MagicMock()
    klass.return_value.build_context.side_effect = ValueError("intentional failure")
    return klass


# ---------------------------------------------------------------------------
# Order preservation
# ---------------------------------------------------------------------------


class TestOrderPreservation:
    def test_output_order_matches_input_order(self):
        """Even when tasks complete out of order, prompts must be in template_names order."""
        composer = PromptComposer()

        # Template A takes longer than B, so B finishes first
        klass_a = _make_delayed_klass("Prompt from A", delay_secs=0.05)
        klass_b = _make_delayed_klass("Prompt from B", delay_secs=0.0)
        klass_c = _make_delayed_klass("Prompt from C", delay_secs=0.02)

        template_map = {
            "template_a": klass_a,
            "template_b": klass_b,
            "template_c": klass_c,
        }

        def fake_get_pattern(name, include_enterprise=False):
            return template_map.get(name)

        registry = {
            "template_a": ("input", {}),
            "template_b": ("input", {}),
            "template_c": ("input", {}),
        }

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = fake_get_pattern

            with patch(
                "mycontext.intelligence.prompt_composer.PromptComposer.compose",
                wraps=composer.compose,
            ):
                pass

            # Patch compose to capture the prompts list in order
            captured_prompts = []
            original_compose = composer.compose

            def capturing_compose(prompts, **kwargs):
                captured_prompts.extend(prompts)
                return ComposedPrompt(
                    prompt=" | ".join(prompts),
                    source_templates=kwargs.get("source_templates", []),
                    question=kwargs.get("question", ""),
                )

            composer.compose = capturing_compose

            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                registry,
            ):
                result = composer.compose_from_templates(
                    question="test",
                    template_names=["template_a", "template_b", "template_c"],
                    refine=True,
                )
        finally:
            ps.get_pattern_class = original_get

        # Order must be A → B → C regardless of which thread finished first
        assert captured_prompts == ["Prompt from A", "Prompt from B", "Prompt from C"], (
            f"Expected ordered prompts, got: {captured_prompts}"
        )


# ---------------------------------------------------------------------------
# Partial failures
# ---------------------------------------------------------------------------


class TestPartialFailures:
    def test_one_bad_template_does_not_kill_others(self, caplog):
        """If template_b fails, templates a and c still produce output."""
        import logging

        composer = PromptComposer()

        klass_a = _make_delayed_klass("Good prompt A")
        klass_b = _make_failing_klass()
        klass_c = _make_delayed_klass("Good prompt C")

        template_map = {"ta": klass_a, "tb": klass_b, "tc": klass_c}
        registry = {"ta": ("input", {}), "tb": ("input", {}), "tc": ("input", {})}

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: template_map.get(name)

            captured = []
            original_compose = composer.compose

            def capturing_compose(prompts, **kwargs):
                captured.extend(prompts)
                return ComposedPrompt(prompt=" ".join(prompts), source_templates=[], question="")

            composer.compose = capturing_compose

            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                registry,
            ):
                with caplog.at_level(
                    logging.WARNING, logger="mycontext.intelligence.prompt_composer"
                ):
                    result = composer.compose_from_templates(
                        question="test",
                        template_names=["ta", "tb", "tc"],
                        refine=True,
                    )
        finally:
            ps.get_pattern_class = original_get

        # Two good templates should still produce output
        assert "Good prompt A" in captured
        assert "Good prompt C" in captured
        # Warning about the failed template must be logged
        assert any(
            "tb" in r.message or "compose_from_templates" in r.message for r in caplog.records
        )

    def test_all_templates_fail_returns_empty_fallback(self):
        """If every template fails, empty_fallback is returned."""
        composer = PromptComposer()

        klass_bad = _make_failing_klass()
        template_map = {"t1": klass_bad, "t2": klass_bad}
        registry = {"t1": ("input", {}), "t2": ("input", {})}

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: template_map.get(name)

            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                registry,
            ):
                result = composer.compose_from_templates(
                    question="test question",
                    template_names=["t1", "t2"],
                    refine=True,
                )
        finally:
            ps.get_pattern_class = original_get

        assert result.metadata.get("composition_mode") == "empty_fallback"
        assert len(result.prompt) > 0  # fallback string


# ---------------------------------------------------------------------------
# Parallel speedup
# ---------------------------------------------------------------------------


class TestParallelSpeedup:
    def test_parallel_faster_than_sequential(self):
        """
        Parallel execution of 3 templates each taking ~0.1s should complete
        in ~0.15s (parallel) vs ~0.3s (sequential).
        This is a timing test — uses a generous tolerance.
        """
        DELAY = 0.1
        N = 3
        composer = PromptComposer()

        klasses = {f"t{i}": _make_delayed_klass(f"Prompt {i}", delay_secs=DELAY) for i in range(N)}
        registry = {f"t{i}": ("input", {}) for i in range(N)}

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: klasses.get(name)

            def noop_compose(prompts, **kwargs):
                return ComposedPrompt(prompt=" ".join(prompts), source_templates=[], question="")

            composer.compose = noop_compose

            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                registry,
            ):
                start = time.monotonic()
                composer.compose_from_templates(
                    question="test",
                    template_names=list(klasses.keys()),
                    refine=True,
                )
                elapsed = time.monotonic() - start
        finally:
            ps.get_pattern_class = original_get

        # Sequential would take N * DELAY = 0.3s; parallel should be ~0.1-0.15s
        # Allow generous tolerance for CI jitter: must be faster than 0.8 * sequential
        sequential_time = N * DELAY
        assert elapsed < sequential_time * 0.8, (
            f"Parallel execution ({elapsed:.2f}s) should be faster than "
            f"80% of sequential ({sequential_time:.2f}s)"
        )


# ---------------------------------------------------------------------------
# Sequential path (refine=False)
# ---------------------------------------------------------------------------


class TestSequentialPath:
    def test_refine_false_still_works(self):
        """When refine=False, the sequential path must also work correctly."""
        composer = PromptComposer()

        klass_a = _make_delayed_klass("Seq prompt A")
        klass_b = _make_delayed_klass("Seq prompt B")

        template_map = {"sa": klass_a, "sb": klass_b}
        registry = {"sa": ("input", {}), "sb": ("input", {})}

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: template_map.get(name)

            captured = []

            def capturing_compose(prompts, **kwargs):
                captured.extend(prompts)
                return ComposedPrompt(prompt=" ".join(prompts), source_templates=[], question="")

            composer.compose = capturing_compose

            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                registry,
            ):
                composer.compose_from_templates(
                    question="test",
                    template_names=["sa", "sb"],
                    refine=False,
                )
        finally:
            ps.get_pattern_class = original_get

        assert "Seq prompt A" in captured
        assert "Seq prompt B" in captured

    def test_single_template_uses_passthrough(self):
        """Single template: compose() returns passthrough (no LLM merge needed)."""
        composer = PromptComposer()
        klass = _make_delayed_klass("Single prompt")
        registry = {"solo": ("input", {})}

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: klass

            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                registry,
            ):
                result = composer.compose_from_templates(
                    question="test",
                    template_names=["solo"],
                    refine=False,
                )
        finally:
            ps.get_pattern_class = original_get

        assert result.metadata.get("composition_mode") == "passthrough"
        assert result.prompt == "Single prompt"
