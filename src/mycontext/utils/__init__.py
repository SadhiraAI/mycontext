"""
Utilities Module - Essential tools for context engineering.

This module provides production-ready utilities for:
- Structured output generation (JSON, Pydantic models)
- Output parsing and validation
- Token optimization
- Batch processing
"""

from .structured_output import (
    StructuredOutputMixin,
    JSONOutput,
    PydanticOutput,
    output_format,
)

from .parsers import (
    OutputParser,
    JSONParser,
    XMLParser,
    ListParser,
    CodeBlockParser,
    MarkdownParser,
)

from .optimizers import (
    TokenOptimizer,
    ContextCompressor,
    RedundancyRemover,
)

from .batch import (
    BatchProcessor,
    BatchResult,
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
