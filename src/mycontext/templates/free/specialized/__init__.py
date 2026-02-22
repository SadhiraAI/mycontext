"""Specialized Patterns - Domain-specific and unique patterns"""
from .code_reviewer import CodeReviewer
from .socratic_questioner import SocraticQuestioner
from .intent_recognizer import IntentRecognizer
from .risk_assessor import RiskAssessor
from .conflict_resolver import ConflictResolver
from .synthesis_builder import SynthesisBuilder

__all__ = [
    "CodeReviewer",
    "SocraticQuestioner",
    "IntentRecognizer",
    "RiskAssessor",
    "ConflictResolver",
    "SynthesisBuilder",
]
