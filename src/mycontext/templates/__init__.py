"""
mycontext Templates - Pre-built context engineering templates.

This module provides production-ready templates built on mycontext SDK.
Free templates are available in the open-source edition.
Premium templates require a Pro license.
"""

from .free import (
    QuestionAnalyzer,
    CodeReviewer,
    StepByStepReasoner,
    ConceptExplainer,
    ContentOutliner,
)

__all__ = [
    # Free templates (open source)
    "QuestionAnalyzer",
    "CodeReviewer",
    "StepByStepReasoner",
    "ConceptExplainer",
    "ContentOutliner",
]
