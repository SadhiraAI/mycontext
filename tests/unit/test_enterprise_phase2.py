"""
Unit tests for Phase 2 Enterprise patterns (Learning & Evaluation).

Tests for:
- Learning patterns (5)
- Evaluation patterns (5)
"""

from mycontext.intelligence.quality_metrics import QualityMetrics

# Evaluation patterns
from mycontext.templates.enterprise.evaluation import (
    FormativeAssessmentFramework,
    PeerAssessmentStructure,
    RubricDesigner,
    SelfAssessmentGuide,
    SummativeEvaluator,
)

# Learning patterns
from mycontext.templates.enterprise.learning import (
    CognitiveLoadManager,
    ConceptualChangeAnalyzer,
    ScaffoldingFramework,
    SpacedRepetitionOptimizer,
    ZoneOfProximalDevelopment,
)


class TestLearningPatterns:
    """Test Learning & Knowledge Building patterns."""

    def test_scaffolding_framework_basic(self):
        """Test ScaffoldingFramework pattern basics."""
        pattern = ScaffoldingFramework()

        # Check metadata
        assert pattern.name == "scaffolding_framework"
        assert "learning" in pattern.tags
        assert "enterprise" in pattern.tags
        assert pattern.metadata["category"] == "learning"
        assert pattern.metadata["license"] == "enterprise"

        # Build context
        context = pattern.build_context(
            task="Learn recursive programming",
            current_skill_level="Can write loops, unfamiliar with recursion",
        )

        # Verify context structure
        assert context.guidance.role == "Expert Instructor and Learning Scaffold Designer"
        assert "SCAFFOLDING FRAMEWORK" in context.directive.content
        assert "FADING STRATEGY" in context.directive.content
        print("[OK] ScaffoldingFramework basic test passed")

    def test_spaced_repetition_optimizer_basic(self):
        """Test SpacedRepetitionOptimizer pattern."""
        pattern = SpacedRepetitionOptimizer()

        assert pattern.name == "spaced_repetition_optimizer"
        assert "spaced-repetition" in pattern.tags

        context = pattern.build_context(
            learning_material="Spanish vocabulary: 50 words", initial_mastery="Just learned today"
        )

        assert "SPACED REPETITION SCHEDULE" in context.directive.content
        assert "FORGETTING CURVE" in context.directive.content
        assert "RETRIEVAL PRACTICE" in context.directive.content
        print("[OK] SpacedRepetitionOptimizer basic test passed")

    def test_zpd_basic(self):
        """Test ZoneOfProximalDevelopment pattern."""
        pattern = ZoneOfProximalDevelopment()

        assert pattern.name == "zone_of_proximal_development"
        assert "zpd" in pattern.tags

        context = pattern.build_context(
            learner_current_abilities="Can write basic Python functions",
            learning_goal="Master object-oriented programming",
        )

        assert "ZONE OF PROXIMAL DEVELOPMENT" in context.directive.content
        assert "THREE-ZONE ANALYSIS" in context.directive.content
        print("[OK] ZoneOfProximalDevelopment basic test passed")

    def test_cognitive_load_manager_basic(self):
        """Test CognitiveLoadManager pattern."""
        pattern = CognitiveLoadManager()

        assert pattern.name == "cognitive_load_manager"
        assert "cognitive-load" in pattern.tags

        context = pattern.build_context(
            learning_material="Quantum mechanics module",
            learner_background="Undergraduate physics students",
        )

        assert "COGNITIVE LOAD ANALYSIS" in context.directive.content
        assert "THREE-TYPE LOAD ANALYSIS" in context.directive.content
        assert "EXTRANEOUS LOAD" in context.directive.content
        assert "GERMANE LOAD" in context.directive.content
        print("[OK] CognitiveLoadManager basic test passed")

    def test_conceptual_change_analyzer_basic(self):
        """Test ConceptualChangeAnalyzer pattern."""
        pattern = ConceptualChangeAnalyzer()

        assert pattern.name == "conceptual_change_analyzer"
        assert "conceptual-change" in pattern.tags

        context = pattern.build_context(
            topic="Newton's laws of motion",
            current_understanding="Objects need continuous force to stay in motion",
        )

        assert "CONCEPTUAL CHANGE ANALYSIS" in context.directive.content
        assert "DIAGNOSE MISCONCEPTION" in context.directive.content
        assert "CREATE DISSATISFACTION" in context.directive.content
        print("[OK] ConceptualChangeAnalyzer basic test passed")


class TestEvaluationPatterns:
    """Test Evaluation & Assessment patterns."""

    def test_rubric_designer_basic(self):
        """Test RubricDesigner pattern."""
        pattern = RubricDesigner()

        assert pattern.name == "rubric_designer"
        assert "rubric" in pattern.tags
        assert "evaluation" in pattern.tags

        context = pattern.build_context(
            assessment_task="Research paper",
            learning_objectives="Synthesize sources, analyze critically",
        )

        assert "RUBRIC DESIGN" in context.directive.content
        assert "PERFORMANCE LEVEL DESCRIPTORS" in context.directive.content
        print("[OK] RubricDesigner basic test passed")

    def test_formative_assessment_basic(self):
        """Test FormativeAssessmentFramework pattern."""
        pattern = FormativeAssessmentFramework()

        assert pattern.name == "formative_assessment_framework"
        assert "formative" in pattern.tags

        context = pattern.build_context(
            learning_unit="Quadratic equations", learning_goal="Solve using multiple methods"
        )

        assert "FORMATIVE ASSESSMENT FRAMEWORK" in context.directive.content
        assert "CLARIFY LEARNING INTENTIONS" in context.directive.content
        assert "FEEDBACK THAT MOVES LEARNING FORWARD" in context.directive.content
        print("[OK] FormativeAssessmentFramework basic test passed")

    def test_summative_evaluator_basic(self):
        """Test SummativeEvaluator pattern."""
        pattern = SummativeEvaluator()

        assert pattern.name == "summative_evaluator"
        assert "summative" in pattern.tags

        context = pattern.build_context(
            course_title="Introduction to Data Science",
            learning_outcomes="Apply statistics, visualize data, build models",
        )

        assert "SUMMATIVE EVALUATION DESIGN" in context.directive.content
        assert "BACKWARD DESIGN" in context.directive.content
        print("[OK] SummativeEvaluator basic test passed")

    def test_peer_assessment_basic(self):
        """Test PeerAssessmentStructure pattern."""
        pattern = PeerAssessmentStructure()

        assert pattern.name == "peer_assessment_structure"
        assert "peer-assessment" in pattern.tags

        context = pattern.build_context(
            assessment_task="Research paper peer review",
            learning_objective="Evaluate research quality",
        )

        assert "PEER ASSESSMENT STRUCTURE" in context.directive.content
        assert "REVIEWER TRAINING" in context.directive.content
        print("[OK] PeerAssessmentStructure basic test passed")

    def test_self_assessment_basic(self):
        """Test SelfAssessmentGuide pattern."""
        pattern = SelfAssessmentGuide()

        assert pattern.name == "self_assessment_guide"
        assert "self-assessment" in pattern.tags

        context = pattern.build_context(
            work_to_assess="Final project", success_criteria="Functional UI, meets requirements"
        )

        assert "SELF-ASSESSMENT GUIDE" in context.directive.content
        assert "EVIDENCE-BASED SELF-EVALUATION" in context.directive.content
        assert "GOAL SETTING" in context.directive.content
        print("[OK] SelfAssessmentGuide basic test passed")


class TestPhase2Quality:
    """Test quality scores for Phase 2 patterns."""

    def test_learning_patterns_quality(self):
        """Test quality scores for learning patterns."""
        metrics = QualityMetrics(mode="heuristic")

        # Test Scaffolding
        pattern = ScaffoldingFramework()
        context = pattern.build_context(
            task="Learn Python decorators",
            current_skill_level="Can write functions, new to decorators",
            goal="Understand and apply decorators",
        )
        score = metrics.evaluate(context)
        assert score.overall >= 0.70, f"Scaffolding quality too low: {score.overall}"
        print(f"[OK] ScaffoldingFramework quality: {score.overall:.2f}")

        # Test Spaced Repetition
        pattern = SpacedRepetitionOptimizer()
        context = pattern.build_context(
            learning_material="French vocabulary: 100 words",
            initial_mastery="Just learned",
            previous_performance="80% recall after 1 day",
        )
        score = metrics.evaluate(context)
        assert score.overall >= 0.70
        print(f"[OK] SpacedRepetitionOptimizer quality: {score.overall:.2f}")

    def test_evaluation_patterns_quality(self):
        """Test quality scores for evaluation patterns."""
        metrics = QualityMetrics(mode="heuristic")

        # Test Rubric Designer
        pattern = RubricDesigner()
        context = pattern.build_context(
            assessment_task="Essay on climate change",
            learning_objectives="Analyze sources, develop argument, write clearly",
        )
        score = metrics.evaluate(context)
        assert score.overall >= 0.70
        print(f"[OK] RubricDesigner quality: {score.overall:.2f}")

        # Test Formative Assessment
        pattern = FormativeAssessmentFramework()
        context = pattern.build_context(
            learning_unit="Linear equations module",
            learning_goal="Solve and graph linear equations",
        )
        score = metrics.evaluate(context)
        assert score.overall >= 0.70
        print(f"[OK] FormativeAssessmentFramework quality: {score.overall:.2f}")


if __name__ == "__main__":
    # Run tests
    print("=== Testing Learning Patterns ===")
    test_learning = TestLearningPatterns()
    test_learning.test_scaffolding_framework_basic()
    test_learning.test_spaced_repetition_optimizer_basic()
    test_learning.test_zpd_basic()
    test_learning.test_cognitive_load_manager_basic()
    test_learning.test_conceptual_change_analyzer_basic()

    print("\n=== Testing Evaluation Patterns ===")
    test_eval = TestEvaluationPatterns()
    test_eval.test_rubric_designer_basic()
    test_eval.test_formative_assessment_basic()
    test_eval.test_summative_evaluator_basic()
    test_eval.test_peer_assessment_basic()
    test_eval.test_self_assessment_basic()

    print("\n=== Testing Quality Scores ===")
    test_quality = TestPhase2Quality()
    test_quality.test_learning_patterns_quality()
    test_quality.test_evaluation_patterns_quality()

    print("\n✅ ALL PHASE 2 TESTS PASSED!")
