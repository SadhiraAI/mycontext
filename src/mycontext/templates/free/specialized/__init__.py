"""Specialized Patterns - Domain-specific and unique patterns"""
from .code_reviewer import CodeReviewer
from .conflict_resolver import ConflictResolver
from .intent_recognizer import IntentRecognizer
from .memory_compressor import MemoryCompressor
from .rag_answerer import RagAnswerer
from .risk_assessor import RiskAssessor
from .socratic_questioner import SocraticQuestioner
from .synthesis_builder import SynthesisBuilder

__all__ = [
    "CodeReviewer",
    "ConflictResolver",
    "IntentRecognizer",
    "MemoryCompressor",
    "RagAnswerer",
    "RiskAssessor",
    "SocraticQuestioner",
    "SynthesisBuilder",
]
