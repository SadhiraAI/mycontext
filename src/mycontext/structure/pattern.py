"""
Pattern - Reusable context templates

Patterns are like functions in traditional programming - reusable,
composable units that encapsulate context engineering best practices.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import yaml
from pydantic import BaseModel, Field

from ..foundation import Constraints, Directive, Guidance

if TYPE_CHECKING:
    from ..core import Context


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

    name: str = Field(..., description="Pattern name/identifier", min_length=1)

    description: str | None = Field(default=None, description="What this pattern does")

    guidance: Guidance | None = Field(default=None, description="Default guidance for this pattern")

    directive_template: str | None = Field(
        default=None, description="Template for directive (supports variables)"
    )

    constraints: Constraints | None = Field(default=None, description="Default constraints")

    input_schema: dict[str, type] = Field(
        default_factory=dict, description="Expected input structure"
    )

    output_schema: dict[str, type] = Field(
        default_factory=dict, description="Expected output structure"
    )

    tags: list[str] = Field(default_factory=list, description="Categorization tags")

    version: str = Field(default="1.0.0", description="Pattern version")

    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    GENERIC_PROMPT: ClassVar[str | None] = None

    def generic_prompt(self, **kwargs) -> str:
        """Return a concise, pre-authored prompt that captures this template's essence.

        Generic prompts are static, hand-crafted paragraphs (~600-1200 chars)
        that distill the template's core methodology into a self-contained prompt
        any LLM can execute directly.  User inputs are injected via keyword
        arguments matching the template's ``build_context`` signature.

        Two modes are available to users:
          * **generic** — fast, zero-cost, lighter prompt (this method)
          * **full**    — the rich, structured directive template (``build_context``)

        Raises:
            NotImplementedError: If the template has no generic prompt defined.
        """
        if self.GENERIC_PROMPT is None:
            raise NotImplementedError(
                f"Template '{self.name}' does not have a generic prompt. "
                "Use build_context() for the full template instead."
            )
        filled = self.GENERIC_PROMPT
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            if placeholder in filled:
                filled = filled.replace(placeholder, str(value))

        import re

        filled = re.sub(r"\{context_section\}", "", filled)
        filled = re.sub(r"\n{3,}", "\n\n", filled).strip()
        return filled

    @staticmethod
    def _apply_default_self_check(ctx: Context, defaults: list[str]) -> None:
        """Set default self_check on a Context's constraints if not already set.

        If the Context has no constraints, creates one with just self_check.
        If constraints exist but self_check is None, sets the defaults.
        If self_check is already set (user-provided), leaves it untouched.
        """
        if ctx.constraints is None:
            ctx.constraints = Constraints(self_check=defaults)
        elif ctx.constraints.self_check is None:
            ctx.constraints = ctx.constraints.model_copy(update={"self_check": defaults})

    def build_context(self, output_format: str = "structured", **inputs) -> Context:
        """
        Build a Context from this pattern with the given inputs.

        Args:
            output_format: Controls presentation style of the LLM response.
                Human formats: "structured" (default), "narrative", "brief",
                "actionable", "slides", "email", "qa", "checklist".
                Machine formats: "json", "table".
            **inputs: Input values matching input_schema

        Returns:
            Context instance ready to execute

        Raises:
            ValueError: If required inputs are missing or output_format is invalid
        """
        from ..core import Context
        from ..utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive

        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )

        # Validate inputs
        self._validate_inputs(inputs)

        # Build directive from template (safe formatting — no injection risk)
        directive = None
        if self.directive_template:
            from ..utils.template_safety import safe_format_template

            directive_content = safe_format_template(self.directive_template, **inputs)
            fmt = get_format_directive(output_format)
            if fmt:
                directive_content += fmt
            directive = Directive(content=directive_content)

        # Create context
        context = Context(
            guidance=self.guidance, directive=directive, constraints=self.constraints, data=inputs
        )

        context.metadata["pattern"] = self.name
        context.metadata["pattern_version"] = self.version
        context.metadata["output_format"] = output_format

        return context

    def execute(
        self,
        provider: str = "openai",
        mode: str = "full",
        output_format: str = "structured",
        **inputs,
    ) -> Any:
        """
        Execute this pattern directly.

        Args:
            provider: LLM provider to use
            mode: "full" for the rich template, "generic" for the concise prompt
            output_format: Controls presentation style of the LLM response.
                Human formats: "structured" (default), "narrative", "brief",
                "actionable", "slides", "email", "qa", "checklist".
                Machine formats: "json", "table".
            **inputs: Input values (template inputs + provider kwargs like 'model')

        Returns:
            Execution result
        """
        from ..utils.format_directives import is_machine_format

        template_inputs = {}
        provider_kwargs = {}

        provider_params = {
            "model",
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "user",
            "api_key",
            "base_url",
        }

        for key, value in inputs.items():
            if key in provider_params:
                provider_kwargs[key] = value
            else:
                template_inputs[key] = value

        # Machine formats work best at low temperature
        if is_machine_format(output_format) and "temperature" not in provider_kwargs:
            provider_kwargs["temperature"] = 0.0

        if mode == "generic":
            from ..core import Context
            from ..utils.format_directives import get_format_directive

            prompt_text = self.generic_prompt(**template_inputs)
            fmt = get_format_directive(output_format)
            if fmt:
                prompt_text += fmt
            ctx = Context(directive=Directive(content=prompt_text))
            ctx.metadata["output_format"] = output_format
            return ctx.execute(provider=provider, **provider_kwargs)

        context = self.build_context(output_format=output_format, **template_inputs)
        return context.execute(provider=provider, **provider_kwargs)

    def _validate_inputs(self, inputs: dict[str, Any]) -> None:
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
    def load(cls, name: str, library_path: Path | None = None) -> Pattern:
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

        with open(pattern_file) as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def save(self, path: Path) -> None:
        """
        Save pattern to file.

        Args:
            path: Where to save the pattern
        """
        with open(path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Pattern:
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
