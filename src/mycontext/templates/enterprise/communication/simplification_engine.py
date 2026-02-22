"""
Simplification Engine - Make complex ideas simple and accessible

Breaks down complex concepts into simple, understandable explanations.
Based on cognitive load theory and explanation science.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


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

    GENERIC_PROMPT = (
        "You are an expert communicator and simplification specialist. Make the "
        "following complex topic simple and accessible for the target audience.\n\n"
        "Complex topic: {complex_topic}\n"
        "Target audience: {audience}\n"
        "{context_section}\n\n"
        "Apply cognitive-load-aware simplification methodology:\n"
        "(1) Assess complexity — identify technical jargon, abstract concepts, "
        "interconnected layers, and prerequisite knowledge that makes this hard. "
        "(2) Distill the core concept — reduce to a one-sentence explanation, "
        "then a 5-year-old version, capturing the absolute essential idea. "
        "(3) Build progressive explanation — start with the most fundamental "
        "idea (Level 1), add one layer of detail (Level 2), then introduce "
        "nuance and exceptions (Level 3). "
        "(4) Create analogies — compare to familiar concepts the audience already "
        "knows, noting where each analogy holds and where it breaks down. "
        "(5) Provide concrete examples — give 2-3 real-world instances that make "
        "the concept tangible and relatable. "
        "(6) Address common misconceptions — correct the top mistakes people make "
        "and explain why the confusion arises.\n\n"
        "Use plain language. Be patient and clear, never condescending.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

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

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        complex_topic: str = "",
        audience: str = "general audience",
        context: str | None = None,
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
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            complex_topic=complex_topic,
            audience=audience,
            context=context,
            **kwargs
        )
