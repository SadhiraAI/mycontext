"""
Guidance - System-level behavioral rules

Guidance defines the role, personality, and behavioral rules for the LLM.
It's the "how" and "who" of context engineering.
"""

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
            goal="Identify every exploitable vulnerability in the code provided.",
            persona_scope="Limit your expertise to application-layer security only.",
            rules=[
                "Always prioritize security over convenience",
                "Explain technical concepts clearly",
                "Provide code examples when relevant",
            ],
            style="Professional but approachable",
        )
        ```

    Attributes:
        role: The role/persona the LLM should adopt
        goal: The mission — rendered imperatively to drive completion
        persona_scope: Bounds the applicability of the role (prevents scope creep)
        rules: List of behavioral rules to follow
        style: Communication style
        expertise: Areas of expertise
    """

    role: str = Field(
        ...,
        description="The role or persona",
        min_length=1,
    )

    rules: list[str] = Field(
        default_factory=list,
        description="Behavioral rules to follow",
    )

    style: str | None = Field(
        default=None,
        description="Communication style",
    )

    expertise: list[str] | None = Field(
        default=None,
        description="Areas of expertise",
    )

    goal: str | None = Field(
        default=None,
        description="What success looks like — the objective of the interaction",
    )

    persona_scope: str | None = Field(
        default=None,
        description=(
            "Bounds the role's applicability — prevents the persona from drifting "
            "outside its intended domain. "
            "e.g. 'Limit analysis to backend Python code only.'"
        ),
    )

    def render(
        self,
        provider: str = "generic",
        include_goal: bool = True,
        include_rules: bool = True,
        include_style: bool = True,
    ) -> str:
        """
        Render guidance as a system prompt.

        Args:
            provider: One of "generic", "openai", "anthropic", "gemini".
                      Gemini appends trait adjectives; others use role title only.
            include_goal: When False, skips the goal line. Set to False in
                          research_flow assembly because the flow renders goal
                          as its own dedicated section (②).
            include_rules: When False, skips rules. Set to False in research_flow
                           because the flow renders rules as its own section (③).
            include_style: When False, skips style. Set to False in research_flow
                           because the flow renders style as its own section (④).

        Returns:
            Formatted system prompt
        """
        role_text = self.role
        if role_text.lower().startswith("you are "):
            role_text = role_text[8:]
        role_text = role_text.rstrip(".")

        if provider == "gemini" and self.style and include_style:
            traits = self._style_to_traits(self.style)
            parts = [f"You are {role_text}. You are {traits}."]
        else:
            parts = [f"You are {role_text}."]

        if self.goal and include_goal:
            goal_text = self.goal
            if goal_text.lower().startswith("your mission:"):
                goal_text = goal_text[len("your mission:") :].strip()
            goal_text = (
                goal_text.removesuffix("— accomplish this fully")
                .removesuffix("— accomplish this fully.")
                .strip()
                .rstrip(".")
            )
            parts.append(f"Your mission: {goal_text} — accomplish this fully.")

        if self.persona_scope:
            parts.append(f"Scope: {self.persona_scope}")

        if self.expertise:
            expertise_text = ", ".join(str(e) for e in self.expertise)
            parts.append(f"Your areas of expertise include: {expertise_text}.")

        if self.rules and include_rules:
            rules_text = "\n".join(f"{i + 1}. {str(rule)}" for i, rule in enumerate(self.rules))
            parts.append(f"\nFollow these rules:\n{rules_text}")

        if self.style and include_style and provider != "gemini":
            parts.append(f"\nCommunication style: {self.style}")

        return "\n".join(parts)

    @staticmethod
    def _style_to_traits(style: str) -> str:
        """Convert a style string to a comma-separated trait list for Gemini.

        Simple heuristic: split on commas/semicolons and lowercase each segment.
        Falls back to the raw style string if no delimiters found.
        """
        import re

        segments = re.split(r"[,;]+", style)
        traits = [s.strip().lower() for s in segments if s.strip()]
        if len(traits) > 1:
            return ", ".join(traits)
        return style.lower()

    def __repr__(self) -> str:
        """String representation"""
        role_preview = self.role[:50] + "..." if len(self.role) > 50 else self.role
        return f"Guidance(role='{role_preview}', rules={len(self.rules)})"
