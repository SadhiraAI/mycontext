"""
Narrative Builder - Construct compelling narratives and stories

Creates engaging narratives using story structure frameworks.
Based on narrative theory and storytelling research.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


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
                    "End with transformation"
                ],
                style="engaging, vivid, compelling"
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
            input_schema={
                "topic": str,
                "audience": str,
                "context_section": str,
                "goal": str
            },
            constraints=Constraints(
                must_include=["hook", "conflict", "resolution"],
                style_guide="Be engaging and authentic"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        topic: str = "",
        audience: str = "general",
        goal: str = "Engage and inspire",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            topic=topic,
            audience=audience,
            goal=goal,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        topic: str = "",
        audience: str = "general",
        goal: str = "Engage and inspire",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            topic=topic,
            audience=audience,
            goal=goal,
            context=context,
            **kwargs
        )
