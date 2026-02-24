"""
Tests for Phase 5 — Pydantic schemas for intelligence parsing.

Covers:
  ── schemas.py ──
  1. PatternSuggestionResponse validates correct selections
  2. PatternSuggestionResponse normalises name formats
  3. PatternSuggestionResponse allows unknown names (passes through with warning)
  4. IntegrationResponse validates with all fields
  5. IntegrationResponse works with minimal/empty fields
  6. ContextSpec validates full spec
  7. ContextSpec normalises invalid thinking_strategy to step_by_step
  8. ContextSpec.to_dict() roundtrips correctly
  9. parse_with_fallback succeeds on valid JSON
  10. parse_with_fallback raises ValueError on malformed JSON
  11. _extract_json_block strips markdown fences

  ── pattern_suggester integration ──
  12. _suggest_with_llm uses Pydantic parse when LLM returns JSON
  13. _suggest_with_llm falls back to regex when JSON parse fails
  14. _suggest_with_llm returns empty list on complete LLM failure

  ── template_integrator_agent integration ──
  15. _parse_result uses Pydantic path when raw is valid JSON
  16. _parse_result falls back to regex on non-JSON raw

  ── context_generator integration ──
  17. _parse_llm_json returns validated dict from JSON string
  18. _parse_llm_json falls back to legacy parser on schema failure
  19. _parse_llm_json raises ValueError on completely unparseable input
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from mycontext.intelligence.schemas import (
    ContextSpec,
    IntegrationResponse,
    PatternSelection,
    PatternSuggestionResponse,
    _extract_json_block,
    parse_with_fallback,
)

# ---------------------------------------------------------------------------
# Schema unit tests
# ---------------------------------------------------------------------------

class TestPatternSuggestionResponse:

    def test_valid_selections(self):
        data = {
            "selections": [
                {"name": "root_cause_analyzer", "reason": "Good for finding root causes."},
                {"name": "risk_assessor", "reason": "Assesses risks."},
            ],
            "integration": "Use first then second.",
        }
        resp = PatternSuggestionResponse.model_validate(data)
        assert len(resp.selections) >= 1
        assert resp.integration == "Use first then second."

    def test_name_normalisation(self):
        sel = PatternSelection.model_validate({"name": "Root-Cause-Analyzer", "reason": "test"})
        assert sel.name == "root_cause_analyzer"

    def test_name_with_spaces_normalised(self):
        sel = PatternSelection.model_validate({"name": "risk assessor", "reason": "test"})
        assert sel.name == "risk_assessor"

    def test_unknown_names_pass_through_with_warning(self, caplog):
        import logging
        data = {
            "selections": [{"name": "totally_fake_xyz", "reason": "reason"}],
            "integration": "",
        }
        with caplog.at_level(logging.WARNING, logger="mycontext.intelligence.schemas"):
            resp = PatternSuggestionResponse.model_validate(data)
        # Unknown names are kept (validator logs warning but doesn't drop them)
        assert len(resp.selections) == 1

    def test_min_length_enforced(self):
        with pytest.raises(Exception):
            PatternSuggestionResponse.model_validate({"selections": [], "integration": ""})

    def test_max_length_enforced(self):
        selections = [{"name": f"pattern_{i}", "reason": "r"} for i in range(6)]
        with pytest.raises(Exception):
            PatternSuggestionResponse.model_validate({"selections": selections, "integration": ""})


class TestIntegrationResponse:

    def test_full_fields(self):
        data = {
            "role": "Senior analyst",
            "rules": ["Rule one", "Rule two"],
            "directive": "Analyze the following data...",
            "output_requirements": ["Summary", "Risks"],
            "integration_rationale": "Combines templates A and B.",
        }
        resp = IntegrationResponse.model_validate(data)
        assert resp.role == "Senior analyst"
        assert len(resp.rules) == 2
        assert resp.directive == "Analyze the following data..."

    def test_minimal_fields_use_defaults(self):
        resp = IntegrationResponse.model_validate({})
        assert resp.role == ""
        assert resp.rules == []
        assert resp.directive == ""


class TestContextSpec:

    def _full_data(self):
        return {
            "rules": ["Be precise", "Always cite sources"],
            "style": "Professional and concise",
            "expertise": ["Machine learning", "Data analysis"],
            "thinking_strategy": "step_by_step",
            "examples": [{"input": "Q1", "output": "A1"}],
            "output_schema": [{"name": "summary", "type": "str"}],
            "must_include": ["confidence score"],
            "must_not_include": ["opinions"],
        }

    def test_full_spec_validates(self):
        spec = ContextSpec.model_validate(self._full_data())
        assert spec.thinking_strategy == "step_by_step"
        assert len(spec.rules) == 2

    def test_invalid_strategy_normalised(self):
        data = self._full_data()
        data["thinking_strategy"] = "made_up_strategy"
        spec = ContextSpec.model_validate(data)
        assert spec.thinking_strategy == "step_by_step"

    def test_all_valid_strategies_accepted(self):
        for strategy in ("step_by_step", "multiple_angles", "verify", "explain_simply", "creative"):
            data = self._full_data()
            data["thinking_strategy"] = strategy
            spec = ContextSpec.model_validate(data)
            assert spec.thinking_strategy == strategy

    def test_to_dict_roundtrip(self):
        data = self._full_data()
        spec = ContextSpec.model_validate(data)
        d = spec.to_dict()
        assert d["rules"] == data["rules"]
        assert d["style"] == data["style"]
        assert d["thinking_strategy"] == data["thinking_strategy"]
        assert d["examples"] == data["examples"]
        assert d["output_schema"] == data["output_schema"]

    def test_empty_spec_uses_defaults(self):
        spec = ContextSpec.model_validate({})
        assert spec.rules == []
        assert spec.thinking_strategy == "step_by_step"


# ---------------------------------------------------------------------------
# parse_with_fallback
# ---------------------------------------------------------------------------

class TestParseWithFallback:

    def test_valid_json_succeeds(self):
        raw = json.dumps({
            "selections": [{"name": "root_cause_analyzer", "reason": "good"}],
            "integration": "works together",
        })
        result = parse_with_fallback(PatternSuggestionResponse, raw)
        assert len(result.selections) == 1

    def test_json_in_markdown_fence_succeeds(self):
        raw = '```json\n{"selections":[{"name":"risk_assessor","reason":"r"}],"integration":""}\n```'
        result = parse_with_fallback(PatternSuggestionResponse, raw)
        assert len(result.selections) == 1

    def test_malformed_json_raises_value_error(self):
        with pytest.raises(ValueError, match="Could not parse LLM response"):
            parse_with_fallback(PatternSuggestionResponse, "not json at all {{{{")


class TestExtractJsonBlock:

    def test_bare_json(self):
        raw = '{"key": "value"}'
        assert _extract_json_block(raw) == raw

    def test_strips_markdown_fence(self):
        raw = '```json\n{"key": "value"}\n```'
        result = _extract_json_block(raw)
        assert result == '{"key": "value"}'

    def test_extracts_outermost_braces(self):
        raw = 'Some text before {"key": "value"} some text after'
        result = _extract_json_block(raw)
        assert '{"key": "value"}' in result


# ---------------------------------------------------------------------------
# pattern_suggester integration
# ---------------------------------------------------------------------------

class TestSuggestWithLLMPydantic:

    def _make_json_response(self):
        return json.dumps({
            "selections": [
                {"name": "root_cause_analyzer", "reason": "finds root causes"},
                {"name": "risk_assessor", "reason": "assesses risk"},
            ],
            "integration": "Use in sequence.",
        })

    def test_pydantic_parse_used_when_llm_returns_json(self):
        """When the LLM returns valid JSON, Pydantic parsing should succeed."""
        from mycontext.intelligence.pattern_suggester import _suggest_with_llm

        mock_resp = MagicMock()
        mock_resp.response = self._make_json_response()

        with patch("mycontext.intelligence.schemas._INSTRUCTOR_AVAILABLE", False):
            with patch("mycontext.core.Context.execute", return_value=mock_resp):
                selections, integration, _ = _suggest_with_llm(
                    "What caused the outage?", provider="openai", model="gpt-4o-mini"
                )

        assert len(selections) >= 1
        assert selections[0][0] in ("root_cause_analyzer", "risk_assessor")

    def test_regex_fallback_used_when_json_parse_fails(self):
        """When the LLM returns TEMPLATE/REASON format, regex fallback is used."""
        from mycontext.intelligence.pattern_suggester import _suggest_with_llm

        mock_resp = MagicMock()
        mock_resp.response = (
            "TEMPLATE: root_cause_analyzer\n"
            "REASON: Identifies the root cause.\n"
            "INTEGRATION: Use for systematic analysis."
        )

        with patch("mycontext.intelligence.schemas._INSTRUCTOR_AVAILABLE", False):
            with patch("mycontext.core.Context.execute", return_value=mock_resp):
                selections, integration, _ = _suggest_with_llm(
                    "Why did sales drop?", provider="openai", model="gpt-4o-mini"
                )

        assert len(selections) >= 1
        assert selections[0][0] == "root_cause_analyzer"

    def test_returns_empty_on_llm_failure(self):
        from mycontext.intelligence.pattern_suggester import _suggest_with_llm

        with patch("mycontext.intelligence.schemas._INSTRUCTOR_AVAILABLE", False):
            with patch("mycontext.core.Context.execute", side_effect=RuntimeError("LLM down")):
                selections, integration, _ = _suggest_with_llm(
                    "Any question", provider="openai", model="gpt-4o-mini"
                )

        assert selections == []


# ---------------------------------------------------------------------------
# template_integrator_agent integration
# ---------------------------------------------------------------------------

class TestTemplateIntegratorParsing:

    def _make_agent(self):
        from mycontext.intelligence.template_integrator_agent import TemplateIntegratorAgent
        agent = TemplateIntegratorAgent.__new__(TemplateIntegratorAgent)
        agent.include_enterprise = True
        agent._last_structured = None
        return agent

    def test_pydantic_path_when_raw_is_json(self):
        agent = self._make_agent()
        raw = json.dumps({
            "role": "Senior analyst",
            "rules": ["Be precise"],
            "directive": "Analyze thoroughly and provide actionable insights.",
            "output_requirements": ["Summary"],
            "integration_rationale": "Works well together.",
        })
        result = agent._parse_result("test question", ["root_cause_analyzer"], raw)
        assert result.role == "Senior analyst"
        assert result.rules == ["Be precise"]

    def test_regex_fallback_when_raw_is_not_json(self):
        agent = self._make_agent()
        raw = (
            "ROLE: Senior analyst\n"
            "RULES:\n- Be precise\n- Be thorough\n"
            "DIRECTIVE:\nAnalyze the situation in detail.\n"
            "OUTPUT MUST INCLUDE:\n- Summary\n- Recommendations\n"
        )
        result = agent._parse_result("test question", ["root_cause_analyzer"], raw)
        assert result.role == "Senior analyst"
        assert len(result.rules) >= 1


# ---------------------------------------------------------------------------
# context_generator integration
# ---------------------------------------------------------------------------

class TestContextGeneratorParsing:

    def test_pydantic_path_on_valid_json(self):
        from mycontext.intelligence.context_generator import _parse_llm_json

        raw = json.dumps({
            "rules": ["Rule A", "Rule B"],
            "style": "Professional",
            "expertise": ["Finance"],
            "thinking_strategy": "step_by_step",
            "examples": [{"input": "Q", "output": "A"}],
            "output_schema": [{"name": "result", "type": "str"}],
            "must_include": ["confidence"],
            "must_not_include": ["opinions"],
        })
        result = _parse_llm_json(raw)
        assert result["rules"] == ["Rule A", "Rule B"]
        assert result["thinking_strategy"] == "step_by_step"

    def test_normalises_invalid_strategy(self):
        from mycontext.intelligence.context_generator import _parse_llm_json

        raw = json.dumps({
            "rules": [],
            "style": "",
            "expertise": [],
            "thinking_strategy": "invalid_one",
            "examples": [],
            "output_schema": [],
            "must_include": [],
            "must_not_include": [],
        })
        result = _parse_llm_json(raw)
        assert result["thinking_strategy"] == "step_by_step"

    def test_legacy_fallback_on_partial_json(self):
        from mycontext.intelligence.context_generator import _parse_llm_json

        # Extra fields that don't match ContextSpec — should fall back to raw parse
        raw = '{"custom_field": "some_value", "rules": ["Rule 1"]}'
        result = _parse_llm_json(raw)
        # Legacy path returns the raw dict as-is
        assert isinstance(result, dict)

    def test_raises_on_completely_unparseable(self):
        from mycontext.intelligence.context_generator import _parse_llm_json

        with pytest.raises(ValueError, match="Could not extract valid JSON"):
            _parse_llm_json("This is not JSON at all, completely unstructured text.")

    def test_handles_markdown_fence(self):
        from mycontext.intelligence.context_generator import _parse_llm_json

        raw = '```json\n{"rules":["R1"],"style":"","expertise":[],"thinking_strategy":"verify","examples":[],"output_schema":[],"must_include":[],"must_not_include":[]}\n```'
        result = _parse_llm_json(raw)
        assert result["thinking_strategy"] == "verify"
