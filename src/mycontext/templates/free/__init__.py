"""
Free Templates - Open source cognitive tools for context engineering.

Free Edition: 16 patterns across 6 categories.

Categories:
- analysis: QuestionAnalyzer, DataAnalyzer (2)
- reasoning: StepByStepReasoner, RootCauseAnalyzer, HypothesisGenerator (3)
- creative: Brainstormer (1)
- communication: AudienceAdapter, TechnicalTranslator (2)
- planning: ScenarioPlanner, StakeholderMapper (2)
- specialized: CodeReviewer, SocraticQuestioner, IntentRecognizer, RagAnswerer, RiskAssessor, ConflictResolver, SynthesisBuilder (7)
"""

from .analysis import (
    DataAnalyzer,
    QuestionAnalyzer,
)
from .communication import (
    AudienceAdapter,
    TechnicalTranslator,
)
from .creative import Brainstormer
from .planning import (
    ScenarioPlanner,
    StakeholderMapper,
)
from .reasoning import (
    HypothesisGenerator,
    RootCauseAnalyzer,
    StepByStepReasoner,
)
from .specialized import (
    CodeReviewer,
    ConflictResolver,
    IntentRecognizer,
    MemoryCompressor,
    RagAnswerer,
    RiskAssessor,
    SocraticQuestioner,
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
    "MemoryCompressor",
    "RagAnswerer",
    "RiskAssessor",
    "ConflictResolver",
    "SynthesisBuilder",
]
