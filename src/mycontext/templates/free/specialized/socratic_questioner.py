"""
Socratic Questioner Template - Question assumptions through structured inquiry.

Based on the Socratic method of inquiry through questioning.
Helps users examine beliefs, assumptions, and reasoning.

Depth parameter now drives a genuinely different directive per level:
  basic    — 2 categories: clarifying + assumptions
  detailed — 4 categories: + evidence + viewpoints + synthesis (default)
  thorough — all 6 categories + implications + meta questions + synthesis
"""

from __future__ import annotations

from mycontext.foundation import Directive, Guidance
from mycontext.structure import Pattern

VALID_DEPTHS: frozenset[str] = frozenset({"basic", "detailed", "thorough"})


def _build_directive(depth: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    cats = {
        "clarifying": (
            "**1. CLARIFYING QUESTIONS**\n"
            "   Probe the meaning and scope of the statement:\n"
            "   - Q1: What exactly do you mean by [key term]?\n"
            "   - Q2: Can you give a concrete example of this in practice?\n"
            "   - Q3: [Generate a third clarifying question specific to the statement]"
        ),
        "assumptions": (
            "**2. PROBING ASSUMPTIONS**\n"
            "   Surface what is being taken for granted:\n"
            "   - Q1: What are you assuming here that you have not stated?\n"
            "   - Q2: Why would someone believe that assumption holds in this case?\n"
            "   - Q3: What would change if the opposite assumption were true?"
        ),
        "evidence": (
            "**3. PROBING REASONS AND EVIDENCE**\n"
            "   Challenge the epistemic basis:\n"
            "   - Q1: What evidence would you point to in support of this?\n"
            "   - Q2: How do you know this is true rather than merely widely believed?\n"
            "   - Q3: What would it take to change your mind on this?"
        ),
        "viewpoints": (
            "**4. QUESTIONING VIEWPOINTS AND PERSPECTIVES**\n"
            "   Explore alternative framings:\n"
            "   - Q1: How would someone who disagrees with this view it?\n"
            "   - Q2: What are the strongest arguments against this position?\n"
            "   - Q3: What does this statement assume about the people or systems it describes?"
        ),
        "implications": (
            "**5. PROBING IMPLICATIONS AND CONSEQUENCES**\n"
            "   Follow the logical and practical consequences:\n"
            "   - Q1: If this is true, what else must necessarily follow?\n"
            "   - Q2: What unintended consequences might arise from acting on this belief?\n"
            "   - Q3: Who benefits and who is harmed if this assumption holds?"
        ),
        "meta": (
            "**6. QUESTIONING THE QUESTION**\n"
            "   Examine the inquiry itself:\n"
            "   - Q1: Why is this question worth asking now?\n"
            "   - Q2: What assumptions does the question itself contain?\n"
            "   - Q3: Is this the right question, or is there a better one beneath it?"
        ),
    }
    synthesis = (
        "**SYNTHESIS**\n"
        "   The questions above reveal:\n"
        "   - Core tension: [The central unresolved conflict or ambiguity]\n"
        "   - Key assumption to examine: [The one assumption that, if wrong, changes everything]\n"
        "   - Insight: [What deeper understanding the questioning process surfaces]"
    )

    configs = {
        "basic": {
            "keys": ["clarifying", "assumptions"],
            "include_synthesis": False,
            "instruction": (
                "Apply the two foundational Socratic moves: clarify what is meant, "
                "then surface what is being assumed. Generate 2\u20133 targeted questions per category."
            ),
            "total": "2 categories",
        },
        "detailed": {
            "keys": ["clarifying", "assumptions", "evidence", "viewpoints"],
            "include_synthesis": True,
            "instruction": (
                "Apply four Socratic categories: clarifying, assumptions, evidence, and "
                "alternative viewpoints. Generate 2\u20133 targeted questions per category, "
                "then synthesise the key insight the questioning reveals."
            ),
            "total": "4 categories + synthesis",
        },
        "thorough": {
            "keys": ["clarifying", "assumptions", "evidence", "viewpoints", "implications", "meta"],
            "include_synthesis": True,
            "instruction": (
                "Apply the full Socratic method across all six categories. "
                "Generate 2\u20133 penetrating questions per category, tailored to this specific "
                "statement. Then synthesise the core tension, the key assumption, and the "
                "deeper insight the inquiry reveals."
            ),
            "total": "6 categories + synthesis",
        },
    }
    cfg = configs.get(depth, configs["detailed"])
    categories_text = "\n\n".join(cats[k] for k in cfg["keys"])
    synthesis_text = f"\n\n{synthesis}" if cfg["include_synthesis"] else ""

    return (
        f'Apply Socratic questioning to examine this statement:\n\n"{{statement}}"\n\n'
        f"{{context_section}}\n\n"
        f"**DEPTH OF INQUIRY**: {depth} ({cfg['total']})\n\n"
        f"{cfg['instruction']}\n\n"
        f"For each category, generate questions targeted specifically at the statement above \u2014 "
        f"do not produce generic placeholder questions.\n\n"
        f"{categories_text}{synthesis_text}"
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------

class SocraticQuestioner(Pattern):
    """
    Socratic questioning for deep inquiry and assumption examination.

    Uses the Socratic method to question underlying assumptions, explore
    implications, examine evidence, and promote critical thinking.

    The **depth** parameter drives a genuinely different directive per level:

    - ``basic`` (2 categories): Clarifying + Assumptions.
      Fast — good for quick belief checks or warm-up facilitation.
    - ``detailed`` (4 categories + synthesis, default): + Evidence + Viewpoints.
      Good for most analytical, strategic, or ethical questions.
    - ``thorough`` (6 categories + synthesis): + Implications + Meta-questions.
      Good for deep philosophical inquiry, policy analysis, or debate prep.

    Examples:
        >>> questioner = SocraticQuestioner()
        >>> # Quick assumption check
        >>> result = questioner.execute(
        ...     provider="openai",
        ...     statement="AI will replace most knowledge workers within 10 years",
        ...     depth="basic",
        ... )
        >>> # Full Socratic examination
        >>> result = questioner.execute(
        ...     provider="openai",
        ...     statement="We should implement AI in our hiring process",
        ...     depth="thorough",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Apply the Socratic method to examine the following statement:\n\n"
        "Statement: {statement}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Generate probing questions to clarify meaning, surface unstated assumptions, "
        "challenge evidence and epistemic basis, explore alternative viewpoints, examine "
        "implications and consequences, and question the question itself.\n\n"
        "Generate 2\u20133 penetrating questions per category, then synthesise the core "
        "tension and key insight the inquiry reveals."
    )

    def __init__(self):
        super().__init__(
            name="socratic_questioner",
            description="Question assumptions and beliefs through Socratic dialogue",
            guidance=Guidance(
                role="Socratic Philosopher and Critical Thinking Expert",
                rules=[
                    "Ask probing questions rather than making statements",
                    "Question underlying assumptions systematically",
                    "Explore implications and consequences",
                    "Challenge reasoning with evidence",
                    "Guide toward deeper understanding through inquiry",
                    "Be respectful and intellectually humble",
                    "Focus on clarifying thinking, not attacking the person",
                ],
                style="inquisitive, patient, thought-provoking",
            ),
            directive_template=_build_directive("detailed"),
            input_schema={
                "statement": str,
                "context_section": str,
                "depth": str,
            },
        )

    def _render_context_section(self, context: str) -> str:
        if not context or context.strip() == "":
            return ""
        return f"\nAdditional Context:\n{context}\n"

    def build_context(
        self,
        statement: str,
        context: str = "",
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Build a context for Socratic questioning.

        Args:
            statement: The claim, belief, or position to examine
            context: Optional additional context
            depth: Level of inquiry — ``"basic"`` | ``"detailed"`` (default)
                | ``"thorough"``
            **kwargs: Additional parameters

        Returns:
            Context configured for Socratic questioning
        """
        if depth not in VALID_DEPTHS:
            raise ValueError(
                f"Invalid depth {depth!r}. Choose from: {sorted(VALID_DEPTHS)}"
            )
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        directive_text = _build_directive(depth)
        directive_content = safe_format_template(
            directive_text, statement=statement, context_section=context_section, depth=depth
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"statement": statement, "context_section": context_section, "depth": depth},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["depth"] = depth
        return ctx

    def execute(
        self,
        provider: str = "openai",
        statement: str = None,
        context: str = "",
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Execute Socratic questioning.

        Args:
            provider: LLM provider to use
            statement: The claim to examine
            context: Optional additional context
            depth: Level of inquiry — ``"basic"`` | ``"detailed"`` (default)
                | ``"thorough"``
            **kwargs: Provider parameters (model, temperature, max_tokens, etc.)

        Returns:
            Provider response with Socratic questions and insights
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(statement=statement, context=context, depth=depth)
        return ctx.execute(provider=provider, **provider_kwargs)
