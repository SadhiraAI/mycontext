"""
Knowledge Layer - Archive Management

The Archive component provides persistent storage for sessions and contexts.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json
import os
from pathlib import Path

from .session import Session, Message


class ArchiveEntry(BaseModel):
    """
    A single entry in the archive.
    
    Attributes:
        id: Unique entry ID
        session_id: Associated session ID
        timestamp: When the entry was archived
        data: The archived data
        tags: Searchable tags
        metadata: Additional metadata
    """
    
    id: str = Field(..., description="Entry ID")
    session_id: Optional[str] = Field(None, description="Session ID")
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any] = Field(..., description="Archived data")
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseArchive(ABC):
    """
    Abstract base class for archive backends.
    
    Implementations can use different storage backends:
    - FileArchive: JSON files
    - RedisArchive: Redis database
    - PostgresArchive: PostgreSQL
    - S3Archive: AWS S3
    """
    
    @abstractmethod
    def save_session(self, session: Session) -> str:
        """Save a session to the archive"""
        pass
    
    @abstractmethod
    def load_session(self, session_id: str) -> Optional[Session]:
        """Load a session from the archive"""
        pass
    
    @abstractmethod
    def list_sessions(
        self,
        limit: int = 100,
        tags: Optional[List[str]] = None
    ) -> List[ArchiveEntry]:
        """List archived sessions"""
        pass
    
    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Delete a session from the archive"""
        pass
    
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[ArchiveEntry]:
        """Search the archive"""
        pass


class FileArchive(BaseArchive):
    """
    File-based archive using JSON files.
    
    Simple, portable storage for sessions and contexts.
    Good for development and small-scale use.
    
    Example:
        >>> from mycontext.knowledge import FileArchive, Session
        >>> 
        >>> archive = FileArchive("./my_archive")
        >>> 
        >>> session = Session()
        >>> session.add_message("user", "Hello")
        >>> session.add_message("assistant", "Hi!")
        >>> 
        >>> # Save session
        >>> entry_id = archive.save_session(session)
        >>> 
        >>> # Load it back
        >>> loaded = archive.load_session(session.id)
        >>> print(len(loaded.messages))  # 2
    """
    
    def __init__(self, directory: str = "./archive"):
        """
        Initialize file archive.
        
        Args:
            directory: Directory to store archive files
        """
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.directory / "sessions").mkdir(exist_ok=True)
        (self.directory / "index").mkdir(exist_ok=True)
    
    def save_session(
        self,
        session: Session,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Save a session to the archive.
        
        Args:
            session: Session to save
            tags: Optional tags for searching
            
        Returns:
            Entry ID
        """
        # Create entry
        entry = ArchiveEntry(
            id=session.id,
            session_id=session.id,
            data=session.model_dump(mode='json'),
            tags=tags or []
        )
        
        # Save to file
        filepath = self.directory / "sessions" / f"{session.id}.json"
        with open(filepath, 'w') as f:
            json.dump(entry.model_dump(mode='json'), f, indent=2, default=str)
        
        # Update index
        self._update_index(entry)
        
        return entry.id
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """
        Load a session from the archive.
        
        Args:
            session_id: Session ID to load
            
        Returns:
            Session or None if not found
        """
        filepath = self.directory / "sessions" / f"{session_id}.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            entry_data = json.load(f)
        
        entry = ArchiveEntry(**entry_data)
        
        # Reconstruct session
        session = Session(**entry.data)
        
        return session
    
    def list_sessions(
        self,
        limit: int = 100,
        tags: Optional[List[str]] = None
    ) -> List[ArchiveEntry]:
        """
        List archived sessions.
        
        Args:
            limit: Maximum number to return
            tags: Filter by tags (optional)
            
        Returns:
            List of archive entries
        """
        entries = []
        
        # Load all session files
        session_dir = self.directory / "sessions"
        for filepath in session_dir.glob("*.json"):
            with open(filepath, 'r') as f:
                entry_data = json.load(f)
            
            entry = ArchiveEntry(**entry_data)
            
            # Filter by tags
            if tags:
                if not any(tag in entry.tags for tag in tags):
                    continue
            
            entries.append(entry)
        
        # Sort by timestamp (newest first)
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries[:limit]
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session from the archive.
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        filepath = self.directory / "sessions" / f"{session_id}.json"
        
        if not filepath.exists():
            return False
        
        filepath.unlink()
        
        # TODO: Update index
        
        return True
    
    def search(self, query: str, limit: int = 10) -> List[ArchiveEntry]:
        """
        Search the archive for sessions.
        
        Simple text-based search in message content.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            Matching archive entries
        """
        results = []
        query_lower = query.lower()
        
        # Search through all sessions
        for entry in self.list_sessions(limit=1000):
            # Search in message content
            session_data = entry.data
            messages = session_data.get("messages", [])
            
            for msg in messages:
                content = msg.get("content", "").lower()
                if query_lower in content:
                    results.append(entry)
                    break
            
            if len(results) >= limit:
                break
        
        return results[:limit]
    
    def _update_index(self, entry: ArchiveEntry) -> None:
        """Update search index"""
        # TODO: Implement proper indexing
        # For now, index is just the session files themselves
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get archive statistics.
        
        Returns:
            Dictionary with stats
        """
        sessions = self.list_sessions(limit=10000)
        
        total_messages = 0
        for entry in sessions:
            messages = entry.data.get("messages", [])
            total_messages += len(messages)
        
        return {
            "total_sessions": len(sessions),
            "total_messages": total_messages,
            "storage_path": str(self.directory),
        }


class MemoryArchive(BaseArchive):
    """
    In-memory archive for testing and temporary storage.
    
    Not persistent - data is lost when process ends.
    
    Example:
        >>> from mycontext.knowledge import MemoryArchive
        >>> 
        >>> archive = MemoryArchive()
        >>> # Use like FileArchive but data isn't saved to disk
    """
    
    def __init__(self):
        self._storage: Dict[str, ArchiveEntry] = {}
    
    def save_session(
        self,
        session: Session,
        tags: Optional[List[str]] = None
    ) -> str:
        """Save session to memory"""
        entry = ArchiveEntry(
            id=session.id,
            session_id=session.id,
            data=session.model_dump(mode='json'),
            tags=tags or []
        )
        
        self._storage[session.id] = entry
        
        return entry.id
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """Load session from memory"""
        entry = self._storage.get(session_id)
        
        if not entry:
            return None
        
        return Session(**entry.data)
    
    def list_sessions(
        self,
        limit: int = 100,
        tags: Optional[List[str]] = None
    ) -> List[ArchiveEntry]:
        """List sessions in memory"""
        entries = list(self._storage.values())
        
        # Filter by tags
        if tags:
            entries = [
                e for e in entries
                if any(tag in e.tags for tag in tags)
            ]
        
        # Sort by timestamp
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries[:limit]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session from memory"""
        if session_id in self._storage:
            del self._storage[session_id]
            return True
        return False
    
    def search(self, query: str, limit: int = 10) -> List[ArchiveEntry]:
        """Search sessions in memory"""
        results = []
        query_lower = query.lower()
        
        for entry in self._storage.values():
            messages = entry.data.get("messages", [])
            
            for msg in messages:
                content = msg.get("content", "").lower()
                if query_lower in content:
                    results.append(entry)
                    break
            
            if len(results) >= limit:
                break
        
        return results[:limit]
    
    def clear(self) -> None:
        """Clear all data from memory"""
        self._storage.clear()
