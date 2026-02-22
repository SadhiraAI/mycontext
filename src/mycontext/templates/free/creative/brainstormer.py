"""
Brainstormer - Structured brainstorming facilitation

Facilitates productive brainstorming sessions using proven techniques.
Based on creative facilitation and group ideation research.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class Brainstormer(Pattern):
    """
    Facilitate structured brainstorming.
    
    Techniques:
    - Divergent thinking
    - Build on ideas
    - Quantity over quality initially
    - Defer judgment
    - Wild ideas encouraged
    
    Based on: Brainstorming and creative facilitation research
    
    Example:
        >>> brainstormer = Brainstormer()
        >>> context = brainstormer.build_context(
        ...     topic="Ways to increase user engagement",
        ...     constraints=["Must be implementable in Q1"]
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a creative facilitator and brainstorming specialist. Conduct a "
        "structured brainstorming session on the following:\n\n"
        "Topic: {topic}\n"
        "Goal: {goal}\n"
        "{context_section}\n"
        "Constraints: {constraints}\n\n"
        "Apply divergent-then-convergent thinking: "
        "(1) Frame the topic and define the brainstorming scope. "
        "(2) Generate 15-20+ ideas rapidly using multiple techniques — free "
        "association, reverse brainstorming (what would make it worse?), random "
        "stimulus, constraint removal (what if there were no limits?), and "
        "cross-domain analogies. "
        "(3) Build on the most promising ideas — combine, extend, and cross-pollinate. "
        "(4) Cluster ideas into thematic groups. "
        "(5) Evaluate using quick criteria: feasibility, impact, novelty, and "
        "alignment with goal. "
        "(6) Identify 3-5 top ideas and refine each with a brief rationale and "
        "next step. "
        "(7) Highlight 1-2 'dark horse' ideas that are unconventional but potentially "
        "transformative. "
        "(8) Recommend an action plan for the strongest concepts.\n\n"
        "Prioritize quantity and diversity. Defer judgment during generation."
    )

    def __init__(self):
        super().__init__(
            name="brainstormer",
            description="Structured brainstorming facilitation",
            guidance=Guidance(
                role="Expert Creative Facilitator and Brainstorming Specialist",
                rules=[
                    "Generate quantity first, quality later",
                    "No criticism during generation",
                    "Build on others' ideas",
                    "Encourage wild and unusual ideas",
                    "Stay focused on topic",
                    "One conversation at a time"
                ],
                style="energetic, open, encouraging"
            ),
            directive_template="""Facilitate brainstorming on:

**TOPIC**: {topic}

{context_section}

**GOAL**: {goal}

**CONSTRAINTS**:
{constraints_section}

Structured brainstorming session:

1. **WARM-UP**
   Get creative juices flowing:
   
   - Quick exercise: [Name unrelated uses for a brick]
   - Purpose: [Loosen up thinking]
   - Duration: [2 minutes]

2. **TOPIC FRAMING**
   Clarify what we're brainstorming:
   
   - Core challenge: {topic}
   - Success looks like: [Description]
   - Out of scope: [What we're NOT solving]
   - Why this matters: [Importance]

3. **BRAINSTORMING RULES**
   Ground rules for session:
   
   ✅ DO:
   - Generate lots of ideas
   - Build on others' ideas
   - Go wild and creative
   - Write everything down
   - Stay focused
   
   ❌ DON'T:
   - Criticize ideas
   - Explain or justify
   - Dominate conversation
   - Go off-topic

4. **RAPID IDEA GENERATION** (10 minutes)
   Quick fire ideas - go!
   
   1. [Idea 1]
   2. [Idea 2]
   3. [Idea 3]
   4. [Idea 4]
   5. [Idea 5]
   6. [Idea 6]
   7. [Idea 7]
   8. [Idea 8]
   9. [Idea 9]
   10. [Idea 10]
   11. [Continue to 30+]

5. **BUILD-ON SESSION**
   Pick 3 interesting ideas and build:
   
   **Base Idea A**: [From above]
   - Build 1: Yes, and... [Extension]
   - Build 2: What if we... [Variation]
   - Build 3: Combining with... [Hybrid]
   
   **Base Idea B**: [Another one]
   - Build 1: [Extension]
   - Build 2: [Variation]
   - Build 3: [Combination]
   
   **Base Idea C**: [Third one]
   - Build 1: [Extension]
   - Build 2: [Variation]
   - Build 3: [Combination]

6. **REVERSE BRAINSTORM**
   How could we make this WORSE?
   
   - Bad idea 1: [Terrible approach]
   - Bad idea 2: [Guaranteed failure]
   - Bad idea 3: [Worst possible]
   
   Now flip them:
   - Bad idea 1 reversed: [Good idea]
   - Bad idea 2 reversed: [Useful approach]
   - Bad idea 3 reversed: [Creative solution]

7. **RANDOM STIMULUS**
   Random word: [Generate random word]
   
   Force connections to topic:
   - Connection 1: [Unexpected link]
   - Connection 2: [Creative association]
   - Connection 3: [Novel approach]

8. **ROLE PLAY IDEATION**
   What would these people suggest?
   
   - **Steve Jobs would say**: [Idea]
   - **A 5-year-old would say**: [Innocent idea]
   - **An alien would say**: [Outside perspective]
   - **Future us (10 years) would say**: [Long-term view]
   - **A competitor would say**: [Rival approach]

9. **CONSTRAINT REMOVAL**
   If we had unlimited resources:
   
   - Moonshot 1: [Dream solution]
   - Moonshot 2: [Impossible made possible]
   - Moonshot 3: [No-limits idea]
   
   Now scale them down:
   - Moonshot 1 → Practical: [Scaled version]
   - Moonshot 2 → Doable: [Realistic variant]
   - Moonshot 3 → Achievable: [Implementable form]

10. **CATEGORY EXPLORATION**
    Generate ideas by category:
    
    **Technology-based ideas**:
    - [Idea]
    - [Idea]
    
    **Process-based ideas**:
    - [Idea]
    - [Idea]
    
    **People-based ideas**:
    - [Idea]
    - [Idea]
    
    **Partnership-based ideas**:
    - [Idea]
    - [Idea]

11. **IDEA CLUSTERING**
    Group similar ideas:
    
    **Cluster 1: [Theme]**
    - Ideas: [List related ideas]
    - Core concept: [Unifying principle]
    
    **Cluster 2: [Theme]**
    - Ideas: [Related ideas]
    - Core concept: [Common thread]
    
    **Cluster 3: [Theme]**
    - Ideas: [Similar approaches]
    - Core concept: [Shared element]

12. **DOT VOTING** (Prioritization)
    Which ideas have most potential?
    
    | Idea | Votes | Why |
    |------|-------|-----|
    | [Idea A] | ●●●●● | [Reason] |
    | [Idea B] | ●●●● | [Reason] |
    | [Idea C] | ●●● | [Reason] |

13. **TOP IDEAS REFINEMENT**
    Polish the winners:
    
    **Idea #1**: [Name it]
    - What it is: [Description]
    - Why exciting: [Promise]
    - How to test: [Validation approach]
    - First step: [Immediate action]
    
    **Idea #2**: [Name it]
    - [Same structure]
    
    **Idea #3**: [Name it]
    - [Same structure]

14. **DARK HORSES**
    Unusual ideas worth exploring:
    
    - Dark Horse 1: [Weird but intriguing]
      - Why interesting: [Potential]
      - Risk: [What could go wrong]
    
    - Dark Horse 2: [Another oddball]

15. **NEXT STEPS**
    
    **Immediate actions**:
    - [ ] Prototype top idea
    - [ ] Research feasibility
    - [ ] Get feedback from [stakeholder]
    
    **Follow-up session**:
    - When: [Schedule]
    - Focus: [What to develop]

**OUTPUT FORMAT**: Energetic brainstorm with diverse ideas and clear next steps.""",
            input_schema={
                "topic": str,
                "context_section": str,
                "goal": str,
                "constraints_section": str
            },
            constraints=Constraints(
                must_include=[
                    "diverse_ideas",
                    "build_on_ideas",
                    "prioritization",
                    "next_steps"
                ],
                style_guide="Be enthusiastic, encouraging, and non-judgmental"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def _render_constraints_section(self, constraints: Optional[list]) -> str:
        if constraints:
            return "\n".join(f"- {c}" for c in constraints)
        return "- None specified"
    
    def build_context(
        self,
        topic: str = "",
        goal: str = "Generate creative solutions",
        context: Optional[str] = None,
        constraints: Optional[list] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        constraints_section = self._render_constraints_section(constraints)
        
        return super().build_context(
            topic=topic,
            goal=goal,
            context_section=context_section,
            constraints_section=constraints_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        topic: str = "",
        goal: str = "Generate creative solutions",
        context: Optional[str] = None,
        constraints: Optional[list] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            topic=topic,
            goal=goal,
            context=context,
            constraints=constraints,
            **kwargs
        )
