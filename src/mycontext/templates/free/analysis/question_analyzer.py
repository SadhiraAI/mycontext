"""
Question Analyzer Template - Systematically analyze and break down questions.

Based on "understand_question" cognitive tool from IBM research and Context-Engineering.
Depth parameter now drives a genuinely different directive per level:
  brief        — 3 sections: type + core task + clarified restatement
  moderate     — 5 sections: + knowledge prerequisites + implicit assumptions
  comprehensive — all 8 sections (default)

Free tier template - part of mycontext open source.
"""

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_DEPTHS: frozenset[str] = frozenset({"brief", "moderate", "comprehensive"})


def _build_directive(depth: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    sections_map = {
        "type": (
            "1. **QUESTION TYPE CLASSIFICATION**\n"
            "   Identify the primary question type:\n"
            "   - **Factual**: Seeking specific information or facts\n"
            "   - **Conceptual**: Exploring ideas, theories, or abstract concepts\n"
            "   - **Analytical**: Breaking down and examining components\n"
            "   - **Evaluative**: Making judgments, comparisons, or assessments\n"
            "   - **Procedural**: Explaining how to do something or how something works\n"
            "   - **Causal**: Explaining why something happens or happened\n\n"
            "   Primary type: [Identify]\n"
            "   Secondary type (if any): [Identify]"
        ),
        "core_task": (
            "2. **CORE TASK IDENTIFICATION**\n"
            "   - What specific cognitive action is required? (explain, compare, analyse, evaluate, etc.)\n"
            "   - What is the expected output format? (explanation, list, argument, worked example, etc.)"
        ),
        "components": (
            "3. **KEY COMPONENTS**\n"
            "   - **Primary concepts**: [List main ideas or entities]\n"
            "   - **Related domains**: [Relevant fields of knowledge]\n"
            "   - **Relationships**: [How components connect]\n"
            "   - **Scope boundaries**: [What is included/excluded]"
        ),
        "prerequisites": (
            "4. **KNOWLEDGE PREREQUISITES**\n"
            "   What background knowledge is necessary to answer this well?\n"
            "   - **Required**: [Essential — without this, no useful answer is possible]\n"
            "   - **Helpful**: [Supporting knowledge that deepens the answer]\n"
            "   - **Advanced**: [Deep expertise areas for a comprehensive answer]"
        ),
        "assumptions": (
            "5. **IMPLICIT ASSUMPTIONS**\n"
            "   - Unstated assumptions in the question: [Identify]\n"
            "   - Context clues: [What is implied about audience, purpose, level]\n"
            "   - Potential ambiguities: [What needs clarification]"
        ),
        "complexity": (
            "6. **COMPLEXITY ASSESSMENT** (1\u201310 scale)\n"
            "   - **Rating**: [1\u201310]\n"
            "   - **Factors**:\n"
            "     * Conceptual difficulty: [Low / Medium / High]\n"
            "     * Breadth of knowledge required: [Narrow / Moderate / Broad]\n"
            "     * Reasoning depth needed: [Shallow / Moderate / Deep]\n"
            "     * Interdisciplinary connections: [None / Few / Many]"
        ),
        "strategy": (
            "7. **ANSWER STRATEGY RECOMMENDATION**\n"
            "   - **Optimal approach**: [Suggest reasoning method]\n"
            "   - **Structure**: [How to organise the answer]\n"
            "   - **Key considerations**: [What to emphasise]\n"
            "   - **Potential pitfalls**: [What to avoid]"
        ),
    }
    configs = {
        "brief": {
            "section_keys": ["type", "core_task"],
            "restatement_n": 3,
            "instruction": (
                "Provide a focused, efficient analysis. Identify the question type, "
                "clarify the cognitive task required, then restate the question explicitly."
            ),
        },
        "moderate": {
            "section_keys": ["type", "core_task", "components", "prerequisites", "assumptions"],
            "restatement_n": 6,
            "instruction": (
                "Provide a thorough analysis covering question classification, task, "
                "components, prerequisites, and assumptions before restating."
            ),
        },
        "comprehensive": {
            "section_keys": [
                "type",
                "core_task",
                "components",
                "prerequisites",
                "assumptions",
                "complexity",
                "strategy",
            ],
            "restatement_n": 8,
            "instruction": (
                "Provide a complete analysis across all dimensions. "
                "Rate complexity, recommend an answer strategy, and produce a "
                "fully clarified restatement."
            ),
        },
    }
    cfg = configs.get(depth, configs["comprehensive"])
    sections_text = "\n\n".join(sections_map[k] for k in cfg["section_keys"])
    n = cfg["restatement_n"]
    restatement = (
        f"{n}. **CLARIFIED RESTATEMENT**\n"
        "   Restate the question in your own words, making all implicit elements explicit.\n\n"
        "   **Original**: {question}\n"
        "   **Clarified**: [Your reformulation]"
    )

    return (
        f"Analyse this question before attempting to answer it:\n\n"
        f"**QUESTION**: {{question}}\n\n"
        f"{{context_section}}\n\n"
        f"**ANALYSIS DEPTH**: {depth} ({n} sections)\n\n"
        f"{cfg['instruction']}\n\n"
        f"**IMPORTANT**: Do NOT answer the question — only analyse it.\n\n"
        f"{sections_text}\n\n"
        f"{restatement}\n\n"
        f"**OUTPUT FORMAT**: Structured analysis with clear sections as above."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------


class QuestionAnalyzer(Pattern):
    """
    Analyse questions to identify type, complexity, components, and approach.

    This cognitive tool breaks down complex questions before attempting to answer
    them, ensuring all aspects are properly understood.

    The **depth** parameter drives a genuinely different prompt per level:

    - ``brief`` (3 sections): Type + Core Task + Clarified Restatement.
      Fast, minimal — good for quick question scoping.
    - ``moderate`` (5 sections): + Knowledge Prerequisites + Implicit Assumptions.
      Standard — good for most analytical questions.
    - ``comprehensive`` (8 sections, default): + Components + Complexity + Strategy.
      Full analysis — good for multi-domain or ambiguous questions.

    Based on IBM Zurich research: "Eliciting Reasoning in Language Models
    with Cognitive Tools" (June 2025).

    Examples:
        >>> from mycontext.templates.free import QuestionAnalyzer
        >>>
        >>> analyzer = QuestionAnalyzer()
        >>> # Quick scope — just type + task + restatement
        >>> result = analyzer.execute(
        ...     provider="gemini",
        ...     question="How does quantum entanglement work?",
        ...     depth="brief",
        ... )
        >>>
        >>> # Full analysis
        >>> result = analyzer.execute(
        ...     provider="gemini",
        ...     question="Should we adopt microservices?",
        ...     depth="comprehensive",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        'Analyse the following question before answering it: "{question}"\n\n'
        "{context_section}"
        "Identify the question type, surface implicit assumptions and knowledge "
        "requirements, assess complexity, and restate the question explicitly with "
        "all ambiguities resolved. Do NOT answer the question — only analyse it."
    )

    def __init__(self):
        super().__init__(
            name="question_analyzer",
            guidance=Guidance(
                role="Expert Question Analyst and Cognitive Scientist",
                rules=[
                    "Break down questions systematically using structured analysis",
                    "Identify implicit assumptions and knowledge requirements",
                    "Classify questions by type and complexity",
                    "Provide clear reformulations that capture intent",
                    "Consider multiple interpretation angles",
                ],
                style="analytical, structured, thorough, pedagogical",
            ),
            directive_template=_build_directive("comprehensive"),
            input_schema={
                "question": str,
                "context_section": str,
                "depth": str,
            },
            constraints=Constraints(
                must_include=[
                    "question_type",
                    "clarified_restatement",
                ],
                must_not_include=["actual answer to the question"],
                style_guide="Use structured format with clear headings and bullet points",
            ),
        )

    def _render_context_section(self, context):
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        question: str = "",
        context: str | None = None,
        depth: str = "comprehensive",
        **kwargs,
    ):
        """
        Build context for question analysis.

        Args:
            question: The question to analyse
            context: Optional additional context
            depth: Analysis depth — ``"brief"`` | ``"moderate"``
                | ``"comprehensive"`` (default)
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        if depth not in VALID_DEPTHS:
            raise ValueError(f"Invalid depth {depth!r}. Choose from: {sorted(VALID_DEPTHS)}")
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        directive_text = _build_directive(depth)
        directive_content = safe_format_template(
            directive_text, question=question, context_section=context_section, depth=depth
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"question": question, "context_section": context_section, "depth": depth},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["depth"] = depth
        self._apply_default_self_check(
            ctx,
            [
                "Did I answer what was actually asked, or what I assumed was asked?",
                "Did I identify unstated assumptions in the question?",
            ],
        )
        return ctx

    def execute(
        self,
        provider: str = "gemini",
        question: str = "",
        context: str | None = None,
        depth: str = "comprehensive",
        **kwargs,
    ):
        """
        Execute question analysis.

        Args:
            provider: LLM provider to use
            question: The question to analyse
            context: Optional additional context
            depth: Analysis depth — ``"brief"`` | ``"moderate"``
                | ``"comprehensive"`` (default)
            **kwargs: Provider options (model, temperature, max_tokens, etc.)

        Returns:
            ProviderResponse with the analysis
        """
        provider_params = {
            "model",
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "user",
            "api_key",
            "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(question=question, context=context, depth=depth)
        return ctx.execute(provider=provider, **provider_kwargs)
