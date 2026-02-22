"""
Feedback Composer - Compose constructive feedback

Creates actionable, constructive feedback using best practices.
Based on feedback science and communication research.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


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

    GENERIC_PROMPT = (
        "You are an expert feedback coach and communication specialist. Compose "
        "constructive, actionable feedback for the following situation.\n\n"
        "Situation: {situation}\n"
        "Feedback goal: {goal}\n"
        "{context_section}\n\n"
        "Apply the SBI (Situation-Behavior-Impact) feedback methodology:\n"
        "(1) Set context — describe the specific situation, timing, and what was "
        "observed without judgment or generalization. "
        "(2) Identify strengths — highlight what worked well with concrete examples "
        "and explain the positive impact of those behaviors. "
        "(3) Frame growth opportunities using SBI — for each area, state the "
        "Situation, the specific Behavior observed, and the Impact it had, then "
        "offer a concrete suggestion for improvement. "
        "(4) Provide actionable next steps — give 2-3 specific, measurable actions "
        "the person can take immediately to improve. "
        "(5) Write the complete feedback message in a supportive, growth-oriented "
        "tone that balances positive recognition with constructive guidance.\n\n"
        "Be specific, not vague. Focus on behaviors, not personality.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

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

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        situation: str = "",
        goal: str = "Support growth",
        context: str | None = None,
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
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            situation=situation,
            goal=goal,
            context=context,
            **kwargs
        )
