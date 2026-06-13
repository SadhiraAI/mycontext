"""
Comparative Analyzer Template (Enterprise) - Compare multiple options systematically

Structured comparison framework for evaluating alternatives.

License: Enterprise
"""

from mycontext import Guidance, Pattern


class ComparativeAnalyzer(Pattern):
    """
    Systematic comparison template for evaluating multiple options.

    Provides structured analysis across multiple dimensions:
    - Criteria-based evaluation
    - Pros and cons analysis
    - Side-by-side comparison
    - Context-aware recommendations

    Based on: Multi-criteria decision analysis frameworks

    Example:
        ```python
        from mycontext.templates.enterprise.decision import ComparativeAnalyzer

        analyzer = ComparativeAnalyzer()
        context = analyzer.build_context(
            options=["Option A", "Option B", "Option C"],
            criteria="cost, performance, ease of use",
            depth="comprehensive"
        )
        ```

    Input Schema:
        - options (str or list): Options to compare (comma-separated or list)
        - criteria (str, optional): Comparison criteria
        - context_section (str, optional): Additional context
        - depth (str): Level of analysis ("basic", "detailed", "comprehensive")
    """

    GENERIC_PROMPT = (
        "You are an expert decision analyst specializing in systematic comparison of alternatives. "
        "Evaluate the given options using structured multi-criteria analysis.\n\n"
        "Options: {options}\n"
        "Criteria: {criteria}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Deliver your analysis:\n"
        "(1) Overview of each option with key distinguishing features.\n"
        "(2) Criteria-based evaluation — rate each option with evidence and justification.\n"
        "(3) Pros and cons for every option.\n"
        "(4) Scenario analysis — which option wins under different priority weightings.\n"
        "(5) Summary comparison matrix.\n"
        "(6) Clear recommendation with reasoning, alternatives, and key decision factors.\n\n"
        "Be objective, balanced, and actionable. Quantify where possible.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="comparative_analyzer",
            description="Compare multiple options using structured analysis",
            version="1.0.0",
            tags=["decision", "enterprise", "comparison", "analysis"],
            metadata={"category": "decision", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Decision Analyst and Strategic Advisor",
                rules=[
                    "Be objective and balanced in comparisons",
                    "Use clear, structured comparison frameworks",
                    "Consider both quantitative and qualitative factors",
                    "Identify trade-offs explicitly",
                    "Provide evidence-based assessments",
                    "Consider context and constraints",
                    "Be clear about uncertainties and assumptions",
                ],
                style="analytical, balanced, systematic",
            ),
            directive_template="""Conduct a systematic comparison of these options:

{options_formatted}

{context_section}

{criteria_section}

Depth of analysis: {depth}

Comparison Framework:

1. OVERVIEW
   - Brief description of each option
   - Key distinguishing features

2. DETAILED COMPARISON
   For each criterion:
   - Rate each option (High/Medium/Low or 1-10 scale)
   - Explain the rating with evidence
   - Note any trade-offs

3. PROS AND CONS
   For each option:
   ✅ Strengths/Advantages
   ❌ Weaknesses/Disadvantages

4. SCENARIOS
   - Best option if [criterion X] is most important
   - Best option if [criterion Y] is most important
   - Balanced recommendation

5. DECISION MATRIX
   Create a summary comparison table

6. RECOMMENDATION
   - Primary recommendation with reasoning
   - Alternative options and when they'd be better
   - Key factors that should influence the choice

Be specific, evidence-based, and actionable.""",
            input_schema={
                "options_formatted": str,
                "context_section": str,
                "criteria_section": str,
                "depth": str,
            },
        )

    def _format_options(self, options) -> str:
        """Format options for template"""
        if isinstance(options, str):
            # If comma-separated string, split it
            options = [opt.strip() for opt in options.split(",")]

        formatted = "OPTIONS TO COMPARE:\n"
        for i, opt in enumerate(options, 1):
            formatted += f"{i}. {opt}\n"
        return formatted

    def _render_context_section(self, context: str) -> str:
        """Render the context section"""
        if not context or context.strip() == "":
            return ""
        return f"CONTEXT:\n{context}\n"

    def _render_criteria_section(self, criteria: str) -> str:
        """Render comparison criteria"""
        if not criteria or criteria.strip() == "":
            return "Use standard comparison criteria appropriate for these options."
        return f"COMPARISON CRITERIA:\n{criteria}\n"

    def build_context(
        self, options, criteria: str = "", context: str = "", depth: str = "detailed", **kwargs
    ):
        """
        Build a context for comparative analysis.

        Args:
            options: List of options or comma-separated string
            criteria: Comparison criteria (comma-separated)
            context: Optional additional context
            depth: Level of analysis
            **kwargs: Additional parameters

        Returns:
            Context configured for comparison
        """
        options_formatted = self._format_options(options)
        context_section = self._render_context_section(context or "")
        criteria_section = self._render_criteria_section(criteria or "")

        # Clean up kwargs
        kwargs.pop("context", None)
        kwargs.pop("context_section", None)
        kwargs.pop("criteria_section", None)
        kwargs.pop("options_formatted", None)

        return super().build_context(
            options_formatted=options_formatted,
            context_section=context_section,
            criteria_section=criteria_section,
            depth=depth,
            **kwargs,
        )

    def execute(
        self,
        provider: str = "openai",
        options=None,
        criteria: str = "",
        context: str = "",
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Execute comparative analysis directly.

        Args:
            provider: LLM provider to use
            options: Options to compare
            criteria: Comparison criteria
            context: Additional context
            depth: Analysis depth
            **kwargs: Provider parameters

        Returns:
            Provider response with comparative analysis
        """
        options_formatted = self._format_options(options or [])
        context_section = self._render_context_section(context or "")
        criteria_section = self._render_criteria_section(criteria or "")

        # Separate provider kwargs
        provider_params = {}
        provider_param_names = {
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

        for key in list(kwargs.keys()):
            if key in provider_param_names:
                provider_params[key] = kwargs.pop(key)

        # Clean up
        kwargs.pop("context", None)
        kwargs.pop("context_section", None)
        kwargs.pop("criteria_section", None)
        kwargs.pop("options_formatted", None)

        return super().execute(
            provider=provider,
            options_formatted=options_formatted,
            context_section=context_section,
            criteria_section=criteria_section,
            depth=depth,
            **provider_params,
        )
