"""
Design Thinker - Apply design thinking methodology

Structured design thinking process for human-centered innovation.
Based on Stanford d.school design thinking framework.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class DesignThinker(Pattern):
    """
    Apply design thinking methodology.
    
    Process:
    - Empathize with users
    - Define problem
    - Ideate solutions
    - Prototype
    - Test and iterate
    
    Based on: Design thinking (d.school framework)
    
    Example:
        >>> thinker = DesignThinker()
        >>> context = thinker.build_context(
        ...     challenge="Improve healthcare patient experience",
        ...     users="Hospital patients"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert design thinking facilitator. Apply human-centered "
        "design thinking to the following challenge:\n\n"
        "Challenge: {challenge}\n"
        "Target Users: {users}\n"
        "{context_section}\n\n"
        "Apply this methodology: "
        "(1) Empathize - deeply understand the target users: their needs, "
        "pain points, desires, behaviors, and the context they operate in. "
        "(2) Define - synthesize empathy findings into a clear problem "
        "statement using the 'How Might We...' format with specific success "
        "criteria. "
        "(3) Ideate - generate a wide range of creative solutions, from "
        "incremental improvements to radical innovations, building on ideas "
        "freely. "
        "(4) Prototype - outline a quick, low-fidelity prototype concept that "
        "tests the riskiest assumptions of the top idea. "
        "(5) Test - design a plan to test the prototype with real users, "
        "specifying what to observe, what to ask, and how to measure success. "
        "(6) Iterate - based on anticipated feedback, describe how the "
        "solution would evolve through successive learning loops.\n\n"
        "Stay user-focused and iterative throughout.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="design_thinker",
            description="Design thinking methodology",
            guidance=Guidance(
                role="Expert Design Thinking Facilitator and Human-Centered Designer",
                rules=[
                    "Start with empathy",
                    "Focus on human needs",
                    "Embrace ambiguity",
                    "Prototype to learn",
                    "Iterate based on feedback"
                ],
                style="empathetic, creative, iterative"
            ),
            directive_template="""Apply design thinking to:

**CHALLENGE**: {challenge}

**TARGET USERS**: {users}

{context_section}

Design thinking process:

1. **EMPATHIZE** (Understand users deeply)
   - User research: [What to learn]
   - Observations: [What to watch]
   - Interviews: [What to ask]
   - Pain points: [What frustrates them]
   - Desires: [What they wish for]
   - Context: [Their environment]

2. **DEFINE** (Frame the problem)
   - Point of view: [User + Need + Insight]
   - Problem statement: [How might we...]
   - Success criteria: [What does good look like]
   - Scope: [What's in/out]

3. **IDEATE** (Generate solutions)
   - Brainstorm: [Quantity of ideas]
   - Build on ideas: [Yes, and...]
   - Crazy ideas: [Wild possibilities]
   - Promising directions: [Clusters of ideas]

4. **PROTOTYPE** (Make it tangible)
   - Quick prototype: [Fast version]
   - What to test: [Key assumptions]
   - Fidelity: [How real]
   - Timeline: [How long to build]

5. **TEST** (Get feedback)
   - Test with users: [Who to test with]
   - Observe: [What to watch]
   - Listen: [What they say]
   - Learn: [Insights gained]
   - Iterate: [What to change]

6. **INSIGHTS & LEARNINGS**
   - What worked: [Successes]
   - What didn't: [Failures]
   - Surprises: [Unexpected findings]
   - Next iteration: [What to try next]

7. **REFINED SOLUTION**
   [Description of iterated solution based on learning]

**OUTPUT FORMAT**: Human-centered design process with learning loops.""",
            input_schema={
                "challenge": str,
                "users": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["empathy", "prototype", "learnings"],
                style_guide="Be user-focused and iterative"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        challenge: str = "",
        users: str = "",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            challenge=challenge,
            users=users,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        challenge: str = "",
        users: str = "",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            challenge=challenge,
            users=users,
            context=context,
            **kwargs
        )
