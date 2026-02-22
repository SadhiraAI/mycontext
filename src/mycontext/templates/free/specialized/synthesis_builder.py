"""
Synthesis Builder - Synthesize information from multiple sources

Creates cohesive syntheses from diverse information sources.
Based on synthesis methodology and information integration.
"""

from typing import Optional, List
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class SynthesisBuilder(Pattern):
    """
    Build comprehensive syntheses.
    
    Synthesizes:
    - Multiple sources
    - Diverse perspectives
    - Complementary insights
    - Unified understanding
    
    Based on: Synthesis methodology and knowledge integration
    
    Example:
        >>> builder = SynthesisBuilder()
        >>> context = builder.build_context(
        ...     sources=["Research paper A", "Industry report B", "Expert interview C"],
        ...     goal="Unified view of AI trends"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a research synthesist and knowledge integration specialist. "
        "Synthesize the following sources into a coherent, integrated understanding:\n\n"
        "Sources: {sources}\n"
        "Goal: {goal}\n"
        "{context_section}\n\n"
        "Apply systematic synthesis methodology: "
        "(1) Analyze each source individually — summarize key points, identify the "
        "perspective, and assess evidence strength. "
        "(2) Identify common themes — where do the sources agree? What patterns "
        "emerge across them? "
        "(3) Find complementary insights — how do the sources complete each other's "
        "picture? "
        "(4) Surface contradictions and tensions — where do sources disagree, and "
        "how can these be resolved or explained? "
        "(5) Construct a synthesis narrative — weave the insights into a coherent, "
        "integrated understanding that is greater than the sum of its parts. "
        "(6) Extract meta-insights — what patterns or gaps emerge from viewing the "
        "sources together? "
        "(7) Build an evidence matrix mapping key claims to supporting sources and "
        "evidence strength. "
        "(8) Assess synthesis quality — completeness, coherence, insight depth, and "
        "remaining limitations.\n\n"
        "Find connections others miss. Resolve contradictions rather than ignoring them."
    )

    def __init__(self):
        super().__init__(
            name="synthesis_builder",
            description="Synthesize from multiple sources",
            guidance=Guidance(
                role="Expert Research Synthesist and Knowledge Integration Specialist",
                rules=[
                    "Identify themes across sources",
                    "Find complementary insights",
                    "Resolve contradictions",
                    "Build coherent narrative",
                    "Add meta-insights"
                ],
                style="integrative, insightful, comprehensive"
            ),
            directive_template="""Synthesize information from:

**SOURCES**:
{sources_section}

**SYNTHESIS GOAL**: {goal}

{context_section}

Synthesis process:

1. **SOURCE ANALYSIS**
   For each source:
   - Source 1: [Summary]
     - Key points: [Main ideas]
     - Perspective: [Viewpoint]
     - Evidence: [Support]
   
   - Source 2: [Summary]
     - [Same structure]

2. **COMMON THEMES**
   Across all sources:
   - Theme 1: [What everyone agrees on]
     - Sources: [Which support]
   - Theme 2: [Another common thread]

3. **COMPLEMENTARY INSIGHTS**
   How sources complete each other:
   - Source A provides: [Unique contribution]
   - Source B adds: [Different angle]
   - Together they show: [Combined insight]

4. **CONTRADICTIONS & TENSIONS**
   Where sources disagree:
   - Contradiction 1: [A says X, B says Y]
     - Resolution: [How to reconcile]
   
   - Contradiction 2: [Another conflict]

5. **SYNTHESIS NARRATIVE**
   Integrated understanding:
   [Cohesive synthesis that integrates all sources into unified narrative]

6. **META-INSIGHTS**
   What emerges from synthesis:
   - Pattern 1: [Bigger picture]
   - Pattern 2: [Emergent understanding]
   - Gap: [What's still missing]

7. **EVIDENCE MATRIX**
   | Claim | Source A | Source B | Source C | Strength |
   |-------|----------|----------|----------|----------|
   | [Claim] | [Support] | [Support] | [Support] | [Strong/Weak] |

8. **SYNTHESIS QUALITY**
   - Completeness: [Coverage]
   - Coherence: [Internal consistency]
   - Insight depth: [Level of understanding]
   - Limitations: [What's not captured]

**OUTPUT FORMAT**: Coherent synthesis with integrated understanding.""",
            input_schema={
                "sources_section": str,
                "goal": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["themes", "synthesis_narrative", "meta_insights"],
                style_guide="Be integrative and insightful"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def _render_sources_section(self, sources: Optional[List[str]]) -> str:
        if sources:
            return "\n".join(f"{i+1}. {source}" for i, source in enumerate(sources))
        return "1. [Define sources]"
    
    def build_context(
        self,
        sources: Optional[List[str]] = None,
        goal: str = "Unified understanding",
        context: Optional[str] = None,
        **kwargs
    ):
        sources_section = self._render_sources_section(sources)
        context_section = self._render_context_section(context)
        
        return super().build_context(
            sources_section=sources_section,
            goal=goal,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        sources: Optional[List[str]] = None,
        goal: str = "Unified understanding",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            sources=sources,
            goal=goal,
            context=context,
            **kwargs
        )
