"""
Idea Generator - Creative ideation and brainstorming

Generates creative ideas using structured brainstorming techniques.
Based on creative thinking research and ideation methodologies.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class IdeaGenerator(Pattern):
    """
    Generate creative ideas systematically.
    
    Uses multiple ideation techniques:
    - SCAMPER method
    - Random stimulus
    - Reverse thinking
    - Analogical inspiration
    
    Based on: Creative cognition and ideation research
    
    Example:
        >>> generator = IdeaGenerator()
        >>> context = generator.build_context(
        ...     challenge="Improve customer onboarding experience",
        ...     constraints=["Budget: $10K", "Timeline: 1 month"]
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert creative strategist. Generate diverse, creative "
        "ideas for the following challenge:\n\n"
        "Challenge: {challenge}\n"
        "{context_section}\n"
        "Constraints: {constraints}\n\n"
        "Apply this methodology: "
        "(1) Reframe the challenge - rephrase using 'How might we...' and "
        "explore at least three alternative framings to open new solution "
        "spaces. "
        "(2) SCAMPER technique - generate ideas by Substituting, Combining, "
        "Adapting, Modifying, Putting to other use, Eliminating, and "
        "Reversing elements of the problem. "
        "(3) Random stimulus - pick an unrelated concept and force unexpected "
        "connections to the challenge for breakthrough ideas. "
        "(4) Reverse thinking - ask 'How could we make this worse?' then flip "
        "those anti-solutions into creative approaches. "
        "(5) Convergent evaluation - cluster related ideas, identify the most "
        "promising themes, and select top 3 ideas plus one wild card. "
        "(6) Implementation sketch - for the best idea, outline quick wins, "
        "resources needed, and success criteria.\n\n"
        "Be wildly creative first, then strategically selective.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="idea_generator",
            description="Generate creative ideas systematically",
            guidance=Guidance(
                role="Expert Creative Strategist and Innovation Specialist",
                rules=[
                    "Generate diverse, creative ideas",
                    "Suspend judgment during generation",
                    "Build on existing ideas",
                    "Encourage wild ideas",
                    "Aim for quantity first, then quality"
                ],
                style="creative, open-minded, energetic"
            ),
            directive_template="""Generate creative ideas for:

**CHALLENGE**: {challenge}

{context_section}

**CONSTRAINTS**:
{constraints_section}

Creative ideation process:

1. **CHALLENGE REFRAMING**
   - Original challenge: {challenge}
   - "How might we..." reframe: [Positive reframing]
   - Alternative framings:
     - [Alternative 1]
     - [Alternative 2]
     - [Alternative 3]

2. **SCAMPER IDEATION**
   Generate ideas by:
   
   **Substitute**: What can be replaced?
   - Idea 1: [Replace X with Y]
   - Idea 2: [Substitute approach]
   
   **Combine**: What can be merged?
   - Idea 3: [Combine A and B]
   - Idea 4: [Merge concepts]
   
   **Adapt**: What can be adjusted?
   - Idea 5: [Adapt from another domain]
   - Idea 6: [Modify existing solution]
   
   **Modify**: What can be changed?
   - Idea 7: [Scale up/down]
   - Idea 8: [Change attributes]
   
   **Put to other use**: New applications?
   - Idea 9: [Repurpose for different use]
   - Idea 10: [New context]
   
   **Eliminate**: What can be removed?
   - Idea 11: [Simplify by removing]
   - Idea 12: [Minimal viable approach]
   
   **Reverse**: What if we do opposite?
   - Idea 13: [Flip the approach]
   - Idea 14: [Reverse assumptions]

3. **RANDOM STIMULUS**
   Random word/concept: [Generate random stimulus]
   
   Forced connections:
   - Idea 15: [Connect stimulus to challenge]
   - Idea 16: [Unexpected combination]
   - Idea 17: [Metaphorical link]

4. **ANALOGICAL THINKING**
   Similar challenges in other domains:
   - Domain 1: [e.g., Nature]
     - Idea 18: [Bio-inspired solution]
   - Domain 2: [e.g., Sports]
     - Idea 19: [Athletic principle applied]
   - Domain 3: [e.g., Technology]
     - Idea 20: [Tech-inspired approach]

5. **EXTREME THINKING**
   If money/time/resources were unlimited:
   - Idea 21: [Dream solution]
   - Idea 22: [Moonshot approach]
   
   If we had zero budget:
   - Idea 23: [Scrappy solution]
   - Idea 24: [Guerrilla approach]

6. **REVERSE PROBLEM**
   How could we make this WORSE?
   - Anti-solution 1: [Worst thing to do]
   - Anti-solution 2: [Guaranteed failure]
   
   Now reverse these into solutions:
   - Idea 25: [Reverse of anti-solution 1]
   - Idea 26: [Opposite approach]

7. **BUILD & COMBINE**
   Combining best elements:
   - Hybrid Idea A: [Combine ideas 3 + 7]
   - Hybrid Idea B: [Merge ideas 10 + 18]
   - Hybrid Idea C: [Synthesis of concepts]

8. **WILD CARDS**
   Crazy, unconventional ideas:
   - Wild Idea 1: [Outrageous approach]
   - Wild Idea 2: [Break-all-rules solution]
   - Wild Idea 3: [Impossible-made-possible]

9. **IDEA CLUSTERING**
   Group related ideas:
   
   Cluster 1: [Theme]
   - Ideas: [List]
   - Core concept: [Unifying principle]
   
   Cluster 2: [Theme]
   - Ideas: [List]
   - Core concept: [Unifying principle]

10. **TOP IDEAS SELECTION**
    Most promising ideas:
    
    **Idea #1**: [Name]
    - Description: [What it is]
    - Why promising: [Potential]
    - Next step: [How to prototype]
    
    **Idea #2**: [Name]
    - Description: [What it is]
    - Why promising: [Potential]
    - Next step: [How to test]
    
    **Idea #3**: [Name]
    - Description: [What it is]
    - Why promising: [Potential]
    - Next step: [How to validate]
    
    **Dark Horse Idea**: [Unexpected but intriguing]
    - Why interesting: [Unique angle]

11. **IMPLEMENTATION SKETCH**
    For top idea:
    - Quick wins: [Fast to implement]
    - Resources needed: [What's required]
    - Success criteria: [How to measure]
    - Risks: [What could go wrong]

**OUTPUT FORMAT**: Creative, diverse ideas with actionable next steps.""",
            input_schema={
                "challenge": str,
                "context_section": str,
                "constraints_section": str
            },
            constraints=Constraints(
                must_include=[
                    "multiple_techniques",
                    "diverse_ideas",
                    "top_selections"
                ],
                style_guide="Be wildly creative but structured, divergent then convergent"
            )
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
        challenge: str = "",
        context: str | None = None,
        constraints: list | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        constraints_section = self._render_constraints_section(constraints)

        return super().build_context(
            challenge=challenge,
            context_section=context_section,
            constraints_section=constraints_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        challenge: str = "",
        context: str | None = None,
        constraints: list | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            challenge=challenge,
            context=context,
            constraints=constraints,
            **kwargs
        )
