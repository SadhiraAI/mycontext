"""
Metacognition Patterns (Enterprise) - "Thinking about thinking"

These patterns enable self-monitoring, self-regulation, and metacognitive awareness.
Critical for learning systems, tutoring applications, and skill development.

Research Foundation:
- Flavell, J. H. (1979). Metacognition and cognitive monitoring. American Psychologist, 34(10), 906-911.
- Zimmerman, B. J. (2002). Becoming a self-regulated learner. Theory Into Practice, 41(2), 64-70.
- Efklides, A. (2024). Revisiting the MASRL model. Educational Psychology Review, 36(1), Article 14.

License: Enterprise
Category: Metacognition (5 patterns)
"""

# Patterns implemented - ALL 5 COMPLETE
from .cognitive_strategy_selector import CognitiveStrategySelector
from .error_detection_framework import ErrorDetectionFramework
from .learning_from_experience import LearningFromExperience
from .metacognitive_monitor import MetacognitiveMonitor
from .self_regulation_framework import SelfRegulationFramework

__all__ = [
    "MetacognitiveMonitor",
    "SelfRegulationFramework",
    "CognitiveStrategySelector",
    "LearningFromExperience",
    "ErrorDetectionFramework",
]
