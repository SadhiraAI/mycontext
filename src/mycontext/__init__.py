"""
mycontext - Universal Context Transformation Engine

Transform raw questions into perfect, portable contexts for any AI system.

Context as Code™ - Research-backed cognitive patterns for systematic context engineering.
"""

__version__ = "0.2.0"

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

# Knowledge exports
from .knowledge import (
    Session,
    Message,
    FileArchive,
    MemoryArchive,
)

# Templates module (lazy loading)
from . import templates

# Utilities module (lazy loading)
from . import utils

# Intelligence module (lazy loading)
from . import intelligence

# Integrations module (lazy loading)
from . import integrations

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
    # Knowledge
    "Session",
    "Message",
    "FileArchive",
    "MemoryArchive",
    # Templates
    "templates",
    # Utilities
    "utils",
    # Intelligence
    "intelligence",
    # Integrations
    "integrations",
]
