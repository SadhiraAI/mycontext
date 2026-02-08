"""
Pattern - Reusable context templates

Patterns are like functions in traditional programming - reusable,
composable units that encapsulate context engineering best practices.
"""

from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Field
import yaml
import json
from pathlib import Path

from ..foundation import Guidance, Directive, Constraints


class Pattern(BaseModel):
    """
    A reusable context template that encapsulates best practices.
    
    Patterns are the "functions" of context engineering. They define:
    - The structure of a context
    - Expected inputs and outputs
    - Default guidance and constraints
    - Optimization strategies
    
    Example:
        ```python
        # Define a pattern
        code_review = Pattern(
            name="code_review",
            guidance=Guidance(
                role="Expert code reviewer",
                rules=["Focus on security", "Suggest improvements"]
            ),
            input_schema={
                "code": str,
                "language": str,
                "focus_areas": list
            },
            output_schema={
                "issues": list,
                "score": float,
                "suggestions": list
            }
        )
        
        # Use the pattern
        result = code_review.execute(
            code=my_code,
            language="python",
            focus_areas=["security", "performance"]
        )
        ```
    
    Attributes:
        name: Pattern name/identifier
        description: What this pattern does
        guidance: Default guidance for this pattern
        directive_template: Template for directive (can use variables)
        constraints: Default constraints
        input_schema: Expected input structure
        output_schema: Expected output structure
        tags: Pattern categorization tags
        version: Pattern version
    """
    
    name: str = Field(
        ...,
        description="Pattern name/identifier",
        min_length=1
    )
    
    description: Optional[str] = Field(
        default=None,
        description="What this pattern does"
    )
    
    guidance: Optional[Guidance] = Field(
        default=None,
        description="Default guidance for this pattern"
    )
    
    directive_template: Optional[str] = Field(
        default=None,
        description="Template for directive (supports variables)"
    )
    
    constraints: Optional[Constraints] = Field(
        default=None,
        description="Default constraints"
    )
    
    input_schema: Dict[str, Type] = Field(
        default_factory=dict,
        description="Expected input structure"
    )
    
    output_schema: Dict[str, Type] = Field(
        default_factory=dict,
        description="Expected output structure"
    )
    
    tags: list[str] = Field(
        default_factory=list,
        description="Categorization tags"
    )
    
    version: str = Field(
        default="1.0.0",
        description="Pattern version"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    
    def build_context(self, **inputs) -> "Context":
        """
        Build a Context from this pattern with the given inputs.
        
        Args:
            **inputs: Input values matching input_schema
            
        Returns:
            Context instance ready to execute
            
        Raises:
            ValueError: If required inputs are missing
        """
        from ..core import Context
        
        # Validate inputs
        self._validate_inputs(inputs)
        
        # Build directive from template
        directive = None
        if self.directive_template:
            directive_content = self.directive_template.format(**inputs)
            directive = Directive(content=directive_content)
        
        # Create context
        context = Context(
            guidance=self.guidance,
            directive=directive,
            constraints=self.constraints,
            data=inputs
        )
        
        context.metadata["pattern"] = self.name
        context.metadata["pattern_version"] = self.version
        
        return context
    
    def execute(self, provider: str = "openai", **inputs) -> Any:
        """
        Execute this pattern directly.
        
        Args:
            provider: LLM provider to use
            **inputs: Input values (template inputs + provider kwargs like 'model')
            
        Returns:
            Execution result
        """
        # Separate template inputs from provider kwargs
        template_inputs = {}
        provider_kwargs = {}
        
        # Known provider parameters
        provider_params = {'model', 'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
                          'presence_penalty', 'stop', 'user', 'api_key', 'base_url'}
        
        for key, value in inputs.items():
            if key in provider_params:
                provider_kwargs[key] = value
            else:
                template_inputs[key] = value
        
        # Build context with template inputs only
        context = self.build_context(**template_inputs)
        
        # Execute with provider kwargs
        return context.execute(provider=provider, **provider_kwargs)
    
    def _validate_inputs(self, inputs: Dict[str, Any]) -> None:
        """
        Validate inputs against schema.
        
        Args:
            inputs: Input values to validate
            
        Raises:
            ValueError: If validation fails
        """
        # Check required fields
        for field_name, field_type in self.input_schema.items():
            if field_name not in inputs:
                raise ValueError(f"Missing required input: {field_name}")
            
            # Basic type checking
            if not isinstance(inputs[field_name], field_type):
                raise ValueError(
                    f"Input '{field_name}' must be {field_type.__name__}, "
                    f"got {type(inputs[field_name]).__name__}"
                )
    
    @classmethod
    def load(cls, name: str, library_path: Optional[Path] = None) -> "Pattern":
        """
        Load a pattern from the pattern library.
        
        Args:
            name: Pattern name
            library_path: Path to pattern library (default: built-in)
            
        Returns:
            Pattern instance
            
        Raises:
            FileNotFoundError: If pattern not found
        """
        if library_path is None:
            # Use built-in pattern library
            library_path = Path(__file__).parent.parent / "patterns"
        
        pattern_file = library_path / f"{name}.yaml"
        
        if not pattern_file.exists():
            raise FileNotFoundError(f"Pattern '{name}' not found")
        
        with open(pattern_file, 'r') as f:
            data = yaml.safe_load(f)
        
        return cls(**data)
    
    def save(self, path: Path) -> None:
        """
        Save pattern to file.
        
        Args:
            path: Where to save the pattern
        """
        with open(path, 'w') as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pattern":
        """
        Create from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Pattern instance
        """
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"Pattern(name='{self.name}', version={self.version})"


# Pre-built patterns will be loaded from YAML files
# For now, let's define a few in code

CODE_REVIEW_PATTERN = Pattern(
    name="code_review",
    description="Review code for quality, security, and best practices",
    guidance=Guidance(
        role="Expert code reviewer with 10+ years experience",
        rules=[
            "Focus on security vulnerabilities",
            "Check for performance issues",
            "Verify best practices are followed",
            "Suggest concrete improvements"
        ],
        style="Professional and constructive"
    ),
    directive_template="Review this {language} code:\n\n{code}\n\nFocus on: {focus_areas}",
    input_schema={
        "code": str,
        "language": str,
        "focus_areas": list
    },
    output_schema={
        "issues": list,
        "score": float,
        "suggestions": list
    },
    tags=["code", "review", "quality"]
)

DECISION_MATRIX_PATTERN = Pattern(
    name="decision_matrix",
    description="Multi-criteria decision analysis",
    guidance=Guidance(
        role="Strategic advisor and decision analyst",
        rules=[
            "Consider all options objectively",
            "Weight criteria appropriately",
            "Explain reasoning clearly",
            "Provide actionable recommendation"
        ]
    ),
    directive_template=(
        "Analyze this decision:\n\n"
        "Question: {question}\n"
        "Options: {options}\n"
        "Criteria: {criteria}\n"
        "Context: {context}"
    ),
    input_schema={
        "question": str,
        "options": list,
        "criteria": dict,
        "context": str
    },
    output_schema={
        "recommendation": str,
        "scores": dict,
        "reasoning": list
    },
    tags=["decision", "analysis", "business"]
)
