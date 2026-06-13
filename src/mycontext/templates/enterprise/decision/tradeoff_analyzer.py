"""
Tradeoff Analyzer Template (Enterprise) - Analyze competing priorities and tradeoffs

Structured analysis of competing objectives and constraints.

License: Enterprise
"""

from mycontext import Guidance, Pattern


class TradeoffAnalyzer(Pattern):
    """
    Tradeoff analysis template for examining competing priorities.

    Analyzes situations where:
    - Multiple objectives conflict
    - Resources are constrained
    - Choices have opportunity costs
    - Optimization requires balance

    Based on: Multi-objective optimization and decision theory

    Example:
        ```python
        from mycontext.templates.enterprise.decision import TradeoffAnalyzer

        analyzer = TradeoffAnalyzer()
        context = analyzer.build_context(
            situation="Choosing between speed, quality, and cost",
            objectives="fast delivery, high quality, low cost",
            depth="comprehensive"
        )
        ```

    Input Schema:
        - situation (str): The decision situation with tradeoffs
        - objectives (str, optional): Competing objectives
        - context_section (str, optional): Additional context
        - depth (str): Analysis depth ("basic", "detailed", "comprehensive")
    """

    GENERIC_PROMPT = (
        "You are an expert decision analyst specializing in trade-off evaluation and optimization. "
        "Analyze the competing priorities in the given situation.\n\n"
        "Situation: {situation}\n"
        "Objectives: {objectives}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Deliver your analysis:\n"
        "(1) Identify all competing objectives and why each matters.\n"
        "(2) Map trade-off relationships — how does improving one affect others?\n"
        "(3) Analyze constraints (hard, soft, resource, time, budget).\n"
        "(4) Explore scenarios: maximize each objective separately, then find balanced approaches.\n"
        "(5) Pareto analysis — which solutions dominate, where are the sweet spots?\n"
        "(6) Quantify opportunity costs and recommend an optimization strategy.\n\n"
        "Be realistic about limits. Propose creative solutions that reduce trade-offs where possible.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="tradeoff_analyzer",
            description="Analyze competing priorities and tradeoffs",
            version="1.0.0",
            tags=["decision", "enterprise", "tradeoff", "optimization"],
            metadata={"category": "decision", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Decision Analyst and Strategic Optimization Specialist",
                rules=[
                    "Identify all competing objectives clearly",
                    "Quantify tradeoffs where possible",
                    "Consider opportunity costs explicitly",
                    "Examine constraints and boundaries",
                    "Explore Pareto optimal solutions",
                    "Consider different stakeholder priorities",
                    "Be realistic about what can be optimized simultaneously",
                    "Propose balanced compromises",
                ],
                style="analytical, balanced, pragmatic",
            ),
            directive_template="""Analyze the tradeoffs in this situation:

"{situation}"

{objectives_section}

{context_section}

Analysis depth: {depth}

Tradeoff Analysis Framework:

1. SITUATION CLARIFICATION
   - What decision needs to be made?
   - What's at stake?
   - Who are the stakeholders?
   - What are the constraints?

2. COMPETING OBJECTIVES
   Identify and define each objective:
   - Objective 1: [Description, why it matters]
   - Objective 2: [Description, why it matters]
   - Objective 3: [Description, why it matters]
   [Continue as needed]

3. TRADEOFF RELATIONSHIPS
   For each pair of objectives:
   - How do they conflict?
   - Can both be partially achieved?
   - What's the exchange rate? (e.g., 10% more X = 5% less Y)
   - Are there thresholds or breaking points?

4. CONSTRAINT ANALYSIS
   - Hard constraints (cannot be violated)
   - Soft constraints (preferences)
   - Resource limitations
   - Time constraints
   - Budget constraints

5. SCENARIOS
   Explore different optimization strategies:
   
   a) Maximize Objective A
      - What happens to other objectives?
      - Overall outcome
      - Stakeholders helped/hurt
   
   b) Maximize Objective B
      - What happens to other objectives?
      - Overall outcome
      - Stakeholders helped/hurt
   
   c) Balanced Approach
      - How to optimize across objectives?
      - Compromise points
      - Overall outcome

6. PARETO ANALYSIS
   - What solutions dominate others? (Better on all metrics)
   - What's the Pareto frontier? (Can't improve one without hurting another)
   - Sweet spots where multiple objectives align

7. OPPORTUNITY COSTS
   For each major choice:
   - What are you giving up?
   - What's the value of the next best alternative?
   - Are the tradeoffs worth it?

8. PHASING AND SEQUENCING
   - Can objectives be pursued sequentially?
   - Can you optimize for different objectives in different phases?
   - How do priorities change over time?

9. CREATIVE SOLUTIONS
   - Are there ways to reduce the tradeoff?
   - Can technology/innovation help?
   - Are there synergies to exploit?
   - Can constraints be relaxed?

10. RECOMMENDATION
    - Recommended optimization strategy
    - Why this balance is appropriate
    - What you're sacrificing and why it's acceptable
    - Conditions that would warrant a different approach
    - How to monitor and adjust

Use specific examples, quantify where possible, and be realistic about limits.""",
            input_schema={
                "situation": str,
                "objectives_section": str,
                "context_section": str,
                "depth": str,
            },
        )

    def _render_objectives_section(self, objectives: str) -> str:
        """Render the objectives section"""
        if not objectives or objectives.strip() == "":
            return ""
        return f"\nCompeting Objectives:\n{objectives}\n"

    def _render_context_section(self, context: str) -> str:
        """Render the context section"""
        if not context or context.strip() == "":
            return ""
        return f"\nAdditional Context:\n{context}\n"

    def build_context(
        self,
        situation: str,
        objectives: str = "",
        context: str = "",
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Build a context for tradeoff analysis.

        Args:
            situation: The decision situation with tradeoffs
            objectives: Competing objectives (comma-separated)
            context: Optional additional context
            depth: Analysis depth
            **kwargs: Additional parameters

        Returns:
            Context configured for tradeoff analysis
        """
        objectives_section = self._render_objectives_section(objectives or "")
        context_section = self._render_context_section(context or "")

        # Clean up kwargs
        kwargs.pop("context", None)
        kwargs.pop("context_section", None)
        kwargs.pop("objectives_section", None)

        return super().build_context(
            situation=situation,
            objectives_section=objectives_section,
            context_section=context_section,
            depth=depth,
            **kwargs,
        )

    def execute(
        self,
        provider: str = "openai",
        situation: str = None,
        objectives: str = "",
        context: str = "",
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Execute tradeoff analysis directly.

        Args:
            provider: LLM provider to use
            situation: The situation to analyze
            objectives: Competing objectives
            context: Additional context
            depth: Analysis depth
            **kwargs: Provider parameters

        Returns:
            Provider response with tradeoff analysis
        """
        objectives_section = self._render_objectives_section(objectives or "")
        context_section = self._render_context_section(context or "")

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
        kwargs.pop("objectives_section", None)

        return super().execute(
            provider=provider,
            situation=situation,
            objectives_section=objectives_section,
            context_section=context_section,
            depth=depth,
            **provider_params,
        )
