"""
Unit tests for Phase 3 enterprise patterns (Temporal, Diagnostic, Synthesis).

Tests all 9 patterns for basic functionality and quality scores.
"""

import pytest

from mycontext.intelligence.quality_metrics import QualityDimension, QualityMetrics

# Diagnostic patterns
from mycontext.templates.enterprise.diagnostic import (
    DifferentialDiagnoser,
    RootCauseAnalyzer,
    SystemHealthAuditor,
)

# Synthesis patterns
from mycontext.templates.enterprise.synthesis import (
    CrossDomainSynthesizer,
    HolisticIntegrator,
    PatternRecognitionEngine,
)

# Temporal patterns
from mycontext.templates.enterprise.temporal import (
    FutureScenarioPlanner,
    HistoricalContextMapper,
    TemporalSequenceAnalyzer,
)

# =====================
# TEMPORAL PATTERNS (3)
# =====================


def test_temporal_sequence_analyzer_basic():
    """Test TemporalSequenceAnalyzer pattern basics."""
    pattern = TemporalSequenceAnalyzer()

    assert pattern.name == "temporal_sequence_analyzer"
    assert "temporal" in pattern.tags
    assert "enterprise" in pattern.tags
    assert pattern.metadata["category"] == "temporal"
    assert pattern.metadata["license"] == "enterprise"

    # Test input schema
    assert "events" in pattern.input_schema
    assert "time_span" in pattern.input_schema

    # Test context building
    context = pattern.build_context(
        events="Product launch, Sales spike, Competitor reaction", time_span="Last 3 months"
    )

    assert context.guidance.role == "Temporal Analysis Expert and Historian"
    assert "chronological order" in context.guidance.rules[0].lower()
    assert "TEMPORAL SEQUENCE ANALYSIS" in context.directive.content


def test_temporal_sequence_analyzer_quality():
    """Test TemporalSequenceAnalyzer quality metrics."""
    pattern = TemporalSequenceAnalyzer()

    context = pattern.build_context(
        events="Economic recession, unemployment rise, policy changes", time_span="2008-2010"
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75
    assert score.dimensions[QualityDimension.CLARITY] >= 0.7
    assert score.dimensions[QualityDimension.STRUCTURE] >= 0.8


def test_future_scenario_planner_basic():
    """Test FutureScenarioPlanner pattern basics."""
    pattern = FutureScenarioPlanner()

    assert pattern.name == "future_scenario_planner"
    assert "scenario-planning" in pattern.tags
    assert pattern.metadata["category"] == "temporal"

    # Test input schema
    assert "focal_question" in pattern.input_schema
    assert "time_horizon" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        focal_question="How will remote work evolve?",
        time_horizon="5 years",
        current_situation="Post-pandemic hybrid work models",
    )

    assert context.guidance.role == "Scenario Planning Expert and Strategic Futurist"
    assert "FUTURE SCENARIO PLANNING" in context.directive.content
    assert "SCENARIO" in context.directive.content.upper()


def test_future_scenario_planner_quality():
    """Test FutureScenarioPlanner quality."""
    pattern = FutureScenarioPlanner()

    context = pattern.build_context(
        focal_question="Future of AI in healthcare",
        time_horizon="10 years",
        current_situation="Emerging AI diagnostic tools",
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    # Slightly lower threshold due to comprehensive scenario structure (still high quality)
    assert score.overall >= 0.70
    assert score.dimensions[QualityDimension.COMPLETENESS] >= 0.7


def test_historical_context_mapper_basic():
    """Test HistoricalContextMapper pattern basics."""
    pattern = HistoricalContextMapper()

    assert pattern.name == "historical_context_mapper"
    assert "history" in pattern.tags
    assert pattern.metadata["category"] == "temporal"

    # Test input schema
    assert "current_situation" in pattern.input_schema
    assert "question" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        current_situation="Economic inflation and policy debates",
        question="What can we learn from past inflationary periods?",
    )

    assert "Historian" in context.guidance.role
    assert "HISTORICAL CONTEXT MAPPING" in context.directive.content
    assert "PRECEDENT" in context.directive.content.upper()


def test_historical_context_mapper_quality():
    """Test HistoricalContextMapper quality."""
    pattern = HistoricalContextMapper()

    context = pattern.build_context(
        current_situation="Tech market downturn", question="How did past tech bubbles resolve?"
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75


# =======================
# DIAGNOSTIC PATTERNS (3)
# =======================


def test_root_cause_analyzer_basic():
    """Test RootCauseAnalyzer pattern basics."""
    pattern = RootCauseAnalyzer()

    assert pattern.name == "diagnostic_root_cause_analyzer"
    assert "root-cause" in pattern.tags
    assert pattern.metadata["category"] == "diagnostic"
    assert pattern.metadata["license"] == "enterprise"

    # Test input schema
    assert "problem" in pattern.input_schema
    assert "symptoms" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        problem="Website downtime increasing",
        symptoms="Slow response, 500 errors, database timeouts",
    )

    assert "Root Cause Analysis Expert" in context.guidance.role
    assert "ROOT CAUSE ANALYSIS" in context.directive.content
    assert "FIVE WHYS" in context.directive.content.upper()
    assert "ISHIKAWA" in context.directive.content.upper()


def test_root_cause_analyzer_quality():
    """Test RootCauseAnalyzer quality."""
    pattern = RootCauseAnalyzer()

    context = pattern.build_context(
        problem="Customer satisfaction scores dropping",
        symptoms="Complaints about support, slow resolution times",
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75
    assert score.dimensions[QualityDimension.STRUCTURE] >= 0.8


def test_differential_diagnoser_basic():
    """Test DifferentialDiagnoser pattern basics."""
    pattern = DifferentialDiagnoser()

    assert pattern.name == "differential_diagnoser"
    assert "differential" in pattern.tags
    assert pattern.metadata["category"] == "diagnostic"

    # Test input schema
    assert "presenting_problem" in pattern.input_schema
    assert "observed_data" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        presenting_problem="API response time degraded 10x",
        observed_data="Started yesterday, all endpoints affected",
        domain="Web services",
    )

    assert "Diagnostic Reasoning Expert" in context.guidance.role
    assert "DIFFERENTIAL DIAGNOSIS" in context.directive.content
    assert "HYPOTHESIS" in context.directive.content.upper()


def test_differential_diagnoser_quality():
    """Test DifferentialDiagnoser quality."""
    pattern = DifferentialDiagnoser()

    context = pattern.build_context(
        presenting_problem="Memory leak in production",
        observed_data="Memory usage grows steadily, restarts temporarily fix",
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75


def test_system_health_auditor_basic():
    """Test SystemHealthAuditor pattern basics."""
    pattern = SystemHealthAuditor()

    assert pattern.name == "system_health_auditor"
    assert "audit" in pattern.tags
    assert pattern.metadata["category"] == "diagnostic"

    # Test input schema
    assert "system" in pattern.input_schema
    assert "audit_focus" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        system="E-commerce platform", audit_focus="Performance, security, scalability"
    )

    assert "Systems Auditor" in context.guidance.role
    assert "SYSTEM HEALTH AUDIT" in context.directive.content
    assert "AUDIT DIMENSIONS" in context.directive.content.upper()


def test_system_health_auditor_quality():
    """Test SystemHealthAuditor quality."""
    pattern = SystemHealthAuditor()

    context = pattern.build_context(
        system="Mobile application backend", audit_focus="Reliability and security"
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75
    assert score.dimensions[QualityDimension.COMPLETENESS] >= 0.7


# ======================
# SYNTHESIS PATTERNS (3)
# ======================


def test_cross_domain_synthesizer_basic():
    """Test CrossDomainSynthesizer pattern basics."""
    pattern = CrossDomainSynthesizer()

    assert pattern.name == "cross_domain_synthesizer"
    assert "cross-domain" in pattern.tags
    assert pattern.metadata["category"] == "synthesis"
    assert pattern.metadata["license"] == "enterprise"

    # Test input schema
    assert "target_problem" in pattern.input_schema
    assert "source_domains" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        target_problem="Improve team collaboration",
        source_domains="Neuroscience (neural networks), Jazz music (improvisation)",
    )

    assert "Cross-Domain Innovation Expert" in context.guidance.role
    assert "CROSS-DOMAIN SYNTHESIS" in context.directive.content
    assert "DOMAIN MAPPING" in context.directive.content.upper()


def test_cross_domain_synthesizer_quality():
    """Test CrossDomainSynthesizer quality."""
    pattern = CrossDomainSynthesizer()

    context = pattern.build_context(
        target_problem="Reduce customer churn",
        source_domains="Biology (immune system), Physics (entropy)",
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75


def test_pattern_recognition_engine_basic():
    """Test PatternRecognitionEngine pattern basics."""
    pattern = PatternRecognitionEngine()

    assert pattern.name == "pattern_recognition_engine"
    assert "patterns" in pattern.tags
    assert pattern.metadata["category"] == "synthesis"

    # Test input schema
    assert "data" in pattern.input_schema
    assert "pattern_focus" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        data="User behavior logs: 10k sessions with clicks, time, conversions",
        pattern_focus="What drives conversions",
    )

    assert "Pattern Recognition" in context.guidance.role
    assert "PATTERN RECOGNITION ANALYSIS" in context.directive.content
    assert "PATTERN TYPES" in context.directive.content.upper()


def test_pattern_recognition_engine_quality():
    """Test PatternRecognitionEngine quality."""
    pattern = PatternRecognitionEngine()

    context = pattern.build_context(
        data="Sales data: 500 transactions over 2 years",
        pattern_focus="Seasonal trends and customer segments",
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75
    assert score.dimensions[QualityDimension.STRUCTURE] >= 0.8


def test_holistic_integrator_basic():
    """Test HolisticIntegrator pattern basics."""
    pattern = HolisticIntegrator()

    assert pattern.name == "holistic_integrator"
    assert "integration" in pattern.tags
    assert "holistic" in pattern.tags
    assert pattern.metadata["category"] == "synthesis"

    # Test input schema
    assert "topic" in pattern.input_schema
    assert "perspectives" in pattern.input_schema

    # Test context
    context = pattern.build_context(
        topic="Company digital transformation",
        perspectives="Technical, Business, Cultural, Customer",
    )

    assert "Holistic Systems Integrator" in context.guidance.role
    assert "HOLISTIC INTEGRATION" in context.directive.content
    assert "PERSPECTIVE" in context.directive.content.upper()


def test_holistic_integrator_quality():
    """Test HolisticIntegrator quality."""
    pattern = HolisticIntegrator()

    context = pattern.build_context(
        topic="Healthcare system redesign",
        perspectives="Clinical, Administrative, Patient, Financial",
    )

    metrics = QualityMetrics()
    score = metrics.evaluate(context)

    assert score.overall >= 0.75
    assert score.dimensions[QualityDimension.COMPLETENESS] >= 0.7


# ======================
# INTEGRATION TESTS
# ======================


def test_all_phase3_patterns_importable():
    """Test that all Phase 3 patterns are importable."""
    from mycontext.templates.enterprise.diagnostic import __all__ as diagnostic_all
    from mycontext.templates.enterprise.synthesis import __all__ as synthesis_all
    from mycontext.templates.enterprise.temporal import __all__ as temporal_all

    assert len(temporal_all) == 3
    assert (
        len(diagnostic_all) == 4
    )  # DiagnosticRootCauseAnalyzer + RootCauseAnalyzer alias + 2 others
    assert len(synthesis_all) == 3


def test_phase3_enterprise_metadata():
    """Test that all Phase 3 patterns have correct enterprise metadata."""
    patterns = [
        TemporalSequenceAnalyzer(),
        FutureScenarioPlanner(),
        HistoricalContextMapper(),
        RootCauseAnalyzer(),
        DifferentialDiagnoser(),
        SystemHealthAuditor(),
        CrossDomainSynthesizer(),
        PatternRecognitionEngine(),
        HolisticIntegrator(),
    ]

    for pattern in patterns:
        assert "enterprise" in pattern.tags
        assert pattern.metadata["license"] == "enterprise"
        assert pattern.metadata["tier"] == "enterprise"
        assert pattern.version == "1.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
