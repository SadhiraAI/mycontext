"""
Intelligence Layer - Advanced AI capabilities for mycontext SDK.

This layer provides:
- RAG (Retrieval-Augmented Generation) - Knowledge as Code™

Quick Start - RAG:
    >>> from mycontext.intelligence.rag import create_retriever
    >>> 
    >>> retriever = create_retriever(
    ...     documents=["Doc 1", "Doc 2"],
    ...     embedder="sentence-transformers"
    ... )
    >>> 
    >>> results = retriever.retrieve("query", k=5)

Note: For agent orchestration examples, see examples/reference_implementations/
      mycontext focuses on context engineering, not agent frameworks.
"""

# RAG System
from . import rag

__all__ = [
    "rag",
]
