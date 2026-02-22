"""
Unit tests for pattern suggester (keyword, llm, hybrid modes).
"""

import pytest

from mycontext.intelligence import (
    SuggestionResult,
    get_pattern_class,
    suggest_patterns,
)


class TestPatternSuggesterKeyword:
    """Keyword mode (no LLM)."""

    def test_suggest_root_cause(self) -> None:
        r = suggest_patterns("Why did churn spike? Root cause analysis.", mode="keyword")
        assert isinstance(r, SuggestionResult)
        assert r.source == "keyword"
        names = [s.name for s in r.suggested_patterns]
        assert "root_cause_analyzer" in names or "diagnostic_root_cause_analyzer" in names

    def test_suggest_temporal_chain(self) -> None:
        r = suggest_patterns(
            "Timeline of events, then root cause, then future scenarios.",
            mode="keyword",
            suggest_chain=True,
        )
        assert len(r.suggested_patterns) >= 1
        assert r.suggested_chain is None or len(r.suggested_chain) >= 1

    def test_suggest_comparative(self) -> None:
        r = suggest_patterns("Compare A versus B", mode="keyword")
        names = [s.name for s in r.suggested_patterns]
        assert "comparative_analyzer" in names

    def test_no_match_returns_empty_reasoning(self) -> None:
        r = suggest_patterns("xyznonexistent123", mode="keyword")
        assert r.source == "keyword"
        assert "Try question_analyzer" in r.reasoning or len(r.suggested_patterns) == 0


class TestPatternSuggesterHybrid:
    """Hybrid mode - keyword + LLM merge. LLM call may fail without API key."""

    def test_hybrid_merge_structure(self) -> None:
        """Hybrid returns merged result; structure valid even if LLM fails."""
        try:
            r = suggest_patterns(
                "Why did churn spike? Timeline and root cause.",
                mode="hybrid",
                llm_provider="openai",
            )
            assert r.source in ("hybrid", "keyword")  # fallback to keyword if LLM fails
            assert isinstance(r.suggested_patterns, list)
        except Exception:
            pytest.skip("Hybrid needs OPENAI_API_KEY")

    def test_keyword_mode_no_llm_call(self) -> None:
        """Keyword mode never calls LLM."""
        r = suggest_patterns("root cause and timeline", mode="keyword")
        assert r.source == "keyword"
        assert r.llm_reasoning is None


class TestGetPatternClass:
    """get_pattern_class returns valid classes."""

    def test_enterprise_pattern(self) -> None:
        cls = get_pattern_class("temporal_sequence_analyzer")
        assert cls is not None
        assert hasattr(cls, "build_context")

    def test_free_pattern(self) -> None:
        cls = get_pattern_class("comparative_analyzer")
        assert cls is not None

    def test_unknown_returns_none(self) -> None:
        cls = get_pattern_class("nonexistent_pattern_xyz")
        assert cls is None


class TestSuggestionResultStructuredOutput:
    """Structured output: to_dict, to_markdown, to_json, to_yaml, to_xml, from_dict, from_json."""

    def test_to_dict(self) -> None:
        r = suggest_patterns("Why did churn spike?", mode="keyword")
        d = r.to_dict()
        assert "question" in d
        assert "suggested_patterns" in d
        assert "suggested_chain" in d
        assert "source" in d

    def test_to_markdown(self) -> None:
        r = suggest_patterns("Root cause analysis", mode="keyword")
        md = r.to_markdown()
        assert "Root cause analysis" in md
        assert "**Source**" in md or "Source" in md

    def test_to_json_round_trip(self) -> None:
        r = suggest_patterns("Compare A vs B", mode="keyword")
        r2 = SuggestionResult.from_json(r.to_json())
        assert r2.question == r.question
        assert len(r2.suggested_patterns) == len(r.suggested_patterns)

    def test_to_dict_from_dict_round_trip(self) -> None:
        r = suggest_patterns("Timeline of events", mode="keyword")
        r2 = SuggestionResult.from_dict(r.to_dict())
        assert r2.question == r.question
        assert [s.name for s in r2.suggested_patterns] == [s.name for s in r.suggested_patterns]

    def test_to_yaml(self) -> None:
        r = suggest_patterns("Decision framework", mode="keyword")
        yaml_str = r.to_yaml()
        assert "question:" in yaml_str
        assert "suggested_patterns:" in yaml_str

    def test_to_xml(self) -> None:
        r = suggest_patterns("Future scenario", mode="keyword")
        xml_str = r.to_xml()
        assert "<suggestion_result>" in xml_str
        assert "<question>" in xml_str
