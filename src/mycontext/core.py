"""
Core Context class - The heart of mycontext

This is where Context as Code™ comes to life.
"""

from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field

from .foundation import Directive, Guidance, Constraints


class Context(BaseModel):
    """
    Core Context class that represents a complete contextual environment for LLM interaction.
    
    The Context is the fundamental building block that combines:
    - Guidance (system-level behavioral rules)
    - Directives (specific instructions)
    - Knowledge (memory, documents, state)
    - Data (user inputs and parameters)
    
    Example:
        ```python
        from mycontext import Context, Guidance
        
        # Simple usage
        context = Context("You are a helpful assistant")
        
        # Advanced usage
        context = Context(
            guidance=Guidance(role="Expert code reviewer", rules=["Be thorough"]),
            directive=Directive("Review this code for security issues")
        )
        ```
    """
    
    guidance: Optional[Guidance] = Field(
        default=None,
        description="System-level behavioral guidance"
    )
    
    directive: Optional[Directive] = Field(
        default=None,
        description="Specific instruction for this interaction"
    )
    
    constraints: Optional[Constraints] = Field(
        default=None,
        description="Hard constraints and guardrails"
    )
    
    knowledge: Optional[str] = Field(
        default=None,
        description="Retrieved knowledge, documents, or memory context"
    )
    
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data and parameters"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about this context (tags, version, etc.)"
    )
    
    def __init__(
        self,
        guidance: Union[str, Guidance, None] = None,
        directive: Union[str, Directive, None] = None,
        **kwargs
    ):
        """
        Initialize a Context.
        
        Args:
            guidance: System-level guidance (can be string or Guidance object)
            directive: Specific directive (can be string or Directive object)
            **kwargs: Additional parameters (data, constraints, etc.)
        """
        # Convert simple strings to appropriate objects
        if isinstance(guidance, str):
            guidance = Guidance(role=guidance)
        
        if isinstance(directive, str):
            directive = Directive(content=directive)
        
        super().__init__(guidance=guidance, directive=directive, **kwargs)
    
    def assemble(self) -> str:
        """
        Assemble the complete context into a formatted string.
        
        This is where the magic happens - combining all components
        into a coherent context that can be sent to an LLM.
        
        Returns:
            Assembled context as a formatted string
        """
        parts = []
        
        # Add guidance (system-level)
        if self.guidance:
            parts.append(self.guidance.render())
        
        # Add constraints (boundaries)
        if self.constraints:
            parts.append(self.constraints.render())
        
        # Add knowledge (retrieved information)
        if self.knowledge:
            parts.append(f"# Knowledge\n\n{self.knowledge}")
        
        # Add directive (specific instruction)
        if self.directive:
            parts.append(self.directive.render())
        
        # Join with double newlines for clarity
        return "\n\n".join(filter(None, parts))
    
    def execute(self, provider: str = "openai", **kwargs) -> Any:
        """
        Execute this context with an LLM provider.
        
        Args:
            provider: Provider name ('openai', 'anthropic', 'google', etc.)
            **kwargs: Additional parameters for the provider
            
        Returns:
            Provider response
            
        Example:
            ```python
            context = Context("You are a helpful assistant")
            result = context.execute(
                user="What is context engineering?",
                provider="gpt-4"
            )
            print(result.response)
            ```
        """
        from .providers import get_provider
        
        provider_instance = get_provider(provider)
        return provider_instance.generate(self, **kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert context to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return self.model_dump()
    
    def to_messages(self, user_message: Optional[str] = None) -> list:
        """
        Export context as OpenAI-style message array.
        
        Universal format compatible with OpenAI, Anthropic, and most LLM providers.
        
        Args:
            user_message: Optional user message to append
            
        Returns:
            List of message dictionaries [{"role": "system", "content": "..."}, ...]
            
        Example:
            ```python
            context = Context(guidance="Expert analyst")
            messages = context.to_messages(user_message="Analyze this data")
            # Use with any provider that accepts messages format
            openai.chat.completions.create(messages=messages, model="gpt-4")
            ```
        """
        messages = []
        
        # System message from assembled context
        assembled = self.assemble()
        if assembled:
            messages.append({"role": "system", "content": assembled})
        
        # Optional user message
        if user_message:
            messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def to_langchain(self):
        """
        Export context for LangChain/LangGraph integration.
        
        Returns:
            Dictionary with 'system_message' and 'context' keys
            
        Example:
            ```python
            context = Context(guidance="Expert", directive="Analyze")
            lc_format = context.to_langchain()
            
            # Use in LangChain
            from langchain.schema import SystemMessage
            system_msg = SystemMessage(content=lc_format['system_message'])
            ```
        """
        return {
            "system_message": self.assemble(),
            "context": self.to_dict(),
            "guidance": self.guidance.model_dump() if self.guidance else None,
            "directive": self.directive.model_dump() if self.directive else None,
            "knowledge": self.knowledge,
        }
    
    def to_markdown(self) -> str:
        """
        Export context as human-readable Markdown.
        
        Useful for documentation, debugging, or human review.
        
        Returns:
            Markdown-formatted string
            
        Example:
            ```python
            context = Context(guidance="Expert", directive="Analyze this")
            print(context.to_markdown())
            # Output:
            # # Context
            # ## Guidance
            # Role: Expert
            # ...
            ```
        """
        lines = ["# Context\n"]
        
        if self.guidance:
            lines.append("## Guidance\n")
            lines.append(f"**Role:** {self.guidance.role}\n")
            if self.guidance.rules:
                lines.append("**Rules:**\n")
                for rule in self.guidance.rules:
                    lines.append(f"- {rule}\n")
            if self.guidance.style:
                lines.append(f"**Style:** {self.guidance.style}\n")
        
        if self.directive:
            lines.append("\n## Directive\n")
            lines.append(f"{self.directive.content}\n")
        
        if self.constraints:
            lines.append("\n## Constraints\n")
            if self.constraints.must_include:
                lines.append("**Must Include:**\n")
                for item in self.constraints.must_include:
                    lines.append(f"- {item}\n")
            if self.constraints.must_not_include:
                lines.append("**Must NOT Include:**\n")
                for item in self.constraints.must_not_include:
                    lines.append(f"- {item}\n")
            if self.constraints.format_rules:
                lines.append("**Format Rules:**\n")
                for rule in self.constraints.format_rules:
                    lines.append(f"- {rule}\n")
        
        if self.knowledge:
            lines.append("\n## Knowledge\n")
            lines.append(f"{self.knowledge}\n")
        
        if self.data:
            lines.append("\n## Data\n")
            for key, value in self.data.items():
                lines.append(f"**{key}:** {value}\n")
        
        return "".join(lines)
    
    def to_json(self) -> str:
        """
        Export context as JSON string.
        
        Useful for API transmission, storage, or language-agnostic consumption.
        
        Returns:
            JSON string representation
            
        Example:
            ```python
            context = Context(guidance="Expert")
            json_str = context.to_json()
            # Send via API, save to file, etc.
            ```
        """
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Context":
        """
        Create context from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Context instance
        """
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "Context":
        """
        Create context from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            Context instance
        """
        import json
        return cls.from_dict(json.loads(json_str))
    
    def __repr__(self) -> str:
        """String representation"""
        parts = []
        if self.guidance:
            parts.append(f"guidance={self.guidance.role}")
        if self.directive:
            parts.append(f"directive={self.directive.content[:50]}...")
        return f"Context({', '.join(parts)})"
