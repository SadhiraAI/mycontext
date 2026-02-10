"""Specialized Patterns - Domain-specific and unique patterns"""

from .code_reviewer import CodeReviewer
from .content_outliner import ContentOutliner
from .socratic_questioner import SocraticQuestioner
from .intent_recognizer import IntentRecognizer
from .ambiguity_resolver import AmbiguityResolver
from .risk_assessor import RiskAssessor
from .risk_mitigator import RiskMitigator
from .impact_assessor import ImpactAssessor
from .conflict_resolver import ConflictResolver
from .concept_explainer import ConceptExplainer
from .synthesis_builder import SynthesisBuilder

__all__ = [
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
