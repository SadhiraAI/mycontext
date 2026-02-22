"""
Unit tests for Structure layer (Pattern and Blueprint)
"""

import pytest

from mycontext.foundation import Guidance
from mycontext.structure import Blueprint, Pattern


class TestPattern:
    """Tests for Pattern class"""

    def test_create_simple_pattern(self):
        """Test creating a simple pattern"""
        pattern = Pattern(
            name="test_pattern",
            description="A test pattern"
        )
        assert pattern.name == "test_pattern"
        assert pattern.version == "1.0.0"

    def test_pattern_with_guidance(self):
        """Test pattern with guidance"""
        guidance = Guidance(role="Expert")
        pattern = Pattern(
            name="expert_pattern",
            guidance=guidance
        )
        assert pattern.guidance.role == "Expert"

    def test_pattern_with_schema(self):
        """Test pattern with input/output schema"""
        pattern = Pattern(
            name="code_review",
            input_schema={"code": str, "language": str},
            output_schema={"issues": list, "score": float}
        )
        assert "code" in pattern.input_schema
        assert "issues" in pattern.output_schema

    def test_pattern_build_context(self):
        """Test building context from pattern"""
        pattern = Pattern(
            name="simple",
            guidance=Guidance(role="Assistant"),
            directive_template="Process: {input_text}",
            input_schema={"input_text": str}
        )
        context = pattern.build_context(input_text="Hello")
        assert context is not None
        assert context.guidance.role == "Assistant"
        assert "Hello" in context.directive.content

    def test_pattern_validate_inputs(self):
        """Test input validation"""
        pattern = Pattern(
            name="validator",
            input_schema={"required_field": str}
        )
        with pytest.raises(ValueError):
            pattern.build_context()  # Missing required field

    def test_pattern_to_dict(self):
        """Test converting pattern to dict"""
        pattern = Pattern(name="test", description="Test pattern")
        data = pattern.to_dict()
        assert data["name"] == "test"
        assert data["description"] == "Test pattern"


class TestBlueprint:
    """Tests for Blueprint class"""

    def test_create_simple_blueprint(self):
        """Test creating a simple blueprint"""
        blueprint = Blueprint(
            name="simple_assistant",
            description="Basic assistant"
        )
        assert blueprint.name == "simple_assistant"
        assert blueprint.token_budget == 4000  # default

    def test_blueprint_with_guidance(self):
        """Test blueprint with guidance"""
        guidance = Guidance(role="Expert assistant")
        blueprint = Blueprint(
            name="expert_bp",
            guidance=guidance
        )
        assert blueprint.guidance.role == "Expert assistant"

    def test_blueprint_with_token_budget(self):
        """Test blueprint with custom token budget"""
        blueprint = Blueprint(
            name="large_context",
            token_budget=8000
        )
        assert blueprint.token_budget == 8000

    def test_blueprint_build(self):
        """Test building context from blueprint"""
        blueprint = Blueprint(
            name="simple",
            guidance=Guidance(role="Assistant"),
            directive_template="Query: {query}",
            token_budget=2000
        )
        context = blueprint.build(query="Hello")
        assert context is not None
        assert context.guidance.role == "Assistant"
        assert "Hello" in context.directive.content

    def test_blueprint_estimate_tokens(self):
        """Test token estimation"""
        blueprint = Blueprint(
            name="test",
            guidance=Guidance(role="A" * 100)  # Long role
        )
        estimated = blueprint.estimate_tokens()
        assert estimated > 0

    def test_blueprint_optimize(self):
        """Test blueprint optimization"""
        blueprint = Blueprint(name="test")
        optimized = blueprint.optimize(strategy="speed")
        assert optimized.optimization == "speed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
