"""
Tests for the heuristic complexity pre-screen in pattern_suggester.

Covers:
  - Arithmetic expressions → raw (no LLM)
  - Very short simple questions → raw (no LLM)
  - Short questions WITH complexity signals → pass to LLM (returns None)
  - Simple factual openers without complexity → raw (no LLM)
  - Complex factual openers WITH complexity signals → pass to LLM (returns None)
  - Empty / whitespace-only input → pass to LLM (returns None)
  - assess_complexity uses heuristic fast-path (no LLM call)
  - assess_complexity with skip_heuristic=True calls LLM
"""

import pytest
from unittest.mock import MagicMock, patch

from mycontext.intelligence.pattern_suggester import (
    ComplexityResult,
    _heuristic_classify,
    assess_complexity,
)


# ---------------------------------------------------------------------------
# Direct heuristic tests
# ---------------------------------------------------------------------------

class TestHeuristicClassify:

    def test_pure_arithmetic_returns_raw(self):
        result = _heuristic_classify("2 + 2")
        assert result is not None
        assert result.recommendation == "raw"
        assert result.complexity == "low"

    def test_arithmetic_with_question_mark(self):
        result = _heuristic_classify("12 * 7 =?")
        assert result is not None
        assert result.recommendation == "raw"

    def test_float_arithmetic(self):
        result = _heuristic_classify("3.14 * 2.0")
        assert result is not None
        assert result.recommendation == "raw"

    def test_short_simple_question_returns_raw(self):
        result = _heuristic_classify("What is Python?")
        assert result is not None
        assert result.recommendation == "raw"

    def test_short_greeting_returns_raw(self):
        result = _heuristic_classify("Hello!")
        assert result is not None
        assert result.recommendation == "raw"

    def test_simple_factual_opener_returns_raw(self):
        result = _heuristic_classify("What is the capital of France?")
        assert result is not None
        assert result.recommendation == "raw"

    def test_who_is_returns_raw(self):
        result = _heuristic_classify("Who is Alan Turing?")
        assert result is not None
        assert result.recommendation == "raw"

    def test_define_returns_raw(self):
        result = _heuristic_classify("Define machine learning.")
        assert result is not None
        assert result.recommendation == "raw"

    def test_empty_string_returns_none(self):
        result = _heuristic_classify("")
        assert result is None

    def test_whitespace_only_returns_none(self):
        result = _heuristic_classify("   ")
        assert result is None

    def test_complex_signals_override_short_length(self):
        """Even a short question with strategy/risk signals should go to LLM."""
        result = _heuristic_classify("Analyze strategic risks.")
        # Should be None (uncertain → LLM) because of "strategic" and "risk"
        assert result is None

    def test_multi_domain_complex_question_returns_none(self):
        result = _heuristic_classify(
            "What strategic roadmap should we prioritize to reduce churn "
            "while managing regulatory risk in three markets?"
        )
        assert result is None

    def test_root_cause_analysis_returns_none(self):
        result = _heuristic_classify("What is the root cause of our performance degradation?")
        assert result is None

    def test_ethical_question_returns_none(self):
        result = _heuristic_classify("What are the ethical implications of this policy?")
        assert result is None

    def test_simple_factual_with_complex_signal_returns_none(self):
        """'What is' opener but with complexity signal → LLM decision."""
        result = _heuristic_classify(
            "What is the best framework for analyzing multi-stakeholder risk?"
        )
        assert result is None

    def test_short_technical_deep_question_returns_none(self):
        """Short but genuinely ambiguous technical question."""
        result = _heuristic_classify("Evaluate the trade-offs.")
        # "trade-offs" triggers _COMPLEX_SIGNALS
        assert result is None

    def test_heuristic_result_fields_complete(self):
        result = _heuristic_classify("2 + 2")
        assert result is not None
        assert isinstance(result, ComplexityResult)
        assert result.recommendation in ("raw", "single_template", "integrated")
        assert result.complexity in ("low", "medium", "high")
        assert isinstance(result.reasoning, str) and len(result.reasoning) > 0

    def test_result_is_raw_not_single_template(self):
        """Heuristic should only ever return 'raw' — template selection requires LLM."""
        for q in ["What is 2+2?", "Hello!", "Define entropy.", "Who is Einstein?"]:
            result = _heuristic_classify(q)
            if result is not None:
                assert result.recommendation == "raw", (
                    f"Heuristic classified '{q}' as '{result.recommendation}' "
                    "(only 'raw' is valid from the heuristic)"
                )


# ---------------------------------------------------------------------------
# assess_complexity integration — heuristic fast-path avoids LLM
# ---------------------------------------------------------------------------

class TestAssessComplexityHeuristicIntegration:

    def test_simple_question_skips_llm(self):
        """LLM should NOT be called for an obviously simple question."""
        with patch("litellm.completion") as mock_llm:
            result = assess_complexity("What is Python?", provider="openai")

        mock_llm.assert_not_called()
        assert result.recommendation == "raw"

    def test_arithmetic_skips_llm(self):
        """Arithmetic expression should be handled entirely by the heuristic."""
        with patch("litellm.completion") as mock_llm:
            result = assess_complexity("100 / 4", provider="openai")

        mock_llm.assert_not_called()
        assert result.recommendation == "raw"

    def test_skip_heuristic_true_calls_llm(self):
        """skip_heuristic=True must bypass the pre-screen and call the LLM."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            '{"complexity": "low", "domains": [], "reasoning_type": "explanatory", '
            '"recommendation": "raw", "best_template": "", "reasoning": "simple"}'
        )
        mock_response.usage = MagicMock(
            total_tokens=20, prompt_tokens=15, completion_tokens=5
        )

        with patch("litellm.completion", return_value=mock_response) as mock_llm:
            with patch("litellm.completion_cost", return_value=0.0):
                result = assess_complexity(
                    "What is Python?",
                    provider="openai",
                    model="gpt-4o-mini",
                    skip_heuristic=True,
                )

        mock_llm.assert_called_once()
        assert result.recommendation == "raw"

    def test_complex_question_still_calls_llm(self):
        """A genuinely complex question must reach the LLM even with heuristic enabled."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            '{"complexity": "high", "domains": ["business", "technical"], '
            '"reasoning_type": "strategic", "recommendation": "integrated", '
            '"best_template": "", "reasoning": "multi-domain"}'
        )
        mock_response.usage = MagicMock(
            total_tokens=50, prompt_tokens=35, completion_tokens=15
        )

        complex_q = (
            "What strategic roadmap should we prioritize to reduce customer churn "
            "while managing regulatory risk across three different global markets?"
        )
        with patch("litellm.completion", return_value=mock_response) as mock_llm:
            with patch("litellm.completion_cost", return_value=0.0):
                result = assess_complexity(complex_q, provider="openai", model="gpt-4o-mini")

        mock_llm.assert_called_once()
        assert result.recommendation == "integrated"

    def test_heuristic_result_type(self):
        """Heuristic-derived result should still be a valid ComplexityResult."""
        result = assess_complexity("Hello!", provider="openai")
        assert isinstance(result, ComplexityResult)
        assert result.recommendation == "raw"

    def test_assess_complexity_fallback_on_llm_error(self):
        """If the LLM fails on a complex question, the error fallback still works."""
        with patch("litellm.completion", side_effect=RuntimeError("LLM down")):
            result = assess_complexity(
                "Analyze multi-stakeholder strategic risk trade-offs.",
                provider="openai",
                model="gpt-4o-mini",
            )
        # Error fallback returns a default ComplexityResult — should not raise
        assert isinstance(result, ComplexityResult)
        assert result.recommendation in ("raw", "single_template", "integrated")
