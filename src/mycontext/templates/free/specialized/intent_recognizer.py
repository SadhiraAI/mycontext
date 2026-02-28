"""
Intent Recognition Pattern - Identify underlying goals and motivations

Helps understand what the user REALLY wants, not just what they asked.
Grounded in Speech Act Theory, Gricean pragmatics, and goal inference
research.  The depth parameter controls how many analytical layers are
applied: quick (4), standard (8), or comprehensive (12).
"""


from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern


_SECTION_SURFACE = """
1. **SURFACE ANALYSIS**
   - Explicit question/request: [What was literally asked?]
   - Key terms and phrases: [Important words/concepts]
   - Question type: [Information, advice, decision, validation, etc.]"""

_SECTION_GOALS = """
2. **GOAL INFERENCE**
   - Immediate goal: [What do they want right now?]
   - Underlying goal: [What's the real objective?]
   - Long-term goal: [Where are they trying to get?]
   - Success criteria: [How will they know they succeeded?]"""

_SECTION_MOTIVATION = """
3. **MOTIVATION ANALYSIS**
   - Primary motivation: [What's driving this?]
   - Pain points: [What problem are they solving?]
   - Constraints: [What limitations exist?]
   - Urgency: [How time-sensitive is this?]"""

_SECTION_CONTEXT = """
4. **CONTEXT INTERPRETATION**
   - Situation: [What's their current state?]
   - Background: [Relevant history or experience?]
   - Stakeholders: [Who else is involved?]
   - Environment: [External factors?]"""

_SECTION_ASSUMPTIONS = """
5. **IMPLICIT ASSUMPTIONS**
   - Unstated beliefs: [What are they assuming?]
   - Bias indicators: [Any cognitive biases?]
   - Knowledge gaps: [What don't they know they don't know?]
   - Misconceptions: [Potential misunderstandings?]"""

_SECTION_NEEDS = """
6. **NEED CLASSIFICATION**
   - Information need: [What do they need to know?]
   - Decision need: [What do they need to decide?]
   - Action need: [What do they need to do?]
   - Validation need: [Do they need confirmation?]"""

_SECTION_REFORMULATED = """
{n}. **REFORMULATED INTENT**
   **Original Input**: {{input}}

   **True Intent**: [State the actual underlying intent]

   **Real Question**: [Reformulate as what they really want to know]

   **Optimal Response Type**: [What kind of answer would best serve their needs?]"""

_SECTION_RECOMMENDATION = """
{n}. **RECOMMENDATION**
   To address this intent effectively:
   - Approach: [How to best respond]
   - Key elements: [What to include]
   - Avoid: [What not to do]
   - Success indicators: [How to measure if you helped]"""

_SECTION_SPEECH_ACTS = """
7. **SPEECH ACT ANALYSIS**
   - Locutionary act: [What was literally said — the propositional content]
   - Illocutionary act: [What was intended — request, complaint, threat, plea, etc.]
   - Perlocutionary act: [What effect do they want on the listener — persuade, alarm, reassure?]
   - Illocutionary force mismatch: [Is the surface speech act different from the intended one?]"""

_SECTION_IMPLICATURE = """
8. **CONVERSATIONAL IMPLICATURE** (Gricean Analysis)
   - Quantity: [Are they saying too much or too little? What does the over/under-sharing signal?]
   - Quality: [Any hedging, exaggeration, or qualifiers that signal uncertainty?]
   - Relation: [What seems irrelevant but was mentioned? Why include that detail?]
   - Manner: [Is the phrasing unusually indirect, formal, or vague? What does the style signal?]
   - What is NOT being said: [Conspicuous omissions — topics they are avoiding]"""

_SECTION_INDIRECTNESS = """
9. **INDIRECTNESS & POWER DYNAMICS**
   - Directness level: [Scale 1-5, where 1 is highly indirect]
   - Face-saving moves: [Are they protecting their own face or the listener's?]
   - Power asymmetry: [Who has authority? How does it shape the request?]
   - Politeness strategy: [Bald-on-record, positive, negative, or off-record?]
   - Escalation signals: [Is this a first ask, a repeat, or a final warning?]"""

_SECTION_FRAMES = """
10. **FRAME & ABSENCE ANALYSIS**
   - Activated frames: [What conceptual domains does this request invoke?]
   - Alternative frames: [How would this look reframed from a different perspective?]
   - Conspicuous absences: [What would you expect to see mentioned but isn't?]
   - Temporal signals: [Time-of-day, day-of-week, deadline proximity — what do they reveal?]
   - Metaphor analysis: [Any metaphors or analogies that reveal how they conceptualize the problem?]"""

_DEPTH_CONFIGS = {
    "quick": {
        "sections": [
            _SECTION_SURFACE,
            _SECTION_GOALS,
        ],
        "reformulated_n": 3,
        "recommendation_n": 4,
        "instruction": "Provide a focused, efficient analysis. Prioritize the true intent and actionable recommendation.",
    },
    "standard": {
        "sections": [
            _SECTION_SURFACE,
            _SECTION_GOALS,
            _SECTION_MOTIVATION,
            _SECTION_CONTEXT,
            _SECTION_ASSUMPTIONS,
            _SECTION_NEEDS,
        ],
        "reformulated_n": 7,
        "recommendation_n": 8,
        "instruction": "Provide thorough analysis across all standard dimensions.",
    },
    "comprehensive": {
        "sections": [
            _SECTION_SURFACE,
            _SECTION_GOALS,
            _SECTION_MOTIVATION,
            _SECTION_CONTEXT,
            _SECTION_ASSUMPTIONS,
            _SECTION_NEEDS,
            _SECTION_SPEECH_ACTS,
            _SECTION_IMPLICATURE,
            _SECTION_INDIRECTNESS,
            _SECTION_FRAMES,
        ],
        "reformulated_n": 11,
        "recommendation_n": 12,
        "instruction": (
            "Conduct the deepest possible analysis. Apply linguistic and pragmatic "
            "frameworks (Speech Act Theory, Gricean implicature, Politeness Theory, "
            "Frame Semantics) to uncover layers that surface-level analysis misses."
        ),
    },
}


def _build_directive(depth: str) -> str:
    """Assemble the directive template for the given depth level."""
    cfg = _DEPTH_CONFIGS.get(depth, _DEPTH_CONFIGS["comprehensive"])
    sections = "\n".join(cfg["sections"])
    reformulated = _SECTION_REFORMULATED.format(n=cfg["reformulated_n"])
    recommendation = _SECTION_RECOMMENDATION.format(n=cfg["recommendation_n"])
    total = cfg["recommendation_n"]

    return f"""Analyze the true intent behind this input:

**INPUT**: {{input}}

{{context_section}}

**ANALYSIS DEPTH**: {depth} ({total} sections)

{cfg['instruction']}

Conduct systematic intent recognition:
{sections}
{reformulated}
{recommendation}

**OUTPUT FORMAT**: Clear, structured analysis with specific insights."""


class IntentRecognizer(Pattern):
    """
    Recognize the true intent behind a question or request.

    Goes beyond surface-level understanding to identify:
    - Real underlying goals and hidden motivations
    - Implicit assumptions and cognitive biases
    - Speech acts, conversational implicature, and power dynamics
    - Conspicuous absences and conceptual frames

    The **depth** parameter controls analytical rigour:
    - ``quick`` (4 sections): Surface, Goals, Reformulated Intent, Recommendation
    - ``standard`` (8 sections): + Motivation, Context, Assumptions, Needs
    - ``comprehensive`` (12 sections): + Speech Acts, Implicature, Indirectness, Frames

    Grounded in Speech Act Theory (Austin/Searle), Gricean pragmatics,
    Politeness Theory (Brown & Levinson), and Frame Semantics (Fillmore).

    Example:
        >>> recognizer = IntentRecognizer()
        >>> context = recognizer.build_context(
        ...     input="What's the best programming language?",
        ...     context="Asking for a friend who wants to switch careers",
        ...     depth="comprehensive"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an intent analyst grounded in pragmatic linguistics. "
        "Analyze the following input to uncover the true intent behind it:\n\n"
        "Input: {input}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Apply multi-layer intent analysis:\n"
        "(1) Surface Analysis — what is explicitly stated, key terms, literal request type.\n"
        "(2) Goal Inference — immediate, underlying, and long-term goals; success criteria.\n"
        "(3) Motivation Analysis — what drives this request; pain points, constraints, urgency.\n"
        "(4) Context Interpretation — situation, background, stakeholders, environment.\n"
        "(5) Implicit Assumptions — unstated beliefs, biases, knowledge gaps.\n"
        "(6) Need Classification — information, decision, action, or validation need.\n"
        "(7) Speech Act Analysis — locutionary vs illocutionary vs perlocutionary act; "
        "is the surface speech act different from the intended one?\n"
        "(8) Conversational Implicature — Gricean maxim violations (quantity, quality, "
        "relation, manner); what is conspicuously NOT being said?\n"
        "(9) Indirectness & Power — directness level, face-saving, power asymmetry, "
        "escalation signals.\n"
        "(10) Frame & Absence Analysis — conceptual frames activated, alternative frames, "
        "conspicuous absences, temporal signals.\n"
        "(11) Reformulated Intent — true intent, real question, optimal response type.\n"
        "(12) Recommendation — best approach, key elements, what to avoid.\n\n"
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
                    "Recognize implicit assumptions and cognitive biases",
                    "Analyze speech acts — what is said vs. what is meant vs. desired effect",
                    "Apply Gricean maxims — note what is conspicuously NOT said",
                    "Consider power dynamics, face-saving, and indirectness",
                    "Distinguish stated vs. actual needs",
                    "Identify success criteria",
                ],
                style="perceptive, analytical, empathetic"
            ),
            directive_template=_build_directive("comprehensive"),
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

    def _render_context_section(self, context: str | None) -> str:
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        input: str = "",
        context: str | None = None,
        depth: str = "comprehensive",
        **kwargs
    ):
        """
        Build context for intent recognition.

        The directive template is dynamically selected based on ``depth``,
        so quick/standard/comprehensive produce genuinely different prompts.

        Args:
            input: The question/request to analyze
            context: Optional additional context
            depth: Analysis depth ("quick", "standard", "comprehensive")
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        directive_text = _build_directive(depth)
        directive_content = safe_format_template(
            directive_text, input=input, context_section=context_section, depth=depth
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"input": input, "context_section": context_section, "depth": depth},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        return ctx

    def execute(
        self,
        provider: str = "openai",
        input: str = "",
        context: str | None = None,
        depth: str = "comprehensive",
        **kwargs
    ):
        """
        Execute intent recognition.

        Args:
            provider: LLM provider to use
            input: The question/request to analyze
            context: Optional additional context
            depth: Analysis depth ("quick", "standard", "comprehensive")
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
