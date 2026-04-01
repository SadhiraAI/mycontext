"""
Blueprint - Multi-component context architecture

Blueprints are like architectural diagrams - they define how multiple
components come together to form a complete, production-ready context.
"""

from typing import Any

from pydantic import BaseModel, Field

from ..core import Context
from ..foundation import Constraints, Directive, Guidance


class Blueprint(BaseModel):
    """
    Multi-component context architecture for complex applications.

    Blueprints orchestrate multiple components (guidance, knowledge,
    reasoning, etc.) into a cohesive, optimized context. They handle:
    - Component assembly and ordering
    - Token budget management
    - Automatic optimization
    - Context compilation

    Example:
        ```python
        from mycontext.structure import Blueprint

        blueprint = Blueprint(
            name="research_assistant",
            guidance=Guidance("Expert research assistant"),
            components=[
                Session(max_history=10),
                Index(documents=["papers/"]),
            ],
            token_budget=4000,
            optimization="balanced"
        )

        context = blueprint.build(query="Explain quantum computing")
        ```

    Attributes:
        name: Blueprint name
        description: What this blueprint creates
        guidance: Primary guidance
        components: List of components to include
        token_budget: Maximum tokens (will auto-optimize)
        optimization: Strategy ("speed", "quality", "cost", "balanced")
        priority_order: Order of component priority for optimization
    """

    name: str = Field(..., description="Blueprint name", min_length=1)

    description: str | None = Field(default=None, description="What this blueprint creates")

    guidance: Guidance | None = Field(default=None, description="Primary guidance")

    directive_template: str | None = Field(default=None, description="Template for directive")

    constraints: Constraints | None = Field(default=None, description="Default constraints")

    components: list[Any] = Field(
        default_factory=list, description="Components to include (Session, Index, etc.)"
    )

    token_budget: int = Field(default=4000, ge=100, le=1000000, description="Maximum token budget")

    optimization: str = Field(default="balanced", description="Optimization strategy")

    priority_order: list[str] = Field(
        default_factory=lambda: ["guidance", "directive", "constraints", "knowledge", "memory"],
        description="Component priority order",
    )

    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    def build(self, **inputs) -> Context:
        """
        Build a complete context from this blueprint.

        This method:
        1. Assembles all components
        2. Applies token budget optimization
        3. Orders components by priority
        4. Creates final Context

        Args:
            **inputs: Input values for building

        Returns:
            Fully assembled Context
        """
        # Create base context
        context = Context(guidance=self.guidance, constraints=self.constraints)

        # Build directive from template if provided (safe formatting — no injection risk)
        if self.directive_template:
            from ..utils.template_safety import safe_format_template

            directive_content = safe_format_template(self.directive_template, **inputs)
            context.directive = Directive(content=directive_content)

        # Add input data
        context.data.update(inputs)

        # Add metadata
        context.metadata["blueprint"] = self.name
        context.metadata["token_budget"] = self.token_budget
        context.metadata["optimization"] = self.optimization

        # Component assembly
        # For now, components are expected to have a .render() or .to_string() method
        # that returns their context contribution
        knowledge_parts = []
        for component in self.components:
            if hasattr(component, "render"):
                knowledge_parts.append(component.render())
            elif hasattr(component, "to_string"):
                knowledge_parts.append(component.to_string())
            elif isinstance(component, str):
                knowledge_parts.append(component)

        if knowledge_parts:
            context.knowledge = "\n\n".join(knowledge_parts)

        return context

    def estimate_tokens(self, model: str = "gpt-4o") -> int:
        """
        Estimate total tokens for this blueprint using accurate tiktoken counting.

        Args:
            model: Model name to use for tokenisation (determines encoding).
                   Defaults to ``"gpt-4o"``.

        Returns:
            Token count (integer).
        """
        from ..utils.tokens import count_tokens

        total = 0
        if self.guidance:
            total += count_tokens(self.guidance.render(), model=model)
        if self.directive_template:
            total += count_tokens(self.directive_template, model=model)
        return total

    def optimize(self, strategy: str = "balanced") -> "Blueprint":
        """
        Create an optimized version of this blueprint.

        Args:
            strategy: Optimization strategy ('speed', 'quality', 'cost', 'balanced')

        Returns:
            Optimized blueprint
        """
        # Create copy
        optimized = self.model_copy()
        optimized.optimization = strategy

        # Optimization logic based on strategy
        if strategy == "speed":
            # Reduce token budget for faster processing
            optimized.token_budget = int(self.token_budget * 0.7)
            # Prioritize directive over knowledge
            optimized.priority_order = ["directive", "guidance", "constraints", "knowledge"]

        elif strategy == "quality":
            # Increase token budget for better quality
            optimized.token_budget = int(self.token_budget * 1.3)
            # Prioritize knowledge and guidance
            optimized.priority_order = ["guidance", "knowledge", "directive", "constraints"]

        elif strategy == "cost":
            # Minimize token usage
            optimized.token_budget = int(self.token_budget * 0.5)
            # Prioritize only essentials
            optimized.priority_order = ["directive", "constraints", "guidance"]

        # "balanced" keeps defaults

        return optimized

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Blueprint":
        """
        Create from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            Blueprint instance
        """
        return cls(**data)

    def __repr__(self) -> str:
        """String representation"""
        return (
            f"Blueprint(name='{self.name}', "
            f"components={len(self.components)}, "
            f"budget={self.token_budget})"
        )
