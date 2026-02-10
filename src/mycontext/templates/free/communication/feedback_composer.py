"""
Feedback Composer - Compose constructive feedback

Creates actionable, constructive feedback using best practices.
Based on feedback science and communication research.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class FeedbackComposer(Pattern):
    """
    Compose effective, constructive feedback.
    
    Uses:
    - SBI (Situation-Behavior-Impact) model
    - Growth mindset language
    - Specific, actionable guidance
    - Balanced positive and constructive
    
    Based on: Feedback science and communication research
    
    Example:
        >>> composer = FeedbackComposer()
        >>> context = composer.build_context(
        ...     situation="Team member's presentation",
        ...     goal="Improve future presentations"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="feedback_composer",
            description="Compose constructive feedback",
            guidance=Guidance(
                role="Expert Feedback Coach and Communication Specialist",
                rules=[
                    "Be specific, not vague",
                    "Focus on behavior, not person",
                    "Be actionable",
                    "Balance positive and constructive",
                    "Maintain growth mindset"
                ],
                style="supportive, specific, actionable"
            ),
            directive_template="""Compose feedback for:

**SITUATION**: {situation}

{context_section}

**FEEDBACK GOAL**: {goal}

Feedback composition:

1. **CONTEXT SETTING**
   - When: [Specific time/situation]
   - Where: [Context]
   - What was observed: [Specific behavior]

2. **STRENGTHS (What worked well)**
   - Strength 1: [Specific positive]
     - Why effective: [Impact]
     - Encourage: [Keep doing]
   
   - Strength 2: [Another positive]
     - Impact: [Result]

3. **GROWTH OPPORTUNITIES** (Areas to improve)
   Using SBI model:
   
   **Opportunity 1**:
   - Situation: [When this happened]
   - Behavior: [What was done]
   - Impact: [Effect it had]
   - Suggestion: [Specific action to improve]
   
   **Opportunity 2**:
   - [Same structure]

4. **ACTIONABLE RECOMMENDATIONS**
   Specific next steps:
   - Action 1: [What to do differently]
   - Action 2: [How to practice]
   - Resource: [Where to learn more]

5. **COMPLETE FEEDBACK MESSAGE**
   [Full feedback written in supportive, constructive tone]

**OUTPUT FORMAT**: Balanced, actionable feedback message.""",
            input_schema={
                "situation": str,
                "context_section": str,
                "goal": str
            },
            constraints=Constraints(
                must_include=["strengths", "growth_opportunities", "actions"],
                style_guide="Be supportive and specific"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        situation: str = "",
        goal: str = "Support growth",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            situation=situation,
            goal=goal,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        situation: str = "",
        goal: str = "Support growth",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            situation=situation,
            goal=goal,
            context=context,
            **kwargs
        )
