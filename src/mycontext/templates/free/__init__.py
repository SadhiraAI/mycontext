"""
Free Templates - Open source cognitive tools for context engineering.

These templates are part of the mycontext SDK Community Edition.
Based on research from IBM Zurich, Context-Engineering, and industry best practices.

🎉 50 PATTERNS COMPLETE - Organized by category! 🎉

Categories:
- analysis: Data, trends, gaps, SWOT (6 patterns)
- reasoning: Logic, causality, hypotheses (5 patterns)
- decision: Decision frameworks, comparisons, trade-offs (5 patterns)
- creative: Ideation, innovation, design thinking (5 patterns)
- communication: Clarity, persuasion, translation (7 patterns)
- planning: Scenarios, stakeholders, priorities (5 patterns)
- problem_solving: Decomposition, optimization, constraints (6 patterns)
- specialized: Domain-specific and unique patterns (11 patterns)

Usage:
    from mycontext.templates.free import QuestionAnalyzer  # Works as before
    from mycontext.templates.free.analysis import QuestionAnalyzer  # Category-specific import
    from mycontext.templates.free.decision import *  # All decision patterns
"""

# Import all patterns from category modules for backward compatibility
from .analysis import (
    QuestionAnalyzer,
    DataAnalyzer,
    TrendIdentifier,
    GapAnalyzer,
    SWOTAnalyzer,
    AnomalyDetector,
)

from .reasoning import (
    StepByStepReasoner,
    AnalogicalReasoner,
    CausalReasoner,
    RootCauseAnalyzer,
    HypothesisGenerator,
)

from .decision import (
    DecisionFramework,
    ComparativeAnalyzer,
    TradeoffAnalyzer,
    MultiObjectiveOptimizer,
    CostBenefitAnalyzer,
)

from .creative import (
    IdeaGenerator,
    Brainstormer,
    InnovationFramework,
    DesignThinker,
    MetaphorGenerator,
)

from .communication import (
    SimplificationEngine,
    ClarityOptimizer,
    AudienceAdapter,
    PersuasionFramework,
    NarrativeBuilder,
    TechnicalTranslator,
    FeedbackComposer,
)

from .planning import (
    ScenarioPlanner,
    StakeholderMapper,
    PrioritySetter,
    DeadlineManager,
    ResourceAllocator,
)

from .problem_solving import (
    ProblemDecomposer,
    BottleneckIdentifier,
    ConstraintOptimizer,
    DependencyMapper,
    EfficiencyAnalyzer,
    TradeSpaceExplorer,
)

from .specialized import (
    CodeReviewer,
    ContentOutliner,
    SocraticQuestioner,
    IntentRecognizer,
    AmbiguityResolver,
    RiskAssessor,
    RiskMitigator,
    ImpactAssessor,
    ConflictResolver,
    ConceptExplainer,
    SynthesisBuilder,
)

__all__ = [
    # Analysis (6)
    "QuestionAnalyzer",
    "DataAnalyzer",
    "TrendIdentifier",
    "GapAnalyzer",
    "SWOTAnalyzer",
    "AnomalyDetector",
    # Reasoning (5)
    "StepByStepReasoner",
    "AnalogicalReasoner",
    "CausalReasoner",
    "RootCauseAnalyzer",
    "HypothesisGenerator",
    # Decision (5)
    "DecisionFramework",
    "ComparativeAnalyzer",
    "TradeoffAnalyzer",
    "MultiObjectiveOptimizer",
    "CostBenefitAnalyzer",
    # Creative (5)
    "IdeaGenerator",
    "Brainstormer",
    "InnovationFramework",
    "DesignThinker",
    "MetaphorGenerator",
    # Communication (7)
    "SimplificationEngine",
    "ClarityOptimizer",
    "AudienceAdapter",
    "PersuasionFramework",
    "NarrativeBuilder",
    "TechnicalTranslator",
    "FeedbackComposer",
    # Planning (5)
    "ScenarioPlanner",
    "StakeholderMapper",
    "PrioritySetter",
    "DeadlineManager",
    "ResourceAllocator",
    # Problem Solving (6)
    "ProblemDecomposer",
    "BottleneckIdentifier",
    "ConstraintOptimizer",
    "DependencyMapper",
    "EfficiencyAnalyzer",
    "TradeSpaceExplorer",
    # Specialized (11)
    "CodeReviewer",
    "ContentOutliner",
    "SocraticQuestioner",
    "IntentRecognizer",
    "AmbiguityResolver",
    "RiskAssessor",
    "RiskMitigator",
    "ImpactAssessor",
    "ConflictResolver",
    "ConceptExplainer",
    "SynthesisBuilder",
]
