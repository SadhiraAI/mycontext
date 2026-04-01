"""
Innovation Framework - Systematic innovation methodology

Structured innovation process using proven frameworks.
Based on innovation theory and design thinking.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class InnovationFramework(Pattern):
    """
    Apply systematic innovation framework.

    Uses:
    - Design thinking
    - Jobs-to-be-done
    - Blue ocean strategy
    - Innovation pipeline

    Based on: Innovation theory and design thinking

    Example:
        >>> framework = InnovationFramework()
        >>> context = framework.build_context(
        ...     challenge="Disrupt traditional banking",
        ...     context="Fintech startup"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert innovation strategist. Apply a systematic "
        "innovation framework to the following challenge:\n\n"
        "Challenge: {challenge}\n"
        "{context_section}\n\n"
        "Apply this methodology: "
        "(1) Reframe the problem - challenge existing assumptions and "
        "redefine the problem space to uncover hidden opportunities. "
        "(2) Jobs-to-be-done analysis - identify what users are really trying "
        "to accomplish, including their functional, emotional, and social "
        "jobs. "
        "(3) Blue ocean exploration - look beyond current market boundaries "
        "for uncontested spaces where competition is irrelevant. "
        "(4) Innovation types - consider incremental improvements, adjacent "
        "expansions, and transformational breakthroughs across the innovation "
        "spectrum. "
        "(5) Feasibility assessment - evaluate each innovation concept on "
        "novelty, feasibility (can we build it?), viability (can it "
        "succeed?), and desirability (do people want it?). "
        "(6) Implementation roadmap - create a phased plan from MVP prototype "
        "through scaling to optimization with clear milestones.\n\n"
        "Be creative but systematic, ambitious but grounded.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="innovation_framework",
            description="Systematic innovation methodology",
            guidance=Guidance(
                role="Expert Innovation Strategist and Design Thinker",
                rules=[
                    "Start with user needs",
                    "Challenge assumptions",
                    "Think beyond incremental",
                    "Prototype and test",
                    "Iterate rapidly",
                ],
                style="creative, systematic, user-focused",
            ),
            directive_template="""Apply innovation framework to:

**CHALLENGE**: {challenge}

{context_section}

Innovation process:

1. **EMPATHIZE** (Understand users)
   - User needs: [What do they need?]
   - Pain points: [What frustrates them?]
   - Jobs-to-be-done: [What are they trying to accomplish?]
   - Unmet needs: [What's missing?]

2. **DEFINE** (Problem statement)
   - Problem: [Clear statement]
   - Opportunity: [What could be different]
   - Success criteria: [What does success look like]

3. **IDEATE** (Generate solutions)
   - Incremental ideas: [Improvements]
   - Disruptive ideas: [Game changers]
   - Blue ocean ideas: [Untapped markets]

4. **PROTOTYPE** (Build to learn)
   - MVP concept: [Minimum viable product]
   - Test assumptions: [What to validate]
   - Build approach: [How to prototype]

5. **TEST** (Learn and iterate)
   - Hypothesis: [What we believe]
   - Test method: [How to validate]
   - Success metrics: [What to measure]

6. **INNOVATION ASSESSMENT**
   - Novelty: [How new]
   - Feasibility: [Can we build it]
   - Viability: [Can it succeed]
   - Desirability: [Do people want it]

7. **IMPLEMENTATION ROADMAP**
   - Phase 1: [First steps]
   - Phase 2: [Scale]
   - Phase 3: [Optimization]

**OUTPUT FORMAT**: Systematic innovation plan from empathy to execution.""",
            input_schema={"challenge": str, "context_section": str},
            constraints=Constraints(
                must_include=["user_needs", "ideas", "prototype_plan"],
                style_guide="Be creative but systematic",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(self, challenge: str = "", context: str | None = None, **kwargs):
        context_section = self._render_context_section(context)

        return super().build_context(challenge=challenge, context_section=context_section, **kwargs)

    def execute(
        self, provider: str = "openai", challenge: str = "", context: str | None = None, **kwargs
    ):
        return super().execute(provider=provider, challenge=challenge, context=context, **kwargs)
