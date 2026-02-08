"""
Retriever - High-level RAG retrieval with reranking and filtering.

Combines chunking, embedding, and vector search into a simple API.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

from .chunker import Chunk, ChunkingStrategy, chunk_text
from .embedder import Embedder, get_embedder
from .vector_store import VectorStore, SearchResult, create_vector_store


@dataclass
class RetrievalResult:
    """
    Result from retrieval with reranking.
    
    Attributes:
        text: Retrieved text
        score: Final score (after reranking if applied)
        original_score: Original similarity score
        chunk: Original chunk object
        rank: Final rank position
    """
    text: str
    score: float
    original_score: float
    chunk: Chunk
    rank: int


class Retriever:
    """
    High-level retrieval system for RAG.
    
    Handles the complete pipeline:
    1. Document chunking
    2. Embedding generation
    3. Vector storage
    4. Similarity search
    5. Optional reranking
    
    Examples:
        >>> # Create retriever
        >>> retriever = Retriever(
        ...     embedder="sentence-transformers",
        ...     vector_store="memory",
        ...     chunk_size=1000
        ... )
        >>> 
        >>> # Add documents
        >>> retriever.add_documents([
        ...     "Python is a programming language...",
        ...     "Machine learning is a field..."
        ... ])
        >>> 
        >>> # Search
        >>> results = retriever.retrieve("What is Python?", k=5)
        >>> for result in results:
        ...     print(f"Score: {result.score:.3f} - {result.text[:100]}")
    """
    
    def __init__(
        self,
        embedder: Optional[Embedder] = None,
        vector_store: Optional[VectorStore] = None,
        chunker: Optional[ChunkingStrategy] = None,
        chunk_strategy: str = "semantic",
        chunk_size: int = 1000,
        embedder_provider: str = "sentence-transformers",
        embedder_model: Optional[str] = None,
        vector_store_backend: str = "memory",
        **vector_store_kwargs
    ):
        """
        Initialize retriever.
        
        Args:
            embedder: Custom embedder (or use embedder_provider)
            vector_store: Custom vector store (or use vector_store_backend)
            chunker: Custom chunking strategy (or use chunk_strategy)
            chunk_strategy: Chunking strategy name
            chunk_size: Target chunk size
            embedder_provider: Embedder provider if embedder not provided
            embedder_model: Embedder model name
            vector_store_backend: Vector store backend if not provided
            **vector_store_kwargs: Additional vector store arguments
        """
        # Setup embedder
        if embedder is None:
            self.embedder = get_embedder(
                provider=embedder_provider,
                model=embedder_model
            )
        else:
            self.embedder = embedder
        
        # Setup vector store
        if vector_store is None:
            # Auto-provide dimension for FAISS
            if vector_store_backend == "faiss" and "dimension" not in vector_store_kwargs:
                vector_store_kwargs["dimension"] = self.embedder.dimension
            
            self.vector_store = create_vector_store(
                backend=vector_store_backend,
                **vector_store_kwargs
            )
        else:
            self.vector_store = vector_store
        
        # Setup chunker
        self.chunker = chunker
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        show_progress: bool = False
    ):
        """
        Add documents to the retriever.
        
        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            show_progress: Show progress during processing
        """
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        all_chunks = []
        all_chunk_metadatas = []
        
        # Chunk all documents
        for doc_idx, (doc, doc_meta) in enumerate(zip(documents, metadatas)):
            if show_progress:
                print(f"\rChunking document {doc_idx + 1}/{len(documents)}", end="")
            
            # Chunk document
            if self.chunker:
                chunks = self.chunker.chunk(doc, metadata=doc_meta)
            else:
                chunks = chunk_text(
                    doc,
                    strategy=self.chunk_strategy,
                    chunk_size=self.chunk_size,
                    metadata=doc_meta
                )
            
            all_chunks.extend(chunks)
            
            # Prepare metadata
            for chunk in chunks:
                chunk_meta = {
                    **doc_meta,
                    "doc_index": doc_idx,
                    "chunk_index": chunk.index
                }
                all_chunk_metadatas.append(chunk_meta)
        
        if show_progress:
            print(f"\n{len(all_chunks)} chunks created")
        
        # Generate embeddings
        if show_progress:
            print("Generating embeddings...")
        
        chunk_texts = [chunk.text for chunk in all_chunks]
        embeddings = self.embedder.embed(chunk_texts)
        
        # Add to vector store
        if show_progress:
            print("Adding to vector store...")
        
        self.vector_store.add(
            texts=chunk_texts,
            embeddings=embeddings,
            metadatas=all_chunk_metadatas
        )
        
        if show_progress:
            print(f"✅ Added {len(documents)} documents ({len(all_chunks)} chunks)")
    
    def retrieve(
        self,
        query: str,
        k: int = 5,
        rerank: bool = False,
        rerank_fn: Optional[Callable] = None,
        filter_fn: Optional[Callable[[SearchResult], bool]] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query: Query text
            k: Number of results to return
            rerank: Apply reranking
            rerank_fn: Custom reranking function
            filter_fn: Filter function for results
            
        Returns:
            List of retrieval results sorted by score
        """
        # Embed query
        query_embedding = self.embedder.embed_query(query)
        
        # Search vector store (get more if reranking)
        search_k = k * 3 if rerank else k
        search_results = self.vector_store.search(query_embedding, k=search_k)
        
        # Apply filter if provided
        if filter_fn:
            search_results = [r for r in search_results if filter_fn(r)]
        
        # Rerank if requested
        if rerank:
            if rerank_fn:
                # Custom reranking
                search_results = rerank_fn(query, search_results)
            else:
                # Default reranking (by length and position)
                search_results = self._default_rerank(query, search_results)
            
            # Take top k after reranking
            search_results = search_results[:k]
        
        # Convert to RetrievalResult
        results = []
        for rank, result in enumerate(search_results):
            # Reconstruct chunk (simplified)
            chunk = Chunk(
                text=result.text,
                index=result.metadata.get("chunk_index", 0),
                start_char=0,
                end_char=len(result.text),
                metadata=result.metadata
            )
            
            results.append(RetrievalResult(
                text=result.text,
                score=result.score,
                original_score=result.score,
                chunk=chunk,
                rank=rank
            ))
        
        return results
    
    def _default_rerank(
        self,
        query: str,
        results: List[SearchResult]
    ) -> List[SearchResult]:
        """
        Default reranking strategy.
        
        Considers:
        - Similarity score (primary)
        - Text length (prefer medium-length chunks)
        - Query term overlap
        """
        query_terms = set(query.lower().split())
        
        scored_results = []
        for result in results:
            # Base score from similarity
            score = result.score
            
            # Length bonus (prefer 200-800 chars)
            text_len = len(result.text)
            if 200 <= text_len <= 800:
                length_bonus = 0.1
            elif text_len < 100 or text_len > 1500:
                length_bonus = -0.1
            else:
                length_bonus = 0
            
            # Term overlap bonus
            result_terms = set(result.text.lower().split())
            overlap = len(query_terms & result_terms) / len(query_terms)
            overlap_bonus = overlap * 0.1
            
            # Final score
            final_score = score + length_bonus + overlap_bonus
            
            # Create new result with updated score
            scored_results.append((final_score, result))
        
        # Sort by final score
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        return [result for _, result in scored_results]
    
    def build_context(
        self,
        query: str,
        k: int = 5,
        max_length: int = 4000,
        separator: str = "\n\n---\n\n"
    ) -> str:
        """
        Build context string from retrieved chunks.
        
        Args:
            query: Query text
            k: Number of chunks to retrieve
            max_length: Maximum context length
            separator: Separator between chunks
            
        Returns:
            Formatted context string
        """
        results = self.retrieve(query, k=k, rerank=True)
        
        context_parts = []
        current_length = 0
        
        for result in results:
            chunk_text = result.text
            chunk_length = len(chunk_text) + len(separator)
            
            if current_length + chunk_length > max_length:
                break
            
            context_parts.append(chunk_text)
            current_length += chunk_length
        
        return separator.join(context_parts)
    
    def clear(self):
        """Clear all documents from retriever."""
        self.vector_store.clear()
    
    def __len__(self) -> int:
        """Return number of chunks in store."""
        return len(self.vector_store)
    
    def save(self, path: str):
        """
        Save retriever state to disk.
        
        Args:
            path: Directory path to save to
        """
        # Save vector store
        self.vector_store.save(path)
    
    @classmethod
    def load(cls, path: str, **kwargs) -> "Retriever":
        """
        Load retriever from disk.
        
        Args:
            path: Directory path to load from
            **kwargs: Additional retriever arguments
            
        Returns:
            Loaded retriever
        """
        # This would need to serialize embedder config too
        # For now, raise NotImplementedError
        raise NotImplementedError(
            "Loading retriever not yet implemented. "
            "Please recreate retriever and add documents."
        )


# Convenience function

def create_retriever(
    documents: Optional[List[str]] = None,
    embedder: str = "sentence-transformers",
    embedder_model: Optional[str] = None,
    vector_store: str = "memory",
    chunk_strategy: str = "semantic",
    chunk_size: int = 1000,
    **kwargs
) -> Retriever:
    """
    Quick retriever creation with documents.
    
    Args:
        documents: Optional documents to add immediately
        embedder: Embedder provider
        embedder_model: Embedder model name
        vector_store: Vector store backend
        chunk_strategy: Chunking strategy
        chunk_size: Chunk size
        **kwargs: Additional retriever arguments
        
    Returns:
        Retriever instance
        
    Examples:
        >>> retriever = create_retriever(
        ...     documents=["Doc 1", "Doc 2"],
        ...     embedder="sentence-transformers",
        ...     vector_store="memory"
        ... )
        >>> 
        >>> results = retriever.retrieve("query", k=5)
    """
    retriever = Retriever(
        embedder_provider=embedder,
        embedder_model=embedder_model,
        vector_store_backend=vector_store,
        chunk_strategy=chunk_strategy,
        chunk_size=chunk_size,
        **kwargs
    )
    
    if documents:
        retriever.add_documents(documents, show_progress=True)
    
    return retriever
