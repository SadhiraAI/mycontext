"""
Embeddings - Generate vector embeddings for text chunks.

Supports multiple embedding providers with consistent interface.
"""

from typing import List, Optional, Protocol
from abc import ABC, abstractmethod
import numpy as np


class Embedder(ABC):
    """Base class for embedding providers."""
    
    @abstractmethod
    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        pass
    
    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            numpy array of shape (embedding_dim,)
        """
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension."""
        pass


class OpenAIEmbedder(Embedder):
    """
    OpenAI embeddings (text-embedding-3-small, text-embedding-3-large).
    
    Examples:
        >>> embedder = OpenAIEmbedder(model="text-embedding-3-small")
        >>> embeddings = embedder.embed(["Hello", "World"])
        >>> print(embeddings.shape)  # (2, 1536)
    """
    
    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """
        Initialize OpenAI embedder.
        
        Args:
            model: Model name ("text-embedding-3-small" or "text-embedding-3-large")
            api_key: Optional API key (defaults to OPENAI_API_KEY env var)
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. "
                "Install with: pip install mycontext[openai]"
            )
        
        self.model = model
        self.client = OpenAI(api_key=api_key)
        
        # Model dimensions
        self._dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        
        embeddings = [item.embedding for item in response.data]
        return np.array(embeddings)
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for query."""
        return self.embed([query])[0]
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dimensions.get(self.model, 1536)


class SentenceTransformerEmbedder(Embedder):
    """
    Sentence Transformers embeddings (local, free).
    
    Popular models:
    - all-MiniLM-L6-v2 (384 dims, fast, good quality)
    - all-mpnet-base-v2 (768 dims, best quality)
    - multi-qa-mpnet-base-dot-v1 (768 dims, optimized for QA)
    
    Examples:
        >>> embedder = SentenceTransformerEmbedder("all-MiniLM-L6-v2")
        >>> embeddings = embedder.embed(["Hello", "World"])
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize Sentence Transformer embedder.
        
        Args:
            model_name: Model name from Sentence Transformers
            device: Device to use ("cuda", "cpu", or None for auto)
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )
        
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=device)
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for query."""
        return self.embed([query])[0]
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self.model.get_sentence_embedding_dimension()


class CachedEmbedder(Embedder):
    """
    Wrapper that caches embeddings to avoid recomputation.
    
    Examples:
        >>> base_embedder = OpenAIEmbedder()
        >>> embedder = CachedEmbedder(base_embedder, max_cache_size=1000)
        >>> 
        >>> # First call - computes embedding
        >>> emb1 = embedder.embed_query("Hello")
        >>> 
        >>> # Second call - returns cached
        >>> emb2 = embedder.embed_query("Hello")  # Instant!
    """
    
    def __init__(
        self,
        embedder: Embedder,
        max_cache_size: int = 10000
    ):
        """
        Initialize cached embedder.
        
        Args:
            embedder: Base embedder to wrap
            max_cache_size: Maximum cache entries
        """
        self.embedder = embedder
        self.max_cache_size = max_cache_size
        self._cache = {}
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings with caching."""
        # Check which texts are cached
        cached_indices = []
        uncached_texts = []
        uncached_indices = []
        
        for i, text in enumerate(texts):
            if text in self._cache:
                cached_indices.append(i)
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # Get uncached embeddings
        if uncached_texts:
            new_embeddings = self.embedder.embed(uncached_texts)
            
            # Cache them
            for text, embedding in zip(uncached_texts, new_embeddings):
                if len(self._cache) < self.max_cache_size:
                    self._cache[text] = embedding
        
        # Reconstruct full array
        result = np.zeros((len(texts), self.dimension))
        
        # Fill cached
        for i in cached_indices:
            result[i] = self._cache[texts[i]]
        
        # Fill uncached
        if uncached_texts:
            for i, orig_i in enumerate(uncached_indices):
                result[orig_i] = new_embeddings[i]
        
        return result
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for query with caching."""
        if query in self._cache:
            return self._cache[query]
        
        embedding = self.embedder.embed_query(query)
        
        if len(self._cache) < self.max_cache_size:
            self._cache[query] = embedding
        
        return embedding
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self.embedder.dimension
    
    def clear_cache(self):
        """Clear embedding cache."""
        self._cache.clear()
    
    def cache_stats(self) -> dict:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "max_size": self.max_cache_size,
            "usage": len(self._cache) / self.max_cache_size * 100
        }


class BatchEmbedder:
    """
    Utility for efficient batch embedding of large text collections.
    
    Examples:
        >>> embedder = OpenAIEmbedder()
        >>> batch_embedder = BatchEmbedder(embedder, batch_size=100)
        >>> 
        >>> texts = ["text"] * 10000
        >>> embeddings = batch_embedder.embed_all(texts, show_progress=True)
    """
    
    def __init__(
        self,
        embedder: Embedder,
        batch_size: int = 100
    ):
        """
        Initialize batch embedder.
        
        Args:
            embedder: Base embedder
            batch_size: Batch size for processing
        """
        self.embedder = embedder
        self.batch_size = batch_size
    
    def embed_all(
        self,
        texts: List[str],
        show_progress: bool = False
    ) -> np.ndarray:
        """
        Embed all texts in batches.
        
        Args:
            texts: List of texts to embed
            show_progress: Show progress bar
            
        Returns:
            Embeddings array
        """
        embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_embeddings = self.embedder.embed(batch)
            embeddings.append(batch_embeddings)
            
            if show_progress:
                progress = (i + len(batch)) / len(texts) * 100
                print(f"\rEmbedding progress: {progress:.1f}%", end="")
        
        if show_progress:
            print()  # New line
        
        return np.vstack(embeddings)


# Convenience function

def get_embedder(
    provider: str = "sentence-transformers",
    model: Optional[str] = None,
    **kwargs
) -> Embedder:
    """
    Get embedder by provider name.
    
    Args:
        provider: Provider name ("openai", "sentence-transformers")
        model: Optional model name
        **kwargs: Additional provider-specific arguments
        
    Returns:
        Embedder instance
        
    Examples:
        >>> # OpenAI
        >>> embedder = get_embedder("openai", model="text-embedding-3-small")
        >>> 
        >>> # Sentence Transformers (local, free)
        >>> embedder = get_embedder("sentence-transformers", model="all-MiniLM-L6-v2")
    """
    if provider == "openai":
        model = model or "text-embedding-3-small"
        return OpenAIEmbedder(model=model, **kwargs)
    
    elif provider == "sentence-transformers":
        model = model or "all-MiniLM-L6-v2"
        return SentenceTransformerEmbedder(model_name=model, **kwargs)
    
    else:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Choose from: 'openai', 'sentence-transformers'"
        )


# Similarity functions

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity (0-1)
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def batch_cosine_similarity(query: np.ndarray, embeddings: np.ndarray) -> np.ndarray:
    """
    Calculate cosine similarity between query and multiple embeddings.
    
    Args:
        query: Query vector of shape (embedding_dim,)
        embeddings: Embeddings array of shape (n, embedding_dim)
        
    Returns:
        Similarity scores of shape (n,)
    """
    # Normalize
    query_norm = query / np.linalg.norm(query)
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    # Dot product
    similarities = np.dot(embeddings_norm, query_norm)
    
    return similarities
