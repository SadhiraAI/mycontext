"""
Structure Layer - Composition and Patterns

This layer provides the tools to compose and structure contexts:
- Pattern: Reusable context templates (like functions)
- Blueprint: Multi-component context architectures
- Assembly: Dynamic context construction
"""

from .pattern import Pattern
from .blueprint import Blueprint

__all__ = ["Pattern", "Blueprint"]
