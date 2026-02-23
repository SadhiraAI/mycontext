"""
Constraints - Boundaries and guardrails

Constraints define hard limits and boundaries for LLM behavior.
They are the "must not" and "must" rules that cannot be violated.
"""


from pydantic import BaseModel, Field


class Constraints(BaseModel):
    """
    Hard constraints and guardrails for LLM behavior.

    Constraints are non-negotiable boundaries that the LLM must respect.
    They ensure safety, compliance, and adherence to requirements.

    Example:
        ```python
        constraints = Constraints(
            must_include=["error handling", "unit tests"],
            must_not_include=["deprecated APIs", "hardcoded secrets"],
            format_rules=["Use TypeScript", "Follow PEP 8"],
            max_length=1000
        )
        ```

    Attributes:
        must_include: Things that must be included
        must_not_include: Things that must not be included
        format_rules: Formatting and style rules
        max_length: Maximum output length
        language: Required output language
    """

    must_include: list[str] | None = Field(
        default=None,
        description="Elements that must be included"
    )

    must_not_include: list[str] | None = Field(
        default=None,
        description="Elements that must not be included"
    )

    format_rules: list[str] | None = Field(
        default=None,
        description="Formatting and style rules"
    )

    max_length: int | None = Field(
        default=None,
        ge=1,
        description="Maximum output length (tokens or characters)"
    )

    language: str | None = Field(
        default=None,
        description="Required output language"
    )

    output_schema: list[dict] | None = Field(
        default=None,
        description="Structured output schema — list of {'name': str, 'type': str} field definitions"
    )

    def render(self) -> str:
        """
        Render constraints as formatted text.

        Returns:
            Formatted constraints string
        """
        parts = ["CONSTRAINTS:"]

        if self.must_include:
            must_inc = "\n".join(f"  - {item}" for item in self.must_include)
            parts.append(f"Must include:\n{must_inc}")

        if self.must_not_include:
            must_not = "\n".join(f"  - {item}" for item in self.must_not_include)
            parts.append(f"Must NOT include:\n{must_not}")

        if self.format_rules:
            formats = "\n".join(f"  - {rule}" for rule in self.format_rules)
            parts.append(f"Format rules:\n{formats}")

        if self.output_schema:
            fields = [f for f in self.output_schema if f.get("name")]
            if fields:
                schema_lines = "\n".join(
                    f"  - {f['name']} ({f.get('type', 'str')})" for f in fields
                )
                parts.append(f"Output schema:\n{schema_lines}")

        if self.max_length:
            parts.append(f"Maximum length: {self.max_length}")

        if self.language:
            parts.append(f"Language: {self.language}")

        # Join sections with double newline so Markdown renders proper paragraph breaks
        return "\n\n".join(parts)

    def __repr__(self) -> str:
        """String representation"""
        rules_count = sum([
            len(self.must_include or []),
            len(self.must_not_include or []),
            len(self.format_rules or [])
        ])
        return f"Constraints({rules_count} rules)"
