"""
Constraints - Boundaries and guardrails

Constraints define hard limits and boundaries for LLM behavior.
They are the "must not" and "must" rules that cannot be violated.
"""

from __future__ import annotations

from typing import Literal

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
            output_contract="Return ONLY a JSON object. No prose, no markdown wrapper.",
            style_guide="Formal, third-person, present tense.",
            max_length=1000,
        )
        ```

    Attributes:
        must_include: Things that must be included
        must_not_include: Things that must not be included — rendered as positive redirects
        format_rules: Formatting and style rules
        output_contract: Explicit contract for what the response must look like
        style_guide: Tone, voice, and prose style requirements (separate from format_rules)
        max_length: Maximum output length
        language: Required output language
        output_schema: Structured field schema for JSON responses
        verbosity: Output detail level — auto-suggested by PromptArchitect, user-overridable
        communication_posture: Interaction tone — auto-suggested by PromptArchitect
        forbidden_phrases: Phrases the LLM must never use in output
        answer_first: Whether to lead with the conclusion before reasoning
        self_check: Domain-specific verification questions the LLM applies before responding
    """

    must_include: list[str] | None = Field(
        default=None,
        description="Elements that must be included",
    )

    must_not_include: list[str] | None = Field(
        default=None,
        description="Elements that must not be included",
    )

    format_rules: list[str] | None = Field(
        default=None,
        description="Formatting and style rules",
    )

    output_contract: str | None = Field(
        default=None,
        description=(
            "Explicit output contract — what the final response must look like. "
            "e.g. 'Return ONLY a JSON object. No prose, no markdown wrapper.'"
        ),
    )

    style_guide: str | None = Field(
        default=None,
        description=(
            "Tone, voice, and prose style — separate from structural format_rules. "
            "e.g. 'Formal, third-person, present tense. Avoid hedging language.'"
        ),
    )

    max_length: int | None = Field(
        default=None,
        ge=1,
        description="Maximum output length (tokens or characters)",
    )

    language: str | None = Field(
        default=None,
        description="Required output language",
    )

    output_schema: list[dict] | None = Field(
        default=None,
        description="Structured output schema — list of {'name': str, 'type': str} field definitions",
    )

    verbosity: Literal["minimal", "standard", "detailed"] | None = Field(
        default=None,
        description=(
            "Output detail level. 'minimal' for quick decisions, "
            "'standard' for most tasks, 'detailed' for deep analysis. "
            "Auto-suggested by PromptArchitect based on task context."
        ),
    )

    communication_posture: Literal["direct", "collaborative", "educational"] | None = Field(
        default=None,
        description=(
            "Interaction tone. 'direct' for experienced audiences, "
            "'collaborative' for brainstorming, 'educational' for learning. "
            "Auto-suggested by PromptArchitect based on task context."
        ),
    )

    forbidden_phrases: list[str] | None = Field(
        default=None,
        description=(
            "Phrases the LLM must never use in its response. "
            "Auto-suggested by PromptArchitect; extends the built-in anti-boilerplate list."
        ),
    )

    answer_first: bool | None = Field(
        default=None,
        description=(
            "When True, the LLM states its conclusion/answer before supporting reasoning. "
            "Auto-suggested by PromptArchitect: True for decisions/analysis, False for tutorials."
        ),
    )

    self_check: list[str] | None = Field(
        default=None,
        description=(
            "Domain-specific verification questions the LLM must check before finalizing. "
            "Auto-suggested by PromptArchitect based on task failure modes."
        ),
    )

    def render_quality_segments(self) -> list[str]:
        """Narrative paragraphs for 0.11+ quality fields.

        Used by :meth:`render` and by research-flow assembly (GUARD RAILS) so
        ``verbosity``, ``communication_posture``, ``answer_first``,
        ``forbidden_phrases``, and ``self_check`` appear in ``assemble()`` when
        ``research_flow=True``.
        """
        segments: list[str] = []

        if self.verbosity == "minimal":
            segments.append(
                "Be concise. Lead with the essential answer. "
                "Omit preamble, filler, and restatements of the question."
            )
        elif self.verbosity == "detailed":
            segments.append(
                "Provide thorough analysis with supporting evidence, "
                "examples, and alternative perspectives where relevant."
            )

        if self.communication_posture == "direct":
            segments.append("Respond directly. Skip meta-commentary about your process.")
        elif self.communication_posture == "collaborative":
            segments.append(
                "Use a collaborative tone. Propose options, invite refinement, "
                "and frame suggestions as starting points."
            )
        elif self.communication_posture == "educational":
            segments.append(
                "Explain your reasoning. Define terms that may be unfamiliar. "
                "Use analogies where they aid understanding."
            )

        if self.answer_first is True:
            segments.append(
                "State your conclusion or answer first, then provide supporting reasoning."
            )

        if self.forbidden_phrases:
            phrase_list = ", ".join(f'"{p}"' for p in self.forbidden_phrases)
            segments.append(f"Do NOT use these phrases in your response: {phrase_list}")

        if self.self_check:
            checks = "\n".join(f"  - {c}" for c in self.self_check)
            segments.append(f"SELF-VERIFICATION — before finalizing, confirm:\n{checks}")

        return segments

    def render(self, provider: str = "generic") -> str:
        """
        Render constraints as formatted text.

        Args:
            provider: One of "generic", "openai", "anthropic", "gemini".
                      Adjusts constraint phrasing style to match provider preferences.

        Returns:
            Formatted constraints string
        """
        parts = ["CONSTRAINTS:"]

        if self.output_contract:
            parts.append(f"Output contract: {self.output_contract}")

        if self.style_guide:
            parts.append(f"Style: {self.style_guide}")

        if self.must_include:
            must_inc = "\n".join(f"  - {item}" for item in self.must_include)
            parts.append(f"Must include:\n{must_inc}")

        if self.must_not_include:
            parts.append(self._render_exclusions(self.must_not_include, provider))

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

        parts.extend(self.render_quality_segments())

        return "\n\n".join(parts)

    @staticmethod
    def _render_exclusions(items: list[str], provider: str) -> str:
        """Render must_not_include with provider-appropriate phrasing.

        - anthropic / gemini: positive reframe — "Omit X; use Y instead" style
        - openai / generic: direct imperative — "Exclude: X"
        """
        if provider in ("anthropic", "gemini"):
            lines = "\n".join(f"  - Omit {item}." for item in items)
            return f"Exclude the following (use alternatives where needed):\n{lines}"
        else:
            lines = "\n".join(f"  - {item}" for item in items)
            return f"Must NOT include:\n{lines}"

    def __repr__(self) -> str:
        """String representation"""
        rules_count = sum(
            [
                len(self.must_include or []),
                len(self.must_not_include or []),
                len(self.format_rules or []),
            ]
        )
        return f"Constraints({rules_count} rules)"
