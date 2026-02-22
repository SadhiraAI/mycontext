"""
Intent Recognition Pattern - Identify underlying goals and motivations

Helps understand what the user REALLY wants, not just what they asked.
Based on context engineering research on goal inference.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class IntentRecognizer(Pattern):
    """
    Recognize the true intent behind a question or request.
    
    Goes beyond surface-level understanding to identify:
    - Real underlying goals
    - Hidden motivations
    - Implicit assumptions
    - Success criteria
    
    Based on: Goal inference and intent recognition research
    
    Example:
        >>> recognizer = IntentRecognizer()
        >>> context = recognizer.build_context(
        ...     input="What's the best programming language?",
        ...     context="Asking for a friend who wants to switch careers"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an intent analyst and communication specialist. Analyze the following "
        "input to uncover the true intent behind it:\n\n"
        "Input: {input}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Apply multi-layer intent analysis: "
        "(1) Surface Analysis — what is explicitly stated? What are the key terms "
        "and the literal request type? "
        "(2) Goal Inference — what is the immediate goal, the underlying goal, and "
        "the long-term goal? What does success look like? "
        "(3) Motivation Analysis — what is driving this request? What pain points, "
        "constraints, or urgency exist? "
        "(4) Context Interpretation — what situation, background, and stakeholders "
        "are involved? "
        "(5) Implicit Assumptions — what beliefs, biases, knowledge gaps, or "
        "misconceptions are unstated? "
        "(6) Need Classification — is this primarily an information need, a decision "
        "need, an action need, or a validation need? "
        "(7) Reformulated Intent — state the true intent, the real question being "
        "asked, and the optimal response type. "
        "(8) Recommendation — the best approach to address the real need, what to "
        "emphasize, and what to avoid.\n\n"
        "Look beyond the surface. The stated question is rarely the full picture."
    )

    def __init__(self):
        super().__init__(
            name="intent_recognizer",
            description="Recognize true intent behind questions",
            guidance=Guidance(
                role="Expert Intent Analyst and Communication Specialist",
                rules=[
                    "Look beyond surface-level questions",
                    "Identify underlying goals and motivations",
                    "Recognize implicit assumptions",
                    "Consider context and constraints",
                    "Distinguish stated vs. actual needs",
                    "Identify success criteria"
                ],
                style="perceptive, analytical, empathetic"
            ),
            directive_template="""Analyze the true intent behind this input:

**INPUT**: {input}

{context_section}

**ANALYSIS DEPTH**: {depth}

Conduct systematic intent recognition:

1. **SURFACE ANALYSIS**
   - Explicit question/request: [What was literally asked?]
   - Key terms and phrases: [Important words/concepts]
   - Question type: [Information, advice, decision, validation, etc.]

2. **GOAL INFERENCE**
   - Immediate goal: [What do they want right now?]
   - Underlying goal: [What's the real objective?]
   - Long-term goal: [Where are they trying to get?]
   - Success criteria: [How will they know they succeeded?]

3. **MOTIVATION ANALYSIS**
   - Primary motivation: [What's driving this?]
   - Pain points: [What problem are they solving?]
   - Constraints: [What limitations exist?]
   - Urgency: [How time-sensitive is this?]

4. **CONTEXT INTERPRETATION**
   - Situation: [What's their current state?]
   - Background: [Relevant history or experience?]
   - Stakeholders: [Who else is involved?]
   - Environment: [External factors?]

5. **IMPLICIT ASSUMPTIONS**
   - Unstated beliefs: [What are they assuming?]
   - Bias indicators: [Any cognitive biases?]
   - Knowledge gaps: [What don't they know they don't know?]
   - Misconceptions: [Potential misunderstandings?]

6. **NEED CLASSIFICATION**
   - Information need: [What do they need to know?]
   - Decision need: [What do they need to decide?]
   - Action need: [What do they need to do?]
   - Validation need: [Do they need confirmation?]

7. **REFORMULATED INTENT**
   **Original Input**: {input}
   
   **True Intent**: [State the actual underlying intent]
   
   **Real Question**: [Reformulate as what they really want to know]
   
   **Optimal Response Type**: [What kind of answer would best serve their needs?]

8. **RECOMMENDATION**
   To address this intent effectively:
   - Approach: [How to best respond]
   - Key elements: [What to include]
   - Avoid: [What not to do]
   - Success indicators: [How to measure if you helped]

**OUTPUT FORMAT**: Clear, structured analysis with specific insights.""",
            input_schema={
                "input": str,
                "context_section": str,
                "depth": str
            },
            constraints=Constraints(
                must_include=[
                    "underlying_goal",
                    "true_intent",
                    "reformulated_question"
                ],
                style_guide="Be empathetic but analytical, specific but not presumptuous"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        input: str = "",
        context: Optional[str] = None,
        depth: str = "comprehensive",
        **kwargs
    ):
        """
        Build context for intent recognition.
        
        Args:
            input: The question/request to analyze
            context: Optional additional context
            depth: Analysis depth ("quick", "standard", "comprehensive")
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        context_section = self._render_context_section(context)
        
        return super().build_context(
            input=input,
            context_section=context_section,
            depth=depth,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        input: str = "",
        context: Optional[str] = None,
        depth: str = "comprehensive",
        **kwargs
    ):
        """
        Execute intent recognition.
        
        Args:
            provider: LLM provider to use
            input: The question/request to analyze
            context: Optional additional context
            depth: Analysis depth
            **kwargs: Provider parameters
        
        Returns:
            ProviderResponse with the analysis
        """
        return super().execute(
            provider=provider,
            input=input,
            context=context,
            depth=depth,
            **kwargs
        )
