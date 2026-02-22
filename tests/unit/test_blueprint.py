"""
Tests for Blueprint class
"""
from src.mycontext.foundation import Guidance
from src.mycontext.structure import Blueprint


class TestBlueprintCreation:
    """Test Blueprint creation"""

    def test_simple_blueprint(self):
        """Test creating a simple blueprint"""
        blueprint = Blueprint(
            name="test_blueprint",
            description="A test blueprint",
            guidance=Guidance(role="Test Assistant")
        )
        assert blueprint.name == "test_blueprint"
        assert blueprint.guidance.role == "Test Assistant"
        assert blueprint.token_budget == 4000  # default

    def test_with_custom_budget(self):
        """Test blueprint with custom token budget"""
        blueprint = Blueprint(
            name="test",
            token_budget=8000
        )
        assert blueprint.token_budget == 8000

    def test_with_components(self):
        """Test blueprint with components"""
        blueprint = Blueprint(
            name="test",
            components=["Component 1", "Component 2"]
        )
        assert len(blueprint.components) == 2


class TestBlueprintBuild:
    """Test Blueprint.build() method"""

    def test_build_basic(self):
        """Test building basic context from blueprint"""
        blueprint = Blueprint(
            name="test",
            guidance=Guidance(role="Expert")
        )
        context = blueprint.build()

        assert context.guidance.role == "Expert"
        assert context.metadata["blueprint"] == "test"

    def test_build_with_directive_template(self):
        """Test building with directive template"""
        blueprint = Blueprint(
            name="test",
            directive_template="Analyze: {topic}"
        )
        context = blueprint.build(topic="AI")

        assert context.directive is not None
        assert "AI" in context.directive.content

    def test_build_with_components(self):
        """Test that components are assembled into knowledge"""
        class MockComponent:
            def render(self):
                return "Mock component output"

        blueprint = Blueprint(
            name="test",
            components=[
                MockComponent(),
                "String component"
            ]
        )
        context = blueprint.build()

        assert context.knowledge is not None
        assert "Mock component output" in context.knowledge
        assert "String component" in context.knowledge

    def test_build_metadata(self):
        """Test that metadata is set correctly"""
        blueprint = Blueprint(
            name="test_bp",
            token_budget=5000,
            optimization="quality"
        )
        context = blueprint.build()

        assert context.metadata["blueprint"] == "test_bp"
        assert context.metadata["token_budget"] == 5000
        assert context.metadata["optimization"] == "quality"


class TestBlueprintOptimization:
    """Test Blueprint.optimize() method"""

    def test_optimize_speed(self):
        """Test speed optimization strategy"""
        blueprint = Blueprint(
            name="test",
            token_budget=4000
        )
        optimized = blueprint.optimize("speed")

        assert optimized.optimization == "speed"
        assert optimized.token_budget < 4000  # Should reduce budget
        assert optimized.priority_order[0] == "directive"  # Prioritizes directive

    def test_optimize_quality(self):
        """Test quality optimization strategy"""
        blueprint = Blueprint(
            name="test",
            token_budget=4000
        )
        optimized = blueprint.optimize("quality")

        assert optimized.optimization == "quality"
        assert optimized.token_budget > 4000  # Should increase budget
        # Should prioritize knowledge
        assert "knowledge" in optimized.priority_order[:2]

    def test_optimize_cost(self):
        """Test cost optimization strategy"""
        blueprint = Blueprint(
            name="test",
            token_budget=4000
        )
        optimized = blueprint.optimize("cost")

        assert optimized.optimization == "cost"
        assert optimized.token_budget < 4000  # Should minimize budget

    def test_optimize_balanced(self):
        """Test balanced optimization (default)"""
        blueprint = Blueprint(
            name="test",
            token_budget=4000
        )
        optimized = blueprint.optimize("balanced")

        assert optimized.optimization == "balanced"
        # Should keep defaults

    def test_optimization_doesnt_modify_original(self):
        """Test that optimization creates a copy"""
        original = Blueprint(
            name="test",
            token_budget=4000,
            optimization="balanced"
        )
        optimized = original.optimize("speed")

        # Original should be unchanged
        assert original.optimization == "balanced"
        assert original.token_budget == 4000

        # Optimized should be different
        assert optimized.optimization == "speed"
        assert optimized.token_budget != 4000


class TestBlueprintSerialization:
    """Test Blueprint serialization"""

    def test_to_dict(self):
        """Test converting blueprint to dictionary"""
        blueprint = Blueprint(
            name="test",
            description="Test blueprint",
            token_budget=5000
        )
        data = blueprint.to_dict()

        assert isinstance(data, dict)
        assert data["name"] == "test"
        assert data["description"] == "Test blueprint"
        assert data["token_budget"] == 5000

    def test_from_dict(self):
        """Test creating blueprint from dictionary"""
        data = {
            "name": "test",
            "description": "Test blueprint",
            "token_budget": 6000,
            "optimization": "quality"
        }
        blueprint = Blueprint.from_dict(data)

        assert blueprint.name == "test"
        assert blueprint.description == "Test blueprint"
        assert blueprint.token_budget == 6000
        assert blueprint.optimization == "quality"


class TestBlueprintTokenEstimation:
    """Test token estimation"""

    def test_estimate_empty(self):
        """Test estimating tokens for empty blueprint"""
        blueprint = Blueprint(name="test")
        estimate = blueprint.estimate_tokens()
        assert estimate >= 0

    def test_estimate_with_guidance(self):
        """Test estimating tokens with guidance"""
        blueprint = Blueprint(
            name="test",
            guidance=Guidance(
                role="Expert Analyst",
                rules=["Rule 1", "Rule 2"]
            )
        )
        estimate = blueprint.estimate_tokens()
        assert estimate > 0

    def test_estimate_with_template(self):
        """Test estimating tokens with directive template"""
        blueprint = Blueprint(
            name="test",
            directive_template="This is a longer directive template with more words"
        )
        estimate = blueprint.estimate_tokens()
        assert estimate > 0


class TestBlueprintRepresentation:
    """Test Blueprint string representation"""

    def test_repr(self):
        """Test __repr__"""
        blueprint = Blueprint(
            name="test_bp",
            components=["c1", "c2"],
            token_budget=5000
        )
        repr_str = repr(blueprint)

        assert "Blueprint" in repr_str
        assert "test_bp" in repr_str
        assert "2" in repr_str  # component count
        assert "5000" in repr_str  # token budget
