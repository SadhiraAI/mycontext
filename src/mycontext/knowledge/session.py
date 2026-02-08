"""
Knowledge Layer - Session Management

The Session component manages conversational context and message history.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Message(BaseModel):
    """
    A single message in a conversation.
    
    Attributes:
        role: Message role ('system', 'user', 'assistant')
        content: Message content
        timestamp: When the message was created
        metadata: Additional message metadata
        id: Unique message identifier
    """
    
    role: str = Field(..., description="Message role (system/user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID")
    
    def render(self) -> Dict[str, str]:
        """Render as OpenAI/Anthropic message format"""
        return {
            "role": self.role,
            "content": self.content
        }


class Session(BaseModel):
    """
    Manages conversational context and message history.
    
    The Session maintains a rolling conversation, handling:
    - Message history
    - Token budgeting
    - Context window management
    - Conversation summarization
    
    Example:
        >>> from mycontext.knowledge import Session
        >>> 
        >>> session = Session(max_tokens=4000)
        >>> session.add_message("system", "You are a helpful assistant")
        >>> session.add_message("user", "Hello!")
        >>> session.add_message("assistant", "Hi! How can I help?")
        >>> 
        >>> messages = session.get_messages()
        >>> print(f"Messages: {len(messages)}")
    """
    
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique session ID"
    )
    
    messages: List[Message] = Field(
        default_factory=list,
        description="Message history"
    )
    
    max_tokens: int = Field(
        default=4000,
        description="Maximum tokens to maintain in history"
    )
    
    max_messages: Optional[int] = Field(
        default=None,
        description="Maximum number of messages to keep"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Session metadata"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Session creation time"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Last update time"
    )
    
    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Add a message to the session.
        
        Args:
            role: Message role ('system', 'user', 'assistant')
            content: Message content
            metadata: Optional message metadata
            
        Returns:
            Created message
            
        Example:
            >>> session.add_message("user", "What is 2+2?")
            >>> session.add_message("assistant", "4")
        """
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        self.updated_at = datetime.now()
        
        # Prune if needed
        self._prune_messages()
        
        return message
    
    def add_user_message(self, content: str, **metadata: Any) -> Message:
        """Add a user message (convenience method)"""
        return self.add_message("user", content, metadata)
    
    def add_assistant_message(self, content: str, **metadata: Any) -> Message:
        """Add an assistant message (convenience method)"""
        return self.add_message("assistant", content, metadata)
    
    def add_system_message(self, content: str, **metadata: Any) -> Message:
        """Add a system message (convenience method)"""
        return self.add_message("system", content, metadata)
    
    def get_messages(
        self,
        limit: Optional[int] = None,
        role: Optional[str] = None
    ) -> List[Message]:
        """
        Get messages from the session.
        
        Args:
            limit: Maximum number of messages to return
            role: Filter by role (optional)
            
        Returns:
            List of messages
            
        Example:
            >>> # Get last 5 messages
            >>> recent = session.get_messages(limit=5)
            >>> 
            >>> # Get only user messages
            >>> user_msgs = session.get_messages(role="user")
        """
        messages = self.messages
        
        # Filter by role
        if role:
            messages = [msg for msg in messages if msg.role == role]
        
        # Limit
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def render_messages(self) -> List[Dict[str, str]]:
        """
        Render messages in OpenAI/Anthropic format.
        
        Returns:
            List of message dicts with 'role' and 'content'
            
        Example:
            >>> messages = session.render_messages()
            >>> # [{"role": "user", "content": "Hello"}, ...]
        """
        return [msg.render() for msg in self.messages]
    
    def estimate_tokens(self) -> int:
        """
        Estimate total tokens in message history.
        
        Uses rough approximation: 4 chars ≈ 1 token
        
        Returns:
            Estimated token count
        """
        total_chars = sum(len(msg.content) for msg in self.messages)
        return total_chars // 4
    
    def clear(self) -> None:
        """
        Clear all messages from the session.
        
        Example:
            >>> session.clear()
            >>> assert len(session.messages) == 0
        """
        self.messages = []
        self.updated_at = datetime.now()
    
    def _prune_messages(self) -> None:
        """Prune messages to stay within limits"""
        # Prune by message count
        if self.max_messages and len(self.messages) > self.max_messages:
            # Keep system messages + recent messages
            system_msgs = [msg for msg in self.messages if msg.role == "system"]
            other_msgs = [msg for msg in self.messages if msg.role != "system"]
            
            # Keep latest messages
            keep_count = self.max_messages - len(system_msgs)
            other_msgs = other_msgs[-keep_count:]
            
            self.messages = system_msgs + other_msgs
        
        # Prune by token count
        estimated_tokens = self.estimate_tokens()
        while estimated_tokens > self.max_tokens and len(self.messages) > 1:
            # Remove oldest non-system message
            for i, msg in enumerate(self.messages):
                if msg.role != "system":
                    self.messages.pop(i)
                    break
            
            estimated_tokens = self.estimate_tokens()
    
    def to_context_string(self) -> str:
        """
        Convert session to a context string.
        
        Useful for passing to Context objects.
        
        Returns:
            Formatted conversation string
        """
        parts = []
        for msg in self.messages:
            parts.append(f"{msg.role.upper()}: {msg.content}")
        
        return "\n\n".join(parts)
    
    def __len__(self) -> int:
        """Return number of messages"""
        return len(self.messages)
    
    def __repr__(self) -> str:
        return f"Session(id={self.id[:8]}, messages={len(self.messages)}, tokens≈{self.estimate_tokens()})"
