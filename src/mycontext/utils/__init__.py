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
]
