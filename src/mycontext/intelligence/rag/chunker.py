"""
Document Chunking - Split documents into processable chunks for RAG.

This module provides multiple chunking strategies optimized for different
document types and use cases.
"""

from typing import List, Dict, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import re


@dataclass
class Chunk:
    """
    A chunk of text with metadata.
    
    Attributes:
        text: The chunk content
        index: Chunk position in document
        start_char: Starting character position
        end_char: Ending character position
        metadata: Additional chunk metadata (source, page, etc.)
    """
    text: str
    index: int
    start_char: int
    end_char: int
    metadata: Dict[str, Any]
    
    def __len__(self) -> int:
        """Return character length of chunk."""
        return len(self.text)
    
    def token_estimate(self) -> int:
        """Rough token count estimate (1 token ≈ 4 chars)."""
        return len(self.text) // 4


class ChunkingStrategy(ABC):
    """Base class for chunking strategies."""
    
    @abstractmethod
    def chunk(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Chunk]:
        """
        Split text into chunks.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to all chunks
            
        Returns:
            List of Chunk objects
        """
        pass


class FixedSizeChunker(ChunkingStrategy):
    """
    Split text into fixed-size chunks with optional overlap.
    
    Best for: Uniform documents, simple retrieval
    
    Examples:
        >>> chunker = FixedSizeChunker(chunk_size=1000, overlap=200)
        >>> chunks = chunker.chunk(long_text)
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
        separator: str = " "
    ):
        """
        Initialize fixed-size chunker.
        
        Args:
            chunk_size: Target chunk size in characters
            overlap: Number of characters to overlap between chunks
            separator: Character to split on (default: space)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator
    
    def chunk(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Chunk]:
        """Split text into fixed-size chunks."""
        if metadata is None:
            metadata = {}
        
        chunks = []
        start = 0
        index = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If we're not at the end, try to break at separator
            if end < len(text):
                # Look for separator within overlap range
                separator_pos = text.rfind(self.separator, end - self.overlap, end)
                if separator_pos > start:
                    end = separator_pos + 1
            
            # Extract chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append(Chunk(
                    text=chunk_text,
                    index=index,
                    start_char=start,
                    end_char=end,
                    metadata=metadata.copy()
                ))
                index += 1
            
            # Move start position (accounting for overlap)
            start = max(start + 1, end - self.overlap)
        
        return chunks


class SemanticChunker(ChunkingStrategy):
    """
    Split text at semantic boundaries (sentences, paragraphs).
    
    Best for: Natural language, maintaining context
    
    Examples:
        >>> chunker = SemanticChunker(chunk_size=1000, min_chunk_size=100)
        >>> chunks = chunker.chunk(document)
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        min_chunk_size: int = 100,
        respect_paragraphs: bool = True
    ):
        """
        Initialize semantic chunker.
        
        Args:
            chunk_size: Target chunk size in characters
            min_chunk_size: Minimum chunk size
            respect_paragraphs: Try to keep paragraphs together
        """
        self.chunk_size = chunk_size
        self.min_chunk_size = min_chunk_size
        self.respect_paragraphs = respect_paragraphs
    
    def chunk(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Chunk]:
        """Split text at semantic boundaries."""
        if metadata is None:
            metadata = {}
        
        # Split into paragraphs first if requested
        if self.respect_paragraphs:
            paragraphs = text.split('\n\n')
            units = []
            for para in paragraphs:
                if para.strip():
                    # Split paragraph into sentences
                    sentences = self._split_sentences(para)
                    units.extend(sentences)
        else:
            # Just use sentences
            units = self._split_sentences(text)
        
        # Group units into chunks
        chunks = []
        current_chunk = []
        current_size = 0
        start_char = 0
        index = 0
        
        for unit in units:
            unit_size = len(unit)
            
            # If adding this unit exceeds chunk_size and we have content
            if current_size + unit_size > self.chunk_size and current_chunk:
                # Create chunk from accumulated units
                chunk_text = ' '.join(current_chunk)
                
                if len(chunk_text) >= self.min_chunk_size:
                    chunks.append(Chunk(
                        text=chunk_text,
                        index=index,
                        start_char=start_char,
                        end_char=start_char + len(chunk_text),
                        metadata=metadata.copy()
                    ))
                    index += 1
                
                # Start new chunk
                current_chunk = [unit]
                current_size = unit_size
                start_char += len(chunk_text) + 1
            else:
                # Add to current chunk
                current_chunk.append(unit)
                current_size += unit_size + 1  # +1 for space
        
        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(Chunk(
                    text=chunk_text,
                    index=index,
                    start_char=start_char,
                    end_char=start_char + len(chunk_text),
                    metadata=metadata.copy()
                ))
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitter (could be enhanced with spaCy/NLTK)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]


class RecursiveChunker(ChunkingStrategy):
    """
    Recursively split text by trying multiple separators.
    
    Best for: Code, structured documents, markdown
    
    Examples:
        >>> chunker = RecursiveChunker(
        ...     chunk_size=1000,
        ...     separators=['\n\n', '\n', '. ', ' ']
        ... )
        >>> chunks = chunker.chunk(code)
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize recursive chunker.
        
        Args:
            chunk_size: Target chunk size
            overlap: Overlap between chunks
            separators: List of separators to try (in order)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separators = separators or ['\n\n', '\n', '. ', ' ', '']
    
    def chunk(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Chunk]:
        """Split text recursively."""
        if metadata is None:
            metadata = {}
        
        chunks = self._recursive_split(text, 0)
        
        # Convert to Chunk objects
        result = []
        for i, (chunk_text, start) in enumerate(chunks):
            result.append(Chunk(
                text=chunk_text,
                index=i,
                start_char=start,
                end_char=start + len(chunk_text),
                metadata=metadata.copy()
            ))
        
        return result
    
    def _recursive_split(self, text: str, offset: int = 0) -> List[tuple]:
        """Recursively split text."""
        # Base case: text is small enough
        if len(text) <= self.chunk_size:
            return [(text, offset)] if text.strip() else []
        
        # Try each separator
        for separator in self.separators:
            if separator in text:
                parts = text.split(separator)
                
                # Reconstruct with separator
                chunks = []
                current_pos = offset
                
                for i, part in enumerate(parts):
                    if i > 0:
                        # Account for separator
                        current_pos += len(separator)
                    
                    # If part is too large, recursively split it
                    if len(part) > self.chunk_size:
                        sub_chunks = self._recursive_split(part, current_pos)
                        chunks.extend(sub_chunks)
                    elif part.strip():
                        chunks.append((part, current_pos))
                    
                    current_pos += len(part)
                
                return chunks
        
        # Fallback: force split
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk.strip():
                chunks.append((chunk, offset + i))
        
        return chunks


class MarkdownChunker(ChunkingStrategy):
    """
    Split markdown documents by headers while respecting structure.
    
    Best for: Documentation, markdown files
    
    Examples:
        >>> chunker = MarkdownChunker(max_chunk_size=1500)
        >>> chunks = chunker.chunk(markdown_doc)
    """
    
    def __init__(self, max_chunk_size: int = 1500):
        """
        Initialize markdown chunker.
        
        Args:
            max_chunk_size: Maximum chunk size
        """
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Chunk]:
        """Split markdown by headers."""
        if metadata is None:
            metadata = {}
        
        # Find all headers
        header_pattern = r'^(#{1,6})\s+(.+)$'
        lines = text.split('\n')
        
        sections = []
        current_section = []
        current_header = None
        current_start = 0
        char_pos = 0
        
        for line in lines:
            match = re.match(header_pattern, line)
            
            if match:
                # Save previous section
                if current_section:
                    sections.append({
                        'header': current_header,
                        'content': '\n'.join(current_section),
                        'start': current_start
                    })
                
                # Start new section
                current_header = line
                current_section = [line]
                current_start = char_pos
            else:
                current_section.append(line)
            
            char_pos += len(line) + 1  # +1 for newline
        
        # Add final section
        if current_section:
            sections.append({
                'header': current_header,
                'content': '\n'.join(current_section),
                'start': current_start
            })
        
        # Convert sections to chunks (split large sections)
        chunks = []
        index = 0
        
        for section in sections:
            content = section['content']
            
            if len(content) <= self.max_chunk_size:
                # Section fits in one chunk
                chunks.append(Chunk(
                    text=content,
                    index=index,
                    start_char=section['start'],
                    end_char=section['start'] + len(content),
                    metadata={
                        **metadata,
                        'header': section.get('header', 'No header')
                    }
                ))
                index += 1
            else:
                # Split large section
                sub_chunker = SemanticChunker(chunk_size=self.max_chunk_size)
                sub_chunks = sub_chunker.chunk(content, metadata={
                    **metadata,
                    'header': section.get('header', 'No header')
                })
                
                for sub_chunk in sub_chunks:
                    chunks.append(Chunk(
                        text=sub_chunk.text,
                        index=index,
                        start_char=section['start'] + sub_chunk.start_char,
                        end_char=section['start'] + sub_chunk.end_char,
                        metadata=sub_chunk.metadata
                    ))
                    index += 1
        
        return chunks


# Convenience function

def chunk_text(
    text: str,
    strategy: str = "semantic",
    chunk_size: int = 1000,
    metadata: Optional[Dict[str, Any]] = None,
    **kwargs
) -> List[Chunk]:
    """
    Quick text chunking with automatic strategy selection.
    
    Args:
        text: Text to chunk
        strategy: Chunking strategy ("fixed", "semantic", "recursive", "markdown")
        chunk_size: Target chunk size
        metadata: Optional metadata to attach to chunks
        **kwargs: Additional strategy-specific arguments (for chunker constructor)
        
    Returns:
        List of chunks
        
    Examples:
        >>> chunks = chunk_text(document, strategy="semantic", chunk_size=1000)
    """
    strategies = {
        "fixed": FixedSizeChunker,
        "semantic": SemanticChunker,
        "recursive": RecursiveChunker,
        "markdown": MarkdownChunker,
    }
    
    if strategy not in strategies:
        raise ValueError(f"Unknown strategy: {strategy}. Choose from: {list(strategies.keys())}")
    
    chunker_class = strategies[strategy]
    chunker = chunker_class(chunk_size=chunk_size, **kwargs)
    
    return chunker.chunk(text, metadata=metadata)
