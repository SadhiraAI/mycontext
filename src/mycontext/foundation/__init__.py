"""
Foundation Layer - The base building blocks

This layer provides the fundamental primitives for context engineering:
- Directive: Single instruction units
- Guidance: System-level behavioral rules
- Constraints: Boundaries and guardrails
- TaskContract: L0 metadata (domain, audience, genre, grounding)
"""

from .constraints import Constraints
from .directive import Directive
from .guidance import Guidance
from .task_contract import TaskContract

__all__ = ["Directive", "Guidance", "Constraints", "TaskContract"]
