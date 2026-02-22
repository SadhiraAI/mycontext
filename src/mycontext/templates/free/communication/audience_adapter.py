"""
Audience Adapter - Adapt communication for different audiences

Tailors messages, tone, and content to specific audiences.
Based on communication theory and audience analysis.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class AudienceAdapter(Pattern):
    """
    Adapt communication for target audiences.
    
    Adapts:
    - Technical level
    - Tone and style
    - Examples and analogies
    - Detail level
    - Format and structure
    
    Based on: Communication and audience analysis research
    
    Example:
        >>> adapter = AudienceAdapter()
        >>> context = adapter.build_context(
        ...     message="Explain our AI technology",
        ...     current_audience="engineers",
        ...     target_audience="C-suite executives"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a communication strategist and audience specialist. Adapt the "
        "following content for a different audience:\n\n"
        "Original message: {message}\n"
        "Current audience: {current_audience}\n"
        "Target audience: {target_audience}\n"
        "{context_section}\n\n"
        "Apply audience-centered adaptation: "
        "(1) Profile the target audience — expertise level, interests, communication "
        "preferences, and what they care about. "
        "(2) Extract the core message that must survive the adaptation. "
        "(3) Adjust language — match technical level, translate jargon, and "
        "calibrate complexity. "
        "(4) Reframe — choose examples, analogies, and framing that resonate with "
        "the target audience's experience. "
        "(5) Adapt tone and style — formal vs. casual, authoritative vs. "
        "collaborative, detail-oriented vs. big-picture. "
        "(6) Optimize structure for how this audience consumes information. "
        "(7) Deliver the fully adapted message. "
        "(8) Note key adaptations made and potential questions the new audience "
        "might have.\n\n"
        "Preserve the core message's accuracy while optimizing resonance for the "
        "target audience."
    )

    def __init__(self):
        super().__init__(
            name="audience_adapter",
            description="Adapt communication for audiences",
            guidance=Guidance(
                role="Expert Communication Strategist and Audience Specialist",
                rules=[
                    "Understand audience deeply",
                    "Match technical level appropriately",
                    "Use relevant examples",
                    "Respect audience intelligence",
                    "Focus on what matters to them"
                ],
                style="adaptive, empathetic, clear"
            ),
            directive_template="""Adapt this communication:

**ORIGINAL MESSAGE**: {message}

**CURRENT AUDIENCE**: {current_audience}

**TARGET AUDIENCE**: {target_audience}

{context_section}

Audience adaptation:

1. **TARGET AUDIENCE ANALYSIS**
   
   **Who they are**:
   - Role/position: [What they do]
   - Background: [Education, experience]
   - Technical level: [Novice/Intermediate/Expert]
   - Domain knowledge: [What they know]
   
   **What they care about**:
   - Primary interests: [Top priorities]
   - Pain points: [What concerns them]
   - Decision criteria: [How they evaluate]
   - Time constraints: [How busy]
   
   **Communication preferences**:
   - Preferred style: [Formal/casual/technical]
   - Detail level: [High-level/detailed]
   - Format: [Presentation/doc/conversation]
   - Attention span: [Short/medium/long]

2. **LANGUAGE ADAPTATION**
   
   **Technical Level Adjustment**:
   - Original: [Technical terminology]
   - Adapted: [Appropriate terminology]
   
   **Jargon Translation**:
   | Original Term | Audience-Friendly |
   |---------------|-------------------|
   | [Tech term 1] | [Plain language] |
   | [Tech term 2] | [Accessible term] |
   | [Tech term 3] | [Understood phrase] |
   
   **Complexity Level**:
   - Original complexity: [Rating]
   - Target complexity: [Appropriate level]
   - Adjustment: [How simplified/enriched]

3. **CORE MESSAGE EXTRACTION**
   
   **Essential Points** (Keep these):
   1. [Key message 1]
   2. [Key message 2]
   3. [Key message 3]
   
   **Supporting Details** (Adjust amount):
   - For this audience: [How much detail]
   - What to emphasize: [Focus areas]
   - What to minimize: [Less important]

4. **FRAMING FOR AUDIENCE**
   
   **Their Perspective**:
   - What matters to them: [Primary concern]
   - Frame message through: [Their lens]
   
   **Value Proposition** (Reframe for audience):
   - Business value: [If executives]
   - Technical merit: [If engineers]
   - User benefit: [If end-users]
   - Strategic fit: [If leadership]

5. **EXAMPLE & ANALOGY ADAPTATION**
   
   **Original Examples**:
   - Example 1: [From original]
   - Example 2: [From original]
   
   **Audience-Appropriate Examples**:
   - Example 1: [Relatable to them]
     - Why relevant: [Connection]
   - Example 2: [Familiar to them]
     - Why resonates: [Meaning]
   
   **Analogies**:
   - Original: [If any]
   - Adapted: [Using their domain]

6. **TONE & STYLE ADJUSTMENT**
   
   **Original Tone**: [Description]
   **Target Tone**: [What's appropriate]
   
   **Style Shifts**:
   - Formality: [Adjust level]
   - Energy: [Match their pace]
   - Confidence: [Appropriate assertion]
   - Empathy: [Emotional connection]

7. **STRUCTURE OPTIMIZATION**
   
   **For This Audience**:
   - Opening: [Hook that grabs them]
   - Organization: [Structure they prefer]
   - Flow: [Logical to them]
   - Closing: [Strong finish with CTA]
   
   **Time Consideration**:
   - Attention span: [Duration]
   - Information density: [Pace]
   - Break points: [If long]

8. **ADAPTED MESSAGE**
   
   [Full adapted version of the message, completely rewritten for the target audience, maintaining all key information but adjusted in language, examples, tone, and structure]

9. **KEY ADAPTATIONS MADE**
   
   Summary of changes:
   - Language: [What changed]
   - Examples: [New examples used]
   - Focus: [Shifted emphasis]
   - Tone: [Adjustment made]
   - Length: [Expanded/condensed]

10. **POTENTIAL QUESTIONS**
    What this audience might ask:
    
    - Q1: [Likely question]
      - A: [Prepared answer]
    
    - Q2: [Another question]
      - A: [Response]
    
    - Q3: [Third question]
      - A: [Answer]

11. **DELIVERY RECOMMENDATIONS**
    
    **How to present**:
    - Medium: [Email/presentation/conversation]
    - Timing: [When to deliver]
    - Setting: [Formal/informal]
    - Support materials: [What to include]
    
    **What to avoid**:
    - Don't: [Pitfalls with this audience]
    - Don't: [What not to assume]

12. **SUCCESS INDICATORS**
    How to know it worked:
    
    - Immediate: [Engagement signals]
    - Short-term: [Understanding confirmed]
    - Long-term: [Desired action taken]

**OUTPUT FORMAT**: Fully adapted message with explanation of changes.""",
            input_schema={
                "message": str,
                "current_audience": str,
                "target_audience": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=[
                    "audience_analysis",
                    "adapted_message",
                    "key_changes"
                ],
                style_guide="Be respectful of both audiences, not condescending"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        message: str = "",
        current_audience: str = "general",
        target_audience: str = "specific group",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            message=message,
            current_audience=current_audience,
            target_audience=target_audience,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        message: str = "",
        current_audience: str = "general",
        target_audience: str = "specific group",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            message=message,
            current_audience=current_audience,
            target_audience=target_audience,
            context=context,
            **kwargs
        )
