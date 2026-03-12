"""
Brainstormer - Structured brainstorming facilitation.

Facilitates productive brainstorming sessions using proven techniques.
Based on creative facilitation and group ideation research.

mode parameter controls the brainstorming approach:
  divergent — full structured session (14 sections, default)
  focused   — lean idea generation + clustering + top picks (5 sections)
  reverse   — reverse brainstorm only: what makes it worse? then flip it
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_MODES: frozenset[str] = frozenset({"divergent", "focused", "reverse"})


def _build_directive(mode: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    s = {
        "framing": (
            "1. **TOPIC FRAMING**\n"
            "   Clarify what we are brainstorming:\n"
            "   - Core challenge: {topic}\n"
            "   - Success looks like: [Description of a good outcome]\n"
            "   - Out of scope: [What we are NOT solving today]\n"
            "   - Why this matters: [Importance and stakes]"
        ),
        "rules": (
            "2. **GROUND RULES**\n"
            "   \u2705 Generate lots of ideas | Build on existing ones | Go wild and creative\n"
            "   \u274c No criticism during generation | No forcing justification | No going off-topic"
        ),
        "rapid": (
            "3. **RAPID IDEA GENERATION**\n"
            "   Quick-fire ideas \u2014 aim for 30+. No filtering yet.\n"
            "   1. [Idea 1]\n"
            "   2. [Idea 2]\n"
            "   3. [Idea 3]\n"
            "   ...continue to 30+"
        ),
        "build_on": (
            "4. **BUILD-ON SESSION**\n"
            "   Pick 3 promising ideas from above and extend each:\n"
            "   **Base Idea A**: [From above]\n"
            "   - Yes, and... [Extension]\n"
            "   - What if we... [Variation]\n"
            "   - Combining with... [Hybrid]\n\n"
            "   **Base Idea B**: [Another one]\n"
            "   - [Same structure]\n\n"
            "   **Base Idea C**: [Third one]\n"
            "   - [Same structure]"
        ),
        "random_stimulus": (
            "6. **RANDOM STIMULUS**\n"
            '   Pick an unrelated concept (e.g. "bridge", "jazz", "hospital") and force connections:\n'
            "   - Connection 1: [Unexpected link to topic]\n"
            "   - Connection 2: [Creative association]\n"
            "   - Connection 3: [Novel approach this inspires]"
        ),
        "role_play": (
            "7. **ROLE PLAY IDEATION**\n"
            "   What would these people suggest?\n"
            "   - **A 10-year-old**: [Innocent, simple idea]\n"
            "   - **A competitor**: [What a rival might do]\n"
            "   - **Someone from 10 years in the future**: [Long-term view]\n"
            "   - **Someone who hates the current approach**: [Contrarian perspective]"
        ),
        "constraint_removal": (
            "8. **CONSTRAINT REMOVAL (MOONSHOTS)**\n"
            "   If we had unlimited resources / no regulations / no legacy systems:\n"
            "   - Moonshot 1: [Dream solution]  \u2192  Scaled down: [Realistic version]\n"
            "   - Moonshot 2: [Impossible idea] \u2192  Scaled down: [Achievable form]\n"
            "   - Moonshot 3: [No-limits idea]  \u2192  Scaled down: [Implementable variant]"
        ),
        "category": (
            "9. **CATEGORY EXPLORATION**\n"
            "   Generate 2 ideas per category:\n"
            "   - **Technology-based**: [Idea], [Idea]\n"
            "   - **Process-based**: [Idea], [Idea]\n"
            "   - **People-based**: [Idea], [Idea]\n"
            "   - **Partnership-based**: [Idea], [Idea]"
        ),
    }

    def _reverse(n: int) -> str:
        return (
            f"{n}. **REVERSE BRAINSTORM**\n"
            "   How could we make this WORSE? (Then flip the answers into solutions)\n"
            "   - Bad idea 1: [Guaranteed to fail]  \u2192  Flipped: [What this suggests doing instead]\n"
            "   - Bad idea 2: [Terrible approach]   \u2192  Flipped: [Useful insight from the inverse]\n"
            "   - Bad idea 3: [Worst possible]      \u2192  Flipped: [Creative solution]"
        )

    def _clustering(n: int) -> str:
        return (
            f"{n}. **IDEA CLUSTERING**\n"
            "   Group related ideas into themes:\n"
            "   - **Cluster 1 \u2014 [Theme name]**: [Ideas] | Core concept: [Unifying principle]\n"
            "   - **Cluster 2 \u2014 [Theme name]**: [Ideas] | Core concept: [Common thread]\n"
            "   - **Cluster 3 \u2014 [Theme name]**: [Ideas] | Core concept: [Shared element]"
        )

    def _voting(n: int) -> str:
        return (
            f"{n}. **PRIORITISATION**\n"
            "   | Idea | Impact | Feasibility | Novelty | Overall |\n"
            "   |------|--------|-------------|---------|--------|\n"
            "   | [Idea A] | H/M/L | H/M/L | H/M/L | \u2b50\u2b50\u2b50\u2b50\u2b50 |\n"
            "   | [Idea B] | H/M/L | H/M/L | H/M/L | \u2b50\u2b50\u2b50\u2b50 |"
        )

    def _top_ideas(n: int) -> str:
        return (
            f"{n}. **TOP IDEAS REFINEMENT**\n"
            "   Polish the top 3 winners:\n"
            "   **Idea #1 \u2014 [Name it]**:\n"
            "   - What it is: [Clear description]\n"
            "   - Why promising: [The core insight]\n"
            "   - How to test it: [Cheapest validation approach]\n"
            "   - First step: [Immediate action]\n\n"
            "   **Idea #2 \u2014 [Name it]**: [Same structure]\n"
            "   **Idea #3 \u2014 [Name it]**: [Same structure]"
        )

    def _dark_horses(n: int) -> str:
        return (
            f"{n}. **DARK HORSES**\n"
            "   Unusual ideas worth keeping on the radar:\n"
            "   - Dark Horse 1: [Weird but intriguing] \u2014 Why it could work: [Potential]\n"
            "   - Dark Horse 2: [Another unconventional idea]"
        )

    def _next_steps(n: int) -> str:
        return (
            f"{n}. **NEXT STEPS**\n"
            "   - [ ] Test: [Cheapest way to validate the top idea]\n"
            "   - [ ] Research: [What needs investigation first]\n"
            "   - [ ] Decision: [Who needs to greenlight the top pick and when]"
        )

    if mode == "focused":
        sections_list = [
            s["framing"], s["rapid"], _reverse(3), _clustering(4), _top_ideas(5),
        ]
        instruction = (
            "Run a lean, high-signal brainstorm. Frame the challenge, generate "
            "30+ ideas rapidly, apply reverse brainstorming to stress-test them, "
            "cluster into themes, and surface the top 3 with clear next steps."
        )
        total = "5 sections"
    elif mode == "reverse":
        sections_list = [s["framing"], _reverse(2)]
        instruction = (
            "Apply reverse brainstorming only. Ask: what would make this problem "
            "WORSE? Generate 5-8 bad ideas, then flip each one into a potential "
            "solution or insight."
        )
        total = "2 sections (reverse brainstorm only)"
    else:
        sections_list = [
            s["framing"], s["rules"], s["rapid"], s["build_on"], _reverse(5),
            s["random_stimulus"], s["role_play"], s["constraint_removal"], s["category"],
            _clustering(10), _voting(11), _top_ideas(12), _dark_horses(13), _next_steps(14),
        ]
        instruction = (
            "Facilitate a comprehensive divergent brainstorming session. "
            "Apply every technique: rapid ideation, build-on, reverse brainstorm, "
            "random stimulus, role-play, constraint removal, and category exploration. "
            "Then converge: cluster, prioritise, refine the top 3, and capture dark horses."
        )
        total = "14 sections"

    sections_text = "\n\n".join(sections_list)
    return (
        f"Facilitate brainstorming on:\n\n"
        f"**TOPIC**: {{topic}}\n\n"
        f"{{context_section}}\n\n"
        f"**GOAL**: {{goal}}\n\n"
        f"**CONSTRAINTS**:\n{{constraints_section}}\n\n"
        f"**MODE**: {mode} ({total})\n\n"
        f"{instruction}\n\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Energetic brainstorm with diverse, specific ideas and clear next steps."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------

class Brainstormer(Pattern):
    """
    Facilitate structured brainstorming using proven ideation techniques.

    The **mode** parameter controls the brainstorming approach:

    - ``divergent`` (14 sections, default): Full structured session — framing,
      rapid ideation (30+ ideas), build-on, reverse brainstorm, random stimulus,
      role-play, moonshots, category exploration, clustering, prioritisation,
      top-3 refinement, dark horses, and next steps.  Use for open-ended
      exploration where breadth and creative coverage matter.
    - ``focused`` (5 sections): Framing → rapid generation → reverse brainstorm
      → clustering → top-3.  ~65% fewer sections.  Use when you need actionable
      ideas quickly or when the problem is well-scoped.
    - ``reverse`` (2 sections): Framing + reverse brainstorm only — what makes
      this WORSE? then flip it.  Use as a standalone constraint-challenge tool
      when you already have ideas and want to stress-test or complement them.

    Examples:
        >>> brainstormer = Brainstormer()
        >>> # Full divergent session
        >>> result = brainstormer.execute(
        ...     provider="openai",
        ...     topic="Ways to reduce customer churn in the first 30 days",
        ...     mode="divergent",
        ... )
        >>> # Focused — ideas fast
        >>> result = brainstormer.execute(
        ...     provider="openai",
        ...     topic="Marketing ideas for a developer tools launch",
        ...     mode="focused",
        ... )
        >>> # Stress-test existing ideas
        >>> result = brainstormer.execute(
        ...     provider="openai",
        ...     topic="Our plan to launch a freemium tier",
        ...     mode="reverse",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Conduct a structured brainstorming session on the following:\n\n"
        "Topic: {topic}\n"
        "Goal: {goal}\n"
        "{context_section}\n"
        "Constraints: {constraints}\n\n"
        "Generate ideas using divergent-then-convergent thinking: produce a large "
        "quantity of ideas rapidly, build on the most promising ones, cluster them "
        "into themes, evaluate and prioritise, then surface the top 3 with a next step "
        "and 1-2 unconventional dark horse ideas.\n\n"
        "Prioritise quantity and diversity. Defer judgment during generation."
    )

    def __init__(self):
        super().__init__(
            name="brainstormer",
            description="Structured brainstorming facilitation",
            guidance=Guidance(
                role="Expert Creative Facilitator and Brainstorming Specialist",
                rules=[
                    "Generate quantity first, quality later",
                    "No criticism during generation phase",
                    "Build on ideas — 'yes, and' thinking",
                    "Encourage wild and unusual ideas",
                    "Stay focused on the topic",
                    "Every idea deserves to be written down",
                ],
                style="energetic, open, encouraging",
            ),
            directive_template=_build_directive("divergent"),
            input_schema={
                "topic": str,
                "context_section": str,
                "goal": str,
                "constraints_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "diverse_ideas",
                    "prioritisation",
                    "next_steps",
                ],
                style_guide="Be enthusiastic, encouraging, and non-judgmental",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_constraints_section(self, constraints: list | None) -> str:
        if constraints:
            return "\n".join(f"- {c}" for c in constraints)
        return "- None specified"

    def build_context(
        self,
        topic: str = "",
        goal: str = "Generate creative solutions",
        context: str | None = None,
        constraints: list | None = None,
        mode: str = "divergent",
        **kwargs,
    ):
        """
        Build context for brainstorming.

        Args:
            topic: The brainstorming topic or problem
            goal: What a successful brainstorm would achieve
            context: Optional background context
            constraints: Optional list of constraints to work within
            mode: Brainstorming approach — ``"divergent"`` (default, 14 sections)
                | ``"focused"`` (5 sections) | ``"reverse"`` (2 sections)
        """
        if mode not in VALID_MODES:
            raise ValueError(
                f"Invalid mode {mode!r}. Choose from: {sorted(VALID_MODES)}"
            )
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        constraints_section = self._render_constraints_section(constraints)
        directive_text = _build_directive(mode)
        directive_content = safe_format_template(
            directive_text,
            topic=topic,
            goal=goal,
            context_section=context_section,
            constraints_section=constraints_section,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={
                "topic": topic, "goal": goal,
                "context_section": context_section,
                "constraints_section": constraints_section,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["mode"] = mode
        return ctx

    def execute(
        self,
        provider: str = "openai",
        topic: str = "",
        goal: str = "Generate creative solutions",
        context: str | None = None,
        constraints: list | None = None,
        mode: str = "divergent",
        **kwargs,
    ):
        """
        Execute brainstorming.

        Args:
            provider: LLM provider to use
            topic: The brainstorming topic
            goal: What success looks like
            context: Optional background context
            constraints: Optional list of constraints
            mode: ``"divergent"`` (default) | ``"focused"`` | ``"reverse"``
            **kwargs: Provider parameters (model, temperature, max_tokens, etc.)
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            topic=topic, goal=goal, context=context,
            constraints=constraints, mode=mode,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
