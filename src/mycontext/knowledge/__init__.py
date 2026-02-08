"""
Knowledge Layer (Layer 3) - Session, Archive, Index

This layer manages conversational memory and knowledge storage:

- **Session**: Manages conversational context and message history
- **Archive**: Persistent storage for sessions
- **Index**: (Coming soon) Fast retrieval and search

Example:
    >>> from mycontext.knowledge import Session, FileArchive
    >>> 
    >>> # Create a session
    >>> session = Session(max_tokens=4000)
    >>> session.add_message("user", "Hello!")
    >>> session.add_message("assistant", "Hi! How can I help?")
    >>> 
    >>> # Archive it
    >>> archive = FileArchive("./my_archive")
    >>> archive.save_session(session)
    >>> 
    >>> # Load it later
    >>> loaded = archive.load_session(session.id)
"""

from .session import Session, Message
from .archive import (
    BaseArchive,
    FileArchive,
    MemoryArchive,
    ArchiveEntry,
)

__all__ = [
    # Session
    "Session",
    "Message",
    # Archive
    "BaseArchive",
    "FileArchive",
    "MemoryArchive",
    "ArchiveEntry",
]
