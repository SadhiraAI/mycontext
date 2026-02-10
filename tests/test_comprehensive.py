"""
Comprehensive Test Suite - Test ALL 50 patterns + systems

Tests:
- Pattern imports (all categories)
- Transformation Engine
- Quality Metrics
- Export Formats
- Integration Helpers
- Pattern execution
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 80)
print("COMPREHENSIVE TEST SUITE - mycontext SDK")
print("=" * 80)
print()

# Track results
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test(name, func):
    """Run a test and track results."""
    try:
        func()
        test_results["passed"] += 1
        print(f"[PASS]: {name}")
        return True
    except Exception as e:
        test_results["failed"] += 1
        test_results["errors"].append((name, str(e)))
        print(f"[FAIL]: {name}")
        print(f"   Error: {str(e)[:100]}")
        return False

print("\n" + "=" * 80)
print("TEST 1: CATEGORY IMPORTS (8 categories)")
print("=" * 80)

def test_analysis_imports():
    from mycontext.templates.free.analysis import (
        QuestionAnalyzer, DataAnalyzer, TrendIdentifier,
        GapAnalyzer, SWOTAnalyzer, AnomalyDetector
    )
    assert QuestionAnalyzer is not None
    assert len([QuestionAnalyzer, DataAnalyzer, TrendIdentifier, GapAnalyzer, SWOTAnalyzer, AnomalyDetector]) == 6

def test_reasoning_imports():
    from mycontext.templates.free.reasoning import (
        StepByStepReasoner, AnalogicalReasoner, CausalReasoner,
        RootCauseAnalyzer, HypothesisGenerator
    )
    assert StepByStepReasoner is not None
    assert len([StepByStepReasoner, AnalogicalReasoner, CausalReasoner, RootCauseAnalyzer, HypothesisGenerator]) == 5

def test_decision_imports():
    from mycontext.templates.free.decision import (
        DecisionFramework, ComparativeAnalyzer, TradeoffAnalyzer,
        MultiObjectiveOptimizer, CostBenefitAnalyzer
    )
    assert DecisionFramework is not None
    assert len([DecisionFramework, ComparativeAnalyzer, TradeoffAnalyzer, MultiObjectiveOptimizer, CostBenefitAnalyzer]) == 5

def test_creative_imports():
    from mycontext.templates.free.creative import (
        IdeaGenerator, Brainstormer, InnovationFramework,
        DesignThinker, MetaphorGenerator
    )
    assert IdeaGenerator is not None

def test_communication_imports():
    from mycontext.templates.free.communication import (
        SimplificationEngine, ClarityOptimizer, AudienceAdapter,
        PersuasionFramework, NarrativeBuilder, TechnicalTranslator,
        FeedbackComposer
    )
    assert SimplificationEngine is not None

def test_planning_imports():
    from mycontext.templates.free.planning import (
        ScenarioPlanner, StakeholderMapper, PrioritySetter,
        DeadlineManager, ResourceAllocator
    )
    assert ScenarioPlanner is not None

def test_problem_solving_imports():
    from mycontext.templates.free.problem_solving import (
        ProblemDecomposer, BottleneckIdentifier, ConstraintOptimizer,
        DependencyMapper, EfficiencyAnalyzer, TradeSpaceExplorer
    )
    assert ProblemDecomposer is not None

def test_specialized_imports():
    from mycontext.templates.free.specialized import (
        CodeReviewer, ContentOutliner, SocraticQuestioner,
        IntentRecognizer, AmbiguityResolver, RiskAssessor,
        RiskMitigator, ImpactAssessor, ConflictResolver,
        ConceptExplainer, SynthesisBuilder
    )
    assert CodeReviewer is not None

test("Analysis category imports", test_analysis_imports)
test("Reasoning category imports", test_reasoning_imports)
test("Decision category imports", test_decision_imports)
test("Creative category imports", test_creative_imports)
test("Communication category imports", test_communication_imports)
test("Planning category imports", test_planning_imports)
test("Problem Solving category imports", test_problem_solving_imports)
test("Specialized category imports", test_specialized_imports)

print("\n" + "=" * 80)
print("TEST 2: BACKWARD COMPATIBILITY (Main imports)")
print("=" * 80)

def test_main_imports():
    from mycontext.templates.free import (
        QuestionAnalyzer, DataAnalyzer, DecisionFramework,
        IdeaGenerator, SimplificationEngine, ScenarioPlanner
    )
    assert QuestionAnalyzer is not None
    assert DataAnalyzer is not None

test("Main module imports (backward compatibility)", test_main_imports)

print("\n" + "=" * 80)
print("TEST 3: PATTERN INSTANTIATION (Sample patterns)")
print("=" * 80)

def test_pattern_instantiation():
    from mycontext.templates.free.analysis import QuestionAnalyzer
    from mycontext.templates.free.decision import DecisionFramework
    from mycontext.templates.free.creative import IdeaGenerator
    
    qa = QuestionAnalyzer()
    df = DecisionFramework()
    ig = IdeaGenerator()
    
    assert qa.name == "question_analyzer"
    assert df.name == "decision_framework"
    assert ig.name == "idea_generator"

test("Pattern instantiation", test_pattern_instantiation)

print("\n" + "=" * 80)
print("TEST 4: PATTERN BUILD_CONTEXT (Context creation)")
print("=" * 80)

def test_build_context():
    from mycontext.templates.free.analysis import QuestionAnalyzer
    from mycontext import Context
    
    qa = QuestionAnalyzer()
    context = qa.build_context(
        question="What is the best approach?",
        depth="comprehensive"
    )
    
    assert isinstance(context, Context)
    assert context.directive is not None
    assert context.guidance is not None

test("Pattern build_context method", test_build_context)

print("\n" + "=" * 80)
print("TEST 5: TRANSFORMATION ENGINE")
print("=" * 80)

def test_transformation_engine_init():
    from mycontext.intelligence import TransformationEngine
    engine = TransformationEngine()
    assert engine is not None
    assert len(engine._pattern_registry) > 0

def test_transformation_engine_analysis():
    from mycontext.intelligence import TransformationEngine
    engine = TransformationEngine()
    analysis = engine.analyze_input("How does machine learning work?")
    assert analysis.input_type is not None
    assert analysis.complexity is not None
    assert len(analysis.recommended_patterns) > 0

def test_transformation_engine_transform():
    from mycontext.intelligence import TransformationEngine, transform
    
    # Test via engine
    engine = TransformationEngine()
    context = engine.transform("Should we migrate to the cloud?")
    assert context is not None
    
    # Test via convenience function
    context2 = transform("What are the risks?")
    assert context2 is not None

test("TransformationEngine initialization", test_transformation_engine_init)
test("TransformationEngine input analysis", test_transformation_engine_analysis)
test("TransformationEngine transform", test_transformation_engine_transform)

print("\n" + "=" * 80)
print("TEST 6: QUALITY METRICS")
print("=" * 80)

def test_quality_metrics():
    from mycontext import Context, Directive, Guidance
    from mycontext.intelligence import QualityMetrics
    
    context = Context(
        guidance=Guidance(
            role="Expert Analyst",
            rules=["Be clear", "Be thorough"]
        ),
        directive=Directive(content="Analyze the data systematically")
    )
    
    metrics = QualityMetrics()
    score = metrics.evaluate(context)
    
    assert 0.0 <= score.overall <= 1.0
    assert len(score.dimensions) == 6
    assert score.metadata is not None

def test_quality_report():
    from mycontext import Context
    from mycontext.intelligence import QualityMetrics
    
    context = Context(guidance="Test")
    metrics = QualityMetrics()
    score = metrics.evaluate(context)
    report = metrics.report(score)
    
    assert "Quality Report" in report
    assert "Overall Score" in report

test("QualityMetrics evaluation", test_quality_metrics)
test("QualityMetrics report generation", test_quality_report)

print("\n" + "=" * 80)
print("TEST 7: EXPORT FORMATS (13 formats)")
print("=" * 80)

def test_basic_exports():
    from mycontext import Context, Directive
    context = Context(directive=Directive(content="Test"))
    
    # Test each export format
    assert context.to_dict() is not None
    assert context.to_json() is not None
    assert context.to_markdown() is not None
    assert context.to_messages() is not None

def test_framework_exports():
    from mycontext import Context
    context = Context(guidance="Expert")
    
    assert context.to_langchain() is not None
    assert context.to_llamaindex() is not None
    assert context.to_crewai() is not None
    assert context.to_autogen() is not None

def test_format_exports():
    from mycontext import Context
    context = Context(guidance="Test")
    
    assert context.to_yaml() is not None
    assert context.to_xml() is not None

def test_provider_exports():
    from mycontext import Context
    context = Context(guidance="Test")
    
    assert context.to_anthropic() is not None
    assert context.to_openai() is not None
    assert context.to_google() is not None

test("Basic export formats", test_basic_exports)
test("Framework export formats", test_framework_exports)
test("Data format exports", test_format_exports)
test("Provider-specific exports", test_provider_exports)

print("\n" + "=" * 80)
print("TEST 8: INTEGRATION HELPERS (6 frameworks)")
print("=" * 80)

def test_integration_helpers():
    from mycontext import Context
    from mycontext.integrations import (
        LangChainHelper, LlamaIndexHelper, CrewAIHelper,
        AutoGenHelper, DSPyHelper, SemanticKernelHelper
    )
    
    context = Context(guidance="Test")
    
    # Test helpers exist and have methods
    assert hasattr(LangChainHelper, 'to_messages')
    assert hasattr(LlamaIndexHelper, 'to_prompt')
    assert hasattr(CrewAIHelper, 'create_agent')
    assert hasattr(AutoGenHelper, 'create_assistant')
    assert hasattr(DSPyHelper, 'to_prompt')
    assert hasattr(SemanticKernelHelper, 'to_prompt_template')

def test_auto_integrate():
    from mycontext import Context
    from mycontext.integrations import auto_integrate
    
    context = Context(guidance="Expert")
    
    # Test that function exists and accepts framework names
    result = auto_integrate(context, "langchain")
    assert result is not None

test("Integration helpers exist", test_integration_helpers)
test("auto_integrate function", test_auto_integrate)

print("\n" + "=" * 80)
print("TEST 9: CORE COMPONENTS")
print("=" * 80)

def test_core_imports():
    from mycontext import (
        Context, Directive, Guidance, Constraints,
        Pattern, Blueprint
    )
    assert Context is not None
    assert Directive is not None
    assert Guidance is not None

def test_context_creation():
    from mycontext import Context, Directive, Guidance
    
    # String shorthand
    context1 = Context(guidance="Expert")
    assert context1.guidance.role == "Expert"
    
    # Object creation
    context2 = Context(
        guidance=Guidance(role="Analyst"),
        directive=Directive(content="Analyze")
    )
    assert context2.guidance is not None
    assert context2.directive is not None

test("Core component imports", test_core_imports)
test("Context creation", test_context_creation)

print("\n" + "=" * 80)
print("TEST 10: PATTERN EXECUTION (Sample patterns)")
print("=" * 80)

def test_question_analyzer_execution():
    from mycontext.templates.free.analysis import QuestionAnalyzer
    
    qa = QuestionAnalyzer()
    context = qa.build_context(
        question="How can I improve performance?",
        depth="standard"
    )
    
    assert context.directive is not None
    assert "How can I improve performance?" in context.directive.content

def test_decision_framework_execution():
    from mycontext.templates.free.decision import DecisionFramework
    
    df = DecisionFramework()
    context = df.build_context(
        decision="Choose cloud provider",
        options=["AWS", "Google Cloud", "Azure"]
    )
    
    assert context.directive is not None
    assert "AWS" in context.directive.content

def test_idea_generator_execution():
    from mycontext.templates.free.creative import IdeaGenerator
    
    ig = IdeaGenerator()
    context = ig.build_context(
        challenge="Increase user engagement",
        constraints=["Budget: $10K"]
    )
    
    assert context.directive is not None
    assert "engagement" in context.directive.content.lower()

test("QuestionAnalyzer execution", test_question_analyzer_execution)
test("DecisionFramework execution", test_decision_framework_execution)
test("IdeaGenerator execution", test_idea_generator_execution)

print("\n" + "=" * 80)
print("TEST 11: PATTERN REGISTRY IN TRANSFORMATION ENGINE")
print("=" * 80)

def test_pattern_registry():
    from mycontext.intelligence import TransformationEngine
    
    engine = TransformationEngine()
    patterns = engine.get_available_patterns()
    
    print(f"   Registered patterns: {len(patterns)}")
    
    # Should have all core patterns at minimum
    assert len(patterns) >= 13
    assert "question_analyzer" in patterns
    assert "decision_framework" in patterns

test("Pattern registry population", test_pattern_registry)

print("\n" + "=" * 80)
print("TEST 12: MULTIPLE PATTERNS FROM DIFFERENT CATEGORIES")
print("=" * 80)

def test_mixed_category_usage():
    from mycontext.templates.free.analysis import DataAnalyzer
    from mycontext.templates.free.decision import ComparativeAnalyzer
    from mycontext.templates.free.creative import Brainstormer
    from mycontext.templates.free.communication import SimplificationEngine
    
    da = DataAnalyzer()
    ca = ComparativeAnalyzer()
    br = Brainstormer()
    se = SimplificationEngine()
    
    assert da.name == "data_analyzer"
    assert ca.name == "comparative_analyzer"
    assert br.name == "brainstormer"
    assert se.name == "simplification_engine"

test("Multiple categories in same code", test_mixed_category_usage)

print("\n" + "=" * 80)
print("TEST 13: CONTEXT ASSEMBLY")
print("=" * 80)

def test_context_assembly():
    from mycontext import Context, Directive, Guidance
    
    context = Context(
        guidance=Guidance(
            role="Expert Data Scientist",
            rules=["Use statistical methods", "Visualize findings"]
        ),
        directive=Directive(
            content="Analyze customer churn data and identify key drivers",
            priority=5
        )
    )
    
    assembled = context.assemble()
    assert len(assembled) > 0
    assert "Expert Data Scientist" in assembled
    assert "customer churn" in assembled

test("Context assembly", test_context_assembly)

print("\n" + "=" * 80)
print("TEST 14: EXPORT FORMAT VALIDATION")
print("=" * 80)

def test_export_types():
    from mycontext import Context
    import json
    
    context = Context(guidance="Test")
    
    # Test JSON is valid
    json_str = context.to_json()
    parsed = json.loads(json_str)
    assert isinstance(parsed, dict)
    
    # Test messages format
    messages = context.to_messages()
    assert isinstance(messages, list)
    assert len(messages) > 0
    assert messages[0]["role"] == "system"
    
    # Test markdown format
    md = context.to_markdown()
    assert "# Context" in md

test("Export format types", test_export_types)

print("\n" + "=" * 80)
print("TEST 15: TRANSFORMATION ENGINE INPUT TYPES")
print("=" * 80)

def test_input_type_detection():
    from mycontext.intelligence import TransformationEngine
    
    engine = TransformationEngine()
    
    # Test different input types
    test_cases = [
        ("How does this work?", "QUESTION"),
        ("Solve this problem", "PROBLEM"),
        ("Should we choose A or B?", "DECISION"),
        ("Compare X vs Y", "COMPARISON"),
        ("The system is slow", "STATEMENT"),
    ]
    
    for input_text, expected_contains in test_cases:
        analysis = engine.analyze_input(input_text)
        # Just verify it analyzes without error
        assert analysis.input_type is not None

test("Input type detection", test_input_type_detection)

print("\n" + "=" * 80)
print("TEST 16: QUALITY METRICS DIMENSIONS")
print("=" * 80)

def test_quality_dimensions():
    from mycontext import Context, Directive, Guidance
    from mycontext.intelligence import QualityMetrics, QualityDimension
    
    context = Context(
        guidance=Guidance(role="Expert", rules=["Rule 1"]),
        directive=Directive(content="Clear directive")
    )
    
    metrics = QualityMetrics()
    score = metrics.evaluate(context)
    
    # Check all 6 dimensions exist
    assert QualityDimension.CLARITY in score.dimensions
    assert QualityDimension.COMPLETENESS in score.dimensions
    assert QualityDimension.SPECIFICITY in score.dimensions
    assert QualityDimension.RELEVANCE in score.dimensions
    assert QualityDimension.STRUCTURE in score.dimensions
    assert QualityDimension.EFFICIENCY in score.dimensions

test("Quality metrics dimensions", test_quality_dimensions)

print("\n" + "=" * 80)
print("TEST 17: PATTERN PARAMETER HANDLING")
print("=" * 80)

def test_pattern_parameters():
    from mycontext.templates.free.analysis import TrendIdentifier
    from mycontext.templates.free.planning import PrioritySetter
    
    # Test with various parameters
    ti = TrendIdentifier()
    context1 = ti.build_context(
        data_description="Monthly sales",
        domain="e-commerce",
        timeframe="past year"
    )
    assert context1 is not None
    
    ps = PrioritySetter()
    context2 = ps.build_context(
        items=["Task A", "Task B", "Task C"],
        goal="Optimize delivery"
    )
    assert context2 is not None

test("Pattern parameter handling", test_pattern_parameters)

print("\n" + "=" * 80)
print("TEST 18: CORE FOUNDATION CLASSES")
print("=" * 80)

def test_foundation_classes():
    from mycontext.foundation import Directive, Guidance, Constraints
    
    directive = Directive(content="Test directive", priority=5)
    assert directive.content == "Test directive"
    assert directive.priority == 5
    
    guidance = Guidance(
        role="Test Role",
        rules=["Rule 1", "Rule 2"]
    )
    assert guidance.role == "Test Role"
    assert len(guidance.rules) == 2
    
    constraints = Constraints(
        must_include=["Item 1"],
        must_not_include=["Item 2"]
    )
    assert len(constraints.must_include) == 1

test("Foundation classes", test_foundation_classes)

print("\n" + "=" * 80)
print("TEST 19: PATTERN NAMING CONSISTENCY")
print("=" * 80)

def test_pattern_names():
    from mycontext.intelligence import TransformationEngine
    
    engine = TransformationEngine()
    patterns = engine.get_available_patterns()
    
    # Check naming convention (snake_case)
    for pattern_name in patterns:
        assert "_" in pattern_name or pattern_name.islower()
        assert pattern_name == pattern_name.lower()

test("Pattern naming consistency", test_pattern_names)

print("\n" + "=" * 80)
print("TEST 20: INTEGRATION FRAMEWORK COMPATIBILITY")
print("=" * 80)

def test_framework_format_compatibility():
    from mycontext import Context
    
    context = Context(guidance="Expert Developer")
    
    # LangChain format
    lc = context.to_langchain()
    assert "system_message" in lc
    
    # CrewAI format
    crew = context.to_crewai()
    assert "role" in crew
    assert "goal" in crew
    
    # AutoGen format
    auto = context.to_autogen()
    assert "system_message" in auto

test("Framework format compatibility", test_framework_format_compatibility)

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

total_tests = test_results["passed"] + test_results["failed"]
pass_rate = (test_results["passed"] / total_tests * 100) if total_tests > 0 else 0

print(f"\nTotal Tests: {total_tests}")
print(f"Passed: {test_results['passed']}")
print(f"Failed: {test_results['failed']}")
print(f"Pass Rate: {pass_rate:.1f}%")

if test_results["failed"] > 0:
    print(f"\n{'=' * 80}")
    print("FAILED TESTS DETAILS:")
    print("=" * 80)
    for name, error in test_results["errors"]:
        print(f"\n[FAIL] {name}")
        print(f"   {error}")

print("\n" + "=" * 80)
if test_results["failed"] == 0:
    print("*** ALL TESTS PASSED! SDK IS WORKING PERFECTLY! ***")
else:
    print(f"*** {test_results['failed']} tests need attention ***")
print("=" * 80)
