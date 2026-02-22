"""
Free Templates - Open source cognitive tools for context engineering.

Free Edition: 16 patterns across 6 categories.

Categories:
- analysis: QuestionAnalyzer, DataAnalyzer (2)
- reasoning: StepByStepReasoner, RootCauseAnalyzer, HypothesisGenerator (3)
- creative: Brainstormer (1)
- communication: AudienceAdapter, TechnicalTranslator (2)
- planning: ScenarioPlanner, StakeholderMapper (2)
- specialized: CodeReviewer, SocraticQuestioner, IntentRecognizer, RiskAssessor, ConflictResolver, SynthesisBuilder (6)
"""

from .analysis import (
    QuestionAnalyzer,
    DataAnalyzer,
)

from .reasoning import (
    StepByStepReasoner,
    RootCauseAnalyzer,
    HypothesisGenerator,
)

from .creative import Brainstormer

from .communication import (
    AudienceAdapter,
    TechnicalTranslator,
)

from .planning import (
    ScenarioPlanner,
    StakeholderMapper,
)

from .specialized import (
    CodeReviewer,
    SocraticQuestioner,
    IntentRecognizer,
    RiskAssessor,
    ConflictResolver,
    SynthesisBuilder,
)

__all__ = [
    "QuestionAnalyzer",
    "DataAnalyzer",
    "StepByStepReasoner",
    "RootCauseAnalyzer",
    "HypothesisGenerator",
    "Brainstormer",
    "AudienceAdapter",
    "TechnicalTranslator",
    "ScenarioPlanner",
    "StakeholderMapper",
    "CodeReviewer",
    "SocraticQuestioner",
    "IntentRecognizer",
    "RiskAssessor",
    "ConflictResolver",
    "SynthesisBuilder",
]
