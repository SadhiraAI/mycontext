"""
Vector Store - Store and retrieve embeddings efficiently.

Supports multiple backend implementations for different use cases.
"""

from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
import json
from pathlib import Path


@dataclass
class SearchResult:
    """
    Result from vector search.
    
    Attributes:
        text: Original text
        score: Similarity score
        index: Document index
        metadata: Document metadata
    """
    text: str
    score: float
    index: int
    metadata: Dict[str, Any]


class VectorStore(ABC):
    """Base class for vector stores."""
    
    @abstractmethod
    def add(
        self,
        texts: List[str],
        embeddings: np.ndarray,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Add documents to the store.
        
        Args:
            texts: Document texts
            embeddings: Document embeddings
            metadatas: Optional metadata for each document
        """
        pass
    
    @abstractmethod
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5
    ) -> List[SearchResult]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of search results sorted by similarity
        """
        pass
    
    @abstractmethod
    def delete(self, indices: List[int]):
        """
        Delete documents by index.
        
        Args:
            indices: Document indices to delete
        """
        pass
    
    @abstractmethod
    def clear(self):
        """Clear all documents from store."""
        pass
    
    @abstractmethod
    def __len__(self) -> int:
        """Return number of documents in store."""
        pass


class InMemoryVectorStore(VectorStore):
    """
    Simple in-memory vector store using numpy.
    
    Best for: Small datasets, testing, prototyping
    
    Examples:
        >>> store = InMemoryVectorStore()
        >>> store.add(texts=["Hello"], embeddings=np.array([[0.1, 0.2, ...]]))
        >>> results = store.search(query_embedding, k=5)
    """
    
    def __init__(self):
        """Initialize in-memory store."""
        self.texts: List[str] = []
        self.embeddings: Optional[np.ndarray] = None
        self.metadatas: List[Dict[str, Any]] = []
    
    def add(
        self,
        texts: List[str],
        embeddings: np.ndarray,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ):
        """Add documents to store."""
        self.texts.extend(texts)
        
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        self.metadatas.extend(metadatas)
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5
    ) -> List[SearchResult]:
        """Search for similar documents."""
        if self.embeddings is None or len(self.texts) == 0:
            return []
        
        # Calculate cosine similarity
        from .embedder import batch_cosine_similarity
        similarities = batch_cosine_similarity(query_embedding, self.embeddings)
        
        # Get top k
        k = min(k, len(self.texts))
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append(SearchResult(
                text=self.texts[idx],
                score=float(similarities[idx]),
                index=int(idx),
                metadata=self.metadatas[idx]
            ))
        
        return results
    
    def delete(self, indices: List[int]):
        """Delete documents by index."""
        # Convert to set for O(1) lookup
        to_delete = set(indices)
        
        # Filter texts and metadatas
        self.texts = [t for i, t in enumerate(self.texts) if i not in to_delete]
        self.metadatas = [m for i, m in enumerate(self.metadatas) if i not in to_delete]
        
        # Filter embeddings
        if self.embeddings is not None:
            keep_mask = np.array([i not in to_delete for i in range(len(self.embeddings))])
            self.embeddings = self.embeddings[keep_mask]
    
    def clear(self):
        """Clear all documents."""
        self.texts = []
        self.embeddings = None
        self.metadatas = []
    
    def __len__(self) -> int:
        """Return number of documents."""
        return len(self.texts)
    
    def save(self, path: str):
        """
        Save store to disk.
        
        Args:
            path: Directory path to save to
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save texts and metadata
        with open(path / "texts.json", "w") as f:
            json.dump({
                "texts": self.texts,
                "metadatas": self.metadatas
            }, f)
        
        # Save embeddings
        if self.embeddings is not None:
            np.save(path / "embeddings.npy", self.embeddings)
    
    @classmethod
    def load(cls, path: str) -> "InMemoryVectorStore":
        """
        Load store from disk.
        
        Args:
            path: Directory path to load from
            
        Returns:
            Loaded store
        """
        path = Path(path)
        store = cls()
        
        # Load texts and metadata
        with open(path / "texts.json", "r") as f:
            data = json.load(f)
            store.texts = data["texts"]
            store.metadatas = data["metadatas"]
        
        # Load embeddings
        embeddings_path = path / "embeddings.npy"
        if embeddings_path.exists():
            store.embeddings = np.load(embeddings_path)
        
        return store


class FAISSVectorStore(VectorStore):
    """
    FAISS-based vector store for efficient similarity search.
    
    Best for: Large datasets (10k+ documents), production use
    
    Requires: pip install faiss-cpu (or faiss-gpu)
    
    Examples:
        >>> store = FAISSVectorStore(dimension=768)
        >>> store.add(texts=texts, embeddings=embeddings)
        >>> results = store.search(query_embedding, k=10)
    """
    
    def __init__(self, dimension: int, use_gpu: bool = False):
        """
        Initialize FAISS store.
        
        Args:
            dimension: Embedding dimension
            use_gpu: Use GPU for search (requires faiss-gpu)
        """
        try:
            import faiss
        except ImportError:
            raise ImportError(
                "FAISS not installed. "
                "Install with: pip install faiss-cpu (or faiss-gpu)"
            )
        
        self.dimension = dimension
        self.use_gpu = use_gpu
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine after normalization)
        
        if use_gpu:
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                self.index
            )
        
        self.texts: List[str] = []
        self.metadatas: List[Dict[str, Any]] = []
    
    def add(
        self,
        texts: List[str],
        embeddings: np.ndarray,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ):
        """Add documents to FAISS index."""
        # Normalize embeddings for cosine similarity
        embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add to FAISS
        self.index.add(embeddings_norm.astype('float32'))
        
        # Store texts and metadata
        self.texts.extend(texts)
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        self.metadatas.extend(metadatas)
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5
    ) -> List[SearchResult]:
        """Search using FAISS."""
        if len(self.texts) == 0:
            return []
        
        # Normalize query
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        query_norm = query_norm.reshape(1, -1).astype('float32')
        
        # Search
        k = min(k, len(self.texts))
        scores, indices = self.index.search(query_norm, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:  # FAISS returns -1 for missing results
                results.append(SearchResult(
                    text=self.texts[idx],
                    score=float(score),
                    index=int(idx),
                    metadata=self.metadatas[idx]
                ))
        
        return results
    
    def delete(self, indices: List[int]):
        """
        Delete documents (requires rebuilding index).
        
        Note: FAISS doesn't support direct deletion, so we rebuild the index.
        """
        # This is expensive - consider using a tombstone approach for production
        to_delete = set(indices)
        
        # Get remaining data
        new_texts = [t for i, t in enumerate(self.texts) if i not in to_delete]
        new_metadatas = [m for i, m in enumerate(self.metadatas) if i not in to_delete]
        
        # Rebuild index
        self.texts = new_texts
        self.metadatas = new_metadatas
        
        # Note: Embeddings need to be re-added (store them if you need deletion)
        # For now, we clear the index
        import faiss
        self.index = faiss.IndexFlatIP(self.dimension)
        
        if self.use_gpu:
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                self.index
            )
    
    def clear(self):
        """Clear all documents."""
        import faiss
        self.index = faiss.IndexFlatIP(self.dimension)
        
        if self.use_gpu:
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                self.index
            )
        
        self.texts = []
        self.metadatas = []
    
    def __len__(self) -> int:
        """Return number of documents."""
        return len(self.texts)
    
    def save(self, path: str):
        """Save FAISS index and data."""
        import faiss
        
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))
        
        # Save texts and metadata
        with open(path / "data.json", "w") as f:
            json.dump({
                "texts": self.texts,
                "metadatas": self.metadatas,
                "dimension": self.dimension
            }, f)
    
    @classmethod
    def load(cls, path: str, use_gpu: bool = False) -> "FAISSVectorStore":
        """Load FAISS store from disk."""
        import faiss
        
        path = Path(path)
        
        # Load data
        with open(path / "data.json", "r") as f:
            data = json.load(f)
        
        # Create store
        store = cls(dimension=data["dimension"], use_gpu=use_gpu)
        store.texts = data["texts"]
        store.metadatas = data["metadatas"]
        
        # Load index
        store.index = faiss.read_index(str(path / "index.faiss"))
        
        if use_gpu:
            store.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                store.index
            )
        
        return store


# Convenience function

def create_vector_store(
    backend: str = "memory",
    **kwargs
) -> VectorStore:
    """
    Create vector store with specified backend.
    
    Args:
        backend: Backend type ("memory", "faiss")
        **kwargs: Backend-specific arguments
        
    Returns:
        VectorStore instance
        
    Examples:
        >>> # In-memory (simple, fast for small datasets)
        >>> store = create_vector_store("memory")
        >>> 
        >>> # FAISS (efficient for large datasets)
        >>> store = create_vector_store("faiss", dimension=768)
    """
    if backend == "memory":
        return InMemoryVectorStore()
    
    elif backend == "faiss":
        if "dimension" not in kwargs:
            raise ValueError("FAISS backend requires 'dimension' argument")
        return FAISSVectorStore(**kwargs)
    
    else:
        raise ValueError(
            f"Unknown backend: {backend}. "
            f"Choose from: 'memory', 'faiss'"
        )
