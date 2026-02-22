"""
Learning & Knowledge Building Patterns (Enterprise)

5 patterns for scaffolding, spaced repetition, and cognitive load management.
Based on Vygotsky (1978), Ebbinghaus (1885), Sweller (1988).

License: Enterprise
"""

from .cognitive_load_manager import CognitiveLoadManager
from .conceptual_change_analyzer import ConceptualChangeAnalyzer
from .scaffolding_framework import ScaffoldingFramework
from .spaced_repetition_optimizer import SpacedRepetitionOptimizer
from .zone_of_proximal_development import ZoneOfProximalDevelopment

__all__ = [
    "ScaffoldingFramework",
    "SpacedRepetitionOptimizer",
    "ZoneOfProximalDevelopment",
    "CognitiveLoadManager",
    "ConceptualChangeAnalyzer",
]
