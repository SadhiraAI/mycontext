"""
mycontext - Revolutionary context engineering for LLM applications

Context as Code™ - Treat context with the same rigor as application code
"""

__version__ = "0.1.0"

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
]
