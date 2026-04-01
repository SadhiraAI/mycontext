"""
Conflict Resolver - Resolve conflicts and disagreements

Systematic conflict resolution using proven frameworks.
Based on conflict resolution theory and mediation practices.
"""

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern
from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive


class ConflictResolver(Pattern):
    """
    Resolve conflicts systematically.

    Addresses:
    - Interpersonal conflicts
    - Team disagreements
    - Stakeholder conflicts
    - Value conflicts
    - Resource conflicts

    Based on: Conflict resolution theory and mediation

    Example:
        >>> resolver = ConflictResolver()
        >>> context = resolver.build_context(
        ...     conflict="Team disagrees on technical approach",
        ...     parties=["Engineering team", "Product team"]
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Analyze and resolve the following conflict:\n\n"
        "Conflict: {conflict}\n"
        "Parties involved: {parties}\n"
        "{context_section}\n\n"
        "Classify the conflict type, map each party's position and underlying interests, "
        "identify common ground and root causes, generate resolution options (compromise, "
        "collaboration, creative reframe), and recommend the best resolution with "
        "implementation steps and a follow-up plan.\n\n"
        "Stay neutral. Understand all perspectives before proposing solutions."
    )

    def __init__(self):
        super().__init__(
            name="conflict_resolver",
            description="Resolve conflicts systematically",
            guidance=Guidance(
                role="Expert Mediator and Conflict Resolution Specialist",
                rules=[
                    "Do not favor the party who framed the conflict. Present both perspectives with equal rigor.",
                    "Stay neutral and objective",
                    "Understand all perspectives",
                    "Find common ground",
                    "Focus on interests, not positions",
                    "Seek win-win solutions",
                ],
                style="diplomatic, empathetic, solution-focused",
            ),
            directive_template="""Resolve this conflict:

**CONFLICT**: {conflict}

**PARTIES INVOLVED**: {parties}

{context_section}

Conflict resolution:

1. **CONFLICT ANALYSIS**
   - Type: [Interpersonal/Resource/Value/Process]
   - Severity: [High/Medium/Low]
   - Duration: [How long]
   - Triggers: [What sparked it]

2. **PERSPECTIVES**
   **Party A viewpoint**:
   - Position: [What they want]
   - Interests: [Why they want it]
   - Concerns: [What worries them]
   
   **Party B viewpoint**:
   - [Same structure]

3. **COMMON GROUND**
   What they agree on:
   - Shared goal: [Mutual objective]
   - Shared values: [Common beliefs]
   - Shared constraints: [Common limitations]

4. **ROOT CAUSES**
   Underlying issues:
   - Cause 1: [Real issue]
   - Cause 2: [Another factor]

5. **RESOLUTION OPTIONS**
   **Option A** (Compromise):
   - [Solution]
   - Pros/Cons
   
   **Option B** (Collaboration):
   - [Win-win solution]
   - Pros/Cons
   
   **Option C** (Creative):
   - [Novel approach]
   - Pros/Cons

6. **RECOMMENDED RESOLUTION**
   - Solution: [Best approach]
   - Why: [Rationale]
   - Implementation: [How to execute]
   - Follow-up: [Ensure it sticks]

**OUTPUT FORMAT**: Balanced resolution with implementation plan.""",
            input_schema={"conflict": str, "parties": str, "context_section": str},
            constraints=Constraints(
                must_include=["perspectives", "common_ground", "resolution"],
                style_guide="Be neutral and constructive",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        conflict: str = "",
        parties: str = "",
        context: str | None = None,
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Build context for conflict resolution.

        Args:
            conflict: Description of the conflict
            parties: Parties involved (string or comma-separated list)
            context: Optional additional context
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"`` | ``"table"``
        """
        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )
        context_section = self._render_context_section(context)
        ctx = super().build_context(
            conflict=conflict,
            parties=parties,
            context_section=context_section,
            **kwargs,
        )
        fmt = get_format_directive(output_format)
        if fmt and ctx.directive:
            ctx.directive = Directive(content=ctx.directive.content + fmt)
            ctx.metadata["output_format"] = output_format
        self._apply_default_self_check(
            ctx,
            [
                "Would both parties feel fairly represented?",
                "Am I favoring the party who framed the question?",
            ],
        )
        if ctx.examples is None:
            ctx.examples = [
                {
                    "input": "Marketing wants to launch next week but Engineering says the feature is not ready",
                    "output": (
                        "MARKETING'S POSITION: Revenue target at risk; competitor launching similar feature.\n"
                        "ENGINEERING'S POSITION: Two critical bugs remain; launching risks customer trust.\n"
                        "COMMON GROUND: Both want the product to succeed long-term.\n"
                        "RECOMMENDATION: Launch with a controlled rollout (10% of users) next week — "
                        "Marketing meets their date, Engineering gets real usage data on the bugs "
                        "before full exposure."
                    ),
                }
            ]
        return ctx

    def execute(
        self,
        provider: str = "openai",
        conflict: str = "",
        parties: str = "",
        context: str | None = None,
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Execute conflict resolution.

        Args:
            provider: LLM provider to use
            conflict: Description of the conflict
            parties: Parties involved
            context: Optional additional context
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"`` | ``"table"``
        """
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
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            conflict=conflict,
            parties=parties,
            context=context,
            output_format=output_format,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
