"""
mycontext - Universal Context Transformation Engine

Transform raw questions into perfect, portable contexts for any AI system.

Context as Code™ - Research-backed cognitive patterns for systematic context engineering.
"""

from .version import __version__

# Core exports
# Templates module (lazy loading)
# Utilities module (lazy loading)
# Intelligence module (lazy loading)
# Integrations module (lazy loading)
# Agent Skills (executable, quality-assured, pattern-anchored skills)
from . import fragments, integrations, intelligence, rac, skills, templates, utils
from .core import THINKING_STRATEGIES, Context
from .foundation import Constraints, Directive, Guidance, TaskContract
from .intelligence import (
    BenchmarkResult,
    CAIResult,
    ContextAmplificationIndex,
    GeneratedContext,
    IntegrationResult,
    OutputDimension,
    OutputEvaluator,
    OutputQualityScore,
    TemplateBenchmark,
    TemplateIntegratorAgent,
    generate_context,
    transform,
)

# Licensing
from .license import activate_license, deactivate_license, is_enterprise_active

# Provider exports
from .providers import (
    get_provider,
    list_providers,
    register_provider,
)
from .skills import Skill, SkillRunner, SkillRunResult
from .structure import Blueprint, Pattern

__all__ = [
    "__version__",
    # Core
    "Context",
    "THINKING_STRATEGIES",
    "Directive",
    "Guidance",
    "Constraints",
    "TaskContract",
    # Structure
    "Pattern",
    "Blueprint",
    # Providers
    "get_provider",
    "register_provider",
    "list_providers",
    # Templates
    "templates",
    # Utilities
    "utils",
    # Intelligence
    "intelligence",
    "transform",
    "generate_context",
    "GeneratedContext",
    # Integrations
    "integrations",
    # Licensing
    "activate_license",
    "deactivate_license",
    "is_enterprise_active",
    # Evaluation
    "OutputEvaluator",
    "OutputQualityScore",
    "OutputDimension",
    "ContextAmplificationIndex",
    "CAIResult",
    "TemplateBenchmark",
    "BenchmarkResult",
    # Fragments
    "fragments",
    # Requirements-as-Code authoring + scoring bridge
    "rac",
    # Skills
    "skills",
    "Skill",
    "SkillRunner",
    "SkillRunResult",
]
