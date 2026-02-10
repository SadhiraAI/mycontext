"""
Metaphor Generator - Create powerful metaphors and analogies

Generates effective metaphors for communication and understanding.
Based on metaphor theory and cognitive linguistics.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class MetaphorGenerator(Pattern):
    """
    Generate effective metaphors systematically.
    
    Creates:
    - Explanatory metaphors
    - Conceptual metaphors
    - Visual metaphors
    - Domain mappings
    
    Based on: Conceptual metaphor theory
    
    Example:
        >>> generator = MetaphorGenerator()
        >>> context = generator.build_context(
        ...     concept="How AI learns from data",
        ...     audience="non-technical stakeholders"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="metaphor_generator",
            description="Generate powerful metaphors",
            guidance=Guidance(
                role="Expert Metaphor Specialist and Creative Communicator",
                rules=[
                    "Find familiar source domains",
                    "Map structure, not surface",
                    "Make insights transferable",
                    "Know metaphor limits",
                    "Test understanding"
                ],
                style="creative, insightful, clear"
            ),
            directive_template="""Generate metaphors for:

**CONCEPT**: {concept}

**AUDIENCE**: {audience}

{context_section}

Metaphor generation:

1. **CONCEPT ANALYSIS**
   - Core idea: [Essence]
   - Key attributes: [What matters]
   - Structure: [How it works]
   - Challenges: [What's hard to explain]

2. **SOURCE DOMAIN CANDIDATES**
   Familiar domains to draw from:
   - Domain 1: [e.g., Nature]
   - Domain 2: [e.g., Sports]
   - Domain 3: [e.g., Everyday life]

3. **METAPHOR GENERATION**
   
   **Metaphor 1**: [Concept] is like [Familiar thing]
   - Mapping: [How they correspond]
   - Insight: [What it reveals]
   - Example: "[Specific usage]"
   - Strength: [What works well]
   - Limitation: [Where it breaks down]
   
   **Metaphor 2**: [Alternative metaphor]
   - [Same structure]
   
   **Metaphor 3**: [Third option]
   - [Same structure]

4. **EXTENDED METAPHOR**
   Develop best metaphor fully:
   - Base metaphor: [Core comparison]
   - Extensions: [Deeper mappings]
   - Implications: [What else it explains]

5. **USAGE EXAMPLES**
   How to use in communication:
   - Example 1: "[In a sentence]"
   - Example 2: "[Different context]"

6. **TESTING**
   - Clarity: [Does it clarify?]
   - Accuracy: [Is it faithful to concept?]
   - Memorability: [Will they remember?]
   - Limitations: [What it doesn't capture]

7. **RECOMMENDED METAPHOR**
   Best choice and why

**OUTPUT FORMAT**: Powerful metaphors with usage guidance.""",
            input_schema={
                "concept": str,
                "audience": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["multiple_metaphors", "mappings", "limitations"],
                style_guide="Be creative but accurate"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        concept: str = "",
        audience: str = "general",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            concept=concept,
            audience=audience,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        concept: str = "",
        audience: str = "general",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            concept=concept,
            audience=audience,
            context=context,
            **kwargs
        )
