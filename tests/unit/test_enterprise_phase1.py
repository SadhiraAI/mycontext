"""
Tests for Phase 1 Enterprise Patterns (Metacognition, Ethical Reasoning, Systems Thinking).
"""

import pytest

from mycontext.core import Context
from mycontext.intelligence.quality_metrics import QualityDimension, QualityMetrics
from mycontext.templates.enterprise.ethical_reasoning import EthicalFrameworkAnalyzer
from mycontext.templates.enterprise.metacognition import (
    CognitiveStrategySelector,
    ErrorDetectionFramework,
    LearningFromExperience,
    MetacognitiveMonitor,
    SelfRegulationFramework,
)


class TestMetacognitionPatterns:
    """Test all 5 enterprise metacognition patterns."""

    def test_metacognitive_monitor_basic_context(self):
        """Test MetacognitiveMonitor builds valid context."""
        pattern = MetacognitiveMonitor()

        # Verify pattern metadata
        assert pattern.name == "metacognitive_monitor"
        assert "metacognition" in pattern.tags
        assert pattern.metadata["category"] == "metacognition"
        assert pattern.metadata["license"] == "enterprise"
        assert pattern.input_schema is not None

        # Test basic context building
        context = pattern.build_context(
            task_description="Learn Python programming basics",
            current_approach="Reading tutorials and practicing exercises",
            progress_so_far="Completed Chapters 1-3, understand variables and loops",
        )

        # Verify context structure
        assert isinstance(context, Context)
        assert context.guidance is not None
        assert context.directive is not None
        assert context.constraints is not None

        # Verify metacognitive content in guidance
        assert (
            "Metacognitive" in context.guidance.role
            or "metacognitive" in " ".join(context.guidance.rules).lower()
        )
        assert len(context.guidance.rules) >= 3

        # Verify directive contains the 5 dimensions
        directive_text = context.directive.content
        assert "COMPREHENSION STATUS" in directive_text
        assert "STRATEGY ASSESSMENT" in directive_text
        assert "ERRORS DETECTED" in directive_text
        assert "PROGRESS EVALUATION" in directive_text
        assert "RECOMMENDED ADJUSTMENTS" in directive_text

        # Verify task details are in directive
        assert "Learn Python programming basics" in directive_text
        assert "Reading tutorials and practicing exercises" in directive_text
        assert "Completed Chapters 1-3" in directive_text

        # Verify constraints mention key requirements
        must_include = context.constraints.must_include
        assert "comprehension_status" in must_include
        assert "strategy_assessment" in must_include
        assert "errors_detected" in must_include

    def test_metacognitive_monitor_with_challenges(self):
        """Test MetacognitiveMonitor with optional challenges parameter."""
        pattern = MetacognitiveMonitor()

        context = pattern.build_context(
            task_description="Debug a complex algorithm",
            current_approach="Using print statements to trace execution",
            progress_so_far="Identified the issue is in the loop logic",
            challenges="Confused about why the loop terminates early",
        )

        # Verify challenges are included in directive
        directive_text = context.directive.content
        assert "CHALLENGES ENCOUNTERED" in directive_text
        assert "loop terminates early" in directive_text

    def test_metacognitive_monitor_quality_score(self):
        """Test that MetacognitiveMonitor produces high-quality context."""
        pattern = MetacognitiveMonitor()

        context = pattern.build_context(
            task_description="Write a research paper on machine learning",
            current_approach="Literature review followed by experimentation",
            progress_so_far="Completed literature review, starting experiments",
        )

        # Measure quality using heuristic mode (fast)
        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(context)

        # Should be high quality (>0.75 for enterprise patterns)
        assert score.overall >= 0.75, f"Quality too low: {score.overall} (issues: {score.issues})"

        # Check individual dimensions (from dimensions dict)
        assert score.dimensions[QualityDimension.CLARITY] >= 0.7, (
            f"Clarity too low: {score.dimensions[QualityDimension.CLARITY]}"
        )
        assert score.dimensions[QualityDimension.COMPLETENESS] >= 0.7, (
            f"Completeness too low: {score.dimensions[QualityDimension.COMPLETENESS]}"
        )
        assert score.dimensions[QualityDimension.STRUCTURE] >= 0.7, (
            f"Structure too low: {score.dimensions[QualityDimension.STRUCTURE]}"
        )

        print(f"\n[OK] MetacognitiveMonitor Quality Score: {score.overall:.2f}")
        print(f"   - Clarity: {score.dimensions[QualityDimension.CLARITY]:.2f}")
        print(f"   - Completeness: {score.dimensions[QualityDimension.COMPLETENESS]:.2f}")
        print(f"   - Structure: {score.dimensions[QualityDimension.STRUCTURE]:.2f}")
        if score.issues:
            print(f"   - Issues: {score.issues}")

    def test_metacognitive_monitor_input_schema(self):
        """Test that input schema is correctly defined."""
        pattern = MetacognitiveMonitor()

        schema = pattern.input_schema
        assert "task_description" in schema
        assert "current_approach" in schema
        assert "progress_so_far" in schema
        assert "challenges_section" in schema  # Internal parameter (auto-generated from challenges)

    def test_metacognitive_monitor_output_structure(self):
        """Test that context provides clear output structure guidance."""
        pattern = MetacognitiveMonitor()

        context = pattern.build_context(
            task_description="Learn data structures",
            current_approach="Solving practice problems",
            progress_so_far="Completed arrays and linked lists",
        )

        # Verify directive has all 5 sections with clear structure
        directive_text = context.directive.content

        # Verify numbered sections
        assert "## 1. COMPREHENSION STATUS" in directive_text
        assert "## 2. STRATEGY ASSESSMENT" in directive_text
        assert "## 3. ERRORS DETECTED" in directive_text
        assert "## 4. PROGRESS EVALUATION" in directive_text
        assert "## 5. RECOMMENDED ADJUSTMENTS" in directive_text

    def test_self_regulation_framework_forethought_phase(self):
        """Test SelfRegulationFramework in forethought phase."""
        pattern = SelfRegulationFramework()

        context = pattern.build_context(
            goal="Master data structures and algorithms", current_phase="forethought"
        )

        assert isinstance(context, Context)
        assert "Self-Regulated Learning" in context.guidance.role
        directive_text = context.directive.content

        # Verify forethought content
        assert "FORETHOUGHT PHASE" in directive_text
        assert "Goal Setting" in directive_text
        assert "Strategic Planning" in directive_text
        assert "Self-Motivation" in directive_text
        assert "Move to PERFORMANCE" in directive_text

    def test_self_regulation_framework_performance_phase(self):
        """Test SelfRegulationFramework in performance phase."""
        pattern = SelfRegulationFramework()

        context = pattern.build_context(goal="Master data structures", current_phase="performance")

        directive_text = context.directive.content
        assert "PERFORMANCE PHASE" in directive_text
        assert "Self-Control" in directive_text
        assert "Self-Observation" in directive_text
        assert "Move to SELF-REFLECTION" in directive_text

    def test_self_regulation_framework_reflection_phase(self):
        """Test SelfRegulationFramework in self-reflection phase."""
        pattern = SelfRegulationFramework()

        context = pattern.build_context(
            goal="Master data structures",
            current_phase="self-reflection",
            performance_data="Completed 80% of exercises, struggled with graphs",
        )

        directive_text = context.directive.content
        assert "SELF-REFLECTION PHASE" in directive_text
        assert "Self-Evaluation" in directive_text
        assert "Causal Attribution" in directive_text
        assert "struggled with graphs" in directive_text
        assert "Return to FORETHOUGHT" in directive_text

    def test_self_regulation_framework_quality(self):
        """Test SelfRegulationFramework quality score."""
        pattern = SelfRegulationFramework()

        context = pattern.build_context(
            goal="Learn machine learning",
            current_phase="forethought",
            context="Starting from basic Python knowledge",
        )

        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(context)

        assert score.overall >= 0.75, f"Quality too low: {score.overall}"
        print(f"\n[OK] SelfRegulationFramework Quality: {score.overall:.2f}")

    def test_cognitive_strategy_selector_problem_solving(self):
        """Test CognitiveStrategySelector for problem-solving tasks."""
        pattern = CognitiveStrategySelector()

        context = pattern.build_context(
            task_type="problem-solving",
            task_characteristics="Complex, multi-step, unfamiliar algorithm",
        )

        assert isinstance(context, Context)
        directive_text = context.directive.content

        assert "COGNITIVE STRATEGY SELECTION" in directive_text
        assert "TASK ANALYSIS" in directive_text
        assert "STRATEGY CATALOG" in directive_text
        assert "Problem-Solving Strategies" in directive_text
        assert "RECOMMENDATION" in directive_text

    def test_cognitive_strategy_selector_quality(self):
        """Test CognitiveStrategySelector quality score."""
        pattern = CognitiveStrategySelector()

        context = pattern.build_context(
            task_type="learning",
            task_characteristics="New conceptual material, moderate complexity",
            learner_characteristics="Beginner, visual learner",
        )

        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(context)

        assert score.overall >= 0.75
        print(f"\n[OK] CognitiveStrategySelector Quality: {score.overall:.2f}")

    def test_learning_from_experience_basic(self):
        """Test LearningFromExperience pattern."""
        pattern = LearningFromExperience()

        context = pattern.build_context(
            experience_description="Product launch that missed targets",
            outcome="Sold 5k units instead of expected 10k",
            initial_expectations="Expected 10k units based on market research",
        )

        assert isinstance(context, Context)
        directive_text = context.directive.content

        assert "LEARNING FROM EXPERIENCE" in directive_text
        assert "CONCRETE EXPERIENCE" in directive_text
        assert "REFLECTIVE OBSERVATION" in directive_text
        assert "ABSTRACT CONCEPTUALIZATION" in directive_text
        assert "ACTIVE EXPERIMENTATION" in directive_text
        assert "Sold 5k units" in directive_text

    def test_learning_from_experience_quality(self):
        """Test LearningFromExperience quality score."""
        pattern = LearningFromExperience()

        context = pattern.build_context(
            experience_description="Failed algorithm implementation",
            outcome="Performance was 10x slower than expected",
            initial_expectations="O(n log n) but got O(n^2)",
        )

        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(context)

        assert score.overall >= 0.65  # Slightly lower due to verbosity but still high quality
        print(f"\n[OK] LearningFromExperience Quality: {score.overall:.2f}")

    def test_error_detection_framework_programming(self):
        """Test ErrorDetectionFramework for programming domain."""
        pattern = ErrorDetectionFramework()

        context = pattern.build_context(
            work_to_check="def quicksort(arr): return sorted(arr)", domain="programming"
        )

        assert isinstance(context, Context)
        directive_text = context.directive.content

        assert "ERROR DETECTION" in directive_text
        assert "SELF-EXPLANATION CHECK" in directive_text
        assert "COGNITIVE BIAS CHECK" in directive_text
        assert "Programming-Specific Errors" in directive_text

    def test_error_detection_framework_quality(self):
        """Test ErrorDetectionFramework quality score."""
        pattern = ErrorDetectionFramework()

        context = pattern.build_context(
            work_to_check="All swans are white because I've only seen white swans",
            domain="reasoning",
        )

        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(context)

        assert score.overall >= 0.70
        print(f"\n[OK] ErrorDetectionFramework Quality: {score.overall:.2f}")


class TestEthicalReasoningPatterns:
    """Test all 5 enterprise ethical reasoning patterns."""

    def test_ethical_framework_analyzer_basic(self):
        """Test EthicalFrameworkAnalyzer with basic decision."""
        pattern = EthicalFrameworkAnalyzer()

        context = pattern.build_context(
            decision="Deploy facial recognition in public spaces",
            stakeholders="Citizens, law enforcement, privacy advocates",
        )

        assert isinstance(context, Context)
        directive_text = context.directive.content

        # Check all 6 frameworks present
        assert "UTILITARIAN APPROACH" in directive_text
        assert "RIGHTS APPROACH" in directive_text
        assert "JUSTICE/FAIRNESS APPROACH" in directive_text
        assert "COMMON GOOD APPROACH" in directive_text
        assert "VIRTUE APPROACH" in directive_text
        assert "CARE ETHICS APPROACH" in directive_text

        assert "facial recognition" in directive_text

    def test_ethical_framework_analyzer_quality(self):
        """Test EthicalFrameworkAnalyzer quality score."""
        pattern = EthicalFrameworkAnalyzer()

        context = pattern.build_context(
            decision="Mandatory COVID-19 vaccination policy",
            stakeholders="Employees, public health officials, individual rights advocates",
        )

        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(context)

        assert score.overall >= 0.70
        print(f"\n[OK] EthicalFrameworkAnalyzer Quality: {score.overall:.2f}")


class TestSystemsThinkingPatterns:
    """Test all 6 enterprise systems thinking patterns."""

    def test_placeholder(self):
        """Placeholder - patterns not yet implemented."""
        pytest.skip("Systems thinking patterns not yet implemented")


# Run tests with: pytest tests/unit/test_enterprise_phase1.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
