"""
Data Analyzer - Systematic data analysis and insight extraction

Comprehensive data analysis with pattern detection and insights.
Supports intent-based parameterization (executive, analyst, operations,
summary, comprehensive) and investment levels (quick, standard, thorough).

Based on data science and analytical reasoning frameworks.
"""

from __future__ import annotations

from typing import Any, ClassVar

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern


_SECTION_BLOCKS: dict[str, str] = {
    "data_overview": (
        "1. **DATA OVERVIEW**\n"
        "   - Data type: [What kind of data]\n"
        "   - Time period: [Coverage]\n"
        "   - Sample size: [How much data]\n"
        "   - Variables: [What's measured]\n"
        "   - Quality: [Completeness, accuracy]"
    ),
    "descriptive_statistics": (
        "2. **DESCRIPTIVE STATISTICS**\n"
        "   Summary statistics:\n"
        "   - Central tendency: [Mean, median, mode]\n"
        "   - Dispersion: [Range, variance, std dev]\n"
        "   - Distribution: [Shape, skewness]\n"
        "   - Key figures: [Notable numbers]"
    ),
    "pattern_detection": (
        "3. **PATTERN DETECTION**\n"
        "   \n"
        "   **Trends**:\n"
        "   - Trend 1: [Upward/downward/stable]\n"
        "     - Evidence: [What shows this]\n"
        "     - Magnitude: [How strong]\n"
        "     - Timeframe: [Since when]\n"
        "   \n"
        "   **Seasonality**:\n"
        "   - Pattern: [Recurring cycles]\n"
        "   - Frequency: [How often repeats]\n"
        "   - Amplitude: [How much variation]\n"
        "   \n"
        "   **Clusters**:\n"
        "   - Group 1: [Similar data points]\n"
        "   - Group 2: [Another cluster]\n"
        "   - Characteristics: [What defines each]"
    ),
    "anomaly_detection": (
        "4. **ANOMALY DETECTION**\n"
        "   Outliers and unusual patterns:\n"
        "   \n"
        "   - Anomaly 1: [What's unusual]\n"
        "     - Context: [When/where]\n"
        "     - Severity: [How far from normal]\n"
        "     - Possible cause: [Why it might occur]\n"
        "   \n"
        "   - Anomaly 2: [Another outlier]\n"
        "     - [Same structure]"
    ),
    "correlation_analysis": (
        "5. **CORRELATION ANALYSIS**\n"
        "   Relationships between variables:\n"
        "   \n"
        "   - Correlation 1: [X relates to Y]\n"
        "     - Strength: [Strong/moderate/weak]\n"
        "     - Direction: [Positive/negative]\n"
        "     - Note: [Correlation ≠ causation]\n"
        "   \n"
        "   - Correlation 2: [Another relationship]"
    ),
    "comparative_analysis": (
        "6. **COMPARATIVE ANALYSIS**\n"
        "   How do segments compare?\n"
        "   \n"
        "   | Segment | Metric A | Metric B | Insight |\n"
        "   |---------|----------|----------|--------|\n"
        "   | Seg 1 | [Value] | [Value] | [Finding] |\n"
        "   | Seg 2 | [Value] | [Value] | [Finding] |\n"
        "   \n"
        "   Key differences:\n"
        "   - [Segment X outperforms on Y]\n"
        "   - [Segment A lags in B]"
    ),
    "key_insights": (
        "7. **KEY INSIGHTS**\n"
        "   \n"
        "   **Insight #1**: [Major finding]\n"
        "   - Evidence: [What supports this]\n"
        "   - Confidence: [High/Medium/Low]\n"
        "   - Significance: [Why it matters]\n"
        "   - Action: [What to do about it]\n"
        "   \n"
        "   **Insight #2**: [Another finding]\n"
        "   - Evidence: [Supporting data]\n"
        "   - Confidence: [Level]\n"
        "   - Significance: [Impact]\n"
        "   - Action: [Recommended response]\n"
        "   \n"
        "   **Insight #3**: [Third finding]\n"
        "   - [Same structure]"
    ),
    "hypotheses": (
        "8. **HYPOTHESES**\n"
        "   Possible explanations:\n"
        "   \n"
        "   - Hypothesis 1: [Explanation for pattern]\n"
        "     - Supporting evidence: [What fits]\n"
        "     - Contradicting evidence: [What doesn't]\n"
        "     - Test: [How to verify]\n"
        "   \n"
        "   - Hypothesis 2: [Alternative explanation]"
    ),
    "data_limitations": (
        "9. **DATA LIMITATIONS**\n"
        "   What to be cautious about:\n"
        "   - Limitation 1: [Data gap or issue]\n"
        "   - Limitation 2: [Bias or constraint]\n"
        "   - Limitation 3: [Missing information]\n"
        "   \n"
        "   Confidence caveats:\n"
        "   - [What we can't conclude from this data]"
    ),
    "recommendations": (
        "10. **RECOMMENDATIONS**\n"
        "    Based on analysis:\n"
        "    \n"
        "    **Immediate Actions**:\n"
        "    1. [Action based on insight 1]\n"
        "    2. [Action based on insight 2]\n"
        "    \n"
        "    **Further Investigation**:\n"
        "    - [What additional data needed]\n"
        "    - [What analysis to run next]\n"
        "    \n"
        "    **Success Metrics**:\n"
        "    - [How to measure if actions work]"
    ),
    "visualization_suggestions": (
        "11. **VISUALIZATION SUGGESTIONS**\n"
        "    Best ways to present findings:\n"
        "    - Chart 1: [Type] for [Data]\n"
        "    - Chart 2: [Type] for [Pattern]\n"
        "    - Dashboard: [Key metrics to track]"
    ),
}

_ALL_SECTION_IDS = list(_SECTION_BLOCKS.keys())

_INTENT_SECTIONS: dict[str, list[str] | None] = {
    "executive": [
        "data_overview", "key_insights",
        "visualization_suggestions", "recommendations",
    ],
    "analyst": [
        "data_overview", "descriptive_statistics",
        "pattern_detection", "correlation_analysis",
    ],
    "operations": [
        "data_overview", "anomaly_detection", "recommendations",
    ],
    "summary": [
        "data_overview", "key_insights", "recommendations",
    ],
    "comprehensive": None,
}

_INVESTMENT_CONFIG: dict[str, dict[str, Any]] = {
    "quick": {
        "constraint": (
            "Be concise. Maximum 3 key insights. Use brief bullet points. "
            "Omit lengthy elaboration."
        ),
        "max_tokens_hint": 1500,
    },
    "standard": {
        "constraint": "",
        "max_tokens_hint": 3000,
    },
    "thorough": {
        "constraint": (
            "Be comprehensive. Include full evidence, detailed reasoning, "
            "and thorough analysis for every section."
        ),
        "max_tokens_hint": 5000,
    },
}

VALID_INTENTS = set(_INTENT_SECTIONS.keys())
VALID_INVESTMENTS = set(_INVESTMENT_CONFIG.keys())


class DataAnalyzer(Pattern):
    """
    Analyze data systematically and extract insights.

    Supports two new parameters:

    * **intent** — controls *which* sections are produced:
      ``"executive"`` | ``"analyst"`` | ``"operations"`` | ``"summary"``
      | ``"comprehensive"`` (default, all 11 sections).

    * **investment** — controls *depth / token budget*:
      ``"quick"`` | ``"standard"`` (default) | ``"thorough"``.

    Backward compatible: omitting both gives the original full report.

    Example:
        >>> analyzer = DataAnalyzer()
        >>> # Full report (original behaviour)
        >>> ctx = analyzer.build_context(
        ...     data_description="Monthly sales data",
        ...     goal="Identify growth opportunities",
        ... )
        >>>
        >>> # Executive summary
        >>> ctx = analyzer.build_context(
        ...     data_description="Monthly sales data",
        ...     goal="Key takeaways for leadership",
        ...     intent="executive",
        ...     investment="quick",
        ... )
        >>>
        >>> # Analyst deep-dive on correlations
        >>> result = analyzer.execute(
        ...     data_description="Monthly sales data",
        ...     goal="Variable relationships",
        ...     intent="analyst",
        ...     investment="thorough",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    INTENTS: ClassVar[dict[str, list[str] | None]] = _INTENT_SECTIONS
    INVESTMENTS: ClassVar[dict[str, dict[str, Any]]] = _INVESTMENT_CONFIG
    SECTION_BLOCKS: ClassVar[dict[str, str]] = _SECTION_BLOCKS

    GENERIC_PROMPT = (
        "You are an expert data analyst. Analyze the following data and extract "
        "actionable insights:\n\n"
        "Data: {data_description}\n"
        "{context_section}\n"
        "Goal: {goal}\n\n"
        "Apply a structured analytical approach: "
        "(1) Summarize the data — type, scope, variables, and quality. "
        "(2) Identify patterns including trends, seasonality, and clusters with "
        "supporting evidence. "
        "(3) Detect anomalies and outliers, noting severity and possible causes. "
        "(4) Examine correlations between variables, distinguishing correlation from "
        "causation. "
        "(5) Compare segments and highlight key differences. "
        "(6) Synthesize 3-5 key insights ranked by confidence and significance, each "
        "with a recommended action. "
        "(7) Note data limitations and confidence caveats. "
        "(8) Provide immediate action recommendations and areas for further investigation.\n\n"
        "Be analytical, evidence-based, and actionable."
    )

    _FULL_DIRECTIVE_TEMPLATE: ClassVar[str] = (
        "Analyze this data:\n\n"
        "**DATA**: {data_description}\n\n"
        "{context_section}\n\n"
        "**ANALYSIS GOAL**: {goal}\n\n"
        "Systematic data analysis:\n\n"
        + "\n\n".join(_SECTION_BLOCKS[sid] for sid in _ALL_SECTION_IDS)
        + "\n\n**OUTPUT FORMAT**: Clear, evidence-based analysis with actionable insights."
    )

    def __init__(self):
        super().__init__(
            name="data_analyzer",
            description="Systematic data analysis",
            guidance=Guidance(
                role="Expert Data Analyst and Insights Specialist",
                rules=[
                    "Start with descriptive understanding",
                    "Look for patterns and anomalies",
                    "Distinguish correlation from causation",
                    "Provide actionable insights",
                    "Acknowledge data limitations",
                ],
                style="analytical, evidence-based, clear",
            ),
            directive_template=self._FULL_DIRECTIVE_TEMPLATE,
            input_schema={
                "data_description": str,
                "context_section": str,
                "goal": str,
            },
            constraints=Constraints(
                must_include=["patterns", "insights", "recommendations"],
                style_guide="Be analytical but accessible, rigorous but clear",
            ),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _render_context_section(context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    @classmethod
    def _build_intent_directive(
        cls,
        data_description: str,
        goal: str,
        context_section: str,
        intent: str,
        investment: str,
    ) -> str:
        """Assemble a directive containing only the sections for *intent*."""
        section_ids = cls.INTENTS.get(intent) or _ALL_SECTION_IDS
        blocks = [cls.SECTION_BLOCKS[sid] for sid in section_ids]
        body = "\n\n".join(blocks)

        inv = cls.INVESTMENTS.get(investment, cls.INVESTMENTS["standard"])
        constraint_line = ""
        if inv["constraint"]:
            constraint_line = f"\n**CONSTRAINTS**: {inv['constraint']}"

        return (
            f"Analyze this data:\n\n"
            f"**DATA**: {data_description}\n\n"
            f"{context_section}\n\n"
            f"**ANALYSIS GOAL**: {goal}\n\n"
            f"Produce ONLY these sections (in order):\n\n"
            f"{body}"
            f"{constraint_line}\n\n"
            f"**OUTPUT FORMAT**: Clear, evidence-based, actionable."
        )

    @staticmethod
    def _validate_intent_investment(intent: str, investment: str) -> None:
        if intent not in VALID_INTENTS:
            raise ValueError(
                f"Invalid intent {intent!r}. Choose from: {sorted(VALID_INTENTS)}"
            )
        if investment not in VALID_INVESTMENTS:
            raise ValueError(
                f"Invalid investment {investment!r}. Choose from: {sorted(VALID_INVESTMENTS)}"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_context(
        self,
        data_description: str = "",
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        **kwargs,
    ):
        """Build a Context for this analysis.

        Parameters
        ----------
        data_description : str
            Description of the data to analyze.
        goal : str
            What the analysis should achieve.
        context : str, optional
            Extra context (domain knowledge, constraints, etc.).
        intent : str
            Report type: ``"executive"`` | ``"analyst"`` | ``"operations"``
            | ``"summary"`` | ``"comprehensive"`` (default).
        investment : str
            Depth level: ``"quick"`` | ``"standard"`` (default) | ``"thorough"``.
        """
        self._validate_intent_investment(intent, investment)
        context_section = self._render_context_section(context)

        if intent == "comprehensive" and investment == "standard":
            ctx = super().build_context(
                data_description=data_description,
                goal=goal,
                context_section=context_section,
                **kwargs,
            )
            ctx.metadata["intent"] = intent
            ctx.metadata["investment"] = investment
            return ctx

        from mycontext.core import Context

        directive_content = self._build_intent_directive(
            data_description, goal, context_section, intent, investment,
        )

        constraints = self.constraints
        if investment == "comprehensive" or intent == "comprehensive":
            pass
        else:
            inv = self.INVESTMENTS.get(investment, self.INVESTMENTS["standard"])
            if inv["constraint"]:
                constraints = Constraints(
                    must_include=["insights"],
                    style_guide=inv["constraint"],
                )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=constraints,
            data={
                "data_description": data_description,
                "goal": goal,
                "context_section": context_section,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["intent"] = intent
        ctx.metadata["investment"] = investment
        return ctx

    def execute(
        self,
        provider: str = "openai",
        data_description: str = "",
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        **kwargs,
    ):
        """Execute the analysis and return provider response.

        Accepts the same parameters as :meth:`build_context` plus
        provider kwargs (``model``, ``temperature``, ``max_tokens``, etc.).
        """
        self._validate_intent_investment(intent, investment)

        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        template_kwargs = {k: v for k, v in kwargs.items() if k not in provider_params}

        if "max_tokens" not in provider_kwargs:
            hint = self.INVESTMENTS.get(investment, {}).get("max_tokens_hint")
            if hint and intent != "comprehensive":
                provider_kwargs["max_tokens"] = hint

        ctx = self.build_context(
            data_description=data_description,
            goal=goal,
            context=context,
            intent=intent,
            investment=investment,
            **template_kwargs,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
