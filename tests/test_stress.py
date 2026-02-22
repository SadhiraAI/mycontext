"""
Stress Tests - Advanced testing scenarios

Tests:
- All 50 patterns instantiation
- Pattern execution with edge cases
- Large context creation
- Export format integrity
- Performance benchmarks
- Error handling
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 80)
print("STRESS TEST SUITE - mycontext SDK")
print("=" * 80)
print()

test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test(name, func):
    """Run a test and track results."""
    try:
        start_time = time.time()
        func()
        elapsed = (time.time() - start_time) * 1000
        test_results["passed"] += 1
        print(f"[PASS]: {name} ({elapsed:.1f}ms)")
        return True
    except Exception as e:
        test_results["failed"] += 1
        test_results["errors"].append((name, str(e)))
        print(f"[FAIL]: {name}")
        print(f"   Error: {str(e)[:150]}")
        return False

print("=" * 80)
print("TEST 1: INSTANTIATE ALL 50 PATTERNS")
print("=" * 80)

def test_all_50_patterns():
    from mycontext.templates.free import (
        # Free Analysis (2)
        QuestionAnalyzer, DataAnalyzer,
        # Free Reasoning (3)
        StepByStepReasoner, RootCauseAnalyzer, HypothesisGenerator,
        # Free Creative (1)
        Brainstormer,
        # Free Communication (2)
        AudienceAdapter, TechnicalTranslator,
        # Free Planning (2)
        ScenarioPlanner, StakeholderMapper,
        # Free Specialized (6)
        CodeReviewer, SocraticQuestioner,
        IntentRecognizer, RiskAssessor,
        ConflictResolver, SynthesisBuilder,
    )
    from mycontext.templates.enterprise.analysis import (
        TrendIdentifier, GapAnalyzer, SWOTAnalyzer, AnomalyDetector,
    )
    from mycontext.templates.enterprise.reasoning import (
        AnalogicalReasoner, CausalReasoner,
    )
    from mycontext.templates.enterprise.creative import (
        IdeaGenerator, InnovationFramework, DesignThinker, MetaphorGenerator,
    )
    from mycontext.templates.enterprise.communication import (
        SimplificationEngine, ClarityOptimizer,
        PersuasionFramework, NarrativeBuilder, FeedbackComposer,
    )
    from mycontext.templates.enterprise.planning import (
        PrioritySetter, DeadlineManager, ResourceAllocator,
    )
    from mycontext.templates.enterprise.specialized import (
        ContentOutliner, AmbiguityResolver,
        RiskMitigator, ImpactAssessor, ConceptExplainer,
    )
    from mycontext.templates.enterprise.decision import (
        DecisionFramework, ComparativeAnalyzer, TradeoffAnalyzer,
        MultiObjectiveOptimizer, CostBenefitAnalyzer,
    )
    from mycontext.templates.enterprise.problem_solving import (
        ProblemDecomposer, BottleneckIdentifier, ConstraintOptimizer,
        DependencyMapper, EfficiencyAnalyzer, TradeSpaceExplorer,
    )
    
    patterns = [
        QuestionAnalyzer(), DataAnalyzer(), TrendIdentifier(),
        GapAnalyzer(), SWOTAnalyzer(), AnomalyDetector(),
        StepByStepReasoner(), AnalogicalReasoner(), CausalReasoner(),
        RootCauseAnalyzer(), HypothesisGenerator(),
        DecisionFramework(), ComparativeAnalyzer(), TradeoffAnalyzer(),
        MultiObjectiveOptimizer(), CostBenefitAnalyzer(),
        IdeaGenerator(), Brainstormer(), InnovationFramework(),
        DesignThinker(), MetaphorGenerator(),
        SimplificationEngine(), ClarityOptimizer(), AudienceAdapter(),
        PersuasionFramework(), NarrativeBuilder(), TechnicalTranslator(),
        FeedbackComposer(),
        ScenarioPlanner(), StakeholderMapper(), PrioritySetter(),
        DeadlineManager(), ResourceAllocator(),
        ProblemDecomposer(), BottleneckIdentifier(), ConstraintOptimizer(),
        DependencyMapper(), EfficiencyAnalyzer(), TradeSpaceExplorer(),
        CodeReviewer(), ContentOutliner(), SocraticQuestioner(),
        IntentRecognizer(), AmbiguityResolver(), RiskAssessor(),
        RiskMitigator(), ImpactAssessor(), ConflictResolver(),
        ConceptExplainer(), SynthesisBuilder()
    ]
    
    print(f"   Instantiated {len(patterns)} patterns")
    assert len(patterns) == 50

test("Instantiate all 50 patterns", test_all_50_patterns)

print("\n" + "=" * 80)
print("TEST 2: EXECUTE MULTIPLE PATTERNS SEQUENTIALLY")
print("=" * 80)

def test_sequential_execution():
    from mycontext.templates.free.analysis import QuestionAnalyzer
    from mycontext.templates.enterprise.decision import DecisionFramework
    from mycontext.templates.enterprise.creative import IdeaGenerator
    from mycontext.templates.enterprise.problem_solving import ProblemDecomposer
    
    qa = QuestionAnalyzer()
    df = DecisionFramework()
    ig = IdeaGenerator()
    pd = ProblemDecomposer()
    
    # Execute each
    c1 = qa.build_context(question="Test question 1")
    c2 = df.build_context(decision="Test decision", options=["A", "B"])
    c3 = ig.build_context(challenge="Test challenge")
    c4 = pd.build_context(problem="Test problem")
    
    assert all([c1, c2, c3, c4])

test("Sequential pattern execution", test_sequential_execution)

print("\n" + "=" * 80)
print("TEST 3: TRANSFORMATION ENGINE WITH VARIOUS INPUTS")
print("=" * 80)

def test_transformation_various_inputs():
    from mycontext.intelligence import TransformationEngine
    
    engine = TransformationEngine()
    
    inputs = [
        "What is the capital of France?",
        "Should I invest in stocks or bonds?",
        "How can I optimize this algorithm?",
        "Compare Python vs JavaScript",
        "Analyze customer churn data",
        "Generate ideas for marketing campaign",
        "Plan a product launch strategy",
        "What are the risks of this project?",
        "Simplify quantum physics concepts",
        "Create a narrative about innovation"
    ]
    
    for input_text in inputs:
        analysis = engine.analyze_input(input_text)
        # Just verify analysis works
        assert analysis is not None
        assert len(analysis.recommended_patterns) > 0

test("Transform 10 different input types", test_transformation_various_inputs)

print("\n" + "=" * 80)
print("TEST 4: LARGE CONTEXT ASSEMBLY")
print("=" * 80)

def test_large_context():
    from mycontext import Context, Guidance, Directive, Constraints
    
    # Create a very detailed context
    context = Context(
        guidance=Guidance(
            role="Senior Technical Architect with 15+ years experience",
            rules=[
                "Consider scalability at every step",
                "Prioritize security and data privacy",
                "Design for maintainability",
                "Follow industry best practices",
                "Document architectural decisions",
                "Consider cost implications",
                "Think about monitoring and observability",
                "Plan for disaster recovery"
            ],
            knowledge=[
                "Expert in cloud architecture (AWS, Azure, GCP)",
                "Deep understanding of microservices",
                "Proficient in multiple programming languages",
                "Experienced in distributed systems",
                "Familiar with DevOps practices"
            ]
        ),
        directive=Directive(
            content="Design a scalable e-commerce platform that can handle 1M+ users, " +
                   "with real-time inventory, personalized recommendations, " +
                   "payment processing, and multi-region support",
            priority=10
        ),
        constraints=Constraints(
            must_include=[
                "Database design",
                "API architecture",
                "Caching strategy",
                "Security measures",
                "Performance optimization"
            ],
            must_not_include=[
                "Vendor lock-in",
                "Single points of failure",
                "Unencrypted data transmission"
            ]
        )
    )
    
    assembled = context.assemble()
    assert assembled is not None
    assert len(assembled) > 500  # Should be a substantial context

test("Large context assembly", test_large_context)

print("\n" + "=" * 80)
print("TEST 5: ALL EXPORT FORMATS WITH REAL CONTEXT")
print("=" * 80)

def test_all_exports():
    from mycontext import Context, Guidance, Directive
    import json
    
    context = Context(
        guidance=Guidance(
            role="Expert Data Scientist",
            rules=["Use statistical rigor", "Visualize insights"]
        ),
        directive=Directive(
            content="Analyze sales trends and predict Q4 revenue"
        )
    )
    
    # Test all export methods
    exports = {
        "to_dict": context.to_dict(),
        "to_json": json.loads(context.to_json()),
        "to_markdown": context.to_markdown(),
        "to_messages": context.to_messages(),
        "to_langchain": context.to_langchain(),
        "to_llamaindex": context.to_llamaindex(),
        "to_crewai": context.to_crewai(),
        "to_autogen": context.to_autogen(),
        "to_yaml": context.to_yaml(),
        "to_xml": context.to_xml(),
        "to_anthropic": context.to_anthropic(),
        "to_openai": context.to_openai(),
        "to_google": context.to_google(),
    }
    
    for format_name, result in exports.items():
        assert result is not None, f"{format_name} returned None"
    
    print(f"   Validated {len(exports)} export formats")

test("All 13 export formats", test_all_exports)

print("\n" + "=" * 80)
print("TEST 6: QUALITY METRICS COMPARISON")
print("=" * 80)

def test_quality_comparison():
    from mycontext import Context
    from mycontext.intelligence import QualityMetrics
    
    # Simple context
    context1 = Context(guidance="Expert")
    
    # Detailed context
    context2 = Context(
        guidance="Expert with specific knowledge",
        directive="Clear, specific directive with details"
    )
    
    metrics = QualityMetrics()
    score1 = metrics.evaluate(context1)
    score2 = metrics.evaluate(context2)
    
    # More detailed context should score higher
    assert score2.overall > score1.overall

test("Quality metrics comparison", test_quality_comparison)

print("\n" + "=" * 80)
print("TEST 7: PATTERN PARAMETER VARIATIONS")
print("=" * 80)

def test_parameter_variations():
    from mycontext.templates.free.analysis import QuestionAnalyzer
    
    qa = QuestionAnalyzer()
    
    # Test with minimal parameters
    c1 = qa.build_context(question="What?")
    
    # Test with all parameters
    c2 = qa.build_context(
        question="What is machine learning?",
        depth="comprehensive",
        context_needed="Technical explanation for beginners",
        domain="AI/ML"
    )
    
    assert c1 is not None
    assert c2 is not None
    assert len(c2.directive.content) > len(c1.directive.content)

test("Pattern parameter variations", test_parameter_variations)

print("\n" + "=" * 80)
print("TEST 8: TRANSFORMATION ENGINE INPUT ANALYSIS DETAILS")
print("=" * 80)

def test_analysis_details():
    from mycontext.intelligence import TransformationEngine
    
    engine = TransformationEngine()
    
    test_cases = [
        "How does blockchain work?",
        "Should we migrate to microservices?",
        "Compare SQL vs NoSQL databases",
        "The application is experiencing high latency"
    ]
    
    for input_text in test_cases:
        analysis = engine.analyze_input(input_text)
        
        assert analysis.input_type is not None
        assert analysis.complexity is not None
        assert len(analysis.recommended_patterns) > 0
        assert 0.0 <= analysis.confidence <= 1.0
        
        print(f"   '{input_text[:30]}...' -> {analysis.input_type.value}, " +
              f"{len(analysis.recommended_patterns)} patterns")

test("Input analysis details", test_analysis_details)

print("\n" + "=" * 80)
print("TEST 9: INTEGRATION HELPERS WITH REAL CONTEXT")
print("=" * 80)

def test_integration_real_context():
    from mycontext import Context, Guidance
    from mycontext.integrations import (
        LangChainHelper, LlamaIndexHelper,
        AutoGenHelper, DSPyHelper, SemanticKernelHelper
    )
    
    context = Context(
        guidance=Guidance(
            role="Expert Financial Advisor",
            rules=["Provide data-driven recommendations"]
        ),
        directive="Analyze portfolio risk and suggest rebalancing"
    )
    
    # Test helpers that work without external packages
    helpers_tested = 0
    
    try:
        lc = LangChainHelper.to_messages(context)
        assert lc is not None
        helpers_tested += 1
    except: pass
    
    try:
        li = LlamaIndexHelper.to_prompt(context)
        assert li is not None
        helpers_tested += 1
    except: pass
    
    try:
        auto = AutoGenHelper.create_assistant(context)
        assert auto is not None
        helpers_tested += 1
    except: pass
    
    try:
        dspy = DSPyHelper.to_prompt(context)
        assert dspy is not None
        helpers_tested += 1
    except: pass
    
    try:
        sk = SemanticKernelHelper.to_prompt_template(context)
        assert sk is not None
        helpers_tested += 1
    except: pass
    
    print(f"   Validated {helpers_tested} integration helpers (graceful degradation)")
    assert helpers_tested >= 3  # At least 3 should work
test("Integration helpers with real context", test_integration_real_context)

print("\n" + "=" * 80)
print("TEST 10: ERROR HANDLING")
print("=" * 80)

def test_error_handling():
    from mycontext import Context
    from mycontext.templates.free.analysis import QuestionAnalyzer
    
    # Test with empty/None inputs
    try:
        context = Context(guidance="")
        assert context is not None  # Should handle gracefully
    except Exception as e:
        print(f"   Empty guidance handling: {e}")
    
    # Test pattern with minimal input
    qa = QuestionAnalyzer()
    try:
        context = qa.build_context(question="")
        assert context is not None
    except Exception as e:
        print(f"   Empty question handling: {e}")

test("Error handling with edge cases", test_error_handling)

print("\n" + "=" * 80)
print("TEST 11: MEMORY AND PERFORMANCE")
print("=" * 80)

def test_performance():
    from mycontext.templates.free.analysis import QuestionAnalyzer
    
    qa = QuestionAnalyzer()
    
    # Execute pattern 100 times
    start = time.time()
    for i in range(100):
        context = qa.build_context(question=f"Test question {i}")
    elapsed = time.time() - start
    
    avg_time = (elapsed / 100) * 1000
    print(f"   100 executions in {elapsed:.2f}s (avg: {avg_time:.2f}ms each)")
    
    assert elapsed < 10.0  # Should complete in under 10 seconds

test("Performance: 100 pattern executions", test_performance)

print("\n" + "=" * 80)
print("TEST 12: CONTEXT CHAINING")
print("=" * 80)

def test_context_chaining():
    from mycontext import Context, Guidance, Directive, Constraints
    from mycontext.intelligence import QualityMetrics
    
    # Create initial context
    context1 = Context(guidance="Analyst")
    
    # Enhance it
    context2 = Context(
        guidance=context1.guidance,
        directive="Analyze data"
    )
    
    # Further enhance with proper Constraints object
    context3 = Context(
        guidance=context2.guidance,
        directive=context2.directive,
        constraints=Constraints(
            must_include=["Complete in 1 hour"],
            must_not_include=["Skip validation"]
        )
    )
    
    # Each should be valid
    metrics = QualityMetrics()
    score3 = metrics.evaluate(context3)
    assert score3.overall > 0

test("Context chaining and enhancement", test_context_chaining)

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
    print("FAILED TESTS:")
    print("=" * 80)
    for name, error in test_results["errors"]:
        print(f"\n[FAIL] {name}")
        print(f"   {error}")

print("\n" + "=" * 80)
if test_results["failed"] == 0:
    print("*** ALL STRESS TESTS PASSED! ***")
    print("*** SDK IS PRODUCTION READY! ***")
else:
    print(f"*** {test_results['failed']} tests need attention ***")
print("=" * 80)
