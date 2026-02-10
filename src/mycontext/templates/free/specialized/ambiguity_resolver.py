"""
Ambiguity Resolution Pattern - Clarify unclear or ambiguous inputs

Identifies multiple interpretations and helps resolve ambiguity systematically.
Based on context engineering research on disambiguation.
"""

from typing import Optional, List
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class AmbiguityResolver(Pattern):
    """
    Resolve ambiguous or unclear questions systematically.
    
    Identifies:
    - Multiple possible interpretations
    - Sources of ambiguity
    - Clarifying questions needed
    - Most likely intended meaning
    
    Based on: Disambiguation and clarification research
    
    Example:
        >>> resolver = AmbiguityResolver()
        >>> context = resolver.build_context(
        ...     input="How do I use Python for ML?",
        ...     context="Beginner programmer"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="ambiguity_resolver",
            description="Resolve ambiguous or unclear inputs",
            guidance=Guidance(
                role="Expert Clarity Specialist and Communication Analyst",
                rules=[
                    "Identify all sources of ambiguity",
                    "Generate multiple valid interpretations",
                    "Propose specific clarifying questions",
                    "Assess likelihood of each interpretation",
                    "Provide structured disambiguation"
                ],
                style="precise, systematic, helpful"
            ),
            directive_template="""Resolve ambiguity in this input:

**INPUT**: {input}

{context_section}

**RESOLUTION DEPTH**: {depth}

Systematic ambiguity resolution:

1. **AMBIGUITY IDENTIFICATION**
   List all sources of ambiguity:
   - Lexical: [Multiple word meanings]
   - Syntactic: [Unclear sentence structure]
   - Semantic: [Unclear references or relationships]
   - Pragmatic: [Unclear intent or context]
   - Scope: [Unclear boundaries]

2. **POSSIBLE INTERPRETATIONS**
   For each significant ambiguity, list valid interpretations:
   
   Interpretation A:
   - Meaning: [What this interpretation means]
   - Likelihood: [High/Medium/Low based on context]
   - Assumptions: [What this assumes]
   - Implications: [What this would lead to]
   
   Interpretation B:
   - Meaning: [Alternative interpretation]
   - Likelihood: [High/Medium/Low]
   - Assumptions: [What this assumes]
   - Implications: [Different implications]
   
   [Continue for all significant interpretations]

3. **CONTEXT ANALYSIS**
   - Available context: [What do we know?]
   - Missing context: [What's unclear?]
   - Implicit cues: [Hints from context]
   - Contradictions: [Conflicting information]

4. **CLARIFYING QUESTIONS**
   To resolve ambiguity, ask:
   
   Priority 1 (Critical):
   - [Most important question to ask]
   - [Why this is critical]
   
   Priority 2 (Important):
   - [Important clarification needed]
   - [Why this matters]
   
   Priority 3 (Helpful):
   - [Useful but not essential]
   - [Added value]

5. **LIKELIHOOD ASSESSMENT**
   Based on available context:
   
   Most Likely Interpretation:
   - Interpretation: [Which one]
   - Confidence: [X%]
   - Reasoning: [Why this is most likely]
   
   Alternative Interpretations:
   - [Other possibilities with confidence levels]

6. **DISAMBIGUATION STRATEGY**
   **If clarification is possible:**
   - Approach: [How to ask for clarification]
   - Key questions: [What to ask]
   - Expected info: [What answers would help]
   
   **If must proceed without clarification:**
   - Safest assumption: [Best guess]
   - Hedging strategy: [How to be safe]
   - Multiple answers: [Address main interpretations]

7. **REFORMULATED INPUT**
   **Original**: {input}
   
   **Clarified Versions**:
   - Version A: [If interpretation A is correct]
   - Version B: [If interpretation B is correct]
   
   **Recommended Approach**: [How to proceed given ambiguity]

**OUTPUT FORMAT**: Structured analysis with clear disambiguation path.""",
            input_schema={
                "input": str,
                "context_section": str,
                "depth": str
            },
            constraints=Constraints(
                must_include=[
                    "identified_ambiguities",
                    "possible_interpretations",
                    "clarifying_questions"
                ],
                style_guide="Be thorough but not pedantic, helpful but not condescending"
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
        depth: str = "thorough",
        **kwargs
    ):
        """
        Build context for ambiguity resolution.
        
        Args:
            input: The ambiguous input to resolve
            context: Optional additional context
            depth: Resolution depth ("quick", "standard", "thorough")
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
        depth: str = "thorough",
        **kwargs
    ):
        """
        Execute ambiguity resolution.
        
        Args:
            provider: LLM provider to use
            input: The ambiguous input to resolve
            context: Optional additional context
            depth: Resolution depth
            **kwargs: Provider parameters
        
        Returns:
            ProviderResponse with the resolution
        """
        return super().execute(
            provider=provider,
            input=input,
            context=context,
            depth=depth,
            **kwargs
        )
