"""
Foundation Layer - The base building blocks

This layer provides the fundamental primitives for context engineering:
- Directive: Single instruction units
- Guidance: System-level behavioral rules
- Constraints: Boundaries and guardrails
"""

from .directive import Directive
from .guidance import Guidance
from .constraints import Constraints

__all__ = ["Directive", "Guidance", "Constraints"]
