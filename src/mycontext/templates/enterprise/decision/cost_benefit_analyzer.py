"""
Cost Benefit Analyzer (Enterprise) - Systematic cost-benefit analysis

Comprehensive cost-benefit analysis with ROI calculation.
Based on economic analysis and decision theory.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class CostBenefitAnalyzer(Pattern):
    """
    Conduct systematic cost-benefit analysis.

    Analyzes:
    - All costs (direct, indirect, opportunity)
    - All benefits (tangible, intangible)
    - ROI and payback period
    - Break-even analysis
    - Risk-adjusted returns

    Based on: Economic analysis and cost-benefit frameworks

    Example:
        >>> analyzer = CostBenefitAnalyzer()
        >>> context = analyzer.build_context(
        ...     decision="Migrate to cloud infrastructure",
        ...     timeframe="3 years"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert financial analyst specializing in cost-benefit evaluation. "
        "Conduct a thorough cost-benefit analysis of the proposed decision.\n\n"
        "Decision: {decision}\n"
        "Timeframe: {timeframe}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Direct costs, indirect costs, and opportunity costs — quantify each.\n"
        "(2) Tangible and intangible benefits with estimated monetary values.\n"
        "(3) ROI calculation and payback period.\n"
        "(4) Break-even analysis showing when benefits outweigh costs.\n"
        "(5) Sensitivity analysis — best, base, and worst case scenarios.\n"
        "(6) Go/No-Go recommendation with clear rationale and conditions.\n\n"
        "Be rigorous and quantitative. Include all visible and hidden costs.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="cost_benefit_analyzer",
            description="Cost-benefit analysis",
            version="1.0.0",
            tags=["decision", "enterprise", "finance", "roi"],
            metadata={"category": "decision", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Financial Analyst and Economic Evaluation Specialist",
                rules=[
                    "Include all costs (visible and hidden)",
                    "Quantify benefits where possible",
                    "Consider time value of money",
                    "Include intangibles",
                    "Calculate ROI and payback",
                ],
                style="rigorous, quantitative, balanced",
            ),
            directive_template="""Conduct cost-benefit analysis:

**DECISION**: {decision}

{context_section}

**TIMEFRAME**: {timeframe}

Cost-benefit analysis:

1. **DECISION OVERVIEW**
   - What: [Description]
   - Investment: [Initial cost]
   - Timeline: [Duration]

2. **COST ANALYSIS**
   **Direct Costs**:
   - [Cost 1]: $[Amount]
   - [Cost 2]: $[Amount]
   
   **Indirect Costs**:
   - [Hidden cost 1]: $[Amount]
   - [Hidden cost 2]: $[Amount]
   
   **Opportunity Costs**:
   - [What we give up]: $[Value]
   
   **Total Costs**: $[Sum]

3. **BENEFIT ANALYSIS**
   **Tangible Benefits**:
   - [Benefit 1]: $[Value]
   - [Benefit 2]: $[Value]
   
   **Intangible Benefits**:
   - [Benefit A]: [Estimated value]
   - [Benefit B]: [Estimated value]
   
   **Total Benefits**: $[Sum]

4. **ROI CALCULATION**
   - Total Benefits: $[Amount]
   - Total Costs: $[Amount]
   - Net Benefit: $[Difference]
   - ROI: [Percentage]
   - Payback Period: [Months]

5. **BREAK-EVEN ANALYSIS**
   - Break-even point: [When]
   - Monthly cost: $[Amount]
   - Monthly benefit: $[Amount]

6. **SENSITIVITY ANALYSIS**
   - Best case: [ROI if optimistic]
   - Base case: [Expected ROI]
   - Worst case: [ROI if pessimistic]

7. **RECOMMENDATION**
   - Decision: [Go/No-Go]
   - Rationale: [Why]
   - Conditions: [If any]

**OUTPUT FORMAT**: Quantitative cost-benefit analysis with clear recommendation.""",
            input_schema={"decision": str, "context_section": str, "timeframe": str},
            constraints=Constraints(
                must_include=["costs", "benefits", "roi", "recommendation"],
                style_guide="Be quantitative and rigorous",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self, decision: str = "", timeframe: str = "1 year", context: str | None = None, **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            decision=decision, timeframe=timeframe, context_section=context_section, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        decision: str = "",
        timeframe: str = "1 year",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(
            provider=provider, decision=decision, timeframe=timeframe, context=context, **kwargs
        )
