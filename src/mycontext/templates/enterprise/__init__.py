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

from .analysis import (
    AnomalyDetector,
    GapAnalyzer,
    SWOTAnalyzer,
    TrendIdentifier,
)
from .communication import (
    ClarityOptimizer,
    FeedbackComposer,
    NarrativeBuilder,
    PersuasionFramework,
    SimplificationEngine,
)
from .creative import (
    DesignThinker,
    IdeaGenerator,
    InnovationFramework,
    MetaphorGenerator,
)
from .decision import (
    ComparativeAnalyzer,
    CostBenefitAnalyzer,
    DecisionFramework,
    MultiObjectiveOptimizer,
    TradeoffAnalyzer,
)
from .diagnostic import (
    DiagnosticRootCauseAnalyzer,
    DifferentialDiagnoser,
    RootCauseAnalyzer,
    SystemHealthAuditor,
)
from .ethical_reasoning import (
    ConsequentialistAnalyzer,
    EthicalFrameworkAnalyzer,
    MoralDilemmaResolver,
    StakeholderEthicsAssessor,
    ValueConflictNavigator,
)
from .evaluation import (
    FormativeAssessmentFramework,
    PeerAssessmentStructure,
    RubricDesigner,
    SelfAssessmentGuide,
    SummativeEvaluator,
)
from .learning import (
    CognitiveLoadManager,
    ConceptualChangeAnalyzer,
    ScaffoldingFramework,
    SpacedRepetitionOptimizer,
    ZoneOfProximalDevelopment,
)
from .metacognition import (
    CognitiveStrategySelector,
    ErrorDetectionFramework,
    LearningFromExperience,
    MetacognitiveMonitor,
    SelfRegulationFramework,
)
from .planning import (
    DeadlineManager,
    PrioritySetter,
    ResourceAllocator,
)
from .problem_solving import (
    BottleneckIdentifier,
    ConstraintOptimizer,
    DependencyMapper,
    EfficiencyAnalyzer,
    ProblemDecomposer,
    TradeSpaceExplorer,
)
from .reasoning import (
    AnalogicalReasoner,
    CausalReasoner,
)
from .specialized import (
    AmbiguityResolver,
    ConceptExplainer,
    ContentOutliner,
    ImpactAssessor,
    RiskMitigator,
)
from .synthesis import (
    CrossDomainSynthesizer,
    HolisticIntegrator,
    PatternRecognitionEngine,
)
from .systems_thinking import (
    CausalLoopDiagrammer,
    EmergenceDetector,
    FeedbackLoopIdentifier,
    LeveragePointFinder,
    StockFlowAnalyzer,
    SystemArchetypeAnalyzer,
)
from .temporal import (
    FutureScenarioPlanner,
    HistoricalContextMapper,
    TemporalSequenceAnalyzer,
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
