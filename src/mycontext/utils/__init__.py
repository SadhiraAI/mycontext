"""
Utilities Module - Essential tools for context engineering.

This module provides production-ready utilities for:
- Structured output generation (JSON, Pydantic models)
- Output parsing and validation
- Token optimization
- Batch processing
"""

from .batch import (
    BatchProcessor,
    BatchResult,
)
from .optimizers import (
    ContextCompressor,
    RedundancyRemover,
    TokenOptimizer,
)
from .parsers import (
    CodeBlockParser,
    JSONParser,
    ListParser,
    MarkdownParser,
    OutputParser,
    XMLParser,
)
from .structured_output import (
    JSONOutput,
    PydanticOutput,
    StructuredOutputMixin,
    output_format,
)
from .semantic_cache import SemanticCache, get_default_cache, reset_default_cache
from .template_safety import safe_format_template
from .tokens import count_tokens, estimate_cost_usd, fits_in_window, token_budget_remaining
from .tracing import Span, Tracer, get_tracer
from .validators import (
    ContextValidator,
    OutputValidator,
    SchemaValidator,
)

__all__ = [
    # Structured Output
    "StructuredOutputMixin",
    "JSONOutput",
    "PydanticOutput",
    "output_format",

    # Parsers
    "OutputParser",
    "JSONParser",
    "XMLParser",
    "ListParser",
    "CodeBlockParser",
    "MarkdownParser",

    # Optimizers
    "TokenOptimizer",
    "ContextCompressor",
    "RedundancyRemover",

    # Batch Processing
    "BatchProcessor",
    "BatchResult",

    # Validators
    "ContextValidator",
    "OutputValidator",
    "SchemaValidator",

    # Template Safety
    "safe_format_template",

    # Token Counting
    "count_tokens",
    "fits_in_window",
    "token_budget_remaining",
    "estimate_cost_usd",

    # Semantic Cache
    "SemanticCache",
    "get_default_cache",
    "reset_default_cache",

    # Tracing
    "Span",
    "Tracer",
    "get_tracer",
]
