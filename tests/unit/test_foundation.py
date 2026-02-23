"""
Tests for Foundation classes (Directive, Guidance, Constraints)
"""
import pytest

from mycontext.foundation import Constraints, Directive, Guidance


class TestDirective:
    """Test Directive class"""

    def test_simple_directive(self):
        """Test creating a simple directive"""
        directive = Directive(content="Analyze this code")
        assert directive.content == "Analyze this code"
        assert directive.priority == 5  # default

    def test_with_priority(self):
        """Test directive with custom priority"""
        directive = Directive(content="Critical task", priority=10)
        assert directive.priority == 10

    def test_priority_validation(self):
        """Test that priority is validated (1-10)"""
        # Should work
        Directive(content="Test", priority=1)
        Directive(content="Test", priority=10)

        # Should fail
        with pytest.raises(Exception):  # Pydantic validation error
            Directive(content="Test", priority=0)

        with pytest.raises(Exception):
            Directive(content="Test", priority=11)

    def test_render(self):
        """Test rendering directive"""
        directive = Directive(content="Do this task")
        rendered = directive.render()
        assert rendered == "Do this task"


class TestGuidance:
    """Test Guidance class"""

    def test_simple_guidance(self):
        """Test creating simple guidance"""
        guidance = Guidance(role="Expert Analyst")
        assert guidance.role == "Expert Analyst"
        assert guidance.rules == []  # default
        assert guidance.style is None  # default

    def test_with_rules(self):
        """Test guidance with rules"""
        guidance = Guidance(
            role="Code Reviewer",
            rules=["Be thorough", "Focus on security", "Suggest improvements"]
        )
        assert len(guidance.rules) == 3
        assert "Be thorough" in guidance.rules

    def test_with_style(self):
        """Test guidance with communication style"""
        guidance = Guidance(
            role="Teacher",
            style="patient, encouraging, uses examples"
        )
        assert guidance.style == "patient, encouraging, uses examples"

    def test_render_simple(self):
        """Test rendering simple guidance"""
        guidance = Guidance(role="Expert")
        rendered = guidance.render()
        assert "You are Expert" in rendered

    def test_render_with_rules(self):
        """Test rendering guidance with rules"""
        guidance = Guidance(
            role="Analyst",
            rules=["Be clear", "Use data"]
        )
        rendered = guidance.render()
        assert "You are Analyst" in rendered
        assert "Follow these rules:" in rendered
        assert "Be clear" in rendered
        assert "Use data" in rendered

    def test_render_with_style(self):
        """Test rendering guidance with style"""
        guidance = Guidance(
            role="Assistant",
            style="friendly and helpful"
        )
        rendered = guidance.render()
        assert "Communication style: friendly and helpful" in rendered

    def test_render_complete(self):
        """Test rendering guidance with all fields"""
        guidance = Guidance(
            role="Expert",
            rules=["Rule 1", "Rule 2"],
            style="professional"
        )
        rendered = guidance.render()
        assert "You are Expert" in rendered
        assert "Rule 1" in rendered
        assert "Rule 2" in rendered
        assert "professional" in rendered


class TestConstraints:
    """Test Constraints class"""

    def test_empty_constraints(self):
        """Test creating empty constraints"""
        constraints = Constraints()
        assert not constraints.must_include
        assert not constraints.must_not_include
        assert not constraints.format_rules

    def test_must_include(self):
        """Test must_include constraints"""
        constraints = Constraints(
            must_include=["key metrics", "trends", "recommendations"]
        )
        assert len(constraints.must_include) == 3
        assert "key metrics" in constraints.must_include

    def test_must_not_include(self):
        """Test must_not_include constraints"""
        constraints = Constraints(
            must_not_include=["speculation", "personal opinions"]
        )
        assert len(constraints.must_not_include) == 2
        assert "speculation" in constraints.must_not_include

    def test_format_rules(self):
        """Test format_rules constraints"""
        constraints = Constraints(
            format_rules=[
                "Use bullet points",
                "Maximum 500 words",
                "Include citations"
            ]
        )
        assert len(constraints.format_rules) == 3

    def test_render_empty(self):
        """Test rendering empty constraints"""
        constraints = Constraints()
        rendered = constraints.render()
        assert isinstance(rendered, str)

    def test_render_must_include(self):
        """Test rendering must_include"""
        constraints = Constraints(
            must_include=["data", "examples"]
        )
        rendered = constraints.render()
        assert "include" in rendered.lower()
        assert "data" in rendered
        assert "examples" in rendered

    def test_render_must_not_include(self):
        """Test rendering must_not_include"""
        constraints = Constraints(
            must_not_include=["speculation"]
        )
        rendered = constraints.render()
        assert "not" in rendered.lower()
        assert "speculation" in rendered

    def test_render_format_rules(self):
        """Test rendering format_rules"""
        constraints = Constraints(
            format_rules=["Use markdown", "Be concise"]
        )
        rendered = constraints.render()
        assert "format" in rendered.lower()
        assert "Use markdown" in rendered
        assert "Be concise" in rendered

    def test_render_complete(self):
        """Test rendering all constraint types"""
        constraints = Constraints(
            must_include=["metrics"],
            must_not_include=["opinions"],
            format_rules=["Bullet points"]
        )
        rendered = constraints.render()
        assert "metrics" in rendered
        assert "opinions" in rendered
        assert "Bullet points" in rendered


class TestGuidanceGoal:
    """Test the new goal field on Guidance"""

    def test_goal_defaults_to_none(self):
        g = Guidance(role="Expert")
        assert g.goal is None

    def test_goal_is_stored(self):
        g = Guidance(role="Expert", goal="Find vulnerabilities")
        assert g.goal == "Find vulnerabilities"

    def test_render_includes_goal(self):
        g = Guidance(role="Expert", goal="Find vulnerabilities")
        rendered = g.render()
        assert "Goal: Find vulnerabilities" in rendered

    def test_render_without_goal_unchanged(self):
        g = Guidance(role="Expert", rules=["Be thorough"], style="direct")
        rendered = g.render()
        assert "You are Expert" in rendered
        assert "Goal" not in rendered


class TestConstraintsOutputSchema:
    """Test the new output_schema field on Constraints"""

    def test_output_schema_defaults_to_none(self):
        c = Constraints()
        assert c.output_schema is None

    def test_output_schema_is_stored(self):
        schema = [{"name": "sentiment", "type": "str"}, {"name": "confidence", "type": "float"}]
        c = Constraints(output_schema=schema)
        assert len(c.output_schema) == 2
        assert c.output_schema[0]["name"] == "sentiment"

    def test_render_includes_output_schema(self):
        schema = [{"name": "result", "type": "str"}]
        c = Constraints(output_schema=schema)
        rendered = c.render()
        assert "Output schema" in rendered
        assert "result (str)" in rendered

    def test_render_without_schema_unchanged(self):
        c = Constraints(must_include=["data"])
        rendered = c.render()
        assert "Output schema" not in rendered
        assert "data" in rendered


class TestFoundationIntegration:
    """Test Foundation classes working together"""

    def test_combined_rendering(self):
        """Test that all foundation components can be combined"""
        guidance = Guidance(role="Expert", rules=["Be thorough"])
        directive = Directive(content="Analyze data")
        constraints = Constraints(must_include=["metrics"])

        # All should render to strings
        assert isinstance(guidance.render(), str)
        assert isinstance(directive.render(), str)
        assert isinstance(constraints.render(), str)

        # Combined output
        combined = f"{guidance.render()}\n\n{constraints.render()}\n\n{directive.render()}"
        assert "Expert" in combined
        assert "metrics" in combined
        assert "Analyze data" in combined

    def test_combined_with_new_fields(self):
        """Test that new fields integrate with existing ones"""
        guidance = Guidance(role="Analyst", goal="Find trends", rules=["Be precise"])
        constraints = Constraints(
            must_include=["metrics"],
            output_schema=[{"name": "trend", "type": "str"}]
        )
        assert "Goal: Find trends" in guidance.render()
        assert "trend (str)" in constraints.render()
