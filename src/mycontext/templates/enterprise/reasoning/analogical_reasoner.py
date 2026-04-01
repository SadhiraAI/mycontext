"""
Analogical Reasoning Pattern - Use analogies and mental models for understanding

Leverages analogies to explain complex concepts or solve problems.
Based on cognitive science research on analogical transfer.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class AnalogicalReasoner(Pattern):
    """
    Use analogies and mental models for reasoning and understanding.

    Systematic analogical thinking:
    - Find relevant analogies
    - Map correspondences
    - Transfer insights
    - Identify limitations

    Based on: Cognitive science research on analogical reasoning

    Example:
        >>> reasoner = AnalogicalReasoner()
        >>> context = reasoner.build_context(
        ...     concept="How does a neural network learn?",
        ...     domain="machine learning"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert in analogical reasoning and cognitive science. "
        "Apply systematic analogical thinking to understand this concept:\n\n"
        "Concept: {concept}\n"
        "Domain: {domain}\n"
        "{context_section}\n"
        "Reasoning Depth: {depth}\n\n"
        "Apply this methodology: "
        "(1) Analyze the target - break down the concept into its core "
        "components, relationships, and challenges to understanding. "
        "(2) Search for analogies - find 3-5 meaningful analogies from diverse "
        "domains that share structural similarities, not just surface "
        "resemblance. "
        "(3) Map correspondences - explicitly map elements, relationships, and "
        "processes between the target concept and each analogy in detail. "
        "(4) Transfer insights - extract what each analogy reveals about the "
        "target that was not obvious before. "
        "(5) Identify breakdown points - honestly assess where each analogy "
        "fails, could mislead, or should not be extended. "
        "(6) Synthesize understanding - combine insights from multiple "
        "analogies into a comprehensive, nuanced understanding of the "
        "concept.\n\n"
        "Be creative but grounded, insightful but accurate.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="analogical_reasoner",
            description="Reason using analogies and mental models",
            guidance=Guidance(
                role="Expert Cognitive Scientist and Analogy Specialist",
                rules=[
                    "Find meaningful, not superficial analogies",
                    "Map correspondences explicitly",
                    "Identify where analogies break down",
                    "Use multiple analogies for robustness",
                    "Transfer insights systematically",
                ],
                style="creative, insightful, pedagogical",
            ),
            directive_template="""Use analogical reasoning for this concept/problem:

**TARGET**: {concept}

{context_section}

**DOMAIN**: {domain}

**REASONING DEPTH**: {depth}

Systematic analogical reasoning:

1. **TARGET ANALYSIS**
   - Core concept: [What are we trying to understand/solve?]
   - Key components: [Main parts or aspects]
   - Relationships: [How parts interact]
   - Challenges: [What's difficult about this?]

2. **ANALOGY SEARCH**
   Find 3-5 relevant analogies from different domains:
   
   Analogy 1: [Name] (from [domain])
   - Brief description: [What is it?]
   - Relevance: [Why relevant?]
   - Strength: [High/Medium/Low]
   
   Analogy 2: [Name] (from [domain])
   - [Same structure]
   
   [Continue for 3-5 analogies]

3. **CORRESPONDENCE MAPPING**
   For the strongest analogy, map elements:
   
   | Target Concept | ↔ | Analogy Element | Relationship |
   |----------------|---|-----------------|--------------|
   | Element A      | ↔ | Element X       | [How similar] |
   | Element B      | ↔ | Element Y       | [How similar] |
   | Process P      | ↔ | Process Q       | [How similar] |
   
   Structural similarities:
   - [What patterns match?]
   - [What relationships correspond?]

4. **INSIGHT TRANSFER**
   What can we learn from the analogy?
   
   - Insight 1: [From analogy → Applied to target]
   - Insight 2: [From analogy → Applied to target]
   - Insight 3: [From analogy → Applied to target]
   
   New understanding:
   - [How does this change our understanding?]

5. **LIMITATIONS & BREAKDOWN POINTS**
   Where the analogy fails:
   
   - Difference 1: [Where analogy doesn't match]
   - Difference 2: [Another mismatch]
   - Danger: [Risk of over-extending analogy]
   
   Use with caution when:
   - [Scenarios where analogy misleads]

6. **MULTIPLE PERSPECTIVE SYNTHESIS**
   Combining insights from all analogies:
   
   - Common patterns: [What all analogies share]
   - Complementary insights: [What each uniquely contributes]
   - Comprehensive understanding: [Integrated view]

7. **PRACTICAL APPLICATION**
   How to use these insights:
   
   - Understanding: [How this helps comprehension]
   - Problem-solving: [How this helps find solutions]
   - Communication: [How to explain to others]
   - Decision-making: [How this informs choices]

8. **ANALOGY SUMMARY**
   **Best Analogy**: [Which one is most useful?]
   
   **One-Sentence Explanation**: 
   "[Target concept] is like [analogy] in that [key correspondence]"
   
   **Key Takeaway**: [Most important insight]

**OUTPUT FORMAT**: Creative but rigorous analogical analysis.""",
            input_schema={"concept": str, "context_section": str, "domain": str, "depth": str},
            constraints=Constraints(
                must_include=["multiple_analogies", "correspondence_mapping", "limitations"],
                style_guide="Be creative but grounded, insightful but accurate",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        concept: str = "",
        domain: str = "general",
        context: str | None = None,
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Build context for analogical reasoning.

        Args:
            concept: The concept/problem to reason about
            domain: The domain context
            context: Optional additional context
            depth: Reasoning depth ("quick", "detailed", "deep")
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        context_section = self._render_context_section(context)

        return super().build_context(
            concept=concept, domain=domain, context_section=context_section, depth=depth, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        concept: str = "",
        domain: str = "general",
        context: str | None = None,
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Execute analogical reasoning.

        Args:
            provider: LLM provider to use
            concept: The concept/problem to reason about
            domain: The domain context
            context: Optional additional context
            depth: Reasoning depth
            **kwargs: Provider parameters

        Returns:
            ProviderResponse with the reasoning
        """
        return super().execute(
            provider=provider,
            concept=concept,
            domain=domain,
            context=context,
            depth=depth,
            **kwargs,
        )
