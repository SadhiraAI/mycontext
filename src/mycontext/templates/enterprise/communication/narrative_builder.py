"""
Narrative Builder - Construct compelling narratives and stories

Creates engaging narratives using story structure frameworks.
Based on narrative theory and storytelling research.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class NarrativeBuilder(Pattern):
    """
    Build compelling narratives systematically.

    Uses:
    - Hero's Journey
    - Story arc structure
    - Character development
    - Conflict and resolution

    Based on: Narrative theory and storytelling frameworks

    Example:
        >>> builder = NarrativeBuilder()
        >>> context = builder.build_context(
        ...     topic="Our company transformation journey",
        ...     audience="investors"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert storyteller and narrative architect. Build a compelling "
        "narrative that connects emotionally with the audience.\n\n"
        "Topic: {topic}\n"
        "Audience: {audience}\n"
        "Narrative goal: {goal}\n"
        "{context_section}\n\n"
        "Apply proven narrative construction methodology:\n"
        "(1) Establish the story foundation — identify the core message, the "
        "protagonist (hero), the central challenge they face, the stakes that "
        "make it matter, and the transformation achieved. "
        "(2) Craft a powerful opening hook — set the scene, introduce the "
        "character, and present the inciting incident that grabs attention. "
        "(3) Build rising action — escalate tension through challenges, first "
        "attempts, setbacks, and growing stakes. "
        "(4) Deliver the climax — the critical turning point with maximum "
        "tension and a decisive moment. "
        "(5) Resolve with impact — show the transformation, the new equilibrium, "
        "and the lasting meaning for the audience. "
        "(6) Write the complete narrative with vivid details and emotional arc.\n\n"
        "Show, don't just tell. Make it authentic and memorable.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="narrative_builder",
            description="Build compelling narratives",
            guidance=Guidance(
                role="Expert Storyteller and Narrative Architect",
                rules=[
                    "Create emotional connection",
                    "Build tension and resolution",
                    "Show, don't just tell",
                    "Include concrete details",
                    "End with transformation",
                ],
                style="engaging, vivid, compelling",
            ),
            directive_template="""Build narrative for:

**TOPIC**: {topic}

**AUDIENCE**: {audience}

{context_section}

**NARRATIVE GOAL**: {goal}

Narrative construction:

1. **STORY FOUNDATION**
   - Core message: [What's the point]
   - Hero: [Protagonist]
   - Challenge: [What they face]
   - Stakes: [Why it matters]
   - Transformation: [Change achieved]

2. **OPENING (Hook)**
   [Grab attention immediately]
   - Scene setting
   - Character introduction
   - Inciting incident

3. **RISING ACTION**
   [Build tension]
   - Challenge emerges
   - First attempt
   - Setback
   - Growing stakes

4. **CLIMAX**
   [Peak moment]
   - Critical decision
   - Turning point
   - Maximum tension

5. **RESOLUTION**
   [How it ended]
   - Problem solved
   - Transformation complete
   - New equilibrium

6. **COMPLETE NARRATIVE**
   [Full story written out]

**OUTPUT FORMAT**: Engaging narrative with emotional arc.""",
            input_schema={"topic": str, "audience": str, "context_section": str, "goal": str},
            constraints=Constraints(
                must_include=["hook", "conflict", "resolution"],
                style_guide="Be engaging and authentic",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        topic: str = "",
        audience: str = "general",
        goal: str = "Engage and inspire",
        context: str | None = None,
        **kwargs,
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            topic=topic, audience=audience, goal=goal, context_section=context_section, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        topic: str = "",
        audience: str = "general",
        goal: str = "Engage and inspire",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(
            provider=provider, topic=topic, audience=audience, goal=goal, context=context, **kwargs
        )
