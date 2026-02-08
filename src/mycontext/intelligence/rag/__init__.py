"""
RAG System - Retrieval-Augmented Generation for mycontext SDK.

This module provides a complete RAG pipeline including:
- Document chunking (fixed, semantic, recursive, markdown)
- Embeddings (OpenAI, Sentence Transformers)
- Vector stores (in-memory, FAISS)
- Retrieval with reranking

Quick Start:
    >>> from mycontext.intelligence.rag import create_retriever
    >>> 
    >>> # Create retriever with documents
    >>> retriever = create_retriever(
    ...     documents=["Document 1...", "Document 2..."],
    ...     embedder="sentence-transformers",  # Free, local
    ...     vector_store="memory"
    ... )
    >>> 
    >>> # Retrieve relevant chunks
    >>> results = retriever.retrieve("What is Python?", k=5)
    >>> 
    >>> # Build context for LLM
    >>> context = retriever.build_context("What is Python?", k=3)

Advanced Usage:
    >>> from mycontext.intelligence.rag import (
    ...     Retriever,
    ...     SemanticChunker,
    ...     get_embedder,
    ...     create_vector_store
    ... )
    >>> 
    >>> # Custom configuration
    >>> chunker = SemanticChunker(chunk_size=1000)
    >>> embedder = get_embedder("sentence-transformers", model="all-MiniLM-L6-v2")
    >>> vector_store = create_vector_store("faiss", dimension=384)
    >>> 
    >>> retriever = Retriever(
    ...     embedder=embedder,
    ...     vector_store=vector_store,
    ...     chunker=chunker
    ... )
"""

# Chunking
from .chunker import (
    Chunk,
    ChunkingStrategy,
    FixedSizeChunker,
    SemanticChunker,
    RecursiveChunker,
    MarkdownChunker,
    chunk_text,
)

# Embeddings
from .embedder import (
    Embedder,
    OpenAIEmbedder,
    SentenceTransformerEmbedder,
    CachedEmbedder,
    BatchEmbedder,
    get_embedder,
    cosine_similarity,
    batch_cosine_similarity,
)

# Vector Stores
from .vector_store import (
    SearchResult,
    VectorStore,
    InMemoryVectorStore,
    FAISSVectorStore,
    create_vector_store,
)

# Retrieval
from .retriever import (
    RetrievalResult,
    Retriever,
    create_retriever,
)

__all__ = [
    # Chunking
    "Chunk",
    "ChunkingStrategy",
    "FixedSizeChunker",
    "SemanticChunker",
    "RecursiveChunker",
    "MarkdownChunker",
    "chunk_text",
    
    # Embeddings
    "Embedder",
    "OpenAIEmbedder",
    "SentenceTransformerEmbedder",
    "CachedEmbedder",
    "BatchEmbedder",
    "get_embedder",
    "cosine_similarity",
    "batch_cosine_similarity",
    
    # Vector Stores
    "SearchResult",
    "VectorStore",
    "InMemoryVectorStore",
    "FAISSVectorStore",
    "create_vector_store",
    
    # Retrieval
    "RetrievalResult",
    "Retriever",
    "create_retriever",
]
