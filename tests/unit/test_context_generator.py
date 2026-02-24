"""
Unit tests for generate_context — context_generator.py

All tests are offline (no LLM calls). The LLM call is mocked.
"""

import json as _json
from unittest.mock import MagicMock, patch

import pytest

from mycontext import Context, GeneratedContext, generate_context
from mycontext.intelligence.context_generator import (
    _parse_llm_json,
    _spec_to_context,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

VALID_SPEC = {
    "rules": [
        "Every risk must include a probability score (Low/Medium/High)",
        "Always reference the specific transaction ID in findings",
        "Never flag a transaction as fraud without at least two corroborating signals",
    ],
    "style": "Analytical, precise, evidence-first",
    "expertise": ["fraud detection", "AML", "transaction monitoring", "risk scoring"],
    "thinking_strategy": "step_by_step",
    "examples": [
        {
            "input": "Transaction: $12,000 wire to unknown account at 2am",
            "output": "High risk — unusual time, large amount, unknown counterparty. Score: 0.91",
        },
        {
            "input": "Transaction: $50 grocery store purchase",
            "output": "Low risk — routine amount, known merchant category. Score: 0.04",
        },
    ],
    "output_schema": [
        {"name": "risk_level", "type": "str"},
        {"name": "score", "type": "float"},
        {"name": "reasoning", "type": "str"},
        {"name": "recommended_action", "type": "str"},
    ],
    "must_include": ["risk_level", "score", "reasoning"],
    "must_not_include": ["speculative conclusions without transaction evidence"],
}


def _make_mock_provider(response_text: str) -> MagicMock:
    mock_result = MagicMock()
    mock_result.response = response_text
    mock_provider = MagicMock()
    mock_provider.generate.return_value = mock_result
    return mock_provider


# ── _parse_llm_json ───────────────────────────────────────────────────────────

class TestParseLlmJson:
    def test_bare_json(self):
        text = '{"rules": ["rule one"], "style": "professional"}'
        result = _parse_llm_json(text)
        assert result["rules"] == ["rule one"]

    def test_json_with_markdown_fence(self):
        text = '```json\n{"rules": ["rule one"]}\n```'
        result = _parse_llm_json(text)
        assert result["rules"] == ["rule one"]

    def test_json_with_prose_around_it(self):
        text = 'Here is the spec:\n{"rules": ["rule one"]}\nEnd.'
        result = _parse_llm_json(text)
        assert result["rules"] == ["rule one"]

    def test_raises_on_invalid(self):
        with pytest.raises(ValueError, match="Could not extract valid JSON"):
            _parse_llm_json("This is not JSON at all.")

    def test_json_fence_no_language_tag(self):
        text = "```\n{\"style\": \"direct\"}\n```"
        result = _parse_llm_json(text)
        assert result["style"] == "direct"


# ── _spec_to_context ──────────────────────────────────────────────────────────

class TestSpecToContext:
    def test_produces_context_with_research_flow(self):
        ctx = _spec_to_context(
            role="Fraud analyst",
            goal="Detect fraud",
            task="Analyze this transaction",
            spec=VALID_SPEC,
        )
        assert isinstance(ctx, Context)
        assert ctx.research_flow is True

    def test_guidance_fields_populated(self):
        ctx = _spec_to_context(
            role="Fraud analyst",
            goal="Detect fraud",
            task=None,
            spec=VALID_SPEC,
        )
        assert ctx.guidance.role == "Fraud analyst"
        assert ctx.guidance.goal == "Detect fraud"
        assert len(ctx.guidance.rules) == 3
        assert ctx.guidance.style == "Analytical, precise, evidence-first"
        assert "fraud detection" in ctx.guidance.expertise

    def test_directive_set_from_task(self):
        ctx = _spec_to_context(
            role="Analyst",
            goal="Detect fraud",
            task="Analyze this batch",
            spec=VALID_SPEC,
        )
        assert ctx.directive is not None
        assert ctx.directive.content == "Analyze this batch"

    def test_no_directive_when_task_is_none(self):
        ctx = _spec_to_context(
            role="Analyst",
            goal="Detect fraud",
            task=None,
            spec=VALID_SPEC,
        )
        assert ctx.directive is None

    def test_thinking_strategy_valid(self):
        ctx = _spec_to_context("r", "g", None, {**VALID_SPEC, "thinking_strategy": "verify"})
        assert ctx.thinking_strategy == "verify"

    def test_thinking_strategy_invalid_becomes_none(self):
        ctx = _spec_to_context("r", "g", None, {**VALID_SPEC, "thinking_strategy": "made_up_strategy"})
        assert ctx.thinking_strategy is None

    def test_examples_populated(self):
        ctx = _spec_to_context("r", "g", None, VALID_SPEC)
        assert ctx.examples is not None
        assert len(ctx.examples) == 2
        assert ctx.examples[0]["input"].startswith("Transaction:")

    def test_constraints_populated(self):
        ctx = _spec_to_context("r", "g", None, VALID_SPEC)
        assert ctx.constraints is not None
        assert ctx.constraints.must_include == ["risk_level", "score", "reasoning"]
        assert len(ctx.constraints.output_schema) == 4

    def test_empty_spec_produces_minimal_context(self):
        ctx = _spec_to_context("Analyst", "Detect stuff", None, {})
        assert ctx.research_flow is True
        assert ctx.guidance.role == "Analyst"
        assert ctx.guidance.rules == []
        assert ctx.constraints is None
        assert ctx.examples is None

    def test_malformed_examples_skipped(self):
        spec = {**VALID_SPEC, "examples": [{"input": "x"}, {"output": "y"}, {"input": "a", "output": "b"}]}
        ctx = _spec_to_context("r", "g", None, spec)
        # Only the complete example {"input": "a", "output": "b"} should survive
        assert ctx.examples == [{"input": "a", "output": "b"}]

    def test_assemble_runs_without_error(self):
        ctx = _spec_to_context("Fraud analyst", "Detect fraud", "Analyze batch", VALID_SPEC)
        assembled = ctx.assemble()
        assert "## ROLE" in assembled
        assert "## GOAL" in assembled
        assert "## YOUR TASK" in assembled
        assert "Analyze batch" in assembled


# ── generate_context (mocked LLM) ────────────────────────────────────────────


class TestGenerateContext:
    def _mock_generate(self, spec: dict) -> MagicMock:
        mock_provider = _make_mock_provider(_json.dumps(spec))
        return mock_provider

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_returns_generated_context(self, mock_get_provider):
        mock_get_provider.return_value = self._mock_generate(VALID_SPEC)
        result = generate_context(
            role="Fraud analyst",
            goal="Detect fraud",
            task="Analyze this batch",
        )
        assert isinstance(result, GeneratedContext)
        assert isinstance(result.context, Context)

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_context_has_research_flow(self, mock_get_provider):
        mock_get_provider.return_value = self._mock_generate(VALID_SPEC)
        result = generate_context(role="Analyst", goal="Find risks")
        assert result.context.research_flow is True

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_generation_meta_is_raw_spec(self, mock_get_provider):
        mock_get_provider.return_value = self._mock_generate(VALID_SPEC)
        result = generate_context(role="Analyst", goal="Find risks")
        assert result.generation_meta == VALID_SPEC

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_assemble_passthrough(self, mock_get_provider):
        mock_get_provider.return_value = self._mock_generate(VALID_SPEC)
        result = generate_context(role="Analyst", goal="Detect fraud", task="Analyze batch")
        assembled = result.assemble()
        assert isinstance(assembled, str)
        assert len(assembled) > 100

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_to_context_returns_context(self, mock_get_provider):
        mock_get_provider.return_value = self._mock_generate(VALID_SPEC)
        result = generate_context(role="Analyst", goal="Find risks")
        ctx = result.to_context()
        assert isinstance(ctx, Context)

    def test_raises_on_empty_role(self):
        with pytest.raises(ValueError, match="role must be a non-empty string"):
            generate_context(role="", goal="Detect fraud")

    def test_raises_on_empty_goal(self):
        with pytest.raises(ValueError, match="goal must be a non-empty string"):
            generate_context(role="Analyst", goal="")

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_raises_on_unparseable_llm_response(self, mock_get_provider):
        mock_provider = _make_mock_provider("I cannot help with that request.")
        mock_get_provider.return_value = mock_provider
        with pytest.raises(ValueError, match="Could not parse LLM response"):
            generate_context(role="Analyst", goal="Detect fraud")

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_llm_failure_raises_runtime_error(self, mock_get_provider):
        mock_provider = MagicMock()
        mock_provider.generate.side_effect = Exception("API timeout")
        mock_get_provider.return_value = mock_provider
        with pytest.raises(RuntimeError, match="LLM call failed"):
            generate_context(role="Analyst", goal="Detect fraud")

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_fenced_json_response_parsed_correctly(self, mock_get_provider):
        fenced = f"```json\n{_json.dumps(VALID_SPEC)}\n```"
        mock_get_provider.return_value = _make_mock_provider(fenced)
        result = generate_context(role="Analyst", goal="Find risks")
        assert result.generation_meta == VALID_SPEC

    @patch("mycontext.intelligence.context_generator.get_provider")
    def test_top_level_import(self, mock_get_provider):
        """generate_context is importable from the top-level mycontext package."""
        mock_get_provider.return_value = self._mock_generate(VALID_SPEC)
        import mycontext
        result = mycontext.generate_context(role="Analyst", goal="Detect fraud")
        assert isinstance(result, GeneratedContext)
