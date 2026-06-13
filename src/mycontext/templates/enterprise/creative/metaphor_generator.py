"""
Metaphor Generator - Create powerful metaphors and analogies

Generates effective metaphors for communication and understanding.
Based on metaphor theory and cognitive linguistics.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


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

    GENERIC_PROMPT = (
        "You are an expert in metaphor and creative communication. Generate "
        "powerful metaphors and analogies for the following:\n\n"
        "Concept: {concept}\n"
        "Target Audience: {audience}\n"
        "{context_section}\n\n"
        "Apply this methodology: "
        "(1) Analyze the concept - break it down into its core idea, key "
        "attributes, structure, and what makes it challenging to explain. "
        "(2) Identify source domains - find 3-5 familiar domains your "
        "audience knows well that share structural similarities with the "
        "concept. "
        "(3) Generate metaphors - create at least three distinct metaphors, "
        "mapping specific elements of each source domain to the concept. "
        "(4) Evaluate mappings - for each metaphor, assess what it "
        "illuminates, what insights it transfers, and where the comparison "
        "breaks down. "
        "(5) Develop the strongest - extend the best metaphor into a rich, "
        "layered comparison with deeper correspondences and usage examples. "
        "(6) Provide usage guidance - suggest how to deploy each metaphor in "
        "context with example sentences tailored to the audience.\n\n"
        "Be creative but accurate, vivid but faithful to the concept.\n\n"
    )

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
                    "Test understanding",
                ],
                style="creative, insightful, clear",
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
            input_schema={"concept": str, "audience": str, "context_section": str},
            constraints=Constraints(
                must_include=["multiple_metaphors", "mappings", "limitations"],
                style_guide="Be creative but accurate",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self, concept: str = "", audience: str = "general", context: str | None = None, **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            concept=concept, audience=audience, context_section=context_section, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        concept: str = "",
        audience: str = "general",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(
            provider=provider, concept=concept, audience=audience, context=context, **kwargs
        )
