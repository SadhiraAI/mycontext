"""
Directive - The atomic instruction unit

A Directive is a single, focused instruction that guides the LLM's behavior
for a specific task. Think of it as a function call in traditional programming.
"""


from pydantic import BaseModel, Field


class Directive(BaseModel):
    """
    A single instruction unit - the atomic building block of context.
    
    Directives are focused, actionable instructions that tell the LLM
    exactly what to do. They are the "what" of context engineering.
    
    Example:
        ```python
        directive = Directive(
            content="Analyze this code for security vulnerabilities",
            priority=9,
            constraints=["Focus on SQL injection", "Check authentication"]
        )
        ```
    
    Attributes:
        content: The instruction content
        priority: Priority level (1-10, higher = more important)
        constraints: Optional list of specific constraints
        tags: Optional tags for categorization
    """

    content: str = Field(
        ...,
        description="The instruction content",
        min_length=1
    )

    priority: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Priority level (1-10)"
    )

    constraints: list[str] | None = Field(
        default=None,
        description="Specific constraints for this directive"
    )

    tags: list[str] | None = Field(
        default=None,
        description="Tags for categorization"
    )

    def render(self) -> str:
        """
        Render the directive as a formatted string.
        
        Returns:
            Formatted directive string
        """
        parts = [self.content]

        if self.constraints:
            constraints_text = "\n".join(f"- {c}" for c in self.constraints)
            parts.append(f"Focus on:\n{constraints_text}")

        return "\n".join(parts)

    def __repr__(self) -> str:
        """String representation"""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Directive('{content_preview}', priority={self.priority})"
