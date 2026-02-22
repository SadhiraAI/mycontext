"""
Persuasion Framework - Build persuasive arguments systematically

Creates compelling, ethical persuasive communication.
Based on rhetoric, influence psychology, and argumentation theory.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class PersuasionFramework(Pattern):
    """
    Build persuasive arguments systematically.
    
    Uses:
    - Classical rhetoric (ethos, pathos, logos)
    - Influence principles
    - Argument structure
    - Objection handling
    
    Based on: Rhetoric and influence research
    
    Example:
        >>> framework = PersuasionFramework()
        >>> context = framework.build_context(
        ...     goal="Convince leadership to adopt AI tools",
        ...     audience="C-suite executives"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert rhetorician and persuasion specialist. Build a "
        "compelling, ethical persuasive argument for the following goal.\n\n"
        "Persuasion goal: {goal}\n"
        "Target audience: {audience}\n"
        "{context_section}\n\n"
        "Apply classical rhetoric and modern influence methodology:\n"
        "(1) Analyze the audience — profile their current beliefs, values, pain "
        "points, decision criteria, and likely objections. "
        "(2) Establish ethos (credibility) — build trust through credentials, "
        "shared values, evidence of success, and third-party validation. "
        "(3) Connect through pathos (emotion) — tap into aspirations, concerns, "
        "identity, and a relatable story with character, challenge, and triumph. "
        "(4) Build logos (logical case) — present a clear problem, supporting "
        "evidence from data and research, and a logical argument structure with "
        "concrete, measurable benefits. "
        "(5) Handle objections proactively — anticipate the top 2-3 concerns "
        "and address each with counter-evidence and reassurance. "
        "(6) Close with a clear call to action — state exactly what to do, "
        "why now, and how easy the first step is.\n\n"
        "Be compelling but ethical, persuasive but respectful.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="persuasion_framework",
            description="Build persuasive arguments",
            guidance=Guidance(
                role="Expert Rhetorician and Persuasion Specialist",
                rules=[
                    "Be ethical - never manipulate",
                    "Build credibility (ethos)",
                    "Connect emotionally (pathos)",
                    "Use logic (logos)",
                    "Address objections proactively",
                    "Call to action clearly"
                ],
                style="compelling, ethical, respectful"
            ),
            directive_template="""Build persuasive argument:

**PERSUASION GOAL**: {goal}

{context_section}

**TARGET AUDIENCE**: {audience}

Systematic persuasion framework:

1. **AUDIENCE ANALYSIS**
   - Who are they: [Profile]
   - Current beliefs: [What they think now]
   - Values: [What matters to them]
   - Pain points: [What concerns them]
   - Decision criteria: [How they decide]
   - Objections: [What they'll resist]

2. **POSITIONING**
   - Your credibility: [Why listen to you]
   - Common ground: [What you share]
   - Shared values: [Mutual beliefs]
   - Trust builders: [Credibility signals]

3. **ETHOS (Credibility)**
   Establish authority and trust:
   
   - Credentials: [Your qualifications]
   - Experience: [Relevant background]
   - Evidence of success: [Proof points]
   - Endorsements: [Third-party validation]
   - Alignment: [Shared interests]

4. **PATHOS (Emotional Appeal)**
   Connect on emotional level:
   
   - Aspiration: [What they want to achieve]
   - Fear: [What they want to avoid]
   - Belonging: [Group identity]
   - Pride: [What makes them proud]
   - Story: [Narrative that resonates]
     - Character: [Relatable protagonist]
     - Challenge: [Obstacle they face]
     - Transformation: [How they succeeded]

5. **LOGOS (Logical Argument)**
   Build rational case:
   
   **Problem Statement**:
   [Clear problem definition]
   
   **Evidence**:
   - Fact 1: [Data/research]
   - Fact 2: [Statistics/studies]
   - Fact 3: [Expert opinion]
   
   **Logical Structure**:
   - Premise 1: [Foundation]
   - Premise 2: [Building block]
   - Conclusion: [Logical result]
   
   **Benefits**:
   - Benefit 1: [Concrete advantage]
   - Benefit 2: [Measurable outcome]
   - Benefit 3: [Strategic value]

6. **INFLUENCE PRINCIPLES**
   Apply psychological principles:
   
   **Reciprocity**: [Give first]
   - What you offer: [Value provided]
   
   **Social Proof**: [Others are doing it]
   - Examples: [Who else]
   
   **Authority**: [Expert validation]
   - Sources: [Credible voices]
   
   **Scarcity**: [Limited opportunity]
   - Urgency: [Time/availability constraint]
   
   **Consistency**: [Align with their values]
   - Connection: [How it fits their identity]

7. **OBJECTION HANDLING**
   Anticipate and address concerns:
   
   - Objection 1: [Likely concern]
     - Response: [Counter-argument]
     - Evidence: [Supporting data]
   
   - Objection 2: [Another worry]
     - Response: [How you address it]
     - Reassurance: [Risk mitigation]
   
   - Objection 3: [Third concern]
     - Response: [Clarification]

8. **CALL TO ACTION**
   What you want them to do:
   
   **Primary CTA**:
   [Specific, clear action]
   - Why now: [Urgency]
   - How easy: [Low friction]
   - What happens: [Next steps]
   
   **Fallback CTA**:
   [Smaller commitment if hesitant]

9. **MESSAGE STRUCTURE**
   
   **Opening (Hook)**:
   [Grab attention immediately]
   - Question, story, or surprise fact
   
   **Body (Build Case)**:
   - Point 1 + Evidence
   - Point 2 + Evidence
   - Point 3 + Evidence
   
   **Climax (Peak Impact)**:
   [Most compelling argument]
   
   **Close (Call to Action)**:
   [What to do now]

10. **DELIVERY STRATEGY**
    **Tone**: [How to sound]
    **Pace**: [Information flow]
    **Emphasis**: [What to stress]
    **Repetition**: [Key messages]

11. **SUCCESS METRICS**
    How to measure persuasiveness:
    - Immediate: [Reaction]
    - Short-term: [Actions taken]
    - Long-term: [Behavior change]

**OUTPUT FORMAT**: Compelling, ethical persuasive framework.""",
            input_schema={
                "goal": str,
                "context_section": str,
                "audience": str
            },
            constraints=Constraints(
                must_include=[
                    "ethos_pathos_logos",
                    "objection_handling",
                    "call_to_action"
                ],
                style_guide="Be persuasive but ethical, compelling but respectful"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        goal: str = "",
        audience: str = "general audience",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            goal=goal,
            audience=audience,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        goal: str = "",
        audience: str = "general audience",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            goal=goal,
            audience=audience,
            context=context,
            **kwargs
        )
