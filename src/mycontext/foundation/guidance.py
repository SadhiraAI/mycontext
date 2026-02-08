"""
Guidance - System-level behavioral rules

Guidance defines the role, personality, and behavioral rules for the LLM.
It's the "how" and "who" of context engineering.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Guidance(BaseModel):
    """
    System-level behavioral guidance that defines how the LLM should act.
    
    Guidance is like the personality and expertise definition - it tells
    the LLM who it is and how it should behave across all interactions.
    
    Example:
        ```python
        guidance = Guidance(
            role="Expert security engineer with 10 years experience",
            rules=[
                "Always prioritize security over convenience",
                "Explain technical concepts clearly",
                "Provide code examples when relevant"
            ],
            style="Professional but approachable"
        )
        ```
    
    Attributes:
        role: The role/persona the LLM should adopt
        rules: List of behavioral rules to follow
        style: Communication style
        expertise: Areas of expertise
    """
    
    role: str = Field(
        ...,
        description="The role or persona",
        min_length=1
    )
    
    rules: List[str] = Field(
        default_factory=list,
        description="Behavioral rules to follow"
    )
    
    style: Optional[str] = Field(
        default=None,
        description="Communication style"
    )
    
    expertise: Optional[List[str]] = Field(
        default=None,
        description="Areas of expertise"
    )
    
    def render(self) -> str:
        """
        Render guidance as a system prompt.
        
        Returns:
            Formatted system prompt
        """
        parts = [f"You are {self.role}."]
        
        if self.expertise:
            expertise_text = ", ".join(self.expertise)
            parts.append(f"Your areas of expertise include: {expertise_text}.")
        
        if self.rules:
            rules_text = "\n".join(f"{i+1}. {rule}" for i, rule in enumerate(self.rules))
            parts.append(f"\nFollow these rules:\n{rules_text}")
        
        if self.style:
            parts.append(f"\nCommunication style: {self.style}")
        
        return "\n".join(parts)
    
    def __repr__(self) -> str:
        """String representation"""
        role_preview = self.role[:50] + "..." if len(self.role) > 50 else self.role
        return f"Guidance(role='{role_preview}', rules={len(self.rules)})"
