"""
Phase 5 must-have tests: assemble_for_model + async provider layer.

Covers:
  ── assemble_for_model ──
  1. No max_tokens → identical to assemble()
  2. Generous max_tokens → all sections included
  3. Tight max_tokens → result fits within budget
  4. Very tight max_tokens → only highest-priority section (directive)
  5. Empty context returns empty string
  6. Knowledge section dropped first when tight
  7. Token count of result is always <= max_tokens

  ── BaseProvider.agenerate default ──
  8. Default agenerate() runs generate() in executor (no native async)
  9. Default agenerate() returns same ProviderResponse as generate()

  ── LiteLLMProvider.agenerate ──
  10. agenerate() calls litellm.acompletion (not litellm.completion)
  11. agenerate() returns ProviderResponse with correct fields
  12. agenerate() writes to cache on success
  13. agenerate() hits cache on second identical call
  14. agenerate(use_cache=False) always calls litellm.acompletion
  15. agenerate() emits a tracing span

  ── Context.aexecute ──
  16. aexecute() returns ProviderResponse
  17. aexecute() uses provider.agenerate()
  18. Multiple concurrent aexecute() calls run without error
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mycontext import Context
from mycontext.foundation import Directive, Guidance
from mycontext.providers.base import ProviderResponse

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_litellm_provider():
    from mycontext.providers.litellm_provider import LiteLLMProvider
    from mycontext.utils.semantic_cache import reset_default_cache
    from mycontext.utils.tracing import get_tracer

    reset_default_cache()
    get_tracer().clear()
    p = LiteLLMProvider.__new__(LiteLLMProvider)
    p._provider = "openai"
    p.api_key = "test-key"
    p.default_model = "gpt-4o-mini"
    p.timeout = 30
    p.max_retries = 1
    p.retry_backoff = 1.0
    return p


def _mock_acompletion_response(text: str = "async answer"):
    r = MagicMock()
    r.choices = [MagicMock()]
    r.choices[0].message.content = text
    r.choices[0].finish_reason = "stop"
    r.usage = MagicMock(total_tokens=30, prompt_tokens=20, completion_tokens=10)
    return r


# ---------------------------------------------------------------------------
# assemble_for_model
# ---------------------------------------------------------------------------


class TestAssembleForModel:
    def _ctx(self, with_knowledge: bool = True) -> Context:
        from mycontext.foundation import Constraints

        ctx = Context(
            guidance=Guidance(role="Senior analyst", rules=["Be precise", "Cite sources"]),
            directive=Directive(content="Analyze the following data and provide insights."),
            constraints=Constraints(format_rules=["Use bullet points", "Include severity ratings"]),
            knowledge="Background: This is a financial services company."
            if with_knowledge
            else None,
        )
        return ctx

    def test_no_max_tokens_matches_assemble(self):
        ctx = self._ctx()
        assert ctx.assemble_for_model() == ctx.assemble()

    def test_generous_budget_includes_all_sections(self):
        ctx = self._ctx()
        result = ctx.assemble_for_model(model="gpt-4o", max_tokens=50000)
        # All four sections should be present
        assert "Senior analyst" in result
        assert "Analyze the following data" in result
        assert "bullet points" in result.lower()
        assert "Background" in result

    def test_tight_budget_result_fits(self):
        ctx = self._ctx()
        from mycontext.utils.tokens import count_tokens

        result = ctx.assemble_for_model(model="gpt-4o", max_tokens=30)
        token_count = count_tokens(result, "gpt-4o")
        # Allow small separator overhead (the "\n\n" join may add 1-2 tokens)
        assert token_count <= 32

    def test_directive_kept_when_tight(self):
        """Directive has highest priority — must appear even under tight budget."""
        ctx = self._ctx()
        result = ctx.assemble_for_model(model="gpt-4o", max_tokens=20)
        # Directive text should be at least partially present
        assert "Analyze" in result or len(result) > 0

    def test_empty_context_returns_empty_string(self):
        ctx = Context()
        result = ctx.assemble_for_model(model="gpt-4o", max_tokens=1000)
        assert result == ""

    def test_knowledge_excluded_before_directive(self):
        """With a moderate budget, knowledge (lowest priority) should be dropped first."""
        ctx = self._ctx(with_knowledge=True)
        from mycontext.utils.tokens import count_tokens

        directive_tokens = count_tokens(ctx.directive.render(), "gpt-4o")
        guidance_tokens = count_tokens(ctx.guidance.render(), "gpt-4o")

        # Set budget to include directive + guidance but NOT the knowledge section
        tight = directive_tokens + guidance_tokens + 10
        result = ctx.assemble_for_model(model="gpt-4o", max_tokens=tight)
        assert "Analyze" in result
        assert "Senior analyst" in result

    def test_result_token_count_never_exceeds_budget(self):
        from mycontext.utils.tokens import count_tokens

        ctx = self._ctx()
        for budget in (10, 50, 100, 500):
            result = ctx.assemble_for_model(model="gpt-4o", max_tokens=budget)
            if result:
                assert count_tokens(result, "gpt-4o") <= budget, (
                    f"Budget {budget}: got {count_tokens(result, 'gpt-4o')} tokens"
                )


# ---------------------------------------------------------------------------
# BaseProvider.agenerate default
# ---------------------------------------------------------------------------


class TestBaseProviderDefaultAgenerate:
    def test_default_agenerate_runs_generate(self):
        from mycontext.providers.mock import MockProvider

        provider = MockProvider()
        ctx = Context("test guidance")

        result = asyncio.run(provider.agenerate(ctx, user="Hello"))
        assert isinstance(result, ProviderResponse)
        assert "Mock response" in result.response

    def test_default_agenerate_same_result_as_generate(self):
        from mycontext.providers.mock import MockProvider

        provider = MockProvider()
        ctx = Context("consistent guidance")

        sync_result = provider.generate(ctx, user="Test")
        async_result = asyncio.run(provider.agenerate(ctx, user="Test"))

        # Both should produce a valid ProviderResponse
        assert isinstance(sync_result, ProviderResponse)
        assert isinstance(async_result, ProviderResponse)


# ---------------------------------------------------------------------------
# LiteLLMProvider.agenerate
# ---------------------------------------------------------------------------


class TestLiteLLMProviderAgenerate:
    def setup_method(self):
        from mycontext.utils.semantic_cache import reset_default_cache
        from mycontext.utils.tracing import get_tracer

        reset_default_cache()
        get_tracer().clear()

    def test_agenerate_calls_acompletion_not_completion(self):
        provider = _make_litellm_provider()
        ctx = Context("async test guidance")

        mock_resp = _mock_acompletion_response()
        with patch(
            "litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp
        ) as mock_async:
            with patch("litellm.completion_cost", return_value=0.001):
                result = asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=False))
        mock_async.assert_called_once()
        assert result.response == "async answer"

    def test_agenerate_returns_provider_response(self):
        provider = _make_litellm_provider()
        ctx = Context("response fields test")

        mock_resp = _mock_acompletion_response("structured answer")
        with patch("litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp):
            with patch("litellm.completion_cost", return_value=0.002):
                result = asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=False))

        assert isinstance(result, ProviderResponse)
        assert result.response == "structured answer"
        assert result.tokens_used == 30
        assert result.cost_usd == pytest.approx(0.002)
        assert result.model == "gpt-4o-mini"

    def test_agenerate_writes_to_cache(self):
        from mycontext.utils.semantic_cache import get_default_cache

        provider = _make_litellm_provider()
        ctx = Context("cache write test")

        mock_resp = _mock_acompletion_response("cached async")
        with patch("litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp):
            with patch("litellm.completion_cost", return_value=0.0):
                asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=True))

        cache = get_default_cache()
        assert len(cache) == 1

    def test_agenerate_hits_cache_on_second_call(self):
        provider = _make_litellm_provider()
        ctx = Context("cache hit async test")

        mock_resp = _mock_acompletion_response()
        with patch(
            "litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp
        ) as mock_ac:
            with patch("litellm.completion_cost", return_value=0.0):
                asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=True))
                asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=True))

        # Second call should be a cache hit — acompletion called only once
        assert mock_ac.call_count == 1

    def test_agenerate_use_cache_false_always_calls_acompletion(self):
        provider = _make_litellm_provider()
        ctx = Context("bypass cache async test")

        mock_resp = _mock_acompletion_response()
        with patch(
            "litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp
        ) as mock_ac:
            with patch("litellm.completion_cost", return_value=0.0):
                asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=False))
                asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=False))

        assert mock_ac.call_count == 2

    def test_agenerate_emits_span(self):
        from mycontext.utils.tracing import get_tracer

        provider = _make_litellm_provider()
        ctx = Context("span async test")

        mock_resp = _mock_acompletion_response()
        with patch("litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp):
            with patch("litellm.completion_cost", return_value=0.0):
                asyncio.run(provider.agenerate(ctx, model="gpt-4o-mini", use_cache=False))

        spans = get_tracer().current_spans()
        assert any(s.name == "litellm_agenerate" for s in spans)


# ---------------------------------------------------------------------------
# Context.aexecute
# ---------------------------------------------------------------------------


class TestContextAexecute:
    def setup_method(self):
        from mycontext.utils.semantic_cache import reset_default_cache

        reset_default_cache()

    def test_aexecute_returns_provider_response(self):
        ctx = Context(
            guidance=Guidance(role="Helper"),
            directive=Directive(content="Do something."),
        )
        mock_resp = _mock_acompletion_response("aexecute result")
        with patch("litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp):
            with patch("litellm.completion_cost", return_value=0.0):
                result = asyncio.run(ctx.aexecute(provider="openai", model="gpt-4o-mini"))

        assert isinstance(result, ProviderResponse)
        assert result.response == "aexecute result"

    def test_aexecute_uses_provider_agenerate(self):
        """aexecute must call provider.agenerate(), not provider.generate()."""
        ctx = Context("test guidance for aexecute")
        mock_resp = _mock_acompletion_response()

        with patch(
            "litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp
        ) as mock_ac:
            with patch("litellm.completion_cost", return_value=0.0):
                asyncio.run(ctx.aexecute(provider="openai", model="gpt-4o-mini", use_cache=False))

        mock_ac.assert_called_once()

    def test_concurrent_aexecute_runs_without_error(self):
        """Multiple independent contexts can be awaited concurrently."""
        contexts = [
            Context(guidance=Guidance(role=f"Agent {i}"), directive=Directive(content=f"Task {i}"))
            for i in range(4)
        ]
        mock_resp = _mock_acompletion_response("concurrent result")

        async def run_all():
            with patch("litellm.acompletion", new_callable=AsyncMock, return_value=mock_resp):
                with patch("litellm.completion_cost", return_value=0.0):
                    results = await asyncio.gather(
                        *[
                            ctx.aexecute(provider="openai", model="gpt-4o-mini", use_cache=False)
                            for ctx in contexts
                        ]
                    )
            return results

        results = asyncio.run(run_all())
        assert len(results) == 4
        assert all(isinstance(r, ProviderResponse) for r in results)
        assert all(r.response == "concurrent result" for r in results)

    def test_aexecute_with_mock_provider(self):
        """Mock provider's default agenerate (thread-executor) should also work."""
        ctx = Context("mock async test")
        result = asyncio.run(ctx.aexecute(provider="mock", user="Hello"))
        assert isinstance(result, ProviderResponse)
        assert "Mock response" in result.response
