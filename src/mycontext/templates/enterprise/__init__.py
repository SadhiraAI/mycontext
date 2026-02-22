"""
mycontext Enterprise Templates - Advanced cognitive patterns for professional use.

**69 Enterprise Patterns** across 16 categories:
- Analysis (4): Trend, gap, SWOT, anomaly
- Reasoning (2): Analogical, causal
- Creative (4): Ideation, innovation, design thinking, metaphors
- Communication (5): Simplification, clarity, persuasion, narrative, feedback
- Planning (3): Priority, deadline, resource allocation
- Specialized (5): Content, ambiguity, risk mitigation, impact, concepts
- Decision (5): Decision framework, comparative, tradeoff, multi-objective, cost-benefit
- Problem Solving (6): Decomposition, bottleneck, constraint, dependency, efficiency, trade space
- Metacognition (5): Self-monitoring, self-regulation, learning
- Ethical Reasoning (5): Moral judgment, stakeholder analysis, values
- Systems Thinking (6): Feedback loops, leverage points, emergence
- Learning (5): Scaffolding, spaced repetition, ZPD, cognitive load
- Evaluation (5): Rubrics, formative/summative assessment, peer review
- Temporal (3): Sequence analysis, scenario planning, historical context
- Diagnostic (3): Root cause, differential diagnosis, system health
- Synthesis (3): Cross-domain synthesis, pattern recognition, holistic integration

License: Enterprise
"""

from .decision import (
    DecisionFramework,
    ComparativeAnalyzer,
    TradeoffAnalyzer,
    MultiObjectiveOptimizer,
    CostBenefitAnalyzer,
)

from .problem_solving import (
    ProblemDecomposer,
    BottleneckIdentifier,
    ConstraintOptimizer,
    DependencyMapper,
    EfficiencyAnalyzer,
    TradeSpaceExplorer,
)

from .metacognition import (
    MetacognitiveMonitor,
    SelfRegulationFramework,
    CognitiveStrategySelector,
    LearningFromExperience,
    ErrorDetectionFramework,
)

from .ethical_reasoning import (
    EthicalFrameworkAnalyzer,
    MoralDilemmaResolver,
    StakeholderEthicsAssessor,
    ValueConflictNavigator,
    ConsequentialistAnalyzer,
)

from .systems_thinking import (
    FeedbackLoopIdentifier,
    LeveragePointFinder,
    EmergenceDetector,
    SystemArchetypeAnalyzer,
    CausalLoopDiagrammer,
    StockFlowAnalyzer,
)

from .learning import (
    ScaffoldingFramework,
    SpacedRepetitionOptimizer,
    ZoneOfProximalDevelopment,
    CognitiveLoadManager,
    ConceptualChangeAnalyzer,
)

from .evaluation import (
    RubricDesigner,
    FormativeAssessmentFramework,
    SummativeEvaluator,
    PeerAssessmentStructure,
    SelfAssessmentGuide,
)

from .temporal import (
    TemporalSequenceAnalyzer,
    FutureScenarioPlanner,
    HistoricalContextMapper,
)

from .diagnostic import (
    DiagnosticRootCauseAnalyzer,
    RootCauseAnalyzer,
    DifferentialDiagnoser,
    SystemHealthAuditor,
)

from .synthesis import (
    CrossDomainSynthesizer,
    PatternRecognitionEngine,
    HolisticIntegrator,
)

from .analysis import (
    TrendIdentifier,
    GapAnalyzer,
    SWOTAnalyzer,
    AnomalyDetector,
)

from .reasoning import (
    AnalogicalReasoner,
    CausalReasoner,
)

from .creative import (
    IdeaGenerator,
    InnovationFramework,
    DesignThinker,
    MetaphorGenerator,
)

from .communication import (
    SimplificationEngine,
    ClarityOptimizer,
    PersuasionFramework,
    NarrativeBuilder,
    FeedbackComposer,
)

from .planning import (
    PrioritySetter,
    DeadlineManager,
    ResourceAllocator,
)

from .specialized import (
    ContentOutliner,
    AmbiguityResolver,
    RiskMitigator,
    ImpactAssessor,
    ConceptExplainer,
)

__all__ = [
    "DecisionFramework",
    "ComparativeAnalyzer",
    "TradeoffAnalyzer",
    "MultiObjectiveOptimizer",
    "CostBenefitAnalyzer",
    "ProblemDecomposer",
    "BottleneckIdentifier",
    "ConstraintOptimizer",
    "DependencyMapper",
    "EfficiencyAnalyzer",
    "TradeSpaceExplorer",
    "MetacognitiveMonitor",
    "SelfRegulationFramework",
    "CognitiveStrategySelector",
    "LearningFromExperience",
    "ErrorDetectionFramework",
    "EthicalFrameworkAnalyzer",
    "MoralDilemmaResolver",
    "StakeholderEthicsAssessor",
    "ValueConflictNavigator",
    "ConsequentialistAnalyzer",
    "FeedbackLoopIdentifier",
    "LeveragePointFinder",
    "EmergenceDetector",
    "SystemArchetypeAnalyzer",
    "CausalLoopDiagrammer",
    "StockFlowAnalyzer",
    "ScaffoldingFramework",
    "SpacedRepetitionOptimizer",
    "ZoneOfProximalDevelopment",
    "CognitiveLoadManager",
    "ConceptualChangeAnalyzer",
    "RubricDesigner",
    "FormativeAssessmentFramework",
    "SummativeEvaluator",
    "PeerAssessmentStructure",
    "SelfAssessmentGuide",
    "TemporalSequenceAnalyzer",
    "FutureScenarioPlanner",
    "HistoricalContextMapper",
    "DiagnosticRootCauseAnalyzer",
    "RootCauseAnalyzer",
    "DifferentialDiagnoser",
    "SystemHealthAuditor",
    "CrossDomainSynthesizer",
    "PatternRecognitionEngine",
    "HolisticIntegrator",
    "TrendIdentifier",
    "GapAnalyzer",
    "SWOTAnalyzer",
    "AnomalyDetector",
    "AnalogicalReasoner",
    "CausalReasoner",
    "IdeaGenerator",
    "InnovationFramework",
    "DesignThinker",
    "MetaphorGenerator",
    "SimplificationEngine",
    "ClarityOptimizer",
    "PersuasionFramework",
    "NarrativeBuilder",
    "FeedbackComposer",
    "PrioritySetter",
    "DeadlineManager",
    "ResourceAllocator",
    "ContentOutliner",
    "AmbiguityResolver",
    "RiskMitigator",
    "ImpactAssessor",
    "ConceptExplainer",
]
