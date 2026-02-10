"""
Simplification Engine - Make complex ideas simple and accessible

Breaks down complex concepts into simple, understandable explanations.
Based on cognitive load theory and explanation science.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class SimplificationEngine(Pattern):
    """
    Simplify complex ideas for accessibility.
    
    Techniques:
    - Progressive complexity reduction
    - Analogies and metaphors
    - Visual thinking
    - Plain language
    
    Based on: Cognitive load and explanation research
    
    Example:
        >>> engine = SimplificationEngine()
        >>> context = engine.build_context(
        ...     complex_topic="How quantum computing works",
        ...     audience="High school students"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="simplification_engine",
            description="Simplify complex ideas",
            guidance=Guidance(
                role="Expert Communicator and Simplification Specialist",
                rules=[
                    "Start with the core concept",
                    "Use familiar analogies",
                    "Avoid jargon unless necessary",
                    "Build up complexity gradually",
                    "Test for understanding"
                ],
                style="clear, accessible, patient"
            ),
            directive_template="""Simplify this complex topic:

**COMPLEX TOPIC**: {complex_topic}

{context_section}

**TARGET AUDIENCE**: {audience}

Systematic simplification:

1. **COMPLEXITY ASSESSMENT**
   What makes this complex?
   - Technical terms: [List difficult terms]
   - Abstract concepts: [Hard-to-grasp ideas]
   - Multiple layers: [Interconnected parts]
   - Prerequisites: [What you need to know first]

2. **CORE CONCEPT**
   Reduce to absolute simplest form:
   
   **One-Sentence Explanation**:
   [Explain in one simple sentence]
   
   **5-Year-Old Version**:
   [Explain as if to a child]
   
   **Essential Idea**:
   [The absolute core concept]

3. **PROGRESSIVE EXPLANATION**
   Build up understanding layer by layer:
   
   **Level 1 - Basics**:
   [Start with most fundamental idea]
   - Key point A: [Simple concept]
   - Key point B: [Another basic idea]
   
   **Level 2 - Adding Detail**:
   [Add one layer of complexity]
   - How it works: [Simple mechanism]
   - Important feature: [Key characteristic]
   
   **Level 3 - Deeper Understanding**:
   [More nuance and detail]
   - Nuance A: [Subtlety explained simply]
   - Exception B: [Special case]

4. **ANALOGIES & METAPHORS**
   Compare to familiar concepts:
   
   **Primary Analogy**:
   "{complex_topic} is like [familiar thing]"
   - Similarity 1: [How they match]
   - Similarity 2: [Another parallel]
   - Where analogy breaks: [Limits]
   
   **Alternative Analogies**:
   - Analogy 2: [Different comparison]
   - Analogy 3: [Another angle]

5. **CONCRETE EXAMPLES**
   Make it real and relatable:
   
   - Example 1: [Real-world instance]
     - Why it matters: [Relevance]
   - Example 2: [Everyday scenario]
     - Connection: [How it relates]
   - Example 3: [Practical application]
     - Impact: [What it means]

6. **VISUAL THINKING**
   How to picture this:
   
   Mental model: [Describe a mental image]
   - Visual 1: [What to imagine]
   - Visual 2: [Another visualization]
   
   Diagram suggestion:
   - Type: [Flowchart, diagram, etc.]
   - Key elements: [What to show]

7. **COMMON MISCONCEPTIONS**
   What people often get wrong:
   
   - Misconception 1: [Wrong belief]
     - Why wrong: [Explanation]
     - Correct understanding: [Right way]
   
   - Misconception 2: [Another error]
     - Clarification: [Truth]

8. **KEY VOCABULARY**
   Essential terms explained simply:
   
   - **Term 1**: [Simple definition]
     - In context: [How it's used]
   - **Term 2**: [Plain language]
     - Why it matters: [Significance]

9. **UNDERSTANDING CHECKPOINTS**
   Questions to test comprehension:
   
   - Question 1: [Simple question]
     - Answer: [Verification]
   - Question 2: [Understanding check]
     - Answer: [Confirmation]

10. **NEXT STEPS FOR LEARNING**
    How to deepen understanding:
    
    **If you get this**:
    - Next concept: [What to learn next]
    - Resource: [Where to learn more]
    
    **If still confused**:
    - Revisit: [What to review]
    - Alternative: [Different explanation]

11. **SIMPLIFIED SUMMARY**
    **In Plain English**:
    [2-3 sentence summary using simple words]
    
    **Key Takeaways**:
    1. [Most important point]
    2. [Second key idea]
    3. [Third essential concept]
    
    **Why It Matters**:
    [Relevance to audience]

**OUTPUT FORMAT**: Clear, accessible explanation appropriate for audience.""",
            input_schema={
                "complex_topic": str,
                "context_section": str,
                "audience": str
            },
            constraints=Constraints(
                must_include=[
                    "analogies",
                    "progressive_explanation",
                    "simplified_summary"
                ],
                style_guide="Be patient, clear, and encouraging. No condescension."
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        complex_topic: str = "",
        audience: str = "general audience",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            complex_topic=complex_topic,
            audience=audience,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        complex_topic: str = "",
        audience: str = "general audience",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            complex_topic=complex_topic,
            audience=audience,
            context=context,
            **kwargs
        )
