"""
Tests for structured logging — verifying that previously silent exceptions
are now surfaced via logger.warning() instead of being swallowed.

These tests do NOT make real LLM calls. They use mocking to simulate failures
and assert that:
  1. A warning is logged with the right message/level.
  2. The calling function still returns a usable fallback (no crash).
  3. Error information is preserved (not lost) in metadata or return value.
"""

import logging
from unittest.mock import MagicMock, patch

from mycontext.intelligence.prompt_composer import ComposedPrompt, PromptComposer

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_warnings(caplog):
    return [r for r in caplog.records if r.levelno == logging.WARNING]


# ---------------------------------------------------------------------------
# PromptComposer
# ---------------------------------------------------------------------------


class TestPromptComposerLogging:
    """Verify that PromptComposer logs warnings instead of silently swallowing errors."""

    def test_compose_llm_failure_logs_warning(self, caplog):
        """compose(): when the LLM merge call raises, a warning is logged and fallback is used."""
        composer = PromptComposer()

        # Context is imported at top level in prompt_composer.py
        with patch("mycontext.intelligence.prompt_composer.Context") as MockCtx:
            mock_instance = MagicMock()
            mock_instance.execute.side_effect = RuntimeError("LLM unavailable")
            MockCtx.return_value = mock_instance

            with caplog.at_level(logging.WARNING, logger="mycontext.intelligence.prompt_composer"):
                result = composer.compose(
                    prompts=["Prompt A.", "Prompt B."],
                    question="test question",
                    provider="openai",
                )

        assert isinstance(result, ComposedPrompt)
        assert result.metadata.get("composition_mode") == "fallback"
        assert "LLM unavailable" in result.metadata.get("error", "")
        warnings = _get_warnings(caplog)
        assert any("compose" in r.message and "LLM merge" in r.message for r in warnings), (
            f"Expected compose warning, got: {[r.message for r in warnings]}"
        )

    def test_compose_llm_failure_fallback_is_non_empty(self, caplog):
        """Fallback result must be non-empty."""
        composer = PromptComposer()

        with patch("mycontext.intelligence.prompt_composer.Context") as MockCtx:
            mock_instance = MagicMock()
            mock_instance.execute.side_effect = ConnectionError("Timeout")
            MockCtx.return_value = mock_instance

            with caplog.at_level(logging.WARNING, logger="mycontext.intelligence.prompt_composer"):
                result = composer.compose(
                    prompts=["Alpha prompt content.", "Beta prompt content."],
                    question="my question",
                    provider="openai",
                )

        assert len(result.prompt) > 0

    def test_compose_failure_is_warning_not_error(self, caplog):
        """Fallback failures should be logged as WARNING, never ERROR.
        Note: compose() short-circuits to passthrough when len(prompts)==1,
        so we need at least 2 prompts to trigger the LLM merge path."""
        composer = PromptComposer()

        with patch("mycontext.intelligence.prompt_composer.Context") as MockCtx:
            mock_instance = MagicMock()
            mock_instance.execute.side_effect = RuntimeError("test")
            MockCtx.return_value = mock_instance

            with caplog.at_level(logging.DEBUG, logger="mycontext.intelligence.prompt_composer"):
                composer.compose(
                    prompts=["Prompt A content.", "Prompt B content."],
                    question="q",
                    provider="openai",
                )

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(warning_records) >= 1
        assert len(error_records) == 0, (
            f"Fallback failures should be WARNING not ERROR. Got errors: {[r.message for r in error_records]}"
        )

    def test_compose_from_templates_bad_klass_logs_warning(self, caplog):
        """compose_from_templates(): a template whose build_context raises logs a warning."""
        composer = PromptComposer()

        bad_klass = MagicMock()
        bad_klass.return_value.build_context.side_effect = ValueError("bad template config")

        # get_pattern_class is imported inside compose_from_templates from .pattern_suggester
        # Patch it at the source module so the local import picks up the mock
        with patch(
            "mycontext.intelligence.pattern_suggester.get_pattern_class",
            return_value=bad_klass,
        ):
            # Also patch it at prompt_composer's local import resolution
            with patch(
                "mycontext.intelligence.prompt_composer.PromptComposer.compose_from_templates",
                wraps=composer.compose_from_templates,
            ):
                pass  # wraps trick not needed; patch at function-call time below

        # Simpler approach: monkeypatch the function-local import by patching
        # the actual function in pattern_suggester that is called
        original_get = None
        try:
            import mycontext.intelligence.pattern_suggester as ps

            original_get = ps.get_pattern_class
            ps.get_pattern_class = lambda name, include_enterprise=False: bad_klass

            with caplog.at_level(logging.WARNING, logger="mycontext.intelligence.prompt_composer"):
                result = composer.compose_from_templates(
                    question="test question",
                    template_names=["bad_template"],
                    refine=False,
                )
        finally:
            if original_get is not None:
                ps.get_pattern_class = original_get

        warnings = _get_warnings(caplog)
        assert any("compose_from_templates" in r.message for r in warnings), (
            f"Expected compose_from_templates warning. Got: {[r.message for r in warnings]}"
        )
        assert isinstance(result, ComposedPrompt)

    def test_compile_generic_failure_logs_warning(self, caplog):
        """compile_generic(): a template whose generic_prompt() raises logs a warning."""
        composer = PromptComposer()

        mock_instance = MagicMock()
        mock_instance.generic_prompt.side_effect = NotImplementedError("no generic prompt")

        with patch(
            "mycontext.intelligence.prompt_composer._resolve_generic_template",
            return_value=(mock_instance, "some_template"),
        ):
            with caplog.at_level(logging.WARNING, logger="mycontext.intelligence.prompt_composer"):
                result = composer.compile_generic(
                    question="test question",
                    template_names=["some_template"],
                )

        warnings = _get_warnings(caplog)
        assert any("compile_generic" in r.message for r in warnings), (
            f"Expected compile_generic warning. Got: {[r.message for r in warnings]}"
        )
        assert isinstance(result, ComposedPrompt)

    def test_get_generic_prompt_for_failure_logs_warning(self, caplog):
        """get_generic_prompt_for(): generic_prompt() failure warns and returns None."""
        from mycontext.intelligence.prompt_composer import get_generic_prompt_for

        mock_instance = MagicMock()
        mock_instance.generic_prompt.side_effect = RuntimeError("boom")

        with patch(
            "mycontext.intelligence.prompt_composer._resolve_generic_template",
            return_value=(mock_instance, "any_template"),
        ):
            # PATTERN_BUILD_CONTEXT_REGISTRY is imported locally inside get_generic_prompt_for
            # from chain_orchestration_agent — patch it there
            with patch(
                "mycontext.intelligence.chain_orchestration_agent.PATTERN_BUILD_CONTEXT_REGISTRY",
                {"any_template": ("input", {})},
            ):
                with caplog.at_level(
                    logging.WARNING,
                    logger="mycontext.intelligence.prompt_composer",
                ):
                    result = get_generic_prompt_for("any_template", "test question")

        assert result is None
        warnings = _get_warnings(caplog)
        assert any("get_generic_prompt_for" in r.message for r in warnings), (
            f"Expected get_generic_prompt_for warning. Got: {[r.message for r in warnings]}"
        )


# ---------------------------------------------------------------------------
# TemplateIntegratorAgent
# ---------------------------------------------------------------------------


class TestTemplateIntegratorLogging:
    """Verify that TemplateIntegratorAgent._get_template_detail logs warnings."""

    def test_get_template_detail_failure_logs_warning(self, caplog):
        """_get_template_detail(): when build_context raises, a warning is logged."""
        from mycontext.intelligence.template_integrator_agent import TemplateIntegratorAgent

        agent = TemplateIntegratorAgent()

        bad_klass = MagicMock()
        bad_klass.return_value.build_context.side_effect = RuntimeError("context error")

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: bad_klass

            with caplog.at_level(
                logging.WARNING,
                logger="mycontext.intelligence.template_integrator_agent",
            ):
                result = agent._get_template_detail("some_pattern")
        finally:
            ps.get_pattern_class = original_get

        assert result == ""
        warnings = _get_warnings(caplog)
        assert any("_get_template_detail" in r.message for r in warnings), (
            f"Expected _get_template_detail warning. Got: {[r.message for r in warnings]}"
        )

    def test_get_template_detail_missing_class_returns_empty(self):
        """_get_template_detail(): when pattern class is None, returns '' (no warning needed)."""
        from mycontext.intelligence.template_integrator_agent import TemplateIntegratorAgent

        agent = TemplateIntegratorAgent()

        import mycontext.intelligence.pattern_suggester as ps

        original_get = ps.get_pattern_class
        try:
            ps.get_pattern_class = lambda name, include_enterprise=False: None
            result = agent._get_template_detail("nonexistent_pattern")
        finally:
            ps.get_pattern_class = original_get

        assert result == ""


# ---------------------------------------------------------------------------
# PatternSuggester
# ---------------------------------------------------------------------------


class TestPatternSuggesterLogging:
    """Verify that _suggest_with_llm logs warnings on failure."""

    def test_suggest_with_llm_failure_logs_warning(self, caplog):
        """_suggest_with_llm(): LLM call failure must be logged as WARNING."""
        # Context is imported locally inside _suggest_with_llm: from ..core import Context
        # Patch at the source: mycontext.core.Context
        import mycontext.core as core_mod
        from mycontext.intelligence import pattern_suggester

        original_ctx = core_mod.Context

        class FakeContext:
            def __init__(self, **kwargs):
                pass

            def execute(self, **kwargs):
                raise ConnectionError("API timeout")

        try:
            core_mod.Context = FakeContext

            with caplog.at_level(
                logging.WARNING,
                logger="mycontext.intelligence.pattern_suggester",
            ):
                result = pattern_suggester._suggest_with_llm(
                    question="What is the best strategy?",
                    provider="openai",
                    temperature=0.3,
                    model="gpt-4o-mini",
                )
        finally:
            core_mod.Context = original_ctx

        names, integration_note, error_str = result
        assert names == []
        assert "API timeout" in error_str
        warnings = _get_warnings(caplog)
        assert any("_suggest_with_llm" in r.message for r in warnings), (
            f"Expected _suggest_with_llm warning. Got: {[r.message for r in warnings]}"
        )

    def test_suggest_with_llm_failure_preserves_error_string(self):
        """The error tuple must include the original exception message."""
        import mycontext.core as core_mod
        from mycontext.intelligence import pattern_suggester

        original_ctx = core_mod.Context

        class FakeContext:
            def __init__(self, **kwargs):
                pass

            def execute(self, **kwargs):
                raise ValueError("Invalid API key: sk-xxx")

        try:
            core_mod.Context = FakeContext
            names, note, err = pattern_suggester._suggest_with_llm(
                question="test",
                provider="openai",
                temperature=0.3,
                model="gpt-4o-mini",
            )
        finally:
            core_mod.Context = original_ctx

        assert "Invalid API key" in err
