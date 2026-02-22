"""
mycontext - Universal Context Transformation Engine

Transform raw questions into perfect, portable contexts for any AI system.

Context as Code™ - Research-backed cognitive patterns for systematic context engineering.
"""

__version__ = "0.3.0"

# Core exports
from .core import Context
from .foundation import Directive, Guidance, Constraints
from .structure import Pattern, Blueprint

# Provider exports
from .providers import (
    get_provider,
    register_provider,
    list_providers,
)

# Templates module (lazy loading)
from . import templates

# Utilities module (lazy loading)
from . import utils

# Intelligence module (lazy loading)
from . import intelligence
from .intelligence import transform
from .intelligence import TemplateIntegratorAgent, IntegrationResult
from .intelligence import OutputEvaluator, OutputQualityScore, OutputDimension
from .intelligence import ContextAmplificationIndex, CAIResult
from .intelligence import TemplateBenchmark, BenchmarkResult

# Integrations module (lazy loading)
from . import integrations

# Licensing
from .license import activate_license, deactivate_license, is_enterprise_active

# Agent Skills (executable, quality-assured, pattern-anchored skills)
from . import skills
from .skills import Skill, SkillRunner, SkillRunResult
__all__ = [
    # Core
    "Context",
    "Directive",
    "Guidance",
    "Constraints",
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
    # Skills
    "skills",
    "Skill",
    "SkillRunner",
    "SkillRunResult",
]
