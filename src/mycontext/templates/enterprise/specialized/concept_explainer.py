"""
Concept Explainer Template - Clear, accessible explanations of complex concepts.

Based on pedagogical best practices and cognitive tools methodology.
Free tier template - part of mycontext open source.
"""

from mycontext import Pattern, Guidance, Directive, Constraints


class ConceptExplainer(Pattern):
    """
    Explain complex concepts clearly with examples, analogies, and visual aids.
    
    This template structures explanations using proven pedagogical techniques:
    - Start with the "why" before the "how"
    - Use multiple representation modes (text, examples, analogies, visuals)
    - Build from familiar to unfamiliar
    - Include concrete examples
    - Check understanding with edge cases
    
    Examples:
        >>> from mycontext.templates.free import ConceptExplainer
        >>> 
        >>> explainer = ConceptExplainer()
        >>> result = explainer.execute(
        ...     provider="gemini",
        ...     concept="quantum entanglement",
        ...     audience="high school students",
        ...     depth="comprehensive"
        ... )
        >>> print(result.response)
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert educator and science communicator. Explain the "
        "following concept clearly and accessibly for the target audience.\n\n"
        "Concept: {concept}\n"
        "Audience: {audience}\n"
        "Depth level: {depth}\n"
        "{context_section}\n\n"
        "Apply layered pedagogical explanation methodology:\n"
        "(1) Start with why it matters — explain the real-world relevance, what "
        "problems it solves, and where it shows up in practice. "
        "(2) Give a simple definition — one clear sentence accessible to the "
        "audience, then the core insight without jargon. "
        "(3) Build detailed explanation in layers — from basic mechanism to key "
        "principles to important nuances, increasing depth progressively. "
        "(4) Provide concrete examples — at least two real-world instances "
        "(one basic, one realistic) that make the concept tangible. "
        "(5) Create analogies — compare to familiar concepts the audience knows, "
        "noting where each analogy holds and where it breaks down. "
        "(6) Address common misconceptions — correct the top wrong beliefs and "
        "clarify key distinctions with related concepts.\n\n"
        "Adjust complexity to the audience. Use active voice and clear language.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )
    
    def __init__(self):
        super().__init__(
            name="concept_explainer",
            guidance=Guidance(
                role="Expert Educator and Science Communicator",
                rules=[
                    "Start with why the concept matters before explaining how it works",
                    "Use multiple explanation modes: definitions, examples, analogies, visuals",
                    "Build from familiar concepts to new ones",
                    "Provide concrete, relatable examples",
                    "Address common misconceptions explicitly",
                    "Check understanding with thought experiments or edge cases"
                ],
                style="clear, accessible, engaging, pedagogical"
            ),
            directive_template="""Explain this concept clearly and comprehensively.

**CONCEPT**: {concept}

**AUDIENCE**: {audience}

**DEPTH LEVEL**: {depth}

{context_section}

Provide a structured explanation using multiple approaches:

## 1. THE BIG PICTURE (Why This Matters)

**Real-World Relevance**:
- Why should someone care about this concept?
- What problems does it solve or what phenomena does it explain?
- Where does this show up in everyday life or professional work?

**Context in the Field**:
- How does this fit into the broader field?
- What came before this concept (historical context)?
- What does this enable or make possible?

## 2. SIMPLE DEFINITION

**One-Sentence Summary**:
[Explain the concept in one clear sentence accessible to the audience]

**Key Idea**:
The core insight in simple terms: [Explain the central idea without jargon]

## 3. DETAILED EXPLANATION

**What It Is**:
[Detailed explanation of the concept]

**How It Works**:
- **Mechanism/Process**: [Step-by-step or component-by-component]
- **Key Principles**: [Fundamental rules or patterns]
- **Important Properties**: [Essential characteristics]

**Visual Representation**:
```
[ASCII diagram, flowchart, or visual aid]
┌─────────────┐
│   [Label]   │
└──────┬──────┘
       │
       ▼
   [Process]
```

## 4. CONCRETE EXAMPLES

**Example 1** (Basic):
[Simple, clear example that demonstrates the core concept]
- Setup: [Context]
- Application: [How the concept applies]
- Result: [What happens]

**Example 2** (Realistic):
[Real-world scenario showing practical application]

**Example 3** (Edge Case):
[Interesting case showing boundaries or limitations]

## 5. ANALOGIES & METAPHORS

**Analogy 1**: [Concept] is like [familiar thing]
- Similarity: [How they're alike]
- Where it breaks down: [Limitations of this analogy]

**Analogy 2** (if helpful):
[Alternative way to think about it]

## 6. COMMON MISCONCEPTIONS

**Misconception 1**: "[Common wrong belief]"
- **Reality**: [Correct understanding]
- **Why the confusion**: [Why people think this]

**Misconception 2**: [If applicable]

## 7. KEY DISTINCTIONS

**What It IS**:
- [Essential characteristic 1]
- [Essential characteristic 2]

**What It's NOT**:
- [Common confusion 1]
- [Common confusion 2]

**Related Concepts**:
| Concept | Relationship | Key Difference |
|---------|--------------|----------------|
| [Related concept A] | [How they relate] | [Main distinction] |
| [Related concept B] | [How they relate] | [Main distinction] |

## 8. DEEPER UNDERSTANDING (Optional for {depth})

**Implications**:
- What follows from this concept?
- What questions does it raise?

**Advanced Nuances** (for advanced audience):
- [Subtleties or complexities]

**Current Research/Open Questions**:
- [What's still being figured out, if applicable]

## 9. PRACTICAL TAKEAWAYS

**Remember These Key Points**:
1. [Essential point 1]
2. [Essential point 2]
3. [Essential point 3]

**To Check Your Understanding**:
- Can you explain this to someone else in your own words?
- Can you think of your own example?
- Can you identify this concept when you see it?

## 10. FURTHER EXPLORATION (Optional)

**Next Steps**:
- [Related concepts to explore next]
- [Questions to deepen understanding]

---

**REQUIREMENTS**:
- Adjust complexity to audience level
- Use active voice and clear language
- Include specific examples, not just abstractions
- Address potential confusions proactively
- Make it engaging and memorable""",
            input_schema={
                "concept": str,
                "audience": str,
                "depth": str,
                "context": str
            },
            constraints=Constraints(
                must_include=[
                    "why it matters",
                    "simple definition",
                    "concrete examples",
                    "visual representation",
                    "common misconceptions"
                ],
                must_not_include=[
                    "unexplained jargon",
                    "pure abstractions without examples"
                ],
                style_guide="Use clear headings, examples, analogies, and visual aids. Adjust complexity to audience."
            )
        )
    
    def _render_context_section(self, context):
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""
    

    def build_context(self, concept="", audience="general audience", depth="comprehensive", context=None, **kwargs):
        if context is None:
            context = ""
        context_section = self._render_context_section(context)
        return super().build_context(
            concept=concept,
            audience=audience,
            depth=depth,
            context=context,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider="gemini",
        concept="",
        audience="general audience",
        depth="comprehensive",
        context=None,
        temperature=0.7,  # Moderate temp for clear but engaging explanations
        **kwargs
    ):
        """
        Execute concept explanation.
        
        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            concept: The concept to explain
            audience: Target audience ("general audience", "high school students", 
                     "college students", "professionals", "experts")
            depth: Explanation depth ("brief", "moderate", "comprehensive")
            context: Optional context about why this explanation is needed
            temperature: Moderate values (0.6-0.8) for clarity with engagement
            **kwargs: Additional provider options
        
        Returns:
            ProviderResponse with the explanation
        """
        # Provide defaults for optional fields
        if context is None:
            context = ""
        
        context_section = self._render_context_section(context)
        
        return super().execute(
            provider=provider,
            concept=concept,
            audience=audience,
            depth=depth,
            context=context,
            context_section=context_section,
            temperature=temperature,
            **kwargs
        )
