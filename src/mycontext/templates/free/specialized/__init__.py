"""Specialized Patterns - Domain-specific and unique patterns"""
from .code_reviewer import CodeReviewer
from .conflict_resolver import ConflictResolver
from .intent_recognizer import IntentRecognizer
from .risk_assessor import RiskAssessor
from .socratic_questioner import SocraticQuestioner
from .synthesis_builder import SynthesisBuilder

__all__ = [
    "CodeReviewer",
    "ConflictResolver",
    "IntentRecognizer",
    "RiskAssessor",
    "SocraticQuestioner",
    "SynthesisBuilder",
]
