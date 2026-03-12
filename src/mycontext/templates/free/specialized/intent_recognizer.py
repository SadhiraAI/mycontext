"""
Intent Recognition Pattern - Identify underlying goals and motivations

Helps understand what the user REALLY wants, not just what they asked.
Grounded in Speech Act Theory, Gricean pragmatics, and goal inference
research.  The depth parameter controls how many analytical layers are
applied: quick (4), standard (8), or comprehensive (12).
"""


from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern
from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive


def _build_directive(depth: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    section_texts = {
        "surface": (
            "\n1. **SURFACE ANALYSIS**\n"
            "   - Explicit question/request: [What was literally asked?]\n"
            "   - Key terms and phrases: [Important words/concepts]\n"
            "   - Question type: [Information, advice, decision, validation, etc.]"
        ),
        "goals": (
            "\n2. **GOAL INFERENCE**\n"
            "   - Immediate goal: [What do they want right now?]\n"
            "   - Underlying goal: [What's the real objective?]\n"
            "   - Long-term goal: [Where are they trying to get?]\n"
            "   - Success criteria: [How will they know they succeeded?]"
        ),
        "motivation": (
            "\n3. **MOTIVATION ANALYSIS**\n"
            "   - Primary motivation: [What's driving this?]\n"
            "   - Pain points: [What problem are they solving?]\n"
            "   - Constraints: [What limitations exist?]\n"
            "   - Urgency: [How time-sensitive is this?]"
        ),
        "context": (
            "\n4. **CONTEXT INTERPRETATION**\n"
            "   - Situation: [What's their current state?]\n"
            "   - Background: [Relevant history or experience?]\n"
            "   - Stakeholders: [Who else is involved?]\n"
            "   - Environment: [External factors?]"
        ),
        "assumptions": (
            "\n5. **IMPLICIT ASSUMPTIONS**\n"
            "   - Unstated beliefs: [What are they assuming?]\n"
            "   - Bias indicators: [Any cognitive biases?]\n"
            "   - Knowledge gaps: [What don't they know they don't know?]\n"
            "   - Misconceptions: [Potential misunderstandings?]"
        ),
        "needs": (
            "\n6. **NEED CLASSIFICATION**\n"
            "   - Information need: [What do they need to know?]\n"
            "   - Decision need: [What do they need to decide?]\n"
            "   - Action need: [What do they need to do?]\n"
            "   - Validation need: [Do they need confirmation?]"
        ),
        "affective": (
            "\n7. **AFFECTIVE STATE ANALYSIS**\n"
            "   - Emotional valence: [Positive / Neutral / Negative]\n"
            "   - Dominant emotion: [Frustrated / Anxious / Curious / Hopeful / Urgent / Other]\n"
            "   - Confidence level: [How certain does the person seem?]\n"
            "   - Stress indicators: [Language markers of pressure or urgency]\n"
            "   - Response tone needed: [What emotional register is appropriate?]"
        ),
        "speech_acts": (
            "\n8. **SPEECH ACT ANALYSIS**\n"
            "   - Locutionary act: [What was literally said]\n"
            "   - Illocutionary act: [What was intended \u2014 request, complaint, plea, etc.]\n"
            "   - Perlocutionary act: [What effect do they want \u2014 persuade, alarm, reassure?]\n"
            "   - Illocutionary force mismatch: [Is surface speech act different from intended?]"
        ),
        "implicature": (
            "\n9. **CONVERSATIONAL IMPLICATURE** (Gricean Analysis)\n"
            "   - Quantity: [Over/under-sharing signal?]\n"
            "   - Quality: [Hedging, exaggeration, or qualifiers indicating uncertainty?]\n"
            "   - Relation: [What seems irrelevant but was mentioned?]\n"
            "   - Manner: [Unusually indirect, formal, or vague?]\n"
            "   - What is NOT being said: [Conspicuous omissions]"
        ),
        "indirectness": (
            "\n10. **INDIRECTNESS & POWER DYNAMICS**\n"
            "   - Directness level: [Scale 1-5, where 1 is highly indirect]\n"
            "   - Face-saving moves: [Protecting own or listener's face?]\n"
            "   - Power asymmetry: [Who has authority? How does it shape the request?]\n"
            "   - Politeness strategy: [Bald-on-record, positive, negative, or off-record?]\n"
            "   - Escalation signals: [First ask, repeat, or final warning?]"
        ),
        "frames": (
            "\n11. **FRAME & ABSENCE ANALYSIS**\n"
            "   - Activated frames: [What conceptual domains does this invoke?]\n"
            "   - Alternative frames: [How would this look from a different perspective?]\n"
            "   - Conspicuous absences: [What would you expect to see mentioned but isn't?]\n"
            "   - Temporal signals: [Deadline proximity, urgency indicators]\n"
            "   - Metaphor analysis: [Metaphors revealing how they conceptualise the problem]"
        ),
    }

    def _reformulated(n: int) -> str:
        return (
            f"\n{n}. **REFORMULATED INTENT**\n"
            "   **Original Input**: {{input}}\n\n"
            "   **True Intent**: [State the actual underlying intent]\n\n"
            "   **Real Question**: [Reformulate as what they really want to know]\n\n"
            "   **Optimal Response Type**: [What kind of answer would best serve their needs?]"
        )

    def _recommendation(n: int) -> str:
        return (
            f"\n{n}. **RECOMMENDATION**\n"
            "   To address this intent effectively:\n"
            "   - Approach: [How to best respond]\n"
            "   - Key elements: [What to include]\n"
            "   - Avoid: [What not to do]\n"
            "   - Success indicators: [How to measure if you helped]"
        )

    configs = {
        "quick": {
            "keys": ["surface", "goals"],
            "reformulated_n": 3,
            "recommendation_n": 4,
            "instruction": (
                "Provide a focused, efficient analysis. "
                "Identify the true intent and give an actionable recommendation."
            ),
        },
        "standard": {
            "keys": ["surface", "goals", "motivation", "context", "assumptions", "needs", "affective"],
            "reformulated_n": 8,
            "recommendation_n": 9,
            "instruction": (
                "Provide thorough analysis across all standard dimensions, including an "
                "affective state analysis to identify the emotional context and what response "
                "tone is appropriate."
            ),
        },
        "comprehensive": {
            "keys": [
                "surface", "goals", "motivation", "context", "assumptions", "needs",
                "affective", "speech_acts", "implicature", "indirectness", "frames",
            ],
            "reformulated_n": 12,
            "recommendation_n": 13,
            "instruction": (
                "Conduct the deepest possible analysis. Apply affective state analysis to "
                "identify the emotional context, then apply linguistic and pragmatic frameworks "
                "(Speech Act Theory, Gricean implicature, Politeness Theory, Frame Semantics) "
                "to uncover layers that surface-level analysis misses."
            ),
        },
    }
    cfg = configs.get(depth, configs["comprehensive"])
    total = cfg["recommendation_n"]
    sections_text = "".join(section_texts[k] for k in cfg["keys"])
    sections_text += _reformulated(cfg["reformulated_n"])
    sections_text += _recommendation(cfg["recommendation_n"])

    return (
        f"Analyze the true intent behind this input:\n\n"
        f"**INPUT**: {{input}}\n\n"
        f"{{context_section}}\n\n"
        f"**ANALYSIS DEPTH**: {depth} ({total} sections)\n\n"
        f"{cfg['instruction']}\n\n"
        f"Conduct systematic intent recognition:\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Clear, structured analysis with specific insights."
    )


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
    - ``standard`` (9 sections): + Motivation, Context, Assumptions, Needs, Affective State
    - ``comprehensive`` (13 sections): + Speech Acts, Implicature, Indirectness, Frames

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
        "Analyze the following input to uncover the true intent behind it:\n\n"
        "Input: {input}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Apply multi-layer intent analysis to identify surface meaning, underlying goals, "
        "motivations, implicit assumptions, and emotional context. Use linguistic and "
        "pragmatic frameworks to uncover what is really being asked versus what is stated. "
        "Reformulate the true intent and recommend the most effective response approach.\n\n"
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
                    "reformulated_question",
                ],
                style_guide=(
                    "Be empathetic but analytical, specific but not presumptuous. "
                    "When identifying emotional state, be clinical and descriptive — "
                    "not judgmental."
                ),
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
        output_format: str = "structured",
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
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
                | ``"json"`` | ``"table"``
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )

        context_section = self._render_context_section(context)
        directive_text = _build_directive(depth)
        directive_content = safe_format_template(
            directive_text, input=input, context_section=context_section, depth=depth
        )
        directive_content += get_format_directive(output_format)

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"input": input, "context_section": context_section, "depth": depth},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["output_format"] = output_format
        return ctx

    def execute(
        self,
        provider: str = "openai",
        input: str = "",
        context: str | None = None,
        depth: str = "comprehensive",
        output_format: str = "structured",
        **kwargs
    ):
        """
        Execute intent recognition.

        Args:
            provider: LLM provider to use
            input: The question/request to analyze
            context: Optional additional context
            depth: Analysis depth ("quick", "standard", "comprehensive")
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
                | ``"json"`` | ``"table"``
            **kwargs: Provider parameters

        Returns:
            ProviderResponse with the analysis
        """
        ctx = self.build_context(
            input=input,
            context=context,
            depth=depth,
            output_format=output_format,
        )
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        return ctx.execute(provider=provider, **provider_kwargs)
