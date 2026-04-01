"""
Tests for Pattern class and template system
"""

import pytest

from mycontext.foundation import Guidance
from mycontext.structure import Pattern
from mycontext.templates.free import QuestionAnalyzer, StepByStepReasoner

# Note: PerspectiveShifter, AssumptionChallenger, DecisionFramework
# will be added when those templates are implemented


class TestPatternBase:
    """Test base Pattern functionality"""

    def test_pattern_creation(self):
        """Test creating a simple pattern"""
        pattern = Pattern(
            name="test_pattern",
            description="A test pattern",
            guidance=Guidance(role="Test Expert"),
            directive_template="Process: {input}",
            input_schema={"input": str},
        )
        assert pattern.name == "test_pattern"
        assert pattern.guidance.role == "Test Expert"

    def test_pattern_validation(self):
        """Test pattern input validation"""
        pattern = Pattern(
            name="test_pattern",
            directive_template="Process: {required_input}",
            input_schema={"required_input": str},
        )

        # Should raise error for missing input
        with pytest.raises(ValueError):
            pattern.build_context()

    def test_pattern_build_context(self):
        """Test building context from pattern"""
        pattern = Pattern(
            name="test_pattern",
            guidance=Guidance(role="Expert"),
            directive_template="Analyze: {topic}",
            input_schema={"topic": str},
        )

        context = pattern.build_context(topic="AI")
        assert context.guidance.role == "Expert"
        assert "AI" in context.directive.content


class TestQuestionAnalyzer:
    """Test QuestionAnalyzer template"""

    def test_creation(self):
        """Test creating QuestionAnalyzer"""
        analyzer = QuestionAnalyzer()
        assert analyzer.name == "question_analyzer"
        assert analyzer.guidance is not None

    def test_build_context_simple(self):
        """Test building context with simple question"""
        analyzer = QuestionAnalyzer()
        context = analyzer.build_context(question="What is AI?", depth="brief")
        assert context.directive is not None
        assert "What is AI?" in context.directive.content

    def test_build_context_comprehensive(self):
        """Test building context with comprehensive depth"""
        analyzer = QuestionAnalyzer()
        context = analyzer.build_context(
            question="Should I invest in solar panels?", depth="comprehensive"
        )
        assert context.directive is not None
        assert "solar panels" in context.directive.content
        # Comprehensive depth should add more structure
        assert context.metadata.get("pattern") == "question_analyzer"

    def test_with_additional_context(self):
        """Test analyzer with additional context"""
        analyzer = QuestionAnalyzer()
        context = analyzer.build_context(
            question="What car should I buy?",
            context="Budget: $30,000, Family of 4",
            depth="moderate",
        )
        assert context.directive is not None
        # Context section should be included
        assert "Budget" in context.directive.content or "30,000" in context.directive.content


class TestStepByStepReasoner:
    """Test StepByStepReasoner template"""

    def test_creation(self):
        """Test creating StepByStepReasoner"""
        reasoner = StepByStepReasoner()
        assert reasoner.name == "step_by_step_reasoner"
        assert reasoner.guidance is not None

    def test_build_context(self):
        """Test building context for step-by-step reasoning"""
        reasoner = StepByStepReasoner()
        context = reasoner.build_context(
            problem="How to optimize database queries?", depth="detailed"
        )
        assert context.directive is not None
        assert "database queries" in context.directive.content


# TODO: Add tests for remaining templates when implemented
# class TestPerspectiveShifter:
# class TestAssumptionChallenger:
# class TestDecisionFramework:


class TestPatternParameterSeparation:
    """Test that Pattern correctly separates template vs provider parameters"""

    def test_provider_params_not_in_context(self):
        """Test that provider params don't leak into context data"""
        analyzer = QuestionAnalyzer()

        context = analyzer.build_context(question="Test question", depth="brief")

        # Template inputs are stored in context.data (by design)
        assert "question" in context.data
        assert "depth" in context.data
        # Provider-level params should never appear
        assert "model" not in context.data
        assert "api_key" not in context.data

    def test_metadata_is_set(self):
        """Test that pattern metadata is set correctly"""
        analyzer = QuestionAnalyzer()
        context = analyzer.build_context(question="Test", depth="brief")

        assert context.metadata.get("pattern") == "question_analyzer"
        assert "pattern_version" in context.metadata


class TestTemplateIntegration:
    """Test templates working together"""

    def test_chain_templates(self):
        """Test using output of one template as input to another"""
        # First analyze a question
        analyzer = QuestionAnalyzer()
        analysis_context = analyzer.build_context(
            question="Should I start a business?", depth="comprehensive"
        )

        # Then reason through it step by step
        reasoner = StepByStepReasoner()
        reasoning_context = reasoner.build_context(
            problem="Starting a business successfully", depth="detailed"
        )

        # Both should produce valid contexts
        assert analysis_context.directive is not None
        assert reasoning_context.directive is not None

    def test_export_from_template(self):
        """Test that template-created contexts can be exported"""
        reasoner = StepByStepReasoner()
        context = reasoner.build_context(problem="How to learn Python?", depth="detailed")

        # Should be able to export in all formats
        messages = context.to_messages()
        assert len(messages) >= 1

        markdown = context.to_markdown()
        assert "# Context" in markdown

        lc_format = context.to_langchain()
        assert "system_message" in lc_format

        json_str = context.to_json()
        assert isinstance(json_str, str)
